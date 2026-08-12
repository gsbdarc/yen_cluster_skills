---
name: yen-access
description: Guide approved, secure access to Stanford GSB's Yen cluster. Use when a user needs to determine eligibility, connect through SSH with a SUNet ID and Duo, open JupyterHub on an interactive Yen server, or diagnose a basic access problem. Do not use for work after login, Slurm jobs, or software-module management.
---

# Yen Access

Help users reach Yen without handling credentials or performing work on the cluster.

## Safety boundary

- Never request, receive, store, paste, or transmit passwords, Duo prompts, recovery codes, SSH private keys, or other secrets.
- Explain that the user must complete Stanford authentication themselves.
- Stop after successful access is established. Hand off work on a logged-in Yen session to the `yen-modules` skill or another appropriate skill.

## Determine the route

1. Use SSH when the user needs a terminal.
2. Use JupyterHub when the user needs web-based notebooks, a browser terminal, or a graphical research environment.
3. Explain that the public SSH entry point load-balances across the interactive Yen servers, while each JupyterHub instance is tied to the selected server.

## SSH onboarding

1. Confirm that the user has a SUNet ID. GSB faculty, staff, PhD students, and research fellows normally have access; others need approved sponsorship.
2. Tell the user to open a local terminal and run `ssh <SUNetID>@yen.stanford.edu`.
3. Tell them to complete Duo themselves. Do not ask them to share authentication details.
4. If they are connecting remotely and fail to reach Yen, suggest checking Stanford VPN and retrying with the full host name.
5. For a deliberate connection to an interactive server, use its full name, for example `ssh <SUNetID>@yen3.stanford.edu`.

## JupyterHub onboarding

1. Direct the user to the JupyterHub page for one interactive server: `https://yen1.stanford.edu` through `https://yen5.stanford.edu`.
2. Tell them to sign in with their SUNet credentials and select **Start My Server**.
3. Explain that sessions on different Yen servers are independent. Use the same server again when continuity matters.
4. Recommend a non-Safari browser if JupyterHub behaves unexpectedly.

## Troubleshoot only basic access

- For an ineligible user, point to the approved sponsorship process; do not attempt to request sponsorship on their behalf.
- For an expired sponsored account, tell the user to verify renewal with the sponsoring GSB faculty member or the cluster support process.
- For a hostname error, use the complete `yenN.stanford.edu` address.
- For a maintenance notice, explain that access may be temporarily unavailable and defer to the cluster status and support channels.

## Reference

Read [references/access.md](references/access.md) when a user needs eligibility details or authoritative access links.
