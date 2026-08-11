---
type: entity
nav_path: "Entity → SEO Meta"
aliases: ["SEO Meta", "Meta tags", "Meta information", "Meta title", "Meta description", "OG image", "Open Graph image", "Canonical URL", "Мета информация", "Мета заглавие", "Мета описание", "Мета тагове"]
tags: [entity, seo, marketing, meta-tags, translations]
created: 2026-05-24
updated: 2026-06-10
source_count: 4
---

# SEO Meta

## Identity

**SEO Meta** is the bundle of meta-tag content the storefront renders inside the `<head>` of each page so search engines (Google, Bing, Yandex) and share-preview generators (Facebook, LinkedIn, X / Twitter) display the merchant's content correctly in search results and social cards. The bundle covers a **meta title** (the `<title>` tag — what appears in browser tabs and as the headline of a Google search snippet), a **meta description** (the `<meta name="description">` tag — the snippet text beneath the title), an **OG image** (the `og:image` tag — the image rendered in Facebook / LinkedIn / X link previews), a **canonical URL** (the `<link rel="canonical">` tag — Google's signal for which URL is the "master" copy when duplicates exist), and an optional **no-index meta** flag (the `<meta name="robots" content="noindex">` tag — tells Google NOT to index this page).

SEO Meta is **per-entity**: each [[product|Product]], [[category|Category]], [[marketing-landing-pages|CMS Page]], [[vendor|Vendor]], and [[blog-article|Blog Article]] carries its own meta-title / meta-description / OG-image override on its own admin editor. Additionally, the platform-level [[marketing-seo-meta]] screen sets the **page-type defaults** for five "section" pages (Home, Contacts, Products, Vendors, Blog) — these defaults are used when an individual page has no per-entity override. In multi-language stores, each meta value is stored **per-language** (per-locale) so each storefront language carries its own meta. The platform also auto-generates a meta title and description from the entity's name + description when the merchant hasn't typed an explicit one — see [[seo-handling]] for the full SEO model.

SEO Meta is distinct from a **301 Redirect** ([[seo-redirect]]): a redirect changes the URL the browser ends up on; SEO Meta is content rendered into the page once it loads. SEO Meta is also distinct from **canonical tagging** at the site level (the global `<link rel="canonical">` toggle on [[marketing-seo-canonical]]) and **deindex of filtered pages** (the global "noindex on filtered URLs" toggle on [[marketing-seo-deindex]]) — those are storefront-wide rules; SEO Meta carries per-entity / per-section values.

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[seo-meta-fields]] — the catalogue of meta fields (meta_title, meta_description, og_image, canonical_url, no_index_meta) and what each one renders in the storefront HTML.
- [[seo-meta-fallback-chain]] — the 4-layer priority order (per-entity → section → language file → English) + auto-generation + blank-field semantics.
- [[seo-meta-section-defaults]] — the [[marketing-seo-meta]] Vue page (5 exposed sections, missing 11+ sections, legacy-cookie escape hatch, single global Save, no SERP preview / no length validation).
- [[seo-meta-per-entity]] — per-entity meta storage on Product / Category / Vendor / CMS Page / Blog Article (column on the entity row, edited inside the parent editor).
- [[seo-meta-multilang-storage]] — per-language + per-theme storage as Translation rows, the `is_translated` flag, translation cache invalidation on save.
- [[seo-meta-canonical-noindex]] — the `canonical_url` and `no_index_meta` fields on CMS Pages, no-inheritance rule, OG-image-dimension non-validation, permission and plan gates.

## Aliases

- **SEO Meta** / **Meta tags** / **Meta information** — the canonical merchant-facing terms ([[marketing-seo-meta]] page title: "Meta settings").
- **Meta title** / **Meta description** — the two main fields.
- **OG image** / **Open Graph image** — the social-preview image (the `og:image` HTML tag).
- **Canonical URL** — the master-copy URL signal (separate per-entity, separate from the site-wide canonical toggle).
- **Мета информация** / **Мета заглавие** / **Мета описание** / **Мета тагове** — Bulgarian terms.

