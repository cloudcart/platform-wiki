---
type: feature
nav_path: "Orders → Order details"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Order details", "Order edit", "Order view", "Детайли на поръчка", "Преглед на поръчка"]
tags: [orders, details, edit, smarty]
plan_gates: ["orders_amount", "orders_revenue", "users_traffic"]
created: 2026-05-21
updated: 2026-08-06
source_count: 23
---

# Order details

## Purpose

The **per-order edit page** — where the merchant does almost everything related to one order: see its summary (products + totals + comments), change its status, edit the customer / addresses, manage payments (mark paid, refund, capture, cancel authorisation), manage shipping (change courier, generate / re-issue waybills, request insurance, print labels), edit products on the order (add lines, change quantities, remove, apply per-line discounts), generate / download / send invoices and credit notes, print the order receipt, archive / unarchive, cancel, and mark as completed.

For draft orders the page also surfaces a guidance alert explaining what's missing (products, payment, shipping) before the order can be "created" (transitioned out of draft).

## Where to find it

From [[orders]] → click any order row → opens `/admin/orders/details/<order_id>`. Route name: `admin.orders.details`.

Also reachable from [[customers-details-orders]] (per-customer order history) by clicking an order in the customer's history.

## Sub-pages (in this cluster)

This page is split into nine aspect pages. The page itself is a wide layout with a top header, a main column (summary + action rows), and a right sidebar — each aspect documents one slice of that surface.

- [[orders-details-header]] — top header / breadcrumb area: prev-next nav, status pill (and why it can read **Fulfilled**), draft alert, header-toolbar actions (View invoice, **Issue return**, Print, Copy checkout link, 3-dot menu with Cancel / Archive / Mark as completed).
- [[orders-details-products]] — main products table + per-line edits (quantity, override price, per-line discount, line options, remove). Pointer to the dedicated [[orders-products]] page for the full line-edit field catalogue.
- [[orders-details-addresses]] — shipping + billing address sidebar blocks: view, edit, add, swap saved address, office / locker pickup radio modes. Pointer to [[orders-address-edit]].
- [[orders-details-payment]] — Payment action row: provider, change provider, primary buttons + cog dropdown (mark paid, sync, capture / cancel authorisation, refund, manual confirm, lease, View more inline panel). Pointers to [[orders-payment-mark-paid]] / [[orders-payment-refund]] / [[orders-payment-capture]] / [[orders-payment-manual]].
- [[orders-details-shipping]] — Shipping action row: provider swap, **Fulfill products** (waybill), Print label, **Mark as unfulfilled**, EUR-variant waybill, courier-specific app rows. Pointer to [[orders-shipping-waybill]].
- [[orders-details-returns]] — the returns surface on this page: **Issue return**, the **Returns & exchanges** box, per-line return tags, and why a pending return hides the Fulfill-products button.
- [[orders-details-history]] — audit-log surface on this page; pointer to the canonical [[orders-history]] page.
- [[orders-details-actions]] — right-rail actions and convenience surfaces: Notify customer toggle, admin Note textarea, Recalculate-lock, Convert-to-EUR, Banned-IP add, ERP / fiscal-printer rows. Pointers to [[orders-notify-customer]] / [[orders-invoice]] / [[orders-credit]] / [[orders-receipt]].
- [[orders-details-known-issues]] — by-design vs bug catalogue: opening the page LOCKS the order, auto-promotion to completed on save, status pill omits five statuses, draft pill only offers Cancelled, waybill EUR hard-error after 2026-01-01, the invoice edit-lock, customer-edit only allowed for some statuses, address-change does NOT propagate to the customer's saved addresses.

## What the merchant can do here

In one screen: change status, edit customer + addresses, manage payment, manage shipping + waybill, edit line items, add / remove discount, issue a return, generate invoice / credit note / receipt, print order, archive / cancel / mark-completed, write admin note, toggle customer notifications. Each is covered on the aspect page above; the dedicated action pages (linked from each aspect) hold the field-by-field catalogue.

**Cannot** from this page: bulk-edit multiple orders (use [[orders]] list), convert a completed / paid / refunded order back to `pending` (status pill omits the path), delete the order (there is no delete action anywhere — orders are archived, see [[orders-archive]]), edit anything on the order once an **invoice number** has been issued (see below), or send arbitrary email content to the customer (the notify-customer route uses the per-status template — see [[orders-notify-customer]]).

### What is editable — three separate gates

The page does **not** have one "is this order editable" rule. Three different surfaces use three different gates, which is why a merchant can often still change the shipping address on an order whose line items are already frozen:

| Surface | Blocked when |
|---|---|
| **Line items** (add product, per-row cog, quantity / price / line discount) | an **invoice number** exists — checked first, regardless of status; otherwise unless the status is `pending` / `paid` / `authorized` AND the order is not fulfilled. See [[orders-details-products]]. |
| **Customer info** (name / email on the order) | status is anything other than `pending`, `paid` or `disputed` — note `authorized` is NOT allowed — or the order is archived. **No invoice check.** See [[orders-details-actions]]. |
| **Addresses** | **Billing**: an invoice number exists, OR status is `completed`, OR the order is fulfilled. **Shipping**: only status `completed` or fulfilled — **an invoice does NOT block the shipping address**. See [[orders-details-addresses]]. |

### The invoice lock arrives earlier than merchants expect

With **default** invoicing settings the platform issues the invoice number **by itself** as soon as the order becomes `paid` or `completed`, as soon as it is fulfilled, or immediately for a fully-digital order. Nothing is clicked. So a `paid` order — nominally an "editable" status — is in practice **already invoiced and already locked**. Un-fulfilling does not re-open it; corrections go through a return / credit note ([[orders-details-returns]]) or a new order. Full detail and the setting that changes it: [[orders-details-known-issues]].

