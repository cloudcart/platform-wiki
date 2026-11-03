---
type: feature
nav_path: "Apps → Szamlazz → Orders → Receipt"
route_name: apps.szamlazz.orders.receipt
route_path: /admin/apps/szamlazz/orders/receipt
aliases: ["Szamlazz Receipt", "Szamlazz e-receipt", "Szamlazz nyugta"]
tags: [apps, administration, szamlazz, receipt, hungary]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Szamlazz → Orders → Receipt

## Purpose

The **Orders → Receipt** view is the **per-document list of all RECEIPTS** issued via Szamlazz. A **receipt** (Hungarian: **nyugta**) is a simpler tax document than an invoice — typically used for B2C cash / digital-payment confirmation without the full invoice's business-data requirements (no buyer company info needed).

Hungarian tax law differentiates between:
- **Invoice (számla)** — formal tax document requiring buyer's tax-identifiable info (typically for B2B or when the customer requests one).
- **Receipt (nyugta)** — simpler proof-of-purchase, sufficient for most B2C transactions.

The merchant typically issues receipts by default for B2C orders, with invoices on-request.

The `:type` URL parameter is `receipt` (route shared with invoice + credit_note).

For the full Szamlazz feature set, see [[apps-szamlazz]].

## Where to find it

Sidebar → Apps → Szamlazz → **Receipt tab**. Route: `/admin/apps/szamlazz/orders/receipt`.

API: `GET /api/szamlazz/orders/receipt` (route `apps.szamlazz.orders` with type=receipt).

## What the merchant can do here

### Documents data table

Same `DocumentsList` Vue as [[apps-szamlazz-orders-invoice]] / [[apps-szamlazz-orders-credit-note]] — uniform UX. The `:type=receipt` filter scopes the data.

Per row:

| Column | Notes |
|---|---|
| **Order ID** | Source order link. |
| **Date** | Receipt issue date. |
| **Response** | Szamlazz API response. |
| **Download PDF** | Get the receipt PDF. |
| **Actions** | Cloud-upload icon (Send / Create), Times-circle icon (Cancel) — per `Table/Actions.vue`. Only 2 icon buttons appear; visibility depends on row state (see Actions section). |

### Download receipt PDF

`GET /api/szamlazz/pdf/{orderId}/receipt` — fetches the cached PDF from `order.meta.szamlazz_receipt_pdf`.

### Issue / Cancel

Same routes as invoice/credit-note:
- `apps.szamlazz.createDocument` with `documentType=receipt`.
- `apps.szamlazz.cancelDocument` with `documentType=receipt`.

### What the merchant CANNOT do here
- Use a receipt as a tax-deductible invoice — B2B customers typically request the formal invoice instead.
- Have BOTH invoice AND receipt for the same order without explicit issuance (typically the merchant picks one).
- Edit issued receipts.

## Settings & fields

### Per-row data

| Field | Notes |
|---|---|
| **order_id** | Source order. |
| **szamlazz_receipt_id** | Szamlazz's internal ID. |
| **szamlazz_receipt_number** | Legal receipt number. |
| **szamlazz_receipt_date** | Issue date. |
| **szamlazz_receipt_pdf** | Base64 PDF (cached). |
| **szamlazz_receipt_error** | Error if issuance failed. |

## Business rules

### Receipt is simpler than invoice

Receipts:
- Don't require buyer's tax-identification (BULSTAT / company name).
- Are sufficient for B2C transactions where the customer is a private individual.
- Have their own numbering series (separate from invoices).

Invoices:
- Require full buyer + seller tax info.
- Required for B2B transactions where the buyer needs to deduct VAT.

### Receipt cancellation flow

Like invoices, cancelling a receipt creates a storno document. Both are preserved.

### Customer request triggers invoice

When a customer asks for an invoice instead of (or in addition to) a receipt, the merchant typically:
1. Cancels the receipt.
2. Issues an invoice with the customer's tax info.

OR:
1. Issues an invoice on top of the existing receipt (some Hungarian merchants do this; verify legal acceptability).

### NAV reporting

Receipts are also reported to NAV's Online Számla. The threshold for NAV reporting differs (small-value receipts may have simpler reporting requirements — verify current rules).

### Permission
Standard apps permission scope.

## Related

- [[apps-szamlazz]] — Szamlazz hub.
- [[apps-szamlazz-orders-invoice]] — invoice list.
- [[apps-szamlazz-orders-credit-note]] — credit note list.
- [[apps-szamlazz-settings]] — credentials + config.
- [[orders-receipt]] — generic receipt flow.

## How it works (verified against backend)

### Receipt vs invoice — both can be active simultaneously

Per [[apps-szamlazz-settings]] and the platform code: the merchant configures `receipt.active` and `invoice.active` INDEPENDENTLY. Both can be `1` at the same time, meaning a single order can trigger BOTH a receipt AND an invoice (if both have `generate = 'auto'` and the order's status is in both `generate_status` lists).

The merchant typically sets:
- For pure B2C stores: `receipt.active = 1`, `invoice.active = 0` (or only on-request).
- For mixed B2B/B2C: both active, with each triggered by different statuses.
- Or: `invoice.active = 1` only (typical for B2B-only stores) — receipts are skipped entirely.

There's NO storefront customer-request flow for "I need an invoice instead" — the merchant decides which document types are issued based on order status, not customer choice.

### Cancel-Receipt removes the receipt data entirely

When the merchant cancels a receipt, the platform calls Szamlazz's `reverse receipt` endpoint and then REMOVES the receipt meta from the order entirely (`szamlazz_receipt_id`, `_pdf`, `_number`, `_date`, `_error`).

This differs from invoice cancellation where `credit_note.active = 1` PRESERVES the original. Receipt cancellation in this integration is a clean delete from CloudCart's side — Szamlazz retains the cancelled receipt + counter-document in its audit history per Hungarian law, but CloudCart's order looks like it never had a receipt.

There's currently NO automatic credit-note generation for receipt cancellation — capturing the cancellation document's id/pdf is planned but not enabled.

### Receipt formatter — same structure as invoice but simpler header

The receipt format is:
- Header: payment method, currency (order's), prefix (from `receipt.prefix` setting), comment (from `receipt.comment` setting). NO language field, NO buyer block (receipts in Szamlazz don't carry buyer tax info).
- Items: same logic as invoice — one row per product + discount rows + tax rows.

### Receipt language

Receipts use Szamlazz's default language (Hungarian) — there's NO `receipt.language` setting in the configuration. The merchant cannot localize receipts. Customer's language is irrelevant.

### Auto-trigger event flow for receipts

The receipt fires on order-created and order-status-change events when:
- `receipt.active = 1` AND `receipt.generate = 'auto'`.
- Current order status is in `receipt.generate_status` (merchant-configured list).
- For status-change, the order doesn't already have a `szamlazz_receipt_id`.

The auto-cancel flow: when status becomes `refunded` or `cancelled` AND order has a receipt → auto-cancel.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
