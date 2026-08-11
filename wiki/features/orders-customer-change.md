---
type: feature
nav_path: "Orders → Order details → Customer → Edit"
route_name: admin.orders.customer.edit
route_path: /admin/orders/action/customer/:order_id/edit
aliases: ["Edit customer on order", "Change order customer", "Update customer info on order", "Промяна на клиент на поръчка", "Редакция на клиент на поръчка"]
tags: [orders, customer, edit, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Customer edit (on order)

## Purpose

The flow for **editing the customer information attached to a specific order** — first name, last name, email — without (necessarily) modifying the underlying customer record. Used when:

- The customer placed an order with a typo in their name → merchant corrects it on the order.
- The merchant phoned the customer and clarified their actual name / email.
- Two customer records were created in error and the merchant needs to manually correct the per-order data.
- The order has a different recipient than the registered customer (e.g., gift to a friend).

The page exposes a critical toggle: **"Update customer info"** — intended to also propagate the changes to the underlying customer record. In practice the toggle is effectively decorative; see [[orders-customer-change-propagation]] for the real propagation conditions.

The page does NOT let the merchant SWAP the order to a different customer account. To do that, the merchant would need to delete the order and recreate it OR contact CloudCart support.

This cluster is split into focused aspects because the flow combines a snapshot data-model, a counter-intuitive propagation rule, status-gating, and a layered validation chain — each worth its own page.

## Sub-pages (in this cluster)

- [[orders-customer-change-panel]] — the side-panel UI: where to find it, the cog-menu status gate (`pending` / `paid` / `disputed`), form fields, after-save partial reloads.
- [[orders-customer-change-snapshot-model]] — the order's customer snapshot (three fields) vs the live customer record; why phone is NOT here; notification re-routing when the email changes.
- [[orders-customer-change-propagation]] — the "Update customer info" toggle, the decorative-toggle quirk, the three propagation conditions, and why no `customer.updated` webhook fires.
- [[orders-customer-change-validation]] — required-field + max-191 rules, the archived-order block and its ordering, the full before/after history diff, no email-uniqueness check.

## Where to find it

From [[orders-details]] → in the **Customer sidebar card** → settings cog → **Edit customer info on this order** (`order.customer_edit`).

Only available when the order's status is `pending`, `paid`, or `disputed` (per [[orders-details]]'s sidebar conditional). The interface is a **side panel** (slides from right) — same panel UX as the address-edit flows. Full UI + status-gate detail is on [[orders-customer-change-panel]].

Routes:
- `admin.orders.customer.edit` (GET) — opens the edit panel.
- (same route, POST) — saves the changes.

## What the merchant can do here

- Edit the order's **First name**, **Last name**, and **Email** snapshot fields. These three are the ONLY editable fields — see [[orders-customer-change-snapshot-model]].
- Optionally propagate those changes to the linked customer record (intended via the **Update customer info** toggle, but the real rule is on [[orders-customer-change-propagation]]).

What the merchant CANNOT do here:
- Change which customer the order belongs to (no `customer_id` field). To reassign, use DB intervention or CloudCart support.
- Edit phone — phone lives on the address records, edited via [[orders-address-edit]].
- Edit on an **archived** order — blocked with *"Cannot perform this operation on archived order"* (unarchive via [[orders-archive]] first).
- Edit on an order in `cancelled`, `completed`, `paid + fulfilled`, or `refunded` state — the sidebar cog hides the action.
- Add / remove customer tags, change password, or create a new customer record (use [[customers-details]] / [[customers]] / [[orders-add]]).

## Settings & fields

The order's customer-related fields are an **independent snapshot** — `customer_id` (link to the underlying customer; NOT changed by this flow), `customer_first_name`, `customer_last_name`, `customer_email`. The three name/email fields are what this form edits; the snapshot semantics (why past orders keep old data, why invoices use the snapshot) are detailed on [[orders-customer-change-snapshot-model]].

The **Update customer info** toggle (header switch) writes a hidden `update_info` input (`"yes"` / `"no"`). Its real effect is documented on [[orders-customer-change-propagation]].

## Business rules

- **Snapshot model** — orders store customer info as a snapshot at order time, independent of current customer state. See [[orders-customer-change-snapshot-model]].
- **Propagation** — changes can flow to the customer record under specific conditions; the visible toggle does NOT gate it as the UI suggests. See [[orders-customer-change-propagation]].
- **Archived orders are protected** — save raises *"Cannot perform this operation on archived order"*; unarchive first via [[orders-archive]].
- **Status gate** — the edit action only appears in `pending` / `paid` / `disputed`. See [[orders-customer-change-panel]].
- **Validation** — first/last name + email required, max 191 chars each; email must be valid format. See [[orders-customer-change-validation]].
- **Permission** — standard orders permission scope.
- **Side effects on save** — the order's customer name / email snapshot updates; (conditionally, via the *Update customer info* toggle) the linked customer record updates too; an `order_customer_edit` history entry is written; the Customer sidebar card + history panel reload on [[orders-details]]. **No webhook fires** — unlike most order edits, the customer-edit action does **not** trigger an `order.updated` webhook (verified — the controller writes the history row but never calls the order's hook trigger). See [[order-pipeline-stage-5-edit]].

## Related

- [[orders-details]] — parent page (Customer sidebar card).
- [[customers]] — customer list (where the customer record lives).
- [[customers-details]] — customer profile (full customer data editing).
- [[orders-history]] — `order_customer_edit` action_string event.
- [[order-pipeline-stage-5-edit]] — order-edit side-effect matrix; customer-edit is one of the few edits that does **not** fire `order.updated`.
- [[orders-invoice]] — invoices use the order's snapshot (not live customer data).
- [[orders-credit]] — credit notes use the order's snapshot.
- [[orders-address-edit]] — phone is edited here, not on the customer panel.
- [[orders-archive]] — unarchive an order before editing.
- [[order]] — entity page.
- [[customer]] — entity page.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
