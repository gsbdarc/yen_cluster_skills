# Yen resource reference

Use this reference for high-level resource guidance. Keep time-sensitive capacity and partition details out of the main skill; direct users to the live cluster tools or official documentation when exact availability matters.

- Yen overview: https://rcpedia.stanford.edu/_getting_started/yen-servers/
- Yen Slurm guide: https://rcpedia.stanford.edu/_user_guide/slurm/
- GPU Slurm jobs: https://rcpedia.stanford.edu/_user_guide/using_gpu/
- Interactive user limits: https://rcpedia.stanford.edu/_policies/user_limits/
- Storage guide: https://rcpedia.stanford.edu/_user_guide/storage/

## Verified guidance

- `yen1` through `yen5` are the interactive shared servers.
- Yen Slurm is a separate scheduler-managed cluster that uses the same broader Yen environment and filesystem.
- Slurm requests CPU, memory, and time; queued jobs begin according to resource availability.
- Slurm is the appropriate route for work that exceeds interactive-node community limits, needs scheduled resources, or can run as batch jobs.
- GPU compute is provided through Slurm. GPU use requires compatible software and an explicit GPU-oriented job request.

## Node inventory

Treat this as guidance, not a live availability report. Check the official current-cluster table or the scheduler before making a resource-specific plan.

### Interactive Yen servers

| Node | Physical CPU cores | Memory | CPU model |
|---|---:|---:|---|
| yen1 | 256 | 1.0 TB | AMD EPYC 7H12 @ 2.6 GHz |
| yen2 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen3 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen4 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen5 | 32 | 1.5 TB | Intel Xeon Gold 6134 @ 3.2 GHz |

### Yen Slurm CPU nodes

| Node | Physical CPU cores | Memory | CPU model |
|---|---:|---:|---|
| yen10 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen11 | 512 | 1.5 TB | AMD EPYC 9754 |
| yen12 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen13 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen14 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen15 | 256 | 1.0 TB | AMD EPYC 7763 |
| yen16 | 128 | 3.0 TB | Intel Xeon Gold 6130 @ 2.10 GHz |
| yen20 | 512 | 1.5 TB | AMD EPYC 9755 |

### Yen Slurm GPU nodes

| Node | Physical CPU cores | System memory | GPU configuration |
|---|---:|---:|---|
| yen-gpu1 | 64 | 0.25 TB | 4 × NVIDIA Ampere A30, 24 GB GPU memory each |
| yen-gpu2 | 64 | 0.25 TB | 4 × NVIDIA Ampere A40, 48 GB GPU memory each |
| yen-gpu3 | 64 | 0.25 TB | 4 × NVIDIA Ampere A40, 48 GB GPU memory each |
| yen-gpu4 | 256 | 0.75 TB | 2 × NVIDIA Hopper H200, 141 GB GPU memory each |

## Storage architecture

Yen uses VAST all-flash storage, which replaced the legacy ZFS backend. The familiar `/zfs/projects/...` and `/yen/projects/...` paths refer to the same VAST-backed project storage.

| Space | Intended use | Scope and durability |
|---|---|---|
| Home directory | Small personal scripts and utilities | Private, persistent; target limit is 80 GB. Do not use for large data or outputs. A full home directory can prevent JupyterHub access. |
| Project directory | Shared datasets, research outputs, collaboration, and persistent workflows | VAST-backed and shared through Stanford workgroups; available under `/zfs/projects/...` and `/yen/projects/...`. |
| `/tmp` | Fast temporary files for a job on one node | Node-local, typically about 1 TB; unavailable from other nodes and cleared after jobs or reboots. |
| `/scratch/users/$SUNET` | Private temporary scratch data | Shared VAST filesystem and available from all Yen nodes; not backed up and periodically purged. |
| `/scratch/shared` | Temporary data that must be shared across nodes or jobs | Shared across Yen nodes; not backed up, periodically purged, and requires user-managed permissions. |

### Storage rules

- Check the data license and platform security requirements before transferring data. Yen storage is not approved for high-risk data.
- Keep home-directory usage below the 80 GiB target. A full home directory can block access to JupyterHub.
- Keep the only durable copy of important data and final results in project storage, with an appropriate backup or versioning practice.
- Use node-local `/tmp` for maximum temporary I/O performance only when the work stays on one node.
- Use per-user or shared scratch only for disposable intermediate data. Per-user scratch is private by default; shared scratch requires deliberate access controls.
- Treat project snapshots as recovery help, not as a primary backup strategy.

## Choosing temporary storage

Use this decision order:

1. Use `/tmp` for fast, disposable files used by one process or job on one Yen node. Its storage is local to that specific node, so another Yen server or a separate Slurm node cannot see those files.
2. Use `/scratch/users/$SUNET` for temporary files that need to follow one user across Yen nodes but do not need to be shared with collaborators.
3. Use `/scratch/shared` for temporary intermediate files that multiple Yen servers or multiple Slurm jobs need to access. Create a private subdirectory for the work and protect it with appropriate permissions.
4. Use project storage instead whenever the data, output, or script must persist, be backed up, or be shared as durable project material.

## Typical directory layout

```text
/home/users/$SUNET/                 # Personal scripts and small utilities
/zfs/projects/...                   # Durable shared project storage (same as /yen/projects/...)
/tmp/                               # Fast, node-local temporary files
/scratch/users/$SUNET/              # Private temporary scratch, visible from all Yen nodes
/scratch/shared/<private-work-dir>/ # Temporary cross-node or Slurm-shared work
```

Do not rely on `/tmp` or either scratch location for the only copy of a result. Move results that matter to project storage before the job ends or temporary storage is purged.
