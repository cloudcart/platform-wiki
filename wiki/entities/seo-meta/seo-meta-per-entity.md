---
type: entity
nav_path: "Entity → SEO Meta → Per-entity overrides"
aliases: ["Per-entity meta", "Per-product meta", "Per-category meta", "Per-vendor meta", "Per-CMS-page meta", "Per-blog-article meta", "Entity column meta", "Meta override on product"]
tags: [entity, seo, marketing, meta-tags, per-entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[seo-meta]]. See the hub for the other aspects (fields, fallback chain, section defaults, multi-language storage, canonical / no-index).

# SEO Meta — Per-entity overrides

## Identity

**Per-entity meta** is the highest-priority layer of the [[seo-meta-fallback-chain|fallback chain]]: a meta value typed directly on a Product / Category / Vendor / CMS Page / Blog Article editor wins over the section default and the language file. It is stored as **columns on the entity row** (not as separate translation rows) — so the meta lives and dies with the entity it belongs to.

There is **no dedicated "Meta" edit screen per entity** in the admin panel. The merchant edits per-entity meta inside the entity's own editor — usually as a "SEO" section / tab / accordion at the bottom of the page. Saving the entity saves the meta in the same submit.

## Aliases

- **Per-entity meta** / **Per-product meta** / **Per-category meta** / **Per-vendor meta** / **Per-CMS-page meta** / **Per-blog-article meta**.
- **Entity column meta** — emphasises the storage model (column on the entity row).
- **Meta override** — emphasises the fallback-chain role.

## Key Attributes

The 5 entity types that carry per-entity meta and the fields each one exposes:

| Entity | meta_title | meta_description | og_image | canonical_url | no_index_meta |
|--------|------------|------------------|----------|---------------|---------------|
| [[product]] | yes | yes | yes | — | — |
| [[category]] | yes | yes | yes | — | — |
| [[vendor]] | yes | yes | yes | — | — |
| [[marketing-landing-pages|CMS Page]] | yes | yes | yes | yes | yes |
| [[blog-article]] | yes | yes | yes | — | — |

Only [[marketing-landing-pages|CMS Pages]] carry `canonical_url` and `no_index_meta` — see [[seo-meta-canonical-noindex]] for why those two fields are CMS-page-only.

| Aspect | Behaviour |
|--------|-----------|
| **Storage** | Columns directly on the entity row (`meta_title`, `meta_description`, `og_image`, `canonical_url`, `no_index_meta` where applicable). NOT a separate Translation row — this is a different storage model from the per-section defaults — see [[seo-meta-multilang-storage]]. |
| **Editor location** | Embedded in the entity's own admin editor as a "SEO" section / tab / accordion. There is no standalone "Meta" edit screen per entity. |
| **Save mechanism** | Saves with the parent entity's main Save button. The merchant edits product fields + meta fields together and clicks Save once. No separate API call. |
| **Per-language behaviour** | In multi-language stores, per-entity meta is typically also per-language — entity translations carry the localised `meta_title` / `meta_description` / `og_image` for each language. The language switcher on the entity editor exposes the multi-language meta fields. |
| **Fallback** | Blank per-entity field falls back to the section default ([[marketing-seo-meta]]) → language file → English. See [[seo-meta-fallback-chain]]. |
| **Auto-generation** | When `meta_title` / `meta_description` are blank, the storefront typically derives a meta title from the entity's name (`<Entity Name> | <Store Name>`) and a description from the entity's first paragraph (truncated). Theme-controlled; different themes can override the template. |
| **Bulk edit** | [[apps-seo-spinner]] can bulk-write per-product `meta_title` / `meta_description` variations using `{$name}` and `{$price}` substitution variables. |
| **Validation** | NONE — no length cap, no character counter, no merge-tag validation. The platform accepts whatever text the merchant types. |
| **Plan gate** | None — every plan supports per-entity meta. |

**Per-entity overrides win over section defaults** — even when the merchant has typed a section-default on [[marketing-seo-meta]], a per-entity value still overrides it. This is the cornerstone of the [[seo-meta-fallback-chain|fallback chain]].

**Per-entity meta is NOT inherited** — setting `meta_title` on a Category does NOT propagate to products in that category. Each entity carries its own independent meta. Same applies to `no_index_meta` on Categories: it only affects the category listing page, not the products in it — see [[seo-meta-canonical-noindex]].

**Clearing a per-entity meta field** falls the storefront back to the section / language-file / English layer. There is no UNDO confirmation; the next page-load reflects the change after the translation cache flushes.

## Where it appears

- **[[product]] editor** — meta_title, meta_description, og_image inputs at the bottom of the editor.
- **[[category]] editor** — same 3 fields.
- **[[vendor]] editor** — same 3 fields.
- **[[blog-article]] editor** — same 3 fields.
- **[[marketing-landing-pages|CMS Page]] editor** — all 5 fields (meta_title, meta_description, og_image, canonical_url, no_index_meta).
- **[[apps-seo-spinner]]** — bulk-writes per-product `meta_title` / `meta_description` from AI-generated variations using the `{$name}` and `{$price}` substitution variables.
- The language switcher on each entity editor — exposes the per-language meta fields when the multi-language app is installed.

## Related

- [[seo-meta]] — hub.
- [[seo-meta-fields]] — the field semantics each entity exposes.
- [[seo-meta-fallback-chain]] — per-entity is Layer 1 (highest priority).
- [[seo-meta-section-defaults]] — per-entity overrides win over section defaults.
- [[seo-meta-multilang-storage]] — per-language behaviour for entity translations.
- [[seo-meta-canonical-noindex]] — why CMS Pages have 2 extra fields the other entity types don't.
- [[product]] / [[category]] / [[vendor]] / [[blog-article]] / [[marketing-landing-pages]] — the 5 entity types that carry per-entity meta.
- [[apps-seo-spinner]] — bulk per-product meta generation.
- [[multi-language]] — the app that adds per-language meta to each entity.

## Open Questions

None.
