---
name: yen-resource-limits
description: Explain and check current per-user compute, Slurm, GPU, job-array, and storage limits on Stanford GSB's Yen cluster. Use when a user asks how many CPU cores, how much RAM, time, GPU capacity, array size, or storage they may use, or needs help checking current quota and partition limits. Do not use to submit jobs or change data or access permissions.
---

# Yen Resource Limits

Provide accurate, scoped Yen limits and explain how they apply to the user's chosen environment.

## Principles

- State whether a limit applies to an interactive Yen server, JupyterHub, a Slurm partition, a GPU job, or storage.
- Treat the documented values as a reference and use live, read-only commands when the user needs the current operational state.
- Explain that limits are per user where specified. Do not add together limits from separate contexts unless the policy explicitly allows it.
- Warn that jobs exceeding CPU or RAM limits can be terminated and that a full home directory can block JupyterHub access.

## Interactive and Jupyter limits

1. Use `hostname` to identify the interactive Yen server when checking a live session.
2. Explain that Jupyter notebooks and other interactive scripts have the same per-node CPU and RAM limits, but their usage is accounted separately even when they run on the same interactive server.
3. Use `userload`, `top`, or a user-filtered `htop` view to inspect current CPU and memory use before advising on a larger run.
4. Recommend Slurm rather than an interactive node when the job needs more than the applicable shared-node limit, dedicated resources, or a long unattended run.

## Slurm limits

1. Use the reference table to explain the documented caps for `normal`, `long`, `dev`, and `gpu`.
2. Use `sacctmgr show qos <partition>` and `sinfo` to verify the current partition configuration before planning a submission.
3. Distinguish the partition time limit from the default requested time. Tell users to request an appropriate duration rather than assuming the maximum.
4. State that the maximum Yen Slurm job-array size is 512 tasks.
5. Hand off to the `yen-slurm` skill for creating, submitting, monitoring, or cancelling a job.

## Storage limits

1. Explain that home directories have an 80 GiB soft quota and a 300 GiB hard quota.
2. Use `gsbquota` to check the user's current home quota, or `gsbquota <project-path>` for a project space.
3. Use `gsbbrowser` when the user needs to identify large items in their home directory.
4. Hand off to the `yen-project-spaces` skill for durable project storage and the `yen-guide` skill for selecting among home, project, temporary, and scratch spaces.

## Common questions

Answer questions such as:

- “How much CPU and RAM can I use on yen3?”
- “What is the maximum memory for a long Slurm job?”
- “How many GPU resources can I request?”
- “Why did my interactive job stop?”
- “How many tasks can my job array contain?”
- “Why can’t I open JupyterHub?”

## Reference

Read [references/limits.md](references/limits.md) before giving an exact documented value.
