---
name: yen-guide
description: Explain Stanford GSB's Yen computing environment and help users choose among interactive Yen servers, Yen Slurm, and GPU resources. Use when a user asks which Yen resource fits their work, how interactive and scheduled computing differ, whether a workload belongs on a GPU, or what to do next before running work. Do not use to log in, run commands, load modules, create Slurm jobs, or manage a live session.
---

# Yen Guide

Explain the Yen environment, recommend an appropriate compute or storage resource, and hand off to a focused skill only after the user understands the choice.

## Scope

- Remain explanation-only. Do not run shell, module, scheduler, or GPU commands.
- Ask only for the details needed to make a resource recommendation: expected runtime, CPU or memory needs, GPU requirement, interactivity, and whether the work is already tested.
- State uncertainty when information is missing instead of guessing resource requirements.

## Describe the choices

### Interactive Yen servers

Recommend an interactive server for exploration, short tests, development, and work that benefits from a live terminal or notebook. Explain that the shared entry point assigns the user to one of the interactive Yen servers and that shared resources require considerate use.

Recommend a future interactive-work skill for long-running interactive tasks, including persistent terminal workflows such as tmux, once that skill is installed.

### Yen Slurm

Recommend Yen Slurm for long-running, resource-intensive, repeatable, parallel, or batch work. Explain that a scheduler queues jobs and provides requested CPU, memory, time, and GPU resources. Smaller, right-sized requests usually begin sooner.

Before recommending a Slurm submission, check that the program can run successfully from an interactive Yen command line. Recommend the `yen-slurm` skill for creating, submitting, monitoring, and canceling jobs.

### GPU resources

Recommend GPU resources only when the user's workload and software can use a GPU, such as compatible machine-learning training or inference. Explain that GPU jobs use the GPU Slurm partition and need a scheduler workflow; do not imply that a GPU automatically speeds up arbitrary Python, R, or Stata code.

### Storage spaces

Explain the difference between persistent VAST-backed home and project storage, node-local temporary storage, private per-user scratch, and shared scratch. State that temporary and scratch spaces are not backed up and must not hold the only copy of important work. Do not give deletion commands; recommend moving valuable results to project storage and using a focused storage skill for file management.

## Recommendation workflow

1. Ask whether the work is exploratory or a repeatable job.
2. Ask whether it needs to run longer than a brief shared interactive session, requires guaranteed resources, or can be split into independent tasks.
3. Ask whether it needs a GPU and, if so, which software or framework will use it.
4. Recommend one of these paths:
   - Interactive Yen for short, hands-on development and tests.
   - Yen Slurm for scheduled CPU, high-memory, long-running, or batch work.
   - GPU Slurm for software that genuinely supports GPUs.
5. Explain the reason for the recommendation in plain language, then name the focused next skill or the action it should eventually provide.

## Common questions

Answer questions such as:

- “Should I use an interactive Yen server or Slurm?”
- “Is my workload a good fit for a GPU?”
- “Why should I test my code interactively before submitting it?”
- “What information do I need before requesting Slurm resources?”
- “When should I use a persistent interactive session instead of a scheduled job?”
- “Where should I store a large dataset or temporary intermediate files?”
- “What is the difference between my home directory, project storage, and scratch?”

## Focused handoffs

- Use the `yen-access` skill for access onboarding.
- Use the `yen-modules` skill after login to inspect or change installed software modules.
- Use the `yen-resource-limits` skill for exact interactive, Slurm, GPU, array, or storage limits.
- Use the `yen-slurm` skill for job creation, submission, monitoring, and cancellation.
- Use the `yen-project-spaces` skill for durable shared project storage and its workgroup access.
- Recommend the future interactive-work skill for tmux and other persistent interactive workflows.

## Reference

Read [references/resources.md](references/resources.md) when explaining cluster characteristics or confirming current official guidance.
