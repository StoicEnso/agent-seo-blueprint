---
title: Schema Types Reference — Google Rich Results and JSON-LD Templates
area: content
updated: 2026-05
verification: Checked against Schema.org and Google Search structured-data docs on 2026-05-31. Verify current docs before shipping because rich-result eligibility changes.
---

# Schema Types Reference — Google Rich Results and JSON-LD Templates

**What it is.** A practical catalog for choosing structured data during audits and content briefs. It separates:
1. Schema.org vocabulary support — the type/property exists in Schema.org.
2. Google Search rich-result support — Google may show an enhanced Search feature for that markup.
3. Low-visibility, changed, or unsupported Google features — markup may be harmless but produce no visible Search enhancement.

**When to use.**
- Step 3 of `workflows/site-audit.md` — detect stale, low-ROI, invalid, or missing structured data.
- Step 5 of `workflows/content-production.md` — select appropriate JSON-LD for a new page brief.
- AI-search audits — schema can help machine readability and entity clarity, but it is not a guaranteed AI citation lever.

---

## Format Guidance: Prefer JSON-LD

Use `<script type="application/ld+json">` for structured data unless a platform has a specific reason not to. JSON-LD is easier to maintain, validate, and keep separate from template markup than Microdata/RDFa.

**Rendering caveat:** For commercial or time-sensitive pages, include important schema in the initial HTML where possible. JavaScript-injected schema may be processed later or missed by some crawlers/fetchers.

**Validation rule:** Validate against the current Google rich-result docs and Schema.org before shipping. Search features change; unsupported structured data usually does not hurt Search, but it can create noise and false confidence.

---

## Structured Data Feature Families to Consider

Start from the current Google Search structured-data docs for rich-result eligibility. These common feature families are useful audit prompts when they match the actual page type; do not promise a visible rich result without validating the current docs.

| Feature / Type family | Primary use case | Notes |
|---|---|---|
| Article / BlogPosting / NewsArticle | News, sports, blog, long-form articles | Use `Article` family with publisher, author, dates, image. |
| BreadcrumbList | Site hierarchy | Broadly useful when it reflects the real site hierarchy. |
| Carousel | Sequential list/gallery | Must be combined with eligible item types such as Recipe, Course list, Restaurant, or Movie. |
| Course list | Course provider pages | Use for lists of courses, not random educational blog posts. |
| Dataset | Large data sets | Verify current Google support and required properties before recommending. |
| DiscussionForumPosting | Forum/community threads | For user-generated discussion pages. |
| Education Q&A / Q&A | Question-and-answer education or Q&A pages | Use only where page format is genuinely Q&A. |
| EmployerAggregateRating | Employer ratings | For hiring organizations with aggregate employer ratings. |
| Event | Live or virtual events | Include start/end date, location/virtual location, organizer, offers where relevant. |
| FAQPage | Frequently asked questions | Visibility is restricted; see “Restricted / low-visibility” below. |
| Image metadata / ImageObject | Image ownership/licensing metadata | Useful for Google Images where image rights matter. |
| JobPosting | Job listing pages | Requires strict freshness and removal when expired. |
| LocalBusiness | Physical/local businesses | Include NAP, opening hours, geo where truthful. |
| MathSolver | Math problem solver pages | Specific educational tool pages only. |
| Movie | Movie lists/details | Mainly entertainment/movie result features. |
| Organization | Brand/company entity | Use on home/about/contact; supports entity clarity. |
| Product / Offer / AggregateRating / Review | Product pages | Follow price, availability, merchant, review policy rules. |
| ProfilePage / Person | Author, creator, or organization profiles | Useful for authorship/entity/E-E-A-T clarity. |
| Recipe | Recipe pages | Requires actual recipe content. |
| Review snippet | Review/rating snippets | Strict self-serving review rules apply. |
| SoftwareApplication | Apps/software | Useful for SaaS/app pages when rating/offers are truthful. |
| Speakable | News text-to-speech | Narrow use case; verify eligibility. |
| Subscription and paywalled content | Paywalled pages | Helps distinguish paywall from cloaking when implemented correctly. |
| Vacation rental | Vacation property listings | Specific vertical. |
| VideoObject | Video pages / embedded video | Include thumbnail, upload date, duration, content/embed URL. |
| WebSite / WebPage | Site/page metadata | Useful entity scaffolding; verify any SearchAction/sitelinks-search-box expectation against current docs. |

---

## Restricted, Low-Visibility, or Changed Google Features

Do not over-sell these in briefs. They may be valid Schema.org, but Google Search visibility can be restricted, changed, or unavailable for the site/page type.

| Markup | Status | Audit action |
|---|---|---|
| FAQPage | Google has restricted FAQ rich-result visibility heavily. | For most commercial sites, treat as low visible benefit; not an error if present. Verify current docs for eligible contexts. |
| HowTo | Google visibility has changed over time and may not be useful for many sites. | Verify current docs before recommending; do not build a strategy around it. |
| Sitelinks Search Box / `WebSite` `SearchAction` | Google has retired the visible sitelinks-search-box feature. Unsupported markup is not usually an emergency. | Optional cleanup only; no ranking emergency. Keep `WebSite` for site/entity metadata if useful. |
| SpecialAnnouncement | Narrow emergency/announcement use case. | Avoid unless current docs explicitly match the site use case. |

**Audit severity guidance:** Invalid schema that blocks a rich result can be medium/high depending on page value. Unsupported-but-harmless legacy markup is usually low/medium cleanup, not a critical issue.

---

## Version and Support Caveat

Schema.org support does not equal Google rich-result support. If a type exists in Schema.org but not Google’s gallery, it may still help entity clarity, but do not promise a visible rich result. If a recommendation depends on a newly added, changed, or deprecated type/property, verify the live Schema.org and Google docs during the audit.

---

## Validation Checklist

Before including schema in a brief or recommendation:

1. `@context` is `"https://schema.org"`.
2. `@type` matches the real page/entity type.
3. The feature is supported by current Google docs if the goal is a Search rich result.
4. Required and recommended properties are present.
5. Property values match expected data types: URL, Date, Text, Number, Offer, Organization, Person, etc.
6. No placeholders (`TODO`, `[Business Name]`, fake ratings, fake reviews).
7. URLs are absolute and crawlable.
8. Dates are ISO 8601 and reflect the actual content state.
9. Ratings/reviews are truthful, visible to users, and policy-compliant.
10. Important schema appears in initial HTML where possible.

---

## Minimal Safe Templates

Replace placeholders with truthful, visible, verifiable data. Remove properties you cannot honestly fill.

### Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Company Name]",
  "url": "https://example.com/",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/example",
    "https://x.com/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "support@example.com"
  }
}
```

### LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "url": "https://example.com/",
  "telephone": "+44-0000-000000",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "postalCode": "[Postcode]",
    "addressCountry": "GB"
  },
  "openingHours": "Mo-Fr 09:00-17:00"
}
```

### Article / BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Title — concise and accurate]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]",
    "url": "https://example.com/authors/name"
  },
  "datePublished": "2026-05-31",
  "dateModified": "2026-05-31",
  "image": "https://example.com/article-image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "[Publisher Name]",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

### Product / Offer
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Product Name]",
  "image": "https://example.com/product.jpg",
  "description": "[Visible product description]",
  "brand": {
    "@type": "Brand",
    "name": "[Brand]"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "GBP",
    "price": "99.00",
    "availability": "https://schema.org/InStock"
  }
}
```

---

**Related.** `workflows/site-audit.md`, `workflows/content-production.md`, `references/playbooks/content/eeat-framework.md`, `workflows/geo-audit.md`.
