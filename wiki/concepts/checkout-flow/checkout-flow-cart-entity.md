---
type: concept
nav_path: "Concept → Checkout flow → Cart entity"
aliases: ["Cart entity lifecycle", "Cart cookie", "ccchc cookie", "Cart auto-touch", "Cart TTL", "Cart cleanup", "Merge cart on login"]
tags: [orders, checkout, cart, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[checkout-flow]]. See the hub for the other aspects (abandoned detection, submit-to-order, guest vs registered, lifecycle overview, discounts & rules, events & webhooks).

# Checkout flow — Cart entity

## Definition

The **Cart entity** is the database row that backs the customer's basket during the pre-order phase of [[checkout-flow]]. It is created on the first **Add to cart** click, mutated by every subsequent change, and either snapshotted into an [[order|Order]] at submit or soft-deleted by a maintenance job after a TTL window. The Cart's `updated_at` is the **single timestamp** that drives abandoned-cart eligibility, session "alive" detection, and cleanup pacing.

## Scope

Covered:

- Cart creation on first add (guest vs registered binding).
- The `ccchc` cookie + its 24-hour sliding lifetime.
- Cart auto-touch on revisit (`cart.autoupdate`).
- Cart row TTL (`cart.lifetime` = 7 days) + post-conversion cleanup on the `system3` queue.
- The **Merge cart on login** (`merge_cart`) setting that decides whether an anonymous cart's lines fold into the logged-in cart at sign-in.

Not covered here:

- When the cart is considered abandoned + the recovery flow — see [[checkout-flow-abandoned-detection]].
- What runs when the customer submits the cart — see [[checkout-flow-submit-order-creation]].
- What differs for guest vs registered customers — see [[checkout-flow-guest-vs-registered]].

## Contrasts

- **Guest cart vs registered cart** — guest carts are bound to the `ccchc` cookie + session; registered carts are bound by `customer_id` (or `user_id`) and persist past cookie expiry. A logged-in customer who returns days later still sees their cart; a guest does not.
- **Cookie lifetime vs row TTL** — the `ccchc` cookie expires after 24 hours of inactivity (visitor gets a fresh cart in the browser); the underlying cart ROW survives for 7 days in the DB. So abandoned-cart recovery emails may still fire against rows the customer can no longer reach via cookie.
- **Auto-touch (10 min) vs abandoned threshold (60 min default)** — the cart's `updated_at` is silently refreshed when the customer revisits the storefront more than 10 minutes after the last touch (`cart.autoupdate` config). The abandoned-cart timer measures **session inactivity**, not raw cart stillness. (verify config key)

## Where it applies

- **First add-to-cart** — storefront creates the Cart row (associated with the session for guests, with the Customer ID for logged-in customers). Every subsequent additions / removes / edits update the same Cart row and refresh `updated_at`.
- **Sign-in mid-session** — if **Merge cart on login** (`merge_cart`) is ON in [[settings-cart]], the platform merges the anonymous cart's lines into the persistent logged-in cart at sign-in. When OFF, the anonymous cart is dropped.
- **Revisit > 10 minutes since last touch** — `cart.autoupdate` refreshes `updated_at` silently; the abandoned-cart clock resets even without touching the cart UI. A homepage reload at the 55-minute mark resets the timer. (verify)
- **Maintenance sweep on `system3` queue** — applies two cleanup passes:
  - Soft-delete carts whose `updated_at` is older than **7 days** (`cart.lifetime` config) — captures dead anonymous sessions that never produced an order.
  - Soft-delete carts that already have an Order pointing to them via `orders.cart_id` — converted carts are no longer needed.
- **Hard-delete pass** — runs after soft-delete; cascades child rows (cart items, options, shipping quotes, bundles, cross-sells, item-storage entries) for soft-deleted carts. Logged-in customers' carts persist by `user_id` even past TTL — the customer's cart is recovered on the next sign-in. (verify queue name)

### Cookie summary

| Property | Value | Notes |
|---|---|---|
| Cookie name | `ccchc` | Points to the visitor's cart row. |
| Lifetime | 24 hours | Sliding — refreshed on every cart interaction. |
| Post-expiry behaviour | Visitor gets a fresh cart | Underlying row still in DB; still recovery-email eligible. |
| Logged-in override | Cart persisted by Customer ID | Cookie age irrelevant. |

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-abandoned-detection]] — what happens once `updated_at` crosses the abandoned threshold.
- [[checkout-flow-submit-order-creation]] — the cart-to-order snapshot that ends this entity's active life.
- [[cart]] — Cart entity reference.
- [[cart-vs-order-lifecycle]] — entity-by-entity state breakdown.
- [[settings-cart]] — `merge_cart` toggle + cart-cookie configuration.
- [[storefront-known-issues]] — items 10 & 11 describe the merge-on-login + 24-hour cookie behaviours from the merchant's perspective.

## Open Questions

- Confirm the exact `cart.autoupdate` config key + default (10 minutes) (verify).
- Confirm `cart.lifetime` default = 7 days against current the platform code (verify).
- Confirm the soft-delete cleanup queue name is `system3` (verify).
