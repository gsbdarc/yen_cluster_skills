#!/usr/bin/env python3
"""Structural checks for the skills in this repo. CI runs this on every push and PR.

    scripts/validate.py            # exit 1 on any error; warnings never fail

Errors:
  * every skills/<name>/ has SKILL.md, EXAMPLE.md, manifest.yaml
  * SKILL.md frontmatter follows the Agent Skills spec: name matches the folder,
    description <= 1024 chars, compatibility <= 500 chars, metadata is string->string
  * manifest.yaml has author, created (YYYY-MM-DD), summary, requires.plugins,
    requires.secrets; secrets is [] (end-user skills read no credential files)
  * nothing shaped like an API key, token, or private key anywhere in skills/ or templates/
  * both .claude/skills/ and .agents/skills/ link every skill, and nothing else
  * every skill has a row in the README "Included skills" table
  * .claude-plugin/marketplace.json, if present: each plugin has a valid name and a
    description, uses source "./skills" with strict false, lists only existing skills
    as "./<name>", shares no skill with another plugin, and is named in README.md;
    no plugin.json at the repo root or under skills/ (it would conflict)
Warnings:
  * a personal absolute path (/home/users/<sunet>) in SKILL.md
"""
import datetime as dt
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required. On the Yens: /opt/jupyterhub/bin/python3 has it; "
             "elsewhere: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
TEMPLATES_DIR = ROOT / "templates"
LINK_DIRS = [ROOT / ".claude" / "skills", ROOT / ".agents" / "skills"]
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PERSONAL_PATH_RE = re.compile(r"(?:/yen)?/home/users/[a-z0-9]+")

# Strings that look like secret values. Any match is an error.
SECRET_VALUE_PATTERNS = {
    "Airtable personal access token": re.compile(r"\bpat[A-Za-z0-9]{14}\.[0-9a-f]{64}\b"),
    "Airtable legacy API key": re.compile(r"\bkey[A-Za-z0-9]{14}\b"),
    "AWS access key id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


class Skill:
    def __init__(self, path):
        self.path = path
        self.name = path.name
        self.frontmatter = {}
        self.manifest = {}
        self.errors = []
        self.warnings = []

    def err(self, msg):
        self.errors.append(f"{self.name}: {msg}")

    def warn(self, msg):
        self.warnings.append(f"{self.name}: {msg}")


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with a '---' frontmatter block")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter block is not closed with '---'")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML map")
    return data


def load_skill(path):
    s = Skill(path)
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        s.err("missing SKILL.md")
        return s
    text = skill_md.read_text(encoding="utf-8")

    try:
        s.frontmatter = parse_frontmatter(text)
    except ValueError as e:
        s.err(str(e))
    else:
        check_frontmatter(s)

    for required in ("EXAMPLE.md", "manifest.yaml"):
        if not (path / required).is_file():
            s.err(f"missing {required}")

    if (path / "manifest.yaml").is_file():
        try:
            s.manifest = yaml.safe_load((path / "manifest.yaml").read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            s.err(f"manifest.yaml does not parse: {e}")
        else:
            check_manifest(s)

    for m in PERSONAL_PATH_RE.findall(text):
        s.warn(f"personal absolute path in SKILL.md: {m}")
    return s


def check_frontmatter(s):
    fm = s.frontmatter
    name = fm.get("name")
    if not isinstance(name, str) or not name:
        s.err("frontmatter needs a non-empty 'name'")
    else:
        if name != s.name:
            s.err(f"frontmatter name '{name}' does not match folder name")
        if len(name) > 64 or not NAME_RE.match(name):
            s.err("name must be 1-64 chars of lowercase letters, digits, and single hyphens")
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        s.err("frontmatter needs a non-empty 'description'")
    elif len(desc) > 1024:
        s.err(f"description is {len(desc)} chars; max 1024")
    compat = fm.get("compatibility")
    if compat is not None and (not isinstance(compat, str) or not 1 <= len(compat) <= 500):
        s.err("compatibility must be a string of 1-500 chars")
    meta = fm.get("metadata")
    if meta is not None:
        if not isinstance(meta, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in meta.items()):
            s.err("metadata must be a map of string keys to string values")


def check_manifest(s):
    m = s.manifest
    if not isinstance(m, dict):
        s.err("manifest.yaml must be a YAML map")
        s.manifest = {}
        return
    if not isinstance(m.get("author"), str) or not m["author"].strip():
        s.err("manifest.yaml: author must be the GitHub handle of whoever made the skill")
    created = m.get("created")
    if isinstance(created, dt.datetime):
        created = created.date()
    if not isinstance(created, dt.date):
        try:
            dt.date.fromisoformat(str(created))
        except ValueError:
            s.err("manifest.yaml: created must be a date, YYYY-MM-DD")
    if not isinstance(m.get("summary"), str) or not m["summary"].strip():
        s.err("manifest.yaml: summary must be one or two sentences on what the skill does")

    rq = m.get("requires")
    if not isinstance(rq, dict):
        s.err("manifest.yaml: requires block is required (plugins: [], secrets: [])")
        return
    for key in ("plugins", "secrets"):
        val = rq.get(key)
        if not isinstance(val, list) or not all(isinstance(x, str) and x.strip() for x in val):
            s.err(f"manifest.yaml: requires.{key} must be a list of names (use [] for none)")
    if rq.get("secrets"):
        s.err("manifest.yaml: requires.secrets must be []; end-user skills read no credential files. "
              "Auth goes through a connector (requires.plugins) or the user's own login")


def load_all():
    skills = []
    if not SKILLS_DIR.is_dir():
        sys.exit("no skills/ directory found")
    for path in sorted(SKILLS_DIR.iterdir()):
        if path.is_dir() and not path.name.startswith((".", "_")):
            skills.append(load_skill(path))
    return skills


def check_links(skills):
    """Both agent directories must link every skill and nothing else."""
    errors = []
    names = {s.name for s in skills}
    for link_dir in LINK_DIRS:
        rel = link_dir.relative_to(ROOT).as_posix()
        if not link_dir.is_dir():
            errors.append(f"{rel}/ is missing")
            continue
        present = set()
        for entry in sorted(link_dir.iterdir()):
            present.add(entry.name)
            if not entry.is_symlink():
                errors.append(f"{rel}/{entry.name} is not a symlink; skills live in skills/ and are linked from here")
                continue
            target = (link_dir / entry.readlink()).resolve()
            expected = (SKILLS_DIR / entry.name).resolve()
            if entry.name not in names:
                errors.append(f"{rel}/{entry.name} links to a skill that does not exist in skills/")
            elif target != expected:
                errors.append(f"{rel}/{entry.name} should link to ../../skills/{entry.name}")
        for missing in sorted(names - present):
            errors.append(f"{rel}/{missing} is missing (ln -s ../../skills/{missing} {rel}/{missing})")
    return errors


def check_secret_values():
    """No file under skills/ or templates/ may contain something shaped like a secret."""
    errors = []
    for base in (SKILLS_DIR, TEMPLATES_DIR):
        if not base.is_dir():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for label, pattern in SECRET_VALUE_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f"{path.relative_to(ROOT).as_posix()}: contains what looks like a {label}; "
                                  f"no secret value belongs in this repo")
                    break
    return errors


