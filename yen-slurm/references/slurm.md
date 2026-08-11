# Yen Slurm reference

Use this reference for Yen-specific scheduler context. Verify live availability and current policy with the scheduler before submitting a job.

- Slurm guide: https://rcpedia.stanford.edu/_user_guide/slurm/
- GPU jobs guide: https://rcpedia.stanford.edu/_user_guide/using_gpu/
- Job arrays: https://rcpedia.stanford.edu/_user_guide/job_arrays/
- GPU architecture: use `$yen-guide`.

## Core commands

| Goal | Command |
|---|---|
| Submit a script | `sbatch <script>.slurm` |
| View the user's jobs | `squeue -u $USER` |
| View current user's jobs | `squeue --me` |
| View jobs in one partition | `squeue -p <partition>` |
| Estimate a pending job's start | `squeue --start <job-id>` |
| Inspect one live job | `scontrol show job <job-id>` |
| Inspect a completed job | `sacct -j <job-id>` |
| Inspect partitions and nodes | `sinfo -o "%P %D %N"` |
| Inspect node features | `sinfo -o "%20N %5c %5m %64f %10G"` |
| Inspect detailed node resources | `scontrol show nodes` |
| Summarize interactive and Slurm load | `checkyens` |
| View own jobs | `squeue --me` |
| Cancel one job | `scancel <job-id>` |

## Resource directives

| Purpose | Directive |
|---|---|
| Job name | `#SBATCH -J <name>` |
| Partition | `#SBATCH -p <partition>` |
| CPU cores | `#SBATCH -c <cores>` |
| Total node memory | `#SBATCH --mem=<size>` |
| Memory per allocated CPU | `#SBATCH --mem-per-cpu=<size>` |
| Time limit | `#SBATCH -t <time>` |
| Output path | `#SBATCH -o <path>` |
| Job email notifications | `#SBATCH --mail-type=ALL` and `#SBATCH --mail-user=<address>` |
| GPU count | `#SBATCH -G <count>` |
| Job-array range | `#SBATCH --array=<start>-<end>` |

## Current guidance

- Use the `normal` partition for ordinary CPU jobs, `dev` for short tests, `long` for longer jobs, and `gpu` for GPU-compatible workloads.
- Slurm scheduler requests should accurately match needed CPU, memory, and time. Smaller, correctly sized requests generally begin sooner.
- The GPU partition has a one-day runtime limit and a maximum of four GPUs per user. Verify these limits live before relying on them.
- GPU jobs require compatible software and an explicit GPU request. The GPU nodes provide A30, A40, and H200 hardware; consult `$yen-guide` for per-node capacities.
- Test the command interactively before putting it into a Slurm script.
- Profile a small representative run before choosing CPU, memory, and time. Record wall-clock time, observed CPU use, and peak memory; use a measured buffer rather than an arbitrary large request.
- A Slurm script runs in a fresh shell. Include the project-directory change, module load or environment activation, and the program command inside the script.
- Keep output and error logs separate when practical, and ensure their parent directory exists before submission; Slurm does not create missing directories.
- When a user requests job-email notifications, run `whoami` in the active Yen session and propose the standard `<SUNetID>@stanford.edu` address for the user's confirmation. Verify log and output directories before submitting; do not create a missing directory without the user's approval.
- Use current partition and queue state to warn about likely contention, especially for large, long, high-memory, or GPU requests. Treat every wait-time estimate as provisional.
- Use job completion information—logs, exit status, and utilization summaries—to improve future requests. Favor checkpoints for long-running work when the program supports them.

## Job-array patterns

- Use `SLURM_ARRAY_TASK_ID` to select one independent unit of work per task. Be explicit about whether task IDs begin at zero or one.
- Use `%A` and `%a` in output and error paths so every array task receives its own logs, for example `logs/job_%A_%a.out` and `logs/job_%A_%a.err`.
- Arrange outputs so that each task writes to a unique file or directory. A task should skip valid existing output when it is safe to do so, allowing a resubmission to redo only missing or failed work.
- Monitor the array with `squeue --me`; its tasks appear as sub-identifiers beneath the array's job identifier.
- Treat cancelling an array as a potentially broad action. Confirm whether the user wants to cancel the whole array or only a specific task.
