---
type: entity
nav_path: "Entity → Cart → Data model"
aliases: ["Cart data model", "Cart attributes", "Cart token", "Cart line items", "Cart step", "ccchc cookie", "Cart fingerprint", "Cart device", "Структура на количка"]
tags: [entity, orders, cart, checkout, core]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[cart]]. See the hub for the other aspects (lifecycle, stock & pricing, recovery, merge).

# Cart — Data model

## Identity

This page describes **what a Cart stores** — the data shape of the pre-purchase record. A Cart bundles the customer's selected line items with their quantities and options, the addresses and checkout selections the customer has made so far, the currency and locale inherited from the storefront session, the running totals, and a set of internal markers (device, checkout step, content fingerprint, abandonment / recovery flags) that drive cleanup, analytics, and resume-checkout behaviour. Everything here is **mutable** while the customer browses — the cart is frozen into an immutable [[order|Order]] only at Place-order time (see [[cart-vs-order-lifecycle]]).

The cart can belong to a registered [[customer|Customer]] (`customer_id` / `user_id` set) or be an anonymous **guest cart** identified only by its session token.

## Aliases

- **Cart token** / **cart key** — the session identifier tying a guest cart to its browser.
- **Line item** — one cart-item row per (product / variant) added.
- **`ccchc` cookie** — the cart-content fingerprint cookie (an MD5 content hash, NOT the cart key).
- **`step`** — the last checkout step the customer reached.
- **`device`** — `desktop` or `mobile`, auto-detected at cart creation.

## Key Attributes

| Attribute | What it stores | Notes |
|-----------|----------------|-------|
| **Cart token** | Anonymous identifier | The session token that ties a guest cart to its browser session. Persists across page loads via cookie. |
| **Customer association** (`customer_id` / `user_id`) | Optional FK → [[customer]] | NULL for guest carts; set when the customer is logged in. A logged-out cart that the customer then logs into can be merged — see [[cart-entity-merge]]. |
| **Customer email** | Email captured at checkout | Optional — captured when the customer enters their email on the checkout email step (even before they finish). Used for abandoned-cart recovery on identifiable email subscribers — see [[cart-entity-recovery]]. |
| **Line items** | One row per product/variant | Each line carries the variant ID, quantity, price snapshot, options, and any per-line discount. Stock is NOT decremented while items sit in cart — only on order placement (see [[cart-entity-stock-pricing]]). |
| **Shipping address** | The address selected at checkout | Captured from the customer's chosen address (default or new). Editable by the customer until order placement. |
| **Billing address** | The billing address selected at checkout | Optional depending on the store's billing-address-required setting on [[settings-cart]]. |
| **Shipping method** + **shipping provider** | Couriers selected at the shipping step | Auto-selected if "automatically choose shipping if there's only one option" is on (per [[settings-cart]]). |
| **Payment provider** | Provider chosen at the payment step | Default provider auto-selects per [[settings-cart]]. A selection only — no money moves (see [[cart-entity-stock-pricing]]). |
| **Currency** | ISO currency code from the storefront session | Mirrors the storefront's current currency. **Frozen onto the resulting Order at submit time.** See [[cart-entity-stock-pricing]]. |
| **Locale** | Language code from the storefront session | The storefront language the customer is browsing in. Frozen onto the resulting Order at submit. |
| **Applied discounts** | Discount records attached to the cart | Re-evaluated on every cart read — see [[cart-entity-stock-pricing]]. |
| **Subtotal / total** | Computed from line items + discounts + shipping + tax | Live-recomputed; not stored as immutable until the order is created. |
| **`updated_at`** | Last-modified timestamp | The platform compares this to the abandonment threshold to decide whether the cart is "abandoned" — see [[cart-entity-lifecycle]]. |
| **Recovery flags** (`date_sent`, `abandoned_message_sent`, `source`, restore-link token) | Abandoned-cart recovery markers | Set when the recovery flow reaches the cart — full semantics on [[cart-entity-recovery]]. |
| **Device** (`device`) | `desktop` or `mobile` | Auto-detected from the user-agent at cart creation. Drives device-segmentation analytics. **Never re-evaluated** — a cart created on mobile stays `device = mobile` even if the customer later resumes on desktop. |
| **Step** (`step`) | Checkout step the customer last reached | One of `authorize`, `shippingAddress`, `billingAddress`. Reset to `authorize` on changes that invalidate shipping — see [[cart-entity-merge]]. Used internally to resume checkout after browser close. |
| **Hash check** (`hash_check`, derived) | MD5 of cart-item contents | Surfaces as the `ccchc` cookie (cart fingerprint) so the storefront can detect cart-content changes between page loads. NOT the cart key — this is a content hash that changes whenever items change. |
| **Auto-touch timer** | Internal | The cart's `updated_at` is silently refreshed on every page load if the cart was last touched >10 minutes ago. This means the abandoned timer measures session inactivity, not strict cart-content-stillness — see [[cart-entity-lifecycle]]. |

## Where it appears

- [[settings-cart]] — default payment / shipping selection, billing-address requirement, cart-UI behaviour, decrement-trigger status.
- [[orders-abandoned]] — the abandoned-cart list reads cart token, customer email, line items, and `updated_at`.
- [[storefront-cart]] — the storefront cart drawer / page that renders these attributes for the customer.
- [[checkout-flow]] — the flow that populates addresses, shipping / payment selections, and advances `step`.
- [[analytics-abandoned-carts]] — device segmentation reads the `device` attribute.

## Related

- [[cart]] — hub.
- [[order]] — the immutable record the cart's attributes are snapshotted into at submit.
- [[customer]] — owner of a registered cart (`customer_id`).
- [[product]] / [[variant]] — referenced per line item.
- [[discount]] — applied-discount records on the cart.
- [[payment-provider]] / [[shipping-provider]] — selected at the corresponding checkout step.
- [[cart-vs-order-lifecycle]] — why the attributes are mutable on the cart and frozen on the order.

## Open Questions

None.
