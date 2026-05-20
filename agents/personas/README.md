# Persona library

Reusable ideal-customer profiles that the persona launcher (`../icp-persona.md`) loads
to summon Opus subagents during research and ideation. Saving a persona here means you
don't re-describe a buyer segment from scratch every time you research a new niche — you
load a profile, drop in the product/niche, and dispatch.

## How these are used

1. The main agent picks 3-6 personas that span the niche's segments (different budgets,
   roles, sophistication). It loads matching profiles from this folder.
2. For each, it fills the `{{PLACEHOLDERS}}` in `../icp-persona.md` from the profile's
   fields and launches one Opus subagent **per persona, all in parallel** (see the
   launch notes at the top of `icp-persona.md`).
3. The N raw outputs go to `../synthesizer.md`, which merges them into ranked angles,
   clustered keyword seeds, and a niche-validation verdict.

A profile here is **niche-agnostic** — it describes a *type of person*, not a reaction to
a specific product. The product/niche is supplied at launch time. The same
`indie-hacker-founder` can react to an SEO tool today and a fitness app tomorrow.

## File format

One Markdown file per persona, named `kebab-case.md`. Front-matter for quick scanning,
then the fields that map directly onto the launcher's placeholders.

```markdown
---
name: Short Persona Name
segment: one-line who-they-are
sophistication: low | medium | high
budget: free-only | low | medium | high
---

# <Persona Name>

- **Role & context** -> fills {{ROLE_AND_CONTEXT}}
- **Demographics / situation** -> fills {{DEMOGRAPHICS}}
- **Goals & constraints** -> fills {{GOALS_AND_CONSTRAINTS}}
- **Tech sophistication & stack** -> fills {{SOPHISTICATION_AND_STACK}}
- **Money / buying power** -> fills {{BUDGET_AND_BUYING_POWER}}
- **Voice & quirks** -> how they talk, what they care about, their biases (keeps role-play sharp)
```

Keep each profile tight (under ~40 lines). The launcher supplies the product and the
output structure; the profile only needs to make the person feel real and distinct.

## Building a good roster

- **Make personas genuinely different.** Two personas with the same budget and
  sophistication waste a parallel slot. Span the spectrum.
- **Include at least one skeptic / non-buyer.** The persona who'd never pay is a critical
  validation signal, not a wasted launch.
- **Match personas to the niche before launching.** A B2B SaaS niche and a hobbyist niche
  pull different rosters. Edit the product-fit on the fly or write a new profile.

## Included profiles

- `indie-hacker-founder.md` — solo technical founder shipping products, allergic to
  bloated pricing, lives on X/IndieHackers.
- `budget-conscious-smb-owner.md` — non-technical small-business owner, time-poor,
  cost-sensitive, wants results without learning the jargon.
