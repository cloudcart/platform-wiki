---
type: concept
nav_path: "Concept → Shipping provider mechanism → Status tracking & overrides"
aliases: ["Shipping status tracking", "Carrier webhooks", "Tracking webhook updates", "Cart rules override shipping", "Customer group shipping restriction", "Default shipping selection", "Delete protection shipping", "Уебхук за статус на доставка", "Кеш правила за доставка", "Защита от изтриване"]
tags: [shipping, couriers, providers, webhooks, status, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (configuration, pricing models, pickup points, waybill, COD, geo routing).

# Shipping provider mechanism — Status tracking & overrides

## Definition

**Status tracking** is the post-dispatch half of the mechanism: issuing a waybill ([[shipping-provider-mech-waybill]]) sets the order's [[shipping-status]] to **Fulfilled** and the customer gets the shipment email. From then on the parcel's progress is the carrier's own tracking status, which some courier integrations show for each shipment; the order's shipping status has only two values and does not follow it. **Overrides** are the cross-cutting side rules that bend the standard pipeline — Cart Rules can hide / force shipping methods, customer groups can see different method sets, the default selection at checkout is controlled in [[settings-cart]], and methods with order history can't be deleted.

This page collects every "after the carrier is configured and quoting works" rule in one place — the things merchants encounter once orders are flowing.

## Scope

Covered:

- The carrier's tracking status vs the order's shipping status.
- The customer email on fulfilment.
- Cart Rules override (force, modify, COD surcharge).
- Customer-group restrictions on method visibility.
- Default-selection rules at checkout.
- Delete protection for methods with orders attached.

Not covered:

- The waybill action that *initiates* status tracking — see [[shipping-provider-mech-waybill]].
- Cart Rules engine itself — see [[apps-cart-rules]].
- Customer group entity — see [[customers-custom-groups]].
- Status label renaming UI — see [[settings-statuses]].

## Contrasts

- **Carrier tracking status vs. shipping status**: the carrier's statuses (picked up, in transit, delivered, returned …) belong to the shipment and are shown in the courier integration where it keeps them. The order's shipping status is `not_fulfilled` or `fulfilled` only, and a waybill makes it `fulfilled`.
- **`shipping-status` (the value) vs. status label (the displayed string)**: the two values are fixed. The [[settings-statuses]] Shipping tab lets the merchant rename their *displayed labels* without changing the value — useful for storefront tone (e.g., "Sent on its way" instead of "Fulfilled").
- **Cart Rules override vs. method configuration**: method configuration (per-method Geo Zone, customer groups, pricing) decides which methods are eligible by default. Cart Rules sit *after* discounts and can force a specific method, modify the shipping line, or add COD surcharges *on this cart only* — they're per-cart overrides on top of the per-method config.
- **Default carrier (settings-cart) vs. method ordering (settings-shipping)**: [[settings-cart]] picks which method auto-selects at checkout when multiple are eligible. The order methods appear in the checkout picker is configured separately on [[settings-shipping]] (drag-reorder). Both are merchant-facing UX decisions and don't affect pricing.

## Where it applies

### Carrier tracking

After the waybill, the carrier tracks the parcel: picked up, in transit, out for delivery, delivered, or failed and returned. Where a courier integration keeps this status, it is shown for each shipment in that integration's shipments list, for example Econt's *Pending pickup / In transit / Delivered / Failed / Returned* ([[econt-shipments]]). It does not change the order's shipping status, which stays **Fulfilled**. Delivery is recorded on the order only as the expected **Delivery date** entered with the fulfilment, and a parcel that comes back is handled as a return ([[orders-details-returns]]). (verify — how often each integration refreshes the carrier status.)

### Customer notification on fulfilment

Shipping statuses have no per-status notification switch. When the order is fulfilled (by a waybill, **Fulfill products** or the status menu), the customer gets the shipment email, provided the order's Notify-customer flag is on. Un-fulfilling sends no email. See [[shipping-status-side-effects]] and [[notification-delivery]].

### Cart Rules override

Cart Rules ([[apps-cart-rules]]) can override the standard shipping pipeline at three levels:

- **Force a specific shipping method** on qualifying carts (e.g., "carts over 5kg must use Econt to-address only").
- **Modify the shipping line** (add / subtract a fixed amount, apply a percentage discount).
- **Add / remove COD surcharges** independent of the carrier's default.

Cart Rules run **after** discounts on the cart, so a free-shipping discount that already zeroed the line will see zero shipping when the Cart Rule runs. See [[shipping-calc-discounts-rules]] for the interaction with discounts.

### Customer Group restriction — wholesale vs. retail

Customer groups ([[customers-custom-groups]]) can restrict which shipping methods are visible to which group. Common pattern: wholesale customers see a different set of shipping methods (heavy / pallet-only) than retail customers. Configured per-method via the allowed-customer-groups multi-select (when present) or per-discount via the customer-group restriction on the discount.

### Default selection at checkout

The default shipping method auto-selected at the customer's checkout step is configured in [[settings-cart]] — **NOT** in [[settings-shipping]]. The setting picks both default shipping TYPE (carrier vs. custom) and default PROVIDER (specific carrier).

When [[settings-cart]]'s *"Automatically select if only one is available"* toggle is ON and exactly one method matches the customer's cart, that method is pre-selected without showing the picker. This is the smoothest UX when the merchant has only one shipping method that covers the customer's region.

### Delete protection — orders attached block deletion

A shipping method that has orders attached to it **cannot be deleted**. The error *"You can not delete this shipping method because there are orders attached to it"* fires when the merchant attempts to remove it.

The workaround is to toggle the method OFF (active = no) — it disappears from the storefront but the historical data stays intact. This protects accounting / fulfillment audit trails: order records keep their canonical reference to the carrier they shipped via, even years later.

For "I can't delete this method" support tickets, the answer is always the same: toggle Inactive in [[settings-shipping]]; don't try to delete.

## Related

- [[shipping-provider-mechanism]] — hub.
- [[shipping-status]] — the two values: not fulfilled / fulfilled.
- [[settings-statuses]] — Shipping tab; rename the two labels.
- [[notification-delivery]] — the full notification pipeline.
- [[shipping-provider-mech-waybill]] — the action that initiates tracking.
- [[apps-cart-rules]] — Cart Rules engine.
- [[shipping-calc-discounts-rules]] — discount + rule interaction.
- [[customers-custom-groups]] — customer-group entity.
- [[settings-cart]] — default carrier + auto-select toggle.
- [[settings-shipping]] — Active/Inactive toggle and method ordering.
- [[shipping-provider-lifecycle]] — sister entity-side documentation of soft-delete + delete-protection.

## Open Questions

- ⏸️ Exact polling cadence for carriers without webhook support. Differs per carrier and likely per plan/environment.
- ⏸️ Whether the "force a specific shipping method" Cart Rule action can force a method that's normally outside the customer's Geo Zone (i.e., does the override bypass geo gating?). (verify against the rule engine.)
