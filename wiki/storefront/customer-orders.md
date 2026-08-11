---
type: storefront-page
route_name: site.account.orders / site.account.order
route_path: /customer/account/orders, /customer/account/order-view/{order_id}
themes_using: [all]
tags: [storefront, customer, account, orders, invoices]
created: 2026-06-08
updated: 2026-06-08
source_count: 4
---

# Customer orders & invoices

## Purpose

Shows the signed-in customer their full order history. Each row is a one-line summary; expanding a row (or clicking through) loads the detail view with line items, addresses, totals, payment + shipment status, tracking, digital-file downloads, invoice download/print links, and a "Re-order" button that pushes the past order's variants into the cart.

## URL & route

- List: `site.account.orders` → `GET /customer/account/orders`
- Detail (by id or `increment_hash`): `site.account.order` → `GET /customer/account/order-view/{order_id}`
- Re-order (turns a past order into a cart payload): `site.account.order.reorder` → `GET /customer/account/order-reorder/{increment_hash}`
- Public-by-hash variants (link from emails): `site.account.order.hash` → `GET /customer/account/order/{hash}`, `site.account.order.inh` → `GET /customer/account/order/i/{hash}` — in the same `customer` middleware group but reachable by guests via the middleware allow-list (`site.account.order.hash, site.account.order.reorder, site.account.order.inh, invoice.display.hash, invoice.download.hash`).
- Invoice routes (separate controller, see [[settings-invoicing]]): `invoice.display` (`{order_id}`), `invoice.display.hash` (`{hash}`), `invoice.download` (`{order_id}`), `invoice.download.hash` (`{hash}`).

## How it loads

1. List: paginates the signed-in customer's own orders into the account layout.
2. Detail: resolves an order matching `id == intval(order_id)` OR `increment_hash` on the customer's own orders, then renders the detail partial — reused inside an AJAX panel when expanded inline from the list.
3. Hash-by-link entry points decrypt the hash and render the same detail view — used by the "view your order" links in transactional emails so a guest can land directly on the page.
4. Site-specific carve-out: site id `17987` (or `?17987` in dev) uses a custom account/orders template pair with ticket-barcode columns — a single-merchant integration, noted only so support knows why that account's layout differs.

## What the customer sees

List view (`cc-account-table cc-account-table-orders`), columns:

- Order number (`order_number`)
- Date (`date_added_formatted`)
- Total (`price_total_formatted`)
- Status (`status_formatted`, colour-classed `status-{status_color}`)
- Shipment status (`status_fulfillment_formatted`, `status-{status_fulfillment_color}`)
- Actions cell:
  - Chevron-down `js-load-order` → expand inline, AJAX-loads the detail into the next `tr.js-load-order-content`
  - Chevron-up `js-load-order-remove` → collapse the inline detail
  - `cc-repurchase` icon (repeat) → triggers `addToCart(increment_hash)` inline JS that calls `site.account.order.reorder`
  - Truck icon (only when `status_fulfillment == 'fulfilled'` and a fulfillment `shipping_tracking_url` is set) → opens the tracking URL in a new tab

If the customer has no orders, an empty-state `_notification` paragraph reads `sf.account.orders.warn.no_orders_made`.

Pagination uses a shared paging partial. There is **no built-in filter by status or date range** — every order belongs to the page-size scroll. (verify whether any theme adds a filter module)

Detail view (`cc-order-details`):

- Meta grid: order id, order date, order status, shipment status (with expedition date when fulfilled), shipping address + delivery date, billing address (falls back to shipping when absent), tracking provider + number + delivery date, payment method(s), ticket validity + barcode SVG (custom integration).
- Totals breakdown with `group=shipping` and `group=total` rows specially classed.
- Invoice actions (when invoicing is on): "Download invoice" + "Print invoice" links pointing at `invoice.download.hash` / `invoice.display.hash` — both use the hash variant so they survive being shared.
- Per-line-item card: image (150×150), name, SKU, barcode, parameters, options (with file-option download links via `site.download.public` or `site.download.private.hash`), quantity × unit price, weight, digital-file downloads, and any per-line discount / discount-code / modifier rows.
- For membership / digital-page products ([[apps-membership]]): if the order is `paid` or `completed`, lists "access to" links to the private pages with expiry; otherwise prompts for payment.
- Big "Re-order" button at the bottom (`_button add-cart-product`) — also wired to the same `addToCart` JS.

## Storefront behaviour

