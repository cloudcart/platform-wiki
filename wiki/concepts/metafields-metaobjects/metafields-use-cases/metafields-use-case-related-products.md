---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Typed product relationships"
aliases: ["Complementary products metafield", "Accessories metafield", "Spare parts", "Consumables", "Refills", "Complete the look", "Replaced by", "Successor product", "Upgrade product", "Аксесоари", "Резервни части", "Консумативи", "Допълнете визията", "Заменен от"]
tags: [metafields, use-case, merchandising, cross-sell, references]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: typed product relationships: accessories, consumables, successors

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

The platform already has a product-to-product list: **Linked products** in the product editor ([[products-editor]]), a manual list in the merchant's order. On the Storefront API it is `Product.linkedProducts`. `Product.relatedProducts` adds the main category's products after it. For "You may also like", nothing more is needed.

What one list cannot say is **what kind** of relationship it is, for example:

- the cartridge that **refills** this printer;
- the case that **is an accessory** to this phone;
- the trousers that **complete** this jacket;
- the model that **replaced** this discontinued one.

**Product and variant reference metafields** keep each relationship in its own field, so a Nitrogen storefront can label them and place them differently. A variant reference names the exact variant, such as the right size of a refill.

## Scope

### The data model

| `namespace.key` | Type | Shown as |
|---|---|---|
| `custom.accessories` | `list.product_reference` | "Accessories" |
| `custom.consumables` | `list.variant_reference` | "Refills and spare parts": the exact variant, ready to add to the cart |
| `custom.complete_the_look` | `list.product_reference`, `list.max` 6 | "Complete the look" |
| `custom.replaced_by` | `product_reference` | On a discontinued product: "Replaced by …" |
| `custom.upgrade` | `product_reference` | "Need more? See …" |
| `custom.explore_categories` | `list.collection_reference` | "Explore also": categories, not products |

### On the Nitrogen storefront

- Each list is read with the product (`metafields(identifiers:)`), and `references` returns the products with the fields the page needs (title, price, image, availability), in the stored order.
- A **variant** reference returns the `ProductVariant`, so "Add refill" puts that exact variant in the cart without a size picker.
- A referenced product the storefront does not show is **left out**, so no block links to a dead page. A product that is **deleted** disappears from every list that held it ([[metafields-definitions]]).
- `linkedProducts` stays the general "You may also like" row. The typed lists sit where they belong: consumables next to the buy button, `replaced_by` instead of the buy button on a discontinued product.

### Upkeep

- `list.max` caps how many a merchandiser can add.
- An integration fills the lists in bulk with the Admin GraphQL API's `metafieldsSet`, 25 values per call, e.g. from a spare-parts table in an ERP.

## Contrasts

- **Linked products vs typed lists**: Linked products is one untyped list, shown on classic themes too. Typed lists carry meaning and variant precision, but only a Nitrogen storefront shows them. A store needing one recommendation row uses Linked products.
- **Cross-Sell & UpSell** ([[marketing-cross-sell]]): offers triggered by the cart or the checkout, with conditions. The lists here are fixed facts about a product.
- **Bundles** ([[bundle]]): a set sold as one product with its own price. Reference lists only suggest products bought separately.

## Where it applies

- Printers and cartridges, appliances and spare parts, phones and accessories, coffee machines and capsules, outfits, furniture sets, discontinued models and their successors.
- A list holds up to 128 products or variants ([[metafields-limits]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[products-editor]]: the native Linked products list.
- [[marketing-cross-sell]]: conditional cart and checkout offers.
- [[metafields-use-case-compatibility]]: when "fits" depends on a device rather than a product.

## Open Questions

- None known.
