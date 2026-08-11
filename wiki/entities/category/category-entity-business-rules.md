---
type: entity
nav_path: "Entity → Category → Business rules"
aliases: ["Category business rules", "Display subcategories", "Per-category payment shipping", "Category URL handle 301", "Category sibling uniqueness", "Make interval", "Category multi-language"]
tags: [entity, catalog, categories, business-rules]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[category]]. See the hub for the other aspects (attributes, lifecycle, relationships, side effects and API).

# Category — Business rules

## Identity

The non-obvious behaviours a merchant must understand to use [[category|Categories]] correctly — `display_child` recursive inclusion, **AND-combined** per-category payment / shipping restrictions across cart products, URL-handle 301 redirects, sibling-scoped name uniqueness, auto-assigned sort order, technological delivery time, multi-language scope, SEO defaults, and the manual-vs-import duplicate-handle divergence. The rules the AI Assistant cites when a merchant asks *"Why does my checkout show no payment methods?"* or *"Why did my deep `display_child = OFF` category still appear under its parent?"*.

## Aliases

- **Category business rules** — the catch-all term for the non-obvious behaviours.
- **Display subcategories pitfall** — read-at-browsed-level, no descendant override.
- **Per-category payment / shipping AND-combine** — the cart-rule intersection across products.

## Key Attributes

### Display-subcategories toggle controls product inheritance

When a customer browses a parent category:

- **`Display subcategories = ON`** — listing shows products directly in this category AND in any descendant subcategory (recursive). Typical for top levels like "Electronics".
- **`Display subcategories = OFF`** — only products directly assigned to this category. Subcategory products hidden until the customer drills in.

**No per-level override.** The toggle is read only at the level being browsed. Setting it ON at "Electronics" surfaces everything in Electronics → Phones → Smartphones regardless of each descendant's own toggle. A deep `display_child = OFF` does **NOT** block descendants from appearing in an ancestor's listing.

### Per-category payment / shipping restrictions are AND-combined across cart products

The rule that needs the most explanation:

- A category with "Define custom payment methods = ON" and 3 selected methods means: for ANY order containing at least one product from this category, only those 3 payment methods are offered.
- If the cart contains products from TWO categories that BOTH have restrictions, the **intersection** of the two sets is offered. If the intersection is empty, the customer sees no payment methods and cannot complete checkout.
- Same logic for shipping.

**Practical pitfall**: restrictions on multiple categories can produce an empty intersection — customers see "no payment methods available" at checkout for mixed-category orders. Coordinate restrictions carefully, OR keep them on a single "special" category.

### URL handle changes generate 301 redirects

Editing the URL handle records the previous handle as an entry in [[marketing-seo-301-redirects]]. The storefront serves a permanent (HTTP 301) redirect from the old URL to the new one. Search engines update their indexes over time; bookmarked links continue to work.

### Sibling-scoped name uniqueness

Names must be unique **among direct siblings** (same `parent_id`), NOT store-wide. "Shoes" can exist once under "Men" and once under "Women". Duplicate-among-siblings is rejected with *"This name is already taken"*. The same check fires on rename and on drag-drop re-parent on the Organize tab.

### Sibling-scoped sort order auto-assigned on create

When a new Category is saved with no explicit `order`, the platform scans siblings (same `parent_id`) for MAX(`order`) and sets the new row to `MAX + 1`. So a freshly-created category lands at the **bottom** of its parent's child list. Scoped per-parent: a new "Electronics" child gets a position relative to other Electronics children only. The merchant re-orders via drag-and-drop on the Organize tab if a different position is preferred.

### Publish requires at least one category on products

A [[product|Product]] cannot be `active = yes` without a `category_id` set — the product save rejects the publish. Categories are a hard prerequisite for publishing the catalog — the merchant must create at least one before publishing any product. Drafts (`active = no`) can exist without a category.

### Multi-language naming is per-locale; taxonomy is store-wide

For multi-language stores ([[multi-language]]), the category name + description + SEO fields + URL handle are translated **per-locale** (so `/category/electronics` in EN ↔ `/category/elektronika` in BG). The Google Product Taxonomy (`taxonomy_id`) is **store-wide** (not per-language) and informational only — see [[products-categories-taxonomy]] for taxonomy mapping, product inheritance, and the feed / search consumers.

### SEO fields & taxonomy do NOT inherit from the parent

Each category stores its own SEO fields and `taxonomy_id`; nothing cascades from the parent (an empty `seo_title` falls back to the category's **own** name, not the parent's). The full SEO-default fallback chain and bulk generation via [[apps-seo-spinner]] live on [[products-categories-seo]].

### Technological delivery time pushes the earliest slot

When `make_interval > 0` on a category, the customer's earliest delivery slot is pushed beyond the maximum `make_interval` of all cart products. Used for build-to-order / custom-cut categories with a known production lead time. Only affects the delivery date picker when [[apps-shipping-hours]] (or equivalent delivery-time feature) is enabled.

### Duplicate URL handles diverge by entry path

Admin form rejects a duplicate handle (validation error); CSV / XML import ([[apps-csv-import]]) silently appends `-1`, `-2`, … so bulk imports never fail on a slug clash; JSON-API v2 ([[api-categories]]) returns 422. Detail on [[products-categories-seo]] and [[category-entity-side-effects-and-api]].

### Categories cannot be merged

There is no built-in **merge** ("transfer all products from A to B then delete A") action. Reassign products individually (or via bulk-edit on [[products-products]] with a category filter) before deleting — the deletion guard blocks delete until the category is empty (see [[category-entity-lifecycle]]).

### Category images — protected + orphan-on-delete

The image field is protected from mass-assignment — uploads go through the dedicated upload pipeline on the edit modal, not via bulk-edit / API patches. Images are stored in [[settings-files]] alongside other store assets. Deleting a category does NOT auto-delete its image file — the file becomes orphan in storage. See [[category-entity-attributes]] for the field, [[category-entity-lifecycle]] for delete behaviour.

## Where it appears

- [[products-categories]] — Add / Edit modal surfaces every toggle described here.
- [[checkout-flow]] — payment / shipping AND-combine is evaluated at checkout.
- [[shipping-calculation]] — `make_interval` and allowed-shipping-method filter apply.
- [[apps-shipping-hours]] — consumes `make_interval` for the delivery date picker.
- [[apps-seo-spinner]] — writes SEO descriptions; sets `seo_generated_through_spinner`.
- [[multi-language]] — per-locale name / description / SEO / URL handle.
- [[marketing-seo-301-redirects]] — receives URL-handle rename entries.
- [[apps-csv-import]] — auto-suffix path for duplicate handles.

## Related

- [[category]] — hub.
- [[category-entity-attributes]] — fields these rules govern.
- [[category-entity-lifecycle]] — deletion guard, depth cap, save-time transitions.
- [[category-entity-relationships]] — primary vs additional category on Products.
- [[category-entity-side-effects-and-api]] — JSON-API v2 enforces every rule here.
- [[product]] — publish-requires-category dependency.
- [[payment-provider]] / [[shipping-provider]] — referenced by the intersection rule.
- [[checkout-flow]] — where the intersection is computed.
- [[multi-language]] — per-locale translations.

## Open Questions

- Confirm whether `make_interval` is read once at cart-load or recomputed at each delivery-slot refresh (verify).
