# Internal-linking source adaptation — 18 October 2026

Owner asked for the full Google-discovery method, a programmable route, a Landscapio homepage keyword audit, an app PR from Zara, and method PRs in both Agent SEO repositories. This change covers the reusable method and offline helper, not the app or a live release.

## Sources actually inspected

- Paul Vengeons: https://x.com/VengeonsP/status/2110831074787963098 (15 October). Complete main text, original annotated Google image and two visible replies were read on 18 October. No full-thread claim. No separate X Article or programmable code in the main post.
- A visible reply from @Quent_l recommends MaillageBooster by @Pierre_Rib. Its public store listing was resolved and read: https://chromewebstore.google.com/detail/maillagebooster/okbkojlihlckehofpgkgbiidoghjaang . Listing states version1.9.2, updated16October. No extension installation, package download, account grant or privacy/code verification.
- Google first-party link and `site:` operator guidance are linked in the playbook. They do not support a required five-link count or forced exact-match anchors.

## Retained

Choose one target/intent owner; use `site:domain "exact phrase"` to find existing discussions; inspect actual body context; add a descriptive in-body link only when useful; retain an inspectable source/target ledger.

## Narrowed or rejected

- Five links: bounded pilot heuristic, not a ranking threshold.
- Exact anchors: natural where appropriate, not mandatory or mechanically repeated.
- Every Google result should link: rejected. Footer matches, stale snippets, existing links, noncanonical aliases, protected pages and different reader intent must be excluded.
- Cheapest SEO lever / ranking lift: unverified source opinion, not a benchmark or result promise.
- One-click automation / local-only privacy / free-unlimited use: vendor claims, not independently tested guarantees. Browser permissions remain a separate decision.
- Automatic publication: rejected. The new helper reads saved HTML only; candidates cannot merge, deploy, request indexing or create schedules.

## Implementation boundary

The stdlib-only `scripts/internal_link_opportunities.py` is original code, not recovered vendor source. It reports exact-phrase candidates and exclusion reasons from a bounded capture manifest, requires canonical/same-origin/status checks, excludes selected boilerplate/anchors, hashes inputs, protects input files and labels review-only decisions. It makes no network requests. It is not a rendered crawler or semantic relevance model. Tests exercise success, duplicate/target/protected/hidden/linked/alias/noindex/path boundaries and CLI input preservation.

The private Landscapio audit and raw first-party query rows are deliberately not shipped. No installed skill, live site, merge, deployment, schedule, outreach, account or spending change is included. Existing topic architecture and ledger remain the single workflow; this adds a focused optimisation branch.
