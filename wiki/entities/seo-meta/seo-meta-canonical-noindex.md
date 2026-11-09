---
type: entity
nav_path: "Entity → SEO Meta → Canonical and no-index"
aliases: ["Canonical URL per page", "Per-page canonical_url", "No-index per page", "CMS Page canonical", "CMS Page noindex", "OG image dimensions not validated", "SEO meta plan gates", "marketing.seo permission"]
tags: [entity, seo, marketing, canonical, noindex, cms-page]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[seo-meta]]. See the hub for the other aspects (fields, fallback chain, section defaults, per-entity storage, multi-language storage).

# SEO Meta — Canonical and no-index

## Identity

Of the SEO Meta fields ([[seo-meta-fields|catalogued here]]), `canonical_url` is CMS-page-only (curated selections carry their own canonical too). The merchant uses it to point a CMS Page's canonical tag elsewhere, e.g. the thank-you page to the home page so it doesn't compete in search.

**There is no per-page noindex field.** No CMS page, product, category, vendor or article has a noindex switch; the platform has no `no_index_meta`.

This page also covers OG image non-validation and the plan and permission gates.

## Aliases

- **canonical_url** / **Canonical URL** / **`<link rel="canonical">`** / **Per-page canonical**.
- **Per-page noindex / noindex toggle** — does not exist; see below.
- **OG image dimensions** — the unvalidated upload.
- **`marketing.seo` permission** — the API gate.

## Key Attributes

### `canonical_url` — Per-CMS-page canonical

| Aspect | Behaviour |
|--------|-----------|
| **Carried by** | [[marketing-landing-pages|CMS Page]] only. Not on Product / Category / Vendor / Blog Article. |
| **HTML emitted** | `<link rel="canonical" href="<url>">` |
| **Typical use** | The thank-you-page canonical points to the home page so the thank-you URL doesn't compete in search results. Affiliate landing pages canonical to the master campaign page. Duplicate-content variants canonical to the primary URL. |
| **Relationship to site-wide canonical** | The site-wide canonical toggle on [[marketing-seo-canonical]] controls whether the canonical tag renders **at all** on storefront pages. This per-page `canonical_url` field controls the **value** when it does. With the site-wide toggle OFF, the per-page value has no effect. |
| **Validation** | None on the URL format itself (verify). |
| **Storage** | Column on the CMS Page row. |

### No per-page noindex

A storefront page is `noindex` only through the platform's own rules ([[seo-canonical-noindex]]): filtered and sorted listings, the always-noindex system pages (cart, checkout, account, sign-in, compare), `/products`, the 404 page and demo stores. The Deindex card on [[marketing-seo-deindex]] governs only the filtered listings. To keep a specific page out of search the merchant can deactivate it (it then answers 404), redirect it ([[marketing-seo-301-redirects]]), point a CMS page's canonical elsewhere, or add a `Disallow` line in robots.txt ([[marketing-seo-robots]]), which stops crawling rather than indexing.

### OG image dimensions are not validated

The `og_image` field accepts any uploaded image regardless of size. The platform does NOT enforce or warn about:

- Facebook's recommended **1200×630** for `og:image`.
- LinkedIn's similar recommendations.
- Aspect ratio for Twitter / X card images.

A merchant who uploads a tiny 200×200 image or a giant 4000×3000 image saves it unchanged; the receiving social platform decides how to crop / scale / reject. The platform's only validation is the generic image-upload validation (file type, max size in MB) — nothing SEO-specific.

### Permission and plan gates

| Gate | Value |
|------|-------|
| **API permission group** | `marketing.seo` — the [[marketing-seo-meta]] page and per-entity SEO endpoints sit behind this permission. Merchants with restricted users must grant `marketing.seo` for the user to edit any SEO meta. |
| **Plan gate** | NONE — every plan supports SEO meta editing (per-section and per-entity). |
| **App gate** | [[apps-seo-spinner]] is an app — its bulk-generation features are gated by app installation. The underlying per-entity meta fields it writes to are universally available. |

## Where it appears

- **[[marketing-landing-pages]] (CMS Page editor)** — `canonical_url` (text input) in the SEO section of the editor.
- **[[marketing-seo-canonical]]** — the site-wide canonical toggle that gates whether `canonical_url` is rendered at all.
- **[[marketing-seo-deindex]]** — the site-wide deindex toggle for filtered listings.
- **API permission management** — `marketing.seo` permission group.

## Related

- [[seo-meta]] — hub.
- [[seo-meta-fields]] — the field catalogue.
- [[seo-meta-per-entity]] — which fields each entity type carries.
- [[seo-meta-fallback-chain]] — canonical does not take part in the meta-title fallback chain.
- [[marketing-landing-pages]] — the CMS Page editor where the canonical field lives.
- [[marketing-seo-canonical]] — site-wide canonical toggle.
- [[marketing-seo-deindex]] — site-wide deindex of filtered URLs.
- [[seo-handling]] — the concept hub for the 10 SEO surfaces.
- [[apps-seo-spinner]] — bulk per-product meta generation app.

## Open Questions

None.
