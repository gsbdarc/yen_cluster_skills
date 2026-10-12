# Yen resource limits reference

Verify time-sensitive limits with the live cluster tools and official policy page before planning a consequential job.

- Official policy: https://rcpedia.stanford.edu/_policies/user_limits/
- Slurm guide: https://rcpedia.stanford.edu/_user_guide/slurm/

## Interactive and Jupyter limits

| Interactive server | CPU limit per user | RAM limit per user |
|---|---:|---:|
| yen1 | 48 cores | 192 GB |
| yen2 | 48 cores | 192 GB |
| yen3 | 48 cores | 192 GB |
| yen4 | 48 cores | 192 GB |
| yen5 | 12 cores | 320 GB |

- JupyterHub and other interactive scripts are subject to these limits.
- Their CPU and RAM use are counted separately, even when both run on the same interactive Yen server.
- Work exceeding CPU or RAM limits can be terminated automatically.

## Slurm limits by partition

| Partition | CPU limit per user | Memory limit | Time limit | Default time |
|---|---:|---:|---:|---:|
| normal | 512 cores | 3,000 GB | 2 days | 2 hours |
| long | 256 cores | 3,000 GB | 7 days | 2 hours |
| dev | 2 cores | 46 GB | 2 hours | 1 hour |
| gpu | 64 cores | 250 GB | 1 day | 2 hours |

- Maximum job-array size: 512 tasks.
- Check the current partition QoS with `sacctmgr show qos <partition>` before relying on these values.

## Storage limits and checks

- Home-directory soft quota: 80 GiB.
- Home-directory hard quota: 300 GiB. Exceeding the soft quota for too long can lead to lockout; exceeding the hard quota prevents writes.
- A full home directory can prevent JupyterHub access and other basic tasks.
- Use `gsbquota` to inspect home usage and `gsbbrowser` to find large files.
