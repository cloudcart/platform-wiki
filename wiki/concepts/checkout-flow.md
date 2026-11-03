---
type: concept
nav_path: "Concept → Checkout flow"
route_name: ""
route_path: ""
aliases: ["Checkout flow", "Order placement flow", "Cart to order flow", "Customer purchase flow", "Checkout pipeline", "Покупка", "Поръчка", "Чекаут процес", "Завършване на поръчка"]
tags: [orders, checkout, cart, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 7
---

# Checkout flow

## Definition

The **checkout flow** is the end-to-end journey that converts a customer's open [[cart|Cart]] into a placed [[order|Order]]. It begins the moment the customer's browser session adds the first product to the cart, runs through shipping + payment selection, and ends at the order-confirmation page after the order is persisted, the customer is emailed, and webhooks have fired to the merchant's external systems.

Along the way, the cart accumulates totals (subtotal, taxes, shipping, discounts), discounts attach automatically as conditions match, Cart Rules fire AFTER discounts, and a Cart entity tracks every change. If the customer leaves before submitting, the cart is **abandoned**; the platform attempts recovery via the abandoned-cart pipeline and may eventually convert the cart back into an order if the customer returns through a recovery link. If the customer submits, the cart's data is snapshotted into a new Order row (`status = pending`), the payment provider takes over, and the order's lifecycle ([[order-status-workflow]]) begins.

The single most-important boundary: this concept covers everything **up to and including** order creation. What runs AFTER the order is placed (status-machine rules, full pipeline side-effects, payment money-lifecycle) lives in [[order-status-workflow]] + [[order-processing-pipeline]] + [[payment-status]]. The state-machine snapshot at the moment of creation is documented here; per-status transition rules are not.

## Sub-pages (in this cluster)

This concept is split into 8 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[checkout-flow-cart-entity]] — Cart row creation, the `ccchc` cookie (24h), auto-touch on revisit, 7-day TTL + cleanup, **Merge cart on login** behaviour.
- [[checkout-flow-abandoned-detection]] — `abandoned_remainder_interval` (60-min default), recovery email + Messenger, restore-link mechanics, the direct-resubmit edge case (`abandoned = 0`).
- [[checkout-flow-submit-order-creation]] — the 8-step submit pipeline, `PreOrderCreated` guest-to-customer conversion, immutable `currency` / `locale` / `unit_system` snapshot, source attribution, customer's confirmation URL.
- [[checkout-flow-guest-vs-registered]] — the behaviour matrix, **Customer accounts** (`registered` / `guests` / `both`), **Convert guests into members**, per-customer discount caps.
- [[checkout-flow-order-lifecycle-overview]] — initial `pending` / `not_fulfilled` state, positive flow + `order_complete` auto-promote, `authorized` step, seven negative-branch statuses, three payment-status lifecycle shapes.
- [[checkout-flow-discounts-and-rules]] — discounts attach during cart, snapshot at submit, Cart Rules run AFTER discounts (post-discount price input), `discounts_used_statuses` counted-status setting.
- [[checkout-flow-events-and-webhooks]] — `OrderCreated` chain, 4-stage `OrderStatusChange` / `PostOrderStatusChange` sequence, `order-events8` queue, per-status customer-email gating, `is_draft` early-return.
- [[checkout-flow-storefront-backend-bridge]] — DOM → endpoint → cart-attribute → reload-fragment map for every storefront submit on `/checkout`. The "what does this submit do on the server?" reference; companion to per-step storefront pages under [[checkout]].

## Scope

What this concept covers (across the 7 sub-pages):

- The **Cart → Order** transition: when a Cart entity is created, when it transitions to "active" / "abandoned" / "recovered" / "lost" / "converted".
- The order's initial status (`pending`) and the four-state positive lifecycle (`pending` → `paid` → `completed`, plus the optional `authorized` pre-auth state).
- The seven negative-branch statuses (`failed`, `cancelled`, `voided`, `timeouted`, `refunded`, `chargebacked`, `disputed`).
- Guest vs registered checkout differences.
- The three payment-status lifecycle shapes (direct charge / authorize-then-capture / manual offline).
- When discounts attach (during cart, fix at submit) and when Cart Rules run (after discounts).
- The transactional-email + webhook fan-out triggered at each transition.

What it does NOT cover:

