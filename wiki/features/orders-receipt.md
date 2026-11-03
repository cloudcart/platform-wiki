---
type: feature
nav_path: "Orders → Order details → Receipt"
route_name: admin.orders.receipt
route_path: /admin/orders/receipt/:order_id
aliases: ["Receipt", "Receipt PDF", "Касова бележка", "Разписка", "Proof of payment", "Order receipt"]
tags: [orders, receipt, pdf, invoicing, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Receipt (per order)

## Purpose

The **receipt PDF generation flow** for an order — a "proof of payment" document, distinct from the formal tax invoice ([[orders-invoice]]). A receipt is a simpler document that confirms the customer paid; it is commonly given to customers as a quick reference, attached to packages, or printed for in-person collection. The invoice is the formal tax document with full legal information (company data, VAT breakdown).

Some merchants do not issue formal invoices for every order (e.g. B2C cash-on-delivery where the courier provides a delivery receipt) but DO want a printable receipt for the customer. Some merchants issue BOTH (receipt to the customer, invoice for accounting). A merchant can issue: receipt only (B2C cash flows), invoice only (B2B), or both (typical e-commerce).

The platform delegates receipt rendering to the active Invoicing provider (configured in [[settings-invoicing]] / an installed invoicing app). The whole receipt flow is gated on the **N18 Audit** app ([[apps-n18-audit]]) being installed — receipts are primarily for Bulgarian fiscal-compliance (Наредба № Н-18). Merchants in other countries typically rely on the invoice flow instead.

This page is the **hub** for the per-order receipt cluster. The detailed mechanics live in the four aspect pages below — drill into the one that matches the question rather than reading all of them.

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question.

- [[orders-receipt-surfaces]] — where the receipt link actually lives (Order-history entry only — NO toolbar button), the automatic customer-email on `paid`/`completed`, the absent "Send receipt" action, the unused legacy translation key.
- [[orders-receipt-eligibility]] — the gates that decide when a receipt exists: N18 Audit app installed, active provider, `isReadyForReceipt` mirroring invoice eligibility (paid/completed/fulfilled/digital-only), provider-gated 404.
- [[orders-receipt-numbering]] — the separate sequential receipt series, `max + 1` generation with retry-5 backoff, number permanence, auto-generation via order events (not a click), the `order_receipt_sent` history row (action code 48).
- [[orders-receipt-rendering]] — the small thermal-size (format `B`) PDF, print-only protection, order-locale language, order-currency amounts, download filename pattern, N18-controlled template, "Powered by" footer gating.

## Where to find it

**The receipt is NOT a top-level button on the order-details toolbar.** Unlike the Invoice and Credit-note actions, the merchant CANNOT click a *"View receipt"* button. The platform auto-generates the receipt number on the side, and the merchant opens the PDF in ONE place only: [[orders-details]] → **Order history** section → entry labelled *"Order receipt #&lt;number&gt;"* (`order.history.order_receipt_number`) → the number is a clickable link that opens the PDF in a new tab. Full surface map + the customer auto-email on [[orders-receipt-surfaces]].

Route: `/admin/orders/receipt/{order_id}/{output?}` where `output` is `I` (inline, default) or `D` (download). If the provider returns null for this order at click time, the route returns HTTP 404.

## What the merchant can do here

- **View / download / print** the receipt PDF — open the order on [[orders-details]] → **Order history** → click the *"Order receipt #&lt;number&gt;"* link (opens inline in a new tab); then view, save to disk, or print from the browser.

### What the merchant CANNOT do here

- Edit the receipt's content — it comes from the order data via the Invoicing provider.
- Choose a different receipt template — single template per Invoicing provider; layout is N18-controlled (see [[orders-receipt-rendering]]).
- Email the receipt on demand — there is no admin-side "Send receipt" button; emailing is automatic on the configured status change (see [[orders-receipt-surfaces]]).
- Issue a "credit-receipt" (refund document) — for that, use [[orders-credit]].
- Generate a receipt for an unpaid order — receipts are gated on payable/fulfilled state (see [[orders-receipt-eligibility]]).

## Settings & fields

### Output parameter

| Output | Behaviour |
|--------|-----------|
| **`I`** (default) | Inline — PDF opens in a new tab. |
| **`D`** | Download — PDF triggers a Save File dialog in the browser. |

The receipt layout (logo, totals, signature lines, QR code) is rendered by the active Invoicing provider's / N18 Audit app's template; the merchant cannot customise it from the admin UI. The receipt typically does NOT include the customer's full legal company info (that is the invoice's job). Note: the `print_body` setting on [[settings-invoicing]] is for the **Print Order** action, NOT for receipts — see [[orders-receipt-rendering]].

