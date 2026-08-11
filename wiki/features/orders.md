---
type: feature
nav_path: "Orders"
route_name: admin.orders
route_path: /admin/orders/list
aliases: ["Orders", "Order list", "Order management", "Поръчки", "Списък с поръчки"]
tags: [orders, list, core, smarty, hub]
plan_gates: ["orders_amount", "orders_revenue", "users_traffic", "abandoned_orders_info", "new_orders"]
created: 2026-05-21
updated: 2026-08-06
source_count: 13
---

# Orders

## Purpose

The **central order management** screen — the merchant's primary working surface for every order placed on the store. Lists every order with status, total, customer / shipping address, courier, payment status, and quick-access actions. The page lets the merchant search free-text, filter aggressively (22+ filter types — see [[orders-list-filters]]), bulk-archive / unarchive / mark-complete (see [[orders-list-bulk-actions]]), add a new manual order, and export the list (see [[orders-list-export]]). It is the canonical merchant order workflow; the modern Vue admin surfaces only ancillary order views (e.g. the customer-scoped order history in [[customers-details-orders]]).

When the store has **no orders at all**, the page replaces the whole filter bar + table + export button with an empty state reading *"You have not received any orders yet"* / *"Your store's orders will show up here"*, plus *"Having trouble with orders? Follow the link below."* and an **Orders help** link to the support site. This is an unfiltered check — a store that has orders but none matching the current filter sees an empty **table**, not this screen.

## Where to find it

Sidebar → **Orders**. Breadcrumb reads "Orders". Route `/admin/orders` (or `/admin/orders/list`), route name `admin.orders`.

## Sub-pages (in this cluster)

The Orders list is split into seven aspect pages. Each covers one well-scoped slice; drill into the aspect matching the question rather than reading every page.

- [[orders-list-columns]] — the 8 (+1 conditional) list columns, which five are sortable, the comment icon, and the header actions (**+ Add order**, **Export**).
- [[orders-list-filters]] — the free-text search box, the 22+ filter types, saved filter presets, session persistence, the numeric operator encoding, and the two filter combinations that silently return the wrong rows.
- [[orders-list-bulk-actions]] — bulk Archive / Unarchive / Mark as completed: the exact confirmation strings, customer-notification side-effect, the archive status gate, and why a mixed selection aborts the whole batch (and why a bulk status change can report success while changing nothing).
- [[orders-list-status-taxonomy]] — the 11 hard-coded canonical statuses (positive flow + `NEGATIVE_STATUS` array), the bulk-status dropdown restriction (5 statuses removed), and how custom statuses from [[settings-statuses]] layer as sub-labels.
- [[orders-list-default-visibility]] — the silent default exclusion (cancelled / voided / archived hidden until ANY filter is applied), the default sort by order ID descending, and the implication for "count of orders" tickets.
- [[orders-list-export]] — the 2FA-gated export, its two outcomes (inline download vs queued + emailed), what it contains, and why it does NOT hide the same rows the list hides.
- [[orders-list-locking]] — the **Lock orders** moderator-collision protection (7-minute window, owner bypass), the auto-promotion to `completed` on save side-effect, and the "any save fires the full pipeline" caveat.

## What the merchant can do here

In one screen: scan all orders, search free-text, filter aggressively, save a filter set for reuse, sort by five columns, open one order ([[orders-details]]), add a manual order ([[orders-add]]), bulk-archive / bulk-unarchive / bulk-mark-completed, and export the list. Detail pages handle per-order editing (status, customer, addresses, payment, shipping, products, invoice, refund, returns) — none of those are reachable inline from the list.

**Cannot** from this list:
- **Delete orders — in bulk or one at a time.** There is no order-delete action anywhere in the admin panel, and none on the order detail page either; the JSON-API v2 orders resource excludes DELETE as well. Orders are **archived** ([[orders-archive]]).
- Edit individual order fields inline. All editing happens in the order's detail page.
- Switch to card / Kanban / calendar view. The list is table-only.

### Free-text search

Above the filter bar sits a single keyword box that most merchants never notice. It matches, depending on what is typed:

- **A number** → order number, invoice number, receipt number, product SKU, product barcode, and the shipping / billing **phone** (matched from the end, so leading zeros and country prefixes can be omitted).
- **Text** → customer email, customer first / last name, the customer's checkout note, and product name / category / vendor.
- **Anything with `@`** → customer email.
- **Anything else** → courier **waybill number**, payment hash / provider reference, and the order's checkout hash.

It is the fastest way to answer *"the customer says they ordered but I can't find it"* — searching their phone number or the waybill usually lands it immediately. Note that using it counts as applying a filter, so it also reveals archived / cancelled / voided orders (see [[orders-list-default-visibility]]).

## Settings & fields

Sortable columns: **Order** (`number`), **Date** (`date_added`), **Fulfillment**, **Receiving**, **Total** (`price_total`) — plus **Shipping date** when the Shipping Hours app is installed. Address, Status and Comment are display-only. See [[orders-list-columns]].

Bulk action routes: Archive / Unarchive use `admin.orders.archive-bulk` (action `yes` / `no`); Mark as completed uses `admin.orders.bulk-status` (status `completed`). See [[orders-list-bulk-actions]].

Per-aspect configuration (column toggles, available filters, alert thresholds) lives on the linked aspect pages above.

## Business rules

### List is the canonical merchant working surface

The list is where merchants spend most of their daily time — checking new orders, dispatching them, tracking payment status, archiving completed work. Typical filter workflows: "Show me orders to fulfill today" → Status = Paid + Fulfillment = Not fulfilled + Date added = Today. See [[orders-list-filters]] for the full filter catalogue.

