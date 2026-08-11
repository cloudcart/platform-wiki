---
type: feature
nav_path: "Customers → Customer details → Orders → Scoping & query rules"
route_name: customers-orders.new
route_path: /admin/customers-new/details/:id/orders
aliases: ["Customer orders scoping", "Order history query rules", "Voided orders excluded", "Customer order permission", "Order history pagination"]
tags: [customers, orders, history, scoping, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-orders]]. See the hub for the other aspects (list view, filters).

# Customer orders — Scoping & query rules

## Purpose

The server-side rules that decide **which** orders the customer order-history list actually returns — independent of any filter the merchant applies. This aspect covers the strict customer auto-scope, the hard-excluded voided orders, the Archived opt-in, the Completed fulfilled-rollup, the free-text query columns, the sort/pagination caps, the orders-permission gate, the guest-order exclusion, and the known "is_admin" chip-label bug. The visible columns are on [[customer-details-orders-list]]; the filter catalogue is on [[customer-details-orders-filters]].

## Where to find it

These rules apply transparently to the **Orders** tab from [[customers-details]] at `/admin/customers-new/details/:id/orders`. They are server-side and not directly visible, but they explain why some orders do or do not appear.

## What the merchant can do here

- Free-text search across many order columns via the `?query=` field above the filter chips.
- Reveal archived orders by explicitly applying the `Archived = Yes` filter.
- Filter by Completed and additionally pull fulfilled-but-not-yet-completed orders (the rollup below).

### What the merchant CANNOT do here

- See orders for other customers — the scope is strict to this one customer ID.
- See voided orders — they are hard-excluded even when Voided is selected.
- Find guest orders placed under the same email but never linked to this customer record (use the global Orders feature and search by email).
- Sort by any column other than Order ID or Date, or pull more than 100 rows per page.

## Settings & fields

### Free-text query field searches many columns

The `?query=` field (the free-text search above the filter chips) searches across: **order id, customer first name, customer last name, customer email, increment_hash** (the order's external 16-char id), **invoice number, receipt number, shipping-address phone, billing-address address1**. The merchant can type a phone number, an invoice number, an email, or part of an address to find an order.

### Sort + pagination caps

- The backend validates the sort field against only `id,date_added`. Any other column header is non-sortable; default sort is `id DESC`.
- Default page size is 25; the backend caps `perpage` at 100. The merchant cannot exceed 100 even if they pass a higher value in the URL.

## Business rules

### Auto-scoped to one customer

The page automatically adds `filters[customer_id]=<this customer's ID>` to every query — the merchant cannot widen the view to see other customers' orders. The match is a strict `whereIn('customer_id', [<id>])`. To search across customers, the merchant goes to the global Orders feature.

### Customer scope is strict — no email-aggregation for guests

Because the scope keys on `customer_id`, anonymous / guest orders placed by the SAME email but never linked to this customer record (no `customer_id`) will NOT appear here. To find them, the merchant uses the global Orders feature and searches by email.

### Voided orders never appear, ever

The backend default scope is `whereNull(date_archived) AND status NOT IN ('voided')`. Voided orders are HARD-EXCLUDED — even if the merchant selects `Order status = Voided` in the filter, the result is still empty for voided rows on this tab. The Voided value remains in the dropdown (see [[customer-details-orders-filters]]) but does not bring back voided orders.

### Archived filter is required to see archived orders

By default the listing only shows non-archived orders (`date_archived IS NULL`). To see archived orders, the merchant must explicitly add the `Archived = Yes` filter, which switches the default `IS NULL` to `IS NOT NULL`. Without that filter, archived orders never appear in this list even if they belong to the customer.

### "Completed" filter is enhanced with a fulfilled-orders rollup

When the merchant selects ONLY `Order status = Completed` (operator "is" or "in"), the backend additionally includes orders where `status_fulfillment = fulfilled` AND status is not in the negative set (cancelled / failed / refunded / voided / chargebacked, etc.). So filtering by Completed brings back BOTH true completed-status orders AND fulfilled-but-not-yet-marked-completed orders. This is a special-case rollup applied to that one status value.

### Order status taxonomy is platform-wide

The 11 order statuses (Authorized / Pending / Voided / Timeouted / Cancelled / Failed / Refunded / Chargebacked / Paid / Completed / Disputed) are platform-defined and shared with the global orders feature and [[settings-statuses]] taxonomy. Custom statuses the merchant defined in [[settings-statuses]] are not shown in this filter dropdown — they fall under one of the platform buckets.

### Permission

The backend endpoint requires the **orders** permission (`hasApiPermission:orders` middleware), NOT the customers permission. So a merchant role with customers access but no orders access will see the Orders tab in the UI, but the list will not load (403 from the API). The per-row actions (view PDF invoice, edit, on the order detail page) likewise inherit the orders permission.

### "Is admin" filter chip label bug

There is a known mislabel: when the merchant applies the `Created by admin` filter, the filter chip displayed above the table reads "draft" (not "is_admin"). The filtering still works correctly server-side — it's only the chip label that's wrong.

## Related

- [[customers-details-orders]] — hub.
- [[settings-statuses]] — platform-wide order / payment status taxonomies.
- [[order]] — entity page.
- [[customer]] — entity page; the `customer_id` the scope keys on.
- [[settings-invoicing]] — invoice / receipt numbers searched by the query field.

## Open questions

None.
