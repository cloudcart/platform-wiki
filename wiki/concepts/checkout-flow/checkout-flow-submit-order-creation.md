---
type: concept
nav_path: "Concept → Checkout flow → Submit → Order creation"
aliases: ["Place order pipeline", "Cart to order snapshot", "Order creation steps", "PreOrderCreated", "OrderCreated", "guest_to_customer", "Currency lock", "Locale lock", "Unit system lock", "Source attribution"]
tags: [orders, checkout, submit, order-creation, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[checkout-flow]]. See the hub for the other aspects (cart entity, abandoned detection, guest vs registered, lifecycle overview, discounts & rules, events & webhooks).

# Checkout flow — Submit → Order creation

## Definition

This aspect documents what runs when the customer clicks **Place order** on the storefront checkout page — the moment a Cart row is snapshotted into an Order row and the customer hands off to the payment provider. The pipeline is deterministic: final validation → discount/rule re-evaluation → Order row + child rows persisted (initial `status = pending`, `status_fulfillment = not_fulfilled`) → optional guest-to-customer promotion → payment record + redirect → conditional stock decrement → `OrderCreated` event fans out.

## Scope

Covered:

- The 8-step submit pipeline, in order.
- The `PreOrderCreated` listener that runs guest-to-customer conversion when `setting('guest_to_customer')` is ON.
- The three immutable-from-store fields snapshotted at create time: `currency`, `locale`, `unit_system`.
- Source / attribution capture (`cart_id`, `campaign_id`, `campaign_action_id`, `subscriber_id`, `customer_ip`, `customer_geoip`).
- The customer's order-confirmation URL (`/orders/<id>?hash=<increment_hash>`).

Not covered here:

- The guest-vs-registered behaviour matrix — see [[checkout-flow-guest-vs-registered]].
- The `OrderCreated` event's fan-out (queues, webhooks, emails) — see [[checkout-flow-events-and-webhooks]].
- The post-creation order lifecycle (pending → paid → completed) — see [[checkout-flow-order-lifecycle-overview]] + [[order-status-workflow]].
- Discount + Cart Rule mechanics during submit — see [[checkout-flow-discounts-and-rules]].

## Contrasts

- **Submit pipeline vs draft-order creation** — when the merchant creates an order from [[orders-add]], no Cart exists, the order is `is_draft = 1` until **Create order** is clicked, and stock is NOT decremented during draft. The `OrderCreated` event fires only at draft-to-live conversion — see [[checkout-flow-events-and-webhooks]] for the gating.
- **Storefront submit vs payment-provider return** — submit creates the order in `pending` and sends the customer to the provider; the **return** URL (`/orders/<id>?hash=<increment_hash>`) is a separate request that renders the confirmation page. Refreshing the return page does NOT re-charge — the `payment_hash` is single-use + already-completed at that point.
- **Currency / locale / unit_system locked at create vs store-level edit** — these three fields are stamped onto the order at create time ONLY if not already set, and nothing in the normal order flow changes them afterwards. The one exception is the BGN→EUR migration: the **Convert prices to EUR** button on [[orders-details]] permanently rewrites the order's amounts at the fixed rate and sets its currency to EUR. It is a one-way action, and it is refused once the order has an invoice number — see [[orders-details-actions]].

## Where it applies

### The submit pipeline (verbatim from backend)

When the customer hits **Place order** on the checkout page:

