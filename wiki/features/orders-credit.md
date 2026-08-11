---
type: feature
nav_path: "Orders → Order details → Credit note"
route_name: admin.order.credit.action
route_path: /admin/orders/credit/action/:order_id
aliases: ["Credit note", "Credit memo", "Refund document", "Order credit note", "Кредитно известие"]
tags: [orders, credit-note, refund, pdf, invoicing, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 7
---
# Credit note (per order)

## Purpose

The **credit note generation, download, and customer-send flow** for a single order. A credit note is the tax-document counterpart to an invoice — issued when an order is refunded or cancelled, it formally documents the merchant's reversal of charges for accounting and tax compliance. Required by tax law in most jurisdictions whenever a sale is reversed.

The merchant works with credit notes entirely from the **View credit note** dropdown on [[orders-details]] — there is no separate screen. The dropdown exposes up to three actions: **Create**, **Download**, and **Send to customer**. This hub gives the overview; each aspect below covers one slice in depth.

## Where to find it

From [[orders-details]] → action toolbar → **View credit note** button (icon `fa-file-alt`). Clicking it toggles a small hover-style dropdown (`.credit-note-dropdown`) anchored below the button: white background, 1 px grey border, 5 px radius, min-width 185 px. The button + dropdown appear only when the order is eligible (provider-gated) or a credit note already exists — see [[orders-credit-eligibility]].

## What the merchant can do here

- **Create credit note** — issues the credit note via the active Invoicing provider, consuming the next credit-note number. See [[orders-credit-actions]].
- **Download credit note** — opens the rendered PDF in a new tab. See [[orders-credit-document]].
- **Send credit note** — emails the PDF to the customer through the notification pipeline. See [[orders-credit-actions]] + [[orders-credit-send-quirks]].

What the merchant CANNOT do here:

- Issue a credit note before the order is `cancelled` / `refunded` with an invoice already on it — see [[orders-credit-eligibility]].
- Edit the credit note's content (line items, totals, reason) — all of it comes from the order's current state.
- Issue a **partial-amount** credit note from this dropdown, or a second whole-order one — the order holds exactly one whole-order credit note. A partial credit note is issued on a **return** instead — see [[orders-credit-numbering]] and [[orders-returns-lifecycle]].

## Settings & fields

The credit-note flow has **no data-entry UI** — no amount field, no reason field, no date picker. Everything is filled from the order's current state at issuance:

- **Credit-note number** — from a separate sequential counter. See [[orders-credit-numbering]].
- **Credit-note date** — set to "now" (UTC) at issuance.
- **Line items + totals** — taken verbatim from the order (negative-sense in the PDF).
- **Reason / VAT-exemption text** — from [[settings-invoicing]] `credit_body` if customised, else the default template. See [[orders-credit-document]].

For a **partial refund** this flow is not the answer: it can only credit the whole order. The merchant issues a **return** for the affected lines and issues that return's own credit note — see [[orders-returns-lifecycle]] and [[orders-credit-numbering]].

## Business rules

- **Eligibility is provider-gated and strict** — the built-in provider requires `cancelled`/`refunded` status + an invoice number + invoicing enabled. See [[orders-credit-eligibility]].
- **One WHOLE-ORDER credit note per order** — the order carries a single `credit_number` / `credit_date`. Partial credit notes exist, but they live on the order's returns, not here. See [[orders-credit-numbering]].
- **Issuing a credit note locks the order's status** — a cancelled / refunded order that carries a credit note or a return can no longer be moved back to a normal status. See [[orders-credit-numbering]].
- **Send always emails, ignoring the order's `notify_customer` flag** — and has several UI quirks (always-green toast, silent no-op on ineligible orders). See [[orders-credit-send-quirks]].
- **Send issues-on-the-fly** — clicking Send with no credit note yet will create one first, then send. See [[orders-credit-actions]].
- **External invoicing apps** (Szamlazz, FGO, SmartBill, FlixFacts) own their own number assignment and storage; the platform stores a reference. See [[orders-credit-eligibility]] + [[apps-szamlazz-orders-credit-note]].

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages. Drill into the one that matches the question rather than reading all five.

- [[orders-credit-actions]] — the three dropdown actions (Create / Download / Send), button + dropdown UI, visibility-state matrix, no-modal inline AJAX flow, issue-and-send chain.
- [[orders-credit-eligibility]] — provider-gated eligibility; the strict `cancelled`/`refunded` + invoice-number + `allow_invoicing` gate; external-app integration.
- [[orders-credit-numbering]] — the separate credit-number series shared with partial returns; one whole-order `credit_number`/`credit_date`; permanence; the over-credit ceiling; the post-reversal status lock; the real partial-refund path.
- [[orders-credit-document]] — the credit-note PDF (A4, watermark, print-only protection); the `credit_body` custom template; download filename; styling parity with the invoice.
- [[orders-credit-send-quirks]] — Send bypasses `notify_customer`; always-success toast; silent no-op on ineligible orders; no rate-limit; async external-provider failures.

## Related

- [[invoicing-and-accounting]] — invoicing & accounting concept hub.
- [[orders-details]] — parent page (the dropdown lives here).
- [[orders-returns]] — returns; a **partial** return carries its own credit note instead of using this flow.
- [[orders-returns-lifecycle]] — the partial-credit-note path and the lock it puts on a later full reversal.
- [[orders-details-products]] — why an invoiced order can't simply be edited before crediting.
- [[orders-invoice]] — sister flow for the original invoice.
- [[settings-invoicing]] — invoice + credit-note template + numbering configuration.
- [[settings-invoicing-credit-note]] — credit-note template settings.
- [[apps-szamlazz-orders-credit-note]] — external-app credit-note flow (Szamlazz).
- [[orders-payment-refund]] — the money-movement side of a refund.
- [[orders-invoices-export]] — bulk export including credit notes.
- [[orders]] — parent list.
- [[order]] — entity page.
- [[credit-note]] — credit-note entity.
- [[settings-hooks]] — `order.updated` webhook fires when a credit note is issued (verify).

## Open questions

- Whether a merchant-facing "cancel credit note" button exists, or whether cancellation requires CloudCart support. See [[orders-credit-numbering]].
