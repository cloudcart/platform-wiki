---
type: entity
nav_path: "Entity → Shipping Status → Lifecycle"
aliases: ["Shipping status lifecycle", "Fulfillment lifecycle", "Shipping status transitions", "Fulfillment status flow", "Auto-fulfill on waybill", "Жизнен цикъл на статус на доставка"]
tags: [entity, orders, shipping, statuses]
created: 2026-06-10
updated: 2026-10-21
source_count: 0
---

> Part of [[shipping-status]]. See the hub for the other aspects (values, side-effects).

# Shipping Status — the lifecycle

## Identity

This page documents **how an [[order|Order]]'s Shipping Status moves** through its values over time — the flow between its two values, what triggers each transition, who drives it (the merchant by hand, a courier waybill, or an automatic rule), and which gates apply. For the meaning of each value, see [[shipping-status-values]]; for what a transition triggers downstream (notifications, webhook, auto-completion), see [[shipping-status-side-effects]].

## Aliases

- "Shipping status lifecycle" / "Fulfillment lifecycle" — the order of states over time.
- "Shipping status transitions" — the moves between values.
- "Auto-fulfill on waybill" — the rule that issuing a label flips `fulfilled`.
- Bulgarian: "Жизнен цикъл на статус на доставка".

## Key Attributes

### The flow

```
not_fulfilled ⇄ fulfilled
```

There are only these two values. Nothing comes after `fulfilled`: a courier's tracking events do not change the shipping status, delivery is recorded only as the expected **Delivery date** entered with the fulfilment, and a parcel that comes back is a separate return record ([[orders-details-returns]]).

### Transition triggers

| Transition | Trigger |
|------------|---------|
| `not_fulfilled` → `fulfilled` | The merchant clicks **Fulfill products** on [[orders-details-shipping]]: a courier waybill ([[orders-shipping-waybill]]), or a manual record of the dispatch for shipping methods without a courier integration. Also picking **Fulfilled** in the order's status menu (shipping methods without a courier integration only), and automatically when an order with only digital products becomes paid. |
| `fulfilled` → `not_fulfilled` | **Mark as unfulfilled** on the same row, or picking **Not fulfilled** in the status menu (shipping methods without a courier integration only). Automatically when a fulfilled order moves to a negative status (cancelled, refunded …). |

### Manual stores vs courier-integrated stores

- **Without a courier integration**: the merchant records the dispatch with **Fulfill products**, or picks the value in the status menu.
- **With a courier integration**: issuing the waybill fulfils the order (below). The status menu does not offer the shipping values; the courier's own tracking status, where an integration keeps one, is shown in that integration's shipments list (for example [[econt-shipments]]), not as the order's shipping status.

### Auto-fulfill on waybill issue (every courier integration)

For integrations that auto-fulfill on waybill issue (most couriers), generating a waybill via [[orders-shipping-waybill]] sets `status_fulfillment = fulfilled` in the same save, **IF the Order is not already fulfilled**. This applies to Econt, Speedy, Cargus, DPD Bulgaria, DPD Romania, DHL, DHL Express, GLS, BoxNow, Berry, Rapido, Albanian Courier, NTC Logistics, ELS Logistic. The waybill flow checks whether the order is already fulfilled (status is `fulfilled` or a fulfillment record already exists) and skips re-fulfilling; if neither holds, generating the label flips `fulfilled` in the same save. For manual stores or integrations that decouple the two actions, the merchant marks fulfillment separately from waybill issue.

## Where it appears

- [[orders-details]] — the per-order edit hub where the merchant changes the Shipping Status manually (the status menu offers **Fulfilled** / **Not fulfilled** for shipping methods without a courier integration).
- [[orders-shipping-waybill]] — waybill issuance that auto-fulfills the order in the same save.
- [[shipping-provider-mechanism]] — courier integrations, whose waybill sets `fulfilled`.
- [[order]] — carries the current `status_fulfillment` value the lifecycle moves through.

## Related

- [[shipping-status]] — hub.
- [[order]] — carries the `status_fulfillment` value through its lifecycle.
- [[shipping-provider]] — the courier whose waybill fulfils the order in integrated stores.
- [[shipping-provider-mechanism]] — how courier integrations issue waybills.
- [[orders-shipping-waybill]] — waybill issuance and the auto-fulfill rule.
- [[orders-details]] — manual status changes.
- [[order-status-workflow]] — how the lifecycle interacts with Order and Payment status.

## Open Questions

No outstanding questions.