## Settings & fields

The page itself does not own settings — it surfaces actions backed by other settings pages:

- [[settings-cart]] — `manual_order_payments`, `order_complete`, Google Maps API key.
- [[settings-general-operational-toggles]] — `lock_orders` + `lock_orders_time` (the moderator lock; **Settings → General**, not Cart).
- [[settings-statuses]] — the order-status taxonomy (custom statuses). Note: statuses carry only a name — there is no per-status customer-notification toggle.
- [[settings-invoicing]] — invoice numbering (auto / manual / external), `print_body`.
- [[settings-hooks]] — `order.updated` / `order.deleted` webhook events fired on save.

Per-aspect editable surfaces live on the linked aspect / detail pages.

## Business rules

The page is heavily **state-conditional** — buttons and rows appear / disappear based on `order.status`, `status_fulfillment`, `is_draft`, `is_confirmed`, payment-provider type, stock-sufficiency (`quantity_enough`), installed apps, and invoicing-numbering mode. See [[orders-details-known-issues]] for the full catalogue of state gates.

Every save — even editing just the admin note — runs the platform's order-event chain: stock recompute on canonical-status transitions, invoice / receipt number generation if configured, customer income totals recompute (async), discount usage counters increment, payment-authorisation auto-cancel on transition to a negative status, `order.updated` webhook (see [[settings-hooks]]), audit log row (see [[orders-history]]). Full pipeline on [[order-processing-pipeline]].

## Programmatic access

The full order resource is exposed via **JSON-API v2** — see [[api-orders]] for the canonical endpoint and the related sub-resources ([[api-order-products]], [[api-order-payment]], [[api-order-shipping]], [[api-order-discount]], [[api-order-shipping-address]], [[api-order-billing-address]], [[api-order-fulfillment]], [[api-order-tax]], [[api-order-total]]).

**Read-mostly.** Most sub-resources are READ-ONLY. The merchant can PATCH a small set of order-level attributes (`status`, `note`, `notify_customer` flag) and create / edit `order-fulfillment` records — but rich actions (refund, capture, mark-paid, manual confirm, invoice / credit-note generation, address edit, line CRUD, discount add / delete, waybill generate / remove) are admin-panel-only. Changing `status` via the API runs the SAME pipeline as the status pill — audit row is written with `api2` namespace. See [[json-api-v2]].

## Plan gates

Three numeric plan-features are registered against the path `orders/details/%`: `orders_amount`, `orders_revenue`, `users_traffic`. When one fires, the merchant lands on the [[plan-features]] upsell screen instead of the order detail. Gates extend via feature packs ([[plan-vs-feature-pack]]).

In practice only two of them can fire. `orders_amount` is **not** an order count — it is the **all-time sum of every order's total, in the store's currency** (see [[orders]] for the full explanation), and `orders_revenue` has no active calculator at all, so it always reads 0 and never blocks. `users_traffic` counts storefront sessions per month.

Beyond the page-level path restriction: the **payment capture** flow is gated by `authorize_payment` (see [[orders-payment-capture]]) and the **invoice flows** require the `invoices` access gate (see [[orders-invoice]]).

## Related

- [[orders]] — parent list.
- [[customers-details]] — sidebar "View customer profile" link.
- [[customers-details-orders]] — alternate way to reach this page (from the customer's order history).
- [[settings-statuses]] — the order-status taxonomy (custom statuses); no per-status notification config exists.
- [[settings-payment-providers]] — providers selectable on the order.
- [[shipping]] — shipping integrations + waybill behaviour.
- [[settings-invoicing]] — invoice template + numbering for the View Invoice / Credit Note actions.
- [[settings-cart]] — Google Maps API key for the sidebar map; `manual_order_payments` restriction; `order_complete` auto-promotion.
- [[settings-general-operational-toggles]] — `lock_orders` / `lock_orders_time` moderator lock.
- [[orders-details-returns]] — the returns surface on this page.
- [[settings-hooks]] — `order.updated` / `order.deleted` webhook events.
- [[settings-banned-ip]] — auto-cancel mechanism uses this page's status pipeline.
- [[products-products]] — product editor (click product on the order).
- [[marketing-discounts]] — order-level + line-level discounts.
- [[api-orders]] — JSON-API v2 endpoint (read + limited PATCH).
- [[json-api-v2]] — API overview.
- [[order]] — entity page.
- [[orders-returns]] — issue / process a return (full or partial) on this order — restock, refund, credit note.
- [[order-processing-pipeline]] — every history row on this page maps to an event from the pipeline.
- [[order-status-workflow]] — the status taxonomy + allowed transitions behind the status pill.
- [[order-totals-pipeline]] — how the order summary total is composed (subtotal → discounts → VAT → shipping → total).
- [[order-pipeline-recalculation]] — the Recalculate-lock + why totals freeze once payment completes / fulfilment is confirmed.
- [[payment-provider-mechanism]] — the model behind the Payment row (mark paid, capture, refund, sync).
- [[shipping-provider-mechanism]] — the model behind the Shipping row + waybill generation.
- [[multi-currency]] — the Convert-to-EUR action + the EUR-variant waybill.
- [[invoicing-and-accounting]] — the invoice / credit-note / receipt model behind those header actions.
- [[orders-add]] — manual-order-add page; produces the draft state this page edits.
- [[orders-status-change]] — status-pill change flow.
- [[orders-sync-cod]] — COD-sync sub-action.
- [[orders-user-files]] — per-order file attachments.

## Open questions

None.
