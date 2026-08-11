---
type: feature
nav_path: "Orders → Order details → Invoice → Action surfaces"
route_name: admin.orders.generate.invoice
route_path: /admin/orders/generate-invoice/:order_id
aliases: ["Invoice action surfaces", "Create invoice button", "Manual invoice number dialog", "View invoice link", "Издаване на фактура — бутони"]
tags: [orders, invoice, invoicing, ui, smarty]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
> Part of [[orders-invoice]]. See the hub for the other aspects (numbering, eligibility, rendering, customer email).

# Invoice — action surfaces (per order)

## Purpose

Catalogues the **four distinct UI entry-points** the invoice feature wires into [[orders-details]]. Each opens a different interaction depending on the invoicing mode and the order's current state. Understanding which surface a merchant is looking at is the first step in answering most "how do I create / view an invoice" tickets.

## Where to find it

All four surfaces live on the [[orders-details]] page — three in the order's Action panel (the right-hand list of order actions) and one in the order header toolbar.

Routes involved:
- `/admin/orders/generate-invoice/{order_id}` (route name `admin.orders.generate.invoice`) — GET opens the manual-number dialog, POST saves.
- `/admin/orders/invoice/{order_id}` — the View-invoice PDF link.

## What the merchant can do here

### Surface A — "Create invoice" button (when `invoice_generate = 2` AND no invoice yet)

Shown in the order's Action panel as a row labelled "Invoice" (`order.invoice_line`). Behaviour differs by `invoice_number_type` (see [[orders-invoice-single-numbering]] for the modes):

| `invoice_number_type` | Button behaviour |
|-----------------------|------------------|
| `1` (auto-sequential) | Direct AJAX POST to `admin.orders.generate.invoice` — the platform picks the next number and saves. No dialog. |
| `2` (manual) | Opens a SMALL modal — see Surface B. |
| `3` (external app — Szamlazz / SmartBill / FGO / etc.) | Direct AJAX POST — platform calls the external app, expects a number+date back. No dialog. |

The button is shown only when the order's `allow_invoicing` is true AND the `generate_order` flag is set (the order is in an invoiceable state per the gates on [[orders-invoice-single-eligibility]]).

### Surface B — Manual invoice number dialog (`invoice/manual_number.tpl`) — verified template

A SMALL modal (`data-modal-size="small"`) with ONE input + the standard modal footer (Save / Cancel):

| Field | Element | Default | Notes |
|-------|---------|---------|-------|
| **Invoice number** | Text input (id `invoice_number`, `data-autofocus`) | empty | Free-text. Validated only in mode 2: required + numeric + unique across the `orders` table. Errors: "Invoice number must be unique", "Invoice number must be numeric", "Invoice number is required". |

Submission posts to `admin.orders.generate.invoice` (the form action). On success, fires `cc.ajax.reload` on `.order-summary`. The platform also queues a send-invoice email to the customer — see [[orders-invoice-single-customer-email]] for the gating.

### Surface C — "View invoice" PDF link (when number already exists)

In the order header toolbar — a direct link to `/admin/orders/invoice/<order_id>` opening the PDF inline (`output=I`, default). The link is hidden when:

- No invoicing provider active per [[settings-invoicing]] (`allow_invoicing` is false).
- No `raw_invoice_number` on the order yet.
- Plan-feature `invoices` gate not satisfied (see [[orders-invoice-single-eligibility]]).

### Surface D — External-app per-app surfaces (SmartBill, Profics, FGO, Szamlazz, etc.)

When external invoicing apps are installed AND active, each adds its OWN action row to the order-actions panel (separate from the platform Surface A). Each row exposes:

- A "Create document" button → POSTs to the app's `apps.<key>.send-order` endpoint.
- If the app already issued a number for this order: shows the document number as a link to the external system (e.g., SmartBill document URL) + a red "Cancel document" button.

These app rows operate in parallel with platform invoicing — a single order can have BOTH a platform invoice number AND an external SmartBill / Profics document. They don't conflict because each tracks its own number in order meta (`smart_bill_invoice_number`, `profics_invoice_id`, `fgo_document_number`, etc.). See [[apps-szamlazz-orders-invoice]] for the Szamlazz instance of this surface.

### What the merchant CANNOT do here

- Edit the invoice content — that comes from the order; edit the order on [[orders-details]] first.
- Open Surface A when an external app drives the number — see Business rules below.

## Settings & fields

The surfaces are driven by two settings on [[settings-invoicing]]: `invoice_generate` (controls whether Surface A appears at all) and `invoice_number_type` (controls Surface A's click behaviour). Both are explained on [[orders-invoice-single-numbering]].

## Business rules

- **Platform Surface A is hidden when `invoice_number_type = 3`** — the external app drives the number, so the platform's own Create-invoice button is suppressed; other modes leave it visible alongside the per-app rows (Surface D).
- **Surface C requires an existing number** — the View-invoice link only renders once `raw_invoice_number` is set, an active provider exists, and the `invoices` plan gate is satisfied.
- **Surface B validation runs only in mode 2** — modes 1 and 3 don't show the dialog, so the numeric/unique validation doesn't apply to them.

## Related

- [[orders-invoice]] — hub.
- [[orders-details]] — parent page hosting all four surfaces.
- [[settings-invoicing]] — `invoice_generate` + `invoice_number_type` configuration.
- [[apps-szamlazz-orders-invoice]] — Szamlazz external-app surface (an instance of Surface D).
- [[apps]] — external invoicing apps catalogue.

## Open questions

None.
