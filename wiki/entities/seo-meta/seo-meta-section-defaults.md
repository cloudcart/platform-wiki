---
type: entity
nav_path: "Entity → SEO Meta → Section defaults"
aliases: ["SEO meta section defaults", "marketing-seo-meta Vue page", "5 section meta cards", "Legacy seo-meta cookie", "Missing sections in Vue page", "Single Save SEO meta", "No SERP preview"]
tags: [entity, seo, marketing, meta-tags, vue]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[seo-meta]]. See the hub for the other aspects (fields, fallback chain, per-entity storage, multi-language storage, canonical / no-index).

# SEO Meta — Section defaults

## Identity

**Section defaults** are the page-type meta values the merchant manages from the [[marketing-seo-meta]] screen. They are the second layer of the [[seo-meta-fallback-chain|fallback chain]] — they apply to a storefront SECTION (e.g., the home page, the products listing, the blog index) when no per-entity override exists.

The new Vue version of [[marketing-seo-meta]] exposes **5 sections only**: Home, Contacts, Products, Vendors, Blog. The underlying SEO translation namespace contains entries for at least 16 sections in total; the missing 11+ are still editable in the **legacy Smarty** version of the page (reachable via a cookie escape hatch). All 5 sections save together with a **single global Save button** in one DB transaction.

## Aliases

- **Section defaults** / **Page-type defaults** / **Section meta** / **Per-section meta**.
- **`marketing-seo-meta` Vue page** / **Meta settings page** / **SEO Meta screen**.
- **Legacy Smarty SEO Meta page** / **Old SEO Meta page** — reachable via the `marketing-seo-meta=old` cookie.
- **Section Home** / **Section Contacts** / **Section Products** / **Section Vendors** / **Section Blog** — the 5 cards.

## Key Attributes

| Aspect | Behaviour |
|--------|-----------|
| **Where it lives** | [[marketing-seo-meta]] — `/admin/marketing/seo/meta` (verify) |
| **Sections exposed (Vue)** | 5 cards: Home, Contacts, Products, Vendors, Blog |
| **Sections in underlying namespace (NOT in Vue)** | `cart`, `checkout` (sub-pages), `account` (sub-pages), `login`, `register`, `search.results`, `shops`, `wishlists`, `product` (per-product fallback), `category` (per-category fallback), `vendor` (per-vendor fallback) |
| **Legacy page escape hatch** | Set the `marketing-seo-meta=old` cookie. The merchant is then routed to the legacy Smarty page that exposes all 16 sections. |
| **Fields per card** | 2 inputs: `seo.<section>.title` (text input) + `seo.<section>.description` (textarea). |
| **Save button** | ONE global Save button at the page level. Changing any field across any card and clicking Save writes all 5 sections in one DB transaction (different from [[marketing-seo]] where each card saves independently). |
| **Submit payload** | Flat `{translations: {"seo.home.title": "...", "seo.home.description": "...", ...}}` map. Server upserts each row inside a DB transaction. (verify) |
| **Toast on success** | *"Saved Successfully"* |
| **SERP preview** | NONE in the Vue rewrite. The legacy Smarty version had a Google snippet preview ("Please enter SEO title and description to preview how your website will be listed in Google search"). NOT ported. |
| **Character counter** | NONE in the Vue rewrite. The fields are plain text inputs with no length cap and no character counter. Google's ~60-character title / ~160-character description guidance is documentary only — merchants who type 300-character titles save them unchanged, and Google truncates at render time. |
| **Length validation** | NONE — the platform does not warn or truncate. |
| **Merge tags / variables** | NONE on per-section fields. `{{store_name}}` and other merge tags would render as literal text. The per-section fields are plain literal strings; `{$name}` / `{$price}` substitution applies only to per-entity SEO Spinner variations (see [[seo-meta-fields]]). |
| **Per-language** | Yes — each saved value is for the active storefront language at save time. To edit meta for a different language, switch the storefront language in [[settings-translations]] and re-visit this page. See [[seo-meta-multilang-storage]]. |
| **Per-theme** | Yes — each saved row is tied to the active storefront theme at save time. |
| **Plan gate** | NONE — included with every plan. |
| **Permission** | `marketing.seo` API permission group (verify). |

**The 5 sections cover the highest-traffic storefront URLs**: the home page, the contact page, the all-products listing, the all-vendors listing, and the blog index. These are the pages most likely to show up in branded search results, so they are the highest-value SEO meta surfaces. Sections excluded from the Vue page (cart, checkout, account, login, register, search results, wishlists, shops) are usually `noindex`'d or low-traffic for SEO purposes, which is why they were deprioritised in the rewrite.

**The legacy cookie escape hatch is the documented workaround** for merchants who need to edit cart / checkout / account meta. Set `marketing-seo-meta=old`, reload the page, and the legacy Smarty version with all 16 sections (plus the SERP preview and character counter) is served. This remains the supported path until the Vue rewrite is extended.

**Per-section meta is plain literal text** — no template variables, no merge tags, no SEO Spinner `{$name}` substitution. The merchant types the exact text they want rendered into `<title>` / `<meta name="description">`.

## Where it appears

- [[marketing-seo-meta]] — the Vue page itself. Single Save button at the page level.
- [[settings-translations]] — manages the storefront language switch. To edit the 5 section meta values for a non-default language, the merchant switches the storefront language here, then returns to [[marketing-seo-meta]] and re-types the values.
- The legacy Smarty version (via `marketing-seo-meta=old` cookie) — exposes all 16 sections plus the SERP preview and character counter that were dropped from the Vue rewrite.
- [[seo-handling]] — the concept hub mentions this Vue page as the high-impact subset of the 16-section SEO translation namespace.

## Related

- [[seo-meta]] — hub.
- [[seo-meta-fields]] — the field semantics on each card.
- [[seo-meta-fallback-chain]] — section defaults are Layer 2 of the fallback chain.
- [[seo-meta-multilang-storage]] — per-language and per-theme row format for the per-section translation rows saved here.
- [[seo-meta-per-entity]] — per-entity overrides win over the section default.
- [[marketing-seo-meta]] — the page itself.
- [[settings-translations]] — language switching.
- [[seo-handling]] — concept hub for the 10 SEO surfaces.

## Open Questions

None.
