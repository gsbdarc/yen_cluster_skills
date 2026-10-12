---
name: new-skill
description: Scaffold a new skill in the yen_cluster_skills repo from the template — creates skills/<name>/ with SKILL.md, EXAMPLE.md, manifest.yaml and agents/openai.yaml, links it for Claude Code and Codex, adds it to the README and to a plugin if wanted, validates it, then helps the author write the first draft to the repo's conventions. Use when someone wants to add, create, or start a Yen skill — "make a new skill for X", "scaffold a skill called Y", "add a skill to the repo". Do not use to edit an existing skill or to report that a skill did not work.
compatibility: Run from a clone of yen_cluster_skills. Needs git and python3 with PyYAML (/opt/jupyterhub/bin/python3 on the Yens), plus the claude CLI when a plugin changes. Nothing is committed or pushed.
---

# Scaffold a new skill

Creates a skill folder from `templates/skill-template/` and walks the author through the parts that need a human: the description, where it runs, what it needs, which plugin it belongs to, and the procedure. The conventions it applies are the ones in `AGENTS.md`; read that file's "Adding a skill", "Grouping skills into a plugin", "Credentials", and "Rules" sections before writing any content.

Skills in this repo are for Yen end users. A new skill must work for someone with ordinary Yen access: no staff privileges and no credential files. Staff-only skills belong in `darc-staff-skills`.

## Requirements

- You are inside a clone of `yen_cluster_skills` (`git rev-parse --show-toplevel`). If not, ask where the clone is and `cd` there.
- `python3` with PyYAML, for `scripts/validate.py`.
- The `claude` CLI (`ml claude-code` on the Yens), for `claude plugin validate .` when `.claude-plugin/marketplace.json` changes. If it is not available, say so and note the skipped check for the PR.

## Inputs

- **name** — lowercase letters, digits, single hyphens, max 64 chars; `yen-<topic>` like the existing skills (`yen-slurm`, `yen-project-spaces`). Check `ls skills/` for collisions and near-duplicates. Propose a name and confirm it.
- **author** — the author's GitHub handle (`gh api user --jq .login`, or ask).
- **what it does and when to use it** — one or two sentences, plus the phrases a user would actually say, plus what it is *not* for and which existing skill handles that instead.
- **where it runs** — any host, or an active Yen shell; whether it needs network; whether it changes anything (jobs, modules, files, access).
- **what it needs** — host commands or modules, and any MCP servers or connectors ("plugins" in `manifest.yaml`). If the skill seems to need a credential file, stop and raise it with the author: end-user skills authenticate through the user's own login or a connector.
- **plugin** — which plugin in the README "Plugins" table it belongs to (today `yen-basics`, `yen-compute`, or `research-practices`), or none.

## Procedure

1. Agree the name and author, then scaffold from the repo root. Stop if `skills/<name>` already exists.

   ```bash
   cp -r templates/skill-template skills/<name>
   ln -s ../../skills/<name> .claude/skills/<name>
   ln -s ../../skills/<name> .agents/skills/<name>
   ```

   In the copy, replace every `skill-template` with `<name>` in `SKILL.md`, `EXAMPLE.md`, and `agents/openai.yaml`.

2. Interview the author for the inputs above. Do not invent requirements or triggers; ask.

3. Fill `skills/<name>/manifest.yaml`: `author`, `created` (today, `YYYY-MM-DD`), `summary` (one or two sentences), `requires.plugins` (connector names, or `[]`), and `requires.secrets: []`.

4. Write `skills/<name>/SKILL.md`:
   - `description`: what it does, when to use it with the user's own phrases, and a closing "Do not use for …". Under 1024 characters.
   - `compatibility`: host, connectors, tools or modules, and permissions, in one line under 500 characters. Delete the line only if the skill truly needs nothing.
   - Body: a Requirements section the agent can check, Inputs with what to do when something is missing, a numbered Procedure with a confirmation gate before anything that changes the user's jobs, environment, data, or access, an Output section that tells the user how to verify the result, and Rules. Keep the file under 500 lines; long reference material goes in `references/`.
   - Refer to other skills as "the `yen-x` skill", never `$yen-x` or `/yen-x`, so the text reads correctly in Codex, in Claude Code, and inside a plugin.

5. Fill `skills/<name>/agents/openai.yaml` (Codex interface metadata): `display_name` in title case, a `short_description` of a few words, and a `default_prompt` that starts `Use $<name> to`.

6. Add a row for the skill to the "Included skills" table in `README.md`: the name linked to its `SKILL.md` and `EXAMPLE.md`, one line on what it is for, and what it needs to run (a short form of `compatibility`). If it belongs to a plugin, add `./<name>` to that plugin's `skills` list in `.claude-plugin/marketplace.json` and to that plugin's row in the README "Plugins" table. Only create a new plugin if the author asks for one; the rules are in AGENTS.md, under "Grouping skills into a plugin".

7. Run `python3 scripts/validate.py` and fix anything it reports. If `marketplace.json` changed, also run `claude plugin validate .`.

8. Tell the author what happens next: run the skill for real and paste the run into `EXAMPLE.md` (including a request it should not trigger on), then open a PR. Once merged, the skill is live, and plugin users get it on their next plugin update. Anyone it does not work for opens a GitHub issue with the "Skill problem" template.

## Output

A new `skills/<name>/` folder that validates, linked from `.claude/skills/` and `.agents/skills/`, with a filled `manifest.yaml` and `agents/openai.yaml`, a first-draft `SKILL.md` written to the conventions, a row in the README table, and, if chosen, an entry in its plugin. Uncommitted; the author reviews and opens the PR.

## Rules

- Never write a secret's value anywhere: not in the skill, not in the manifest, not in the conversation. End-user skills read no credential files.
- Never hardcode a person or a personal absolute path in the new skill.
- Match the voice and structure of the existing skills in `skills/`; read one before writing.
