# Yen Cluster Skills

Reusable agent skills for Stanford GSB's Yen computing environment. Each skill directory works with both Codex and Claude Code.

## Included skills

| Skill | Use it for |
|---|---|
| `yen-access` | Secure SSH and JupyterHub onboarding, eligibility, and basic access troubleshooting. |
| `yen-guide` | Choosing between interactive Yen servers, Slurm, GPU resources, and storage spaces. |
| `yen-modules` | Discovering, loading, switching, and inspecting software modules in an active Yen session. |
| `yen-project-spaces` | VAST-backed project directories, quotas, workgroups, and collaborator access. |
| `yen-resource-limits` | Interactive, Slurm, GPU, job-array, and storage limits. |
| `yen-slurm` | Planning, submitting, monitoring, troubleshooting, and scaling CPU or GPU Slurm jobs. |

## Using the skills with Codex

Codex discovers repository skills in `.agents/skills/` and user-wide skills in `~/.agents/skills/`.

To make these skills available across a user's projects, clone this repository and symlink or copy each skill directory into `~/.agents/skills/`. For example:

```bash
mkdir -p ~/.agents/skills
ln -s /path/to/yen_cluster_skils/yen-access ~/.agents/skills/yen-access
```

Repeat for the skills a user needs. Codex follows symlinked skill directories. Restart Codex if a newly added skill does not appear.

For a project-specific setup, place only the relevant skill directories under that project's `.agents/skills/` directory.

## Using the skills with Claude Code

Claude Code discovers repository skills in `.claude/skills/` and user-wide skills in `~/.claude/skills/`.

This repository already ships `.claude/skills/` with a symlink to each skill directory, so cloning it and running Claude Code from the clone makes all six skills available immediately. The symlinks are relative, so they survive a clone to any path.

To make the skills available in every project, symlink them into your user-wide skills directory:

```bash
mkdir -p ~/.claude/skills
for s in yen-access yen-guide yen-modules yen-project-spaces yen-resource-limits yen-slurm; do
  ln -s /path/to/yen_cluster_skills/$s ~/.claude/skills/$s
done
```

Restart Claude Code if a newly added skill does not appear; run `/context` to confirm it loaded. A user-wide skill is available from any directory, while the repository copy takes precedence when Claude Code runs inside this clone.

Symlinking keeps one source of truth: editing a `SKILL.md` here updates the skill everywhere at once. It also makes the clone a live dependency, so moving, renaming, or deleting it breaks the installed skills. Copy the directories instead of symlinking them if you want each install to stand on its own.

The `agents/openai.yaml` files are Codex interface metadata and are ignored by Claude Code.

## Invocation

Both harnesses can choose a skill automatically when its description matches the request. A user can also invoke a skill directly:

```text
$yen-slurm Help me create a Slurm job for this Python script.   # Codex
/yen-slurm Help me create a Slurm job for this Python script.   # Claude Code
```

## Design

Keep each skill focused. The general guide explains and routes; access, modules, project storage, resource limits, and Slurm operations remain separate so their guidance stays accurate and easy to maintain.

Treat the current cluster policy and live Yen commands as authoritative for time-sensitive limits, availability, and membership state.
