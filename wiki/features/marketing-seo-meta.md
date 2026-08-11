---
type: feature
nav_path: "Marketing → Seo → Meta"
route_name: seo-meta
route_path: /admin/marketing-new/seo/meta
aliases: ["Meta settings", "SEO meta", "Meta information", "Meta titles", "Meta descriptions", "Мета информация", "Мета настройки", "Мета заглавия"]
tags: [marketing, seo, meta-tags, translations]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---
# Meta settings (per-section meta titles & descriptions)

## Purpose

This screen lets the merchant **override the meta title and meta description** rendered in the `<head>` of the storefront for five "section" pages — **Home**, **Contacts**, **Products** (the all-products listing), **Vendors** (the brands index), and **Blog** (the blog index). What the merchant types here is what Google shows in search-result snippets, and what Facebook / LinkedIn preview when those pages are shared.

This is a **page-type meta editor**, not a per-product or per-category one (those carry their own meta fields — see [[seo-meta-per-entity]]). It also does NOT touch sitemap, robots, canonical, or 301 redirects — those live on [[marketing-seo]] and [[marketing-seo-301-redirects]].

## Where to find it

Sidebar → Marketing → SEO → **Meta information**. The route is `/admin/marketing-new/seo/meta`. The page header shows the title "Meta settings"; the breadcrumb reads "Marketing → Meta settings".

This is the new version of the legacy `/admin/marketing/seo/meta` page. Setting a `marketing-seo-meta=old` cookie falls back to the legacy version (still needed for the sections the new page does not expose — see Business rules).

## What the merchant can do here

- Edit the meta title (`<title>…</title>`) and meta description (`<meta name="description" content="…">`) for each of the five sections.
- Save all five sections in a single submit — one global Save button.
- Clear a section's meta (save an empty string) — the storefront then falls back to the platform default.

### What the merchant CANNOT do here

- Set meta for an individual product, category, vendor, CMS page, or blog article — see [[seo-meta-per-entity]].
- Set Open Graph (`og:image`, `og:title`, `og:description`) overrides. The default sharing image is on [[marketing-seo]] ("Main sharing picture"); per-entity `og:*` is on the entity editor. See [[seo-sharing-og-image]].
- Edit per-language meta on one visit — meta is stored against the **current** storefront language. To edit another language, switch it in [[settings-translations]] first, then return. See [[seo-meta-multilang-storage]].
- Edit meta for the inner Checkout / Cart / Account / Login / Register / Search / Wishlist / Shops sub-pages — the new page exposes only 5 of the 16 sections (see Business rules).
- Add new sections — the section list is hard-coded.
- Use template variables / merge tags (no `{{store_name}}` substitution; the field is a literal string).

## Settings & fields

The page renders one **card per section**. Each card has two plain-text fields — no rich text, no character counter, and no Google-snippet preview on this new page (see Business rules).

| Section card | Storefront page | Translation keys |
|---|---|---|
| **Section Home** | home page (`/`) | `seo.home.title`, `seo.home.description` |
| **Section Contacts** | Contacts page | `seo.contacts.title`, `seo.contacts.description` |
| **Section Products** | all-products listing | `seo.products.title`, `seo.products.description` |
| **Section Vendors** | brands index | `seo.vendors.title`, `seo.vendors.description` |
| **Section Blog** | blog index | `seo.blog.title`, `seo.blog.description` |

Per card, two fields:

- **Meta title** (text input) — stored as `seo.<section>.title` for the current language; renders into the storefront `<title>` tag. Default = a platform fallback string (`Home`, `Contacts`, `Products`, `Brands`, `Blog`). No character limit enforced; Google truncates at ~60 chars in SERP snippets but the platform does not warn or truncate.
- **Meta description** (textarea) — stored as `seo.<section>.description`; renders as `<meta name="description" content="…">`. Default = a platform fallback string. No character limit enforced; Google truncates at ~160 chars. Blank = falls back to the language default.

There is one **Save** button (in the settings-wrapper header / floating bar). It writes all changed sections in a single submit; the success toast reads "Saved Successfully".

For the per-field storage model see [[seo-meta-fields]]; for the platform defaults each blank field falls back to, see [[seo-meta-section-defaults]].

## Business rules

### One global save, not per-card

Unlike [[marketing-seo]], all five cards submit together. The merchant changes any field across any card, clicks Save once, and every changed section is written in a single submit.

### Per-language AND per-theme storage

Each saved value is stored against the **storefront language at save time** and the **active storefront theme**. So the meta is both per-language and per-theme: switching theme later may not carry the values over, and a multi-language store needs one visit per language. The full storage model — natural key, the `is_translated` merchant-vs-default flag, no cross-store sharing — is on [[seo-meta-multilang-storage]].

### Fallback chain — what the storefront actually renders

For a section page, the platform resolves the `<title>` / `<meta name="description">` in order: per-entity override → the value saved on this screen (current locale) → the base language-file default → the English language-file default. So leaving a field blank here is safe. Full chain: [[seo-meta-fallback-chain]].

### Only 5 of 16 sections exposed in the new page

The SEO translation namespace also contains `cart`, `checkout`, `account` (and their sub-pages), `login`, `register`, `search.results`, `shops`, `wishlists`, plus the per-entity fallbacks `product` / `category` / `vendor`. These are editable on the legacy page but **NOT** exposed on the new page, which filters to the five top-level sections. Merchants needing the others must use the legacy page via the `marketing-seo-meta=old` cookie.

### No character counter / SERP preview (regression vs legacy)

The legacy page showed a Google SERP preview with character-count limits (the `seo.notice` string: "Please enter SEO title and description to preview how your website will be listed in Google search"). The new page has not yet ported this — the fields are plain inputs with no preview or counter.

### Blank = fall back, no row delete

Saving an empty string for a previously-set field clears the stored value to empty; the storefront then falls back to the language-file default. The screen never deletes a section, and saving here does not affect per-product or per-category meta (independent — see [[seo-meta-per-entity]]).

### Translation cache invalidates on save

After save the platform-wide translation cache is flushed by tag, so the next storefront page-load picks up the new meta without a deploy or manual purge. Because it is the platform-wide cache, that next request rebuilds cached translations for any key requested, not only SEO meta.

### Permission

Reading and saving on this screen sit behind the `marketing.seo` permission — a moderator without it cannot view or change these fields.

### Plan gates

None — included with every plan.

## Related

- [[marketing]] — parent navigation hub.
- [[marketing-seo]] — Main SEO settings (canonical, robots.txt, sitemap, sharing default OG image, RSS feed).
- [[marketing-seo-canonical]] — Canonical tag toggle on the Main SEO page.
- [[marketing-seo-deindex]] — Deindex filtered / sorted pages toggle on the Main SEO page.
- [[marketing-seo-meta-title]] — Pagination word for paginated meta titles on the Main SEO page.
- [[marketing-seo-301-redirects]] — per-URL 301 redirects manager.
- [[seo-meta-fields]] — entity: the per-field storage model.
- [[seo-meta-section-defaults]] — entity: platform fallback strings per section.
- [[seo-meta-fallback-chain]] — entity: full title / description resolution order.
- [[seo-meta-multilang-storage]] — entity: per-language + per-theme row model.
- [[seo-meta-per-entity]] — entity: per-product / category / vendor / blog meta overrides.
- [[seo-sharing-og-image]] — default Open Graph sharing image.
- [[apps-seo-spinner]] — AI content variation generator that can rewrite meta titles / descriptions for products in bulk.
- [[settings-translations]] — manage storefront language strings; meta values are stored against the active storefront language.

## Open questions

No outstanding questions.
