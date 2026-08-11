---
type: entity
nav_path: "Entity → Category Property → Storefront surfaces"
aliases: ["Category Property storefront", "Property filter sidebar", "Property specs table", "Use as filter behaviour", "Property value images"]
tags: [catalog, products, properties, storefront, filters, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[category-property]]. See the hub for the other aspects (attributes, types, business rules, API).

# Category Property — Storefront surfaces

## Identity

How a [[category-property|Category Property]]'s per-product values reach the customer on the storefront. A Property has two customer-facing roles: the **category-page filter sidebar** (gated on the *Use as filter* toggle) where customers narrow the listing by Property values, and the **product detail specs table** (always shown) where the product's per-Property values render as a specification list. This page covers what surfaces where, how the two toggles (`is_visible`, `active`) gate visibility, and how value images / colour swatches appear. The definitions of the toggles live on [[category-property-attributes]].

## Aliases

- **Property filter sidebar** — the category-page narrowing UI.
- **Property specs table** — the product detail specification list.
- **Use as filter behaviour** — the `is_visible` gating.
- **Property value images** — colour swatches / icons next to values.

## Key Attributes

**Storefront category landing page — the filter sidebar.** The sidebar surfaces every Property with *Use as filter* (`is_visible`) = ON, plus the products' per-Property values present in that category. **Checkbox** Properties render as a list of filter checkboxes; **Range** Properties render as a slider with min / max auto-computed at runtime from the per-product values present in the category (see [[category-property-types]]). Customers narrowing by a Property value rewrite the URL with the Property's `url_handle` (`/category/electronics?<handle>=red`). The sidebar is category-by-category: the **active category-page** determines which Properties surface as filters.

**Storefront product detail page — the specs table.** The product's per-Property values render in the Specifications table **regardless of Use as filter** — a Property with `is_visible = OFF` is purely descriptive (visible in the specs table, NOT shown as a filter). The specs table is **scoped to the product's primary category** — only Properties attached to the product's primary `category_id` surface here; Properties attached to its secondary categories do not (see [[category-property-business-rules]]).

**Value images / colour swatches.** Each Checkbox option value can carry an optional image (e.g., colour swatches). Some themes display these in the filter sidebar next to the value, and some display the Property's own `image` icon next to the Property name. All value-images for one Property share the Property's `width` / `height` / `max_thumb_size` dimensions — see [[category-property-attributes]]. Value images reference uploaded assets in the file manager ([[file-asset]] / [[settings-files]]).

**The `active` master toggle hides everywhere.** When a Property's *Active* (`active`) toggle is OFF, the Property disappears from BOTH storefront surfaces (filter sidebar AND specs table) and from the product editor — the per-product values are preserved for later reactivation but surface nowhere while inactive.

| Surface | Gated by | Shows |
|---------|----------|-------|
| Category-page filter sidebar | `active = ON` **and** `is_visible = ON` | Checkbox list / Range slider for narrowing |
| Product detail specs table | `active = ON` **and** Property on primary `category_id` | The product's per-Property value(s) |
| Product editor (admin) | `active = ON` **and** product in an attached Category | The per-product value input |

## Where it appears

- Storefront category landing page — the filter sidebar.
- Storefront product detail page — the specs table.
- [[products-products]] — the per-product value the storefront surfaces is entered here.
- [[products-property]] — the *Use as filter* / *Active* toggles and value images are configured here.
- [[settings-files]] — value images / Property icons live in the file manager.

## Related

- [[category-property]] — hub.
- [[category-property-attributes]] — definitions of `is_visible` (Use as filter), `active`, `url_handle`, image + dimensions.
- [[category-property-types]] — Checkbox renders as checkboxes, Range as a slider (with runtime-computed min/max).
- [[category-property-business-rules]] — the primary-category JOIN scope that limits which Properties appear in the specs table.
- [[file-asset]] — the uploaded assets value images reference.
- [[product]] / [[products-products]] — the per-product values surfaced here.

## Open Questions

None.
