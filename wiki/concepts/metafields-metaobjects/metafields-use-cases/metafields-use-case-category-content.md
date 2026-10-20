---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Category landing content"
aliases: ["Category metafields", "Category hero banner", "Category landing page content", "Collection hero", "SEO text below products", "Featured products in category", "Buying guide link", "Съдържание на категория", "Банер на категория", "SEO текст в категория", "Препоръчани продукти в категория"]
tags: [metafields, metaobjects, use-case, categories, merchandising, seo]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: category landing content

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

A category page is often a store's most visited landing page, and a grid of products alone sells poorly. Merchandisers want more on it:

- a hero banner with a headline;
- a short intro above the grid and a longer SEO text below it;
- a few hand-picked products;
- a link to a buying guide;
- the category's frequent questions.

Natively a category has **one** description, an image, a colour, an icon and SEO fields ([[products-categories]]). **Category metafields** add the rest, so every category gets the same rich layout on a Nitrogen storefront without code changes.

## Scope

### The data model

**Category metafields** (owner type `CATEGORY`):

| `namespace.key` | Type | Purpose |
|---|---|---|
| `custom.hero_image` | file (Image) | A wide banner, separate from the category's own thumbnail image. |
| `custom.hero_headline` | single-line text, `max` 80 | |
| `custom.hero_link` | `link` | `{"text": "Shop the sale", "url": "/selection/sale"}` |
| `custom.intro` | multi-line text, `max` 400 | Above the grid. |
| `custom.seo_text` | rich text | Below the grid; headings and lists allowed. |
| `custom.featured_products` | `list.product_reference`, `list.max` 8 | A hand-picked row at the top. |
| `custom.guide` | `page_reference` | A CMS page buying guide ([[page]]). |
| `custom.faqs` | `list.metaobject_reference` → `faq` | See [[metafields-use-case-faq]]. |
| `custom.promo` | `metaobject_reference` → `banner` | A campaign block that can be switched between active and draft ([[metafields-use-case-banners]]). |
| `custom.size_chart` | `metaobject_reference` → `size_chart` | The default chart for products in it ([[metafields-use-case-size-charts]]). |

Pinned category definitions appear in the category's edit window in pinned order, so merchandisers fill them where they already edit the category ([[metafields-definitions]]).

### On the Nitrogen storefront

- The category route reads `collection(handle:)` with its native fields and `metafields(identifiers:)` for the ones above, all in one request.
- Each block renders only when its field has a value. A category without a hero shows the plain layout, so filling the fields can proceed category by category.
- The featured row's references come back with product data. Hidden or unavailable products are left out automatically.

### Smart-collection pages

A smart collection's landing page gets the same kind of blocks from a `landing_page` metaobject whose `handle` equals the collection's handle. The storefront reads `metaobject(handle: {type: "landing_page", handle})` beside `collection(handle:)` ([[metafields-use-case-page-sections]]).

## Contrasts

- **Native description vs `intro` + `seo_text`**: the native description stays the category's main text, used by classic themes and SEO tools. The metafields add a second text position the native model does not have.
- **Native image vs `hero_image`**: the native image is the category's thumbnail in menus and grids. The hero is a separate, wide image.
- **Featured products vs sorting**: the category's product sort order arranges the whole grid. `featured_products` adds a separate, curated row.
- **Classic themes**: these blocks appear only on Nitrogen ([[metafields-nitrogen]]).

## Where it applies

- Any store with category landing pages that carry traffic from search or ads.
- Up to 256 category definitions and 50 pinned ([[metafields-limits]]).
- Category values are edited by whoever may edit categories ([[metafields-permissions]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[products-categories]]: the category's native fields.
- [[metafields-use-case-page-sections]]: landing pages built from section entries.
- [[metafields-use-case-faq]]: the FAQ entries referenced here.

## Open Questions

- None known.