## Business rules

- **Receipt is conceptually distinct from invoice and credit note.** Receipt = proof of payment (customer-facing convenience, issued at payment time). Invoice = tax-compliant document with full company info + VAT breakdown. Credit note = reversal of an invoice (issued at refund time). See [[orders-invoice]] / [[orders-credit]].
- **Receipt generation requires the N18 Audit app installed** — without it the action is unavailable and the route returns 404. See [[orders-receipt-eligibility]].
- **Eligibility mirrors the invoice** — `isReadyForReceipt` delegates to the same predicate as the invoice flow; a receipt cannot exist for any order that would not yet qualify for an invoice. See [[orders-receipt-eligibility]].
- **The receipt number is its own sequential series**, permanent once assigned, generated automatically by order events (not a merchant click). See [[orders-receipt-numbering]].
- **One receipt per order** — it summarises the order's total payment(s); it does NOT produce a separate receipt per payment record.
- **Pure read action** — clicking the link does NOT email the customer and writes no [[orders-history]] entry; the only history row is the synthetic `order_receipt_sent` row written at first generation. The customer may already have received the receipt as an attachment to the standard `paid`/`completed` status email (per [[settings-statuses]]).

## Related

- [[orders-details]] — parent page (the receipt link lives in the Order history section).
- [[invoicing-and-accounting]] — the platform-wide invoice / receipt / credit-note concept.
- [[online-sales-without-cash-register]] — the fiscal-receipt concept (Наредба Н-18 alternative regime) behind receipt generation + the Annex 38 audit.
- [[orders-invoice]] — invoice flow (formal tax document, different from receipt).
- [[orders-credit]] — credit note (refund document).
- [[settings-invoicing]] — invoicing provider configuration.
- [[settings-statuses]] — customer-notification templates may auto-email a receipt.
- [[apps]] — external invoicing apps (Szamlazz / FGO / SmartBill / etc.) may handle receipts differently per their app.
- [[apps-szamlazz-orders-receipt]] — the Szamlazz external-invoicing receipt surface.
- [[apps-n18-audit]] — the Bulgarian fiscal-compliance app that gates receipt generation; aggregates fulfilled-order receipts into the monthly Annex 38 audit XML submitted to NAP.
- [[orders]] — parent list.
- [[order]] — entity page.
- **Regulation reference** — Наредба № Н-18/2006, Глава седма "г" (Алтернативен режим), Чл. 52о–52у; consolidated text on лекс.бг: https://lex.bg/laws/ldoc/2135540645. Focused local extract at [`wiki/resources/naredba-n18-alt-rezhim.txt`](../resources/naredba-n18-alt-rezhim.txt) (grep `^Чл\. 52о\.` for the receipt-document article; `^Приложение № 38` for the schema annex).
- **Audit XML schema** — [`wiki/resources/dec_audit.xsd`](../resources/dec_audit.xsd) (original Windows-1251), [`dec_audit.utf8.xsd`](../resources/dec_audit.utf8.xsd) (UTF-8 grep-friendly), [`dec_audit-sample.xml`](../resources/dec_audit-sample.xml) (minimal valid sample), [`dec_audit-schema-cheatsheet.md`](../resources/dec_audit-schema-cheatsheet.md) (per-element field reference with Bulgarian docs + value enums for `paym`, `r_paym`, `e_shop_type`).

## Open questions

None.
