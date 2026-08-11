# Yen Cluster Skills

Reusable Codex skills for Stanford GSB's Yen computing environment.

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

## Invocation

Codex can choose a skill automatically when its description matches the request. A user can also invoke a skill directly, for example:

```text
$yen-slurm Help me create a Slurm job for this Python script.
```

## Design

Keep each skill focused. The general guide explains and routes; access, modules, project storage, resource limits, and Slurm operations remain separate so their guidance stays accurate and easy to maintain.

Treat the current cluster policy and live Yen commands as authoritative for time-sensitive limits, availability, and membership state.