## Key Attributes

The headline attributes — see [[seo-meta-fields]] for the full per-field table including the per-section row variants.

| Attribute | What the merchant controls | Where it lives |
|-----------|----------------------------|----------------|
| **Meta title** (`meta_title`) | Text input | Per-entity editor + [[marketing-seo-meta]] per-section card |
| **Meta description** (`meta_description`) | Textarea | Per-entity editor + [[marketing-seo-meta]] per-section card |
| **OG image** (`og_image`) | Image uploader | Per-entity editor |
| **Canonical URL** (`canonical_url`) | Text input | CMS Page editor only |
| **No-index meta** (`no_index_meta`) | Toggle | CMS Page editor only |
| **Locale** (`locale`) | Auto-set to `site('language')` at save | Translation row (per-section meta) |
| **Theme** (`theme`) | Auto-set to active theme at save | Translation row (per-section meta) |

Drill into [[seo-meta-fields]] for the full catalogue (including per-section card field semantics, validation, length-cap status, and per-locale / per-theme storage column behaviour).

## Where it appears

- [[marketing-seo-meta]] — the page-type defaults screen (Home / Contacts / Products / Vendors / Blog). The canonical merchant working surface for section-level meta.
- [[seo-handling]] — concept page on how SEO Meta sits alongside the other 9 SEO surfaces (canonical, deindex, sitemap, robots, etc.).
- [[marketing-seo]] — parent SEO hub; carries the storefront-wide canonical toggle, the default OG image, and other global SEO flags.
- [[marketing-seo-canonical]] — storefront-wide canonical toggle (separate from per-entity `canonical_url`) — see [[seo-meta-canonical-noindex]].
- [[marketing-seo-deindex]] — storefront-wide deindex of filtered / sorted URL variants.
- [[marketing-seo-meta-title]] — pagination word added to paginated meta titles.
- [[marketing-seo-sharing]] — default OG image used when an entity has no `og_image` override — see [[seo-meta-fields]].
- [[marketing-seo-301-redirects]] — sibling SEO entity (URL redirects).
- [[product]] — per-product meta editor (meta_title, meta_description, og_image) — see [[seo-meta-per-entity]].
- [[category]] — per-category meta editor — see [[seo-meta-per-entity]].
- [[vendor]] — per-vendor meta editor — see [[seo-meta-per-entity]].
- [[marketing-landing-pages]] — per-CMS-page meta editor (meta_title, meta_description, og_image, canonical_url, no_index_meta).
- [[blog-article]] — per-blog-article meta editor.
- [[apps-seo-spinner]] — AI content variation generator that can rewrite meta titles / descriptions for products in bulk.
- [[settings-translations]] — manage storefront language strings; the section meta values saved on [[marketing-seo-meta]] are stored against the active storefront language — see [[seo-meta-multilang-storage]].

## Related

- [[seo-handling]] — concept page covering the 10 surfaces of CloudCart's SEO model.
- [[marketing-seo-meta]] — the section-defaults manager screen.
- [[marketing-seo]] — parent SEO hub with the global canonical / OG / sitemap / robots settings.
- [[marketing-seo-meta-title]] — pagination word card on [[marketing-seo]].
- [[marketing-seo-canonical]] — storefront-wide canonical toggle.
- [[marketing-seo-deindex]] — storefront-wide deindex of filtered URLs.
- [[marketing-seo-sharing]] — default OG image and share-module settings.
- [[seo-redirect]] — sister SEO entity (URL redirects).
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — entities carrying per-entity meta.
- [[apps-seo-spinner]] — AI bulk meta generator.
- [[settings-translations]] — per-language storage of section defaults.
- [[multi-language]] — multilanguage app context; each language has its own meta.
- [[apps-google-search-console]] — submits the storefront to Google for indexing; the meta the merchant sets here is what Google's snippets show.

## Open Questions

No outstanding questions — all items resolved or removed.
