# Yen Cluster Skills

Reusable agent skills for Stanford GSB's Yen computing environment, for Claude Code, the claude.ai app, Codex, and ChatGPT. These skills are for Yen end users: they need ordinary Yen access, no staff privileges, and never handle credentials. DARC-internal skills live in [`darc-staff-skills`](https://github.com/gsbdarc/darc-staff-skills), whose conventions this repo follows; they are written out in [`AGENTS.md`](AGENTS.md).

## Included skills

Every skill in `skills/` is live. Each folder's `manifest.yaml` says who made it, when, what it needs, and what it does. If a skill does not work for you, open an issue with the [Skill problem](https://github.com/gsbdarc/yen_cluster_skills/issues/new?template=skill-problem.yml) template; the author in its manifest picks it up.

| Skill | Use it for | Needs |
|---|---|---|
| [`yen-access`](skills/yen-access/SKILL.md) ([example](skills/yen-access/EXAMPLE.md)) | Secure SSH and JupyterHub onboarding, eligibility, and basic access troubleshooting. Never asks for or handles credentials. | Nothing; guidance only, you run SSH and Duo yourself. Any host. |
| [`yen-guide`](skills/yen-guide/SKILL.md) ([example](skills/yen-guide/EXAMPLE.md)) | Choosing between interactive Yen servers, Slurm, GPU resources, and storage spaces. | Nothing; explanation only, runs no commands. Any host. |
| [`yen-modules`](skills/yen-modules/SKILL.md) ([example](skills/yen-modules/EXAMPLE.md)) | Discovering, loading, switching, and inspecting software modules in an active Yen session. | An active Yen shell. |
| [`yen-project-spaces`](skills/yen-project-spaces/SKILL.md) ([example](skills/yen-project-spaces/EXAMPLE.md)) | VAST-backed project directories, quotas, workgroups, and collaborator access. Membership changes go through Stanford Workgroup Manager. | Any host for guidance; an active Yen shell for `gsbquota`. |
| [`yen-resource-limits`](skills/yen-resource-limits/SKILL.md) ([example](skills/yen-resource-limits/EXAMPLE.md)) | Interactive, Slurm, GPU, job-array, and storage limits. | Any host for documented limits; an active Yen shell for live checks. |
| [`yen-slurm`](skills/yen-slurm/SKILL.md) ([example](skills/yen-slurm/EXAMPLE.md)) | Planning, submitting, monitoring, troubleshooting, and scaling CPU or GPU Slurm jobs. Confirms before every `sbatch` or `scancel`. | An active Yen shell with Slurm. |
| [`new-skill`](skills/new-skill/SKILL.md) ([example](skills/new-skill/EXAMPLE.md)) | Scaffolding a new skill from the template — creates the folder, links it for both agents, adds it to a plugin if wanted, validates it, and guides the first draft. Part of the repo's own workflow, not for end users. | A clone of this repo, `git`, python3 with PyYAML, and the `claude` CLI for plugin checks. |

## Plugins

A plugin installs a group of skills together in Claude Code and the claude.ai app. Its skills are invoked as `/<plugin>:<skill>`. Plugins are defined in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json), which points at the skill folders above rather than copying them.

| Plugin | Skills | Needs |
|---|---|---|
| `yen-basics` | `yen-access`, `yen-guide`, `yen-modules`, `yen-project-spaces` | Nothing for access and guidance. Module and quota commands need the agent to be running in an active Yen shell. |
| `yen-compute` | `yen-slurm`, `yen-resource-limits` | An active Yen shell for live scheduler and limit checks. Every job submission or cancellation waits for your confirmation. |

Skills that run commands can only explain them where there is no Yen shell, for example in claude.ai chat. To have them run commands, use Claude Code on a Yen (`ml claude-code`).

**Claude Code.** Run:

```bash
claude plugin marketplace add gsbdarc/yen_cluster_skills
claude plugin install yen-basics@yen-cluster-skills
claude plugin install yen-compute@yen-cluster-skills
```

Then invoke a skill as `/yen-compute:yen-slurm`, or just describe what you need. Run `claude plugin marketplace update yen-cluster-skills` to pick up new skills.

**claude.ai and Claude desktop.** Go to Customize > Plugins > Add marketplace and enter `gsbdarc/yen_cluster_skills`, then install the plugins you want.

**Codex** gets these skills one at a time through `./install.sh` (see below), as `$yen-slurm`, `$yen-access`, and so on.

## Layout

```
skills/<name>/          SKILL.md, EXAMPLE.md, manifest.yaml, agents/openai.yaml  (source of truth)
.claude/skills/<name>   symlink for Claude Code discovery
.agents/skills/<name>   symlink for Codex discovery
.claude-plugin/marketplace.json   plugins: named groups of skills/ folders
templates/skill-template/
scripts/validate.py     structural checks, run by CI
install.sh              link skills into your home directories
```

The `agents/openai.yaml` files are Codex interface metadata and are ignored by Claude Code.

## Using the skills from a clone

**Inside this clone**, every skill is available to both agents immediately: the repo ships `.claude/skills/` and `.agents/skills/` with a relative symlink per skill, so they survive a clone to any path. Inside the clone, the repository copy takes precedence over a user-wide one.

**Everywhere else**, link the skills into your home directories:

```bash
./install.sh              # every skill
./install.sh yen-slurm    # just the named ones
./install.sh --dry-run    # show what would happen
```

For Claude Code, a full run skips skills that belong to a [plugin](#plugins) and prints the `claude plugin install` command instead. Having both copies would give you `/yen-slurm` and `/yen-compute:yen-slurm` side by side. Codex gets every skill. Naming a skill links it either way.

Symlinking keeps one source of truth: pulling this clone updates the skills everywhere at once. It also makes the clone a live dependency, so moving, renaming, or deleting it breaks the installed skills.

Restart the agent if a newly linked skill does not appear. In Claude Code, run `/context` to confirm it loaded.

**Upgrading from the old layout.** Skills used to sit at the top of the repo (`yen-slurm/`) and now live in `skills/yen-slurm/`, so links made from the old instructions no longer resolve. List them with `find ~/.claude/skills ~/.agents/skills -maxdepth 1 -xtype l`, remove the ones that point into this clone, and re-run `./install.sh` or install the plugins.

## Invocation

Every surface can choose a skill automatically when its description matches the request. You can also invoke a skill directly:

```text
$yen-slurm Help me create a Slurm job for this Python script.               # Codex
/yen-compute:yen-slurm Help me create a Slurm job for this Python script.   # Claude Code, plugin
/yen-slurm Help me create a Slurm job for this Python script.               # Claude Code, inside this clone or via install.sh
```

## Design

Keep each skill focused. The general guide explains and routes; access, modules, project storage, resource limits, and Slurm operations remain separate so their guidance stays accurate and easy to maintain.

Treat the current cluster policy and live Yen commands as authoritative for time-sensitive limits, availability, and membership state.

## Adding a skill

From inside the clone, run `/new-skill` (Codex: `$new-skill`) and describe the skill. It scaffolds `skills/<name>/` from the template, links it for both agents, adds it to a plugin if you want, validates it, and helps write the first draft. The manual steps and the conventions are in [`AGENTS.md`](AGENTS.md#adding-a-skill).

`scripts/validate.py` needs Python with PyYAML; on the Yens, `/opt/jupyterhub/bin/python3` has it. CI runs it on every push and PR.
