---
type: feature
nav_path: "Orders → Order details → Receipt → Surfaces"
route_name: admin.orders.receipt
route_path: /admin/orders/receipt/:order_id
aliases: ["Receipt surfaces", "Where is the receipt", "View receipt link", "Order receipt history entry", "Send receipt", "Receipt email attachment"]
tags: [orders, receipt, surfaces, history, notifications]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-receipt]]. See the hub for the other aspects (eligibility, numbering, rendering).

# Receipt — surfaces (per order)

## Purpose

Explains **where the receipt actually appears** for the merchant and the customer — and, just as importantly, where it does NOT. This is the aspect to read for any *"where do I find / print / send the receipt"* ticket. The headline rule: unlike the Invoice and Credit-note actions, the receipt has **no toolbar button**; it surfaces in exactly one place in the admin UI, plus one automatic customer-facing path.

## Where to find it

[[orders-details]] → **Order history** section → entry labelled *"Order receipt #&lt;number&gt;"* (`order.history.order_receipt_number`) → the number renders as a clickable link (the only clickable element in that history row, `target="_blank"`) that opens the receipt PDF in a new tab.

Route behind the link: `/admin/orders/receipt/{order_id}/{output?}` where `output` is `I` (inline, default) or `D` (download).

The history entry (and therefore the link) only appears when an Invoicing provider is active, the N18 Audit app is installed (the platform code), and the order reached a payable / fulfilled state that triggered auto-generation of the receipt number — see [[orders-receipt-eligibility]] for the full gate set and [[orders-receipt-numbering]] for the `order_receipt_sent` history row that creates this link.

## What the merchant can do here

- Open the order on [[orders-details]] → scroll to **Order history** → click the *"Order receipt #&lt;number&gt;"* number.
- The PDF opens in a new tab (inline output): view in the browser, save to disk via the browser's PDF save action, or print directly.

### Customer also receives it automatically

Per the `paid` / `completed` status-change notification template ([[settings-statuses]]), customers may receive the receipt PDF as an **attachment** to their status-change email. The merchant does NOT trigger this — it is automatic when the order reaches the configured trigger status AND the merchant's email template for that status includes the receipt attachment.

### No "Send receipt to customer" action surface

The merchant has NO admin-side button to email the receipt on demand. Receipt emailing happens ONLY as part of the standard customer-notification flow on the `paid` / `completed` status change (above). The N18 Audit app's translation key the platform code (*"Generate and send receipt"*) is currently UNUSED in the admin UI — a legacy string from a feature that never shipped a merchant-facing button.

## Settings & fields

| Output | Behaviour |
|--------|-----------|
| **`I`** (default) | Inline — PDF opens in a new tab. |
| **`D`** | Download — PDF triggers a Save File dialog. |

There is no per-order setting that controls whether the receipt link appears — it is driven entirely by app installation + order state. The customer-attachment behaviour is governed by the relevant status template on [[settings-statuses]], not by any field on the receipt itself.

## Business rules

- **One surface in admin** — the Order-history link is the sole admin entry point. There is intentionally no header-toolbar button (contrast [[orders-invoice]] / [[orders-credit]], which both have toolbar actions).
- **Clicking the link is a pure read** — it does NOT email the customer and writes no new [[orders-history]] row. The only history row associated with the receipt is the synthetic `order_receipt_sent` row written once, at first generation (see [[orders-receipt-numbering]]).
- **Customer-email is decoupled from the merchant click** — the customer's copy arrives (if configured) as the status-change email attachment, which may have fired long before the merchant ever opens the link.
- **Provider-gated link** — if the active provider returns null for this order at click time, the route returns HTTP 404; see [[orders-receipt-eligibility]].

## Related

- [[orders-receipt]] — hub.
- [[orders-details]] — parent page; the Order history section hosts the link.
- [[orders-history]] — the history feed where the `order_receipt_sent` row renders.
- [[settings-statuses]] — status-change templates that may attach the receipt to the customer email.
- [[apps-n18-audit]] — gates whether the history entry appears at all.

## Open questions

None.
