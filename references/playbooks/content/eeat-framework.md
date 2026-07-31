---
title: E-E-A-T Evaluation Framework
area: content
type: reference
updated: 2026-05
verification: Checked against Google Search helpful-content and spam-policy docs on 2026-05-31. This is an operational review checklist, not an official Google scoring model or direct ranking-factor formula.
---

# E-E-A-T Evaluation Framework

**What it is.** An operational review checklist for evaluating Experience, Expertise, Authoritativeness, and Trustworthiness — the quality dimensions Google asks creators and quality raters to consider when judging whether content is helpful, reliable, and people-first.

**Important framing.** Google says E-E-A-T itself is **not** a single specific ranking factor. Google's systems use many signals that can identify content with strong E-E-A-T. Trust is the most important dimension; Experience, Expertise, and Authoritativeness contribute to trust. YMYL topics carry the highest bar, but competitive non-YMYL pages still benefit from clear authorship, evidence, originality, and transparent purpose.

**When to use.**
- Step 5 of `workflows/site-audit.md` — review content quality and trust signals on key pages.
- Step 6 of `workflows/content-production.md` — confirm a new brief includes the evidence and attribution needed to be credible.
- After traffic drops — identify pages that look search-engine-first, generic, outdated, anonymous, or insufficiently supported by first-hand value; treat this as one diagnostic lane, not proof of cause.

---

## Google-Aligned Principles

Use these as the first pass before applying the checklist:

1. **People-first purpose.** The page should exist to help the intended audience, not primarily to capture search traffic.
2. **Original value.** Prefer original information, reporting, research, analysis, examples, screenshots, test results, or first-hand observations over rephrased commodity content.
3. **Clear “Who, How, and Why.”** Make it easy to understand who created the content, how it was produced or verified, and why it exists.
4. **Trust is the gate.** If a page has deceptive claims, hidden ownership, missing business identity, exposed security issues, or unsupported advice, treat that as the priority issue before polishing expertise/authority signals.
5. **YMYL gets the strictest bar.** Health, finance, legal, safety, civic, and other high-impact topics need stronger sourcing, review, credentials, and update discipline.
6. **AI assistance is allowed when value is real.** Automation or AI use is not the problem; low-value, scaled, unreviewed, or manipulative content is.

---

## Review Order and E-E-A-T Checklist

Do **not** present these as Google weights or a ranking formula. Use them as an internal audit structure. Trust comes first because Google explicitly frames Trust as the most important member of the E-E-A-T family; the other dimensions explain why a page deserves trust.

| Dimension | Review question | What strong evidence looks like |
|---|---|---|
| Trustworthiness | Can users understand and trust who is behind this page and why it exists? | Clear owner, contact/about/policies where appropriate, supported claims, no deceptive UX, safe commercial terms. |
| Expertise | Does the creator/reviewer demonstrably know the subject? | Named expert/reviewer or accountable organization, accurate depth, current facts, high-quality sources. |
| Experience | Is there first-hand evidence behind the content? | Original screenshots/photos/data, tests, case studies, usage notes, specific examples, limitations. |
| Authoritativeness | Do others recognize this source/entity as credible in the topic? | Relevant mentions, citations, reviews, backlinks, credentials, entity consistency, topic depth. |

### Trustworthiness — review first

**Signals to check:**
- [ ] HTTPS with valid, non-expired certificate.
- [ ] Clear business or publisher identity: About, Contact, privacy policy, terms where appropriate.
- [ ] Clear authorship or editorial ownership where users would expect it.
- [ ] Claims are supported by citations, evidence, examples, or transparent methodology.
- [ ] Commercial pages include pricing, refund/cancellation terms, shipping/availability where relevant.
- [ ] No deceptive UI, hidden ads, cloaking, misleading affiliate framing, or manipulative claims.
- [ ] Corrections/update history is visible for information that changes over time.

If trust is weak, raise that finding directly. Do not hide it behind a numeric average.

### Expertise

