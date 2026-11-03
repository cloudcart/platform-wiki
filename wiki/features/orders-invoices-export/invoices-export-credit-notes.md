---
type: feature
nav_path: "Invoices → Export → Credit-note rows"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_invoices
aliases: ["Invoice export credit notes", "Credit-note rows in CSV", "Negative credit rows", "Кредитни известия в експорта", "Credit note CSV export"]
tags: [orders, invoices, export, csv, credit-note, accounting]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices-export]]. See the hub for the other aspects (trigger & delivery, column schema, async processing).

# Invoices export — credit-note rows

## Purpose

Explains how **credit notes appear in the invoice CSV export**: how credit-note rows are appended after the invoice rows, which columns identify them (`invoice_number` + `credit_number` both set), why the `amount` and `price` columns are emitted as NEGATIVE numbers, and how the accountant matches a credit back to its invoice.

## Where to find it

Credit-note rows are produced automatically by the **Export** header button on [[orders-invoices]] whenever an invoiced order in the exported scope also has a credit note. See [[invoices-export-trigger]] to launch the export and [[invoices-export-columns]] for the full 12-column schema.

## What the merchant can do here

- Reconcile a credit note against its original invoice in the accounting tool by matching on `invoice_number`.
- Sum the `price` / `amount` columns to see the cancelled order net to zero (invoice positive + credit negative).

What the merchant CANNOT do:

- Export credit notes on their own — they are always appended to the parent invoice's rows.
- Suppress the negative-number sign on credit rows — it is fixed.

## Settings & fields

There are no extra fields for credit rows — they use the same fixed 12-column schema as invoice rows (see [[invoices-export-columns]]). The difference is only in WHICH columns are populated and the SIGN of the money columns:

| Column | Invoice row | Credit-note row |
|--------|-------------|-----------------|
| `invoice_number` | set | set (same number as the invoice) |
| `credit_number` | empty | set |
| `amount` | positive money | NEGATIVE money (× -1) |
| `price` | positive money | NEGATIVE money (× -1) |
| `date` | invoice issue date | credit-note date |

## Business rules

### Credit-note rows are appended after invoice rows

When the order has a credit note, the CSV emits BOTH the invoice's line items AND a separate set of rows for the credit. Invoice rows have `invoice_number` set and `credit_number` empty; credit rows have BOTH `invoice_number` AND `credit_number` set. The merchant matches them in their accounting tool by `invoice_number`.

### Credit-note rows carry NEGATIVE amounts

The credit-note rows have their `amount` and `price` columns EMITTED AS NEGATIVE NUMBERS (multiplied by -1). This is critical for accounting tools that expect a credit-note to reverse the invoice with negative numbers — the accountant sees a clear `+100` invoice line followed by a `-100` credit line, summing to zero for the cancelled order.

Merchants importing into a tool that does NOT expect negative credit rows will see inflated "absolute value" totals if they sum the column naively. The fix is to handle the sign in the import mapping, not to strip it from the export (the sign cannot be turned off from the UI).

### Refunded invoices ARE included

There is no separate "refunded invoices" toggle — when an invoiced order has been credited, its credit rows are simply appended to the export alongside the invoice rows. So a CSV covering a date range with refunds inside it will contain both the original invoice rows and the offsetting credit rows.

## Related

- [[orders-invoices-export]] — hub.
- [[orders-invoices]] — parent invoices list.
- [[invoices-export-columns]] — the fixed 12-column schema these rows reuse.
- [[orders-credit]] — the credit-note flow that produces these rows.
- [[invoice]] — entity page (the exported records).

## Open questions

(none — credit-note rows verified: appended after invoice rows, both numbers set, negative `amount`/`price`.)
