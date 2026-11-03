---
type: entity
nav_path: "Entity → Cart"
aliases: ["Cart", "Shopping cart", "Basket", "Pending cart", "Abandoned cart", "Количка", "Кошница", "Изоставена количка"]
tags: [entity, orders, cart, checkout, core]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Cart

## Identity

A **Cart** is the **pre-purchase, in-progress** record of what a customer is preparing to buy. It holds the customer's selected line items (with quantities, variants, options, and per-line discounts), the chosen shipping + billing address, the shipping method and payment provider picked at checkout, any applied discount codes, the currency, and the running totals — all mutable while the customer browses, edits, and walks through the checkout pages. The Cart can belong to a registered [[customer|Customer]] OR be a **guest cart** (anonymous, identified only by a session token / cart token). Carts exist from the moment the first product is added until the customer submits the order, abandons the cart, or it ages out and is cleaned up.

A Cart is distinct from an [[order|Order]]: the Cart is the customer's editable selection that lives on the storefront; the Order is the snapshotted, status-driven sale record that appears in the merchant's [[orders]] list. The transition happens at exactly one point — the customer's click on **Place order** at the end of [[checkout-flow|checkout]]. Before that click, only a Cart exists. After it, an Order exists; the Cart still exists in the database (referenced as the order's source via `cart_id`) but is no longer modifiable by the customer. See [[cart-vs-order-lifecycle]] for the full distinction.

Carts are NOT directly edited by the merchant from the admin — the admin's only interactions are: viewing **abandoned** carts on [[orders-abandoned]], sending restore links through [[abandoned-cart-recovery|cart recovery]], and configuring cart behaviour on [[settings-cart]]. To act on cart contents the merchant must wait for the customer to submit the order (then edit the resulting Order) or place an admin-side order manually via [[orders-add]].

This page is the **hub** for the Cart entity. The substantive content lives in 5 aspect pages — drill into the one that matches the question.

## Aliases

- **Cart** — the canonical merchant-facing term in the admin and storefront.
- **Shopping cart** / **Basket** — informal merchant phrasing; some storefront themes label the icon "Basket".
- **Pending cart** — used when distinguishing in-progress carts from carts already abandoned or converted.
- **Abandoned cart** — the same Cart entity once its `updated_at` has crossed the abandonment threshold; surfaces on [[orders-abandoned]].
- Bulgarian: **Количка** (standard), **Кошница** (older / theme-specific), **Изоставена количка** ("abandoned cart").

## Key Attributes

The substantive attribute detail lives across the aspect pages. This hub gives the top-level shape — drill in.

### Sub-pages (in this cluster)

- [[cart-entity-model]] — the data shape: cart token, customer association, line items, addresses, shipping / payment selection, currency, locale, device, `step`, the `ccchc` content-hash fingerprint, and the auto-touch timer.
- [[cart-entity-lifecycle]] — the six states (active → abandoned → recovered → converted → lost → hard-deleted), the time-based abandonment transition, the 7-day TTL, post-conversion soft-delete, and the two scheduled cleanup jobs.
- [[cart-entity-stock-pricing]] — why a cart never reserves stock, how currency / locale follow the storefront until submit, why discounts re-evaluate on every read, the payment-selection-without-auth rule, and how cart-content caps enforce.
- [[cart-entity-recovery]] — abandoned-cart recovery from the cart's perspective: recovery channel (`source`), restore-link token, the two-layer consent gate, guest-cart recoverability, recovered-order attribution, and the bulk-send plan quota.
- [[cart-entity-merge]] — merge-cart-on-login (sum quantities for same variant), the bot / crawler sentinel key, and the checkout `step` reset on cart-modifying operations.

### Top-level shape (orientation only)

| Aspect of the Cart | Lives on |
|--------------------|----------|
| What the cart stores (token, items, addresses, selections) | [[cart-entity-model]] |
| What state the cart is in + when it is cleaned up | [[cart-entity-lifecycle]] |
| Why stock isn't reserved + how pricing / discounts behave | [[cart-entity-stock-pricing]] |
| How an abandoned cart is recovered + attributed | [[cart-entity-recovery]] |
| What happens on login-merge / bot loads / cart edits | [[cart-entity-merge]] |

## Relationships

A Cart:

- **Belongs to one** [[customer|Customer]] (optional — guest carts are NULL).
- **Has many** cart-item rows — one per (product / variant) the customer added.
- **References** a [[product|Product]] (and specifically a [[variant|Variant]]) per line item.
- **References** a shipping method, a shipping provider, and a payment provider — the customer's checkout selections.
- **Has many** applied [[discount|Discounts]] (re-evaluated on every read — see [[cart-entity-stock-pricing]]).
- **Produces** zero-or-one [[order|Order]] when the customer clicks Place order. The resulting Order keeps a back-reference (`cart_id`) for audit and abandonment attribution.
- **Is the source for** [[abandoned-cart-recovery|abandoned-cart recovery]] — when `updated_at` crosses the threshold without an order being placed.

## Where it appears

- [[settings-cart]] — every cart behaviour setting: abandoned threshold, default payment / shipping selection, cart caps, decrement-trigger status, cart-UI behaviour, merge-on-login toggle.
- [[orders-abandoned]] — the abandoned-cart list; per-cart and bulk **Send restore link**; manual delete.
- [[abandoned-cart-recovery]] — the end-to-end recovery concept and the seven eligibility checks.
- [[orders]] — placed orders; the **Recovered source** filter surfaces orders that came through a restore link.
- [[orders-history]] — the per-order audit log shows the recovery banner when the order originated from a recovered cart.
- [[analytics-abandoned-carts]] — abandoned-cart trend dashboard (count abandoned, count recovered, recovery rate).
- [[analytics-abandoned-checkout]] — the funnel showing where customers exit before placing an order.
- [[orders-add]] — admin-side manual order creation; bypasses the cart entirely.

## Related

### Related entities

- [[order]] — every Order originates from a Cart (its `cart_id` back-reference). The Cart → Order conversion is the most important state transition in commerce.
- [[customer]] — registered carts belong to a customer; guest carts do not.
- [[subscriber]] — the recovery email respects per-channel Subscriber consent in addition to Customer-level consent.
- [[product]] / [[variant]] — cart line items reference variants under products.
- [[discount]] — discounts attach to carts and re-evaluate on every cart read.
- [[payment-provider]] / [[shipping-provider]] — selected on the cart at the corresponding checkout step.

### Cross-cutting concepts

- [[cart-vs-order-lifecycle]] — the dividing line between cart and order; the foundation for understanding stock decrement timing, discount usage counting, transactional emails, and invoice issuance.
- [[checkout-flow]] — the storefront flow that converts the cart into an order.
- [[abandoned-cart-recovery]] — the end-to-end recovery pipeline (eligibility, channels, timing, attribution).
- [[notification-delivery]] — how the two-layer consent gate (customer + subscriber channel) gates the recovery email.

## Open Questions

- ⏸️ Whether the cart's currency switch mid-session is preserved when the customer abandons + recovers (does the restored cart open in the original currency or the storefront's current currency?).
- ⏸️ The precise behavior when a guest cart's email matches an existing registered Customer record — is the cart auto-linked to the registered Customer at checkout, or kept as a guest cart?
