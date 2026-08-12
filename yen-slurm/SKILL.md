---
name: yen-slurm
description: Prepare, submit, monitor, troubleshoot, and cancel CPU or GPU jobs on Stanford GSB's Yen Slurm cluster. Use when a user needs a Slurm submission script, wants help choosing CPU, memory, time, partition, or GPU resources, needs to submit or inspect a Yen Slurm job, or needs to cancel a specific job. Do not use for cluster access, software-module discovery alone, or general Yen architecture questions.
---

# Yen Slurm

Manage a user’s Yen Slurm workload safely, explain each command, and confirm before any action that creates or cancels a job.

## Safety and scope

- Work only in an active Yen shell session. Use the `yen-access` skill for onboarding and the `yen-modules` skill for module-only tasks.
- Treat `sinfo`, `squeue`, `sacct`, `scontrol show`, and output-file reads as read-only.
- Before `sbatch`, present the script, requested resources, output location, and the exact submission command. Submit only after the user explicitly confirms.
- Before `scancel`, identify the exact job or jobs, state the impact, and obtain explicit confirmation. Never cancel all of a user's jobs by default.
- Do not guess resource requirements. Start from a tested interactive command or ask about runtime, memory, cores, GPU need, and output location. Use the `yen-resource-limits` skill when exact policy limits are needed.

## Build a job plan

1. Confirm that the program succeeds on an interactive Yen server first.
2. Profile a small representative interactive run before sizing a production job. Record wall-clock time, observed CPU use, peak memory, and whether the program is serial or parallel.
3. Use `time`, `userload`, or a user-filtered `htop` view for basic profiling when the user needs help measuring a run. Make the observation from the same interactive Yen node as the running process.
4. Run `whoami` in the active Yen session when job-email notifications are requested. Propose `<SUNetID>@stanford.edu` as the standard notification address, show it to the user, and use a different address only when the user supplies one.
5. Identify the executable, input and output locations, software module or environment, expected runtime, whether the job is CPU, high-memory, parallel, or GPU work, and whether it can resume from a checkpoint.
6. Verify that input files exist and that the parent directory for logs and output exists before proposing the script. If a required log or output directory is absent, explain the path and ask before creating it.
7. Use `sinfo` and the current scheduler state to check available partitions and node features when needed. Use `checkyens` when available for a compact view of interactive and Slurm load.
8. Request only the resources the work will use. Explain that oversized requests wait longer and can affect future priority.
9. Keep durable input and output in project storage. Use `/tmp` only for node-local disposable data and shared scratch only when jobs or nodes must exchange temporary files.

## Create a submission script

1. Include a shell header, a meaningful job name, verified output path, CPU count, memory request, time limit, and partition when appropriate.
2. Add every required setup step to the script: change to the project directory, load the required module or activate the environment, and then run the program. Explain that a Slurm job starts with a fresh shell rather than inheriting the user's working setup reliably.
3. For GPU jobs, request the `gpu` partition and an explicit GPU count. Match the request to the memory needs of the model or dataset.
4. Add `#SBATCH --mail-type=ALL` and the verified notification address when the user asks for job email. Do not invent or silently substitute an address.
5. Keep submission scripts reproducible: use project-relative or absolute paths, write logs to a known location, and avoid embedding secrets.
6. Explain every scheduler directive in plain language before asking for submission confirmation.

## Submit and report

1. Ask for confirmation immediately before running `sbatch <script>`.
2. After submission, report the returned job identifier, requested resources, output path, and the command used.
3. Before submission, inspect the requested partition with `sinfo` and its queue with `squeue`. Explain relevant load, pending jobs, and resource contention in plain language. Warn when a request is unusually large, long, or constrained to scarce GPU or high-memory resources.
4. Describe any pre-submission wait assessment as an estimate only; do not promise a start time. State that scheduler priority, running jobs, and changing demand can alter the wait.
5. Use `squeue --me` or `squeue -u $USER` to inspect that user's current jobs. Explain `R` as running, `PD` as pending, and `CG` as completing, then summarize any displayed reason.
6. Use `scontrol show job <job-id>` for the detailed current request, assigned node, state, and scheduler reason of a live job.
7. Use `squeue --start <job-id>` only as an estimate; explain that start times can change.
8. Use `sacct` for completed or no-longer-visible jobs, including final state, elapsed time, exit code, and recorded resource information when available.
9. Read the specified output and error files when diagnosing a completed or failed job.

## GPU jobs

1. Confirm that the program actually supports GPU execution; a GPU request alone does not accelerate ordinary code.
2. Use the live resource inventory to choose an appropriate GPU type and count. Consult the `yen-guide` skill for the node architecture when the user needs hardware context.
3. Verify that the requested software environment has GPU support.
4. After a GPU job starts, inspect its queue state and, when useful, GPU utilization from the allocated node. Do not attempt to use a GPU node outside the user's scheduled job.

## Cancel and troubleshoot

1. For a specific cancellation, show the exact target job and ask for confirmation before `scancel <job-id>`.
2. For a pending job, inspect its partition, resource request, and scheduler reason before recommending changes.
3. For a failed job, inspect output and error logs first; distinguish application failures from scheduler or resource failures.
4. After a completed job, inspect the logs and, when enabled, the job email's exit status and utilization summary. Compare actual use with the request and recommend a more accurate next request when warranted.
5. For repeated independent work, suggest job arrays only after confirming that tasks are independent, each task has a stable input mapping, and each task can write a distinct output without collisions.
6. For multi-stage pipelines, suggest dependencies only after confirming the order and failure behavior the user wants. Explain that a dependent job may remain pending or need explicit cancellation if its prerequisite fails.
7. For long-running work, ask whether the program can write checkpoints. If it can, keep checkpoint data in durable project storage and document how the job resumes.

## Job arrays

1. Use an array only for independent, similarly sized tasks. Do not use it when one task needs another task's output first.
2. Define the task range deliberately and explain whether the task IDs are zero- or one-based. Verify the mapping from `SLURM_ARRAY_TASK_ID` to the input list so the first item is not skipped and the last task does not exceed the list.
3. Give every task a distinct output and error log using `%A` for the array identifier and `%a` for the task identifier. Ensure every task writes to a distinct result location.
4. Make a task safe to rerun when practical: check whether its expected valid output already exists, then skip completed work rather than recomputing it.
5. Consider total concurrency. If every task can spawn threads or child processes, limit the program's internal parallelism to match the per-task CPU request.
6. Monitor task sub-identifiers in `squeue` and inspect failed tasks' individual logs. Explain that a partial failure need not invalidate successful tasks.
7. Before cancelling, distinguish cancelling the entire array from cancelling one task, identify the exact target, and obtain confirmation.

## Interactive Slurm allocation

- Suggest an interactive Slurm allocation for dedicated-resource debugging or repeated short test runs after the user asks for it.
- Explain that an interactive allocation is still a scheduled job and holds requested resources until the user exits.
- Present the exact `srun --pty` request and ask for confirmation before creating it.

## Reference

Read [references/slurm.md](references/slurm.md) for Yen-specific partition and GPU guidance. Check live scheduler output before relying on time-sensitive limits or availability.
