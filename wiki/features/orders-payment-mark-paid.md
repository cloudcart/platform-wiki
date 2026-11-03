---
type: feature
nav_path: "Orders → Order details → Payment → Mark as paid"
route_name: admin.orders.payment.mark_paid
route_path: /admin/orders/action/payment/mark_paid/:payment_id
aliases: ["Mark as paid", "Mark order paid", "Manual payment confirmation", "Record offline payment", "Маркирай като платена", "Регистрирай плащане"]
tags: [orders, payment, manual-payment, offline, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---
# Mark as paid (offline payment confirmation)

## Purpose

The merchant's way to **manually record an offline payment** as completed — used when the customer has paid via a method the platform cannot automatically detect: cash-on-delivery received by the courier, a bank transfer that landed on the merchant's account, in-person cash, voucher, etc. The merchant inputs an optional **provider reference ID** (bank-transfer reference, COD receipt number, etc.) and clicks Save; the platform marks the payment completed and fires the standard post-payment hooks.

The button shows only for **offline-type payments** in **Pending** state (the order is awaiting bank transfer / COD confirmation). For online payments, the platform tracks status automatically via the gateway's webhooks — no manual mark-paid needed.

This page is the **hub** for the mark-as-paid flow. The form mechanics, the heavyweight post-paid cascade, the order-status auto-flip rules, the adjacent payment buttons, and the API/plan-gate position each live on a dedicated aspect page below — the Assistant should drill into the aspect that matches the merchant's question rather than read all five.

## Sub-pages (in this cluster)

The flow is split into 5 aspect pages. Drill into the one that matches the question.

- [[orders-mark-paid-form]] — when the button appears (offline + Pending/Requested), the two surfaces (primary button + cog-dropdown), the single-field modal (`provider_reference_id`), the Save flow, what the merchant CANNOT do, and the reference-ID storage / searchability / free-text rules.
- [[orders-mark-paid-pipeline]] — the heavyweight post-paid cascade fired on Save: stock decrement (especially on COD), invoice + receipt number generation, customer-income recalculation, `order.updated` webhook, history action 19, payment-date-set-to-NOW, audit capture, and the no-idempotency double-click caveat.
- [[orders-mark-paid-status-flip]] — order-status auto-flip is precedence-based (count of payments per state), NOT amount-based; split-payment flips the whole order paid; the `manual=1` flag skips auto-recalc; authorized-payment interaction; how to reverse a mark-as-paid.
- [[orders-mark-paid-adjacent-actions]] — the neighbouring buttons that share the payment row: **Sync payment** (non-offline pending) and **Payment lease** (credit-type / BNPL), provider exclusions, and multiple-payment-record handling via Change Provider.
- [[orders-mark-paid-api]] — JSON-API v2 is read-only for payments (no mutate endpoint exposes mark-paid); the action's plan-gate position (no per-action gate; only page-level `orders_amount` / `orders_revenue` / `users_traffic` gates apply).

## Where to find it

From [[orders-details]] → **Payment action row**, when the payment is **offline type** (bank transfer, COD, manual, voucher, etc.) AND in **Pending** status (or **Requested** status with a non-credit type). The button label is *"Mark as paid"* (`order.action.mark_as_paid`) and it opens a **modal** (not inline AJAX).

Route: `/admin/orders/action/payment/mark_paid/{payment_id}` — GET renders the form modal (`payment/complete-form.tpl`); POST marks the payment paid. The action appears in two surfaces (primary button + cog dropdown) — see [[orders-mark-paid-form]] for the full visibility matrix.

## What the merchant can do here

Open the single-field modal, optionally type a **provider reference ID**, and Save to mark the payment completed. The full form behaviour — including what the merchant cannot do (mark online payments, specify a partial amount, back-date, or bypass the modal) — is on [[orders-mark-paid-form]]. The cascade that Save triggers is on [[orders-mark-paid-pipeline]].

## Settings & fields

The modal carries exactly ONE field, `provider_reference_id` (optional, free-text). The action is visible when the payment provider's `type` matches `offline`. The offline payment-type taxonomy (`offline`, `cod`, `voucher`, plus app-supplied types) and the modal layout are documented on [[orders-mark-paid-form]].

## Business rules

Marking a payment paid is a **heavyweight** action — the platform treats it as if a gateway just confirmed the payment, running the full post-paid pipeline ([[orders-mark-paid-pipeline]]) and the precedence-based order-status auto-flip ([[orders-mark-paid-status-flip]]). The merchant should be confident the offline payment actually arrived before clicking Save. Standard orders permission scope applies — mark-paid does NOT require the `orders.refund` grant.

## Related

- [[orders-details]] — parent page (button in payment action row).
- [[orders-mark-paid-form]] — aspect: form + visibility + reference ID.
- [[orders-mark-paid-pipeline]] — aspect: post-paid cascade.
- [[orders-mark-paid-status-flip]] — aspect: order-status auto-flip rules.
- [[orders-mark-paid-adjacent-actions]] — aspect: Sync / Lease neighbouring buttons.
- [[orders-mark-paid-api]] — aspect: API position + plan gates.
- [[orders-payment-manual]] — sibling flow for switching the payment provider (NOT for marking as paid).
- [[orders-payment-refund]] — reverse of mark-as-paid (only for completed payments).
- [[orders-payment-capture]] — capture / cancel for Authorized payments.
- [[settings-payment-providers]] — offline payment provider list.
- [[settings-invoicing]] — auto-invoice generation triggered by paid status.
- [[settings-statuses]] — status taxonomy + notification config.
- [[settings-hooks]] — `order.updated` webhook.
- [[orders-history]] — mark-as-paid event appears here.
- [[api-order-payment]] — read-only JSON-API v2 resource.
- [[json-api-v2]] — API overview.
- [[order-processing-pipeline]] — payment-sync side-effects (status auto-recompute, stock decrement, invoice number).

## Open questions

None.
