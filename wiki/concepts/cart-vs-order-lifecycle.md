---
type: concept
nav_path: "Concept → Cart vs order lifecycle"
route_name: ""
route_path: ""
aliases: ["Cart vs order lifecycle", "Cart lifecycle", "Order lifecycle", "Cart vs Order", "Cart to order transition", "Cart states", "Order states", "Abandoned vs lost", "Жизнен цикъл на количка", "Жизнен цикъл на поръчка", "Количка срещу поръчка"]
tags: [orders, cart, lifecycle, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 10
---

# Cart vs order lifecycle

## Definition

A **[[cart|Cart]]** and an **[[order|Order]]** are two distinct entities with overlapping content (line items, customer info, prices) but completely different lifecycles, mutability rules, and merchant-side surfaces. Understanding which one is in play at any moment is the foundation for answering "where is my customer in the purchase journey?" — and for explaining why certain things (discount usage counters, stock decrement, transactional emails, invoice issuance) happen at one specific moment and not earlier or later.

A **Cart** is the **pre-purchase, in-progress** record. It exists from the first Add-to-cart, lives in the customer's browser session (persisted with a session token / customer ID), and is fully mutable until checkout submit.

An **Order** is the **post-purchase, finalised** record. It has a `status` field (default `pending`) that drives a defined workflow, appears in [[orders]], can generate invoices and credit notes, and its mutability is gated by status.

The transition happens at **exactly one point** — the customer's click on **Place order**. At that click the cart's data is **snapshotted** into a new Order (see [[cart-to-order-handoff]]). Before the click only a Cart exists; after it the Cart still exists but is no longer modifiable (it stays linked to the order for audit / abandoned-cart attribution). A Cart unused past the **abandoned threshold** (default 60 min) becomes eligible for the abandoned-cart recovery flow.

## Sub-pages (in this cluster)

This concept is split into 5 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[cart-state-machine]] — Cart entity data shape; the six cart states (Active / Abandoned / Recovered / Converted / Lost / Soft-deleted); identity states (anonymous / UUID-tracked / subscriber / logged-in); 10-min auto-touch; 7-day TTL; login cart-merge; `cart.*` webhooks.
- [[order-state-machine]] — the 11 canonical order statuses + fulfillment status + `is_draft` meta-flag; status-gated mutability table; custom-status slugification; 7-min lock-on-edit; `notify_customer` suppression; hard-delete + `order.*` webhooks.
- [[cart-to-order-handoff]] — the Place-order snapshot pipeline (validation → discount re-eval → child rows → currency / locale freeze → stock decrement → `OrderCreated` → redirect); the cart-vs-order data-shape diff; address snapshot; draft commit; banned-IP auto-cancel.
- [[cart-abandonment]] — the 7 eligibility rules; `abandoned_remainder_interval` (default 60 min); 3-min sweep cadence; per-period `abandoned_notification` plan quota; the Lost end-state.
- [[cart-restore]] — restore-link click handler; cart `key` validation; `restore_source` attribution; the `abandoned = 1` order flag set ONLY by this handler (not retroactively).

## Why it matters to the merchant

Cart vs Order is the **dividing line for most things merchants care about** — when stock comes off, when the customer gets emailed, when the discount counter increments, when invoices can issue, when refunds are possible. Common confusions, by aspect:

- **"Customer added it to cart but no order in [[orders]]."** — Customer is still in Cart state; the cart shows in [[orders-abandoned]] only after the abandonment threshold. See [[cart-state-machine]].
- **"Stock didn't go down on Add-to-cart."** — Correct. Decrement is tied to ORDER status, not cart state — see [[inventory-tracking]].
- **"Discount counter shows 5 but I had 7 orders."** — Usage increments only on orders in counted statuses (default `paid` / `completed` / `fulfilled`). Carts NEVER count. See [[discount-stacking]] + [[order-state-machine]].
- **"Order currency differs from store currency."** — Currency is **frozen at order creation**. See [[cart-to-order-handoff]].
- **"Cart shows the discount but order doesn't."** — Discounts re-evaluate at submit. See [[cart-to-order-handoff]].
- **"Abandoned cart email didn't fire."** — Cart must meet all 7 eligibility rules. See [[cart-abandonment]].

## Scope

What this concept covers (across the 5 aspect pages listed above): the Cart entity and its states, the Order entity and its statuses, the Place-order transition point, status-gated mutability, the abandoned-cart pipeline, address / currency / locale snapshot on the Order, per-order notification suppression and lock-on-edit, admin-side draft orders ([[orders-add]] with `is_draft = 1`) that bypass the cart, and cart-side / order-side webhook events.

