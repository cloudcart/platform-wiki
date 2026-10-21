---
type: entity
nav_path: "Entity → Shipping Status → Values"
aliases: ["Shipping status values", "Shipping status enum", "Fulfillment status values", "2 shipping statuses", "Shipping status meanings", "Стойности на статус на доставка"]
tags: [entity, orders, shipping, statuses]
created: 2026-06-10
updated: 2026-10-21
source_count: 0
---

> Part of [[shipping-status]]. See the hub for the other aspects (lifecycle, side-effects).

# Shipping Status — the values

## Identity

This page is the canonical reference for the **2 Shipping Status values** an [[order|Order]] can hold — what each one means in merchant terms and when it gets set. The values are NOT extensible: the merchant cannot add or delete shipping statuses. What the merchant CAN do via [[settings-statuses]] is give each value a new name — the gates, webhooks, and completion rules read the underlying value, not the custom name.

## Aliases

- "Shipping status values" / "Shipping status enum" — the set of allowed fulfillment states.
- "Fulfillment status values" — same set; the underlying field is `status_fulfillment`.
- "Delivery status options" — informal merchant language.
- Bulgarian: "Стойности на статус на доставка".

## Key Attributes

The Shipping Status has **2 values** (verbatim keys preserved):

| Value | Merchant-facing meaning | When set |
|-------|-------------------------|----------|
| `not_fulfilled` | Shown as **Not fulfilled** (Bulgarian: *Не е изпратена*). The order has not been dispatched. | Set automatically when the order is created; set again by **Mark as unfulfilled** on [[orders-details-shipping]], by picking **Not fulfilled** in the order's status menu (shipping methods without a courier integration only), or automatically when a fulfilled order moves to a negative status (cancelled, refunded …). |
| `fulfilled` | Shown as **Fulfilled** (Bulgarian: *Изпратена*). The order has been dispatched. | Set when the merchant clicks **Fulfill products** on [[orders-details-shipping]] (a courier waybill, or a manual record of the dispatch for shipping methods without a courier integration), by picking **Fulfilled** in the order's status menu (shipping methods without a courier integration only), or automatically when an order with only digital products becomes paid. There is no separate "Mark as fulfilled" button. |

There are no *shipped*, *delivered* or *returned* shipping statuses. *Изпратена* ("shipped") is the Bulgarian name of **Fulfilled**; delivery is recorded only as the expected **Delivery date** entered with the fulfilment; and a return is a separate record with its own status (pending / returned / cancelled) in the **Returns & exchanges** box — see [[orders-details-returns]]. For the flow between the two values, see [[shipping-status-lifecycle]].

### Per-status configuration (from [[settings-statuses]])

On the **Shipping** tab of [[settings-statuses]] the two values are listed with their current name and a **New status name** field. Renaming is the only setting: one name per value (not per language), no adding, deleting or nesting of shipping statuses, and no customer-notification switch on that tab. A rename changes what the merchant and customer **see**; the underlying value is unchanged, so all business logic keeps working.

## Where it appears

- [[order]] — every order carries one of these two values.
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
