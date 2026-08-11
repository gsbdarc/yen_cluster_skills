---
name: yen-modules
description: Discover, load, switch, inspect, and unload software modules in an active Stanford GSB Yen shell session. Use when a user asks which Yen software or versions are available, wants to load Python, Stata, or any other module, needs to check loaded modules, or wants an explanation of module commands that were run. Do not use before the user has logged in to Yen.
---

# Yen Modules

Manage software modules in the user's active Yen shell and clearly report the commands and results.

## Scope and safety

- Work only after the user is connected to Yen. For onboarding, use `$yen-access`.
- Treat `module avail`, `module list`, and `module show` as read-only.
- Run `module load`, `module swap`, `module unload`, or `ml purge` only when the user explicitly requests the change or confirms a proposed change.
- State that module changes affect only the current shell session; reconnecting or opening a new terminal requires loading modules again.
- Do not hard-code an inventory or assume versions. Query the live session first.

## Discover

1. Run `module avail` to view the live catalog.
2. Narrow a search with `module avail <name>/`, such as `module avail python/` or `module avail stata/`.
3. Explain that `(D)` identifies the current default and `(g)` identifies a GPU-enabled build when those markers appear.
4. Run `module list` before changing the environment when existing loaded modules may matter.

## Change the active environment

1. Load the requested default with `module load <name>`.
2. Load an exact version with `module load <name>/<version>` when the user specifies it or chooses it from the live list.
3. Switch an already loaded module with `module swap <name>/<version>` after showing what is loaded.
4. Unload a named module with `module unload <name>/<version>`.
5. Use `ml` as the equivalent shorthand for loading or listing modules only when it improves clarity for the user.

## Verify and explain

1. Run `module list` after each requested change.
2. Run `module show <name>` when the user needs the installation path, dependent modules, or environment changes.
3. Report the exact command run, whether it succeeded, the resulting loaded-module list, and the next command the user can use.
4. For Python or Stata, verify the selected executable or version only when the user asks to use it; distinguish module selection from running a program or submitting a job.

## Handle failures

- If a requested module is absent, show the relevant filtered search result and offer available alternatives without guessing a version.
- If a module conflicts with one already loaded, show the current environment and ask whether the user wants to swap or unload the conflicting module.
- If a command fails unexpectedly, report the error in plain language and avoid destructive cleanup.
