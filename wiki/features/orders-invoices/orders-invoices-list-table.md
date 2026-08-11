---
type: feature
nav_path: "Invoices → List table"
route_name: admin.invoices.list
route_path: /admin/invoices
aliases: ["Invoice list table", "Invoice columns", "Invoice list rows", "Per-row invoice download", "Колони в списъка с фактури"]
tags: [orders, invoices, list, table, accounting]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices]]. See the hub for the other aspects (filters, verification modal, bulk download / export).

# Invoices — list table & per-row download

## Purpose

The table at the centre of the cross-order [[orders-invoices]] list. It shows ONLY orders that have a generated invoice number (a non-null `invoice_number`), one row per such order, with a per-row download link for the invoice PDF (and the credit-note PDF when one exists). This is the read surface the merchant scans before bulk-downloading or exporting for accounting.

## Where to find it

Sidebar → **Invoices** (when invoicing is enabled). The table is the Vue list on `/admin/invoices`.

## What the merchant can do here

- **Scan invoice-generating orders** — every row is an order that has an issued invoice number; orders without one never appear here.
- **Open an order** — the **Order #** cell is clickable and opens the order in [[orders-details]].
- **Download a single invoice PDF** — the per-row Download link (per-order PDF).
- **Download a credit note** — a SECOND button appears in the row when the order also has a credit note.
- **Sort** by Date, Order #, Customer, or Total (see Settings & fields).

## Settings & fields

### Columns (6)

| Column | Sortable | Notes |
|--------|----------|-------|
| **Date** | Yes (default sort) | When the order was placed (`date_added_formatted`). |
| **Order #** | Yes (maps to `orders.id`) | The order's number — clickable to open the order in [[orders-details]]. |
| **Invoice #** | No | The generated invoice number. |
| **Customer** | Yes (maps to `customer_first_name`) | Customer name. |
| **Total** | Yes | Order total (currency-formatted). |
| **View** | No | Per-row download link (single invoice PDF; a second button for the credit note when present). |

### Sortable columns

- `date_added` (default — descending).
- `number` (mapped to `orders.id`).
- `customer` (mapped to `customer_first_name`).
- `price_total`.

## Business rules

### Rows are orders, not a separate invoice table

The list joins to the orders table and returns only orders whose invoice number is not empty. The merchant sees the same data shape as [[orders]], pre-filtered to invoice-generating orders. There is no standalone invoice record being listed — corrections require editing the underlying order.

### Per-row Download routes to the same per-order invoice endpoint

Each row's Download column links to the per-order invoice route — the same one used from [[orders-details]] → View invoice, documented on [[orders-invoice]]. When the order also has a credit note (`credit_number` is not null), a SECOND **Download credit note** button appears next to it. So a row's action area contains one or two buttons depending on the order's credit state. Both buttons open in a new tab (`target="_blank"`).

### The nav link opens the list pre-filtered to last month

Reaching Invoices from the sidebar **Orders → Invoices** link pre-applies a **last-month** Date filter (carried in the URL), so the list opens already scoped. Opened without any filter, the query returns ALL orders with a non-null `invoice_number`, sorted by `date_added` DESC. For very large stores, apply the **Date** filter (in the [[orders-invoices-list-filters|filter panel]]) to keep the list responsive. Note: the filter scopes the list only — the Download / Export currently cover all invoiced orders regardless (see [[orders-invoices-list-bulk]]).

### Performance — filtered at the database level

The page queries orders whose invoice number is not empty, filtered at the database level against an index on the invoice-number column. For very large stores (1M+ orders) the merchant should narrow by date range before relying on the full list.

### Empty selection on filter + page > 1 — auto-fallback to page 1

If the merchant applies a filter while on, say, page 3, and the filtered result set is smaller than that page would require, the platform silently re-queries from page 1 instead of returning an empty page. The merchant always sees results when results exist.

### Read-only beyond download

The merchant CANNOT generate, edit, re-issue, or void an invoice from this table — those are per-order actions on [[orders-details]] / [[orders-invoice]]. Invoice numbering is never triggered from this list; orders without an invoice number simply do not appear here. A merchant who expects an order and doesn't see it should first confirm an invoice was issued on that order.

### Vue list, filter-driven

The table is the platform's Vue list component; it re-fetches on filter / pagination / sort changes without a full page reload. The list query honors the filter chips (the Download / Export buttons do not — see [[orders-invoices-list-bulk]]).

## Related

- [[orders-invoices]] — hub.
- [[orders]] — parent orders list (the source of the invoice data).
- [[orders-details]] — where individual invoices are generated; the Order # cell links here.
- [[orders-invoice]] — per-order Invoice download flow (the route the per-row link uses).
- [[orders-credit]] — credit-note flow (the second per-row button).
- [[order]] — entity page.

## Open questions

None.
