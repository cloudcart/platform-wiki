---
type: feature
nav_path: "Apps → Szamlazz → Orders → Credit Note"
route_name: apps.szamlazz.orders.credit_note
route_path: /admin/apps/szamlazz/orders/credit_note
aliases: ["Szamlazz Credit Note", "Szamlazz Storno", "Szamlazz refund document"]
tags: [apps, administration, szamlazz, credit-note, refund, hungary]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Szamlazz → Orders → Credit Note

## Purpose

The **Orders → Credit Note** view is the **per-document list of all CREDIT NOTES** issued via Szamlazz. A credit note is a tax document that REVERSES (partially or fully) a previously-issued invoice — used for refunds, returns, or any scenario where the merchant needs to reduce the invoiced amount. In Hungarian: **jóváírás** / **számla módosítás** (credit memo / invoice modification).

Different from cancellation (which is a STORNO — full reversal). Credit notes can be partial (refund 1 of 3 items) and reference the original invoice.

The `:type` URL parameter is `credit_note` (route shared with invoice + receipt).

For the full Szamlazz feature set, see [[apps-szamlazz]].

## Where to find it

Sidebar → Apps → Szamlazz → **Credit Note tab**. Route: `/admin/apps/szamlazz/orders/credit_note`.

API: `GET /api/szamlazz/orders/credit_note` (route `apps.szamlazz.orders` with type=credit_note).

## What the merchant can do here

### Documents data table

Same `DocumentsList` Vue component as [[apps-szamlazz-orders-invoice]] — uniform UX across all three sub-tabs (Invoice / Credit Note / Receipt). The `:type` URL parameter filters the data.

Per row:

| Column | Notes |
|---|---|
| **Order ID** | Link to the source order. |
| **Date** | Credit note issue date. |
| **Response** | Szamlazz API response (success / error). |
| **Download PDF** | Get the credit note PDF. |
| **Actions** | Only **Send / Create** (cloud-upload icon) — Cancel is HIDDEN for credit-notes per `Actions.vue` guard (`documentType !== 'credit_note'`). |

### Download credit note PDF

`GET /api/szamlazz/pdf/{orderId}/credit_note` — fetches the cached PDF from `order.meta.szamlazz_credit_note_pdf`.

### Issue a new credit note

Typically triggered from [[orders-credit]] (per-order action) OR auto-triggered when an order is refunded via [[orders-payment-refund]] (if [[apps-szamlazz]] is the active invoicing provider). The `apps.szamlazz.createDocument` route handles issuance with `documentType=credit_note`.

### Cancel a credit note

If the merchant issued a credit note in error, `apps.szamlazz.cancelDocument` route creates a counter-document. Per Hungarian tax law, this preserves the audit trail.

### What the merchant CANNOT do here
- Issue a credit note for an order WITHOUT an existing invoice — credit notes always reference an original invoice.
- Edit a credit note's amount after issuance — must cancel + re-issue.
- Skip the original-invoice reference — Szamlazz validates the chain.

## Settings & fields

### Per-row data

| Field | Notes |
|---|---|
| **order_id** | Source order. |
| **szamlazz_credit_note_id** | Szamlazz's internal document ID. |
| **szamlazz_credit_note_number** | Legal credit-note number. |
| **szamlazz_credit_note_date** | Issue date. |
| **szamlazz_credit_note_pdf** | Base64 PDF content (cached). |
| **szamlazz_credit_note_error** | Error if issuance failed. |
| **referenced_invoice_id** | The original invoice this credit note references. |

## Business rules

### Credit note vs cancellation distinction

- **Cancellation (storno)**: FULL reversal of original. Original is voided; nothing remains payable.
- **Credit note**: PARTIAL reduction. Original stays valid; only the credited amount is reversed.

Use cases:
- Customer returns 1 of 3 items → credit note for that 1 item's amount.
- Defective product, full refund → cancellation of original invoice.
- Pricing adjustment after-the-fact → credit note for the difference.

### NAV reporting required

Credit notes are reported to Hungary's Online Számla system, same as invoices.

### Auto vs manual triggering

When the merchant initiates a refund via [[orders-payment-refund]], the platform CAN auto-trigger credit note issuance if [[apps-szamlazz]] is active. The merchant may also manually trigger from [[orders-credit]].

### Permission
Standard apps permission scope.

## Related

- [[apps-szamlazz]] — Szamlazz hub.
- [[apps-szamlazz-orders-invoice]] — invoice list.
- [[apps-szamlazz-orders-receipt]] — receipt list.
- [[apps-szamlazz-settings]] — credentials + config.
- [[orders-credit]] — generic credit-note flow.
- [[orders-payment-refund]] — refund flow that may trigger credit note issuance.

## How it works (verified against backend)

### Credit note is FULL reverse of invoice, NOT partial

Per [[apps-szamlazz]] `cancelInvoice` + the platform code: when the merchant cancels an invoice with `credit_note.active = 1`, the platform sends a `ReverseInvoice` request to Szamlazz referencing the original invoice number. Szamlazz responds with a counter-document — this is what CloudCart calls a "credit note".

**This is a STORNO (full reversal), not a partial credit note.** The implementation reverses the entire original invoice; there's no per-line-item or partial-amount credit. If the merchant needs partial credit:
1. Cancel the full invoice → credit note generated for the full amount.
2. Issue a NEW invoice for the corrected amount.

### Credit-note list is filtered by cancelled-invoice flag

The credit-note list shows ONLY orders where `szamlazz_invoice_id` exists AND `szamlazz_invoice_cancelled == 1`. The platform doesn't have a separate "create credit note" entry point — credit notes are an artefact of invoice cancellation, not a standalone document type.

### One credit note per invoice

Because credit notes are tied to invoice cancellation and the platform stores them with simple `szamlazz_credit_note_*` keys (no array), there's effectively ONE credit note per invoice. The flow:
1. Invoice issued → `szamlazz_invoice_*` meta populated.
2. Invoice cancelled → `szamlazz_credit_note_*` meta populated, `szamlazz_invoice_cancelled = true`.

Subsequent invoice operations on the same order would need to first re-issue an invoice (which clears the cancelled flag).

### Credit note currency = original invoice currency

The credit note is generated from the original invoice's data — same currency. No option to issue a credit note in a different currency than the original.

### NAV reporting on credit note

Szamlazz reports the credit note to NAV (Online Számla) in real time, same as the invoice. CloudCart only sees the local Szamlazz response — NAV-side status must be checked in the Szamlazz portal.

### Customer notification on credit note

When `auto_send_email` (the global Szamlazz setting) is enabled, Szamlazz emails the credit note PDF to the customer the same way it emails invoices — in the configured `invoice.language`. The merchant doesn't configure a separate credit-note email; it follows the invoice-email setting.

For partial refunds where the customer should NOT be notified by Szamlazz, the merchant disables `auto_send_email` and uses CloudCart's own refund notification ([[orders-payment-refund]]) for customer communication.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
