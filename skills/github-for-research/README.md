# GitHub for Research — a Claude Code skill

A [Claude Code](https://claude.com/claude-code) **skill** that teaches research-grade GitHub practice to researchers who don't have a software background. You describe what you want in plain words; Claude does the mechanical git/GitHub work and follows the conventions the skill encodes — clear attribution, issues for problems, branches for experiments, careful data checking, reproducible environments, and a project history that reads like a lab notebook.

The skill itself lives at [`.claude/skills/github-for-research/SKILL.md`](.claude/skills/github-for-research/SKILL.md). **This README explains the reasoning behind what's in it, with links back to the sources** — so the choices are transparent and checkable.

> **This repository dogfoods its own advice.** It has a structured README, a `LICENSE` that splits code from prose, a `CITATION.cff`, a sensible `.gitignore`, and a commit history that credits Claude — exactly the practices the skill recommends.

---

## Install

The skill is active automatically in any project that contains it at `.claude/skills/github-for-research/`. To use it in **every** project on your machine, link it into your personal skills folder:

```bash
git clone https://github.com/gsbdarc/claude-skill-github-for-research.git
ln -s "$(pwd)/claude-skill-github-for-research/.claude/skills/github-for-research" \
      ~/.claude/skills/github-for-research
```

(Use `cp -R` instead of `ln -s` if you'd rather have a static copy.)

---

## Design philosophy

Three convictions shape every choice in the skill:

1. **Written for non-programmers.** The audience is researchers — economists, political scientists, sociologists, psychologists — not software engineers. Every practice is phrased as *something you ask Claude to do*, never as a command to memorize. Jargon is defined in a plain-language glossary.
2. **The history is a research output.** Following the lab-notebook framing in [The Turing Way](https://book.the-turing-way.org/) and Sandve et al.'s ["Ten Simple Rules for Reproducible Computational Research"](https://doi.org/10.1371/journal.pcbi.1003285), the skill treats commits, issues, and pull requests as the durable record of *what you did and why* — reconstructable months later.
3. **Correctness is not optional.** Data integrity checks are framed as unavoidable: Claude is instructed to **pause and ask** for validation whenever you request a data transformation without it.

---

## What's inside, and why

Each practice below is in the skill because it's documented in an established, citable source. Items are grouped by the section they live in.

### Attribution & transparency
Every Claude-made commit ends with a `Co-Authored-By: Claude …` line and every Claude-written PR notes it was AI-assisted. This makes the human/AI division of labor visible to co-authors, reviewers, and journals at a glance — a transparency norm that costs nothing and Claude adds automatically.

### Organizing your work (the largest addition)
The skill names the **[GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)** cycle explicitly — branch → commit → pull request → review → merge → delete — so researchers have one repeatable loop to internalize, and explains *why* it keeps the main version continuously working. On top of that loop it layers GitHub's own planning features, which the research community endorses in Perez-Riverol et al.'s ["Ten Simple Rules for Taking Advantage of Git and GitHub"](https://doi.org/10.1371/journal.pcbi.1004947):

- **[Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) as the unit of planning**, broken down with **[task-list checkboxes](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-task-lists)** and **[sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)**.
- **[Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)** and a **[roadmap](https://book.the-turing-way.org/project-design/pd-overview/project-repo/project-repo-roadmapping)** tied to research deadlines.
- **[Pull-request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)** — including draft PRs for work-in-progress experiments — and the full **[issue↔PR↔commit linking](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)** mechanics that thread the whole trail together.
- **Commit-message shape** follows Chris Beams' widely-cited ["How to Write a Git Commit Message"](https://cbea.ms/git-commit/): imperative summary, a body that explains *why*, one logical change per commit.

### Data integrity
Raw data stays read-only in `data/raw/`; derived data goes elsewhere and **always gets validation checks** ([Wilson et al., "Good Enough Practices in Scientific Computing"](https://doi.org/10.1371/journal.pcbi.1005510)). The skill names concrete tools so the advice is actionable rather than vague — **[pandera](https://pandera.readthedocs.io/)** as a lightweight Python default, **[Great Expectations](https://greatexpectations.io/)** for heavier pipelines, **[assertr](https://docs.ropensci.org/assertr/)/[pointblank](https://rstudio.github.io/pointblank/)** in R.

### Keeping the repo clean
- **`.gitignore`** seeded from GitHub's official [templates](https://github.com/github/gitignore) plus a data-science layer.
- **Secrets** never get committed; the skill encodes GitHub's own runbook — enable **[push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)**, and if a key ever leaks, **rotate first**, then scrub history with **[`git filter-repo`](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)**. Rotating first is the load-bearing insight — a history rewrite alone doesn't un-leak a key.
- **Notebooks** get **[nbstripout](https://github.com/kynan/nbstripout)** so committed `.ipynb` files carry code, not giant output blobs.

### Reproducibility
Beyond committing a lockfile, the skill adopts the social-science standard from [Gentzkow & Shapiro's *Code and Data for the Social Sciences*](https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf) and the [Project TIER Protocol](https://www.projecttier.org/tier-protocol/protocol-4-0/): **one master script that rebuilds every result**, **relative paths only**, and *don't version output you can cheaply regenerate*.

### Documentation
A **README with a "how to reproduce" section and a script→table/figure map**, modeled on the [Social Science Data Editors' template README](https://social-science-data-editors.github.io/template_README/) used across hundreds of published replication packages. And a **LICENSE** — with the non-obvious point (from [Choose a License](https://choosealicense.com/) and [GEP 2017](https://doi.org/10.1371/journal.pcbi.1005510)) that **code and data need *different* licenses**: permissive (MIT/BSD/Apache) for code, Creative Commons (CC0/CC-BY) for data and text.

---

## What we deliberately left out (for now)

To keep the skill approachable for a non-technical audience, several well-documented but higher-effort practices were intentionally **not** included in this version:

- **Containers** (Docker/[Binder](https://mybinder.org/)) and **continuous integration** (GitHub Actions).
- **FAIR** data framing and formal **data dictionaries / codebooks**.
- **Pre-registration workflows** (freezing a pre-analysis plan via a git tag or [OSF](https://osf.io/) before touching outcome data; confirmatory vs. exploratory separation).

These are real, valuable practices — they're simply the next tier. They're candidates for a future revision aimed at more advanced projects.

---

## Two honesty flags

Most of the skill maps to a specific citation. Two items are **reasonable syntheses** of the literature rather than verbatim from a single source, and the skill presents them as *conventions*, not rules:

1. **The "one milestone/tag per paper stage" mapping** (data → cleaning → analysis → writing → `submitted` → `revision-1` → `accepted`). The research-stage lists and the milestone/tag features are all documented; the exact one-to-one mapping is our packaging.
2. **The solo-vs-team pull-request split.** The pieces (self-review, assigning issues, requiring reviews) are documented; the "here's how a lone researcher adapts vs. a 3-person lab" framing is a synthesis.

---

## How this was built

The practices were compiled through multi-source web research (using Claude) across five bodies of documented guidance: social-science-specific sources (Gentzkow & Shapiro, Project TIER, the AEA Data Editor, BITSS), the reproducibility/open-science literature (The Turing Way, the PLOS "Ten Simple Rules" and "Good Enough Practices" papers), git/GitHub mechanics, GitHub's own official documentation, and research-software-engineering writeups on organizing work. Every retained practice traces to a source in the [Further Reading](.claude/skills/github-for-research/SKILL.md#further-reading) section of the skill.

---

## Sources

**GitHub documentation** — [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) · [About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) · [Task lists](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-task-lists) · [Sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues) · [Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) · [Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones) · [Pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) · [PR reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews) · [Linking PRs to issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) · [Autolinked references](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls) · [Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) · [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) · [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositys-settings-and-features/customizing-your-repository/licensing-a-repository) · [github/gitignore templates](https://github.com/github/gitignore)

**Social science** — Gentzkow & Shapiro, ["Code and Data for the Social Sciences"](https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf) · [Project TIER Protocol 4.0](https://www.projecttier.org/tier-protocol/protocol-4-0/) · [AEA / Social Science Data Editors template README](https://social-science-data-editors.github.io/template_README/) · [BITSS](https://www.bitss.org/)

**Reproducibility & open science** — [The Turing Way](https://book.the-turing-way.org/) · Wilson et al., ["Good Enough Practices in Scientific Computing" (2017)](https://doi.org/10.1371/journal.pcbi.1005510) · Perez-Riverol et al., ["Ten Simple Rules for Taking Advantage of Git and GitHub" (2016)](https://doi.org/10.1371/journal.pcbi.1004947) · Sandve et al., ["Ten Simple Rules for Reproducible Computational Research" (2013)](https://doi.org/10.1371/journal.pcbi.1003285)

**Tools & conventions** — [pandera](https://pandera.readthedocs.io/) · [Great Expectations](https://greatexpectations.io/) · [assertr](https://docs.ropensci.org/assertr/) · [nbstripout](https://github.com/kynan/nbstripout) · [jupytext](https://jupytext.readthedocs.io/) · Chris Beams, ["How to Write a Git Commit Message"](https://cbea.ms/git-commit/) · [Choose a License](https://choosealicense.com/)

---

## License & citation

- **Code** in this repository (snippets, config) is licensed under the [MIT License](LICENSE).
- **The skill prose** (`SKILL.md`) and this README are licensed **[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)** — reuse freely with attribution. (This split is the very code-vs-data licensing advice the skill gives.)
- To cite this skill, see [`CITATION.cff`](CITATION.cff).

🤖 Researched and assembled with [Claude Code](https://claude.com/claude-code).
