---
type: concept
nav_path: "Concept → Checkout flow → Cart entity"
aliases: ["Cart entity lifecycle", "Cart cookie", "Guest cart session", "ccchc cookie", "Cart auto-touch", "Cart TTL", "Cart cleanup", "Merge cart on login"]
tags: [orders, checkout, cart, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[checkout-flow]]. See the hub for the other aspects (abandoned detection, submit-to-order, guest vs registered, lifecycle overview, discounts & rules, events & webhooks).

# Checkout flow — Cart entity

## Definition

The **Cart entity** is the database row that backs the customer's basket during the pre-order phase of [[checkout-flow]]. It is created on the first **Add to cart** click, mutated by every subsequent change, and either snapshotted into an [[order|Order]] at submit or soft-deleted by a maintenance job after a TTL window. The Cart's `updated_at` is the **single timestamp** that drives abandoned-cart eligibility, session "alive" detection, and cleanup pacing.

## Scope

Covered:

- Cart creation on first add (guest vs registered binding).
- How a guest's cart is found (the store session) and what the `ccchc` cookie is.
- Cart auto-touch on revisit (`cart.autoupdate`).
- Cart row TTL (`cart.lifetime` = 7 days) + post-conversion cleanup on the `system3` queue.
- The **Merge cart on login** (`merge_cart`) setting that decides whether an anonymous cart's lines fold into the logged-in cart at sign-in.

Not covered here:

- When the cart is considered abandoned + the recovery flow — see [[checkout-flow-abandoned-detection]].
- What runs when the customer submits the cart — see [[checkout-flow-submit-order-creation]].
- What differs for guest vs registered customers — see [[checkout-flow-guest-vs-registered]].

## Contrasts

- **Guest cart vs registered cart** — a guest's cart is bound to the store session (the `_ccs` cookie); a registered customer's cart is bound to the account, so it is found again at the next sign-in, on any device.
- **Session lifetime vs row TTL** — the session ends after 7 days without a visit, so a guest returning later gets a new, empty cart; the cart row is soft-deleted once it is 7 days past its last change. Abandoned-cart recovery reaches the row through its restore link, not through the session.
- **Auto-touch (10 min) vs abandoned threshold (60 min default)** — the cart's `updated_at` is silently refreshed when the customer revisits the storefront more than 10 minutes after the last touch (`cart.autoupdate` config). The abandoned-cart timer measures **session inactivity**, not raw cart stillness.

## Where it applies

- **First add-to-cart** — storefront creates the Cart row (associated with the session for guests, with the Customer ID for logged-in customers). Every subsequent additions / removes / edits update the same Cart row and refresh `updated_at`.
- **Sign-in mid-session** — if **Merge cart on login** (`merge_cart`) is ON in [[settings-cart]], the platform merges the anonymous cart's lines into the persistent logged-in cart at sign-in. When OFF, the anonymous cart is dropped.
- **Revisit > 10 minutes since last touch** — `cart.autoupdate` refreshes `updated_at` silently; the abandoned-cart clock resets even without touching the cart UI. A homepage reload at the 55-minute mark resets the timer.
- **Maintenance sweep on `system3` queue** — applies two cleanup passes:
  - Soft-delete carts whose `updated_at` is older than **7 days** (`cart.lifetime` config) — captures dead anonymous sessions that never produced an order.
  - Soft-delete carts that already have an Order pointing to them via `orders.cart_id` — converted carts are no longer needed.
- **Hard-delete pass** — a separate hourly job on `system3` permanently deletes every soft-deleted cart and its child rows (cart items, options, shipping quotes, bundles, cross-sells, item-storage entries). The 7-day sweep makes no exception for signed-in customers' carts.

### Cookie summary

| Cookie | What it does | Lifetime |
|---|---|---|
| `_ccs` (store session) | Holds the guest's cart key; this is what finds a guest's cart. | 7 days, renewed on every visit |
| `ccchc` | A fingerprint of the cart's contents, set when the cart changes; the checkout compares it to notice a change made in another tab. It does **not** point to the cart. | 60 days |

There is no `_cart_key` cookie. Full list: [[apps-gdpr-cookies-platform-cookies]].

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-abandoned-detection]] — what happens once `updated_at` crosses the abandoned threshold.
- [[checkout-flow-submit-order-creation]] — the cart-to-order snapshot that ends this entity's active life.
- [[cart]] — Cart entity reference.
- [[cart-vs-order-lifecycle]] — entity-by-entity state breakdown.
- [[settings-cart]] — `merge_cart` toggle + cart-cookie configuration.
- [[storefront-known-issues]] — items 10 & 11 describe the merge-on-login and guest-cart expiry from the merchant's perspective.

## Open Questions

None.