- The storefront's HTML / Vue UI of the cart and checkout pages — frontend / theme topic.
- Payment-provider integration internals (Stripe, PayPal, Klarna, etc.) — see the individual `payment-providers-*` feature pages.
- Shipping calculation / courier integration — see [[shipping-calculation]] / [[shipping-provider]] / the individual `apps-*` shipping app pages.
- Tax computation — see [[tax-computation]].
- Merchant-facing admin order details / edit / refund actions — see [[orders-details]] / [[orders-payment-refund]] / [[orders-status-change]].
- Subscription / recurring orders — see [[orders-subscriptions]].

## Contrasts

- **Checkout flow vs order-status workflow** — checkout flow is what *happens* up to and including order creation. [[order-status-workflow]] is the state-machine that runs *after* the order is created. They overlap only at the moment of order creation.
- **Checkout flow vs abandoned-cart recovery** — the happy path is cart → submit → order. The abandoned-cart flow is the "recovery path" — see [[checkout-flow-abandoned-detection]]. Both end at the same place (an Order in `pending`), but the abandoned-recovery path also sets `abandoned = 1` and records a `restore_source`.
- **Checkout flow vs admin-side order creation** — when the merchant creates an order from [[orders-add]], they bypass the storefront checkout entirely — no cart exists, the order is `is_draft = 1` until **Create order** is clicked, and stock is NOT decremented during draft.
- **Checkout flow vs payment-status lifecycle** — the order's `status` answers *"where is this order in the workflow?"*. The order's `payment.status` answers *"where is the money?"*. An order can be `completed` while its payment is `refunded`. See [[payment-status]].
- **Checkout flow vs cart-vs-order lifecycle** — [[cart-vs-order-lifecycle]] is the dedicated entity-lifecycle page describing each entity's individual states. This concept describes the *journey across both entities*.

## Where it applies

### Storefront surfaces (customer-side)

- [[settings-cart]] — admin configuration of the checkout: account requirements, abandoned-cart timing, field requirements, cart-bubble behaviour, VAT validation, Google Maps integration.
- [[settings-statuses]] — order-status taxonomy (custom statuses). Note: a status carries only a name — there is no per-status notification toggle.
- [[settings-hooks]] — outbound webhooks (`order.*` / `cart.*`).

### Admin surfaces (merchant-side)

- [[orders]] — placed-orders list.
- [[orders-details]] — per-order edit hub.
- [[orders-abandoned]] — abandoned-cart list + recovery configuration.
- [[orders-add]] — admin-side manual order creation (bypasses storefront cart).
- [[orders-status-change]] — manual status transitions.
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] / [[orders-payment-manual]] — payment lifecycle actions.
- [[orders-history]] — per-order audit log.
- [[orders-notify-customer]] — per-order suppression of future status-change emails.

## Related

- [[cart]] — the entity that exists during the pre-order phase.
- [[order]] — the entity created by the flow.
- [[payment-status]] — money-lifecycle independent of order `status`.
- [[customer]] — registered vs guest checkout attaches differently.
- [[discount]] — discounts evaluated during the cart, applied at order creation.
- [[cart-rule]] — cart rules evaluated AFTER discounts.
- [[cart-vs-order-lifecycle]] — entity-by-entity state breakdown.
- [[order-status-workflow]] — what happens to the order after it's placed.
- [[order-processing-pipeline]] — the post-creation pipeline side-effects.
- [[discount-stacking]] — discount-vs-discount interaction rules.
- [[notification-delivery]] — how the order-confirmation email + webhooks dispatch.
- [[shipping-calculation]] — shipping rates computed during cart.
- [[shipping-calc-geo-gating]] — the checkout shipping-address **country restriction** (the *"we don't deliver to this country"* message, or a country missing from the dropdown).
- [[tax-computation]] — taxes computed during cart.
- [[order-totals-pipeline]] — the order-of-operations that produces the cart / checkout total.
- [[inventory-decrement-timing]] — `order_status_for_quantity_decrease` matrix referenced by the submit pipeline.
- [[marketing-discounts]] — discount catalogue + editor.
- [[apps-cart-rules]] — Cart Rule editor.
- [[plan-gates]] — `orders_amount` / `orders_revenue` / `abandoned_notification` quotas.
- [[storefront-known-issues]] — merchant-perspective gotchas around the cart cookie + merge-on-login.

## Open Questions

None at the hub level — all previously-flagged items distributed to sub-pages.
