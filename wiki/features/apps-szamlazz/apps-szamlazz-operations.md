---
type: feature
nav_path: "Apps → Szamlazz → (document mechanics)"
route_name: apps.szamlazz.overview
route_path: /admin/apps/szamlazz
aliases: ["Szamlazz documents", "Szamlazz invoice meta", "Szamlazz cancellation", "Szamlazz credit note logic", "Szamlazz pay invoice", "Szamlazz PDF download"]
tags: [apps, erp, invoicing, hungary, accounting]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-szamlazz]]. See the hub for the other aspects (settings, per-order invoice / credit-note / receipt flows, automation, localization).

# Szamlazz — document mechanics

## Purpose

This aspect documents **what happens to an order when Szamlazz issues, cancels, or marks-paid a document** — the three document types, the per-document data stored on the order, how PDFs are downloaded, the cancellation → credit-note branching that the `credit_note.active` setting controls, the pay-invoice flow, and how errors surface. It is the "what gets recorded and why" layer behind the per-order tabs ([[apps-szamlazz-orders-invoice]] / -credit-note / -receipt).

## Where to find it

The effects described here are triggered from each order's Szamlazz tabs (Sidebar → **Orders** → open an order → invoice / credit-note / receipt actions) and from automation (see [[apps-szamlazz-automation]]). There is no separate screen for the mechanics themselves — they are the behaviour behind the buttons.

## What the merchant can do here

- Issue any of three documents per order: **receipt** (nyugta), **invoice** (számla), **credit note** (jóváírás / storno).
- Download the cached PDF of any issued document from the order.
- Cancel an issued invoice or receipt; the result depends on `credit_note.active` (below).
- Mark an issued invoice as **paid** in Szamlazz (useful when bank-transfer payment is reconciled after the invoice was already issued).
- See the error message and retry when an operation fails.

## Settings & fields

### The three document types

Szamlazz works with exactly three document types. Each one stores its own block of data on the order:

- **receipt** — `szamlazz_receipt_*`
- **invoice** — `szamlazz_invoice_*`
- **credit note** — `szamlazz_credit_note_*`

### Per-document order fields

When Szamlazz issues a document, the platform records the following on the order (where `<type>` is `invoice`, `credit_note`, or `receipt`):

| Field | Content |
|----------|---------|
| `szamlazz_<type>_id` | Szamlazz's internal document ID. |
| `szamlazz_<type>_number` | The legal document number (e.g., `INV-2026-1234`). This is what populates the order's `invoice_number`. |
| `szamlazz_<type>_pdf` | Base64-encoded PDF content. |
| `szamlazz_<type>_date` | Issue date. |
| `szamlazz_<type>_paid` | (Invoice only) `1` once the invoice is marked paid in Szamlazz. |
| `szamlazz_<type>_error` | Error message, set when issuance fails. |
| `szamlazz_<type>_pdf_cancel` | (After cancellation) base64 PDF of the cancellation document. |

### PDF download

PDFs are cached on the order as base64 strings, so download is instant — no fresh API call to Szamlazz is needed. The trade-off is that order records become larger.

## Business rules

### Cancellation creates a credit note — when `credit_note.active = 1`

When the merchant cancels an invoice, the result branches on the store setting `credit_note.active`:

**`credit_note.active = 1` (the legally-correct setting for Hungary):**
- Szamlazz cancels the invoice and returns a **credit note** referencing the original.
- The order gains `szamlazz_credit_note_id`, `szamlazz_credit_note_number`, `szamlazz_credit_note_pdf`, and `szamlazz_credit_note_date`, plus `szamlazz_invoice_cancelled = true`.
- The **original invoice data stays** on the order (number / PDF / date). The credit note is added alongside it — a proper storno + credit-note chain.

**`credit_note.active = 0`:**
- The original invoice data is fully **removed** from the order (`szamlazz_invoice_id`, `_number`, `_pdf`, `_paid`, `_date`, `_error`).
- No credit-note record is created.
- Customer-visible: the order looks like it never had an invoice.

So `credit_note.active` is the single toggle deciding between a formal storno + credit-note chain and a silent invoice removal. For Hungarian tax compliance, keep it at `1`. The original document always remains in Szamlazz's permanent audit regardless of this setting — only the **CloudCart-side record** is what gets removed in the `0` case.

### Pay-invoice flow

Marking an invoice paid updates its status to PAID on the Szamlazz side and sets `szamlazz_invoice_paid = 1` on the order. This is used when payment lands after issuance (e.g., a bank transfer received later). It can be triggered manually from [[apps-szamlazz-orders-invoice]] or automatically on status change — see [[apps-szamlazz-automation]].

### Error handling

Every operation is wrapped so that a failure stores the exception message in `szamlazz_<type>_error` on the order, and the order keeps its non-invoice state. The merchant sees this message in the Response column of the relevant per-order tab. Re-running the operation clears the stored `_error` first, then retries — so a transient Szamlazz / network failure is recoverable by simply clicking again.

## Related

- [[apps-szamlazz]] — hub.
- [[apps-szamlazz-orders-invoice]] — the per-order invoice tab that triggers issue / cancel / pay.
- [[apps-szamlazz-orders-credit-note]] — the per-order credit-note tab.
- [[apps-szamlazz-orders-receipt]] — the per-order receipt tab.
- [[orders-credit]] — generic credit-note flow.
- [[order]] — entity page; the order is where these fields live.

## Open questions

(none — resolved against backend)
