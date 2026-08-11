---
type: entity
nav_path: "Entity → SEO Meta → Fields"
aliases: ["SEO meta fields", "Meta title field", "Meta description field", "OG image field", "Canonical URL field", "No-index meta field", "meta_title column", "meta_description column", "og_image column"]
tags: [entity, seo, marketing, meta-tags]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[seo-meta]]. See the hub for the other aspects (fallback chain, section defaults, per-entity storage, multi-language storage, canonical / no-index).

# SEO Meta — Fields

## Identity

This page catalogues the meta-tag fields that make up a **SEO Meta** record — both the per-entity columns (carried on a Product / Category / Vendor / CMS Page / Blog Article row) and the per-section translation rows (saved by [[marketing-seo-meta]]). Each field maps to exactly one HTML tag that the storefront template emits inside `<head>`.

There are **five user-facing fields** that the merchant controls plus three system-set columns on the per-section translation row. The five user fields are: `meta_title`, `meta_description`, `og_image`, `canonical_url`, and `no_index_meta`. The first three are universal (every entity type carries them); the last two appear only on CMS Pages.

## Aliases

- **meta_title** / **Meta title** / **`<title>` tag** / **Page title** — the headline field.
- **meta_description** / **Meta description** / **`<meta name="description">`** — the snippet field.
- **og_image** / **OG image** / **Open Graph image** / **`<meta property="og:image">`** — the social-preview image.
- **canonical_url** / **Canonical URL** / **`<link rel="canonical">`** — the master-copy URL signal (CMS Pages only).
- **no_index_meta** / **No-index meta** / **`<meta name="robots" content="noindex">`** — the search-engine exclusion flag (CMS Pages only).

## Key Attributes

| Field | What the merchant controls | What the storefront emits | Notes |
|-------|----------------------------|---------------------------|-------|
| **Meta title** (`meta_title`) | Text input on the per-entity editor, or per-section on [[marketing-seo-meta]] | `<title>...</title>` | No length limit enforced by the platform — Google truncates at ~60 characters in search snippets but the platform does NOT warn / truncate. Blank value falls back through the chain — see [[seo-meta-fallback-chain]]. |
| **Meta description** (`meta_description`) | Textarea on the per-entity editor, or per-section on [[marketing-seo-meta]] | `<meta name="description" content="...">` | No length limit enforced — Google truncates at ~160 characters in search snippets. Blank falls back through the same chain. |
| **OG image** (`og_image`) | Image uploader on the per-entity editor (per Product / Category / Page / etc.) | `<meta property="og:image" content="<url>">` | When blank, the platform falls back to the default OG image set on [[marketing-seo]] → "Main sharing picture" (controlled by [[marketing-seo-sharing]]). For products / categories / pages, the entity's main image is usually used as an intermediate fallback before the store-wide default. |
| **Canonical URL** (`canonical_url`) | Text input on the per-entity editor (per CMS Page) | `<link rel="canonical" href="<url>">` | The merchant can set a custom canonical that points elsewhere. Typical use: the thank-you-page canonical points to the home page so the thank-you URL doesn't compete in search. Site-wide toggle on [[marketing-seo-canonical]] controls whether the tag renders at all — see [[seo-meta-canonical-noindex]]. |
| **No-index meta** (`no_index_meta`) | Toggle on the per-entity editor | `<meta name="robots" content="noindex">` | When ON, tells search engines NOT to index this specific page. Typical use: thin product pages, internal-only landing pages, draft content the merchant wants reachable but not indexed. Not inherited from parent — see [[seo-meta-canonical-noindex]]. |
| **Section default — Home** | Text input on the [[marketing-seo-meta]] card "Section Home" | Renders on the storefront home page (`/`) when no per-entity override exists. | Stored as the translation key `seo.home.title` / `seo.home.description` for the current storefront language. |
| **Section default — Contacts** | Text input on "Section Contacts" | Renders on the Contacts page. | Translation key `seo.contacts.title` / `seo.contacts.description`. |
| **Section default — Products** | Text input on "Section Products" | Renders on the all-products listing page (default product catalog index). | Translation key `seo.products.title` / `seo.products.description`. |
| **Section default — Vendors** | Text input on "Section Vendors" | Renders on the all-vendors / brands index page. | Translation key `seo.vendors.title` / `seo.vendors.description`. |
| **Section default — Blog** | Text input on "Section Blog" | Renders on the blog index page. | Translation key `seo.blog.title` / `seo.blog.description`. |
| **Locale** (`locale`) | n/a (set to `site('language')` at save time) | n/a — storage column | Each saved meta value is per-language. To edit meta for a different language, the merchant has to switch the storefront language in their store-language settings first ([[settings-translations]]). See [[seo-meta-multilang-storage]]. |
| **Theme** (`theme`) | n/a (set to the active storefront theme at save time) | n/a — storage column | The saved meta is per-theme. If the merchant switches storefront theme later, the saved meta may or may not transfer (depending on whether the new theme reads the same translation keys). |
| **Is translated** (`is_translated`) | n/a (auto-set on save) | n/a — storage column | `1` when the saved value differs from the language file default; `0` when it matches. Used by the translation system to distinguish merchant overrides from fallback defaults. |
| **Pagination prefix variable** (`{$name}`, `{$price}`) | NOT on per-section meta — only on per-entity meta strings processed by [[apps-seo-spinner]] | Substituted into the rendered meta text at storefront render | The platform's the platform code helper supports `{$name}` and `{$price}` substitutions in meta TEXT only when the SEO Spinner has generated the variation. Per-section meta on [[marketing-seo-meta]] is plain literal text — these variables would render as literal `{$name}` in the title tag. |
| **Storage namespace** (`namespace`) | n/a (always `*`) | n/a — storage column | Translation rows for SEO meta always have `namespace = "*"`. This distinguishes them from app-namespaced translations. |

The five section-default cards on [[marketing-seo-meta]] all save together in a SINGLE submit (one global Save button) — see [[seo-meta-section-defaults]] for the per-section save mechanics. Per-entity meta editors save with their parent entity (e.g., the [[product]] editor's meta fields save with the rest of the product) — see [[seo-meta-per-entity]].

## Where it appears

- [[marketing-seo-meta]] — section-default fields (Home / Contacts / Products / Vendors / Blog) appear here as 5 cards × (title + description).
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] — per-entity editor exposes `meta_title`, `meta_description`, `og_image`.
- [[marketing-landing-pages]] — per-CMS-page editor exposes all 5 fields including `canonical_url` and `no_index_meta`.
- [[marketing-seo-sharing]] — the store-wide default OG image used as final fallback when `og_image` is blank.
- [[apps-seo-spinner]] — AI bulk-generates meta_title / meta_description variations + uses the `{$name}` / `{$price}` substitution variables.

## Related

- [[seo-meta]] — hub.
- [[seo-meta-fallback-chain]] — what happens when a field is blank.
- [[seo-meta-section-defaults]] — the [[marketing-seo-meta]] page mechanics.
- [[seo-meta-per-entity]] — how per-entity fields are stored as columns.
- [[seo-meta-canonical-noindex]] — `canonical_url` and `no_index_meta` specifics.
- [[marketing-seo-meta]] — the section-defaults manager.
- [[marketing-seo-sharing]] — default OG image.
- [[apps-seo-spinner]] — `{$name}` / `{$price}` substitution.

## Open Questions

None.
