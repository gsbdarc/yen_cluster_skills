---
name: github-for-research
description: Best practices for using GitHub on academic and research projects with Claude — clear attribution, issues for problems, branches for experiments and fixes, careful data checking, reproducible environments, and a history that both people and Claude can read later.
---

# GitHub for Research

This skill helps researchers keep a project on GitHub in good shape — with Claude doing most of the hands-on work. It is written for people who do **not** have a software background. You do not need to memorize commands; you can simply ask Claude to do these things, and Claude will follow the practices below.

## When to Use This Skill

Use this skill whenever you are:
- Working inside a research project that is stored on GitHub (or setting one up).
- Running a study, cleaning or processing data, or trying out research ideas.
- Asking Claude to make a change, save your work, or fix something.
- Asking "what happened in this project?" or "what did we already try?"
- Asking about keeping your work reproducible, well-documented, or properly credited.

## The Core Idea

**Treat the project like a shared lab notebook.** Everything you and Claude do should leave a clear, honest trail that a person *or* Claude can read back later and understand: what you did, why you did it, what went wrong, and what you decided.

Two ideas follow from this:
- **The history is part of the research output**, not just a backup. Months from now you (or Claude) should be able to reconstruct the whole story from the project.
- **Claude is your main way of working with GitHub.** You describe what you want in plain words; Claude does the mechanical steps and follows the conventions here so the trail stays clean.

A few plain-language terms you will see below (a fuller list is in the glossary at the end):
- **Repository ("repo")** — the folder that holds your whole project and its history.
- **Commit** — a saved snapshot of your work with a short note explaining it. Like a dated lab-notebook entry.
- **Branch** — a private copy of the project where you can try something without disturbing the working version.
- **Issue** — a logged note describing a problem, question, or task, kept on GitHub.
- **Pull request ("PR")** — a proposal to fold a branch's changes back into the main project, with a description and a chance to review first.

## Always-Do Checklist (the essentials)

These are the habits that matter most. Ask Claude to follow them every time.

1. **Credit Claude on everything it helps with.** Every saved snapshot Claude makes ends with a line crediting it, and every proposal it writes says it was made with Claude (details below). Anyone reading the project can see exactly what was human-written and what was AI-assisted.
2. **Do new work on a branch, not the main copy.** Trying an idea? Fixing a problem? Ask Claude to make a branch for it. The main version stays clean and working.
3. **Work in the same repeatable loop every time.** Branch → save changes → open a proposal → merge it in. This loop (called *GitHub Flow*) keeps the main version working and the history readable. See "Organizing Your Work."
4. **Log problems as issues.** When something breaks, looks wrong, or raises a question — even if you fix it right away — record it as an issue so the problem is visible, not just the fix.
5. **Say *why*, not just *what*.** When Claude saves work or proposes a change, the note should explain the reasoning ("switched to the 2019 sample because the 2020 file was missing three sites"), not only the mechanical change.
6. **Keep the environment reproducible.** Save the list of exact software versions your project uses (the "lockfile") so the analysis can be re-run later and get the same result.
7. **Never quietly change raw data, and always check processed data.** Raw data stays untouched; any step that transforms data gets validation checks. If checks are missing, Claude will ask for them before continuing (see next section).
8. **Never commit secrets.** Passwords, API keys, and tokens must never go into the project. Keep them out from the start — recovering from a leaked secret is painful (see "Keeping the Repository Clean").

## Accuracy and Data Integrity (non-negotiable)

Research has to be **correct**. The project should be set up so that checking your work is unavoidable, especially with data.

**Keep raw data clean and untouchable.**
- Original data lives in a folder like `data/raw/` and is never edited in place — treat it as read-only, the way you would never write over the original readings in a lab notebook.
- Anything you compute from it goes into a *separate* place, like `data/processed/`. The raw file is never overwritten.
- If raw data changes (a new export, a correction), that is a new file with a clear name and date — the old one is kept.

