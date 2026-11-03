---
type: entity
nav_path: "Entity → SEO Meta → Fallback chain"
aliases: ["SEO meta fallback", "Meta priority order", "Per-entity vs section meta", "Meta auto-generation", "Blank meta behaviour"]
tags: [entity, seo, marketing, meta-tags, fallback]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[seo-meta]]. See the hub for the other aspects (fields, section defaults, per-entity storage, multi-language storage, canonical / no-index).

# SEO Meta — Fallback chain

## Identity

When the storefront renders the `<head>` of any page, it picks the meta title / meta description / OG image from a **4-layer fallback chain**. The merchant rarely sees this chain explicitly — they type a value somewhere, save, and the storefront renders. But understanding the chain is the only way to explain why a blank field still produces a sensible meta tag and why an unexpected meta sometimes appears on the storefront after the merchant deleted a per-entity value.

The chain runs **per field, per page-load**: each field (meta title, meta description, OG image) consults its sources independently. Blanks at any layer fall through to the next. The chain always terminates at the English baseline, so there is **no scenario where a meta field renders empty** — the storefront always has SOMETHING to show.

## Aliases

- **Fallback chain** / **Priority order** / **Meta lookup order**.
- **Per-entity override** — the highest-priority layer (the entity row's column).
- **Section default** — the [[marketing-seo-meta]] per-section translation row.
- **Language file default** — the CloudCart-shipped string for the current locale.
- **English fallback** — the terminal layer.
- **Auto-generation** — the synthesised value when the merchant has typed nothing (Entity Name + Store Name etc.).

## Key Attributes

The 4 layers, in priority order:

| Layer | Source | Wins when | Storage |
|-------|--------|-----------|---------|
| **1 — Per-entity override** | The entity's own `meta_title` / `meta_description` / `og_image` column (or `canonical_url` / `no_index_meta` on CMS Pages) | Non-blank value present on the [[product]] / [[category]] / [[vendor]] / [[marketing-landing-pages|CMS Page]] / [[blog-article]] row for the current language | Column on the entity row — see [[seo-meta-per-entity]] |
| **2 — Section default** | Translation row from [[marketing-seo-meta]] (`seo.home.title` / `seo.contacts.title` / `seo.products.title` / `seo.vendors.title` / `seo.blog.title` etc.) for the current locale | No per-entity override; the page is one of the 5 sections | `Translation` model row — see [[seo-meta-multilang-storage]] |
| **3 — Language file base default** | CloudCart-shipped default string for the current language (e.g., `lang/<lang>/sf.php` → `seo.<section>.title`) | No per-entity AND no per-section override | Static file shipped with the platform |
| **4 — English fallback** | The English-language baseline string (`lang/en/sf.php`) | All higher layers blank AND the current language has no base default | Static file shipped with the platform |

**Auto-generation as a special variant of Layer 3**: when a per-entity meta field is blank (Layer 1 falls through) AND the entity-type fallback section (`seo.product.title`, `seo.category.title`, etc.) provides a template, the storefront renderer typically derives the meta from the entity's own name / description. For a product with no per-entity meta title, the rendered `<title>` is usually `<Product Name> | <Store Name>`; for meta description, the entity's first description paragraph (truncated to the first sentence or ~160 chars). The exact format is theme-controlled — different storefront themes can override this template.

## Where it appears

The fallback chain runs **on every storefront page-load** for every meta field. The merchant never sees the layer that won — there is no UI hint about which layer produced the rendered value (no "this came from the section default" badge on the per-entity editor or vice versa).

Specific surfaces where the chain matters:

- **[[marketing-seo-meta]]** — the per-section defaults card. Typing here populates Layer 2. The merchant should not assume "the home page meta is now this text" because a per-entity override on a CMS Page configured as the homepage would still win at Layer 1.
- **Per-entity editors** ([[product]], [[category]], [[vendor]], [[blog-article]], [[marketing-landing-pages]]) — blank fields are NOT an error; they intentionally trigger fallback to Layer 2 → 3 → 4. See [[seo-meta-per-entity]].
- **OG image** — falls back from per-entity `og_image` → (for products / categories / pages) the entity's main image → store-wide default OG from [[marketing-seo-sharing]].
- **Auto-generated meta title format** — `<Entity Name> | <Store Name>` is the typical product / category / vendor pattern; blog articles use `<Article Title> | <Store Name>`; CMS Pages use the page title.

**Blank fields trigger automatic fallback** — leaving a field empty is a valid editorial choice. Clearing a previously-set field (saving an empty string) reverts the storefront to whatever the next layer down resolves to. There is no UNDO confirmation; the next page-load reflects the change after the translation cache flushes — see [[seo-meta-multilang-storage]].

**Multi-language stores layer per-language on top** — Layer 1 reads the entity row in the current storefront language; Layer 2 reads the translation row for the current locale. The chain is identical per language; languages don't cross-feed. See [[seo-meta-multilang-storage]] for the per-locale row format.

## Related

- [[seo-meta]] — hub.
- [[seo-meta-fields]] — the field catalogue this chain resolves.
- [[seo-meta-section-defaults]] — Layer 2 storage / editing UX.
- [[seo-meta-per-entity]] — Layer 1 storage on entity rows.
- [[seo-meta-multilang-storage]] — per-language layering on top of the chain.
- [[marketing-seo-sharing]] — Layer 4 (terminal) for OG image.
- [[marketing-seo-meta]] — Layer 2 manager screen.
- [[settings-translations]] — language-file management.
- [[apps-seo-spinner]] — overrides Layer 1 in bulk for products.

## Open Questions

None.
