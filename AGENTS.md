# yen_cluster_skills — conventions for agents and contributors

This repository is the library of end-user skills for Stanford GSB researchers, covering the Yen computing environment and general research practice, for Claude Code, the claude.ai app, Codex, and ChatGPT. It follows the conventions of [`darc-staff-skills`](https://github.com/gsbdarc/darc-staff-skills), which is the ground truth for how DARC writes skills, with one difference: these skills are for end users. A skill here must work for someone with at most ordinary Yen access, with no staff privileges and no credential files. Staff-only skills belong in `darc-staff-skills`.

This file is read when an agent runs inside this clone. It is for people and agents **editing** the repo. Instructions for **using** a skill live in that skill's own `SKILL.md`, because that is the only file an agent sees when the skill is installed elsewhere.

## Layout

```
skills/<name>/            one folder per skill — the single source of truth
  SKILL.md                agent-facing: frontmatter (name, description, compatibility) + instructions
  EXAMPLE.md              one real, complete run, so readers and agents can see what "working" looks like
  manifest.yaml           who made it, when, what it needs (plugins), one-line summary
  agents/openai.yaml      Codex interface metadata: display name, short description, default prompt
  scripts/ references/ assets/   optional, per the Agent Skills spec
  README.md LICENSE*      optional: a human-facing write-up, and the skill's own license when its text came from elsewhere
.claude/skills/<name>     symlink -> ../../skills/<name>   (Claude Code discovery)
.agents/skills/<name>     symlink -> ../../skills/<name>   (Codex discovery)
.claude-plugin/marketplace.json   plugins: named groups of skills/ folders (see below)
templates/skill-template/ copy this to start a new skill (or run /new-skill)
scripts/validate.py       structural checks; CI runs it on every push and PR
install.sh                link skills into ~/.claude/skills and ~/.agents/skills
```

A skill in `skills/` is live. There is no draft state and no test gate: the README "Included skills" table is the index people and agents browse, and anything that does not work becomes a GitHub issue.

## Adding a skill

The `new-skill` skill does the mechanical steps and walks through the rest; run `/new-skill` inside the clone. By hand:

1. `cp -r templates/skill-template skills/<name>` and replace `skill-template` with `<name>` in `SKILL.md`, `EXAMPLE.md`, and `agents/openai.yaml`. Names are lowercase letters, digits, and single hyphens, max 64 characters; Yen skills start with `yen-`.
2. Write `SKILL.md`. The description says what the skill does, when to use it with phrases a user would say, and ends with what it is **not** for. Put where-it-runs and what-it-needs in `compatibility` (max 500 chars) and in a Requirements section the agent can act on. Keep the file under 500 lines; long reference material goes in `references/`.
3. Fill `manifest.yaml`: `author` (your GitHub handle), `created` (`YYYY-MM-DD`), `summary` (one or two sentences), `requires.plugins` (MCP servers or connectors, or `[]`), `requires.secrets: []`.
4. Fill `agents/openai.yaml`: a title-case `display_name`, a few-word `short_description`, and a `default_prompt` that starts `Use $<name> to`.
5. Record a real run in `EXAMPLE.md`, including a request the skill should *not* trigger on.
6. Link it: `ln -s ../../skills/<name> .claude/skills/<name>` and the same under `.agents/skills/`.
7. Add a row to the "Included skills" table in `README.md`, including what the skill needs to run. The validator fails if a skill has no row. To put it in a plugin, see below.
8. Run `scripts/validate.py` (on the Yens: `/opt/jupyterhub/bin/python3 scripts/validate.py`). Open a PR.

Frontmatter uses Agent Skills spec fields only: `name`, `description`, `compatibility`, and optionally `license` and `allowed-tools`. Team bookkeeping goes in `manifest.yaml`, not in frontmatter `metadata`. Claude Code-only fields are allowed when a skill genuinely needs them, but the skill then cannot claim Codex support.

## Grouping skills into a plugin

A plugin is a named group of skills that installs as one unit in Claude Code and the claude.ai app, invoked as `/<plugin>:<skill>`. The repo root is the plugin marketplace, and `.claude-plugin/marketplace.json` is the only place a plugin is defined. It lists existing `skills/` folders and never copies them:

```json
{
  "name": "yen-compute",
  "description": "What the group is for, in one sentence.",
  "author": { "name": "<github-handle>" },
  "source": "./skills",
  "strict": false,
  "skills": ["./yen-slurm", "./yen-resource-limits"]
}
```

The rules, which the validator enforces:

- `source` is always `"./skills"`, and `strict` is always `false`. The marketplace entry *is* the plugin's manifest.
- Never add a `plugin.json`, whether at the repo root, under `skills/`, or anywhere else. With `strict: false` it makes every plugin fail to load with "conflicting manifests".
- Each `skills` entry is `./<name>` for a folder in `skills/`. A skill belongs to at most one plugin.
- The plugin is named, in backticks, in the README "Plugins" table.
- Leave out `version`. Installs then follow the commit SHA, so a merge to `main` is a release.

To put a skill in a plugin, add `./<name>` to that plugin's `skills` list and to the plugin's row in the README "Plugins" table. The skill still gets its own folder, symlinks, README row and manifest like any other. Do not confuse this with `requires.plugins` in `manifest.yaml`, which lists MCP servers and connectors.

`new-skill` is deliberately in no plugin: it is for contributors working in a clone, not for end users.

Codex and `install.sh`:

- Codex reads this file as a legacy marketplace but doesn't honor the per-entry `skills` list, so Codex users get plugin skills one at a time through `.agents/skills` (`$yen-slurm`).
- For the same reason, `install.sh` skips plugin skills for `~/.claude/skills` on a full run, but still links them for Codex.

Check a plugin change with `claude plugin validate .` as well as `scripts/validate.py`.

## Credentials

End users authenticate themselves, with their SUNet and Duo or by signing in to a connector. The rules:

- No skill reads a credential file. `requires.secrets` is always `[]`; the validator fails otherwise. A skill that needs an external service uses a connector, listed under `requires.plugins`, or the user's own CLI login.
- A skill never asks for, receives, prints, or stores a password, Duo prompt, recovery code, token, or private key.
- No secret value anywhere in this repo: not in `SKILL.md`, not in a script, not in `EXAMPLE.md`, not in an issue. The validator fails a PR that contains anything shaped like an API key, token, or private key.

## When a skill does not work

Open a GitHub issue with the **Skill problem** template: skill, surface (Claude Code, claude.ai, Codex, ChatGPT), agent version, what happened, what `EXAMPLE.md` says should have happened. The `author` in the skill's manifest is who picks it up. From a terminal, `gh issue create` works after `ml gh-cli`.

## Rules that apply to every skill

- Never hardcode a person: identity comes from the session (`whoami`), `git config`, or asking. Never hardcode a personal absolute path.
- Anything that changes the user's jobs, environment, data, or access (`sbatch`, `scancel`, `module load`, a workgroup change) has a confirmation gate and reports how the user can check the result.
- Refer to another skill as "the `yen-x` skill", never `$yen-x` or `/yen-x`, so the text reads correctly in Codex, in Claude Code, and inside a plugin.
- Treat live Yen commands and current cluster policy as authoritative for limits, availability, and membership; `references/` holds the documented values.
- Put context in prose the agent can act on, not in metadata it never reads.
- Edit only what your change needs.

## CI

`.github/workflows/validate.yml` runs `scripts/validate.py` on every push and PR: frontmatter shape and limits, a complete `manifest.yaml` and `EXAMPLE.md` per skill, `requires.secrets` empty, both symlink directories complete, a README row per skill, the plugin rules above, no secret-shaped strings, and a warning for personal absolute paths.

## Agent notes

- Claude Code on the Yens is the Lmod module `claude-code` (`ml claude-code`). Versions below 2.1.277 do not read this file directly; the one-line `CLAUDE.md` imports it so both paths land here.
- Codex on the Yens is the Lmod module `codex`. `gh` is `ml gh-cli`.
- Claude Code invokes skills as `/name`, Codex as `$name`. Plugin skills are `/plugin:name` in Claude Code.
- Inside this clone, anyone who also has a plugin installed sees its skills twice, for example `/yen-slurm` from `.claude/skills/` and `/yen-compute:yen-slurm` from the plugin. That's expected. Edit the copy in `skills/`, which both point to.
