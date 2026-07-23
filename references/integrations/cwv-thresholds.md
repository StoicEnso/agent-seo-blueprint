# Core Web Vitals Thresholds — Reference

**What it provides.** Current Core Web Vitals metric definitions, pass/fail thresholds, field-vs-lab interpretation, LCP diagnostic subparts, and common bottleneck patterns. Use during technical audits to calibrate PageSpeed Insights / CrUX findings.

**Verification:** Checked against Google/web.dev Web Vitals and LCP documentation on 2026-05-31.

**Consumed by:**
- `workflows/site-audit.md` — step 2 (technical audit — speed and Core Web Vitals).
- `references/integrations/pagespeed.md` — complements the PageSpeed API reference with field-data interpretation and LCP subpart context.

---

## Current Thresholds

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5s–4.0s | >4.0s |
| INP (Interaction to Next Paint) | ≤200ms | 200ms–500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1–0.25 | >0.25 |

**Key facts:**
- Google evaluates CWV at the **75th percentile** of page loads, segmented across mobile and desktop.
- A page passes Core Web Vitals when all three metrics meet the “good” target at p75.
- Prefer real-user field data (CrUX / Search Console / RUM) for audit conclusions. Use Lighthouse lab data to diagnose what to fix.
- Page-level and origin-level data can differ. If PSI lacks URL-level field data, it may show origin-level data; note that explicitly.
- Run and report mobile first. Mobile performance often drives the hardest user-experience constraints.

---

## INP — Key Facts

- INP is the current Core Web Vital for interactivity and replaced FID as the stable interactivity metric in 2024.
- INP measures the latency of user interactions across the page lifecycle; high INP usually points to main-thread JavaScript, heavy event handlers, rendering work, or large DOM updates.
- Lighthouse may use lab proxies and diagnostics; field INP from CrUX/RUM is the audit source of truth.

---

## LCP Diagnostic Subparts

LCP can be decomposed into four subparts. Use this decomposition to identify the bottleneck instead of treating LCP as a single opaque number.

| Subpart | What it measures | Audit target |
|---|---|---|
| TTFB (Time to First Byte) | Time until the first byte of HTML arrives | Keep low; >800ms is usually worth investigating |
| Resource load delay | Gap between TTFB and when the LCP resource request starts | Minimize; preload/prioritize the LCP resource |
| Resource load duration | Time to download the LCP resource | Compress/resize/serve from CDN |
| Element render delay | Gap between resource loaded and element painted | Reduce render-blocking CSS/JS and client-side reveal delays |

**Total LCP = TTFB + resource load delay + resource load duration + element render delay.**

Common interpretations:
- Slow TTFB → server/CDN/cache/database issue.
- High resource load delay → browser discovers hero image/video too late; preload/fetchpriority may help.
- High resource load duration → asset too large or network/CDN issue.
- High element render delay → render-blocking CSS/JS, hydration delay, hidden element, font delay, or client-side rendering.

---

## Field Data vs Lab Data

| Source | Type | Used for |
|---|---|---|
| CrUX (Chrome User Experience Report) | Field — real Chrome users | Audit conclusion / real-user performance evidence |
| PageSpeed Insights CrUX section | Field | Quick URL/origin read |
| Search Console Core Web Vitals report | Field | Portfolio view across many URLs |
| RUM analytics | Field | Best site-owned monitoring if implemented correctly |
| Lighthouse / PSI diagnostics | Lab | Debugging causes and testing candidate fixes |
| Chrome DevTools / WebPageTest | Lab | Deep debugging |

**Rule:** Prefer field data for severity. Use lab data for diagnosis. If `field_data_crux` is null in `pagespeed_run.py` output, use Lighthouse as a proxy and say so in the finding.

---

## Common Bottleneck Patterns

### LCP
- Unoptimized hero image: resize, compress, serve WebP/AVIF, and use `fetchpriority="high"` or preload when appropriate.
- Render-blocking CSS/JS: inline critical CSS, defer non-critical JS, split bundles.
- Slow TTFB: add CDN/edge caching, server caching, database/query optimization.
- Client-side rendering delays: server-render or statically render key content and hero elements.
- Web font delay: use `font-display: swap` and preload truly critical fonts.

### INP
- Long tasks on the main thread (>50ms): split work, yield between chunks, move heavy work off-thread.
- Heavy event handlers: debounce/throttle, reduce synchronous state updates.
- Excessive hydration or large JS bundles: code split and delay non-critical interactivity.
- Large DOM updates: virtualize long lists and batch reads/writes.
- Third-party scripts: load async/defer or behind interaction facades.

### CLS
- Images/iframes without dimensions: add width/height or `aspect-ratio`.
- Injected banners/ads above content: reserve space before load.
- Font swaps: use sensible fallback metrics and `font-display`.
- Late-loading embeds: fixed containers/placeholders.

---

## Severity Mapping for Audit Findings

Use these when translating `pagespeed_run.py` output into `site-audit.md` findings:

| Field data result | Severity | Note |
|---|---|---|
| LCP >4.0s (CrUX p75) | Critical | Severe loading problem on affected URL/template |
| LCP 2.5–4.0s (CrUX p75) | High | Meaningful user-experience issue on affected URL/template |
| LCP ≤2.5s (CrUX p75) | Pass | No finding needed |
| INP >500ms (CrUX p75) | Critical | Severe responsiveness issue |
| INP 200–500ms (CrUX p75) | High | Needs interactivity work |
| INP ≤200ms (CrUX p75) | Pass | No finding needed |
| CLS >0.25 (CrUX p75) | High | Severe layout instability |
| CLS 0.1–0.25 (CrUX p75) | Medium | Improve stability |
| CLS ≤0.1 (CrUX p75) | Pass | No finding needed |
| CrUX data null | Use Lighthouse proxy | State “lab proxy; no field data available” |

**Related.** `references/integrations/pagespeed.md`, `workflows/site-audit.md`.
