---
name: skill-template
description: One or two sentences on what the skill does, then when to use it with the phrases a user would actually say — "do X for Y", "check Z". End with what it is not for — "Do not use for A or B." Max 1024 characters.
compatibility: Where it must run and what it needs, in one line — host (any / an active Yen shell), MCP servers or connectors, host tools or modules, permissions. Max 500 characters. Delete this line if the skill has no requirements.
---

# Skill title

One paragraph: what this skill does, what it writes or changes, and what it never does.

## Requirements

- What must be available before the skill can run, in prose the agent can check against (an active Yen session, a module, a command such as `gsbquota`, a connector). If a requirement is missing, the skill should say so and stop rather than improvise.
- No credential files. The user authenticates themselves (SUNet and Duo, or a connector sign-in); the skill never asks for, reads, or handles a password, token, or key.

## Inputs

- What the caller provides, and what to do when something is missing. Prefer asking over guessing.

## Procedure

1. Numbered steps. Include the exact commands or tool calls where they matter.
2. Put a confirmation gate before anything that changes the user's jobs, environment, data, or access (`sbatch`, `scancel`, `module load`, a workgroup change).
3. Keep this file under 500 lines. Move long reference material into `references/` and link it.

## Output

What the user gets back, and how they can verify it themselves (a link, a file path, a command to re-run).

## Rules

- Never hardcode a person's identity or a personal absolute path. Resolve identity from the session (`whoami` on a Yen host) or ask.
- Never ask for, echo, or write a secret: not in this file, a script, `EXAMPLE.md`, or the conversation.
- Anything else the agent must not do.
