---
type: feature
nav_path: "Orders → List → Columns & header actions"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Orders list columns", "Order list grid columns", "Orders header actions", "Order list sortable columns", "Колони на списъка с поръчки"]
tags: [orders, list, columns, sortable, header-actions, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders]]. See the hub for the other aspects (filters, bulk actions, status taxonomy, default visibility, export, locking).

# Orders list — columns and header actions

## Purpose

The list table on `/admin/orders` is the merchant's first read of every order. This aspect documents the **8 default columns (+ 1 conditional)**, which columns are sortable, the comment-icon affordance, and the two header buttons sitting above the table: **+ Add order** and **Export**.

## Where to find it

Sidebar → **Orders**. The header buttons sit above the filter bar; the column row is the table's first row.

## What the merchant can do here

### Header actions

- **+ Add order** — opens a slide-in panel (the manual-order creation flow). Clicking the header button opens the manual-order side-panel inline (via `data-ajax-panel` with class `wide order-preview`). See [[orders-add]] for the full panel contents, fields, and validation.
- **Export** — opens the export flow, which first asks for a **two-factor confirmation code**. The full mechanics (what it contains, inline vs emailed delivery) live on [[orders-list-export]]. The whole header region — including this button — is omitted on a store with no orders at all.

### List columns (8, plus 1 conditional)

| Column | Width | Notes |
|--------|-------|-------|
| **Order** (`number`) | 250 | Order number + key badges (Draft / Fast order / Archived). Sortable. |
| **Address** | 400 | **City on the first line, country on the second** — no recipient name. Not sortable. |
| **Date** (`date_added`) | 120 | When the order was placed. Sortable. Displayed via `date_added_formatted`. |
| **Fulfillment** | 200 | The shipping provider / courier (Econt / DPD / etc.). Sortable (by the date the order was fulfilled). |
| **Receiving** | 200 | Expected delivery / receipt date. Sortable. |
| **Shipping date** (conditional) | 150 | Visible only when the **Shipping Hours** app is installed. Shows the per-hour delivery window. Sortable. |
| **Status** | 200 | Order status badge (centered, colour-coded). Not sortable. |
| **Total** (`price_total`) | 150 | Order total amount (right-aligned). Sortable. Displayed via `price_total_formatted`. |
| **Comment** (icon) | — | File icon — clickable to surface the merchant's note on the order. Not sortable. |

### Sortable columns — five (six with Shipping Hours)

Sortable: **Order** (`number`), **Date** (`date_added`), **Fulfillment**, **Receiving**, **Total** (`price_total`) — plus **Shipping date** when the Shipping Hours app is installed. Sorting by **Fulfillment** orders by the date the order was fulfilled; sorting by **Receiving** orders by the recorded delivery date. Both are useful for "what went out first / what lands first" reviews.

Only **Address**, **Status** and **Comment** are display-only. Status is colour-coded but cannot be sorted — to group by status the merchant applies a Status filter (see [[orders-list-filters]]).

The default sort is by order ID descending (newest orders first) — see [[orders-list-default-visibility]] for default-sort details.

### Comment icon

The comment column renders a file icon when the order has an admin note. Clicking surfaces the merchant's note in a small popover — no need to open the full order detail to read the note. Notes are added / edited from [[orders-details]] (admin note textarea — see [[orders-details-actions]]).

## Settings & fields

The list reads from the orders query API. The data shape behind each column is fixed; the merchant cannot add, remove, or reorder columns from the UI.

Conditional column rules:

- **Shipping date** column appears only when the **Shipping Hours** app is installed. Without it, the merchant sees 8 columns instead of 9.

## Business rules

### Sortable-column whitelist is fixed

Only the columns listed above are wired for server-side sort. Clicking **Address**, **Status** or **Comment** does nothing (no client-side sort fallback).

### Address column shows city and country — not the recipient

The Address column shows the shipping address's **city** on one line and its **country** underneath. It does **not** show the recipient's name or street, so a merchant scanning the list cannot tell two orders to the same city apart by this column. When the order has no shipping address the cell reads *"No address"*. The full address is on [[orders-details]] → addresses sidebar (see [[orders-details-addresses]]); to find an order by recipient, use the free-text search box or the **Region** filter on [[orders-list-filters]].

### Status column shows badge, not text — and may say "Fulfilled"

The **Status** column renders a colour-coded badge (per the [[settings-statuses]] taxonomy). Whenever the order is **fulfilled** and its status is neither `completed` nor `cancelled`, the badge shows the word **Fulfilled** instead of the order status — so a paid, dispatched order appears in this column as *Fulfilled*, not *Paid*. Nothing about the order has changed; see [[orders-details-header]]. To scope to a specific status the merchant uses the **Status** filter.

### Comment icon is read-only from the list

Clicking the comment icon opens a read-only popover. To EDIT the note, the merchant opens the order's detail page. The list does not surface inline edits for any column.

### + Add order opens an inline side-panel, not a new page

Unlike most navigation in the admin, **+ Add order** does NOT navigate to `/admin/orders/add` — it opens an inline side-panel from the same list URL. The full add-flow URL ([[orders-add]]) is still navigable directly; the header button is a convenience.

## Related

- [[orders]] — hub.
- [[orders-list-filters]] — filter bar (sits above the table).
- [[orders-list-export]] — Export header button mechanics.
- [[orders-list-default-visibility]] — default sort behaviour.
- [[orders-add]] — manual-order add flow opened by the **+ Add order** button.
- [[orders-details]] — per-order detail page reached by clicking any row.
- [[orders-details-addresses]] — full address surface (vs the summarised Address column).
- [[orders-details-actions]] — where the admin note is edited.
- [[orders-details-header]] — why the Status column can read "Fulfilled".
- [[settings-statuses]] — status badge colour taxonomy.

## Open questions

None.
