---
type: feature
nav_path: "Orders → Order details → Payment → Change provider"
route_name: admin.orders.payment
route_path: /admin/orders/action/payment/:order_id
aliases: ["Change payment provider", "Switch payment method", "Change provider on order", "Смяна на доставчик за плащане", "Смяна на метод за плащане"]
tags: [orders, payment, change-provider, taxes, shipping-side, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---

> Part of [[orders-payment-manual]]. See the hub for related aspects (Mokka confirm, Klear confirm, lease, API access).

# Change payment provider

## Purpose

The **Change provider** flow swaps the payment provider on an existing order — used when the customer chose one method at checkout but the merchant needs to switch (e.g., "I'll pay by bank transfer instead of card"). The platform creates a NEW payment record with the new provider, deletes taxes tied to the old provider, recomputes the total, and may adjust the shipping-payer side. The change applies immediately when the merchant picks a provider from the dropdown.

## Where to find it

From [[orders-details]], the Payment row shows a `payment_providers_select` dropdown — but **only** when the order's status is NOT in `[authorized, completed, paid, refunded]` AND fulfillment is NOT `fulfilled`. The merchant picks a new provider; the form auto-submits (the dropdown carries `data-change-payment="true"`, which triggers the POST on change).

Route: `/admin/orders/action/payment/{order_id}` (POST with the `payment_provider` field).

## What the merchant can do here

Pick a new provider from the dropdown. On submission the platform:

1. Deletes all order taxes that were tied to the old provider (typically tax surcharges added by the old payment method).
2. Creates a NEW order-payment record with the new provider, the order's invoice total amount, and status `INITIATED`.
3. If the new provider has the `is_seller_payer_shipping` flag AND the order's shipping side isn't already set, updates the order's `side` meta (shipping payer side).
4. Recalculates the order's total with the new provider, re-applying the billing zone's payment-conditional taxes that match the new provider.
5. For offline-type providers (Bank Transfer, COD), immediately runs the new gateway's `purchase` flow to register the offline payment record on the gateway side.

### What the merchant CANNOT do here

- Change provider once the order is `authorized`, `completed`, `paid`, `refunded`, OR fulfillment is `fulfilled` — the dropdown is disabled / not rendered.
- Change provider on an empty-cart order, or on an order with no shipping that is not digital-only — both disable the dropdown (see Business rules).
- Bulk-change the provider — strictly per-order; provider migrations must be scripted via the API or done order-by-order.
- Pick the `tbi` provider (legacy — explicitly excluded) or any provider not enabled in [[settings-payment-providers]].

## Settings & fields

| Control | Notes |
|---------|-------|
| **Provider dropdown** (`payment_providers_select`, field `payment_provider`) | Lists providers the merchant has enabled via [[settings-payment-providers]]. The `tbi` provider is always excluded. If `manual_order_payments` is set on [[settings-cart]], only providers in that whitelist are available for manual orders. Auto-submits on change. |

**Dropdown disable conditions** (beyond the order-status / fulfillment gate):

- Order has NO products (empty cart) → disabled.
- Order has NO shipping AND is not digital-only → disabled.

Both ensure totals can be recalculated deterministically; without shipping set, the new provider's shipping-side adjustment can't run.

## Business rules

### Destructive on taxes — recomputes against payment-conditional taxes

Switching the provider DELETES the order's existing tax records tagged with a `payment_provider` value, then re-applies the new set: for every tax configured in the order's billing zone with a non-null `payment_provider`, the platform checks whether it now matches the new provider + the existing shipping, and re-attaches the matching tax records. This is why provider-conditional surcharges (e.g., "+2% for COD") flip cleanly when switching from card to COD. The merchant should be aware this can change the order's total — they may need to re-add discounts or tax overrides.

### Creates a NEW payment record (old one preserved)

The old payment record is NOT deleted — it stays attached in its historical state. A new order-payment record is created with the new provider in `INITIATED` status. This preserves the audit trail; multiple payment records per order is normal after a switch.

### Shipping-side adjustment

If the new provider has the `is_seller_payer_shipping` flag set (seller pays shipping, common with some BNPL providers) AND the order's shipping side isn't already set, the platform updates the order's `side` meta to "seller pays" (`PAYER_SENDER`) — UNLESS the courier's config explicitly forces `PAYER_OTHER`. This adjustment is provider-driven; the merchant doesn't see it as an explicit step.

The `side` meta has exactly three values:
- `PAYER_SENDER` ('SENDER') — the merchant pays the shipping cost.
- `PAYER_RECEIVER` ('RECEIVER') — the customer pays on delivery.
- `PAYER_OTHER` ('OTHER') — a third party (marketplace / fulfilment partner) covers shipping.

### Re-initialises the gateway for offline-type providers

When the new provider is NOT an online payment (e.g., Bank Transfer or COD), the platform immediately calls the new gateway's `purchase` flow to register the offline payment record on the gateway side. The payment is created in `INITIATED` state and the offline gateway integration sets up the matching record — useful for couriers that require the COD intent to be pre-registered.

### Captured in history

The change runs through the standard order-update hooks, which write an `order_payment_*` history entry. The merchant can later see in [[orders-history]] which provider was active when, plus the acting admin's identity.

### No webhook on provider-only change

No `order.updated` webhook fires on JUST a provider change — verified: the change-provider action doesn't call the order's hook trigger (unlike most other order edits, which do — see [[order-pipeline-stage-5-edit]]). An integration sees the new provider only at the next status change or by polling [[json-api-v2|JSON-API v2]].

### Permission

Standard orders write access; no specific change-provider grant.

## Related

- [[orders-payment-manual]] — hub.
- [[orders-details]] — parent page hosting the dropdown.
- [[settings-payment-providers]] — provider list the dropdown filters against.
- [[settings-cart]] — `manual_order_payments` whitelist for change-provider restrictions.
- [[orders-history]] — provider-change events recorded here.
- [[orders-status-change]] — order status gates dropdown availability.

## Open questions

- Confirm whether any webhook fires on a provider-only change `(verify)`.
