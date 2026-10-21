---
type: feature
nav_path: "Apps → Frisbo → Orders"
route_name: apps.frisbo.orders
route_path: /admin/apps/frisbo/orders
aliases: ["Frisbo Orders", "Frisbo fulfillment list", "Orders sent to Frisbo"]
tags: [apps, administration, frisbo, fulfillment, orders]
plan_gates: []
created: 2026-05-21
updated: 2026-10-21
source_count: 2
---
# Frisbo → Orders

## Purpose

The **Orders** tab lists the store's orders, newest first, with the result of the last attempt to send each one to Frisbo (empty when the order was never sent). Used to:
- See which orders reached Frisbo (*Success send order*) and which failed (Frisbo's error text).
- Send an order that has not reached Frisbo yet.

Frisbo's own fulfilment statuses (picked / packed / shipped / delivered) and tracking numbers are not shown here — they live in Frisbo's portal.

For the full Frisbo feature set, see [[apps-frisbo]].

## Where to find it

Sidebar → Apps → Frisbo → **Orders tab**. Route: `/admin/apps/frisbo/orders`.

## What the merchant can do here

### Orders data table

Per row:

| Column | Source |
|---|---|
| **Order** | Order number and code, linking to [[orders-details]] (new tab); below it "from <customer>" — clicking the name filters the list to that customer. |
| **Created at** | When the order was placed. |
| **Frisbo response** | *Success send order*, Frisbo's error text, or empty when the order was never sent. |
| (action) | **Send order to Frisbo** — shown unless the last result is *Success send order*. |

### Filter / search

One filter: **Customer** (see *Filter dropdown* below).

### Per-row actions

- **Send order to Frisbo** (cloud icon) — sends the order to Frisbo now and shows the result in the **Frisbo response** column. Shown only while the last result is not *Success send order*.

There is no cancel action and no details view.

### What the merchant CANNOT do here
- Edit order content (line items, quantities) after Frisbo has it — request the change via support.
- Cancel an order at Frisbo from this tab — there is no cancel action; cancellations are arranged with Frisbo support.
- Re-allocate stock without re-sending.

## Settings & fields

### Per-row data

| Field | Notes |
|---|---|
| **Order** | Number, code and customer. |
| **Created at** | The order's date. |
| **Frisbo response** | The last send result: *Success send order* or Frisbo's error text; empty if never sent. |

The tab shows no Frisbo status, warehouse, tracking number or shipping date.

## Business rules

### No status updates from Frisbo

The platform does not receive or fetch Frisbo's fulfilment status; the tab only shows the result of the last send.

### Auto-send trigger

Per [[apps-frisbo-settings]] config, orders may auto-send to Frisbo on a configured status (typically "Paid"). The result of each automatic send appears in the order's **Frisbo response** column.

### Side effects per action
- **Send**: the order is sent to Frisbo again; the new result is what the **Frisbo response** column shows.

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

The platform's cancel action is deprecated: it sends the order to Frisbo again instead of cancelling it (no real cancel endpoint is called), which is why this page has no Cancel button. For in-flight cancellations, the merchant must coordinate directly with Frisbo support.

### Orders tab shows the send-attempt result, not Frisbo fulfilment state

The Orders tab lists all of the store's orders. Each row shows the result of the last attempt to push the order to Frisbo: *"Success send order"* (the push succeeded), the Frisbo error text (the push failed), or nothing (never sent). The tab does **not** display Frisbo's downstream fulfilment statuses (picked / packed / shipped / delivered); those live in Frisbo's portal.

### No per-line, bulk, or per-warehouse operations

The tab offers only a per-order **Send order to Frisbo** action (one order at a time). There is no bulk send / cancel button, no partial-cancel (per-line), and no warehouse filter in this list view. Each row links to the underlying CloudCart order; warehouse routing happens via the **Warehouse** setting, not per-order.

### Customer returns are handled in Frisbo's portal

This Orders tab is for outbound sends only. Customer returns / inbound stock movement are managed in Frisbo's portal — not exposed in CloudCart's admin.

### One result shown per order — no per-attempt history

Each Send records a new result, and the tab shows only one result per order (normally the latest): *Success send order* or the latest error text. There is no screen that lists earlier attempts.

## UI structure — DataTable layout

The Orders tab is a single `@components/Table` DataTable with these columns (per `Orders.vue` + `OrdersTable/` cell components):

| Column | Component | Behaviour |
|--------|-----------|-----------|
| **Order** | `OrderId.vue` | Renders `Order #<id> (<increment_hash>)` as a link to `/admin/orders/details/<id>` (opens in new tab). Below it: "from <customer full name>" — clicking the name filters the table to that customer's Frisbo orders (calls `filterByCustomerId(customer_id)`). |
| **Created at** | `DateFormated.vue` | When the order was placed (the order's own date). |
| **Frisbo response** | plain text | The raw `erp_response` string — either `Success send order` or the latest exception text. Note: one result per order is shown; earlier attempts are not listed. |
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
