---
type: entity
nav_path: "Entity → Cart → Lifecycle"
aliases: ["Cart lifecycle", "Cart states", "Active cart", "Abandoned cart state", "Converted cart", "Cart TTL", "Cart cleanup", "Cart purge", "Жизнен цикъл на количка"]
tags: [entity, orders, cart, checkout, lifecycle]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[cart]]. See the hub for the other aspects (data model, stock & pricing, recovery, merge).

# Cart — Lifecycle

## Identity

This page describes the **states a Cart moves through** and how it is eventually cleaned up. A cart's life runs from the first item added, through possible abandonment and recovery, to either conversion into an [[order|Order]] or auto-purge after ageing out. The single most important transition — Cart → Order — is owned by [[cart-vs-order-lifecycle]]; this page covers the cart-side states and the platform-driven cleanup that the merchant cannot tune.

## Aliases

- **Active / pending cart** — the cart while the customer is still shopping.
- **Abandoned cart** — the same cart once `updated_at` crosses the abandonment threshold; surfaces on [[orders-abandoned]].
- **Converted cart** — a cart that has produced an Order.
- **Lost / aged-out cart** — a cart auto-purged after the 7-day TTL.

## Key Attributes

A Cart moves through these states:

1. **Created / Active** — the customer added their first item; `updated_at` is recent. The cart is fully editable. Multiple customers can hold the same last unit of stock in their carts simultaneously (no reservation — see [[cart-entity-stock-pricing]]).
2. **Abandoned** — `updated_at` is older than the **abandoned threshold** (default 60 min; configurable to 30 / 45 / 60 / 90 / 180 minutes on [[settings-cart]]). The cart surfaces on [[orders-abandoned]]. The customer can still return and finish — the cart is NOT locked.
3. **Recovered** — the customer clicked the restore link in the recovery email / Messenger message; the cart's contents are restored into a fresh checkout session. If the customer completes checkout, the resulting Order carries `abandoned = 1` and `restore_source` = `email` or `messenger`. Full detail on [[cart-entity-recovery]].
4. **Converted** — the customer clicked Place order. A new Order is created from the cart's snapshot. The cart's reference (`cart_id`) is kept on the Order for audit, but the cart itself is no longer modifiable by the customer.
5. **Lost / Aged out** — the customer never returned. The platform auto-purges carts older than **7 days** since last modification (TTL governed by the platform; merchant cannot tune).
6. **Hard-deleted** — when the cart's owning customer is hard-deleted, all carts with that `customer_id` are cascade-deleted.

### The abandonment transition is time-based

Cart → Abandoned is **time-based**, not customer-action-based. The customer does nothing — the platform's every-3-minute sweep detects carts whose `updated_at` is older than the threshold and includes them in the abandoned list. Note that the **auto-touch timer** (see [[cart-entity-model]]) silently refreshes `updated_at` on page loads more than 10 minutes apart, so the abandoned timer measures session inactivity rather than strict cart-content stillness.

### TTL and post-conversion soft-delete

- **TTL = 7 days from `updated_at`** (`cart.lifetime` platform config). Carts older than this are soft-deleted, then hard-deleted with their child rows. Not exposed in [[settings-cart]].
- **Post-conversion auto-soft-delete** — any cart that has produced an Order (`orders.cart_id` populated) is soft-deleted **even before the 7-day TTL**. The Order's `cart_id` is preserved for audit; when the cart row is finally hard-deleted, the Order's `cart_id` is set to NULL so no broken references remain.

### Cleanup is enforced by two scheduled jobs

The platform runs two cart-cleanup jobs on its internal `system3` queue:

- One **soft-deletes** carts older than `cart.lifetime` (7 days) plus carts already converted to orders.
- One **hard-deletes** the soft-deleted rows and cascades child cart-item / option / bundle / cross-sell / storage rows.

Both run on the platform's scheduler — not exposed in the admin UI, not tunable by the merchant.

## Where it appears

- [[orders-abandoned]] — lists carts that have entered the Abandoned state.
- [[settings-cart]] — sets the abandoned threshold (the five fixed options).
- [[analytics-abandoned-carts]] — counts abandoned vs recovered carts over time.
- [[orders]] — the placed Orders that converted carts produced.
- [[cart-vs-order-lifecycle]] — the cart-state-machine and the order-state-machine side by side.

## Related

- [[cart]] — hub.
- [[order]] — the record a converted cart produces; keeps `cart_id` for audit.
- [[customer]] — hard-deleting a customer cascade-deletes their carts.
- [[orders-abandoned]] — the abandoned-cart working surface.
- [[abandoned-cart-recovery]] — the recovery pipeline that acts on abandoned carts.
- [[cart-vs-order-lifecycle]] — the full cart vs order state distinction.

## Open Questions

None.
