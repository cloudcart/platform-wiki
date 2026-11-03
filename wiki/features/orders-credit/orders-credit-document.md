---
type: feature
nav_path: "Orders → Order details → Credit note → Document"
route_name: admin.order.credit.action
route_path: /admin/orders/credit/action/:order_id
aliases: ["Credit note PDF", "Credit note document", "Credit note template", "credit_body", "Credit note styling", "Credit note filename"]
tags: [orders, credit-note, refund, pdf, invoicing, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Credit note — the PDF document

> Part of [[orders-credit]]. See the hub for the other aspects (actions, eligibility, numbering, send quirks).

## Purpose

The rendered credit-note **PDF** — its template, layout, watermark, protection, custom-override hook, and download filename. This is the section to cite when a merchant asks "can I change how the credit note looks?", "why does it say Original?", or "what file do I get when I download it?". The action that triggers download/send is on [[orders-credit-actions]].

## Where to find it

The PDF is produced when the merchant clicks **Download** or **Send** in the View credit note dropdown on [[orders-details]] (see [[orders-credit-actions]]). The template that renders it is configured under [[settings-invoicing]] (see [[settings-invoicing-credit-note]]). There is no separate preview screen.

## What the merchant can do here

- Download the PDF (served `content-type: application/pdf`, opens in a new tab).
- Customise the template body via [[settings-invoicing]] `credit_body`.
- Get a date-stamped file when downloading in output mode.

## Settings & fields

### Credit-note template (Smarty PDF)

Rendered as a Smarty PDF. The sub-template includes:

- Payment lines / refund lines.
- Line items being credited.
- Credit totals block.
- VAT-exemption reason text (same as the invoice template).

### Custom template via `credit_body`

When [[settings-invoicing]] has `credit_body` populated, the platform renders the merchant's custom HTML template (variables resolved through the platform's OrderPrint helper). When empty, the standard credit-note Smarty template renders. See [[settings-invoicing-credit-note]].

### Download filename — prefers `credit_date`

When the PDF is downloaded as a file (output mode), the filename is `order_<order_id>_credit_<YYYY-MM-DD>.pdf`. The date prefers the credit issuance date (`credit_date`); if that's somehow null it falls back to the original invoice date.

## Business rules

### A4 layout, same as the invoice

The credit-note PDF format matches the invoice: A4 portrait, 20 mm margins. The credit note and its matching invoice are visually identical side-by-side — only the title (*"Credit note <number>"* vs *"Invoice <number>"*) and the totals signs differ.

### Styling identical to the invoice template

The PDF uses the same Smarty styling conventions as the invoice: sans-serif, 10 pt, 0.1 mm borders, mPDF-compatible HTML+CSS. Merchants customising one should expect the other to follow the same conventions.

### Watermark always reads "Original"

The PDF is watermarked at 10 % opacity in Arial. On Bulgarian-locale orders the watermark always reads *"Original"* — there is no "voided" variant for credit notes, since by definition they are issued on already-cancelled orders.

### Print-only PDF protection (stricter than invoice)

PDF protection is print-only — no modify, no copy. This is stricter than the invoice's modify + print + copy protection.

### Content comes from the order, not an editor

Line items, totals, and reason text are taken verbatim from the order's stored state at issuance time (negative-sense in the rendered PDF). The merchant cannot edit the document content directly — to change figures they must adjust the order first (see [[orders-credit-numbering]]).

## Related

- [[orders-credit]] — hub.
- [[orders-credit-actions]] — the Download / Send actions that produce this PDF.
- [[settings-invoicing]] — `credit_body` + template configuration.
- [[settings-invoicing-credit-note]] — credit-note template settings.
- [[orders-invoice]] — the invoice PDF this matches in layout and styling.

## Open questions

- Whether non-Bulgarian locales change the watermark text from *"Original"* (verify).
