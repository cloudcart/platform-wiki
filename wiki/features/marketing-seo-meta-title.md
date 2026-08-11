---
type: feature
nav_path: "Marketing → SEO → Text to add pagination to meta title and description"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Pagination word", "Meta page word", "meta_page setting", "Pagination text", "Page 2 prefix", "Дума за страница", "Текст за страница в мета"]
tags: [marketing, seo, meta-title, pagination, indexing]
plan_gates: []
created: 2026-05-23
updated: 2026-05-27
source_count: 3
---
# Pagination word in meta title and description

## Purpose

This is the third card on [[marketing-seo]]. It controls a single global string — the literal **word "Page"** (or its translation: "Страница", "Página", "Seite", etc.) — that the storefront prepends to the **meta title** and **meta description** of paginated category, vendor, search, and showcase pages, starting from page 2.

Why this exists: CloudCart uses a **self-canonical-per-page** strategy (see [[marketing-seo-canonical]]) — page 1, 2, 3 of a paginated list each declare themselves canonical, which solves the duplicate-URL problem but leaves every page with the SAME `<title>` and `<meta name="description">`. To avoid duplicate meta tags, the storefront prepends "Page 2 - " (or "Page 3 - ", etc.) on every page beyond the first. The word "Page" is what this card sets.

Despite the field being labelled "Title" in the UI, this is **NOT** a meta-title editor for any section. To edit the actual meta title of Home / Contacts / Products / Vendors / Blog see [[marketing-seo-meta]]; for a single product / category / vendor, use the entity's own editor.

## Where to find it

Sidebar → Marketing → SEO → **Main SEO settings** → the third card, with the info-column heading **"Text to add pagination to meta title and description"** and a single field labelled **Title**.

The card is the new Vue version. A `marketing-seo-main=old` cookie falls back to the legacy Smarty page at `/admin/marketing/seo`.

## What the merchant can do here

- Type the literal word the storefront should prepend to meta title and description on page 2 and beyond of any paginated listing.
- Translate that word to match the storefront's language ("Page" for English, "Страница" for Bulgarian, "Página" for Spanish, etc.).

### What the merchant CANNOT do here

- Edit the meta title of a specific page or section (use [[marketing-seo-meta]] for sections; the per-entity editor for products / categories / vendors).
- Use template variables / merge tags. The field is a literal string — no `{{page_number}}` or `{{store_name}}` substitution. The page number and separator are added automatically; the merchant types only the word.
- Set different words per language. The setting is a single global string; multi-language stores must pick one word that reads in their primary language.
- Disable pagination prefixing entirely. The field is `required`; there is no clean off-switch (a merchant would have to type a single space).
- Change where the prefix is inserted (always at the start) or the separator (always " - ", spaces included).

## Settings & fields

The card has one control.

| Control | What it does | Default | Validation / notes |
|---------|--------------|---------|--------------------|
| **Title** (text input) | Stored under the `meta_page` setting key. The literal word prepended on page 2+ of paginated lists, e.g. "Page 2 - Original Title". | `Page` | `required` — blank shows `"Field is required"` on the client, `"Meta page is required"` from the server. No max length. Saved as a plain string with no sanitization. |

The card has its own Save / Revert action bar via the shared SEO wrapper. On success the toast reads **"Saved Successfully"**.

## Business rules

### Where the prefix actually shows up

The prefix is applied on **paginated** views of these list routes:

- Category view (vendor-filtered AND non-vendor-filtered).
- Vendor view.
- Products listing.
- Curated product list ("Selection").
- Vendor-+-category combinations.

It is applied ONLY when:

- The URL has a `page` query parameter, AND
- That `page` value is numeric AND `> 1`.

So `/category/shoes?page=1` and `/category/shoes` get no prefix; `/category/shoes?page=2` gets "Page 2 - Shoes" as meta title; `/category/shoes?page=3` gets "Page 3 - Shoes"; and so on.

### Exact format of the final meta title

For a category named "Shoes" on page 2 with the default `meta_page = "Page"`, the storefront renders:

```
<title>Page 2 - Shoes</title>
<meta name="description" content="Page 2 - <existing description>">
```

The format is `{meta_page} {page_number} - {existing_title}`. Note the single space between the word and the number, and the ` - ` (space-dash-space) separator before the original meta.

### Default and language

If the field was never set, the storefront falls back to a per-language default ("Page" in English, "Страница" in Bulgarian, etc.); the admin field itself shows the global value with a hard fallback of the English word `Page`. The merchant should set this to match the storefront's primary display language so the meta reads naturally — e.g. "Страница 2 - Категория обувки" on a Bulgarian store.

### Why it lives separately from [[marketing-seo-meta]]

[[marketing-seo-meta]] holds per-SECTION meta titles and descriptions (home, contacts, etc.), persisted as per-language translation rows. This pagination word is a single **global store setting** with no language variant — the merchant has one storefront language displayed at a time and re-sets this value if they switch languages.

### Interaction with [[marketing-seo-canonical]]

Pagination prefixing exists because of self-canonical-per-page. If the merchant turns canonical OFF, Google may merge paginated pages and the per-page prefix becomes redundant — it still renders, but its SEO purpose is gone. The two settings are designed to be used together.

### Permission and plan gates

The save action sits behind the `marketing.seo` permission. No plan gate — included with every plan.

## Related

- [[marketing-seo]] — Main SEO settings hub (this card lives here).
- [[marketing-seo-canonical]] — the canonical tag setting; the pagination word exists because canonical uses a self-canonical-per-page strategy.
- [[marketing-seo-deindex]] — controls which parameterized list pages are deindexed; pagination word still renders on indexable pages.
- [[marketing-seo-meta]] — per-section meta titles and descriptions (Home / Contacts / Products / Vendors / Blog). This is where merchants edit the ACTUAL meta titles, not just the pagination prefix.
- [[marketing-seo-301-redirects]] — per-URL 301 redirects.
- [[product]] — per-product meta title / description / OG image overrides.
- [[category]] — per-category meta title / description overrides; the pagination prefix is added on top of the category's own meta.
- [[vendor]] — per-vendor meta overrides; same pagination prefix applies.

### Hidden behavior verified against backend (2026-05-26)

- **No sanitization, no length cap** — the typed value can be any string (whitespace, emoji, HTML, 10,000 characters) and is accepted as-is. HTML is rendered as literal text inside `<title>` (escaped by modern themes, but not guaranteed).
- **Triggered by the `page` query parameter, not the route** — any list page the storefront paginates via `page > 1` (category, vendor, products listing, selection) gets the prefix on both meta title and description.

## Open questions

No outstanding questions.
