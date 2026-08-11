---
type: entity
aliases: ["Payment status values", "Payment status enum", "13 payment statuses", "Payment status meanings", "Стойности на платежен статус"]
tags: [orders, payments, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[payment-status]]. See the hub for the other aspects (lifecycle, vs order status, provider mappings).

# Payment Status — the values

## Identity

This page is the canonical reference for the **13 platform-defined payment-status values** — what each one means in merchant terms and when it gets set. The values are NOT extensible: the merchant cannot add or delete payment statuses (unlike [[order-status]], which supports custom statuses). The only merchant-editable part is the **label** — via [[settings-statuses]] the merchant renames the merchant-facing text while the underlying enum key stays fixed so all business logic keeps working.

## Aliases

- "Payment status values" / "Payment status enum" — the set of allowed states.
- "Money status options" — informal merchant language.
- Bulgarian: "Стойности на платежен статус".
- In the platform schema this is the `status` column on the order's payment record and on the gateway-side payment row.

## Key Attributes

The payment-status enum has **13 values** (verbatim keys preserved):

| Status value | Merchant-facing meaning | When it's set |
|--------------|-------------------------|---------------|
| `initiated` | The payment record was created but the customer hasn't been sent to the gateway yet. | First step of a checkout — the platform created the record and is about to redirect the customer. |
| `requested` | The customer has been redirected to the gateway; awaiting their action. | Set when the platform issued the checkout-session / payment-intent and is waiting for the customer's return. |
| `pending` | Payment is in progress at the gateway — neither failed nor confirmed. | The gateway accepted the request but hasn't finalised yet (bank approval, async confirmation, manual review). |
| `authorized` | Funds are reserved on the customer's card (pre-auth) but NOT captured. | Gateways with separate auth/capture flow (e.g., Stripe pre-auth, Klarna hold). The merchant must explicitly **Capture** to charge or **Cancel authorization** to release. |
| `held` | Payment is held by the gateway for risk-review or compliance reasons. | Gateway-flagged for review; awaiting resolution. |
| `completed` | Money has been captured / settled. The order is "paid". | Final positive state. Triggers stock decrement, customer-notification email, and (with fulfillment) auto-completion of the order — see [[payment-status-vs-order-status]]. |
| `failed` | Payment attempt failed (card declined, insufficient funds, gateway error). | Negative state. Order typically transitions to `failed` or `pending` so the merchant can retry. |
| `refunded` | Money has been returned to the customer (full refund). | Set after a successful refund call to the gateway. |
| `voided` | Authorisation was cancelled before capture (no charge ever happened). | Set when the merchant clicks **Cancel authorization** on an `authorized` payment. |
| `cancelled` | Payment was cancelled (customer abandoned, merchant cancelled, gateway reported cancelled). | Distinguished from `failed` — typically used when the customer explicitly aborted vs. the card was declined. |
| `timeouted` | Gateway timed out before returning a final answer. | The platform gave up waiting for the gateway's response. The merchant or a sync usually flips it to a final state. |
| `chargebacked` | The customer's bank initiated a chargeback against the captured payment. | Set via reconciliation / sync with the gateway. |
| `disputed` | The payment is under dispute or investigation. | Pre-chargeback state — gateway has flagged the transaction. |

### Per-payment metadata the status reflects / drives

| Attribute | What it carries |
|-----------|-----------------|
| **Provider** (`provider`) | Which [[payment-provider]] processed this payment (`stripe`, `cardlink`, `borica-way4`, `cloudcart-pay`, etc.). |
| **Amount** (`amount`) | The amount captured / requested, in cents. |
| **Provider reference** (`provider_reference_id`) | The gateway's internal ID — Stripe's `pi_...`, PayPal's order ID, etc. Used for sync and refund calls. |
| **Authorize amount** (`authorize_amount`) | For pre-auth payments — the amount currently held (may differ from the capture amount). |
| **Date last update** (`date_last_update`) | When the status last changed. |
| **Hash** (`hash`) | Secret token used in customer-facing payment URLs. |

### Stored constants vs full enum (9 of 13)

Only **9 of the 13 statuses** are defined as code constants: `initiated`, `requested`, `pending`, `authorized`, `completed`, `refunded`, `cancelled`, `failed`, `timeouted`. The other 4 (`held`, `voided`, `chargebacked`, `disputed`) appear in mapping logic but are not constants — they are written by provider-specific code paths only. A merchant filtering "all held payments" or "all disputed payments" relies on each provider having explicitly emitted that status code.

### NEGATIVE_STATUS counterparts

The 11-order-status `NEGATIVE_STATUS` array has direct counterparts in payment status: `voided`, `cancelled`, `failed`, `timeouted`, `refunded`, `chargebacked`, `disputed`. These are the "money didn't ultimately land with the merchant" payment statuses — all shown in red and kept out of revenue.

## Where it appears

- [[settings-statuses]] — the **Payment** tab lists all 13 statuses for label-renaming.
- [[orders]] — payment-status filter and column on the orders list.
- [[orders-details]] — the current value renders as a coloured badge on the payment row.
- [[analytics-full]] — dashboards count `completed` separately from `failed` / `cancelled`.

## Related

- [[payment-status]] — hub.
- [[order-status]] — the OTHER (extensible) status enum; contrast with this fixed 13-value set.
- [[shipping-status]] — fulfillment status; also a separate enum.
- [[payment-provider]] — emits the provider-specific values such as `held` / `disputed`.
- [[settings-statuses]] — Payment tab; rename labels (enum key unchanged).
- [[analytics-full]] — aggregates orders by payment status value.

## Open Questions

No outstanding questions.
