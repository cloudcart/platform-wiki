---
type: feature
nav_path: "Apps → Frisbo → Orders"
route_name: apps.frisbo.orders
route_path: /admin/apps/frisbo/orders
aliases: ["Frisbo Orders", "Frisbo fulfillment list", "Orders sent to Frisbo"]
tags: [apps, administration, frisbo, fulfillment, orders]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Frisbo → Orders

## Purpose

The **Orders** tab is the **list of CloudCart orders sent to Frisbo for fulfillment** — with their Frisbo-side status (picked / packed / shipped / delivered). Used to track:
- Which orders are in Frisbo's queue (waiting to be processed).
- Which orders Frisbo has shipped (with tracking numbers).
- Failed sends (errors from Frisbo).
- Cancellation requests.

For the full Frisbo feature set, see [[apps-frisbo]].

## Where to find it

Sidebar → Apps → Frisbo → **Orders tab**. Route: `/admin/apps/frisbo/orders`.

## What the merchant can do here

### Orders data table

Per row (per `OrdersTable/` Vue components):

| Column | Source |
|---|---|
| **Order ID** (`OrderId.vue`) | CloudCart order ID + link to [[orders-details]]. |
| **Date** (`DateFormated.vue`) | When the order was sent to Frisbo. |
| **Status** | Frisbo's current status — Pending / Picked / Packed / Shipped / Delivered / Failed / Cancelled. |
| **Tracking number** | When Frisbo has dispatched, the courier tracking ID. |
| **Actions** (`Actions.vue`) | Re-send, Cancel, View Frisbo details, Mark complete. |

### Filter / search

Standard filters:
- By Frisbo status.
- By order date.
- By customer name / order ID.

### Per-row actions

- **Send to Frisbo** — calls `sendOrder($orderId)` (per [[apps-frisbo]]).
- **Cancel at Frisbo** — calls `cancelOrder($orderId)`. Time-sensitive: once Frisbo has shipped, cancel may not be possible.
- **View Frisbo details** — opens a modal with full Frisbo state (warehouse, courier, tracking).

### What the merchant CANNOT do here
- Edit order content (line items, quantities) after Frisbo has it — request the change via support.
- Cancel a SHIPPED Frisbo order from this tab — must coordinate with Frisbo support.
- Re-allocate stock without re-sending.

## Settings & fields

### Per-row Frisbo state

| Field | Notes |
|---|---|
| **order_id** | CloudCart order ID. |
| **frisbo_order_id** | Frisbo's internal ID. |
| **frisbo_status** | Current fulfillment state. |
| **frisbo_tracking_number** | Courier tracking. |
| **frisbo_warehouse** | Which Frisbo warehouse is fulfilling. |
| **sent_at** | When sent to Frisbo. |
| **shipped_at** | When Frisbo dispatched. |
| **frisbo_error** | Error message when send failed. |

### Frisbo statuses

| Status | Meaning |
|---|---|
| **Pending** | Sent to Frisbo, awaiting pick. |
| **Picked** | Items picked from warehouse. |
| **Packed** | Ready to ship. |
| **Shipped** | Courier has the package. |
| **Delivered** | Customer received. |
| **Failed** | Frisbo could not fulfill (out of stock / address invalid / etc.). |
| **Cancelled** | Order cancelled before shipment. |

## Business rules

### Real-time status updates

Frisbo pushes status updates (or CloudCart polls). The Orders tab reflects the latest known state — typically within minutes of a Frisbo-side event.

### Auto-send trigger

Per [[apps-frisbo-settings]] config, orders may auto-send to Frisbo on a configured status (typically "Paid"). The Orders tab populates as orders reach that status.

### Cancel is time-sensitive

`cancelOrder` works only BEFORE Frisbo has shipped. After shipping, the merchant must coordinate cancellation via Frisbo support directly.

### Side effects per action
- **Send**: API call to Frisbo with order data; new Pending row.
- **Cancel**: API call to Frisbo cancellation endpoint; status updates to Cancelled.
- **Re-send**: New attempt after a Failed status.

