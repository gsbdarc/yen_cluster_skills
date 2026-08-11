# Yen project spaces and workgroups

Use this reference for project-storage and access-management guidance. Confirm current policy and actual membership through the official services.

- Storage guide: https://rcpedia.stanford.edu/_user_guide/storage/
- Workgroup guide: https://rcpedia.stanford.edu/_policies/workgroups/
- Project Space Request Form: http://darc.stanford.edu/yenstorage

## Project space

- Project spaces use VAST all-flash storage. `/zfs/projects/...` and `/yen/projects/...` lead to the same underlying storage.
- Use `/zfs/projects/faculty/<project>` for faculty-led work and `/zfs/projects/students/<project>` for student-led work.
- Default quotas are 1 TB for faculty-led projects and 200 GB for student-led projects. Additional capacity can be requested.
- Use `gsbquota <project-path>` to check project-space usage.
- Do not store high-risk data on Yen. Project space is mounted only on Yen, not Sherlock or FarmShare.

## Workgroups

- Each project space has a corresponding Stanford workgroup. Members receive project-space read/write access and Yen login access.
- A workgroup administrator can add and remove members and administrators. Treat administrator privileges as high-impact access control.
- Membership changes can require up to 24 hours to propagate to Yen.
- Find an existing project's workgroup in its creation confirmation or by contacting the DARC team; do not guess from the path.
