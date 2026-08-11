---
type: feature
nav_path: "Orders → Order details → Payment → Manual confirm + Change provider"
route_name: admin.orders.payment.manual
route_path: /admin/orders/action/payment/manual/:order_id
aliases: ["Manual confirm order", "Manual payment confirm", "Change payment provider", "Mokka confirm", "Klear confirm", "Ръчно потвърждение", "Смяна на доставчик за плащане"]
tags: [orders, payment, manual-confirm, mokka, klear, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 11
---
# Manual confirm + Change provider

## Purpose

Two related but distinct advanced operations on a single order's payment row:

1. **Manual confirm** — for orders paid via **BNPL providers** (Mokka, Klear) where the provider's flow requires a merchant-side confirmation step BEFORE the payment is finalised (typically when goods are ready to ship or have been signed off). The merchant supplies a **document number** (Mokka) or triggers a one-click capture (Klear); the platform calls the provider's API to commit the transaction. See [[orders-payment-manual-mokka]] and [[orders-payment-manual-klear]].

2. **Change provider** — swap the payment provider on an existing order. Used when the customer chose one provider at checkout but the merchant needs to switch (e.g., customer phoned to say "actually I'll pay by bank transfer instead of card"). Creates a NEW payment record with the new provider; existing taxes and dependent state get cleaned up. See [[orders-payment-manual-change-provider]].

These are advanced operations — typical orders don't need them. This page is the **hub** for the cluster; each flow's exact wire-calls, side-effects, and quirks live on a dedicated aspect page below — the Assistant should drill into the aspect that matches the merchant's question.

## Sub-pages (in this cluster)

- [[orders-payment-manual-mokka]] — Mokka manual confirm: the `document_number` modal, the `finish` API call, the CURRENT-total-not-original quirk, invoice-number pre-fill gating, and `mokka_confirm` row visibility.
- [[orders-payment-manual-klear]] — Klear manual confirm: the no-modal one-click capture, `provider_data->capture` tracking, the error-handling difference vs Mokka, and Klear row visibility.
- [[orders-payment-manual-change-provider]] — swap provider: dropdown gating + disable conditions, new payment record, destructive tax delete + recompute, shipping-side adjustment, offline-gateway re-init.
- [[orders-payment-manual-lease]] — the Payment Lease action for credit-type BNPL in `requested` status (distinct from manual confirm); which providers are excluded.
- [[orders-payment-manual-api-access]] — why both manual-confirm and change-provider are admin-panel-only; what the JSON-API v2 payment resource does and does NOT expose.

## Where to find it

### Manual confirm

Available from [[orders-details]] **only when** the order's payment provider is `mokka` OR `klear` AND the order's status is `completed` OR `paid` AND the confirmation hasn't yet happened. The button lives in a DEDICATED action row in the order-actions summary — separate from the standard Payment action buttons. The row shows the provider's logo + title text *"Confirm `<provider title>`"* and a blue **Confirm** button.

Route: `/admin/orders/action/payment/manual/{order_id}`:
- GET → opens the confirm modal (Mokka only).
- POST → confirms the payment via the provider's API.

The Mokka button opens a small modal containing the `document_number` form; the Klear button POSTs directly with no modal. See the respective aspect pages.

### Change provider

Available as a **dropdown select** in the Payment row of [[orders-details]] when the order's status is NOT in `[authorized, completed, paid, refunded]` AND fulfillment is NOT `fulfilled`. The merchant picks a new provider; the change applies immediately on selection. Route: `/admin/orders/action/payment/{order_id}` (POST with `payment_provider` field). Full gating in [[orders-payment-manual-change-provider]].

## What the merchant can do here

- **Confirm a Mokka BNPL order** by entering a dispatch / shipment document number — see [[orders-payment-manual-mokka]].
- **Confirm a Klear BNPL order** with one click (no form) — see [[orders-payment-manual-klear]].
- **Change the payment provider** on an editable order via the dropdown — see [[orders-payment-manual-change-provider]].
- **Lease (re-confirm) a credit-type BNPL order** still in `requested` status — see [[orders-payment-manual-lease]].

### What the merchant CANNOT do here

- Manual-confirm a non-Mokka / non-Klear order (returns *"This provider does not support manual confirm"*).
- Change provider once the order is `authorized`, `completed`, `paid`, `refunded`, OR fulfillment is `fulfilled` — the dropdown is disabled / not rendered.
- Manually confirm a Mokka order WITHOUT a document number (returns *"Document number is required"*).
- Roll back a manual confirm — once committed via the BNPL API, the merchant must use the provider's dashboard to reverse.
- Bulk-change the payment provider — strictly per-order (see [[orders-payment-manual-change-provider]]).

## Settings & fields

The cluster surfaces one editable field across all flows — the Mokka `document_number` (text, required for Mokka confirm). Everything else is gating, not configuration:

- **Manual-confirm supported providers** — Mokka (requires `document_number`) and Klear (no field) only. See [[orders-payment-manual-mokka]] / [[orders-payment-manual-klear]].
- **Change-provider dropdown filter** — limited to providers enabled via [[settings-payment-providers]]; the `tbi` provider is excluded; if `manual_order_payments` is set on [[settings-cart]], only whitelisted providers appear. See [[orders-payment-manual-change-provider]].

## Business rules

The full rule set is distributed across the aspect pages. The cross-cutting rules in one place:

- **BNPL is two-stage** — the customer applies at checkout (credit check), the merchant later confirms when shipping (funds captured). Manual confirm is the second stage.
- **Manual confirm fires order hooks** — after success the platform fires the order's hooks (like mark-as-paid): customer notification email, invoice generation if configured, webhooks.
- **Confirm is full-amount, all-or-nothing** — there is no UI to confirm only the shipped portion of a partially-shipped order.
- **No background retry on manual confirm** — a network failure leaves the order in pending-confirm; the merchant retries manually.
- **Change provider is destructive on taxes** — it deletes existing provider-scoped tax records and recomputes against the billing zone's payment-conditional taxes, which can change the order total. See [[orders-payment-manual-change-provider]].
- **Change provider creates a NEW payment record** — the old record stays attached for audit; multiple payment records per order is normal after a switch.
- **Permission** — standard orders write access; no specific manual-confirm grant.
- **Manual confirm + change provider are captured in [[orders-history]]** — including the acting admin's identity.

## Related

- [[orders-details]] — parent page hosting both flows.
- [[orders-payment-mark-paid]] — different flow for OFFLINE payment confirmation.
- [[orders-payment-refund]] — reverse a completed BNPL payment via the provider's refund API.
- [[orders-payment-capture]] — capture / cancel authorization (DIFFERENT from manual confirm — those are for card pre-auth).
- [[settings-payment-providers]] — Mokka / Klear / other provider configuration.
- [[settings-cart]] — `manual_order_payments` whitelist for change-provider restrictions.
- [[orders-history]] — manual confirm + change provider events appear here.
- [[orders-invoice]] — invoice's raw number is used as the Mokka document number default.
- [[api-order-payment]] — read-only JSON-API v2 resource.
- [[json-api-v2]] — API overview.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