- Re-order: resolves the order by `increment_hash` — this lookup is **not** scoped to the current customer, so the route relies on the `customer` middleware + `increment_hash` being effectively secret. It keeps only order products with a `variant_id` (skips bundle parents / freebies / line-only items) and merges them into the cart by `variant_id`: if the variant is already there, quantity is summed; otherwise added. On success the JS triggers `cc.ajax.reload` on `._cart-compact` so the header drawer reflects the new contents, then ends the spinner. Toastr error if the response carries `status` + `msg`.
- "View details" with `js-load-order` lazy-loads the detail markup into the row so the customer doesn't navigate away.
- Invoice download/display goes through a separate invoicing controller ([[settings-invoicing]]) which produces a PDF via the configured invoicing app.
- Status display: the storefront only mirrors the order — there is no "return / refund request" form here. Status changes (refunds, partial fulfilment) flow through the admin and appear on the customer's next reload. (verify)
- Tracking: when no carrier-specific URL exists but a tracking number does, the template falls back to `{$TRACK17}{$order->fulfillment->shipping_tracking_number}` — an aftership/17track-style universal tracker URL injected via a Smarty variable. (verify where `$TRACK17` is registered)

## JavaScript behaviour

- Inline `<script>` block in the list template:
  - Defines `msg_1 = sf.wishlist.added_products.one`, `msg_2 = sf.wishlist.added_products.multi` (likely leftover from wishlist add-to-cart; both are loaded but the re-order flow doesn't use them — possible historical baggage).
  - `addToCart(increment_hash)`:
    - Triggers `loading.start` on `.add-cart-product`
    - AJAX GET to `site.account.order.reorder` with the hash substituted
    - On success: `setTimeout( => $('._cart-compact').trigger('cc.ajax.reload'), 50)` and `loading.end`
    - On error with `json.status` + `json.msg`: `toastr.error(json.msg)`
  - `$(document).ready` initialises Bootstrap tooltips on `[data-toggle="tooltip"]`.
- The detail template has its own tiny `<script>` that re-initialises tooltips inside the panel.
- Inline-expand uses generic table-toggle conventions: `js-load-order`, `js-load-order-remove`, `js-load-order-content` — wired up in shared site JS. (verify exact file)

## Customisations available to the merchant

- Invoicing is gated by the invoicing module configuration; without it, the "Download / Print invoice" actions disappear.
- Tracking links render only if the order's fulfillment carries `shipping_tracking_url` (preferred) or `shipping_tracking_number` (fallback to `$TRACK17`). Set up tracking on each **shipping-providers** integration so links appear.
- Status colour-classes (`status-success`, `status-warning`, etc.) are themable via CSS.
- Custom integrations can replace the entire orders list — see the site id `17987` ticket-mode variant.
- Translations through `sf.account.orders.*`, `sf.account.order.details.*`, `sf.global.*`.

## Theme variations

- All standard themes inherit the shared orders-list + order-detail templates. (verify by grep)
- The site id `17987` account/orders template pair is the only known shipped variant — gated by site id.
- Themes restyle the order table via the `cc-account-table-orders` / `cc-order-details-*` class families.

## Known issues / by-design vs bug

- **Sharp edge**: re-order does NOT verify that the order belongs to the current customer — it only validates that `increment_hash` resolves to an order. The protection is the secrecy of the hash + the `customer` middleware (or its hash allow-list for the email-link flow). Treat any leaked `increment_hash` as a "merge this order into your cart" capability.
- **By design**: re-order skips items without a `variant_id` (most simple products have one; bundle children / freebies do not). Customers occasionally complain that "one item is missing" — usually a bundle.
- **By design**: variants that are now archived / out-of-stock are still added to the cart; downstream cart validation handles availability messaging.
- **By design**: no filter / search inside the orders list — pagination only.
- **By design**: no in-page returns / refund request form. Returns are handled out-of-band (email / **messenger** / shipper portal). Status changes show up after they're entered admin-side.
- **Bug-like**: the inline list-template script defines `msg_1` / `msg_2` from wishlist translations but never uses them. Cosmetic only.

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[customer-account]]
- [[customer-addresses]]
- [[checkout]]
- [[settings-invoicing]]
- [[orders]]
- [[order-processing-pipeline]]
- **shipping-providers**
- [[apps-membership]]
- **settings-customers**
- [[customers]]

## Open questions

- Where is `$TRACK17` registered as a Smarty global, and is the universal-tracker URL configurable per merchant?
- Does the customer ever see refund or partial-shipment status changes proactively (email / toast), or only on next visit?
- Are there hooks for theme developers to inject extra columns (e.g. "Reorder all" button per row) without forking the template?
- Is there a setting to expose returns/RMA from this page when an RMA app is installed?
