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

**Status tracking** is the post-dispatch half of the mechanism: after a waybill is issued ([[shipping-provider-mech-waybill]]), the carrier reports delivery progress back to CloudCart, the platform flips the order's [[shipping-status]], and the merchant + customer see live updates. **Overrides** are the cross-cutting side rules that bend the standard pipeline — Cart Rules can hide / force shipping methods, customer groups can see different method sets, the default selection at checkout is controlled in [[settings-cart]], and methods with order history can't be deleted.

This page collects every "after the carrier is configured and quoting works" rule in one place — the things merchants encounter once orders are flowing.

## Scope

Covered:

- Webhook-driven status updates + polling fallback.
- Status-driven customer notification emails.
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

- **Webhook vs. polling**: carriers with mature APIs push status updates via webhooks at key events. For carriers without webhooks, the platform polls the tracking API on a periodic schedule. Webhook = near-real-time; polling = delayed but works for everyone.
- **`shipping-status` (the enum) vs. status label (the displayed string)**: the underlying enum is fixed (e.g., `dispatched`, `in_transit`, `delivered`). [[settings-statuses]] Shipping tab lets the merchant rename the *displayed label* without changing the enum — useful for storefront localisation and tone (e.g., "Sent on its way" vs. "Dispatched").
- **Cart Rules override vs. method configuration**: method configuration (per-method Geo Zone, customer groups, pricing) decides which methods are eligible by default. Cart Rules sit *after* discounts and can force a specific method, modify the shipping line, or add COD surcharges *on this cart only* — they're per-cart overrides on top of the per-method config.
- **Default carrier (settings-cart) vs. method ordering (settings-shipping)**: [[settings-cart]] picks which method auto-selects at checkout when multiple are eligible. The order methods appear in the checkout picker is configured separately on [[settings-shipping]] (drag-reorder). Both are merchant-facing UX decisions and don't affect pricing.

## Where it applies

### Webhook-driven status updates

After waybill generation, the carrier's API can push status updates back to CloudCart via webhook callbacks at key delivery events:

- Package picked up by the courier.
- In transit.
- Out for delivery.
- Delivered (signature captured if required).
- Failed / returned.

Each status update flips the order's [[shipping-status]] enum. For carriers without webhooks, the platform polls the carrier's tracking API on a periodic schedule. (verify — exact polling cadence per carrier.)

### Status-driven customer notification emails

The [[settings-statuses]] Shipping tab lets the merchant rename labels AND toggle customer-notification emails per status — e.g., "Out for delivery" email enabled, "Picked up" silent. The merchant can craft a per-status template; the platform fires the email when the status flip happens.

This is how customers see "Your order is out for delivery" emails. See [[notification-delivery]] for the full notification pipeline.

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
- [[shipping-status]] — the enum tracking dispatch and delivery.
- [[settings-statuses]] — Shipping tab; rename labels + toggle notification emails.
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
