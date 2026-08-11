---
type: entity
nav_path: "Entity → Order"
aliases: ["Order", "Order record", "Sale", "Purchase", "Поръчка", "Продажба"]
tags: [orders, entity]
created: 2026-05-21
updated: 2026-08-06
source_count: 8
---

# Order

## Identity

An **Order** is the record of a customer's purchase intent at the store. It is the central commerce object — every sale the merchant ships, invoices, refunds, or analyses starts as an Order. Each Order snapshots, at the moment it was placed, the **customer** (name + email + IP + group), the **products** (line items with their quantities, prices, options, and any per-line discounts), the **addresses** (shipping + billing + courier office), the **payment** (provider + amount + provider reference), the **shipping** (courier + waybill + insurance + dates), the **totals** (subtotal + shipping + tax + discount + grand total), and the **state** (overall order status, payment status, fulfillment status, archive flag). Once placed, an Order moves through a lifecycle of status transitions driven by payment events from the gateway, shipping events from the courier, and direct merchant actions on [[orders-details]] — and it accumulates an [[orders-history|audit log]] of every change.

An Order is distinct from a **Cart** ([[cart]]): a cart is the customer's in-progress selection that lives only on the storefront and may convert to an Order at checkout — or be abandoned (see [[orders-abandoned]]). An Order is also distinct from an **Invoice** ([[invoice]]) and a **Credit note** ([[credit-note]]): those are accounting documents *issued against* an Order, not the Order itself. See [[cart-vs-order-lifecycle]] for the full distinction.

This page is the **hub** for the Order entity. The substantive content lives in 5 aspect pages — drill into the one that matches the question.

## Aliases

- "Order" — the canonical merchant-facing term in the UI, reports, and emails.
- "Order record" — used internally when distinguishing the persisted entity from the in-progress cart.
- "Sale" / "Purchase" — informal merchant language; "Top sales" reports and "Recent purchases" modules all surface Orders.
- Bulgarian: "Поръчка" (the standard label), "Продажба" (used in some analytics labels).
- Order numbers in the admin and emails are formatted as `#<id>` (e.g., `#12345`). The platform also stores a per-order `usn` (Unique Sale Number) used for store-specific identifiers (POS / external accounting) and an `increment_hash` used in the secure customer-facing order URL.

## Key Attributes

Five aspect pages own the substantive attribute detail. This hub gives the top-level shape — drill in.

### Sub-pages (in this cluster)

- [[order-entity-identifiers]] — the three identifiers (`id`, `usn`, `increment_hash`), the frozen-at-create snapshots (`currency`, `locale`, `unit_system`, `customer_geoip`, `customer_ip`), the customer-fields-as-snapshot rule, notes, and source attribution (`cart_id`, `campaign_id`, `manual`, `abandoned`).
- [[order-entity-lifecycle]] — the 11 canonical statuses (4 positive + 7 negative), `status_fulfillment` independence, the `is_draft` sub-state, the three `validateChangeStatus` guards, auto-promotion to `completed`, banned-IP auto-cancel, fulfillment-removal walk-back, archive status gating.
- [[order-entity-money]] — totals (`price_subtotal`, `price_products_subtotal`, `price_total`, `weight`, `vat_included`), payment records (zero-or-more with their own status), manual "Mark paid" semantics, invoice / credit / receipt issuance and numbering, currency lock at create time, discount uses-counter rule.
- [[order-entity-side-effects]] — `order.created` / `order.updated` / `order.deleted` webhook fan-out, `notify_customer` flag (and the digital-products exception), moderator lock (7 minutes via `lock_orders_time`, on Settings → General), archive as the only cleanup (orders are never deleted), address-edit as snapshot, open-ended meta-keys (`is_draft`, `is_admin`, `integration`, `restore_source`).
- [[order-entity-api-access]] — JSON-API v2 `/api/v2/orders` endpoint: read + limited mutation (PATCH `status` / `note_administrator` / `notify_customer`, POST/DELETE `order-fulfillment`), forbidden operations (POST order, DELETE order, payment actions), same-side-effects principle, `api2` acting namespace on history rows.

### Top-level shape (orientation only)

| Aspect of the Order | Lives on |
|---------------------|----------|
| Who placed it (customer snapshot) | [[order-entity-identifiers]] |
| Where in the workflow it is (`status`) | [[order-entity-lifecycle]] |
| Whether the package has gone out (`status_fulfillment`) | [[order-entity-lifecycle]] |
| Where the money is (payment records, accounting documents) | [[order-entity-money]] |
| What fires when something changes (webhooks, history, locks) | [[order-entity-side-effects]] |
| What integrations can do programmatically | [[order-entity-api-access]] |

