---
type: feature
nav_path: "Orders → Order details → Customer → Edit → Propagation"
route_name: admin.orders.customer.edit
route_path: /admin/orders/action/customer/:order_id/edit
aliases: ["Update customer info toggle", "Propagate order edit to customer record", "Decorative toggle quirk", "customer.updated webhook missing"]
tags: [orders, customer, edit, propagation, webhooks]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[orders-customer-change]]. See the hub for the other aspects (panel UI, snapshot model, validation).

# Customer edit — propagation to the customer record

## Purpose

Covers the **"Update customer info" toggle** and the real conditions under which an edit on the order also rewrites the linked customer record. This is the most counter-intuitive part of the flow: the visible toggle does NOT gate propagation the way the UI implies, and the propagation path is silent to `customer.updated` webhook subscribers.

## Where to find it

The toggle is the **switch in the header** of the customer-edit side panel ([[orders-customer-change-panel]]), reached via [[orders-details]] → Customer sidebar card → cog → **Edit customer info on this order**.

## What the merchant can do here

The merchant flips the **Update customer info** toggle (on-label *"Update customer info"*, `order.label.update_customer_info`) intending to choose whether the edit also updates the underlying customer record. In intent:

| Toggle state | Effect on Order | Effect on Customer record (intended) |
|--------------|-----------------|--------------------------------------|
| **ON** | Order snapshot updated | Customer's name + email also updated |
| **OFF** | Only order snapshot updated | Customer record unchanged |

The actual behaviour differs from this intent — see the business rules below.

## Settings & fields

The toggle writes a hidden `update_info` input — `"yes"` when on, `"no"` when off (default). The backend reads this input but its truthiness check makes the OFF value ineffective (see below). The three snapshot fields it can propagate are documented on [[orders-customer-change-snapshot-model]].

## Business rules

### Propagation requires "is dirty" AND a linked customer (toggle quirk)

In the intended design, the customer record is updated only when all three are true:

1. **Is dirty** — at least one of the three order fields actually changed.
2. **`update_info` toggle is ON** — merchant explicitly opted in via the header switch.
3. **Order has a linked customer** — the order's customer relation isn't null.

**The subtle backend quirk:** the toggle's hidden input always sends a value (`"yes"` on, `"no"` off). The backend checks if that value is *truthy* — and any non-empty string is truthy in PHP, so `"no"` reads as truthy too. As a result, propagation to the customer record happens **regardless of toggle state**, as long as the fields actually changed AND the order has a linked customer. The toggle's OFF state does NOT block propagation as the UI suggests.

In practice: if the merchant changes any of the three fields and the order has a linked customer, the customer record will be updated. To suppress this, the merchant must either:

- Have the order not linked to any customer (rare).
- Avoid changing the fields entirely.

This is a known behavior — the **"Update customer info" toggle is effectively decorative** in the customer-edit panel.

If no fields actually changed, the customer record is NOT touched even though the truthiness check passes (the dirty-check still gates it) — this avoids no-op writes.

### No webhook for customer.updated — only order.updated fires

When the customer record is updated via this propagation path, the platform does NOT fire the `customer.updated` webhook from this controller — only `order.updated` (see [[settings-hooks]]). The customer change happens within the order-edit transaction without surfacing through the customer-events channel. For integrations that need to react to customer profile changes, this can be a **silent data drift** — the customer record changed but no customer-scoped webhook announced it.

## Related

- [[orders-customer-change]] — hub.
- [[orders-details]] — parent page; sidebar customer card.
- [[settings-hooks]] — `order.updated` fires; `customer.updated` does NOT fire from this path.
- [[customers-details]] — where the (silently) updated customer record is viewed.
- [[customer]] — entity page.

## Open questions

None.
