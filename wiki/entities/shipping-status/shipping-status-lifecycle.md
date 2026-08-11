---
type: entity
nav_path: "Entity → Shipping Status → Lifecycle"
aliases: ["Shipping status lifecycle", "Fulfillment lifecycle", "Shipping status transitions", "Fulfillment status flow", "Auto-fulfill on waybill", "Жизнен цикъл на статус на доставка"]
tags: [entity, orders, shipping, statuses]
created: 2026-06-10
updated: 2026-08-06
source_count: 0
---

> Part of [[shipping-status]]. See the hub for the other aspects (values, side-effects).

# Shipping Status — the lifecycle

## Identity

This page documents **how an [[order|Order]]'s Shipping Status moves** through its values over time — the expected flows, what triggers each transition, who drives it (the merchant by hand vs the courier integration via webhook), and why the transitions are NOT strictly enforced as a state machine. For the meaning of each value, see [[shipping-status-values]]; for what a transition triggers downstream (notifications, webhook, auto-completion), see [[shipping-status-side-effects]].

## Aliases

- "Shipping status lifecycle" / "Fulfillment lifecycle" — the order of states over time.
- "Shipping status transitions" — the moves between values.
- "Auto-fulfill on waybill" — the rule that issuing a label flips `fulfilled`.
- Bulgarian: "Жизнен цикъл на статус на доставка".

## Key Attributes

### The canonical flows

The canonical positive flow:

```
not_fulfilled → fulfilled → shipped → delivered
```

The canonical negative branch:

```
(any state) → returned
```

### Transition triggers

| Transition | Typical trigger |
|------------|-----------------|
| `not_fulfilled` → `fulfilled` | Merchant clicks **Fulfill products** on [[orders-details-shipping]], which issues the waybill (see [[orders-shipping-waybill]]). The reverse is the **Mark as unfulfilled** button on the same row. |
| `fulfilled` → `shipped` | Courier integration webhook (parcel scanned at pickup) or manual merchant action. |
| `shipped` → `delivered` | Courier integration webhook (delivery confirmation). |
| `delivered` → `returned` | Courier integration webhook (return-to-sender event) or manual merchant action when handling a return. |
| `fulfilled` / `shipped` → `returned` | Courier reports the parcel was undeliverable or refused at delivery. |

### Transitions are NOT strictly state-machine-enforced

The merchant can in principle move from any Shipping Status to any other from the admin (the status pill on [[orders-details]] accepts any value). The platform expects transitions to follow the positive flow, but out-of-order moves (e.g., `delivered` → `not_fulfilled`) are technically possible — they signal a data-quality issue and may confuse downstream analytics, but the platform does not block them.

### `returned` is NOT strictly terminal

The merchant can manually transition back to `shipped` / `delivered` if the parcel is re-sent after a return. Some courier integrations (Econt, Speedy) report `returned` and then a subsequent re-delivery event re-flips the status. The platform does not block the reverse transition.

### Manual stores vs courier-integrated stores

- **Manual** (no courier integration): the merchant moves the Shipping Status by hand. Most stores stop at `fulfilled` once the parcel is handed to the courier and don't track `shipped` / `delivered` per-order.
- **Integrated**: the courier integration ([[shipping-provider-mechanism]]) drives the Shipping Status via webhooks. The merchant sets `fulfilled` (or it's set automatically on waybill issue), and the rest of the lifecycle is sync'd from the courier's tracking system.

### Auto-fulfill on waybill issue (every courier integration)

For integrations that auto-fulfill on waybill issue (most couriers), generating a waybill via [[orders-shipping-waybill]] sets `status_fulfillment = fulfilled` in the same save, **IF the Order is not already fulfilled**. This applies to Econt, Speedy, Cargus, DPD Bulgaria, DPD Romania, DHL, DHL Express, GLS, BoxNow, Berry, Rapido, Albanian Courier, NTC Logistics, ELS Logistic. The waybill flow checks whether the order is already fulfilled (status is `fulfilled` or a fulfillment record already exists) and skips re-fulfilling; if neither holds, generating the label flips `fulfilled` in the same save. For manual stores or integrations that decouple the two actions, the merchant marks fulfillment separately from waybill issue.

## Where it appears

- [[orders-details]] — the per-order edit hub where the merchant changes the Shipping Status manually (the status pill accepts any value).
- [[orders-shipping-waybill]] — waybill issuance that auto-fulfills the order in the same save.
- [[shipping-provider-mechanism]] — courier integration webhooks that drive `fulfilled → shipped → delivered → returned`.
- [[order]] — carries the current `status_fulfillment` value the lifecycle moves through.

## Related

- [[shipping-status]] — hub.
- [[order]] — carries the `status_fulfillment` value through its lifecycle.
- [[shipping-provider]] — the courier whose webhooks drive the integrated lifecycle.
- [[shipping-provider-mechanism]] — how courier webhooks push transitions.
- [[orders-shipping-waybill]] — waybill issuance and the auto-fulfill rule.
- [[orders-details]] — manual status changes.
- [[order-status-workflow]] — how the lifecycle interacts with Order and Payment status.

## Open Questions

No outstanding questions.