def check_readme(skills):
    """Every skill has a row in the README 'Included skills' table (the central index)."""
    readme = ROOT / "README.md"
    if not readme.is_file():
        return ["README.md is missing"]
    text = readme.read_text(encoding="utf-8")
    return [f"README.md: no row links to skills/{s.name}/SKILL.md in the Included skills table"
            for s in skills if f"skills/{s.name}/SKILL.md" not in text]


def check_marketplace(skills):
    """Plugins group skills from skills/ via one marketplace file; see AGENTS.md."""
    errors = []
    for stray in (ROOT / ".claude-plugin" / "plugin.json", SKILLS_DIR / ".claude-plugin" / "plugin.json"):
        if stray.exists():
            errors.append(f"{stray.relative_to(ROOT).as_posix()}: remove it; plugins are defined only in "
                          f".claude-plugin/marketplace.json, and a plugin.json conflicts with strict: false")
    if not MARKETPLACE.is_file():
        return errors
    rel = MARKETPLACE.relative_to(ROOT).as_posix()
    try:
        market = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return errors + [f"{rel} does not parse: {e}"]
    if not isinstance(market, dict):
        return errors + [f"{rel} must be a JSON object"]
    if not isinstance(market.get("name"), str) or not market["name"]:
        errors.append(f"{rel}: needs a 'name'")
    if not isinstance(market.get("owner"), dict) or not market["owner"].get("name"):
        errors.append(f"{rel}: needs 'owner.name'")
    plugins = market.get("plugins")
    if not isinstance(plugins, list):
        return errors + [f"{rel}: needs a 'plugins' list"]

    names = {s.name for s in skills}
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    owner_of = {}
    for i, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            errors.append(f"{rel}: plugins[{i}] must be an object")
            continue
        name = plugin.get("name")
        where = f"{rel}: plugin '{name}'" if isinstance(name, str) else f"{rel}: plugins[{i}]"
        if not isinstance(name, str) or len(name) > 64 or not NAME_RE.match(name):
            errors.append(f"{where}: name must be 1-64 chars of lowercase letters, digits, and single hyphens")
        if not isinstance(plugin.get("description"), str) or not plugin["description"].strip():
            errors.append(f"{where}: needs a description")
        if plugin.get("source") != "./skills":
            errors.append(f'{where}: source must be "./skills" so the plugin reads from the one copy in skills/')
        if plugin.get("strict") is not False:
            errors.append(f"{where}: strict must be false; the marketplace entry is the plugin's manifest")
        listed = plugin.get("skills")
        if not isinstance(listed, list) or not listed:
            errors.append(f'{where}: needs a non-empty skills list, e.g. ["./<skill-name>"]')
            listed = []
        for entry in listed:
            skill = entry[2:] if isinstance(entry, str) and entry.startswith("./") else None
            if skill not in names:
                errors.append(f'{where}: skills entry {entry!r} must be "./<name>" for a folder in skills/')
            elif skill in owner_of:
                errors.append(f"{where}: skill '{skill}' is already in plugin '{owner_of[skill]}'; "
                              f"a skill belongs to at most one plugin")
            else:
                owner_of[skill] = name
        if isinstance(name, str) and f"`{name}`" not in readme:
            errors.append(f"README.md: plugin `{name}` is not mentioned in the Plugins section")
    return errors


def main():
    skills = load_all()
    errors = ([e for s in skills for e in s.errors] + check_links(skills)
              + check_readme(skills) + check_marketplace(skills) + check_secret_values())
    warnings = [w for s in skills for w in s.warnings]
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(skills)} skills, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
