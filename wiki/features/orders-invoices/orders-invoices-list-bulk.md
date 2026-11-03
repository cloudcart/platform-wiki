---
type: feature
nav_path: "Invoices → Download / Export"
route_name: admin.invoices.list
route_path: /admin/invoices
aliases: ["Bulk invoice download", "Invoice download button", "Invoice export button", "Invoice register export", "Download all invoices", "Масово изтегляне на фактури", "Експорт на фактури", "Изтегли фактури"]
tags: [orders, invoices, list, bulk, download, export, accounting]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices]]. See the hub for the other aspects (list table, filters, verification modal).

# Invoices — Download & Export

## Purpose

The two header actions on the [[orders-invoices]] list that turn the filtered invoice set into a deliverable file: **Download** (the matching invoices as a PDF bundle / ZIP) and **Export** (the filtered list as a CSV register). Both act on the **currently-applied filters** — built for the accounting workflow of pulling a whole period at once.

## Where to find it

Sidebar → **Invoices**. **Download** and **Export** are the two buttons in the **top-right header**. There is **no** date-range picker beside them and **no** per-row bulk menu. Both buttons forward the [[orders-invoices-list-filters|filter panel]] query, but the backend actions currently ignore it — see the scope note below.

## What the merchant can do here

- **Download** — package the matching invoices' PDFs into a single ZIP.
- **Export** — export the matching invoices as a CSV register for an accounting system.

Both currently cover **every invoiced order** — the whole list — **regardless of the applied filter** (see the scope note below). The filter narrows only the list you see on screen, not the file you get.

## Settings & fields

### The two header buttons

- **Download** — matching invoice PDFs bundled into a ZIP.
- **Export** — matching invoices as a CSV register (columns below).

Both **forward the list's current filter query** to the action, but the `download_invoices` / `export_invoices` actions read only the legacy `extra.ids` / `extra.dates` parameters — which the current UI no longer sends — so the filter is **not** applied to the file. There is **no** "Download all (X)" counter and **no** row-selection / per-row bulk dropdown in the current UI.

### Export — fixed CSV columns

The export uses a fixed column set covering order + invoice metadata (date, order ID, invoice number, customer, total, credit-note ref). The merchant CANNOT pick custom fields from this UI — it is a single canonical schema designed to feed accounting systems. See [[orders-invoices-export]].

## Business rules

### Scope — currently ALL invoiced orders (the filter is not applied to the file)

The buttons **forward** the list's current filter query (date / credit-note / customer / search box), but the `download_invoices` / `export_invoices` actions read only the legacy `extra.ids` / `extra.dates` parameters — which the current UI no longer sends. So the applied filter narrows the **on-screen list** but **not** the downloaded / exported file: **both currently cover every invoiced order regardless of the filter.** (This is the reason a merchant who filters by date still gets all invoices in the download — the list-vs-file mismatch introduced by the redesign.) The buttons also do not depend on ticked rows (there is no row selection) and there is no header date-range picker.

### Both actions are 2FA-gated

Each button opens the shared verification step before running (when 2FA is active) — see [[orders-invoices-list-verification]]. A **small** result returns immediately (a CSV download, or a ZIP PDF bundle); a **large** one is **queued** and delivered by an email link. Status appears in [[settings-queue-view]].

### Read-only beyond Download / Export

The invoice list exposes no bulk-delete, bulk-cancel-invoice, or bulk-status-change — it is read-only apart from these two actions. Invoice numbers are issued per-order on [[orders-details]], never from here.

### Invoice-numbering changes do not disrupt a download

When the merchant changes `invoice_number_formatting_*` in [[settings-invoicing]] (e.g. a new fiscal-year prefix), existing orders keep their previously-assigned numbers; only future-issued invoices use the new format. Downloads / exports show all historical numbers as-is.

## Related

- [[orders-invoices]] — hub.
- [[orders-invoices-list-filters]] — the filters both buttons consume (and where to set the period).
- [[orders-invoices-download]] — the PDF-bundle Download in detail.
- [[orders-invoices-export]] — the CSV Export in detail.
- [[orders-invoices-list-verification]] — the 2FA step that guards both.
- [[settings-queue-view]] — async job status for large jobs.
- [[settings-invoicing]] — the Invoicing provider that renders the PDFs + the number formatting.

## Open questions

None.
