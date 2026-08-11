---
type: feature
nav_path: "Invoices → Export → Column schema"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_invoices
aliases: ["Invoices export columns", "Invoice CSV schema", "Invoice export fields", "Колони на експорта на фактури", "CSV схема фактури"]
tags: [orders, invoices, export, csv, accounting]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices-export]]. See the hub for the other aspects (trigger & delivery, credit-note rows, async processing).

# Invoices export — column schema

## Purpose

Documents the **fixed 12-column CSV schema** the invoice export produces: what each column shows, the one-row-per-line-item rule, the English-only (untranslated) headers, and the per-column edge cases (the three-source `name` fallback, the `eik = 999999999` placeholder, `mol`-only-when-a-company-exists, and currency = invoice currency).

## Where to find it

This is the schema produced by the **Export** header button on [[orders-invoices]]. See [[invoices-export-trigger]] for how the export is launched.

## What the merchant can do here

- Read the export into a spreadsheet / ERP / tax-filing tool, mapping columns by their English header keys.
- Match the fixed column set to the accountant's import template.

What the merchant CANNOT do:

- Pick alternative columns or reorder them — the schema is fixed and cannot be changed from the UI.
- Get translated headers — they are always raw English keys, regardless of admin UI language.

## Settings & fields

### Fixed column schema

The CSV uses a fixed 12-column set (verified). One row per ordered LINE ITEM (not per invoice) — a single invoice with N line items produces N rows. When the order has a credit-note, additional rows are appended — see [[invoices-export-credit-notes]].

| # | Column | What it shows |
|---|--------|---------------|
| 1 | `invoice_number` | The invoice number for this row. |
| 2 | `credit_number` | The credit-note number if this row belongs to a credit; empty otherwise. |
| 3 | `date` | Invoice issue date (or credit-note date for credit rows). |
| 4 | `name` | Company name (falls back to billing address full name, then customer full name). |
| 5 | `mol` | The MOL (materially responsible person) — only populated when a company name exists. |
| 6 | `eik` | The company VAT/EIK; defaults to `999999999` if none on file. |
| 7 | `city` | Billing-address city. |
| 8 | `currency` | Invoice currency code (BGN / EUR / etc.). |
| 9 | `amount` | Per-unit price (with VAT) of the line item, formatted as money. |
| 10 | `sku` | Product SKU. |
| 11 | `quantity` | Quantity of the line item. |
| 12 | `price` | Total (with VAT) of the line item — quantity × amount, formatted as money. |

The merchant cannot pick alternative columns from the UI. The headers are NOT translated — they're emitted as raw English keys (`invoice_number`, `credit_number`, etc.), regardless of admin UI language.

### Sort order — by `invoice_number` ASC

The CSV is sorted by invoice number ascending (matches the accounting convention of presenting invoices in series). This ordering is fixed and cannot be changed from the UI.

## Business rules

### One row per LINE ITEM, not per invoice

An invoice with 5 line items emits 5 rows in the CSV — each row contains the same invoice header (number, date, company, etc.) but a different SKU/quantity/amount. Counting rows in the CSV does NOT count invoices. To count distinct invoices, the merchant should sort by `invoice_number` and count unique values.

### `name` falls back through THREE sources

The `name` column reads from the billing address's company name first; if absent, falls back to the billing address's full personal name; if absent, falls back to the customer's full name on the order. So a B2C order with no billing company will show the customer's personal name where a B2B order would show the company.

### `eik` defaults to `999999999` when missing

The `eik` (Bulgarian company VAT/EIK number) column never emits blank. When the billing address has no company VAT on file, the export writes the placeholder `999999999`. This is a Bulgarian accounting convention — the accountant's software typically treats `999999999` as "no VAT registration" and processes it differently from a real EIK. Merchants in non-Bulgarian markets should be aware their export will contain this placeholder for personal orders.

### `mol` (responsible-person) — only populated when company exists

The `mol` column shows the responsible person's full name ONLY when the order's billing address has a company name on file. For personal orders (no company), this column is empty. The intent is that `mol` is the legal person responsible at the company's invoice — it has no meaning for an individual.

### Currency column = invoice currency, NOT store base currency

The `currency` column reflects the currency the order was placed in (BGN, EUR, USD, etc.) — captured at checkout time. For a multi-currency store, the export can contain different currency codes on different rows. The export does NOT convert all amounts to a single base currency; the merchant's accounting tool must handle multi-currency aggregation.

### Headers are English-only — deliberate

Unlike [[orders-export]] (which DOES localize headers based on admin UI language), the invoice export's headers are fixed in English so downstream accounting tools can match columns reliably regardless of the merchant's locale.

## Related

- [[orders-invoices-export]] — hub.
- [[orders-invoices]] — parent invoices list.
- [[invoices-export-credit-notes]] — the extra rows appended when an order has a credit note.
- [[orders-export]] — orders export; produces a DIFFERENT column set (and localizes its headers).
- [[orders-credit]] — credit-note flow (drives the `credit_number` column).
- [[invoice]] — entity page (the exported records).

## Open questions

(none — column set verified: 12 columns, English-only headers, one row per line item.)
