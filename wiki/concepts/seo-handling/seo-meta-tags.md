---
type: concept
nav_path: "Concept → SEO handling → Meta tags and fallback chain"
aliases: ["Meta title", "Meta description", "Per-section meta", "Per-entity meta", "Meta fallback chain", "SEO meta", "Title fallback"]
tags: [seo, meta-tags, title, description, fallback, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[seo-handling]]. See the hub for related aspects (sitemap / robots, canonical / noindex, redirects, sharing / RSS, plan overrides, route catalog).

# SEO — meta tags and the fallback chain

## Definition

The `<title>` and `<meta name="description">` tags emitted in every storefront page's `<head>` come from a **four-step fallback chain**. The merchant configures two levels of input — per-section meta on [[marketing-seo-meta]] (Home / Contacts / Products / Vendors / Blog) and per-entity meta on each product / category / vendor / CMS page / blog article's own admin editor. The storefront walks the chain at request time.

## Scope

Covered:

- The four-step fallback chain: per-entity override → per-section meta → base language file → English fallback.
- Per-section meta storage: per-language AND per-theme.
- Why the new Vue page exposes only 5 section blocks while the legacy Smarty page exposed 16 (the other 11 still exist in the underlying translation namespace; legacy escape hatch via `marketing-seo-meta=old` cookie — verify).
- The "section meta is the fallback, not the override" rule that confuses merchants.
- The global Save model on [[marketing-seo-meta]] (one Save button saves all five sections at once) vs. the per-card model on [[marketing-seo]].

Not covered here:

- The pagination-word prefix on paginated pages 2+ → [[seo-canonical-noindex]].
- Open Graph image (`og:image`) and the dead AddThis sharing module → [[seo-sharing-rss]].
- The trial / demo override that injects `noindex, nofollow` regardless of meta → [[seo-plan-overrides]].

## Contrasts

- **Per-section meta vs. per-entity meta** — per-section meta ([[marketing-seo-meta]]) is the **fallback** for Home / Contacts / Products / Vendors / Blog index pages. Per-entity meta lives on each product / category / vendor / CMS page / blog article's OWN admin editor and **overrides** the section default. Merchants who edit `seo.product.title` on [[marketing-seo-meta]] are setting the fallback for product pages that have no per-product meta — NOT setting the meta for any single product.
- **Legacy Smarty 16 sections vs. new Vue 5 sections** — the legacy version exposed 16 section blocks (account, cart, checkout, login, register, etc.); the new Vue page only exposes 5. The other 11 still exist in the underlying translation namespace and can be edited via the legacy escape hatch (`marketing-seo-meta=old` cookie — verify).
- **Per-card Save ([[marketing-seo]]) vs. Global Save ([[marketing-seo-meta]])** — [[marketing-seo]] saves each card independently. [[marketing-seo-meta]] has ONE global Save button at the bottom that saves all five sections together.

## Where it applies

### Per-section meta — Home / Contacts / Products / Vendors / Blog

[[marketing-seo-meta]] holds the `<title>` and `<meta name="description">` for **five** section index pages. These are stored as per-language translation rows. The storefront's fallback chain when building meta for a page:

1. **Per-entity override** (e.g., the merchant set a meta title on a specific CMS page).
2. **Section meta from this admin screen** (the language-scoped translation row).
3. **Base language file** (platform default for the storefront's current language).
4. **English fallback**.

Leaving a section meta blank just falls back to the platform default for that language. The legacy Smarty version of this page exposed 16 section blocks (account, cart, checkout, login, register, etc.); the new Vue page only exposes 5 — the other 11 sections still exist in the underlying translation namespace and can be edited via the legacy escape hatch (`marketing-seo-meta=old` cookie) (verify).

### Per-entity meta — on the entity editor, not here

Per-product / per-category / per-vendor / per-CMS-page / per-blog-article meta titles, descriptions, and OG images live on the entity's OWN admin screen — see [[product]], [[category]], [[vendor]], [[blog-article]], and the CMS Pages editor. The section meta on [[marketing-seo-meta]] is the FALLBACK used when the per-entity field is empty; it does NOT control per-entity meta.

### Per-section meta is per-language AND per-theme

Section meta on [[marketing-seo-meta]] is stored against the storefront's **current language** AND **current theme**. Switching language requires changing the storefront language on [[settings-translations]] and revisiting this screen. Switching theme may or may not preserve the meta — depends on whether the new theme reads the same translation keys.

### Global Save on [[marketing-seo-meta]]

Unlike the per-card Save on [[marketing-seo]], [[marketing-seo-meta]] has ONE global Save button at the bottom of the page that saves all five sections together.

### What the storefront emits

- `<title>` — built from the fallback chain (per-entity → per-section → language file → English).
- `<meta name="description">` — same chain.
- On paginated pages 2+, the pagination word is prepended — see [[seo-canonical-noindex]].
- On routes that emit `noindex`, the meta tags still render normally; only the robots directive changes — see [[seo-route-catalog]] for which routes are exempt from any robots tag entirely.

## Related

- [[seo-handling]] — hub.
- [[seo-canonical-noindex]] — pagination word that decorates the meta on paginated pages.
- [[seo-sharing-rss]] — `og:image` / `og:title` / `og:description` companions to the meta tags.
- [[seo-plan-overrides]] — overrides that affect the `robots` meta independently of `title` / `description`.
- [[marketing-seo-meta]] — admin screen for per-section meta.
- [[product]] — per-product meta + OG image overrides.
- [[category]] — per-category meta + OG image overrides.
- [[vendor]] — per-vendor meta overrides.
- [[blog-article]] — per-blog-article meta overrides.
- [[settings-translations]] — storefront language affects which translation row stores section meta.

## Open Questions

None.
