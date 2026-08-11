---
type: entity
nav_path: "Entity → Cart → Stock & pricing"
aliases: ["Cart stock", "Cart never reserves stock", "Cart currency", "Cart discounts re-evaluate", "Cart payment selection", "Cart caps", "Minimum order amount", "Maximum order amount", "Наличност в количка", "Лимити на количка"]
tags: [entity, orders, cart, checkout, inventory, pricing, discounts]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[cart]]. See the hub for the other aspects (data model, lifecycle, recovery, merge).

# Cart — Stock & pricing behaviour

## Identity

This page covers how a Cart behaves around **stock, currency, discounts, payment, and content caps** — the live, recompute-on-read rules that distinguish a mutable cart from the frozen [[order|Order]] it becomes. The defining principle: nothing on a cart is committed. Stock is not reserved, money is not moved, currency tracks the storefront, and discounts re-attach or drop off on every read — until the Place-order click freezes the picture onto an Order.

## Aliases

- **No stock reservation** — a cart never holds inventory.
- **Currency follows storefront** — until submit.
- **Discount re-evaluation** — applied discounts re-checked on every cart read.
- **Cart caps** — minimum / maximum order amount, max products of a kind, max total quantity (from [[settings-cart]]).

## Key Attributes

### Stock is never reserved by a cart

A cart can hold any quantity of any in-stock variant without affecting the product's `quantity`. Stock decrements only when the cart converts to an Order AND the Order reaches the decrement-trigger status (per [[settings-cart]] `order_status_for_quantity_decrease` — `pending` decrements immediately at order placement, `paid` decrements only on cleared payment). This means two customers can have the same last unit in their carts; the first to submit wins, the second sees an out-of-stock error at checkout. The full decrement-timing matrix lives on [[inventory-decrement-timing]].

### Currency and locale move with the storefront until submit

A cart's currency mirrors the storefront's current currency — if the customer switches currency mid-cart, the cart's currency follows. The same applies to language (locale). At order submit, the cart's current currency + locale are **frozen** onto the resulting Order and stay there for the lifetime of the Order. Existing orders are never re-priced if the store later changes its default currency.

### Discounts re-evaluate on every cart read

When the customer revisits the cart or moves between checkout steps, the platform re-evaluates every applied discount against the current cart contents:

- Discounts that have expired (`active_to` past), hit their usage cap, or no longer match conditions (e.g., the customer removed a qualifying product) **drop off**.
- New auto-applying discounts (e.g., a Global percent-off whose `cart_min_price` is now satisfied) **attach**.

The customer's order at submit captures exactly the discounts that are ACTIVE at submit time — not what was displayed during a session 10 minutes earlier.

### Cart can hold a payment selection without authorising it

The customer's chosen payment provider sits on the cart as a SELECTION only — no money moves, no auth, no token is created. Authorisation and capture happen during the checkout submit + post-submit redirect dance. A cart in `pending payment` state at the gateway is already a converted Order, not a cart.

### Hard-cap rules from [[settings-cart]] enforce at the cart level

The merchant's cart-content limits — **minimum order amount**, **maximum order amount**, **max products of a kind**, **max total quantity** — are enforced when the customer tries to advance from cart to checkout. The cart can hold values that violate these caps (the customer added them), but advancing is blocked with the corresponding error message until the customer fixes the cart.

## Where it appears

- [[settings-cart]] — `order_status_for_quantity_decrease` (decrement trigger), the four cart caps, default payment selection.
- [[storefront-cart]] — where the customer sees the live totals, discount lines, and cap-violation errors.
- [[checkout-flow]] — re-evaluates discounts and enforces caps as the customer advances.
- [[inventory-decrement-timing]] — the deterministic decrement matrix the cart's no-reservation rule feeds into.
- [[discount]] — the discount records that attach / drop off on cart read.

## Related

- [[cart]] — hub.
- [[order]] — the frozen snapshot the cart's live values commit to at submit.
- [[discount]] — applied-discount re-evaluation.
- [[payment-provider]] — the selection-without-auth rule.
- [[inventory-tracking]] — the stock model the cart never reserves against.
- [[inventory-decrement-timing]] — when stock actually drops (post-conversion).
- [[cart-vs-order-lifecycle]] — stock decrement timing, discount usage counting, and currency lock at the cart→order boundary.

## Open Questions

- ⏸️ Whether the cart's currency switch mid-session is preserved when the customer abandons + recovers (does the restored cart open in the original currency or the storefront's current currency?).