### Archive is the only cleanup path — and it is NOT unconditional

There is **no delete**. Archiving hides an order from the default list while keeping all its data; it stays queryable via **Archived = Yes** ([[orders-list-default-visibility]]).

But archiving is **status-gated**: an order can only be archived when its status is `completed` or `cancelled`. Anything else — `pending`, `paid`, `refunded`, … — is refused with *"Only completed orders can be archived."* (Drafts are the one exception: a draft can be archived in any state.) Unarchiving has no restriction at all.

This matters most in **bulk**: the whole selection runs as a single transaction, so **one ineligible order aborts the entire batch** — nothing is archived, and the merchant only sees the error. The fix is to filter to `completed` / `cancelled` first, then select. See [[orders-archive]] and [[orders-list-bulk-actions]].

### Older list UI

This page is an older revision of the admin UI than the modern screens in [[settings]] / [[customers]] / [[products-products]]. Merchants should expect full-page reloads on most interactions and classic browser confirmation dialogs. When the replacement ships, the route will likely move to `/admin/orders-new/...` while merchant-facing behaviour is preserved.

### Permission

Requires the **orders** permission section. Per [[settings-staff]] restrictions, moderators may be restricted to seeing only orders matching certain criteria — the list auto-applies those restrictions. Concurrent-edit protection: [[orders-list-locking]] (configured on **Settings → General**, see [[settings-general-operational-toggles]]).

## Programmatic access

Orders can be read and (in limited ways) updated via **JSON-API v2** — see [[api-orders]] for endpoint, filters, attributes, and validation. Sub-resources (`order-products`, `order-payment`, `order-shipping`, `order-discount`) are read-only; only `order-fulfillment` is writable. **Orders cannot be created or deleted via the API** — creation is through the storefront checkout or the manual-order flow ([[orders-add]]), and orders are archived rather than deleted ([[orders-archive]]).

API `status` changes run the SAME pipeline as the bulk-action / status-pill flow (status gates, auto-promotion to `completed`, negative-status payment-authorization cancellation, stock decrement/restore, discount-uses recompute, customer email, `order.updated` webhook). The audit log shows "API" as the actor in [[orders-history]]. See [[orders-status-change]], [[order-processing-pipeline]], [[json-api-v2]].

## Plan gates

Gated by plan-features (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]):

- `orders_amount` — **not an order count.** It is the **total money value of every order the store has ever taken**, expressed in the store's currency: the sum of all orders' totals, with no date window and no status filter (cancelled and refunded orders count too). So a plan whose `orders_amount` allowance is, say, 50 000 is capping *cumulative turnover recorded in the platform*, not orders per month — and because nothing ages out, a long-running store creeps toward the cap even in a quiet month. When it fires, both the list and the detail pages redirect to upsell. Sandbox stores are exempt.
- `orders_revenue` — **has no active calculator**: usage always reads 0, so this cap never fires in practice, whatever the plan says. It remains registered on the paths.
- `users_traffic` — numeric (storefront sessions / month). List and details redirect to upsell when the cap is hit.
- `abandoned_orders_info` — boolean. Populates the dashboard abandoned-orders badge only; does NOT block this list.
- `new_orders` — boolean. Drives the dashboard pending-new-orders tile only; does NOT gate this list.

The gates are registered against the paths `orders` and `orders/details/%`. When one fires the merchant lands on [[plan-features]] for the per-feature upsell. The numeric gates extend via feature packs ([[plan-vs-feature-pack]]); permanent lift needs a plan upgrade. The boolean dashboard counters are plan-upgrade only.

## Related

- [[orders-subscriptions]] — recurring / subscription orders (separate listing).
- [[orders-abandoned]] — abandoned-orders companion list.
- [[orders-details]] — per-order detail / edit page.
- [[orders-add]] — manual-order add flow (the side-panel from the header).
- [[orders-export]] — legacy export entry point (also reached from this list).
- [[orders-archive]] — archive toggle flow.
- [[customers-details-orders]] — per-customer-scoped order view (in modern Vue).
- [[settings-statuses]] — order / payment / shipping / fulfillment status taxonomies.
- [[settings-banned-ip]] — order-rejection blacklist.
- [[settings-payment-providers]] — payment providers used in the filter.
- [[shipping]] — shipping integrations used in the filter.
- [[settings-invoicing]] — invoice template + numbering for the invoice / credit-note flows.
- [[orders-returns]] — the order-return process (full / partial, restock, refund, credit note) issued from an order.
- [[apps-aftercare]] — the EU "Withdraw from contract" (right-of-withdrawal) app; its withdrawal-requests inbox lives under Orders (`/admin/orders/aftercare`).
- [[marketing-discounts]] — discount codes used in the filter.
- [[settings-hooks]] — `order.created` / `order.updated` / `order.deleted` webhook events.
- [[api-orders]] — JSON-API v2 endpoint.
- [[json-api-v2]] — API overview + auth + rate limit.
- [[order]] — entity page.
- [[order-processing-pipeline]] — end-to-end side-effects fired across the order lifecycle (placement, status change, fulfillment, edits, refunds).
- [[order-status-workflow]] — the 11 canonical statuses, allowed transitions, custom statuses, and the auto-promotion rules behind the status pill.
- [[order-totals-pipeline]] — how the order Total is composed (subtotal → discounts → VAT → shipping → VAT-on-shipping → total).
- [[cart-vs-order-lifecycle]] — entity-level difference between a cart and the order it becomes.
- [[fulfillment-and-warehouse]] — the fulfillment status used in the list filters + the native fulfillment lifecycle.

## Open questions

None.
