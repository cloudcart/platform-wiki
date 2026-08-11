---
type: feature
nav_path: "Customers → Customer details → Orders"
route_name: customers-orders.new
route_path: /admin/customers-new/details/:id/orders
aliases: ["Customer orders", "Customer order history", "Поръчки на клиента", "История на поръчките"]
tags: [customers, orders, history]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# Customer orders

## Purpose

The customer's full **order history** — every order they've placed with the store, with rich filter and search capabilities. The merchant uses this sub-tab to find a specific order the customer phoned about, audit the customer's recent activity (e.g., for fraud investigation), review the marketing-attribution sources (UTM tags) that brought the customer to the store, or jump from the customer's profile into a specific order to edit.

This is the per-customer filtered view of the global orders feature — same filter and column conventions, but auto-scoped to one customer ID. The tab is **read-only by design**: every per-row interaction either navigates away (opening the order detail page in a new tab) or shows a passive tooltip. There is no Add / Edit / Delete modal on this tab.

This hub is split into focused aspects — read the one that matches the question, not all of them.

## Sub-pages (in this cluster)

- [[customer-details-orders-list]] — the order-list table: eight columns (Order ID, Address, Date, Fulfillment, Receiving, Status, Total price, Actions), sort order, the icons-only Actions column, status-badge colour mapping, and every click-through navigation. The read-only-by-design rule.
- [[customer-details-orders-filters]] — the 21+ filters (order content, payment, fulfillment, provider, discount, date, document, marketing-attribution, metadata), the operator vocabulary, the CcTable filter-chip surface, and the exact-match-not-contains quirk on Made through / UTM / Referer.
- [[customer-details-orders-scoping]] — the server-side rules that shape what the list returns: strict auto-scope to one customer, hard-excluded voided orders, the Archived opt-in, the Completed fulfilled-rollup, free-text query columns, sort/pagination caps, the orders-permission gate, guest-order exclusion, and the "is_admin" chip-label bug.

## Where to find it

From [[customers-details]] → **Orders** tab. The route is `/admin/customers-new/details/:id/orders`.

## What the merchant can do here

- See every order this customer has placed in a paginated table (default 25 per page) — see [[customer-details-orders-list]].
- Sort by Order ID descending (default — newest first) or by Date — see [[customer-details-orders-list]].
- Apply any combination of 21+ filters across order content, payment, fulfillment, marketing attribution, and metadata — see [[customer-details-orders-filters]].
- Free-text search across order id, customer name/email, increment hash, invoice / receipt number, phone, and address — see [[customer-details-orders-scoping]].
- Click an order to open the order detail page (`/admin/orders/details/<id>`) in a **new tab** — see [[customer-details-orders-list]].
- Read the customer-note / admin-note tooltips on the per-row Actions icons — see [[customer-details-orders-list]].

### What the merchant CANNOT do here

- Create a new order on behalf of the customer from this tab — that's done in the orders feature's manual-order creation flow.
- Bulk-edit orders from this tab (e.g., bulk mark as fulfilled) — bulk actions live only on the global Orders feature.
- See orders for OTHER customers — the view is strictly auto-scoped to this one customer ID (see [[customer-details-orders-scoping]]).
- See guest orders placed under the same email but never linked to this customer record — see [[customer-details-orders-scoping]].

## Settings & fields

This is a hub — per-aspect pages carry the detailed tables. Quick map:

- Column definitions + status-badge colours → [[customer-details-orders-list]].
- Filter list + operator vocabulary → [[customer-details-orders-filters]].
- Free-text query columns, sort whitelist, pagination caps → [[customer-details-orders-scoping]].

## Business rules

This is a hub — the load-bearing server-side rules live on the aspect pages:

- **Auto-scoped, voided-excluded, archived opt-in, Completed rollup, permission gate, guest exclusion, sort/pagination caps** → [[customer-details-orders-scoping]].
- **Order-status vs payment-status independence, exact-match attribution filters** → [[customer-details-orders-filters]].
- **Read-only-by-design (no mutating actions), click-through navigation behaviour** → [[customer-details-orders-list]].

## Related

- [[customers-details]] — parent details page.
- [[customers-details-overview]] — overview tab; the 6 order-status cards link to this tab pre-filtered.
- [[settings-statuses]] — order / payment status taxonomies.
- [[settings-payment-providers]] — payment providers used in the filter.
- [[shipping]] — shipping providers used in the filter.
- [[marketing-discounts]] — discount codes used in the filter.
- [[settings-invoicing]] — invoice numbers used in the filter.
- [[order]] — entity page.
- [[customer]] — entity page.

## Open questions

None.
