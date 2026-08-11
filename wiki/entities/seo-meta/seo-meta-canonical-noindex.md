---
type: entity
nav_path: "Entity → SEO Meta → Canonical and no-index"
aliases: ["Canonical URL per page", "Per-page canonical_url", "No-index per page", "no_index_meta toggle", "CMS Page canonical", "CMS Page noindex", "OG image dimensions not validated", "SEO meta plan gates", "marketing.seo permission"]
tags: [entity, seo, marketing, canonical, noindex, cms-page]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[seo-meta]]. See the hub for the other aspects (fields, fallback chain, section defaults, per-entity storage, multi-language storage).

# SEO Meta — Canonical and no-index

## Identity

Of the 5 user-facing SEO Meta fields ([[seo-meta-fields|catalogued here]]), **two** are CMS-page-only: `canonical_url` and `no_index_meta`. They don't appear on Product / Category / Vendor / Blog Article editors. They are the per-page levers the merchant uses to:

- Point a CMS Page's canonical tag elsewhere (e.g., the thank-you page canonical points to the home page so it doesn't compete in search).
- Tell search engines NOT to index a specific CMS Page (thin content, internal-only landing pages, drafts).

This page also documents two non-validation gotchas: OG image dimensions are not platform-validated, and `no_index_meta` is NOT inherited from parent category to child products. Plan and permission gates are also covered here.

## Aliases

- **canonical_url** / **Canonical URL** / **`<link rel="canonical">`** / **Per-page canonical**.
- **no_index_meta** / **No-index meta** / **noindex toggle** / **`<meta name="robots" content="noindex">`**.
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

### `no_index_meta` — Per-CMS-page noindex

| Aspect | Behaviour |
|--------|-----------|
| **Carried by** | [[marketing-landing-pages|CMS Page]] only. (Categories in some platform versions also carry a `no_index_meta` flag — verify which entity types currently expose it.) |
| **HTML emitted (when ON)** | `<meta name="robots" content="noindex">` |
| **Typical use** | Thin product pages, internal-only landing pages, draft content the merchant wants reachable via direct link but not indexed by Google. |
| **NOT inherited** | Setting `no_index_meta = 1` on a Category does NOT propagate to products in that category. Each entity carries its own independent flag. Setting it on a Category only affects that category's listing page; products in that category render with their own per-product flag (or, if blank, are indexed). |
| **Relationship to site-wide deindex** | The site-wide deindex toggle on [[marketing-seo-deindex]] controls noindex for **filtered / sorted URL variants** of storefront pages (e.g., `/products?color=red`). This per-page `no_index_meta` is independent: it applies to the canonical URL itself. The two operate on different surface areas. |
| **Storage** | Column on the CMS Page row (and on Categories where supported). |

### OG image dimensions are not validated

The `og_image` field accepts any uploaded image regardless of size. The platform does NOT enforce or warn about:

- Facebook's recommended **1200×630** for `og:image`.
- LinkedIn's similar recommendations.
- Aspect ratio for Twitter / X card images.

A merchant who uploads a tiny 200×200 image or a giant 4000×3000 image saves it unchanged; the receiving social platform decides how to crop / scale / reject. The platform's only validation is the generic image-upload validation (file type, max size in MB) — nothing SEO-specific.

### `no_index_meta` is per-entity, not per-section

Note that the per-section meta defaults on [[marketing-seo-meta]] **do NOT** expose `no_index_meta` — there is no per-section noindex flag for "noindex the entire home page" or "noindex the entire blog index". To noindex an entire section, the merchant has to set `no_index_meta = 1` on the CMS Page implementing that section, or rely on the site-wide deindex toggle ([[marketing-seo-deindex]]) for filtered variants.

### Permission and plan gates

| Gate | Value |
|------|-------|
| **API permission group** | `marketing.seo` — the [[marketing-seo-meta]] page and per-entity SEO endpoints sit behind this permission. Merchants with restricted users must grant `marketing.seo` for the user to edit any SEO meta. |
| **Plan gate** | NONE — every plan supports SEO meta editing (per-section and per-entity). |
| **App gate** | [[apps-seo-spinner]] is an app — its bulk-generation features are gated by app installation. The underlying per-entity meta fields it writes to are universally available. |

## Where it appears

- **[[marketing-landing-pages]] (CMS Page editor)** — both `canonical_url` (text input) and `no_index_meta` (toggle) appear in the SEO section of the editor.
- **[[marketing-seo-canonical]]** — the site-wide canonical toggle that gates whether `canonical_url` is rendered at all.
- **[[marketing-seo-deindex]]** — the site-wide deindex toggle (different surface from per-entity `no_index_meta`).
- **[[category]] editor** — `no_index_meta` toggle (where supported — verify).
- **API permission management** — `marketing.seo` permission group.

## Related

- [[seo-meta]] — hub.
- [[seo-meta-fields]] — the field catalogue including these two CMS-only fields.
- [[seo-meta-per-entity]] — why CMS Pages have 2 extra fields the other entity types don't.
- [[seo-meta-fallback-chain]] — canonical / noindex don't participate in the meta-title fallback chain; they are independent flags.
- [[marketing-landing-pages]] — the CMS Page editor where these 2 fields live.
- [[marketing-seo-canonical]] — site-wide canonical toggle.
- [[marketing-seo-deindex]] — site-wide deindex of filtered URLs.
- [[seo-handling]] — the concept hub for the 10 SEO surfaces.
- [[apps-seo-spinner]] — bulk per-product meta generation app.

## Open Questions

None.