**Check every data transformation.**
Whenever data is cleaned, merged, filtered, or recomputed, there should be explicit checks saved next to the code that does it. Useful checks include:
- Row counts before and after (did you lose or duplicate rows you didn't mean to?).
- Column types and names are what you expect.
- Values fall in sensible ranges (no ages of 300, no negative counts).
- Missing values and duplicates are counted and handled on purpose.
- Identifiers that should be unique actually are.
- Totals reconcile before and after the step.

You don't have to write these checks by hand. Ask Claude to add them using a data-validation tool so the checks are formal and re-runnable:
- **Python:** [pandera](https://pandera.readthedocs.io/) is a good lightweight default — you describe the shape each table should have (column types, allowed ranges, which columns must be unique or non-missing) and it enforces it. For larger pipelines, [Great Expectations](https://greatexpectations.io/) is a heavier, fuller data-quality tool.
- **R:** [assertr](https://docs.ropensci.org/assertr/) or [pointblank](https://rstudio.github.io/pointblank/) play the same role.
- At minimum, plain `assert` statements checking row counts and column types are far better than nothing.

**Claude must prompt for checks when they are missing.**
If you ask Claude to process data but don't mention how to verify the result, Claude will **not** just do it silently. It will pause, point out that the step has no validation, and suggest specific checks for *that* transformation in plain language — for example: "Before I merge these two files on participant ID, I'd like to confirm every ID matches and no rows are duplicated. Shall I add those checks?" You can approve, adjust, or explain why a check isn't needed.

**Make the checking visible.** Validation code is saved in the project (not run once and forgotten), it's mentioned in the note for the change that added it, and if a check ever fails, that gets logged as an issue so the problem is on the record.

## Crediting Claude

So that it is always clear who did what:
- **Saved snapshots (commits)** that Claude makes end with a credit line:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
- **Change proposals (pull requests)** that Claude writes include a short note in the description: "🤖 Generated with Claude Code."
- Optionally, proposals and issues that Claude worked on can carry a label such as `claude-assisted`, so you can filter for them on GitHub.

You don't have to do any of this by hand — Claude adds these automatically. The point is transparency: a reviewer, a co-author, or a journal can see the AI's involvement at a glance.

## Issues: Recording Problems

An **issue** is a note on GitHub describing a problem, question, or task. Think of it as flagging something in the margin of your lab notebook.

**Open an issue when:**
- Something breaks or produces a wrong-looking result.
- You hit a dead end or a question you can't resolve yet.
- You notice something to fix or investigate later.

Ask Claude to "open an issue for this," and describe it in plain words. Claude writes it up clearly and can add a label:
- `bug` — something is broken or wrong.
- `data` — a problem with the data itself.
- `experiment` — an idea to try.
- `question` — something to figure out.
- `decision` — a choice that needs to be made or recorded.

**Close issues through a change, not silently.** When the problem is resolved, the proposal that fixes it should reference the issue (Claude writes `Closes #12` in the description) so the problem and its resolution are linked forever. That link is what lets you — or Claude — later trace "this issue → this fix → this reasoning." More on linking in "Organizing Your Work."

## Branches: Experiments and Fixes

A **branch** is a private copy of the project where you can work without touching the main version. Two main uses:

- **Trying a research idea** — ask for an experiment branch (Claude names it something like `experiment/logit-instead-of-ols`). You can explore freely; if it doesn't work, the main version was never affected.
- **Fixing a logged problem** — ask for a fix branch tied to the issue (like `fix/12-missing-sites`). When merged, it closes the issue.

Keep the **main version always working and reproducible** — someone who opens it should be able to run the analysis.

**Preserve failed experiments — don't erase them.** In research, something that *didn't* work is a real finding. If an experiment branch doesn't pan out, don't just delete it. Ask Claude to record what happened and why (in the closing issue note or a short summary), and keep or tag the branch. Later, when you ask Claude "did we already try X?", it can tell you that you did, and what went wrong — saving you from repeating it.

## Organizing Your Work

Issues and branches become powerful when you use them in a consistent rhythm and let GitHub track the flow of work for you. You don't have to run any of this by hand — describe what you want, and Claude sets it up.

### The everyday cycle: GitHub Flow

There is one simple loop, called **GitHub Flow**, that works for every piece of work — code, data cleaning, even writing:

1. **Branch** off the main version for the thing you're about to do.
2. **Make focused commits** as you go (small, self-contained saves).
3. **Open a pull request** to propose folding the work back in.
4. **Review and discuss** it (even if the reviewer is just you, later).
5. **Merge** it into the main version.
6. **Delete the branch** to signal the work is finished.

The reason this keeps the main version safe is simple: *your changes don't reach the main version until you merge.* Until then, main stays working and reproducible for anyone who opens it. (Reference: [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow); Perez-Riverol et al., ["Ten Simple Rules for Taking Advantage of Git and GitHub," *PLOS Comp Biol* 2016](https://doi.org/10.1371/journal.pcbi.1004947).)

**About those "focused commits."** When Claude saves a snapshot it writes the note in a standard shape: a short summary line in the imperative ("Add site-level validation," not "Added" or "I added"), then a blank line, then a few sentences explaining *why*. Each commit is **one logical change** — so if something turns out to be wrong later, that piece can be understood or undone on its own. (Reference: Chris Beams, ["How to Write a Git Commit Message"](https://cbea.ms/git-commit/).)

### Break the project into issues, and issues into checkboxes

The simplest way to plan is to turn the work into **issues** — each one a specific thing that moves the project forward. Open issues are your to-do list; closed issues are the record of what got done.

For a bigger piece of work, ask Claude to add a **task list** inside the issue — a set of checkboxes (written as `- [ ]` items) that break it into steps you can tick off. For a large, multi-part effort (say, "revise the methods section"), Claude can create **sub-issues** so the parts are tracked as their own issues under a parent. (Reference: GitHub Docs — [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues), [About task lists](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-task-lists), [Sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues).)

### Milestones and a roadmap tied to your research stages

Group related issues into a **milestone** — a named goal with an optional due date and an automatic progress bar (it fills in as the issues close). Milestones are a natural fit for the arc of a research project: you can point them at real deadlines like a lab meeting, a conference, or a paper submission. If you like a visual view, ask Claude to set up a simple board with **To do / In progress / Done** columns. (Reference: GitHub Docs — [About milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones), [About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects); The Turing Way — [Roadmapping](https://book.the-turing-way.org/project-design/pd-overview/project-repo/project-repo-roadmapping).)

*A useful convention (not a hard rule):* name milestones — and the release tags you make at big moments — after the stages of your paper's life: data collection → cleaning → analysis → writing → `submitted` → `revision-1` → `accepted`. It makes the project's progress legible at a glance.

### Pull requests are where work gets reviewed

A **pull request** is more than a merge button — it's where a change is explained and checked before it lands:
- Ask for a **draft pull request** to share a work-in-progress experiment early, without asking for a formal review yet.
- A review comes in one of three forms: a plain **comment**, an **approve**, or a **request for changes**; reviewers can leave notes on specific lines.
- **On your own?** The PR is still worth it — it's a self-review checkpoint and a clean, written summary of *why* the change was made.
- **On a small team?** Assign issues to whoever owns them, and turn on a rule that requires a review before merging so nothing lands unseen.

(Reference: GitHub Docs — [About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests), [About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews). *The solo-vs-team split is a practical convention, not a single cited rule.*)

### Connect the trail: issues ↔ pull requests ↔ commits

The value of all this is the links between the pieces. Claude wires them up for you:
- In a pull request that resolves an issue, a **closing keyword** auto-closes the issue when the PR merges. Any of these work: `close`, `closes`, `closed`, `fix`, `fixes`, `fixed`, `resolve`, `resolves`, `resolved` — e.g. `Closes #12`.
- Just mentioning `#26` in any commit, comment, or issue **auto-links** to it and leaves a back-reference on the other end — so even without closing anything, the whole conversation threads together.
- One caveat worth knowing: the auto-close only fires when the pull request targets the **default branch** (usually `main`).

(Reference: GitHub Docs — [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue), [Autolinked references](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls).)

### Your history as a lab notebook

Because everything is linked and explained, the project history *is* a research log. Two habits deepen this: treat an **issue as an experiment entry** (hypothesis → method → result → conclusion), updating it as you go; and when you just want to record a thought or decision that doesn't change any files, ask Claude to make an **empty journal commit** (`git commit --allow-empty`) with a note like `[NOTE] decided to drop 2020 data — see #14`. (Reference: Sandve et al., ["Ten Simple Rules for Reproducible Computational Research," *PLOS Comp Biol* 2013](https://doi.org/10.1371/journal.pcbi.1003285); Chen et al., ["GitHub is an effective platform for collaborative and reproducible laboratory research," 2024](https://arxiv.org/abs/2408.09344).)

## Keeping the Repository Clean

A tidy repo is a trustworthy repo. Two things do most of the work here: telling Git what to ignore, and keeping secrets out entirely.

### `.gitignore`: track sources, ignore the rest

A `.gitignore` file is a list of things Git should **not** save — large data, generated outputs, caches, and anything private. Ask Claude to create one, starting from GitHub's official [`Python.gitignore` template](https://github.com/github/gitignore) and adding a data-science layer: `data/raw/` and large data files (`*.csv`, `*.parquet`, `*.pkl`), notebook checkpoints (`.ipynb_checkpoints/`), model/output artifacts, and `.env`. The habit this enforces is healthy: version the *inputs and code*, and regenerate outputs rather than committing them by hand.

### Secrets and credentials: keep them out from the start

Passwords, API keys, and access tokens must **never** be committed — not even once, because Git remembers everything.
- Keep secrets in an ignored `.env` file and read them as environment variables. Commit a `.env.example` that lists the *names* of the required keys (with dummy values) so a collaborator knows what to set, without exposing the real ones.
- Ask Claude to **turn on GitHub's push protection**, which blocks a push if it detects a secret before it ever lands. (Reference: GitHub Docs — [Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection).)
- **If a secret is ever committed anyway,** the order of operations matters — ask Claude to: (1) **rotate/revoke the secret immediately** (assume it's already compromised), (2) rewrite history to purge it with [`git filter-repo`](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository), (3) force-push the cleaned history, and (4) be aware that forks and cached copies may still hold it. Rotating first is the load-bearing step; scrubbing history alone is not enough.

### Notebooks in version control

Jupyter notebooks store their outputs (tables, plots, long numbers) inside the file, which makes for enormous, unreadable diffs and needless merge conflicts. If your project uses notebooks, ask Claude to set up [`nbstripout`](https://github.com/kynan/nbstripout), which strips the saved outputs automatically when you commit — your working copy is untouched, but the saved version stays small and its changes stay readable. For notebooks you want to review closely, [`jupytext`](https://jupytext.readthedocs.io/) can also keep a plain-text (`.py` or `.md`) twin of each notebook that diffs cleanly.

## Showing Figures in Issues and Pull Requests

Research write-ups are full of plots, and it is natural to embed them in an issue or pull-request description. One catch trips this up constantly: **a link like `figures/plot.png` (a path relative to the project) shows up broken in an issue or PR description.** GitHub only resolves those relative paths inside files it renders *within* the repository — your `README.md` displays the figure fine, but the exact same line pasted into a PR description becomes a broken-image icon.

The fix Claude uses: in issue and PR descriptions, point images at the **full web address** of the committed file — `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/figures/plot.png` — rather than the short project-relative path. (Relative paths stay the right choice *inside* `README.md` and other committed Markdown, where they keep working even if the project is moved or renamed.) So the figure must be committed and pushed first, then linked by its full address. If you ever see a broken image in a PR or issue, this is almost always why — ask Claude to switch it to the full address.

## Reproducible Environments

So the analysis can be re-run and trusted later:
- **Save exact software versions.** Ask Claude to create and commit the "lockfile" for your tools — for example `environment.yml` (conda), `uv.lock` or `requirements.txt` (Python), or `renv.lock` (R). This records the precise versions so a re-run behaves the same.
- **One command should rebuild everything.** Ask Claude to set up a single **master script** that runs the whole pipeline from raw data to final outputs, in order. A newcomer (or you, a year later) should be able to reproduce every result by running one thing. Use **relative paths only** — never absolute paths like `/Users/yourname/...`, which break on every other computer. (Reference: Gentzkow & Shapiro, ["Code and Data for the Social Sciences"](https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf); [Project TIER Protocol 4.0](https://www.projecttier.org/tier-protocol/protocol-4-0/).)
- **Don't save output you can regenerate.** If a processed file or figure is cheaply rebuilt by the master script, prefer versioning the *recipe* (the code) over the output — big regenerable files can be added to `.gitignore`. Keep processed data under version control when it's expensive to reproduce or when you need an exact snapshot; otherwise let the pipeline recreate it.
- **Record randomness.** If your analysis uses any random step, fix and record the random seed so results are repeatable.
- **Mark milestones.** At meaningful points (e.g. a paper submission or a revision), ask Claude to tag a release — a permanent, named bookmark like `submission` or `revision-1` you can always return to.
- **Keep large or sensitive data out of the project, and say where it lives.** GitHub is for code and small files. Big datasets, or anything sensitive or restricted (e.g. human-subjects data), should live in approved storage; note in the project where it is and how to get access, rather than committing it.

## Documentation: README and License

Two files do an outsized amount of work in making a project usable and reusable by others.

**A README that is the front door.** Ask Claude to write and maintain a `README.md` covering: what the project is, how to set it up (and its dependencies), and — most importantly for research — a **"How to reproduce"** section with the exact steps to go from a fresh clone to the final results. Include a short **map from each script to the table or figure it produces** (e.g. "`03_model.py` → Table 2, Figure 4"), so a reader or reviewer can trace every exhibit back to the code that made it. (Reference: [AEA Data Editor template README](https://social-science-data-editors.github.io/template_README/); [Project TIER 4.0](https://www.projecttier.org/tier-protocol/protocol-4-0/); Wilson et al., ["Good Enough Practices in Scientific Computing," *PLOS Comp Biol* 2017](https://doi.org/10.1371/journal.pcbi.1005510).)

**A LICENSE so others may actually use your work.** Without a license, default copyright means *no one may legally reuse, share, or build on your project* — the opposite of what most research wants. Ask Claude to add a `LICENSE`, and note that **code and data want different licenses**: a permissive open-source license (MIT, BSD, or Apache-2.0) for **code**, and a Creative Commons license (CC0 to waive rights, or CC-BY to require attribution) for **data and text**. (Reference: [Choose a License](https://choosealicense.com/); GitHub Docs — [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositys-settings-and-features/customizing-your-repository/licensing-a-repository); Wilson et al. 2017.)

## Asking Claude "What Happened Here?"

Because everything above leaves a clean trail, you can later ask Claude to reconstruct the story of the project, and it will look through:
- the issues (what problems came up),
- the proposals/pull requests (what changes were made and why),
- the saved snapshots and their notes (the step-by-step history),
- and the links between them (`Closes #12`) to connect a problem to its fix.

Good habits now — clear notes, logged issues, explained decisions — are what make this work well later. You might ask: "What did we try for the missing-sites problem?" or "Summarize every data-cleaning decision we made," and get a faithful answer drawn from the project's own record.

## Leveling Up (optional, when a project matures)

Once the basics are second nature, ask Claude about these:
- **A citable snapshot (DOI).** Connect the project to Zenodo so a tagged release gets a permanent DOI you can cite in a paper.
- **A citation file.** Add a `CITATION.cff` so others know exactly how to cite your work.
- **Protecting the main version.** Turn on branch protection so changes to main must go through a reviewed proposal.
- **Templates.** Add issue and pull-request templates so every problem and change is described consistently.
- **Large-file handling.** Use Git LFS for large binary files that genuinely need to live with the project.

## Plain-Language Glossary

- **Repository (repo)** — the folder holding your whole project and its full history.
- **Commit** — a saved snapshot of your work with a short note; like a dated lab-notebook entry.
- **Branch** — a private copy of the project for trying or fixing something without disturbing the working version.
- **Issue** — a logged note on GitHub describing a problem, question, or task.
- **Pull request (PR)** — a proposal to merge a branch's changes into the main project, with a description and a review step.
- **GitHub Flow** — the standard loop: branch → commit → pull request → review → merge → delete branch.
- **Pull-request review** — the step where a change is read and either commented on, approved, or sent back for changes before merging.
- **Task list** — checkboxes (`- [ ]`) inside an issue that break it into smaller steps.
- **Milestone** — a named goal (often with a due date) that groups issues and shows progress toward it.
- **Roadmap** — a short description of where the project is and what's coming next.
- **Tag / release** — a permanent, named bookmark of the project at a moment in time (e.g. a submission).
- **Lockfile** — a saved list of the exact software versions your project uses, so it can be re-run identically.
- **`.gitignore`** — a list of files Git should not save (large data, outputs, secrets).
- **License** — the file that says how others are allowed to use your code and data.
- **Merge** — folding one branch's changes into another (usually into the main version).

## Quick Reference

- New idea or fix → **branch** (`experiment/…` or `fix/…`), then the **GitHub Flow** loop (branch → commit → PR → review → merge → delete).
- Something wrong or unresolved → **issue** (with a label); break big work into **task-list checkboxes** or **sub-issues**.
- Group issues toward a deadline → **milestone**; name milestones/tags after paper stages (`submitted`, `revision-1`).
- Every save → **note the *why*** (short imperative summary, one logical change) and **credit Claude**.
- Fixing a problem → **link the issue** (`Closes #…`) in the proposal; mentioning `#12` anywhere auto-links.
- Sharing work-in-progress → **draft pull request**; solo work still gets a PR as a self-review.
- Raw data → **never edited**; processed data → **always validated** (Claude asks if checks are missing; use pandera / assertr).
- **Never commit secrets** → keep them in an ignored `.env`; if one leaks, **rotate first**, then scrub history.
- Notebooks → strip outputs with **nbstripout** before committing.
- Every project → commit the **lockfile**, a **master script** that rebuilds everything with **relative paths**, a **README** with "how to reproduce," and a **LICENSE** (code vs data); milestones → **tag a release**.
- Failed experiment → **record why and keep it**, don't delete.
- Big or sensitive data → **keep out of GitHub**, note where it lives.
- Figure in an **issue/PR description** → link its **full `raw.githubusercontent.com` address** (commit it first); project-relative paths like `figures/x.png` only render inside committed files such as the README.

## Further Reading

The practices above are drawn from established, publicly documented sources. For readers who want to go deeper:

- **GitHub's own documentation** — [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow), [Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues), [Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects), [Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones), [Pull-request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews), [Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection), [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
- **Social-science-specific** — Gentzkow & Shapiro, ["Code and Data for the Social Sciences"](https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf); [Project TIER Protocol 4.0](https://www.projecttier.org/tier-protocol/protocol-4-0/); [AEA Data Editor template README](https://social-science-data-editors.github.io/template_README/).
- **Reproducibility & open science** — [The Turing Way](https://book.the-turing-way.org/); Wilson et al., ["Good Enough Practices in Scientific Computing" (2017)](https://doi.org/10.1371/journal.pcbi.1005510); Perez-Riverol et al., ["Ten Simple Rules for Taking Advantage of Git and GitHub" (2016)](https://doi.org/10.1371/journal.pcbi.1004947); Sandve et al., ["Ten Simple Rules for Reproducible Computational Research" (2013)](https://doi.org/10.1371/journal.pcbi.1003285).
- **Tools & conventions** — [pandera](https://pandera.readthedocs.io/) / [Great Expectations](https://greatexpectations.io/) (data validation), [nbstripout](https://github.com/kynan/nbstripout) (notebooks), Chris Beams, ["How to Write a Git Commit Message"](https://cbea.ms/git-commit/), [Choose a License](https://choosealicense.com/).

## Installing This Skill System-Wide

When this skill lives inside a project at `.claude/skills/github-for-research/`, it is active automatically whenever you work inside that project. To use it in **any** project on your computer, copy or link it into your personal skills folder:

```
# copy it (replace the source path with wherever this skill lives)
cp -R /path/to/project/.claude/skills/github-for-research ~/.claude/skills/

# or link it, so it stays up to date with the original copy
ln -s /path/to/project/.claude/skills/github-for-research ~/.claude/skills/github-for-research
```

After that, Claude can use these practices in every project you work on.
