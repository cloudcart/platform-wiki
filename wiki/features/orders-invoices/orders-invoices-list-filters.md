---
type: feature
nav_path: "Invoices → Filters"
route_name: admin.invoices.list
route_path: /admin/invoices
aliases: ["Invoice filters", "Invoice date filter", "Credit note filter", "Invoice number search", "Филтри по фактури", "Филтър по период", "Филтър по дата фактури"]
tags: [orders, invoices, list, filters, accounting]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices]]. See the hub for the other aspects (list table, verification modal, bulk download / export).

# Invoices — filters

## Purpose

The filtering controls on the cross-order [[orders-invoices]] list. They let the merchant scope the list to a period, customer, or single invoice before **Download** / **Export** — the core accounting workflow. **All filters live in the filter panel (the filter row) plus a search box; there is NO separate date-range picker at the top of the page.**

## Where to find it

Sidebar → **Invoices**. The filters are the **filter chips** in the list's filter row; free-text lookup is the **search box** above the table. The header holds only the **Download** and **Export** buttons — no date-range picker.

## What the merchant can do here

- **Filter by date** — Between / Exactly / Before / After — scoping the **on-screen list** to a period (see the placement-date note below). Note: the filter narrows the list, but the Download / Export buttons currently ignore it and cover all invoiced orders — see [[orders-invoices-list-bulk]].
- **Filter by credit note** — Issued / Not issued — to find refunds still missing a credit note.
- **Filter by customer** — multi-select autocomplete (Is / Is not).
- **Search** — the search box matches **order number, invoice number, or customer name**.

## Settings & fields

### Filter panel (filter chips)

| Filter | Operators | Notes |
|--------|-----------|-------|
| **Date** | Between / Exactly / Before / After | Filters by the order's **placement date** (`date_added`) — see the note below. |
| **Credit note** | Issued / Not issued | Shows only invoices whose order has / hasn't a credit note. |
| **Customer** | Is / Is not (multi-select) | Autocomplete against the customer list (`customer_id`). |

### Search box

A free-text box above the table matches **order number**, **invoice number**, or **customer name** — a lookup, not a filter chip. Invoice numbers match on the stored value, so type the full number.

## Business rules

### The date filter is by ORDER placement date, not invoice-issue date

The single **Date** filter compares against the order's `date_added` — the date the customer **placed** the order — **not** the `invoice_date` (when the invoice number was issued). For most stores the two coincide, but when invoices are issued hours or days after the order, a period selected here is keyed to placement, not issue. **There is no separate invoice-issue-date filter, and no top-of-page date-range picker, on this list** — an earlier design had one, but it is not in the current UI.

### Credit Note filter — only on this list

The Issued / Not issued Credit-Note filter is UNIQUE to the Invoices list; the standard [[orders]] list does NOT expose it. It is critical for tax compliance: when a merchant refunds an order they must issue a credit note (see [[orders-credit]]). Filtering **Not issued** alongside refunded orders surfaces orders that still need a credit note — a check only available here.

### Filters query the underlying orders

Filtering queries the underlying order data, not a separate invoice table — the merchant sees the same data shape as [[orders]] but pre-filtered to invoice-generating orders (see [[orders-invoices-list-table]]).

### No status filter, no multi-store filter, no order-total filter

Invoice status is not a filter here (use [[orders]] for that). There is no explicit store filter — on the Stores app each store sees only invoices for its own orders (via `shop_id`). The redesigned list also no longer exposes the order-total filter the earlier version had.

## Related

- [[orders-invoices]] — hub.
- [[orders]] — parent orders list (Credit Note filter is NOT available there).
- [[orders-credit]] — credit-note flow (the Credit Note filter cross-references this).
- [[orders-invoices-list-bulk]] — the Download / Export buttons that consume these filters.
- [[orders-invoices-list-table]] — the list columns the filters scope.
- [[settings-invoicing]] — `invoice_number_formatting_*` controls the number format the merchant types.

## Open questions

None.
