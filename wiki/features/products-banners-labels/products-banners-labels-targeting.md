---
type: feature
nav_path: "Products → Banners Labels → Conditions"
route_name: product-banners.edit
route_path: /admin/products/banners-labels/edit/banner/:id
aliases: ["Banner conditions", "Label conditions", "Banner targeting", "Record types", "Auto-population", "Banner product matching", "Условия за банер", "Таргетиране на банер"]
tags: [marketing, products, banners-labels]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 10
---

> Part of [[products-banners-labels]]. See the hub for the other aspects (fields & forms, scheduling / lifecycle).

# Banners & Labels — targeting & auto-population

## Purpose

How a banner / label decides **which products it appears on**. The merchant never picks products one-by-one — they define **conditions** (1-2 rows), and the platform automatically maintains the matching product set. This aspect covers the condition record types, the auto-population on save, the re-sync when a product is edited, the exclusions (bundles / draft / inactive), and the smart-collection integration.

## Where to find it

In the create / edit form (see [[products-banners-labels-fields]]) the **Conditions** block sits below the appearance fields. Each row picks a **record type** and one-or-more records of that type.

## What the merchant can do here

- Add **1 to 2** condition rows. One row minimum is required to save; two is the hard maximum.
- For each row, pick a record type and the specific records (categories, vendors, products, selections, discounts, or — labels only — tags).
- After save, the list view shows a **Products** column with the count of products currently matched by the conditions, plus a filter for "Has-products (yes / no)".

For more granular targeting than 2 rows allow, the merchant either creates multiple banners / labels, or points one condition at a **Selection** ([[products-smart-collections]]) — the smart-collection's own rule engine then does the complex matching.

## Settings & fields

### Condition record types

| `record_type` | Badge attaches to products that… |
|---------------|----------------------------------|
| `category` | Belong to this category (by `category_id`). See [[products-categories]]. |
| `vendor` | Have this vendor (by `vendor_id`). |
| `product` | Have this exact product ID. |
| `selection` | Are members of the selected product Selection — see [[products-smart-collections]]. |
| `discount` | Are linked to the selected Discount — see [[marketing-discounts]] (i.e., the discount affects them). |
| `tag` | (**Labels only**) Have this tag from [[products-products]] tags. |

The `tag` record type is available on **labels only**; banners do not offer it.

## Business rules

### Auto-population on save

When the merchant saves a banner / label, the platform immediately:

1. Evaluates all condition rows against the product catalog.
2. Computes the set of matching product IDs.
3. **Detaches** product associations that no longer match (e.g., the product was removed from the targeted category).
4. **Attaches** newly-matched products via the junction table (`products_banners_to_products` / `products_labels_to_products`).

This is why the merchant picks **conditions, not products** — the platform maintains the product list automatically in a single sync.

### Sync on product save (`ProductSaved` event)

Every time a product is saved, the platform re-evaluates **all** banner / label targets against that product:

- If the product newly matches a badge's conditions → attach it.
- If it no longer matches → detach it.

So moving a product into a category instantly gives it that category's banners on the next storefront request, and recategorising removes the obsolete badges — no merchant intervention needed.

### Bundles, draft, and inactive products are excluded

Auto-population explicitly **skips** products where:

- `is_bundle = true` — bundles per [[bundles-list]] never auto-get banners / labels.
- `active != 'yes'` — unpublished products.
- `draft = 'yes'` — draft products.

To badge a bundle, the merchant must target it by the **`product`** record type *after* the bundle is active. (Targeting a bundle by `category` / `vendor` will silently never attach it.)

### Smart-collection re-sync

When a condition row uses `selection`, the badge inherits the membership of that [[products-smart-collections]] Selection. Two queue jobs keep this current — they fire when a selection's rule set changes and re-compute every banner / label that targets that selection. The merchant gets rich, query-driven targeting without editing the banner: the smart-collection acts as a saved query the banner follows.

### No per-customer-group targeting

Unlike [[marketing-discounts]], banners / labels **cannot** be limited to specific customer groups. Every visitor — logged-in or guest, any group — sees the same badges. Targeting is purely catalog-side (category / vendor / product / selection / discount / tag).

## Related

- [[products-banners-labels]] — hub.
- [[products-banners-labels-fields]] — the form where the Conditions block lives.
- [[products-banners-labels-scheduling]] — date / status gating applied on top of the matched product set.
- [[products-smart-collections]] — `selection` record type; smart-collection rules drive auto-population.
- [[products-categories]] — `category` record type targets all products in a category.
- [[marketing-discounts]] — `discount` record type targets all products linked to a discount.
- [[bundles-list]] — bundles are EXCLUDED from auto-population.
- [[products-products]] — products that get the badges; `tag` record type uses product tags.

## Open questions

- Does the storefront cache the banner-to-product mapping? A stale view is possible after a re-sync if so. `(verify)`
