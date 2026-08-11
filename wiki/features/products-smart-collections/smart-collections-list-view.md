---
type: feature
nav_path: "Products → Smart Collections → List view"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections list", "Collections list", "Selections list", "Smart Collections table", "Smart Collections filters"]
tags: [products, collections, selections, list-view, filters]
plan_gates: ["product_collections"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (editor, rule builder, rule types, evaluation, storefront side-effects, rules and limits).

# Smart Collections — list view

## Purpose

The paginated table at `/admin/products/smart-collections` is the merchant's index of every smart collection in the store. It surfaces the collection's identity (ID + Name), its evaluation state (Pending / Finished), the products it currently matches, the rules that produce that match, and any linked discount — letting the merchant find empty collections, find which collections a given product belongs to, and bulk-clean stale collections without opening each one.

## Where to find it

Sidebar → Products → **Smart Collections**. The list is the default landing of the route — there are no list sub-tabs.

## What the merchant can do here

- **Browse** all existing collections in a paginated table.
- **Sort** by ID, Name, Status, or Products count by clicking the column header.
- **Filter** the list by any of:
  - **Status** — Pending / Finished. Tells the merchant which collections are still being evaluated. See [[smart-collections-evaluation]] for what drives the badge.
  - **Has products** — Yes / No. Find empty collections — candidates for cleanup or rule fixes.
  - **Product** — multi-select with Includes / Does not include. Find which collections a specific product currently belongs to.
- **Open the editor** for any collection by clicking its row name — opens the right-side modal documented in [[smart-collections-editor]].
- **Bulk-select rows** via the standard row checkboxes and **bulk-delete** via the standard delete bulk action.
- **Click + Add collection** to open the create modal. The plan-gate check fires at this point — if the merchant is at the cap, the modal is replaced by a plan-upgrade prompt with the verbatim message *"You have reached the maximum number of collections allowed, you need to purchase more to continue."* See [[smart-collections-rules-and-limits]] for the full plan-gate behaviour.
- **Per-row Delete** via the row-actions column.

## Settings & fields

### List columns

| Column | Notes |
|---|---|
| **ID #** | Sequential collection ID. Sortable. |
| **Name** | Collection name. Sortable. Click opens Edit modal. |
| **Status** (`executing`) | Pending = collection is still being evaluated (rules applied async; large collections may take time). Finished = evaluation complete. Sortable. The mechanism is documented on [[smart-collections-evaluation]]. |
| **Discounts** | Only rendered when at least one collection has a linked discount. Cells show the linked discount name(s). Linkage is managed in the Discounts feature, not here. |
| **Products** count | Sortable. Number-formatted. The actual count of products currently matching the collection's rules — sourced from the cached `products` field on the selection record. |
| **Criteria** (`rows`) | Collapsible dropdown summarising each rule (e.g., "Category includes Electronics", "Price between 100 and 500"). |
| **(actions)** | Per-row Delete. |

### Plan-feature chip

The page header shows the merchant their current collection usage as `<used> / <limit>` (e.g., "3 of 10 collections"). When the limit is reached, the Add collection button opens the plan-upgrade flow instead of the create modal. See [[smart-collections-rules-and-limits]] for the verbatim error string and the pack-purchase flow.

## Business rules

### The Status column is the merchant's "is this collection ready" signal

Whenever the merchant saves a new collection or edits the rules of an existing one, the platform re-evaluates which products match. For large catalogues, this is a background task — the collection's status is **Pending** during evaluation and **Finished** when complete. The merchant should not link a discount to a Pending collection — the discount may not apply correctly until the collection settles. Wait for Finished, then assign the discount via the Discounts feature. The full async mechanism (which events trigger regeneration, where the executing flag lives, how to recover from stuck Pending) is on [[smart-collections-evaluation]].

### Filter by Product is the inverse-lookup tool

The Product filter takes a multi-select of products with an Includes / Does not include operator. This is the only screen where the merchant can ask "which collections is product X in" without opening the product's editor — useful when investigating *"why does my discount apply / not apply to this product"* support tickets, since discounts often target collections (see [[smart-collections-storefront-side-effects]]).

### Bulk-delete is the standard pattern

The bulk-delete bar appears once the merchant ticks at least one row checkbox. Deleting a collection that has a linked discount does not cascade-delete the discount — the discount remains but loses its scope. The merchant must edit the discount separately to re-target it. (verify cascade semantics for linked discounts)

### Permission

This page requires the products / collections permission section. Moderators without it cannot see the Smart Collections sidebar entry.

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-editor]] — what opens when the merchant clicks a row or +Add collection.
- [[smart-collections-evaluation]] — what drives the Pending / Finished badge.
- [[smart-collections-rules-and-limits]] — the plan-gate behaviour behind the usage chip and the +Add button.
- [[products-products]] — per-product collection memberships visible on the product editor.
- [[plan-features]] — the per-pack purchase flow surfaced when the cap is reached.

## Open questions

- (verify) Does deleting a collection with a linked discount cascade to remove the discount's scope, or silently leave the discount un-scoped?
