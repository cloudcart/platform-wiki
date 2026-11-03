---
type: feature
nav_path: "Invoices → Export"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_invoices
aliases: ["Invoices export", "Export invoices", "Invoice CSV export", "Invoice metadata export", "Експорт на фактури", "Износ на фактури"]
tags: [orders, invoices, export, csv, 2fa, async, accounting]
plan_gates: ["invoices"]
created: 2026-05-23
updated: 2026-07-29
source_count: 7
---
# Invoices export (CSV)

## Purpose

The **Export** button on [[orders-invoices]] — the top-right header action that turns the invoice list into a **CSV register** of structured invoice metadata (invoice number + order + customer + total + credit-note reference). It feeds external accounting systems (Excel bookkeeping, ERP imports, tax-filing tools) that need the data in tabular form, not as PDF.

Export is the **structured-data complement** to the **Download** button (invoice PDFs bundled into a ZIP — see [[orders-invoices-list-bulk]] / [[orders-invoices-download]]). Many merchants use the CSV for their accountant's spreadsheet and the PDF bundle for the actual documents.

The Export button is **2FA-gated**. There is **no** row selection, **no** "Download all" counter, and **no** date-range picker. It forwards the list's filter query, but the `export_invoices` action reads only the legacy `extra.ids` parameter — which the current UI no longer sends — so it currently exports **every invoiced order regardless of the applied filter**; the filter scopes only the on-screen list (see [[invoices-export-trigger]]).

This page is the **hub** for the invoices-export cluster. It covers the entry point, the plan gate, and points to the four aspect pages below for the detail.

## Sub-pages (in this cluster)

The export is split into four aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[invoices-export-trigger]] — how to launch the export: the header **Export** button, the shared 2FA modal, how the scope is captured from the applied filter chips (not selected rows), the 10-invoice sync-vs-async threshold, and the resulting filenames.
- [[invoices-export-columns]] — the fixed 12-column schema; English-only headers; one-row-per-line-item rule; the three-source `name` fallback; the `eik = 999999999` placeholder; `mol`-only-when-company; currency = invoice currency.
- [[invoices-export-credit-notes]] — how credit-note rows are appended after the invoice rows, with both `invoice_number` + `credit_number` set and `amount`/`price` emitted as NEGATIVE numbers, and how the accountant matches them.
- [[invoices-export-async-processing]] — what happens over 10 invoices: 500-per-chunk background jobs, ZIP-of-parts bundle, email-only delivery, CRLF + UTF-8 BOM encoding, no incremental tracking, and retention.

## Where to find it

Sidebar → **Invoices** → **Export** (top-right header button, next to **Download**).

The Export action is the header button — there is no per-row bulk menu and no date-range picker. **In the current build the export covers all invoiced orders regardless of the filter** — the filter narrows only the on-screen list, not the exported file. See [[invoices-export-trigger]] for the full 2FA + scope flow.

## What the merchant can do here

- Export structured invoice metadata for the filtered invoice list as CSV — see [[invoices-export-trigger]].
- Feed the CSV into an accountant's spreadsheet or an ERP / tax-filing import.
- Note the scope caveat: the export currently covers **all** invoiced orders — the filter panel narrows only the on-screen list, not the exported file.

What the merchant CANNOT do:

- Choose between CSV / XLSX / XML — only CSV is produced via this action.
- Pick custom columns — the 12-column schema is fixed (see [[invoices-export-columns]]).
- Skip 2FA when 2FA email is enabled.
- Resume / cancel a running async job, or get an incremental "only since last export" file.

## Settings & fields

| Parameter | Value | What it controls |
|-----------|-------|------------------|
| **limit** | 10 | Threshold at/below which the export runs synchronously (CSV returned directly in the browser). Over 10 → async. See [[invoices-export-async-processing]]. |
| **chunk** | 500 | Async chunk size — each background job processes 500 invoices. |

### Permission

The `export_invoices` action sits behind the store's orders / invoicing permission scope — a moderator needs the invoices permission granted in [[settings-staff]] to reach the Invoices list and run the export.

## Business rules

- **Currently exports ALL invoiced orders (the filter is not applied).** The Export button forwards the list's filter query, but the `export_invoices` action reads only the legacy `extra.ids` parameter the current UI no longer sends — so it exports every invoiced order regardless of the applied filter. The filter narrows only the on-screen list (whose **Date** filter is the order's *placement* date `date_added`, not the invoice-issue date — see [[orders-invoices-list-filters]]).
- **Async threshold is 10 invoices** — lower than the orders-export threshold of 50, because invoice-export queries are more expensive (they join orders + customers + addresses + invoice fields). Over 10 → queued and emailed (see [[invoices-export-async-processing]]).
- **Fixed 12-column schema, English-only headers, one row per LINE ITEM.** See [[invoices-export-columns]].
- **Credit-note rows are appended with NEGATIVE amounts.** See [[invoices-export-credit-notes]].
- **Not the same as [[orders-export]].** This export covers ONLY invoiced orders and produces invoice-metadata columns; orders export covers ALL orders and produces order-metadata columns. The two CSVs have different column sets and row scopes.

## Plan gates

This feature is gated by the following plan-features (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `invoices` | Access gate (URL `invoices`) | The parent [[orders-invoices]] page is itself gated on `invoices` — when the plan lacks the feature the list page is inaccessible, so the **Export** header button is unreachable. The CSV export endpoint sits behind the same access path. |

When the gate is hit, the merchant is redirected to [[plan-features]] for the per-feature upsell. `invoices` is a boolean access gate — it requires a plan that includes the feature; it does NOT extend via feature packs ([[plan-vs-feature-pack]]).

## Related

- [[orders-invoices]] — parent invoices list (Export is a top-right header button).
- [[orders-invoices-list-bulk]] — the Download + Export header actions overview.
- [[orders-invoices-list-filters]] — the filters the Export button consumes (and where to set the period).
- [[orders-invoices-download]] — sibling PDF-bundle Download.
- [[orders-export]] — orders export (different action, broader scope; shared 2FA modal).
- [[orders-invoice]] — per-order single invoice PDF.
- [[orders-credit]] — credit-note flow (referenced in the credit-note column).
- [[settings-invoicing]] — invoice numbering, template, store-wide invoicing toggle.
- [[settings-staff]] — the invoices permission grant.
- [[settings-queue-view]] — async job status for large exports.
- [[invoice]] — entity page (the exported records).

## Open questions

(none — column set verified against the current exporter (12 columns, English-only headers, one row per line item); the Export entry point is the header button forwarding the list filter query; async threshold 10 / chunk 500 confirmed; credit-note rows appended with negative amounts.)
