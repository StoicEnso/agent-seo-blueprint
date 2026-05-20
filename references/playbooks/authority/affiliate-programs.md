---
title: affiliate-programs
area: authority
source_lessons: ["04-06"]
tools: [ahrefs, hunter, rewardful, stripe, search-console]
---

# affiliate-programs

**What it is.** Using an affiliate program as a backlink engine: affiliates are financially motivated to publish links to you, so a well-structured program can generate hundreds of relevant, decent-DR links at low cost.

**When to use.**
- You have a paid product with a measurable conversion rate you can quote to affiliates.
- Competitors are getting links from review/affiliate sites you'd like to win over.
- You want a scalable, mostly-passive source of in-content backlinks (not just one-off outreach).

**Method.**
1. Set up the program with a tool that produces clean, direct links rather than ugly redirects. The course's pick is Rewardful, which appends a simple `?via=<slug>` parameter to your own URL — so the affiliate link points straight at your domain and the backlink value lands on you (a redirect-through-the-affiliate-platform link does not pass that value).
2. Use a platform that integrates with your billing for easy payouts. Rewardful integrates directly with Stripe and supports Wise/PayPal payouts; the cost is justified once you're paying out a few commissions a month.
3. Set commissions generously — higher than competitors. Affiliates promote whoever pays best, so out-bidding rivals on commission directly increases how often you get recommended and linked.
4. Mine competitor affiliates in Ahrefs to recruit: open Site Explorer for a competitor, go to Backlinks, and filter Target URL to "contains" the affiliate parameter (e.g. `?via=` for Rewardful; try other platforms' tags too). This surfaces every page running that competitor's affiliate links.
5. For each affiliate, pull the contact via Hunter.io and draft an outreach email (for user review, never auto-sent): note you saw them promoting [competitor], state you're a stronger product, offer a higher commission, and quote your conversion rate so they can compute expected earnings (e.g. "~5% convert, ~$X each").
6. For top-tier, high-DR sites already ranking #1, offer a bespoke VIP/elevated commission to become their top pick. The course example: emailing a DR ~94 roundup site a special high affiliate fee got the product promoted as the top recommendation, driving both sales and a powerful link.
7. Protect your link profile from affiliate spam: affiliates may scatter your URL on junk low-DR sites. Periodically review new referring domains and disavow the bad ones in Google Search Console (upload a disavow file telling Google to ignore those links).

**Decision criteria / heuristics.**
- A clean `?via=` style link that resolves to your domain is worth recruiting for; a redirect that bounces through the platform passes little/no link value — deprioritize.
- Quote conversion rate, not just commission — affiliates care about expected dollars per click.
- Reserve VIP rates for the few sites whose placement actually moves rankings (high-DR, exact-niche, currently ranking).
- Disavow only links you genuinely don't endorse; don't over-prune legitimate ones.

**Example.** You target a competitor with ~700 affiliate links. In Ahrefs you Site Explorer them, set Target URL contains `?via=`, and export the affiliate pages. Hunter.io gives you emails. You draft (and the user reviews/sends) a pitch: "Saw you promote [competitor] — we convert ~5% and pay double their commission." Several switch. Separately, you offer a DR ~94 review site a VIP commission and they make you their top pick. Later, a junk site spams your `?via=` link; you add that domain to your Search Console disavow file.

**Pitfalls.**
- Using an affiliate platform whose links redirect through their domain — you lose the backlink value.
- Setting stingy commissions — you'll lose affiliates (and their links) to competitors who pay more.
- Ignoring affiliate-driven spam links until they hurt your profile; review and disavow proactively.
- Auto-sending recruitment emails — draft for user review first.

**Related.** [[link-stealing]] (same Ahrefs+Hunter motion, different target), [[manual-outreach]] (you can also be the affiliate's case study), [[understanding-authority]], [[linkbuilding-what-not-to-do]] (disavow workflow). Course ref: 04-06.
