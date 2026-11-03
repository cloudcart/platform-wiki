---
type: feature
nav_path: "Apps → Szamlazz → Orders → Invoice"
route_name: apps.szamlazz.orders.invoice
route_path: /admin/apps/szamlazz/orders/invoice
aliases: ["Szamlazz Invoice", "Szamlazz Orders Invoice", "Invoice list (Szamlazz)"]
tags: [apps, administration, szamlazz, invoicing, invoice, hungary]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Szamlazz → Orders → Invoice

## Purpose

The **Orders → Invoice** view is the **per-document list of all INVOICES issued via Szamlazz** for the merchant's orders. Each row corresponds to an invoice Szamlazz generated. The merchant can:
- See the Szamlazz-assigned invoice number + date.
- Download the invoice PDF (stored locally, sourced from Szamlazz).
- Cancel a previously-issued invoice (creates a counter-document per Hungarian tax law).
- Trigger fresh issuance for an order missing an invoice.
- See the Szamlazz API response per invoice (success / error details).

The `:type` URL parameter is `invoice` (the route is shared with credit-note and receipt — `apps.szamlazz.orders.{type}` where type is one of receipt|invoice|credit_note).

For the full Szamlazz feature set, see [[apps-szamlazz]].

## Where to find it

Sidebar → Apps → Szamlazz → **Invoice tab** (one of three Orders sub-tabs). Route: `/admin/apps/szamlazz/orders/invoice`.

API endpoint: `GET /api/szamlazz/orders/invoice` (, type filter set to `invoice`).

## What the merchant can do here

### Documents data table

Per row (per `Table/` Vue components):

| Column | Source component |
|---|---|
| **Order ID** (`OrderId.vue`) | Link to [[orders-details]] for the source order. |
| **Date** (`DateFormated.vue`) | When the invoice was issued (Szamlazz issue date). |
| **Response** (`Response.vue`) | Szamlazz API response — success status / error message. |
| **Download PDF** (`DownloadPdf.vue`) | Download the invoice PDF file. |
| **Actions** (`Actions.vue`) | Re-issue, Cancel, View, Email customer. |

The table uses `app-name="szamlazz"` for state.

### Download PDF

The `DownloadPdf` action triggers `GET /api/szamlazz/pdf/{orderId}/invoice`. The PDF is sourced from Szamlazz (cached locally per [[apps-szamlazz]] on `order.meta` as `szamlazz_invoice_pdf` base64).

### Actions (per row)

Only TWO icon-buttons appear per row, with conditional visibility per row state:

| Action | Icon | Visibility condition | API call | Tooltip |
|---|---|---|---|---|
| **Send / Create document** | cloud-upload (`far fa-cloud-upload-alt`) | `!data.document_id` (no doc yet) OR `data.document_cancelled` (was cancelled) | `GET create-document/{order_id}/invoice` | "Creating a new document in Szamlazz" |
| **Cancel document** | times-circle (`far fa-times-circle`) | `data.document_id` AND NOT `data.document_cancelled` AND `documentType !== 'credit_note'` | `GET cancel-document/{order_id}/invoice` | "Cancel a document in Szamlazz" |

While either is loading, a small spinner replaces the icon. The row's `document_id` / `document_number` / `document_error` / `document_cancelled` update from the response (no full table reload). What issuance and cancellation actually record on the order is documented in [[apps-szamlazz-operations]].

### What the merchant CANNOT do here
- Edit an issued invoice — Hungarian tax law forbids edits. Only cancel + re-issue.
- Delete invoices — only Cancel (which creates a counter-document, not a deletion).
- Issue invoices manually here when a document already exists; the typical trigger is automatic on order status change (see [[apps-szamlazz-automation]]) or from the order details page.

## Settings & fields

