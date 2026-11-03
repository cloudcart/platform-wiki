---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Colour families and swatches"
aliases: ["Color swatch metaobject", "Colour swatches", "Sibling products", "Product family", "Color variants as separate products", "Pattern swatch", "Цветове мостри", "Сродни продукти", "Продуктова фамилия", "Цвят като отделен продукт"]
tags: [metafields, metaobjects, use-case, fashion, swatches, merchandising]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Use case: colour families and swatches across separate products

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Many stores list each colour of a model as its **own product**, with its own photos, URL and SEO, instead of as a variant. The shopper should still see the other colours as swatches and jump between them. Two pieces make that work. A **`color_swatch` metaobject** defines each colour once: name, hex value, optionally a pattern image. **Product metafields** say which swatch the product is and which products are its siblings.

## Scope

### The data model

**Metaobject definition `color_swatch`**:

| Field | Type | Notes |
|---|---|---|
| `name` | single-line text, required | Display name: *Forest green*. |
| `hex` | `color` | `#2E5E3E`. |
| `pattern` | file (Image) | For prints and textures where one colour is not enough. |
| `family` | single-line text, `choices`: *Green, Blue, Red, Neutral …* | **Admin filter** on. Groups shades for an index. |

**Product metafields**:

| `namespace.key` | Type | Notes |
|---|---|---|
| `custom.color` | `metaobject_reference` → `color_swatch` | **Smart-collection condition** on. |
| `custom.siblings` | `list.product_reference` | The other colours of the same model, in display order. |
| `custom.family_name` | single-line text | Optional shared name, e.g. *Linen shirt*, for a family heading. |

The siblings list is kept the same on every product of the family, each listing the others. An import or an Admin GraphQL script can write all of them at once from a family code.

### On the Nitrogen storefront

- **Product page**: reads `custom.color` and `custom.siblings`. For each sibling it follows the product's own `custom.color` to draw a dot in the swatch's `hex` (or `pattern`), linking to the sibling's URL.
- **Listing cards**: the same swatches under each card, from the same two fields.
- **Colour index**: `metaobjects(type: "color_swatch", query: "fields.family:Green")` lists all greens. A smart collection per colour (`custom.color` equals *Forest green*) gives the products.

### Why a metaobject and not a colour field

A plain `color` field on the product would repeat `#2E5E3E` on every forest-green product. Renaming *Forest green* to *Pine* would then mean editing all of them. The swatch entry is edited once. It also carries a pattern image and a family, which a plain colour cannot.

## Contrasts

- **Separate products vs variants** ([[products-variants-options]]): if colours are variants of one product, the platform already shows them in the variant selector, and no metafields are needed. The pattern here is for stores that deliberately keep colours as separate products.
- **Linked products** ([[products-editor]]): the native Linked products list could hold the siblings, but carries no colour to draw a swatch from.
- **Colour as a category property** ([[products-property]]): if shoppers should **filter listings** by colour, a property is needed, as storefront filters work by properties. A store can keep both: a property for filtering, and the swatch reference for drawing.

## Where it applies

- Fashion, footwear, bags, furniture fabrics, paints, phone cases: wherever each colour has its own photos and page.
- A list of siblings holds up to 128 products ([[metafields-limits]]).
- Swatches stay `PUBLIC_READ`.

## Related

- [[metafields-use-cases]]: all use cases.
- [[metaobjects-definitions]]: the swatch entries.
- [[products-variants-options]]: colours as variants instead.
- [[metafields-use-case-related-products]]: other product-to-product relationships.

## Open Questions

- None known.
