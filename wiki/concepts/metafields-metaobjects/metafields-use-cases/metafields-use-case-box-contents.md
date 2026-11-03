---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → What's in the box"
aliases: ["What's in the box", "Box contents", "Kit contents", "Package contents", "Included items", "Set contents", "Какво има в кутията", "Съдържание на комплекта", "Съдържание на опаковката", "Включени аксесоари"]
tags: [metafields, metaobjects, use-case, products, kits]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Use case: what's in the box

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Shoppers want to know exactly what they get:

- a drill with two batteries, a charger and a case;
- a starter kit with five items, each of which is also sold separately;
- a gift box of three wines;
- a camera with a lens, strap and cable.

Written in the description, the list cannot link to the separate items or be laid out consistently. A **`box_item` metaobject** describes one line of the contents: what, how many, and optionally which product or variant it is. The product lists its lines **in order**.

## Scope

### The data model

**Metaobject definition `box_item`**:

| Field | Type | Notes |
|---|---|---|
| `label` | single-line text, required | Display name: *18 V battery, 2 Ah*. |
| `quantity` | `number_integer`, `min` 1 | |
| `variant` | `variant_reference` | Optional: the item as sold on its own, for a link and price. |
| `image` | file (Image) | For items not sold separately. |
| `note` | single-line text | *"Not included in the EU version"*. |

**Product metafields**:

| `namespace.key` | Type | Notes |
|---|---|---|
| `custom.in_the_box` | `list.metaobject_reference` → `box_item` | The contents, in order. |
| `custom.not_included` | multi-line text | What the shopper must buy separately, e.g. *"Batteries not included"*. |

When every item is a product in the store and quantities do not matter, a plain `list.variant_reference` is enough, with no metaobject.

### On the Nitrogen storefront

- A **"What's in the box"** block on the product page lists each line as *quantity × label*, with the image, or the referenced variant's image and price.
- Lines with a `variant` link to that variant, as *"Also sold separately — €39"*. A variant the storefront does not show is left out of the reference, and the line falls back to its label.
- The **total value** of separately sold items (*"Worth €210 when bought separately"*) can be computed on the storefront from the referenced variants' prices.

### Reuse

The same `box_item` entry (*USB-C cable, 1 m*) can be referenced by many products. Correcting it, or replacing its variant when the cable is discontinued, updates every product. Deleting a referenced variant clears it from the entry, and the line stays with its label ([[metafields-definitions]]).

## Contrasts

- **Box contents vs bundles** ([[bundle]]): a bundle is sold as one product built from other products, with its own price and stock rules, and is on the Storefront API (`Product.bundle`). Box contents only **describe** a single product: they do not add items to the cart or take stock from them.
- **Box contents vs related products** ([[metafields-use-case-related-products]]): accessories are optional extras the shopper may buy. Box contents are what already comes with the product.
- **Per product vs per variant**: the contents sit on the product. When variants differ in contents (with or without a second battery), each variant's difference goes in the item `note`, or the variants become separate products.

## Where it applies

- Power tools, cameras and electronics, starter kits, gift boxes and hampers, cosmetics sets, toys and games.

## Related

- [[metafields-use-cases]]: all use cases.
- [[bundle]]: products sold as a set.
- [[metafields-types]]: variant references.
- [[metafields-use-case-related-products]]: accessories and consumables.

## Open Questions

- None known.