1. **Final validation** runs — required fields filled, cart amount ≥ `cart.min_amount` and ≤ `cart.max_amount`, per-product quantity ≤ `cart.max_quantity_per_product`, total quantity ≤ `cart.max_quantity_total`.
2. **Discount re-evaluation** — all matching discounts ([[discount]]) re-attach to the cart against the final state. See [[checkout-flow-discounts-and-rules]].
3. **Cart Rules re-evaluation** — Cart Rules ([[cart-rule]]) fire AFTER discounts on the post-discount cart total. See [[checkout-flow-discounts-and-rules]].
4. **Order row is created** — the Cart's lines are snapshotted into Order + Order Products + Order Discounts + Order Addresses + Order Payment rows. The order's initial `status` is `pending` and `status_fulfillment` is `not_fulfilled`. The `currency` and `locale` are locked at this moment and never change afterward (so historical invoices stay correct even if the store later switches currency or language).
5. **Customer linkage** — for registered checkout, `customer_id` is set to the logged-in customer. For guest checkout, `customer_id` is null but `customer_email` / `customer_first_name` / `customer_last_name` are still captured. If the **Convert guests into members** setting is ON, a customer account is also created and a generated password is emailed. See [[checkout-flow-guest-vs-registered]].
6. **Payment record** — a payment row is attached to the order, initially in `initiated` status. The customer is redirected to the payment provider (or, for offline methods, sees the *Thank you / awaiting payment* page).
7. **Stock decrement** — whether stock decrements at order creation or only on payment confirmation depends on the **Reduce items on Paid order** setting (`order_status_for_quantity_decrease`) on [[settings-cart]]: when set to `paid` (default), only `paid` / `authorized` / `completed` orders decrement; when set to `pending`, `pending` orders also decrement immediately. See [[inventory-decrement-timing]] for the full matrix.
8. **`OrderCreated` event fires** — the event bus fans out to: the order-confirmation email job, the per-order analytics job (`analytics2` queue, 60s delay), the merchant's `order.created` webhooks ([[settings-hooks]]), and any app-specific listeners. See [[checkout-flow-events-and-webhooks]] + [[notification-delivery]].

### Pre-order event runs guest-to-customer conversion

When `setting('guest_to_customer')` is ON and the cart belongs to a guest customer (not a registered one) at submit time, the `PreOrderCreated` event listener runs the guest-to-customer conversion — flipping the guest row into a real Customer row, marketing-consent flag preserved, generated password emailed for first login. This happens **before** the order row is persisted, so the resulting order is born linked to the freshly-promoted Customer record (no separate "convert later" workflow needed). (verify event name + setting key)

### Order creation snapshots `unit_system` from store, not cart

Three fields are snapshotted onto the new order at create time from the **store settings** rather than the cart:

| Field | Source | Notes |
|---|---|---|
| `currency` | `site('currency')` | Immutable, except for the one-way BGN → EUR conversion on [[orders-details]] (blocked once the order is invoiced). |
| `locale` | `site('language')` | Immutable. |
| `unit_system` | `site('unit_system')` | `metric` or `imperial`. Immutable — guarantees weight-based shipping stays correct after a store-level unit-system change. |

These are stamped onto the order at create time only if the order doesn't already have them set. After create, all three are immutable for the order's lifetime. (verify field origins)

### Source / attribution capture

The new order captures:

- `cart_id` — the originating cart row.
- `campaign_id` / `campaign_action_id` — the marketing campaign + action that drove the order, if attribution data was set in the visitor's session (cookie / UTM).
- `subscriber_id` — the newsletter subscriber row, if the customer was on a subscribed list.
- `customer_ip` + `customer_geoip` — for fraud investigation + banned-IP matching ([[settings-banned-ip]]).

These fields feed the source-of-sales analytics dashboards ([[analytics-orders-by-social-source]] / [[analytics-sales-by-traffic-source]]).

### Customer's view of the placed order

The customer-facing order-confirmation page is reachable at `/orders/<id>?hash=<increment_hash>` (the `increment_hash` is a secret token on each order — anyone with the link can view the order without authentication). This is the same link used in the order-confirmation email and in payment-provider redirect URLs.

The customer can also view their order from their account area if they're a registered customer (or were converted from guest in step 5).

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-cart-entity]] — the cart row this pipeline reads from.
- [[checkout-flow-guest-vs-registered]] — what differs at step 5.
- [[checkout-flow-discounts-and-rules]] — what runs at steps 2-3.
- [[checkout-flow-order-lifecycle-overview]] — what happens to the order AFTER `pending`.
- [[checkout-flow-events-and-webhooks]] — what fans out at step 8.
- [[inventory-decrement-timing]] — full decrement matrix for step 7.
- [[order-processing-pipeline]] — the post-submit pipeline this hands off to.
- [[settings-cart]] — `cart.min_amount` / `cart.max_amount` / `cart.max_quantity_*` / `order_status_for_quantity_decrease` / `guest_to_customer` settings.
- [[settings-banned-ip]] — IP filter that runs against `customer_ip`.
- [[orders-details]] — the merchant's per-order view after submit.
- [[orders-add]] — admin-side draft-order alternative entry.

## Open Questions

- Confirm `PreOrderCreated` is the exact event name + `guest_to_customer` is the exact setting key (verify).
- Confirm `currency` / `locale` / `unit_system` get their store-level defaults at order-create time (verify field origins).
