---
type: feature
nav_path: "Orders → Order details → Payment → Refund → Gateway quirks"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Refund gateway quirks", "Mokka refund quirk", "Klear refund email", "Stripe pi vs ch refund", "Borica WAY4 idle retry", "Refund network error"]
tags: [orders, payment, refund, gateway, quirks]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-payment-refund]]. See the hub for the other aspects (visibility, provider matrix, side effects, partial refunds, status-flip rules, API access).

# Payment refund — gateway quirks

## Purpose

The refund flow looks uniform from the merchant's perspective (click the red button, see a toast), but the gateway-level behaviour varies enough that several providers need explicit guidance. This page catalogues the known quirks — error patterns, manual-processing flows, network-failure handling, and per-provider request shapes — so a support agent can interpret a confusing refund outcome.

## Where to find it

The quirks below apply when the merchant clicks **Refund payment** on [[orders-details]]. The user-visible difference is the toast message and the resulting state in [[orders-history]] / the gateway's own dashboard. See [[orders-payment-refund-visibility]] for when the button is rendered, and [[orders-payment-refund-provider-matrix]] for which providers expose refund at all.

## What the merchant can do here

Recognise the quirk and respond appropriately — refresh the page, check [[orders-history]] for the action code, verify in the gateway's dashboard, or contact the provider's support.

## Settings & fields

This page documents gateway behaviour, not configuration. The relevant per-provider configuration lives on [[settings-payment-providers]].

## Business rules

### Mokka — error toast even on success

The Mokka refund handler **always** throws `PaymentBadRequest($response['message'])` at the end of the method, AFTER setting the local payment to `refunded`. So clicking Refund on a Mokka order ALWAYS shows an error toast to the merchant — even when Mokka has accepted the refund. The local payment status will already be `refunded` (and an entry exists in [[orders-history]]), but the UX is misleading.

Mokka's request shape:
- Sends `return` if Mokka considers the order `finished`.
- Sends `cancel` if Mokka considers the order not yet finished.
- Always passes the FULL `price_total_input` — so if the order amount changed since checkout, the changed amount is what gets refunded.

After clicking Refund on a Mokka order, the merchant should:

1. Refresh the order page after the error toast.
2. Check [[orders-history]] for action code 20 (`order_payment_refunded`).
3. Verify in Mokka's merchant dashboard whether the refund was actually applied.

### Klear — email-to-staff manual flow

Klear does NOT expose a refund API. Instead, when the merchant clicks Refund on a completed Klear payment:

1. The platform sends an EMAIL to `the provider's support address` with the merchant's public API key, the order ID, and the amount.
2. Klear staff process the refund manually offline.
3. The platform IMMEDIATELY marks the local payment as `refunded` regardless of email outcome.

So on the platform side the order shows refunded, but the customer's actual refund waits on Klear's manual processing turnaround. The Klear refund flow runs ONLY when the original capture is recorded (`provider_data->capture` is non-empty); without a captured Klear payment, the email isn't sent — but the local status flip still happens.

### Stripe — `pi_*` vs `ch_*` handling, full amount only

The Stripe integration handles both legacy charges (`ch_*` prefix) and modern PaymentIntents (`pi_*` prefix). On click:

1. Looks at the provider_reference_id to decide which Stripe object to refund.
2. Sends a full-amount refund (NO amount parameter) — so Stripe refunds whatever is left of the charge.
3. If Stripe's response status is `succeeded`, the platform flips local payment to `refunded` and stores the new reference ID.

Stripe's refund is irrevocable on Stripe's side — once issued, the merchant cannot recall it. Stripe's refund window is on Stripe's side (typically ~180 days from the original charge for the Refunds API); older charges may not be refundable. The platform doesn't surface this — if Stripe rejects, the merchant sees the gateway's error message.

### Borica WAY4 — idle-retry helper

The Borica WAY4 refund call uses the **same idle-retry helper** as capture and cancel. If Borica's endpoint is temporarily idle, the helper retries with a short backoff. This applies only to Borica WAY4; other bank gateways have their own retry behaviour or none.

### CIB Bank — retransfer auto-fallback

The CIB Bank integration includes an auto-fallback to "retransfer" semantics if the primary refund call shape isn't accepted. The merchant sees a single Refund click; CIB handles the fallback internally. The response is logged to the payment log.

### Network errors — HTTP 504 + log entry, no auto-retry

When any gateway call fails with a network error (timeout, gateway unreachable):

1. The platform catches the exception.
2. Logs the failure to the platform's exception store for later diagnosis.
3. Returns **HTTP 504** with the gateway's error message.
4. The merchant sees an error toast — the refund is NOT recorded as successful.
5. The merchant retries the click OR contacts the provider's support to investigate.

The platform does **NOT** automatically retry refund calls — failures need manual investigation because they may indicate ambiguous partial-failure states (gateway processed but didn't acknowledge, vs not processed at all).

### Paynetics — TODO stub, manual portal refund

The Paynetics refund hook is a TODO stub — no automated refund surface is implemented today. Refunds initiate from Paynetics's own merchant portal. The merchant can still mark the local order as refunded via the platform's standard refund handler, but the financial reversal happens at Paynetics. See [[orders-payment-refund-provider-matrix]].

### Sofort — refunds happen at Klarna's portal

Sofort refunds are typically processed in Klarna's portal, not via this Refund button. The platform exposes the button conditionally; the actual reversal is Klarna-side.

### FusionPay — excluded from regular refund flow

FusionPay is excluded from the normal refund handler ("lease" exclusion). The Refund button is not shown for FusionPay payments. (verify)

## Related

- [[orders-payment-refund]] — hub.
- [[orders-payment-refund-provider-matrix]] — full per-provider support list.
- [[orders-payment-refund-side-effects]] — what fires after a successful gateway call.
- [[orders-history]] — verify action code 20 / 21 / 43 after a quirky refund.
- [[settings-payment-providers]] — provider list.

## Open questions

- Whether FusionPay refunds via this UI surface are currently fully excluded or only excluded from the auto-cascade. (verify)
