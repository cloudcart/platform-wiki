---
type: feature
nav_path: "Invoices → Download → Scope"
route_name: admin.core.export
route_path: /admin/api/core/export-import/download_invoices
aliases: ["Invoice download scope", "Download invoices filters", "Download invoices everything", "No targeted orders nor all"]
tags: [orders, invoices, download, filtering, accounting]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---
# Invoices bulk download — scope

> Part of [[orders-invoices-download]]. See the hub for related aspects (entry point, sync/async, rendering, permissions/plan).

## Purpose

Documents **which** invoices go into the ZIP. The Download button forwards the [[orders-invoices]] list's filter query, but the `download_invoices` action reads only the legacy `extra.ids` / `extra.dates` parameters — which the current UI no longer sends — so the bundle currently contains **every invoiced order regardless of the applied filter**. There is no separate date-range picker and no per-row selection.

## Where to find it

The scope comes from the [[orders-invoices-list-filters|filter panel]] on [[orders-invoices]] (the filter chips + the search box). The **Download** button in the header (see [[invoices-download-entry-points]]) forwards whatever the list currently shows.

## What the merchant can do here

- **Filter the on-screen list** — by **Date** (Between / Exactly / Before / After; the order's **placement date**, not the invoice-issue date — see [[orders-invoices-list-filters]]), **Customer**, **Credit note**, or the **search box** (order / invoice number, customer name).
- **Note the Download does not follow the filter (current build)** — whatever the list shows, the Download button currently bundles **all** invoiced orders; the filter is not applied to the bundle.
- **Download everything** — leave the list unfiltered; Download then bundles the whole invoiced set from the start.

### What the merchant CANNOT do here

- Pick individual rows — there is no per-row selection on this list; scope is filter-based, not selection-based.
- Narrow the download by the on-screen filter (current build) — the Download button ignores the applied filter and bundles all invoiced orders.

## Settings & fields

The scope controls are the list's own filters and search box — the full field table lives on [[orders-invoices-list-filters]]. This page only describes how the Download button consumes them:

- **Filter NOT applied to the download** — the button forwards the list's filter query, but the action does not consume it (it reads the legacy `extra.ids` / `extra.dates`), so the bundle covers all invoiced orders regardless of the on-screen filter.
- **No filter → everything** — with nothing applied, the action covers every invoiced order.

## Business rules

### Scope — currently all invoiced orders (the filter is not consumed)

The Download button forwards the list's filter query (date / credit-note / customer / search), but the `download_invoices` action reads only the legacy `extra.ids` / `extra.dates` parameters — which the current UI no longer sends. So the applied filter scopes the **on-screen list** only; the bundle currently contains **every invoiced order**. The button does not depend on ticked rows (there is no row selection) and there is no header date-range picker.

### Unfiltered list downloads everything

With no filter applied, the action's base set is every invoiced order (orders that have an `invoice_number`). On a large store this is a "download everything" job that goes async — see [[invoices-download-sync-async]].

### Empty scope returns a specific error

If the applied filters match zero invoices, the action returns `status: error` with the message *"No targeted orders nor all"* (keyed `global.err.invoice.no_targeted_orders_nor_all`). This is distinct from a failure — it means the filter scope is empty, not that the operation broke. Nothing is downloaded or queued.

### Only invoiced orders are ever in scope

The list — and therefore any download from it — only ever contains orders that already have an invoice number. Orders without an invoice are never included.

## Open questions

(none.)

## Related

- [[orders-invoices-download]] — hub.
- [[orders-invoices]] — parent invoices list where the filters live.
- [[orders-invoices-list-filters]] — the filter panel + search box that define the scope (and the placement-date note).
- [[invoices-download-sync-async]] — how the scoped count decides sync vs async delivery.
- [[invoice]] — entity page (`invoice_number`, `invoice_date`).
