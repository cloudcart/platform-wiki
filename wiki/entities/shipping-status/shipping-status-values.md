---
type: entity
nav_path: "Entity → Shipping Status → Values"
aliases: ["Shipping status values", "Shipping status enum", "Fulfillment status values", "5 shipping statuses", "Shipping status meanings", "Стойности на статус на доставка"]
tags: [entity, orders, shipping, statuses]
created: 2026-06-10
updated: 2026-08-06
source_count: 0
---

> Part of [[shipping-status]]. See the hub for the other aspects (lifecycle, side-effects).

# Shipping Status — the values

## Identity

This page is the canonical reference for the **5 canonical Shipping Status values** stored on an [[order|Order]]'s `status_fulfillment` field — what each one means in merchant terms and when it gets set. The canonical values are NOT extensible: the merchant cannot add or delete the underlying enum keys. What the merchant CAN do via [[settings-statuses]] is rename the merchant-facing label per language, set a customer-notification toggle per status, and layer **custom sub-statuses** on top of a canonical value — the gates, webhooks, and completion rules read the underlying canonical value, not the custom label.

## Aliases

- "Shipping status values" / "Shipping status enum" — the set of allowed fulfillment states.
- "Fulfillment status values" — same set; the underlying field is `status_fulfillment`.
- "Delivery status options" — informal merchant language.
- Bulgarian: "Стойности на статус на доставка".

## Key Attributes

The Shipping Status enum has **5 canonical values** (verbatim keys preserved):

| Value | Merchant-facing meaning | When set |
|-------|-------------------------|----------|
| `not_fulfilled` | Default state. Merchant has not yet marked the order as fulfilled, no waybill issued, no courier pickup. | Set automatically when the order is created. |
| `fulfilled` | Merchant has packed the order and (typically) issued a waybill — ready for courier pickup or already handed over. | Set when the merchant clicks **Fulfill products** on [[orders-details-shipping]] (which generates the waybill), or when the courier integration confirms label generation. There is no separate "Mark as fulfilled" button. |
| `shipped` | Courier has picked up the parcel and it is in transit. | Set by the courier integration's webhook or by manual merchant action when no integration is configured. |
| `delivered` | Customer (or recipient at the courier office) has received the parcel. | Set by the courier integration's delivery webhook. |
| `returned` | Parcel was sent back to the merchant — refused at delivery, undeliverable, or customer-initiated return. | Set by the courier integration or by manual merchant action on a return flow. |

Not every store uses all five values. Stores without courier integrations typically use only `not_fulfilled` ↔ `fulfilled` and manage the rest via [[order-status|Order Status]] (`cancelled`, `refunded`). For the full flow and triggers between these values, see [[shipping-status-lifecycle]].

### Per-status configuration (from [[settings-statuses]])

Each canonical value carries merchant-editable presentation and behaviour settings, managed under [[settings-statuses]]:

| Setting | What it controls |
|---------|------------------|
| Display label (per language) | The text shown in the admin and in customer-facing emails (e.g., the merchant can rename `fulfilled` to "Packed & ready" or its Bulgarian equivalent). The underlying enum key is unchanged, so all business logic keeps working. |
| Customer-notification toggle | When `On`, customers receive an automated email when the order transitions to this status. When `Off`, the transition is silent. See [[shipping-status-side-effects]] for how this interacts with the per-order `notify_customer` flag. |
| Custom sub-statuses | Per-canonical-value sub-labels that layer on the underlying canonical state (e.g., "Awaiting pickup" under `fulfilled`, "At distribution center" or "Out for delivery" under `shipped`). The gates and webhooks check the underlying canonical value, not the custom label. |

### Custom shipping statuses layer on canonical values

The merchant can define custom shipping-status labels (e.g., "At distribution center", "Out for delivery") that layer on top of the canonical values. The custom label changes what the customer and merchant **see**, but the underlying canonical `status_fulfillment` value is what the platform reads for gates, completion rules, webhooks, and discount-uses counting.

## Where it appears

- [[order]] — every order carries one of these five `status_fulfillment` values.
- [[settings-statuses]] — taxonomy management: labels per language, customer-notification toggles, custom sub-statuses.
- [[orders-details]] — the current value renders as a status pill the merchant can change manually.
- [[orders]] — the orders list shows a shipping/fulfillment-status filter and column.

## Related

- [[shipping-status]] — hub.
- [[order]] — carries one `status_fulfillment` value at a time.
- [[order-status]] — the separate (extensible) Order Status enum; stores without couriers manage the negative branch there.
- [[payment-status]] — the separate Payment Status enum.
- [[settings-statuses]] — rename labels, set notification toggles, add custom sub-statuses.

## Open Questions

No outstanding questions.
