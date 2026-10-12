---
name: github-for-research
description: Research-grade GitHub workflow guidance for academic and research projects. Use when working in a GitHub-backed research repository, setting one up, saving or reviewing changes, opening issues or pull requests, preserving a reproducible project history, validating data transformations, documenting analysis pipelines, managing branches for experiments and fixes, or making AI-assisted research work transparent.
---

# GitHub for Research

Use this skill to keep research projects on GitHub organized, reproducible, and transparent. Treat the repository as a shared lab notebook: each issue, branch, commit, and pull request should explain what changed, why it changed, what was checked, and what remains uncertain.

Assume the human user may not have a software background. Do the mechanical Git and GitHub work yourself when tools and permissions allow, and explain decisions in plain language.

## Audience and Tone

Write for researchers first: economists, political scientists, sociologists, psychologists, lab members, students, and co-authors may read the resulting issues, pull requests, and commit history. Avoid assuming they know Git jargon. When a technical term matters, use it, then explain it briefly in plain language.

The `.agents` version is agent-facing, so keep instructions direct and compact, but preserve the original skill's human-facing aim: make the project history useful to people who need to understand the research months later.

## Core Rules

1. Credit AI assistance transparently on commits, pull requests, and issue work.
2. Do new work on a branch, not directly on the default branch.
3. Use the GitHub Flow loop: branch -> focused commits -> pull request -> review -> merge -> delete or archive branch.
4. Log problems, questions, and decisions as issues.
5. Explain why a change was made, not only what changed.
6. Keep environments reproducible with lockfiles or equivalent version records.
7. Keep raw data read-only; validate every processed-data transformation.
8. Never commit secrets, credentials, or sensitive data.
9. Preserve failed experiments with a short record of what was tried and why it did not land.

## Transparent AI Attribution

Use project-specific attribution requirements when they exist. If the repository has no convention, apply a portable convention that is model-agnostic in policy but specific in each recorded attribution:

- In commit bodies for substantive AI-assisted changes, include a line such as `AI-assisted: prepared with <assistant/product and model or version>`.
- In pull-request descriptions, include a short note such as `AI-assisted: this change was prepared with help from <assistant/product and model or version>`.
- Optionally add an issue or PR label such as `ai-assisted` if the repository uses labels for provenance.

Prefer product plus model/version when known, for example `OpenAI Codex (GPT-5)` or `Claude Code (Claude Opus 4.8)`. If the exact assistant, model, or version is unknown, ask the user before writing the attribution. Do not invent a specific model, vendor, or account identity. If a project requires a `Co-Authored-By` trailer, ask the user what name and email to use unless the repository already documents them.

## Data Integrity

Research correctness is non-negotiable. When a task changes, cleans, merges, filters, or recomputes data, make validation part of the saved work.

Keep raw data clean:

- Store original inputs in a folder such as `data/raw/`.
- Treat raw files as read-only.
- Write derived files to a separate location such as `data/processed/`.
- If raw data changes, add a new dated or versioned file instead of overwriting the original.

Add explicit checks for data transformations. Choose checks that match the operation:

- Row counts before and after.
- Expected column names and types.
- Sensible value ranges.
- Missing-value and duplicate counts.
- Unique identifier checks.
- Merge coverage and unmatched-key counts.
- Totals or grouped summaries that reconcile before and after.

Prefer formal, re-runnable validation:

- Python: `pandera` for lightweight schema checks; Great Expectations for larger data-quality workflows.
- R: `assertr` or `pointblank`.
- Minimum fallback: plain assertions for row counts, required columns, types, uniqueness, and ranges.

If the user asks for a data transformation without a validation plan, pause before implementing the transformation. State the missing validation risk and propose concrete checks for that specific task. Continue once the user approves the checks, revises them, or explicitly accepts the risk.

When a validation check fails, log the failure as an issue unless it is an obvious local typo fixed immediately in the same change.

## Issues

Use issues as the planning and record-keeping unit.

Open an issue when:

- Something breaks or produces a wrong-looking result.
- A data question, unresolved assumption, or methodological choice appears.
- A task is too large to fit in one focused change.
- A failed experiment should be recorded for later.

Use clear labels when available:

- `bug` for broken behavior.
- `data` for data quality, access, or interpretation problems.
- `experiment` for analysis ideas or alternatives.
- `question` for unresolved decisions.
- `decision` for choices that should remain visible.
- `ai-assisted` for AI-involved work, if the project uses provenance labels.

