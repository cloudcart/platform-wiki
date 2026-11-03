---
type: entity
nav_path: "Entity → SEO Meta → Multi-language storage"
aliases: ["SEO meta multilang", "Per-language meta storage", "Translation row SEO meta", "Per-theme meta", "is_translated flag", "Translation cache invalidation SEO", "SEO meta cache invalidation"]
tags: [entity, seo, marketing, meta-tags, translations, multilanguage]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[seo-meta]]. See the hub for the other aspects (fields, fallback chain, section defaults, per-entity storage, canonical / no-index).

# SEO Meta — Multi-language storage

## Identity

SEO Meta values are stored **per-language** (per-locale) and **per-theme**. Every saved per-section meta row carries an explicit `locale` column tying it to the storefront language active at save time, and a `theme` column tying it to the active storefront theme at save time. Per-entity meta in multi-language stores is similarly per-language — each entity translation carries its own localised meta fields.

After every save (per-section or per-entity), the **platform-wide translation cache is invalidated** so the next storefront page-load picks up the new meta without a deploy or manual purge.

## Aliases

- **Per-language meta storage** / **Per-locale meta** / **Translation row SEO meta**.
- **Per-theme meta** — emphasises the theme-scoped storage.
- **`is_translated` flag** — the column distinguishing merchant overrides from fallback defaults.
- **Translation cache flush** / **SEO meta cache invalidation** — the side effect on save.

## Key Attributes

### Per-section meta — Translation row format

Each saved per-section row on [[marketing-seo-meta]] is a `Translation` model entry:

| Column | Value | Notes |
|--------|-------|-------|
| `label` | `seo.<section>.<field>` (fully-qualified key, e.g. `seo.home.title`) | Identifies which section + which field. |
| `namespace` | `*` | All SEO meta rows use the global namespace (`*`), distinguishing them from app-namespaced translations. |
| `locale` | `site('language')` at save time | The storefront language active when the merchant clicked Save. To edit meta for a different language, the merchant switches the storefront language in [[settings-translations]] first. |
| `translation` | The merchant's typed value | The literal text the merchant entered. |
| `theme` | Active storefront theme at save time | Switching the storefront theme later may or may not preserve the saved meta (depends on whether the new theme reads the same translation keys). |
| `is_translated` | `1` when the saved value differs from the language file default; `0` when it matches | Used by the translation system to distinguish merchant overrides from fallback defaults. The fallback chain uses `is_translated = 0` as effectively "no override exists at this layer". |

### Per-entity meta — Column on the entity row

Per-entity meta (Product / Category / Vendor / CMS Page / Blog Article) is stored as columns on the entity row, not as Translation rows — see [[seo-meta-per-entity]] for the column model.

In multi-language stores, each entity has a per-language **translation row** (a separate concept from the `Translation` model used for per-section meta) that carries the localised `meta_title` / `meta_description` / `og_image`. The merchant types meta in each language's edit form via the language switcher on the entity editor.

### Per-language editing UX

To populate per-section meta for a non-default language, the merchant must:

1. Switch the storefront language to the target language via [[settings-translations]] (or the language switcher in the admin chrome).
2. Re-visit [[marketing-seo-meta]] — the form fields are now blank (because no per-section row exists yet for the new locale).
3. Type the values in the target language.
4. Click Save — a new set of Translation rows is written with `locale = <target>`.

There is no side-by-side "edit all languages at once" UI on the [[marketing-seo-meta]] section-defaults page.

For per-entity meta, the per-entity editor exposes a language switcher inline — the merchant can flip between languages without leaving the editor.

### Per-theme implications

The `theme` column on each Translation row ties the saved meta to the active storefront theme. If the merchant later switches storefront themes:

- If the new theme reads the same translation keys (`seo.home.title`, etc.), the saved meta continues to render.
- If the new theme uses different keys or a different namespace, the previously-saved meta becomes inert and the storefront falls back through the chain.

This is a low-risk edge case in practice — most themes share the `*` namespace SEO key convention.

### Translation cache invalidation

After every save (per-section or per-entity), the **platform-wide translation cache tag is flushed**. This clears the cached translation map so the next storefront page-load rebuilds it from the DB, picking up the new meta. The merchant does NOT need to deploy, restart, or manually purge — the change is live on the next storefront request.

For per-entity meta, the entity's own page-cache is also invalidated as part of the entity-save flow, so the per-entity meta change also propagates immediately.

### `namespace = "*"` distinguishes SEO meta from app translations

All SEO meta rows have `namespace = "*"` — the global namespace. App-namespaced translations (e.g., translations shipped by [[apps-csv-import]] or [[apps-microbg]]) use the app's namespace. This separation lets the platform-wide translation cache be invalidated globally without affecting app-namespaced translations and vice versa.

## Where it appears

- **[[marketing-seo-meta]]** — saves per-section Translation rows with `locale = site('language')` and `theme = active`.
- **[[settings-translations]]** — the merchant changes the active storefront language here before editing non-default-language meta.
- **Per-entity editors** ([[product]] / [[category]] / [[vendor]] / [[marketing-landing-pages|CMS Page]] / [[blog-article]]) — multi-language per-entity meta is edited via the language switcher inside the editor.
- **The translation cache** — flushed on every save. Storefront page-loads after a save read the new value on the next request.

## Related

- [[seo-meta]] — hub.
- [[seo-meta-fields]] — the storage columns (`locale`, `theme`, `is_translated`, `namespace`) on each per-section row.
- [[seo-meta-section-defaults]] — the [[marketing-seo-meta]] page that writes per-section Translation rows.
- [[seo-meta-per-entity]] — column-on-entity storage model (different from per-section Translation rows).
- [[settings-translations]] — language switching for the merchant.
- [[multi-language]] — the multi-language app context.
- [[marketing-seo-meta]] — the section-defaults manager.

## Open Questions

None.
