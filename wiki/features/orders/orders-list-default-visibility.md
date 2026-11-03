---
type: feature
nav_path: "Orders → List → Default visibility & sort"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Orders default visibility", "Orders default sort", "Hidden by default cancelled voided archived", "Order list default exclusion", "Order count discrepancy", "Видимост по подразбиране на списък с поръчки"]
tags: [orders, list, default-visibility, sort, hidden-orders, support-tickets]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders]]. See the hub for the other aspects (columns, filters, bulk actions, status taxonomy, export, locking).

# Orders list — default visibility and sort

## Purpose

When the merchant first opens **Orders** with NO filters applied, the list silently hides three classes of orders: those with status `cancelled`, those with status `voided`, AND archived orders (regardless of status). This is the single most common cause of "I have orders missing from the list" support tickets. This aspect documents the exact rule, the implication for "count of orders" reads, and the default sort (Order ID descending).

## Where to find it

`/admin/orders` on first load (no `filters[...]` in the URL). The "missing" orders only reappear when the merchant adds a Status or Archived filter.

## What the merchant can do here

### See the default view

With no filters applied: the list shows every order EXCEPT those whose status is `cancelled` or `voided`, AND EXCEPT archived orders. The total count surfaced in the list header is the count of *visible* rows — NOT the count of all orders in the system.

### Reveal the hidden orders

| What's hidden | How to reveal |
|---|---|
| `cancelled` orders | Add **Status** filter → **Is cancelled**. |
| `voided` orders | Add **Status** filter → **Is voided**. |
| Archived orders (any status) | Add **Archived = Yes** filter. |
| ALL orders regardless of status / archive | Add **any** filter at all — even a date range or a word in the search box. The whole exclusion is dropped at once. |

### Default sort — Order ID descending (newest first)

The default sort is by order ID descending. The "Order number" column maps internally to `orders.id` and the default direction is `desc`. Because order ID and date-added increase together, this is effectively newest-first by date too.

Sortable columns: **Order**, **Date**, **Fulfillment**, **Receiving**, **Total** — plus **Shipping date** with the Shipping Hours app (see [[orders-list-columns]]). Clicking any column header flips the sort direction; clicking a different sortable column resets to the new column's default direction.

## Settings & fields

There is no UI setting to change the default-visibility behaviour. It is hard-coded into the orders-list query.

There is no UI setting to change the default sort. The merchant manipulates sort by clicking column headers; unlike the filters, the sort choice is not part of the remembered filter set.

## Business rules

### Default list silently HIDES cancelled, voided AND archived orders

The single most important behaviour merchants miss: a merchant counting orders against "what's in the list" will UNDER-count actual orders in the system. The rule:

- Status `cancelled` → hidden on default load.
- Status `voided` → hidden on default load.
- `archived = yes` → hidden on default load, REGARDLESS of status.

### Applying ANY filter drops the WHOLE exclusion — archive included

The exclusion is a single all-or-nothing switch, not three independent rules. The moment **any** filter registers — a status, a date range, a customer, a discount code, or just a word typed into the free-text search box — the platform stops excluding **all three** classes at once. Archived orders reappear together with cancelled and voided ones, without the merchant ever asking for **Archived = Yes**.

Two practical consequences:

- `Date added = Today` shows **more** orders than the unfiltered list — including archived ones the merchant deliberately put away.
- Two filter sets that look logically equivalent can return different counts purely because one of them is "no filter at all".

### Implications for "order count" support tickets

A common ticket is *"I had 47 orders this month but the list only shows 42"*. Diagnostic walk:

1. Apply a **Date added** filter for the month in question — that alone reveals cancelled, voided *and* archived orders.
2. Reconcile against the export, which never applies the exclusion at all (see [[orders-list-export]]).
3. Remember that filters are **remembered across visits** ([[orders-list-filters]]) — a filter set days ago may still be narrowing the view.

### JSON-API v2 list endpoint does NOT inherit the default exclusion

The JSON-API v2 `/orders` endpoint returns ALL orders regardless of status or archived flag — it has no silent default exclusion. API consumers building a "total orders" widget should NOT compare counts against the UI list. See [[api-orders]] + [[json-api-v2]].

### Default sort is by `orders.id` desc (not `date_added`)

The default sort sorts by the order ID descending, NOT by `date_added`. This is **almost always** equivalent (IDs increase monotonically with creation time), but a merchant who manually sets a back-dated `date_added` on a draft order created in [[orders-add]] would see the order appear at the top of the list (newest ID) despite its older date. This rarely matters in practice.

### Custom-status orders inherit their parent canonical status's visibility

A custom status (defined on [[settings-statuses]]) is associated with a parent canonical status. If the parent is `cancelled` or `voided`, orders in that custom status are silently hidden by default — same as raw `cancelled` / `voided`. See [[orders-list-status-taxonomy]] for the canonical-vs-custom relationship.

## Related

- [[orders]] — hub.
- [[orders-list-filters]] — how to add filters to reveal hidden orders.
- [[orders-list-columns]] — sortable column whitelist.
- [[orders-list-status-taxonomy]] — canonical-status visibility rules.
- [[orders-list-bulk-actions]] — Archive / Unarchive actions that toggle the archive exclusion.
- [[orders-archive]] — per-order archive toggle.
- [[orders-export]] — export entry point.
- [[orders-list-export]] — the export never applies this exclusion.
- [[api-orders]] — JSON-API v2 list endpoint (no silent exclusion).
- [[json-api-v2]] — API overview.

## Open questions

- Does the JSON-API v2 `/orders` listing EVER apply implicit filters (e.g., respect the merchant's "include archived" preference), or is it always fully unfiltered by default? (verify)