For larger issues, add task-list checkboxes with `- [ ]`. For broad work, split into sub-issues when the platform and repository conventions support them.

Close issues through linked changes rather than silently. In the pull-request description for a fix, use a closing keyword such as `Closes #12` so the issue, change, and reasoning remain connected. Remember that GitHub auto-closing applies when the pull request targets the repository default branch.

## Branches

Keep the default branch working and reproducible.

Use branch names that reveal intent:

- `experiment/logit-instead-of-ols`
- `fix/12-missing-sites`
- `data/validate-merge-keys`
- `docs/reproduction-readme`

Create experiment branches for research alternatives. If an experiment does not work, record the hypothesis, method, result, and conclusion in the related issue or PR before closing it. Do not erase failed experiments without leaving a trace.

Create fix branches tied to issues when repairing known problems. Include the issue number in the branch name when helpful.

## Commits

Make focused commits: one logical change per commit. Use commits as dated lab-notebook entries.

Write commit messages in this shape:

```text
Imperative summary under about 72 characters

Explain why this change was made. Mention the research decision, data issue,
validation result, or reproducibility concern that motivated it.

AI-assisted: prepared with <assistant/product and model or version>
Refs #12
```

Use `Closes #12` only when the commit or corresponding PR actually resolves the issue. Use `Refs #12` for related context.

When no files need to change but a decision should be recorded, consider an empty journal commit:

```bash
git commit --allow-empty -m "[NOTE] Drop 2020 data from main sample"
```

Use empty commits sparingly and include enough body text to explain the decision.

## Pull Requests

Use pull requests as review checkpoints and durable summaries.

For each PR, include:

- Purpose: what problem, question, or milestone this addresses.
- Summary: the focused changes made.
- Validation: commands run, data checks performed, or why validation is not applicable.
- Links: `Closes #...` or `Refs #...` as appropriate.
- Attribution: a model-agnostic AI-assistance note when applicable.

Open draft PRs for work-in-progress experiments when early discussion is useful. For solo research, still use PRs as self-review checkpoints before changes land on the default branch.

For PRs that include figures, do not use relative image paths in the PR body. Commit and push the figure first, then link to the full raw GitHub URL:

```text
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/figures/plot.png
```

Relative paths remain appropriate inside committed Markdown files such as `README.md`.

## Milestones and Roadmaps

Use milestones to group issues around research deadlines or paper stages. Useful milestone and tag names include:

- `data-collection`
- `cleaning`
- `analysis`
- `writing`
- `submitted`
- `revision-1`
- `accepted`

When the project benefits from a visual view, use a simple board with `To do`, `In progress`, and `Done`.

At meaningful research moments, create a tag or release so the exact project state can be recovered later.

## Repository Hygiene

Create or maintain `.gitignore` so Git tracks source files and ignores private, generated, or bulky outputs.

For data-science repositories, normally ignore:

- `.env`
- notebook checkpoints such as `.ipynb_checkpoints/`
- local caches and build artifacts
- generated outputs that are cheaply rebuilt
- large raw data files when they belong in external storage
- model artifacts unless they are small, meaningful, and intentionally versioned

Use GitHub's official language templates as a base, then add project-specific research and data-science entries.

For notebooks, prefer `nbstripout` so committed `.ipynb` files do not carry large output blobs. When notebooks need close code review, consider `jupytext` to pair them with plain-text files.

## Secrets and Sensitive Data

Never commit passwords, API keys, tokens, private credentials, or restricted human-subjects data.

Use an ignored `.env` file for local secrets. Commit a `.env.example` with variable names and dummy values so collaborators know what to set.

If a secret is committed:

1. Rotate or revoke it immediately.
2. Purge it from history with an appropriate tool such as `git filter-repo`.
3. Force-push the cleaned history only after understanding collaborator impact.
4. Note that forks, caches, and previous clones may still contain the secret.

Rotating first matters more than history rewriting; the secret should be treated as compromised.

## Reproducibility

Make the project re-runnable from a fresh clone.

Maintain the appropriate environment record:

- Python: `uv.lock`, `requirements.txt`, `poetry.lock`, or `environment.yml`.
- R: `renv.lock`.
- Other stacks: the ecosystem's lockfile or a documented version manifest.

Use relative paths in scripts and docs. Avoid absolute paths such as `/Users/name/project`, which break on other machines.

Create a master script or command that rebuilds the analysis from raw inputs to final tables and figures. Document it in the README. If randomness appears anywhere, fix and document the random seed.