**Signals to check:**
- [ ] Named author, reviewer, or accountable organization with relevant credentials or demonstrated knowledge.
- [ ] Technical depth fits the topic and audience.
- [ ] Factual claims are current and easily verifiable.
- [ ] Sources are high-quality and not circular.
- [ ] The page avoids shallow “best practice” filler and explains tradeoffs, constraints, and edge cases.

### Experience

**Signals to check:**
- [ ] First-hand examples: “we tested,” “I built,” “our benchmark,” “customer result,” “field note.”
- [ ] Original screenshots, photos, data, demos, case studies, or before/after evidence.
- [ ] Specific process details that a generic AI summary would not know.
- [ ] Product/service reviews include actual usage evidence, not just spec-sheet rewriting.
- [ ] The content discloses limitations, failures, and context where appropriate.

### Authoritativeness

**Signals to check:**
- [ ] The site or author is cited by reputable external sources.
- [ ] The brand has consistent entity signals: sameAs profiles, schema, social profiles, directory listings, third-party mentions.
- [ ] Topical coverage shows depth across related questions, not one isolated article.
- [ ] Backlinks/mentions come from relevant sources, not obvious link schemes.
- [ ] Reviews, testimonials, case studies, awards, certifications, or media mentions are visible where relevant.

---

## AI-Assisted Content Quality Tiers

Use these as internal audit tiers. They are not official Google labels; they translate Google’s people-first and spam-policy guidance into practical review buckets.

| Tier | Description | Audit interpretation |
|---|---|---|
| Human-led / AI-assisted | Human expert directs, edits, fact-checks, adds original evidence | Acceptable when useful and accurate |
| Reviewed AI draft | AI drafts; knowledgeable human reviews and adds context/sources | Acceptable for low-risk pages; improve with first-hand value |
| Scaled generic content | Many pages generated from templates with little unique value | High-risk; inspect for search-engine-first intent and thin value |
| Spam / manipulation | Automation used primarily to manipulate rankings or produce unhelpful pages | Critical; remove or rebuild |

**Review questions:**
- Is the use of automation disclosed where users would reasonably care?
- Who verified the facts?
- What original value was added beyond summarizing existing pages?
- Would a user still find this useful if search engines did not exist?

---

## Spam and Quality Abuse Checks

Cross-check weak pages against current Google spam-policy themes:

- **Scaled content abuse:** large volumes of pages made primarily to manipulate rankings and not help users.
- **Site reputation abuse:** third-party content hosted mainly to exploit a strong domain’s reputation.
- **Expired domain abuse:** repurposing expired domains primarily to manipulate rankings with low-value content.
- **Scraping / thin rewriting:** copying or lightly rephrasing other pages without substantial added value.
- **Keyword stuffing / hidden text / link spam:** classic manipulation signals.
- **Cloaking or inaccessible JS-only content:** different or inaccessible content for crawlers/users can create trust and indexation issues.

---

## Severity Guide

Use ordinary audit severity, not a pseudo-scientific E-E-A-T score:

| Severity | Use when |
|---|---|
| Critical | The page is deceptive, unsafe, materially wrong, spammy, or lacks credible ownership in a high-stakes/YMYL context. |
| High | Trust/authorship/evidence gaps materially weaken user confidence, or create a plausible search-quality risk, on an important page. |
| Medium | The page is basically useful but would benefit from stronger sourcing, first-hand proof, clearer author/reviewer information, or freshness. |
| Low | Maintenance/polish: richer media, more examples, better entity consistency, or update notes. |

**Improvement actions:** add author/reviewer accountability, first-hand examples, citations, original screenshots/data, clear editorial purpose, current facts, and relevant third-party proof.

**Pitfalls.**
- Treating E-E-A-T as a meta-tag checklist. It is a quality/trust culture, not one implementation task.
- Over-emphasizing author bios while the page itself remains generic.
- Assuming AI usage is automatically bad. The issue is whether the output is useful, accurate, reviewed, and enriched.
- Applying the same bar to all topics. YMYL and high-stakes pages need stronger evidence and review.

**Related.** `references/playbooks/content/content-fundamentals.md`, `references/playbooks/content/content-what-not-to-do.md`, `references/playbooks/foundations/seo-and-ai-future.md`, `workflows/site-audit.md`, `workflows/content-production.md`.
