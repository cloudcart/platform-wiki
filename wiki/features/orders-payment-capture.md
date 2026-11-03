---
type: feature
nav_path: "Orders → Order details → Payment → Capture / Cancel authorization"
route_name: admin.orders.payment.capture
route_path: /admin/orders/action/payment/capture-authorization/:payment_id
aliases: ["Capture authorization", "Capture payment", "Cancel authorization", "Capture funds", "Pre-auth capture", "Captura na razreshenie", "Захващане на плащане"]
tags: [orders, payment, capture, authorization, smarty]
plan_gates: ["authorize_payment"]
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---

# Payment capture & cancel authorization

## Purpose

Two **complementary actions** on payments in the **Authorized** state (pre-auth hold). When the customer's card has been authorised — the funds are reserved but not yet charged — the merchant has two next steps:

- **Capture authorization** — commit the charge. The funds move from "held" to "captured" on the gateway side; the customer's card statement shows the charge. The payment status flips from Authorized to Completed.
- **Cancel authorization** — release the hold without charging. The funds return to the customer's available balance (typically within a few business days on the gateway side). The payment status flips from Authorized to Cancelled / Voided.

This is the standard **two-phase payment flow** used by card gateways that support delayed capture. The merchant uses it to verify the customer / inventory before committing the charge — e.g. for pre-orders, custom-made products, risk-flagged orders, or **variable-weight goods** (groceries, deli, meat / fish sold by weight) where the picked quantity differs from what was ordered: authorize the full amount at checkout, then **edit the order to the actual picked amount and capture the lower total** — avoiding a small refund (often paired with [[apps-pick-and-pack]] at picking time). Once captured, the only way to reverse is a Refund (see [[orders-payment-refund]]).

This page is the **hub** for the capture / cancel flow. Each visibility rule, each provider, each side-effect cascade, and each automatic trigger lives on a dedicated aspect page below — the Assistant should drill into the aspect that matches the merchant's question, not read every page.

## Sub-pages (in this cluster)

The capture / cancel flow is split into 6 aspect pages. Drill into the one that matches the question.

- [[orders-payment-capture-buttons]] — the two button surfaces (primary action row + cog dropdown); the `allow_capture_authorization` 3-state property; capture = the order's current total (capture less by editing the order down); no bulk / no re-auth UI; the Sync item in the cog dropdown.
- [[orders-payment-capture-provider-matrix]] — the verified set of gateways that actually produce an Authorized state (Borica WAY4 / DSK Bank / Btepos / Raiffeisen / Monri / Revolut Business); and the providers that never do (Stripe / PayPal / CloudCart Pay / Mollie / Mokka / Klear / Iute).
- [[orders-payment-capture-amount-exceeds]] — the one concrete failure case the platform surfaces: order total now exceeds the authorized amount → Capture is replaced by a danger alert AND the matching status change is blocked too.
- [[orders-payment-capture-side-effects]] — what fires on Capture success vs Cancel success (status flips, stock decrement, webhook, history actions 49 / 45 / 40 / 35); no customer email; Btepos / BoricaWay4 loyalty split-call; gateway retry behaviour.
- [[orders-payment-capture-auto-triggers]] — capture happens automatically when a fulfillment is added (gateway-dependent); cancel happens automatically when the order moves to any negative status — so the merchant often never clicks these buttons manually.
- [[orders-payment-capture-api-access]] — JSON-API v2 is read-only for payments; no mutate endpoint captures or cancels directly; the fulfillment-add indirect-capture path; the `authorize_payment` plan gate.

## Where to find it

From [[orders-details]] → the **Payment action row** under the order summary, when the payment status is **Authorized**. The actions appear in two surfaces — a primary action row (large Authorize / Cancel buttons) and a cog/settings dropdown next to the payment status badge. Both call the same routes and produce identical results. See [[orders-payment-capture-buttons]] for the full surface + visibility matrix.

Routes:
- Capture: `/admin/orders/action/payment/capture-authorization/{payment_id}`.
- Cancel: `/admin/orders/action/payment/cancel-authorization/{payment_id}`.

## What the merchant can do here

- **Capture authorization** — click **Authorize `<amount>`** (the amount is shown in the label, e.g. *"Authorize 100.00 BGN"*). A confirmation dialog *"Capture authorization?"* appears; on accept the platform calls the gateway's capture API, the payment flips to Completed, and the order follows the configured "paid" rules (see [[settings-statuses]]).
- **Cancel authorization** — click **Cancel authorization** (red, danger styling). A confirmation dialog *"Cancel authorization?"* appears; on accept the gateway releases the hold and the payment flips to Cancelled / Voided.

What the merchant **cannot** do here: capture **more** than the authorized hold (blocked — see [[orders-payment-capture-amount-exceeds]]), type an arbitrary capture amount (the order total *is* the captured amount — edit the order down to capture less), capture an expired authorization, or re-authorize a cancelled one. See [[orders-payment-capture-buttons]] for these limits.

## Settings & fields

This page documents an **action**, not a configuration form — there are no merchant-editable fields on this surface. The relevant configuration lives elsewhere:

- **Two-phase mode per gateway** — whether a gateway returns payments in Authorized state is set at gateway-config time (see [[settings-payment-providers]]), gated by the `authorize_payment` plan feature — see [[orders-payment-capture-api-access]].
- **Capture-allowed gating** — the per-payment `allow_capture_authorization` property; see [[orders-payment-capture-buttons]].
- **Permission** — standard `orders` scope; no special grant (unlike `orders.refund`). See [[settings-staff]].

## Business rules

The full rule set is distributed across the aspect pages. The cross-cutting rules in one place:

- **Capture vs Cancel are distinct flows** — Capture completes the sale (money to merchant); Cancel abandons it (money back to customer). Once captured, only a Refund reverses it (see [[orders-payment-refund]]).
- **Capture amount = the order's current total** — the gateway is charged the payment's current amount (synced to the order total), capped at the authorized hold. To capture less, edit the order **down** before capturing; there is no separate partial-amount field. See [[orders-payment-capture-buttons]].
- **Two-phase is gateway-driven** — the platform doesn't unilaterally decide; only a verified set of card gateways ever return Authorized state. See [[orders-payment-capture-provider-matrix]].
- **Authorisations expire on the gateway side** — CloudCart does not track or display expiry; the merchant should capture promptly. See [[orders-payment-capture-buttons]].
- **Order total may not exceed the authorized amount** — both the Capture button and status changes are blocked when it does. See [[orders-payment-capture-amount-exceeds]].
- **Capture / cancel often happen automatically** — adding a fulfillment auto-captures; a negative-status flip auto-cancels. See [[orders-payment-capture-auto-triggers]].
- **No customer email** is sent by the capture / cancel handler itself. See [[orders-payment-capture-side-effects]].

## Related

- [[orders-details]] — parent page (buttons live in the payment action row).
- [[orders-payment-refund]] — for already-captured payments needing reversal.
- [[orders-payment-mark-paid]] — for offline payments without programmatic capture.
- [[settings-payment-providers]] — gateway integrations + two-phase support.
- [[settings-statuses]] — the "paid" status rules a capture triggers.
- [[settings-staff]] — orders permission grant.
- [[settings-hooks]] — `order.updated` webhook on capture / cancel.
- [[orders-history]] — capture / cancel events appear in the audit log.
- [[api-order-payment]] — read-only JSON-API v2 resource.
- [[api-order-fulfillment]] — writable; fulfillment add can auto-capture.
- [[json-api-v2]] — API overview.
- [[orders]] — parent list.
- [[order-processing-pipeline]] — the authorise-then-capture trigger at fulfillment.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
