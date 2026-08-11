---
type: feature
nav_path: "Details → Billing → Invoice download"
route_name: billing-list
route_path: /admin/details/billing
aliases: ["Billing invoice download", "Download invoice PDF", "Transaction vs invoice", "Invoice link on billing", "Изтегляне на фактура"]
tags: [accountdetails, details, billing, transactions, invoice]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Billing — invoice download

> Part of [[details-billing]]. See the hub for related aspects (transaction list, statuses, retry schedule).

## Purpose

This aspect documents how the merchant gets the **invoice PDF** from the *Details → Billing* tab: the per-row *Download* button, the rule that decides when it appears, the fact that it serves the exact same PDF as the *Invoices* tab, and the important transaction-vs-invoice distinction (many transactions can point at one invoice). This answers *"how do I download my invoice / why is there no download button on this charge?"*.

## Where to find it

- **Details (sidebar) → Billing** tab — the **Invoice** column on each row, where an approved transaction shows a **Download** link.
- The same PDF is also reachable from the *Invoices* tab ([[customers-details-payments|Invoices]]) and from `/admin/details/invoices`.
- URL pattern of the billing tab: `/admin/details/billing`.

## What the merchant can do here

- **Download the invoice PDF** — the Download button on an approved transaction row opens the PDF in a new tab. The PDF is generated on-demand server-side from the merchant's invoicing details ([[billing-invoicing]]) and the transaction's line items.

## What the merchant cannot do here

- **Download a PDF for an unpaid / voided / failed transaction** — the Download button is hidden when `approved != 1`. For a failed renewal the invoice was never finalised, so no PDF exists; the merchant must wait for a successful retry before a download appears (see [[details-billing-retry-schedule]]).
- **Get a separate "invoice-for-billing" document** — there is no distinct billing-only invoice; the Download serves the same canonical invoice PDF as the Invoices tab.

## Settings & fields

| Element | Field | Notes |
|---------|-------|-------|
| Download link | `invoice_id` | Rendered only when `approved == 1` AND `invoice_id` is non-null |
| Target | (download route) | Opens `/admin/api/core/invoice/download/{invoice_id}` in a new tab |

## Business rules

### Invoice link logic

A row's `invoice_id` is non-null when the transaction was associated with an issued invoice — typically when `approved == 1`. The Download button checks this and links to the invoice download route. For failed transactions the invoice was never finalised, so no PDF exists and no Download link appears.

### Each row is a transaction, not an invoice

Multiple transactions can correspond to the **same** invoice — e.g. a failed charge then a successful retry against the same renewal. The merchant sees each attempt as its own row, with the invoice download appearing only on the row that succeeded. The *Invoices* tab shows the issued-invoices view (one entry per finalised invoice); this Billing tab shows the charge attempts.

### Invoice download = same PDF as the Invoices tab

The Download button opens exactly the PDF the merchant can also get from the *Invoices* tab. It is generated on-demand by the invoice-download route — there is no separate "invoice for billing" document. The PDF layout (recipient info, numbering, language) comes from the merchant's invoicing settings on [[billing-invoicing]].

## Related

- [[details-billing]] — hub.
- [[details-billing-transaction-list]] — the table where the Invoice column renders.
- [[details-billing-statuses]] — only *Paid* (`approved == 1`) rows expose the Download link.
- [[customers-details-payments|Invoices]] — the issued-invoices list (one entry per finalised invoice); this aspect serves the same PDF per charge attempt.
- [[billing-invoicing]] — the invoicing details (recipient / numbering / language) printed on each PDF.

## Open questions

(All resolved.)
