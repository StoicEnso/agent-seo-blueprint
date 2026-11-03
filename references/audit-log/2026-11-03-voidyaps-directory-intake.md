# Void / Hanu Dotstore directory intake — 2026-11-03

## Sources and scope
- Owner supplied: https://x.com/voidyaps/status/2117211405430685874.
- Complete matching article: https://www.dotstore.io/blog/186-launchpads-to-list-your-startup-and-get-backlinks. All 186 ordered source rows and all 186 source listing identities were recovered. Screenshots show only rows 1–76; source DR values changed between the images and the live article, so these files use the dated article values, not a mixed snapshot.
- The article and its `SoftwareApplication.sameAs` metadata are discovery evidence. They do not prove first-party eligibility, current pricing, indexability or link behavior. The X comment link was not verified: the browser read timed out; the complete matching article was recovered independently from the publisher.

## Reconciliation
- 31 source rows already represented in main CSVs or the maintained directory guide.
- 60 rows represented in open directory-intake PRs; these are not claimed as merged.
- 77 additional unverified directory/launch/profile candidates in `assets/voidyaps-missing-candidates.csv`.
- 18 held or kept outside that generic queue: design/editorial/community/games routes, generic web directories without a project-fit case, submission services, unrelated tools, and a label/destination mismatch.
- All 186 rows remain in `assets/voidyaps-directory-intake-20261103.csv`, with source URLs, source-reported claims, destination identities, exact coverage evidence and decisions. No row is dropped from the audit.

Baseline checks included `main` and the existing `henry/launchrepo-directories-20260918`, `henry/launch94-20260920`, `henry/haris-intake-20260920`, `henry/missed-links-20260924`, `henry/directory-gap-intake-20261016` and `henry/rankinpublic-directory-intake-20261023` intakes. Candidate-bearing CSV bytes matched between the two repositories for all nine checked baseline files. Existing main rows are unchanged. Merge order is not assumed: recheck the current union before integrating any open PR.

Identity matching first uses source-listed domains, then compatible normalized/reviewed name aliases for legacy rows without domains. A known different domain is not overwritten by a similar name. Evidence is source identity only; it is not destination ownership certification. Preserve separate domains for `Launch`, `LaunchIt` and `Launchit`.

## Data-quality checks
- The source's broad “free” claim conflicts with its explicit prices and paid/conditional notes. These stay in `_unverified` fields; there is no all-free label or universal dofollow promise.
- [Clearity](https://clearity.nxgntools.com/) returned a CBT journal homepage, not a directory, on 2026-11-03.
- [AI Directories](https://aidirectori.es/) offered paid managed submissions and a discovery list on 2026-11-03; it is not a single direct directory placement.
- The `Linguix` source row points to `reviews.financesonline.com`; it is held for identity review, not silently relabelled.
- [DR Checker](https://drchecker.net/) mentioned eligible Domain Listings; its candidate remains unverified because the complete listing gate was not checked.
- Source-claimed low DR is not by itself a rejection rule. FeedMyStartup remains a research lead with audience and relevance checks.
- Nofollow, redirects, badge conditions and ranking-dependent links remain source claims; no live backlink is asserted.

## Use and limits
Use the existing verification pipeline and tracker. Check the actual project's eligibility, audience and geography; then inspect a destination-owned submit route, cost/moderation, public output, indexability and rendered links. No accounts, submissions, outreach, payments, live-site changes, skill installation, runtime changes, scheduling, merge or deployment occurred. This PR is research-data intake only.

## Validation
The intake tests enforce 186-row coverage, 77 unique additional domains, provenance, unchanged legacy candidate data, pending-versus-main separation, source-claim containment, identity disambiguation, exclusions and empty outcome fields. Run `python3 -m unittest discover -s tests -v` for the full repository suite. Local test results are recorded in the PR; no remote CI or ranking result is implied.

The first full-suite run exposed a pre-existing README/test count mismatch: main contains 67 playbooks, but its labels asserted 66. This PR corrects only those count labels and their matching assertions, as already proposed in the separate long-query review PR. It adds no playbook and does not import that PR’s other changes.
