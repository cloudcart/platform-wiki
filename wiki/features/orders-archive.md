---
type: feature
nav_path: "Orders → Order details → Archive (toggle / bulk)"
route_name: admin.orders.archive.toggle
route_path: /admin/orders/action/archive/:order_id/toggle
aliases: ["Archive order", "Unarchive order", "Bulk archive", "Bulk unarchive", "Архивиране", "Деархивиране"]
tags: [orders, archive, list-management, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 7
---
# Order archive (toggle + bulk)

## Purpose

The **archive flow** moves orders OUT of the default [[orders]] list view (hidden from "all orders" unless explicitly filtered) while preserving ALL their data. It is the platform's **only** cleanup mechanism — there is no delete for an order anywhere in the admin panel or the API. Typical uses:

- **End-of-period cleanup** — archive completed orders from a previous fiscal year to reduce daily-view noise.
- **Keep the list focused** — keep only "active" orders (`pending` / `paid` / not-yet-completed) visible; archive `completed` / `cancelled` ones.
- **Performance** — on stores with 1M+ orders, archiving shrinks the active dataset that filters scan.

The merchant gets it via two paths: a **per-order toggle** from [[orders-details]], and a **bulk archive** from the [[orders]] list.

## Where to find it

### Per-order
From [[orders-details]] → top-right **3-dot menu** (`breadcrumb-settings-button`) → **Archive** (when not archived) or **Unarchive** (when it is). The label flips based on the order's current archive state.

Visible only when the order's status is `completed` or `cancelled`. The whole 3-dot menu is hidden when none of its actions qualify (e.g. a `pending` order with sold-out stock, or a `paid` order not yet fulfilled).

Route: `admin.orders.archive.toggle` (GET) — toggles archive / unarchive based on current state.

### Bulk (from list)
From the [[orders]] list → multi-select rows → bulk action **Archive** OR **Unarchive** → confirmation → applies to all selected.

Route: `admin.orders.archive-bulk` (POST). A single URL parameter flips direction: `/admin/orders/archive-bulk/yes` archives, `/admin/orders/archive-bulk/no` unarchives. Selected order IDs are passed in the POST body.

## What the merchant can do here

### Per-order toggle

| Current state | Dropdown shows | Result on click |
|---------------|---------------|-----------------|
| Not archived | **Archive** | Order moves to archive; label flips to **Unarchive**. |
| Archived | **Unarchive** | Order returns to active list; label flips to **Archive**. |

Click → AJAX call → toast confirms → dropdown label updates in place (the response returns `archived: true/false` plus the new `replace` label text, so no page reload is needed) and the order wrapper picks up an "archived" CSS class as a visual indicator.

### Bulk archive / unarchive

| Bulk action | Confirmation string (verbatim) | What it does |
|-------------|--------------------|--------------|
| **Archive** | *"This will archive your order. Please confirm."* | All selected orders moved to archive — **only if every one qualifies** (see Business rules). |
| **Unarchive** | *"Do you want to unarchive?"* | All selected orders restored. No status restriction. |

Both are phrased in the singular even though they act on the whole selection. The same bulk dropdown also carries **Mark as completed** — that flow is documented on [[orders-status-change]] and [[orders-list-bulk-actions]].

### Viewing archived orders

Archived orders are HIDDEN from the default [[orders]] list. To see them, apply the **Archived = Yes** filter; use **Archived = No** (or unset) for active only. When no filter is applied, archived orders are simply absent — the list does not visually mark them.

### What the merchant CANNOT do here

- Archive a `pending` or `paid` order — the option is hidden and the action is rejected (see Business rules). Cancel or complete it first. (Draft orders are the exception.)
- Reverse anything via archiving — archive does not refund, restore stock, or undo fulfilment. To reverse a charge the merchant refunds; to restore stock they cancel.
- **Permanently delete an order — by any route.** Archive is not a soft-delete on the way to a hard delete: there is no delete button on the order detail page, no bulk delete on the list, and the JSON-API v2 orders resource excludes DELETE. Archiving is as far as removal goes.
- Auto-archive orders older than N days — there is no automatic archive policy.

## Settings & fields

The order has a `date_archived` timestamp column — the **only** field the archive flow changes:

- `null` → not archived (active).
- timestamp → archived at that time.

Archive sets it to the current time; unarchive clears it back to `null`. The 3-dot dropdown and the list's **Archived** filter both read this field to determine state. No products, payments, fulfilment, or stock are touched.

## Business rules

### Archive is data-preserving
Archiving does NOT delete, anonymise, or change order data. Line items, customer association, payments, shipping records, invoice numbers, credit notes, and the history timeline are all kept. It is purely a visibility / list-membership flag, fully reversible by unarchiving.

### Restricted to completed / cancelled (verified)
The action throws *"Only completed orders can be archived."* for any status other than `completed` or `cancelled`. (The message is misleading — `cancelled` is allowed too.) Active orders stay visible because the merchant still has work to do on them. **Draft orders are exempt** — an order with the `is_draft` flag can be archived in any state (`pending`, `paid`, etc.), so a long-lived quote/draft can be hidden and unarchived later when ready to convert.

**Unarchiving is unconditional** — any archived order can be restored regardless of its status.

### Archive locks status changes (verified)
Once archived, an order is frozen against status changes. Attempting a transition returns *"Cannot change the status of archived order. Unarchive first."* This is the platform's mechanism for preventing accidental edits on "closed" orders. Archived orders also block discount edits (see [[orders-discount-add]]) and customer edits (see [[orders-customer-change]]).

### Bulk is all-or-nothing (verified)
The whole bulk run is wrapped in a **single** database transaction. The first order failing the `completed` / `cancelled` gate (e.g. a `pending` order in the selection) throws and the **entire batch rolls back** — NONE are archived, including the ones that would have qualified, and the merchant sees only the *"Only completed orders can be archived."* error with no indication of which row caused it.

Practical workflow: filter the list to `completed` / `cancelled` (or **Archived = No** plus a status filter) BEFORE selecting, so the selection cannot contain an ineligible order. **Unarchive** is unrestricted and cannot fail this way.

### Idempotent (verified)
Re-archiving an already-archived order (or re-unarchiving an active one — e.g. via two browser tabs) returns silently: no error, no duplicate history entry.

### Side effects (verified)
- `date_archived` set on archive, cleared on unarchive.
- Order disappears from / reappears in the default [[orders]] list.
- An archive/unarchive event IS recorded in [[orders-history]], showing the acting admin and timestamp.
- NO `order.updated` webhook fires (see [[settings-hooks]]).
- NO customer notification — archive is a purely internal, merchant-side bookkeeping action, invisible to external systems and customers.

### Permission
Standard orders permission scope.

## Related

- [[orders-details]] — parent page (3-dot dropdown action).
- [[orders]] — list (bulk action + Archived filter).
- [[orders-history]] — captures the archive/unarchive event.
- [[orders-discount-add]] — archived orders block discount edits.
- [[orders-status-change]] — archived orders block status changes; shares the bulk dropdown.
- [[orders-customer-change]] — archived orders block customer edits.
- [[settings-hooks]] — `order.updated` webhook does NOT fire on archive.
- [[order]] — entity page.

## Open questions

None — all previously-flagged items verified against the backend.