Do not version outputs that are cheap to regenerate. Keep processed data under version control only when it is expensive to reproduce, needed as an exact snapshot, or intentionally part of a release artifact.

Keep large or sensitive data outside GitHub in approved storage, and document where authorized collaborators can access it.

## Documentation and Licensing

Maintain a README that covers:

- What the project is.
- How to set it up.
- How to reproduce results from a fresh clone.
- The master command or script order.
- A map from scripts to outputs, such as `03_model.py -> Table 2, Figure 4`.
- Where large, private, or restricted data lives.

Add a license when the project is meant to be reused. Code and data/text often need different licenses:

- Code: permissive open-source license such as MIT, BSD, or Apache-2.0.
- Data and text: Creative Commons license such as CC0 or CC-BY, subject to data rights and institutional requirements.

If licensing is unclear, ask the user before adding a license.

## Reconstructing Project History

When asked what happened in a project, reconstruct the story from:

- Issues: problems, questions, decisions, and experiments.
- Pull requests: proposed changes and review discussion.
- Commits: chronological snapshots and reasoning.
- Links: `Closes #...`, `Refs #...`, branch names, labels, milestones, tags, and releases.

Summarize in research terms: what was tried, why, what changed, what evidence or checks supported it, and what remains unresolved.

## Plain-Language Glossary

- Repository or repo: the folder holding the whole project and its history.
- Commit: a saved snapshot with a note; like a dated lab-notebook entry.
- Branch: a private working copy for trying or fixing something without disturbing the main version.
- Issue: a GitHub note that records a problem, question, task, or decision.
- Pull request or PR: a proposal to merge branch changes into the main project, with a summary and review step.
- GitHub Flow: the loop of branch -> commit -> pull request -> review -> merge -> delete branch.
- Task list: checkboxes inside an issue that break work into smaller steps.
- Milestone: a named goal that groups issues and shows progress toward a deadline.
- Tag or release: a permanent named bookmark of the project at an important moment.
- Lockfile: a saved list of exact software versions so the work can be rerun later.
- `.gitignore`: a file listing local, private, generated, or large files Git should not save.
- License: a file that says how others may use the code, data, and text.

## Quick Reference

- New work -> create a branch, make focused commits, open a PR, review, merge.
- Something wrong or uncertain -> open an issue.
- Data transformation -> add validation checks before or with the transformation.
- Raw data -> never edit in place.
- Commit messages -> imperative summary plus why.
- PR descriptions -> purpose, summary, validation, links, attribution.
- Secrets -> keep out; if leaked, rotate first.
- Notebook outputs -> strip before commit.
- Reproducibility -> lockfile, master script, relative paths, README instructions.
- Failed experiment -> record the result and preserve the trail.

## Further Reading

Use these sources when the user asks for background or stronger justification:

- GitHub Docs: [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow), [issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues), [milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones), [projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects), [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests), [PR reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews), [linking PRs to issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue), [push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection), [removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository), and [licensing repositories](https://docs.github.com/en/repositories/managing-your-repositys-settings-and-features/customizing-your-repository/licensing-a-repository).
- Gentzkow and Shapiro, ["Code and Data for the Social Sciences"](https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf).
- [Project TIER Protocol 4.0](https://www.projecttier.org/tier-protocol/protocol-4-0/).
- [AEA / Social Science Data Editors template README](https://social-science-data-editors.github.io/template_README/).
- [The Turing Way](https://book.the-turing-way.org/).
- Wilson et al., ["Good Enough Practices in Scientific Computing" (2017)](https://doi.org/10.1371/journal.pcbi.1005510).
- Perez-Riverol et al., ["Ten Simple Rules for Taking Advantage of Git and GitHub" (2016)](https://doi.org/10.1371/journal.pcbi.1004947).
- Sandve et al., ["Ten Simple Rules for Reproducible Computational Research" (2013)](https://doi.org/10.1371/journal.pcbi.1003285).
- Chris Beams, ["How to Write a Git Commit Message"](https://cbea.ms/git-commit/).
- Tool docs: [`pandera`](https://pandera.readthedocs.io/), [Great Expectations](https://greatexpectations.io/), [`assertr`](https://docs.ropensci.org/assertr/), [`pointblank`](https://rstudio.github.io/pointblank/), [`nbstripout`](https://github.com/kynan/nbstripout), [`jupytext`](https://jupytext.readthedocs.io/), and [Choose a License](https://choosealicense.com/).
