---
type: feature
nav_path: "Orders → User Files → List view"
route_name: admin.order-files.list
route_path: /admin/order-files
aliases: ["User files list", "Order user files list", "Customer uploads list", "File list grid", "Списък с файлове на потребителите"]
tags: [orders, files, customer-uploads, list-view, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-user-files]]. See the hub for the other aspects (deletion, data model, storage & delivery).

# User Files — the list view

## Purpose

The table that renders every customer-uploaded file in the store, newest first, so the merchant can scan, locate, and open the file that belongs to a given order / product / option. This aspect covers what the grid shows and how the merchant navigates it — not how files are created (see [[orders-user-files-data-model]]) or deleted (see [[orders-user-files-delete]]).

## Where to find it

Sidebar → **Orders** → **User Files** (`/admin/order-files`). The grid is the whole page body below the *"User Files"* breadcrumb.

## What the merchant can do here

- **Scan the file list.** Two columns per row:

  | Column | Sortable | Notes |
  |--------|----------|-------|
  | **File** (composite) | No | Combines order-number link + product name + product-option label. Renders as a multi-line cell showing which order + product + option the file belongs to. |
  | **Action** | No | Per-row delete (X) icon — see [[orders-user-files-delete]]. |

- **Click the order link** in the File cell to jump to that order's details ([[orders-details]]).
- **Open / download the file** by following its `file_url` — see [[orders-user-files-storage-delivery]].
- **Page through the list.** Default sort is `id DESC` (newest uploads first). The merchant cannot change the sort column from the UI.
- **Select rows for bulk delete** via the checkbox + "Select all" master checkbox in the shared `bulk.tpl` chrome at the bottom of the table.

## Settings & fields

- **No search box, no filter categories.** The list uses the platform's `filters_without_search.tpl` partial — it renders only the bulk-action chrome, with no free-text search field and no filter chain. The merchant browses the full paginated list and locates a file by scanning rows or using the browser's in-page find (Ctrl/Cmd-F).
- **No status filter.** Files from ALL order statuses appear — cancelled / refunded orders' files are NOT hidden. There is no way on this page to scope to (say) only paid orders.
- **Bulk-action dropdown** offers a single action, **Delete** — documented on [[orders-user-files-delete]].

## Business rules

### AJAX grid load

The page uses the platform's standard grid-wrapper pattern with `data-url` for AJAX loading. On initial render the merchant sees a loading spinner, then the data populates. The grid supports pagination and bulk-action selection through the standard table-grid helpers.

### Empty state

When no file-type option with a non-null value exists anywhere in the store, the grid is hidden and the merchant sees:

- *"You have not added any files yet"* heading.
- *"Your files will show up here"* paragraph.
- A help-link box: *"Having trouble with files? Follow the link below."* + a link to the support center.

### Empty state is COUNT-gated, and re-shows dynamically

The empty state is decided by a COUNT of file-type non-null records at page-load time. If the count is zero, the grid is hidden and the empty state shows. If a [[orders-user-files-delete|delete]] reduces the count to zero, the grid is hidden dynamically and the empty state re-appears without a full reload.

### What "appears as a row" means

Only an actual upload counts. A product that *defines* a file option but where no customer ever uploaded a file does NOT produce a row — the list reflects real `value`-bearing uploads, not option definitions. The full creation rule is on [[orders-user-files-data-model]].

## Related

- [[orders-user-files]] — hub.
- [[orders]] — parent orders list.
- [[orders-details]] — order the File cell links to.
- [[orders-products]] — the line items the file options attach to.

## Open questions

None.
