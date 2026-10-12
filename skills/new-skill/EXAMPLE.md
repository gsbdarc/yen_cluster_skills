# Example: new-skill

> **Illustrative walkthrough, not a recorded run.** It shows the intended flow for the "future interactive-work skill" that the `yen-guide` skill mentions. Replace it with the first real run of `/new-skill`.

Scaffolding a skill for persistent interactive sessions with tmux, from inside a clone on a Yen host.

## Input

```text
/new-skill I want a skill that helps people keep long interactive work running with tmux on the Yens
```

## What the agent did

1. Confirmed it was inside the clone (`git rev-parse --show-toplevel`) and listed `skills/` to check for an existing tmux or interactive-session skill.
2. Proposed the name `yen-interactive`, got the author's GitHub handle from `gh api user --jq .login`, and confirmed both.
3. Scaffolded from the template:

   ```bash
   cp -r templates/skill-template skills/yen-interactive
   ln -s ../../skills/yen-interactive .claude/skills/yen-interactive
   ln -s ../../skills/yen-interactive .agents/skills/yen-interactive
   ```

   Replaced `skill-template` with `yen-interactive` in `SKILL.md`, `EXAMPLE.md`, and `agents/openai.yaml`, then filled `manifest.yaml`: `author`, `created`, a two-sentence `summary`, `requires.plugins: []`, `requires.secrets: []`.

4. Interviewed the author: what the skill does (start, detach from, list, and reattach to tmux sessions on a specific interactive Yen), the phrases they would say ("keep my script running after I log out", "reattach to my tmux session on yen3"), what it is not for (scheduled batch work, which belongs to the `yen-slurm` skill), where it runs (an active Yen shell, no network), what it changes (creates or kills tmux sessions, so both are gated on confirmation), and which plugin it belongs to (`yen-compute`).
5. Wrote the frontmatter and body of `skills/yen-interactive/SKILL.md` to the conventions in AGENTS.md, and filled `agents/openai.yaml` with `default_prompt: "Use $yen-interactive to keep my interactive work running on Yen."`
6. Added a `yen-interactive` row to the "Included skills" table in `README.md`, added `./yen-interactive` to the `yen-compute` skills list in `.claude-plugin/marketplace.json`, and added it to the `yen-compute` row of the README "Plugins" table.
7. Ran `scripts/validate.py` (`8 skills, 0 errors, 0 warnings`) and `claude plugin validate .` (passed).

## Output

> Created `skills/yen-interactive/`, linked it for Claude Code and Codex, added it to the README, and put it in the `yen-compute` plugin. SKILL.md is drafted; both validators pass.
>
> Next steps for you: run `/yen-interactive` on a real Yen session, paste the run into `skills/yen-interactive/EXAMPLE.md` including one request it should not trigger on, and open a PR. Once merged the skill is live; plugin users get it on their next update.

## What stops it

- A name whose folder already exists: the agent stops before copying and asks for another name.
- An invalid name: the validator reports `name must be 1-64 chars of lowercase letters, digits, and single hyphens`.
- A credential listed under `requires.secrets`: the validator reports that end-user skills read no credential files.
- A secret value pasted into the skill: the validator reports it and the PR fails.

## Should not trigger on

- "Add a Do-not-use line to the yen-slurm description": that is editing an existing skill.
- "yen-modules didn't work for me": that is a GitHub issue, not a new skill.
