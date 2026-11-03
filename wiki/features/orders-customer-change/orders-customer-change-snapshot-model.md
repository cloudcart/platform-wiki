---
type: feature
nav_path: "Orders → Order details → Customer → Edit → Snapshot model"
route_name: admin.orders.customer.edit
route_path: /admin/orders/action/customer/:order_id/edit
aliases: ["Order customer snapshot", "Customer snapshot fields on order", "Order vs customer record", "Why phone is not on customer edit", "Notification re-routing on email change"]
tags: [orders, customer, edit, snapshot]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[orders-customer-change]]. See the hub for the other aspects (panel UI, propagation, validation).

# Customer edit — the order snapshot model

## Purpose

Explains **what the three editable fields actually are**: an independent customer snapshot stored on the order at order time, separate from the live customer record. This is the data-model reasoning behind the whole flow — why editing here doesn't change past invoices, why the customer's later profile changes don't rewrite old orders, why phone is deliberately excluded, and why changing the email re-routes future notifications.

## Where to find it

The snapshot fields are edited from the customer-edit side panel ([[orders-customer-change-panel]]), reached via [[orders-details]] → Customer sidebar card → cog → **Edit customer info on this order**.

## What the merchant can do here

The form fills exactly **three** fields on the order:

- `customer_first_name`
- `customer_last_name`
- `customer_email`

These are the order's own snapshot — distinct from the linked customer record's fields. Editing them changes ONLY this order (propagation to the customer record is a separate, conditional behaviour — see [[orders-customer-change-propagation]]).

### Phone is NOT editable here

Customer phone lives on the address records (shipping / billing) and is edited via [[orders-address-edit]] instead. This is intentional — phone is a delivery contact attribute, not a customer profile attribute on the order's snapshot.

### Customer ID cannot be swapped

The form has no `customer_id` field — only the three snapshot fields are accepted. So this flow CANNOT change which customer the order belongs to. To reassign an order to a different customer, the merchant needs direct DB intervention or CloudCart support.

## Settings & fields

The order's customer-related fields:

- `customer_id` — link to the underlying customer (NOT changed by this flow).
- `customer_first_name` — order's snapshot.
- `customer_last_name` — order's snapshot.
- `customer_email` — order's snapshot.

When the customer changes their account name / email later in [[customers]], it does NOT propagate to past orders — those keep their snapshot. The reverse is also true: editing here (under the conditions on [[orders-customer-change-propagation]]) is the only path back to the customer record.

## Business rules

### Snapshot model — orders are independent of current customer state

CloudCart stores customer info on the order as a **snapshot at order time** (`customer_first_name`, `customer_last_name`, `customer_email` on the order itself). This means:

- When the customer later changes their account name, past orders keep showing the original name.
- When the merchant edits the order's customer info, only that order is affected (unless the propagation conditions on [[orders-customer-change-propagation]] are met).
- Invoices generated from the order use the snapshot, not the live customer data — see [[orders-invoice]] and [[orders-credit]].

This is intentional for legal compliance — invoices and orders are time-locked records.

### Notification implications

The order's `customer_email` is the address that receives all subsequent status-change notifications (per [[orders-notify-customer]]). So editing the email on the order **re-routes future notifications** to the new address — useful when the customer phoned to say *"that email had a typo, please send updates to <correct address>"*.

### No email-conflict check

The save accepts any email format without checking for collision against other customers. The merchant can set the order's email to one that matches a different customer's email; the order's `customer_id` still points to the original customer, but the email field shows the other person's address. This is uncommon but can happen with typo fixes. (The same lack of uniqueness enforcement applies to the propagated customer record — see [[orders-customer-change-validation]].)

## Related

- [[orders-customer-change]] — hub.
- [[order]] — entity page; carries the snapshot fields.
- [[customer]] — entity page; the live record the snapshot is taken from.
- [[customers]] — customer list; later edits here do not rewrite past orders.
- [[orders-address-edit]] — where customer phone is actually edited.
- [[orders-invoice]] — invoices use the order's snapshot.
- [[orders-credit]] — credit notes use the order's snapshot.
- [[orders-notify-customer]] — status-change notifications go to the order's `customer_email`.

## Open questions

None.
