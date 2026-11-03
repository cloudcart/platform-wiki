---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Designers, authors and makers"
aliases: ["Designer profile metaobject", "Author page", "Artist profile", "Maker story", "Brand story", "Producer profile", "Профил на дизайнер", "Автор", "Производител", "История на марката"]
tags: [metafields, metaobjects, use-case, content, brand-story]
plan_gates: []
created: 2026-10-20
updated: 2026-10-21
source_count: 3
---

# Use case: designers, authors, artists and makers

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Many stores sell partly on **who made it**: a fashion designer, a book's author, a winemaker, a ceramicist, a farm. Each person or maker needs a profile (portrait, story, country, links), shown on every product they made and on a page of their own. A **`maker` metaobject** (or `designer`, `author`, `artist`) holds the profile once. Products **reference** it, one maker or several.

## Scope

### The data model

**Metaobject definition `designer`**:

| Field | Type | Notes |
|---|---|---|
| `name` | single-line text, required | Display name; the handle is made from it: `ana-petrova`. |
| `portrait` | file (Image) | |
| `short_bio` | multi-line text, `max` 300 | For product pages. |
| `story` | rich text | The full profile page. |
| `country` | single-line text | **Admin filter** on. |
| `founded` | `date` or `number_integer` | Year active since. |
| `website` | `url` | |
| `instagram` | `link` | `{"text": "@anapetrova", "url": "https://…"}` |
| `gallery` | `list.file_reference` (Image) | Studio photos. |
| `featured` | `list.product_reference` | Hand-picked signature pieces. |
| `collection_handle` | single-line text | The handle of a smart collection with all their products (below). |

**Product metafields**:

| `namespace.key` | Type | Notes |
|---|---|---|
| `custom.designer` | `metaobject_reference` → `designer` | **Smart-collection condition** on. |
| `custom.contributors` | `list.metaobject_reference` → `designer` | For books with several authors, or collaborations. |

### "All products by this designer"

The Storefront API has no reverse lookup from an entry to the products that reference it. The pattern is:

1. Create a **smart collection** per designer whose condition is `custom.designer` equals that entry ([[metafields-capabilities]]).
2. Store the collection's handle in the entry's `collection_handle`.
3. The Nitrogen designer page reads the entry by handle, then `collection(handle:)` for the product grid.

The collection maintains itself as products are tagged with the designer. It is also a working collection page on classic themes ([[selection]]).

### On the Nitrogen storefront

- **Product page**: a "Designed by" card from `custom.designer`, following the reference to `name`, `portrait` and `short_bio`, linking to `/designers/{handle}`.
- **Designer page**: `metaobject(handle: {type: "designer", handle})` for the story and gallery, plus the collection's products.
- **Designers index**: `metaobjects(type: "designer", first: 50)`, optionally filtered by `fields.country:Italy`.

## Contrasts

- **Designer vs the product's brand (vendor)**: the platform's brands ([[products-vendors]]) are one per product, with their own pages and filters on classic themes. A designer metaobject adds what a brand does not hold: several makers per product, a rich story, a gallery, links. A store that only needs "made by" uses the brand. When a brand needs a richer story, a `brand_story` metaobject can carry its brand's name in a field.
- **Reverse lookup**: there is no "products referencing this entry" query on the Storefront API. The smart collection above fills that role. A hand-curated list (`featured`) works too.
- **Single vs list reference**: a smart-collection condition needs the single `custom.designer`. A list (`custom.contributors`) is for display only.

## Where it applies

- Fashion and jewellery designers, book authors and illustrators, artists and print studios, wine and food producers, furniture makers, marketplaces of independent makers.
- Up to 1,000,000 entries per metaobject. For a bookstore with thousands of authors, entries are typically created by an import with `metaobjectUpsert` by handle ([[metafields-admin-api]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[metaobjects-definitions]]: handles, display names, upsert.
- [[metafields-capabilities]]: the smart-collection condition on a reference.
- [[products-vendors]]: the platform's own brands.

## Open Questions

- None known.