Each row is backed by the order's `szamlazz_invoice_*` block — `_id`, `_number` (the legal invoice number, e.g. "INV-2026-00123"), `_date`, `_pdf` (cached base64), `_error`, and `_pdf_cancel` (the counter-document after cancellation). The full per-document field catalogue and the PDF-on-order storage pattern live in [[apps-szamlazz-operations]].

## Business rules

### Hungarian tax law: no edits

Once issued, invoices are immutable per Hungarian tax law. The only way to "change" an invoice is to **Cancel** the original (which creates a permanent counter-document, never a deletion) and **issue a fresh invoice** with the corrected data. Both documents are retained and reported to NAV. The cancel result branches on the `credit_note.active` setting — a storno + credit-note chain when `1`, a silent CloudCart-side removal when `0`; see [[apps-szamlazz-operations]].

### Side effects per row action

- **Send / Create**: new Szamlazz API call; assigns the legal invoice number; populates the `szamlazz_invoice_*` block.
- **Cancel**: storno counter-document created; both PDFs retained (when `credit_note.active = 1`).
- **Download PDF**: serves the cached base64 — no API call to Szamlazz.

Auto-issuance (typically on the "Paid" status) and auto pay / cancel on status change are configured per document type — see [[apps-szamlazz-automation]]. The merchant can also trigger issuance manually from [[orders-details]] → Invoice action.

### Permission
Standard apps permission scope.

## Related

- [[apps-szamlazz]] — Szamlazz hub.
- [[apps-szamlazz-orders-credit-note]] — sister credit-note list.
- [[apps-szamlazz-orders-receipt]] — sister receipt list.
- [[apps-szamlazz-settings]] — Szamlazz credentials + config.
- [[orders-invoice]] — generic invoice flow that delegates to Szamlazz when active.
- [[orders-details]] — source order page.
- [[settings-invoicing]] — invoicing-provider store-wide setting.

## How it works (verified against backend)

### What the issuance payload carries

When an invoice is issued for an order, the platform builds the Szamlazz payload from three parts: a **header** (prefix, comment, payment method, the order's currency, the configured language, issue date, fulfillment date if fulfilled, template, EU-VAT flag, optional extra logo, and paid status — `true` when the order is `paid` / `completed`); a **buyer** block (company-or-personal name, address, email, phone, plus a Hungarian `TaxNumber` or EU `TaxNumberEU` derived from the buyer's tax classification); and **items** — one row per order line plus extra rows for pre-applied discounts and non-VAT tax entries, each carrying `vat`, `vatAmount`, `netPrice`, `grossAmount`. On success the previous error / credit-note meta is cleared and the `szamlazz_invoice_*` block is written (`szamlazz_invoice_paid = 1` only when the order total is fully covered); on failure the message lands in `szamlazz_invoice_error`. The language, template, currency, and the buyer tax-classification rules are owned by [[apps-szamlazz-localization]]; what gets stored on the order is detailed in [[apps-szamlazz-operations]].

### Pay-invoice and cancellation

Marking an invoice paid (sets `szamlazz_invoice_paid = 1`) and cancelling it (the `credit_note.active` storno-vs-removal branch) are both handled by the document-mechanics layer — see [[apps-szamlazz-operations]]. Both can fire automatically on order status change ([[apps-szamlazz-automation]]).

### NAV reporting timing

NAV reporting (Hungary's Online Számla) happens on Szamlazz's side in real time, not in CloudCart. CloudCart only sees the local success/failure response — if NAV rejects an invoice after Szamlazz accepted it, the order still shows the invoice as issued, and the merchant must check NAV-side status in their Szamlazz portal.

### Customer email and reconciliation

The auto-send email is generated by Szamlazz (not CloudCart), in the configured `invoice.language`; the merchant edits that email template inside their Szamlazz portal. This list view has no bulk-cancel, bulk-resend, search-by-invoice-number, or CSV export — per-order operations only, filtered by order ID. For accounting reconciliation the merchant exports from the Szamlazz portal, which has full reporting.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
