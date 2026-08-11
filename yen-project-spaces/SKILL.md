---
name: yen-project-spaces
description: Guide creation, use, quota checking, and access management for Stanford GSB Yen project spaces and their Stanford workgroups. Use when a user needs shared durable Yen storage, wants to understand a project directory or quota, needs to identify the workgroup tied to a project, or needs to add or remove a collaborator. Do not use for temporary scratch storage, Slurm job submission, or general Yen architecture questions.
---

# Yen Project Spaces

Help users use durable shared Yen project storage and understand the workgroup that controls access.

## Safety and access boundary

- Treat project data and workgroup membership as sensitive. Do not change membership, permissions, or sponsorship without the user's explicit approval at the time of the change.
- Explain the impact before any access change: adding a member grants access; removing a member revokes it.
- Do not request passwords, Duo approvals, or other credentials.
- Direct users to the official Stanford Workgroup Manager for membership changes. Do not infer membership or administrator status.

## Explain the storage model

- Recommend project space for durable large datasets, shared research outputs, collaboration, and long-running workflows on Yen.
- Explain that project space is VAST-backed and is available through both `/zfs/projects/...` and `/yen/projects/...`; these paths point to the same storage.
- Distinguish project space from home directories and temporary scratch. Use `$yen-guide` for the broader storage decision when needed.
- Explain that Yen is not approved for high-risk data and that VAST-backed project space is accessible only from Yen, not from Sherlock or FarmShare.

## Request and locate project space

1. Determine whether the user needs a faculty-led or student-led project space.
2. Direct the user to the approved Project Space Request Form for a new space. Explain that the request captures expected storage and initial collaborators.
3. Explain the usual paths: `/zfs/projects/faculty/<project>` for faculty-led work and `/zfs/projects/students/<project>` for student-led work.
4. State the default quotas: 1 TB for faculty-led projects and 200 GB for student-led projects; additional capacity can be requested.
5. For an existing project, ask for the known project path or consult the original creation confirmation. If the corresponding workgroup is unknown, direct the user to DARC rather than guessing.

## Check quota and usage

1. In an active Yen session, use `gsbquota <project-path>` to inspect a specific project space.
2. Explain the reported usage in relation to the project's quota.
3. Recommend archiving inactive data and removing unneeded intermediate results through the team's approved process. Do not delete project data automatically.

## Workgroup access

1. Explain that every Yen project space has a corresponding Stanford workgroup. Workgroup members receive read/write access to that project space and Yen login access.
2. Explain roles: members receive access; administrators can add or remove members and administrators.
3. Tell project administrators to use the Stanford Workgroup Manager for a deliberate membership change.
4. Explain that membership can take up to 24 hours to propagate to Yen. Do not treat an immediate access failure as proof that the change failed.
5. Encourage regular review of members and administrators, especially for external collaborators.

## Common questions

Answer questions such as:

- “Should this data live in project space or scratch?”
- “How much storage is my project using?”
- “How do I add a collaborator to our Yen project?”
- “Why can’t a new workgroup member access the project yet?”
- “What is the difference between a workgroup member and administrator?”

## Reference

Read [references/project-spaces.md](references/project-spaces.md) for official paths, quotas, and workgroup links.
