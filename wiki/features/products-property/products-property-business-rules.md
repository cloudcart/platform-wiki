---
type: feature
nav_path: "Products → Properties → Business rules"
route_name: categories.property
route_path: /admin/products/property
aliases: ["Property business rules", "Property validation", "Property type lock", "Active vs Use as filter", "Delete protection"]
tags: [products, properties, rules, validation, taxonomy]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-property]]. See the hub for the other aspects (list view, wizard, categories, values, merge, programmatic access).

# Properties — business rules

## Purpose

The non-obvious rules that govern how properties behave once they exist: visibility toggles, type-lock, validation strings, delete-protection, sort-priority effects, and storefront edge-cases (primary-category specs, orphan values). Aspect-specific UI mechanics live on the relevant sub-page; this is the cross-cutting reference.

## Where to find it

No dedicated screen — these rules apply across [[products-property-list-view]], [[products-property-wizard]], [[products-property-categories]], [[products-property-values]], and [[products-property-merge]]. The support agent reads this page to confirm a behaviour is expected before answering a ticket.

## What the merchant can do here

Nothing — this is a support reference. The behaviours below cannot be toggled or worked around from the admin UI unless a workaround is explicitly listed.

## Settings & fields

The relevant field caps and validation strings live in the **Rule catalogue** below — specifically the **Field-length caps** and **Range type validation** entries.

## Business rules

### Active vs Use-as-filter — three-state visibility

| Active | Use as filter | Behaviour |
|---|---|---|
| OFF | (any) | Property hidden EVERYWHERE — editor doesn't show it, product detail page doesn't show it, filter sidebar doesn't show it. |
| ON | OFF | Property is editable on products and visible on product detail pages, but NOT shown as a filter on the storefront category sidebar. |
| ON | ON | Full visibility — appears as a filter AND on product specs. |

Both toggles are reachable inline from [[products-property-list-view]] or via the bulk actions.

### Property type is locked after create

Once created as Checkbox (discrete option list) or Range (numeric slider), the type cannot be changed in place. To switch type, the merchant must delete the property (losing assigned values on products) and create a new one. Same on the [[products-property-api|JSON-API v2]] path.

### Range type validation — all values must be numeric

When saving (or attempting to convert) a property as **Range** type, the platform validates every existing option value. If ANY value is non-numeric (e.g., "Cotton"), the save fails with:

*"There are values to the property which are not a number"*

So a "Material: Cotton / Polyester" Checkbox property can't be converted to Range without first clearing or migrating the non-numeric values.

### Delete-protection when in use

Deleting a property that's still in use by products fails with:

*"This property still has products and cannot be deleted"*

The merchant must:
1. Open the property's products list (click the Products count in [[products-property-list-view]]).
2. Either remove the property value from those products, OR delete the products.
3. Try delete again.

**Bulk delete is partially blocked.** If some selected properties are in use, the response message includes the list of blocked names:

*"Some properties still has products: `<comma-separated-names>`"*

Activate / Deactivate / Use-as-filter toggles are **unrestricted by usage** — they can be flipped freely (the property is simply hidden; per-product values are preserved).

### URL handle uniqueness

Two properties can't share a `url_handle` (Color in one and Color in another would clash on the filter URL). The platform validates uniqueness at save time; the filter-URL lookup is refreshed automatically on create and on URL-handle change, so no manual cache flush is needed.

### Field-length caps

- **Property name** — max **191 characters**. Required.
- **Property value name** — max **191 characters** when adding individual values via [[products-property-values]].
- **Image upload over plan storage cap** — *"You have reached your storage limit"*. The check counts the image size **twice** (original + generated thumbnail).

### Sort priority drives TWO surfaces

The Sort priority column / drag-drop reorder on [[products-property-list-view]] controls both the storefront category filter sidebar AND the product editor's category-properties section on [[products-products]]. Merchants typically put the most important properties (Brand, Color for clothing; CPU, RAM for laptops) at the top.

### Properties are category-scoped, not store-wide

A property is only visible on products in categories it's attached to (see [[products-property-categories]]). A "RAM" property attached to "Laptops" appears on laptops but NOT on phones unless also attached to "Phones". This makes properties a category-aware specification system rather than global tags.

### Detaching a category does NOT cascade-delete per-product values

Existing per-product values PRESERVE as orphan data on detach. The storefront filter no longer surfaces them, but they remain in storage and reappear if the category is re-attached. Same on the [[products-property-api|JSON-API v2]] path.

### Specs table shows only the PRIMARY category's properties

When the storefront product detail page renders the "Specifications" table, it shows only property values whose property is attached to the product's **primary category**. So if a product is in Electronics, Phones, and Smartphones with per-product values at each level, only the primary-category values appear. An important constraint when designing multi-category property strategies.

### Range properties don't have option values

Range-type properties skip step 3 of the [[products-property-wizard|wizard]]. They have no discrete values — the slider's min/max is auto-computed from the category's products at runtime. The merchant sets only the `dec_points` precision; the platform derives the slider step (`0.01` for `dec_points = 2`, `0.1` for `1`, `1` for `0`). Default is **2** when `dec_points` is unset.

### Value merging is permanent

The Merge values action is **irreversible** — see [[products-property-merge]] for the mechanics. Once merged, the merged-out values are gone; undoing means manually recreating values and reassigning products.

### Per-product values appear on the product editor

When the merchant edits a product on [[products-products]] and assigns it to a category with properties attached, those properties appear under the Categories section. The merchant fills in each value (picks a Checkbox option, or types a Range number).

### Image dimensions are per-property, merchant-controlled

The `width`, `height`, and `max_thumb_size` fields are set at the property level — not per value — so all value-images for a property share the same dimension rules. The merchant picks dimensions to fit the storefront design; there is no platform default size. This **answers the recommended-image-size question**: the merchant SETS the dimensions; the platform enforces them.

### No time-windowed visibility

Unlike products (which can be scheduled to publish / unpublish), properties have no scheduled-visibility mechanism. The `active` flag is binary. To gate a property to a time window, the merchant toggles Active manually.

### Saves trigger storefront search re-index

Saving / activating a property — or saving a value, or merging values — triggers a storefront search-engine re-index for affected products. Same on the [[products-property-api|JSON-API v2]] path; see that aspect for the full side-effect catalogue.

### Permission

The Properties pages and actions require the `products` permission section. Moderators without it cannot see the Properties sidebar entry.

## Related

- [[products-property]] — hub.
- [[products-property-list-view]] — the toggles and bulk actions enforce these rules.
- [[products-property-wizard]] — type-lock + name-length validations fire at create.
- [[products-property-categories]] — category-scope + orphan-value rule.
- [[products-property-values]] — value-name length cap + image-dimension rule.
- [[products-property-merge]] — irreversibility of merge.
- [[products-property-api]] — same rules enforced on JSON-API v2 writes.
- [[products-products]] — per-product values appear on the editor here.
- [[products-categories]] — category records being attached.

## Open questions

None.