What it does NOT cover:

- Full state-machine of order statuses (which transitions are allowed when, what events fire on each) — see [[order-status-workflow]].
- The detailed cross-entity journey from Add-to-cart to confirmation — see [[checkout-flow]].
- Payment-status mechanics (the money lifecycle, independent of order status) — see [[payment-status]].
- Discount interaction rules (stacking, code suppression) — see [[discount-stacking]].
- Stock decrement timing details — see [[inventory-tracking]] for the `paid` vs `pending` matrix.
- Notification delivery details (email queue, retry profile, webhook delivery) — see [[notification-delivery]].

## Contrasts

- **Cart vs Order**: Cart is pre-purchase, fully mutable, customer-side. Order is post-purchase, status-gated, merchant-side. The transition is the customer's click on Place order — irreversible. See [[cart-state-machine]] + [[order-state-machine]].
- **Cart vs [[cart-rule|Cart Rule]]**: a Cart is the entity holding the customer's selection. A Cart Rule is a marketing rule that fires AFTER discounts at submit.
- **Abandoned vs Lost**: an Abandoned cart crossed the threshold AND has identifiable customer / subscriber — eligible for recovery. A Lost cart aged out without conversion. See [[cart-abandonment]].
- **Cart conversion vs Cart recovery**: Conversion = normal place-order flow. Recovery = customer clicked a restore link, producing an order with `abandoned = 1` + `restore_source`. See [[cart-restore]].
- **Order draft vs Order pending**: a Draft order ([[orders-add]] with `is_draft = 1`) is invisible to the customer, doesn't fire emails, doesn't decrement stock. See [[order-state-machine]].

## Where it applies

The Cart vs Order distinction surfaces across the admin panel — the abandoned-cart screen, the orders list, the order detail hub, settings around timing and counts, and the underlying webhooks. Each aspect page documents its own application surface. The cross-cutting admin / settings / event surfaces:

- **Cart-side admin** — [[orders-abandoned]] (abandoned list + Send restore link / Delete bulk actions), [[analytics-abandoned-carts]], [[analytics-abandoned-checkout]], [[settings-cart]] (`abandoned_remainder_interval`, `merge_cart`, cart caps, decrement timing).
- **Order-side admin** — [[orders]] (placed-orders list), [[orders-details]] (per-order edit hub), [[orders-status-change]], [[orders-history]], [[orders-add]] (admin manual creation), [[orders-archive]], [[orders-customer-change]], [[orders-address-edit]], [[orders-notify-customer]], [[orders-invoice]] / [[orders-credit]] / [[orders-receipt]], [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] / [[orders-payment-manual]].
- **Settings + webhooks** — [[settings-statuses]] (status taxonomy + counted-statuses for discount usage), [[settings-hooks]] (`cart.*` and `order.*` subscriptions), [[settings-banned-ip]] (offline-payment auto-cancel).
- **Storefront events** — the storefront emits ecommerce events to whichever tag / pixel / analytics systems the merchant has installed (see [[apps-google-analytics]], [[apps-tiktok-pixel]], [[apps-google-tags]], [[apps-datalayer]]). The `purchase` / `CompletePayment` event fires ONCE per order — a `js_events` meta flag suppresses re-firing on thank-you-page reloads.

## Related

- [[cart]] — Cart entity.
- [[order]] — Order entity.
- [[checkout-flow]] — cross-entity journey (cart → order).
- [[order-status-workflow]] — post-order status state-machine.
- [[order-processing-pipeline]] — end-to-end side-effects fired at each order lifecycle event.
- [[customer]] — Customer entity; per-customer locale.
- [[discount]] — discount records; usage counter increments on counted-status orders.
- [[discount-stacking]] — multiple discount interaction at submit.
- [[cart-rule]] — Cart Rules; run AFTER discounts at submit.
- [[inventory-tracking]] — stock decrement / re-credit on status transitions.
- [[multi-currency]] — currency freeze on the order.
- [[multi-language]] — locale freeze on the order.
- [[notification-delivery]] — transactional emails + webhooks per transition.
- [[subscriber-vs-customer]] — UUID-tracked anonymous visitors vs subscribers vs customers.
- [[abandoned-cart-recovery]] — the cross-cutting recovery concept page.
- [[plan-gates]] — `abandoned_notification` quota, `orders_amount` / `orders_revenue` plan caps.

## Open Questions

No outstanding questions — all previously-flagged items resolved or distributed to sub-pages.
