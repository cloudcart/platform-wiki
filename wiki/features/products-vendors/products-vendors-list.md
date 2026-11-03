---
type: feature
nav_path: "Products → Vendors → List"
route_name: vendors
route_path: /admin/products/vendors
aliases: ["Vendor list", "Vendors table", "Has products filter", "Vendor cleanup", "Списък производители", "Филтър — има продукти"]
tags: [products, vendors, manufacturers, brands, list]
plan_gates: ["vendors"]
created: 2026-06-10
updated: 2026-06-10
source_count: 10
---

> Part of [[products-vendors]]. See the hub for the other aspects (the Add / Edit modal, business rules + backend behaviour).

# Vendors — list, filters & bulk actions

## Purpose

The table view of the **Vendors** screen — where the merchant browses, sorts, searches, and filters the store's vendors, opens any one for editing, and bulk-deletes vendors. This is also the home of the **cleanup workflow** (find and remove orphan vendors with no products) and the place where the merchant works around the lack of a native vendor-merge tool.

## Where to find it

Sidebar → Products → **Vendors**. The list is the first thing shown on the page (route `/admin/products/vendors`); the Add / Edit modal opens on top of it (see [[products-vendors-editor]]).

## What the merchant can do here

- See all vendors in a paginated table: ID, Name, Created at, Updated at, Products count, plus per-row Edit / Delete actions.
- Sort by ID, Name, Created at, Updated at, or Products count.
- Filter by **Has products** — Yes / No.
- Search by name in the table's search box.
- Click + **Add vendor** to open the create modal (see [[products-vendors-editor]]).
- Click any row's name (or the Edit icon) to open the edit modal pre-filled with the vendor's data.
- Bulk-select rows and **bulk-delete** via the standard delete bulk action.

## Settings & fields

### List columns

| Column | Notes |
|--------|-------|
| **ID #** | Sequential vendor ID. Sortable. |
| **Name** | Vendor name. Sortable. Click opens Edit. |
| **Created at** | When the vendor was added. Sortable. |
| **Updated at** | Most recent edit. Sortable. |
| **Products** (`items_count`) | Count of products assigned to this vendor. Sortable. Informational only — clicking it does not open a product list. |
| **(actions)** | Per-row Edit + Delete buttons. |

### Filters & sorting

- **Has products** — `Yes` / `No`. Find vendors with no assigned products (candidates for cleanup) or vendors that have products (a useful marketing list).
- **Search** — free-text `query` across the vendor name.
- Sortable columns: `id`, `name`, `items_count`. Default sort: `id DESC` (newest first).

## Business rules

### "Has products" filter — the cleanup workflow

The **Has products** filter is most useful as a cleanup tool: filter `Has products = No` to surface orphan vendors (created but never assigned to a product), then bulk-delete them in one pass. Because deletion is blocked while a vendor still has products (see [[products-vendors-rules]]), the `No` filter pre-selects exactly the rows that will delete cleanly.

### Bulk-delete is all-or-nothing per blocked vendor

Bulk-delete validates every selected vendor before deleting. If any one vendor in the selection still has products (or an active XML-import task), the **whole batch fails** and the response lists the blocked vendor names — *"Some vendors still has products: …"*. The merchant must clear the blocking references first. Full deletion-blocking mechanics are on [[products-vendors-rules]].

### What this screen does NOT do

- It does **not** show which specific products belong to a vendor — the Products count is informational. To list a vendor's products, go to [[products-products]] and apply the Vendor filter.
- It does **not** reassign products between vendors — that is the Change vendor bulk action on [[products-products]].

### No native merge tool

If the merchant ends up with duplicate vendors (e.g., *"Apple"* and *"Apple Inc."* created by separate imports), there is **no one-click merge**. The merchant must (a) reassign every product from the duplicate to the canonical vendor using the [[products-products]] **Change vendor** bulk action, then (b) delete the now-empty duplicate from this list. This is a known gap worth flagging during catalogue cleanup.

### Permission

Reaching this list and acting on it requires the products / vendors permission grant. Moderators without it do not see the Vendors sidebar entry. (The read-only autocomplete used by the product editor's vendor picker has a broader gate — see [[products-vendors-rules]].)

## Related

- [[products-vendors]] — hub.
- [[products-products]] — list a vendor's products (Vendor filter) and reassign products (Change vendor bulk action) — both required for the merge workaround.
- [[apps-csv-import]] — bulk-create vendors (not available from this list).
- [[vendor]] — entity page.

## Open questions

None.