### Permission
Standard apps permission scope.

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps-frisbo]] — Frisbo hub.
- [[apps-frisbo-settings]] — credentials + config.
- [[orders]] — source order list.
- [[orders-details]] — per-order detail page (where Send to Frisbo is also triggered).
- [[orders-shipping-waybill]] — Frisbo replaces normal waybill flow.

### Cancel programmatically is unreliable

The Manager's `cancelOrder` action is marked `@deprecated` and its implementation is identical to `sendOrder` (no real cancel endpoint is called). **Practical implication**: clicking Cancel on this page is NOT a reliable way to recall a Frisbo dispatch. For in-flight cancellations, the merchant must coordinate directly with Frisbo support.

### Orders tab shows the send-attempt result, not Frisbo fulfilment state

The Orders tab is an order list filtered by those with a `frisbo_response` meta — meaning the platform attempted to push the order to Frisbo. Each row shows the response: either *"Success send order"* (the push succeeded) or the Frisbo error text (the push failed). The tab does **not** display Frisbo's downstream fulfilment statuses (picked / packed / shipped / delivered); those live in Frisbo's portal.

### No per-line, bulk, or per-warehouse operations

The integration exposes only per-order Send-to-Frisbo and Cancel actions (one order at a time). There is no bulk send / cancel button, no partial-cancel (per-line), and no warehouse filter in this list view. Each row links to the underlying CloudCart order; warehouse routing happens via the settings `warehouse_id` value, not per-order.

### Customer returns are handled in Frisbo's portal

This Orders tab is for outbound sends only. Customer returns / inbound stock movement are managed in Frisbo's portal — not exposed in CloudCart's admin.

### Single `frisbo_response` meta per order — no per-attempt history

Each Send overwrites the previous response in the `frisbo_response` meta key. There is no per-attempt history table — only the most recent outcome (either `Success send order` or the latest error text) is visible. Earlier failed attempts are lost the moment a new attempt fires.

## UI structure — DataTable layout

The Orders tab is a single `@components/Table` DataTable with these columns (per `Orders.vue` + `OrdersTable/` cell components):

| Column | Component | Behaviour |
|--------|-----------|-----------|
| **Order** | `OrderId.vue` | Renders `Order #<id> (<increment_hash>)` as a link to `/admin/orders/details/<id>` (opens in new tab). Below it: "from <customer full name>" — clicking the name filters the table to that customer's Frisbo orders (calls `filterByCustomerId(customer_id)`). |
| **Created at** | `DateFormated.vue` | When the order was sent to Frisbo (uses `dayjs` formatting). |
| **Frisbo response** | plain text | The raw `erp_response` string — either `Success send order` or the latest exception text. Note: just one row's worth of data; previous attempts overwrite. |
| **(empty header)** Actions | `Actions.vue` | Single icon button: **Send to Frisbo** (cloud-upload icon) — only renders when `data.erp_success` is false. Calls `onSend(item)` which sets `item.sending = true`, calls `model.send(item.id)`, then refreshes. A commented-out **Cancel an order at Frisbo** action exists in `Actions.vue` but is disabled (because `cancelOrder` is deprecated and behaves like `sendOrder`). |

### Default state + sorting

- Default sort: `id desc` (newest order first).
- Default page size: 25.
- URL query persistence: filters + page + perpage round-trip through `$route.query`.
- The table model is `js/Orders.js` (extends the standard CC model with `send(id)` and `ignore(id)` actions).

### Filter dropdown

A single filter shows in the filter row at the top of the table:
- **Customer** (`customer_id`, type: `select`, multiple: false) — autocomplete URL `/admin/api/core/customers/autocomplete`. Selecting a customer narrows the list to that customer's Frisbo-pushed orders.

The customer-name link inside each `OrderId.vue` row acts as a quick-filter shortcut into this same filter — clicking the name rewrites the `$route.query` to include `filters[customer_id]=<id>` and reloads the table.

### No bulk operations / no order-status display

There is no bulk select / send button, no row checkbox in `Orders.vue` — each Send action is per-row only. Frisbo's downstream fulfilment statuses (picked / packed / shipped / delivered) are **not displayed in this tab** — those live in Frisbo's portal. The merchant only sees the platform's send-attempt outcome here.

## Open questions
