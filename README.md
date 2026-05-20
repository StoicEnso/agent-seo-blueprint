# agent-seo-blueprint

A comprehensive, agentic **SEO skill** for Claude Code (and compatible agents). It pairs a distilled SEO
**methodology** (mirrored from a full SEO course, searchable) with **runnable pipelines** that execute it against
live data — Ahrefs, Google Search Console, GA4, live SERP, and PageSpeed/Lighthouse — writing artifacts into a
per-project workspace.

> **Status:** private / unreleased. Not affiliated with or endorsed by any course author.

## What it does

- **Answer SEO questions grounded in a real methodology** — `search_course.py "<topic>"` returns the relevant lessons
  and the distilled playbooks to read.
- **Do the work end-to-end** via 5 workflows: research & ideation, content production, site audit, authority/links,
  and rank/traffic monitoring.
- **Ideate with customer personas** — summon Opus subagents that role-play ideal customers to surface content angles,
  search intents, and validate niches.

## Layout

```
SKILL.md                     # intent router + how-to-use
references/
  playbooks/                 # 36 distilled, original-wording playbooks (research/content/authority/foundations/maintenance)
  course-index/              # searchable mirror of all 62 lessons -> playbooks
  integrations/              # Ahrefs / GSC / GA4 / SERP / PageSpeed (API + browser-fallback docs)
  coverage-map.md            # proof every lesson maps to a playbook
workflows/                   # 5 job-oriented runbooks
agents/                      # ICP persona subagents + library
scripts/                     # search, workspace, report, + data-source helpers (Python stdlib only)
assets/                      # report / brief / keyword-map / outreach / monitoring templates
_source/                     # PRIVATE, gitignored — paid-course transcripts (NOT included in this repo)
```

## Install

```bash
git clone <this-repo> ~/.claude/skills/agent-seo-blueprint
```

That's it — the skill is then available to Claude Code. Quick checks:

```bash
cd ~/.claude/skills/agent-seo-blueprint
python3 scripts/search_course.py "programmatic seo"
python3 scripts/workspace.py status --path ./seo-workspace
```

Scripts are **Python 3 standard-library only** — no `pip install` required. Data-source API access is optional
(set keys via env vars named in your workspace `project.json`); without keys, the skill uses documented browser
fallbacks driven by Claude's Chrome integration.

## About the source material

The methodology is **distilled in original wording** from a paid SEO course. The course **transcripts are not
included** in this repo — they are private and live only in a gitignored `_source/` folder on the author's machine.
Everything shipped here (playbooks, index summaries, workflows) is original synthesis of methods and facts, which are
not copyrightable. If you own the course, see `_source/SOURCE.md` for how to add your own transcripts locally to enable
full-text search.

## License

Private / all rights reserved for now. A license will be chosen before any public release.