The order also has **meta-data rows** (`order_meta`) keyed by string — used for `is_draft`, `is_confirmed`, `is_admin`, `integration` (courier brand), and app-specific extensions. The detailed meta-key catalogue lives on [[order-entity-side-effects]].

## Where it appears

- [[orders]] — the master list view. The canonical merchant working surface.
- [[orders-details]] — the per-order edit hub; ~40 sub-actions operate on a single order.
- [[orders-add]] — admin-side manual order creation (creates an Order with `is_draft = 1`).
- [[orders-archive]] — archive / unarchive.
- [[orders-history]] — per-order audit log of every change.
- [[orders-status-change]] — change the order status (bulk + single).
- [[orders-customer-change]] — re-associate the order with a different customer.
- [[orders-address-edit]] — edit shipping / billing address on this specific order (snapshot edit, not propagated to the customer profile).
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] / [[orders-payment-manual]] — payment lifecycle actions.
- [[orders-products]] / [[orders-ordered-products]] — line-item management on the order.
- [[orders-discount-add]] — add an order-level discount.
- [[orders-shipping-waybill]] — generate / re-issue the courier waybill.
- [[orders-invoice]] / [[orders-invoices]] / [[orders-invoices-download]] / [[orders-invoices-export]] — invoice issuance and exports.
- [[orders-credit]] — credit-note flow against the order.
- [[orders-receipt]] — cash receipt issuance.
- [[orders-export]] / [[orders-ordered-products-export]] — bulk export.
- [[orders-notify-customer]] — toggle future-notification suppression.
- [[orders-abandoned]] — abandoned-cart recovery (creates orders via the recovery flow).
- [[orders-subscriptions]] — recurring orders.
- [[customers-details-orders]] — per-customer order list (same data, different filter).
- [[analytics-orders-by-country]] / [[analytics-orders-by-social-source]] / [[analytics-percentage-of-orders]] / [[analytics-average-order-value]] — analytics dashboards aggregating orders.
- [[settings-statuses]] — the taxonomy that defines status / payment-status / fulfillment-status labels and customer-notification toggles.

## Related

### Related entities

- [[order-status]] — entity page for the order status taxonomy.
- [[payment-status]] — entity page for the payment status taxonomy (the money lifecycle).
- [[shipping-status]] — entity page for shipping / fulfillment statuses.
- [[customer]] — every order optionally has one customer; orders snapshot the customer's name + email + group at create time.
- [[cart]] — every order originates from a cart; some carts never convert.
- [[product]] — orders have many product lines (each a snapshot of a product at order time).
- [[discount]] — order-level and per-line discounts; uses counter increments on counted-status orders.
- [[invoice]] / [[credit-note]] — accounting documents issued against an order.
- [[payment-provider]] / [[shipping-provider]] — providers that process the order's money and fulfillment.
- [[tax]] — per-line tax breakdown carried on the order.

### Cross-cutting concepts

- [[cart-vs-order-lifecycle]] — concept page on the cart → order transition.
- [[order-status-workflow]] — how Order × Payment × Fulfillment statuses interact.
- [[order-processing-pipeline]] — the full status-transition pipeline.
- [[checkout-flow]] — the storefront flow that produces orders.
- [[inventory-tracking]] — stock-decrement is driven by Order Status.
- [[notification-delivery]] — how a status change becomes a customer email.

### Settings & integrations

- [[settings-statuses]] — taxonomy + counted-status configuration (a status carries only a name — no per-status notification toggle).
- [[settings-hooks]] — `order.created` / `order.updated` / `order.deleted` webhook events.
- [[settings-banned-ip]] — auto-cancel rules that act on incoming offline-payment orders.
- [[settings-staff]] — moderator lock + per-staff order visibility rules.
- [[settings-cart]] — `order_complete`, `order_status_for_quantity_decrease`.
- [[settings-general-operational-toggles]] — `lock_orders` / `lock_orders_time` moderator lock.
- [[settings-invoicing]] — invoice / credit-note numbering scheme.
- [[marketing-discounts]] — discounts referenced by orders.
- [[api-orders]] — JSON-API v2 endpoint.
- [[json-api-v2]] — API overview.

## Open Questions

No outstanding questions on the hub — all items resolved or distributed to aspect pages.
