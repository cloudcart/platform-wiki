---
type: feature
nav_path: "Products → Properties → Categories (per property)"
route_name: category-property-categories
route_path: /admin/products/property
aliases: ["Property categories", "Property → Categories", "Attach property to category", "Detach property from category"]
tags: [products, properties, categories, taxonomy]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[products-property]]. See the hub for the other aspects (list view, wizard, values, merge, business rules, programmatic access).

# Properties — categories sub-page

## Purpose

The per-property sub-page that manages which [[products-categories|Categories]] this property is attached to. Properties are **category-scoped**, not store-wide — they only appear on the editor for products in attached categories. This page is where the merchant changes the property's reach after it was created.

## Where to find it

Sidebar → Products → **Properties** → click the **Categories** count for the row of the relevant property. The page opens from [[products-property-list-view]].

## What the merchant can do here

- See the list of categories the property is currently attached to.
- **Add categories** via **+ Add category** — opens the Add categories modal (see below).
- **Detach a category** — per-row Delete action removes the property from products in that category (the property stops appearing on those products' editors and storefront filter).

### Add categories modal

Opens as an `md`-sized popup.

## Settings & fields

### Add categories modal

| Field | Notes |
|-------|-------|
| **Add categories** | Tag-mode multi-select searching `/admin/api/core/product-categories/search`. Help text: *"You can add multiple categories that will use this property."* Save button disabled until at least one category is picked. Close cancels with no changes. |

### Per-row list

Each row shows the category name. The per-row Delete action detaches the property from the category (no confirmation modal — the detach is immediate; orphan per-product values remain in storage per the business rule below).

## Business rules

- **Properties are category-scoped, not store-wide.** A property is only visible on products that belong to a category it's attached to. Creating a "RAM" property and attaching it to "Laptops" makes it appear on laptops but NOT on phones (unless the merchant also attaches it to "Phones"). This is what makes properties a CATEGORY-aware specification system rather than global tags.
- **Detaching a category does NOT cascade-delete per-product values.** When a category is detached, the link between Property ↔ Category is removed, but the per-product values already assigned remain in storage as **orphan data** — the storefront filter no longer surfaces them, but the values reappear if the category is re-attached. This holds for both admin saves and [[products-property-api|JSON-API v2]] writes.
- **Categories required at creation, but can be emptied afterwards.** The [[products-property-wizard|wizard]] step 2 allows zero categories (the API call is skipped). After creation, the merchant can detach all categories — the property continues to exist in the list but applies to no products until re-attached.
- **Inline rename / value-add does NOT re-attach to categories.** Editing the property name, URL handle, or adding new values does NOT change category attachment. The merchant manages it explicitly here.
- **Attach / detach triggers a storefront search-engine re-sync** for affected products — see [[products-property-api]] for the side-effect detail.

### Permission

Requires the `products` permission section, same as the list view.

## Related

- [[products-property]] — hub.
- [[products-property-list-view]] — entry point (Categories count cell).
- [[products-property-wizard]] — step 2 uses the same category-search endpoint.
- [[products-property-business-rules]] — full business-rule catalogue (category-scope, orphan values, primary-category JOIN on storefront).
- [[products-categories]] — Categories management page; properties attach to records defined there.
- [[products-products]] — per-product property values appear on the editor when categories with properties are picked.

## Open questions

None.
