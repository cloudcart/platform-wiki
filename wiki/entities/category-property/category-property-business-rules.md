---
type: entity
nav_path: "Entity → Category Property → Business rules"
aliases: ["Category Property business rules", "Property delete block", "Property orphan values", "Property field-length caps", "Property value merge", "Primary-category JOIN scope"]
tags: [catalog, products, properties, business-rules, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[category-property]]. See the hub for the other aspects (attributes, types, storefront, API).

# Category Property — Business rules

## Identity

The constraints and edge-case behaviours that govern a [[category-property|Category Property]] beyond its plain field schema: which Properties surface where, when a delete is blocked, what happens to values when a Category is detached, the server-side length caps, and how the transactional value-merge works. This is the page the AI Assistant cites for *"Why can't I delete this Property?"*, *"Why don't my specs show on the product page?"*, or *"What happens to my values if I detach the category?"*. These rules enforce identically on the JSON-API v2 path — see [[category-property-api]].

## Aliases

- **Property delete block** — the in-use deletion guard.
- **Property orphan values** — values left behind when a Category is detached.
- **Property field-length caps** — the 191-char limits.
- **Property value merge** — the multi-property transactional merge.
- **Primary-category JOIN scope** — why specs only show for the primary category.

## Key Attributes

**Per-product property values JOIN-scope to the primary category only.** The storefront product detail page's Specifications table shows only Property values whose Property is attached to the product's **primary `category_id`**. A product in multiple categories will not surface Properties attached to its secondary categories on the detail page. Storefront filter sidebars work category-by-category — the active category-page determines which Properties surface as filters. See [[category-property-storefront]].

**Deleting a Property in use is BLOCKED** at the API with HTTP 422 *"This property still has products and cannot be deleted"* (when deleting the whole Property) or *"Some property options still has products: {options}"* (when bulk-deleting individual option values). There is no force-delete affordance — the merchant must first clear every per-product value that references the Property (or each value being deleted) before the delete succeeds.

**Bulk-delete partial block** — when multiple Properties are selected and SOME are in use, the API returns 422 with the names of the in-use ones (*"Some properties still has products: A, B, C"*). The platform does NOT silently delete the non-blocked ones in the same call — the merchant must deselect the blocked ones and resubmit.

**Detaching a Category does NOT delete per-product values.** When a Property is detached from a Category, the M2M link is removed, but every per-product value already saved for products in that Category remains in storage as **orphan data**. The storefront filter / specs table stops surfacing them (the JOIN excludes them once the category link is gone), but the values reappear if the Category is re-attached. There is no UI affordance to clean orphan values — they sit silently in storage.

**Field-length caps (validated server-side):**

- **Property name** — max **191 characters**. Required.
- **Property value** — max **191 characters** per option.
- **URL handle** — must be unique across all Properties (NOT scoped per-Category). A duplicate handle is rejected at save.

**Value merge is multi-property, multi-value, transactional.** The merchant can collapse values from DIFFERENT parent Properties into a single survivor (e.g., "Color: Red" + "Colour: Reds" from a typo-spelled second Property → single "Color: Red"). The platform re-points every product, deduplicates the per-product join table (no duplicate values per product), carries over external-integration metadata, deletes the merged-out values, and fires a search-engine re-sync for all affected products — all inside one transaction. Partial merges cannot occur.

## Where it appears

- [[products-property]] — where the merchant hits the delete block, the bulk-delete partial block, and the value-merge surface.
- [[products-products]] — where the per-product value (subject to the primary-category JOIN scope) is entered.
- Storefront product detail page — the specs table that respects the primary-category JOIN scope. See [[category-property-storefront]].
- [[api-properties]] / [[api-property-options]] — the same delete blocks, length caps, and merge transactionality enforce on the JSON-API v2 path. See [[category-property-api]].

## Related

- [[category-property]] — hub.
- [[category-property-attributes]] — the field schema these rules constrain (`name`, `url_handle`, `options_list`, Categories M2M).
- [[category-property-types]] — the type-lock and Range-must-be-all-numeric validations (a related rule set).
- [[category-property-storefront]] — the storefront-side consequence of the primary-category JOIN scope.
- [[category-property-api]] — identical enforcement of these rules on JSON-API v2.
- [[category]] — the Categories whose M2M detach produces orphan values.
- [[products-products]] — where the per-product values live.

## Open Questions

None.
