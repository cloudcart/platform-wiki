---
type: feature
nav_path: "Settings → Statuses → (delete protection)"
route_name: order-statuses
route_path: /admin/settings/statuses/order
aliases: ["Delete custom status", "Attached orders block", "This status has attached", "Status delete protection", "Archived order status rule"]
tags: [settings, statuses, orders]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-statuses]]. See the hub for the three taxonomies and the other cross-cutting mechanics (rename, custom codes, permissions).

# Statuses — delete protection

## Purpose

Custom order statuses can be deleted from [[settings-statuses-orders-tab]] — but only when no order in the store is currently parked at that status. The platform enforces an **attached-orders count gate**: try to delete a custom status that still has orders attached, and the delete is blocked with the count of orders that need to be reassigned first.

This page documents the delete-protection mechanic, the related "archived order" rule that prevents retroactively changing status on archived orders (which is what often blocks the merchant from emptying a custom status before deleting it), and the carrier-locked fulfillment-status carve-out that may stop the merchant from emptying the bin.

## Where to find it

The Delete action is the trash icon in the Actions column on the Orders tab of [[settings-statuses]]. Only rows with `custom: true` show the trash icon — built-in statuses have no Delete action at all. Routes:

- Inline confirmation popover → `DELETE /statuses/order/<status>` where `<status>` is the slug code (see [[settings-statuses-custom-codes]] for how the slug code is generated).

Built-in statuses (any taxonomy) cannot be deleted from this page — the trash icon never renders for them.

## What the merchant can do here

- **Delete a custom order status** by clicking the trash icon, then confirming on the inline popover. Succeeds only if no orders are currently in that status.
- **See the count of attached orders** in the error toast when the delete is blocked — the merchant uses that count to find and reassign / close those orders first.

What the merchant **cannot** do:

- Delete a built-in status (any taxonomy).
- Delete a custom status with orders attached — they must first be moved out of the status, manually one by one (or via bulk actions on [[orders]] *(verify)*).
- Have the platform auto-reassign orders to another status as part of the delete — there is no "delete and move all orders to status X" workflow. The merchant must do that manually from the Orders area.
- Change the status of an **archived** order to vacate the custom status — archived orders are locked. See "Business rules" below.
- Manually change the **fulfillment / shipping status** on an order whose courier integration locks the status — the merchant must trigger waybill generation through the carrier app. See [[orders-status-change-fulfillment-gate]].

## Settings & fields

The delete confirmation popover has no fields — it's a small inline Yes / No confirmation (`CcDeleteComponent`).

| Element | Notes |
|---------|-------|
| **Trash icon** | Renders only on rows where `custom: true`. Click opens confirmation popover. |
| **"Are you sure?"** popover | Yes / No buttons. Yes → fires `DELETE /statuses/order/<status>`. No → dismisses. |
| **Success toast** | *"Deleted successfully"* — the row is removed from the table. |
| **Failure toast** | *"This status has attached: `<N>`"* (literal string with the count appended — no "orders" noun). The row remains in the table. |

There is no merchant-facing UI to LIST which specific orders are attached to a custom status from this page. The merchant must navigate to [[orders]] and filter by the status to find them. *(verify — possibly filterable via the status pill in the orders list)*

## Business rules

### Attached-orders count is checked at delete time

Before deleting a custom status, the platform counts how many orders are currently parked at that status (regardless of archive flag, payment status, etc.). If count > 0, the delete is blocked with **HTTP 422**. The Vue layer surfaces this as a toast: *"This status has attached: `<count>`"* — the response body is literally that string with the number appended (no JSON wrapper, no key like `orders_count`).

### No auto-reassign on delete

There is no "move orders to status X first" workflow as part of the delete. The merchant must (1) note the count from the toast, (2) navigate to [[orders]] and filter by the custom status, (3) bulk-update those orders to another status from the orders list or change them one by one via [[orders-status-change]], (4) re-attempt the delete.

### Archived orders cannot have their status changed

The lang key `err.cannot_change_status_of_archived_order_unarchive_first` = "Статусът на архивирана поръчка не може да бъде променен. Първо разархивирай." → **An archived order's status CANNOT be changed** until it's unarchived.

This is the second-most-common blocker for merchants trying to empty a custom status: there are 5 orders in the custom status, but 3 of them are archived, and the bulk update silently skips those 3. The merchant must unarchive them first (from the orders list), then change their status, then re-archive if desired.

### Carrier-locked fulfillment statuses (related but distinct)

The lang key `err.for_change_fulfillment_status_use_button` = "Моля, генерирайте товарителница за тази поръчка. Смяната на статуса от тук, не е възможен." → Some shipping integrations refuse manual fulfillment-status changes — the merchant must trigger waybill generation through the carrier app. This rule only affects the SHIPPING taxonomy on the order details page; it does NOT prevent deleting a custom ORDER status from [[settings-statuses-orders-tab]]. Documented here because merchants sometimes conflate "I can't move this order out of a custom status" with "I can't delete the custom status".

### Backend route guard

The DELETE endpoint is constrained at the route level to `type = order` (`->where('type', 'order')` on the create + delete routes). `DELETE /statuses/{shipping,payment}/<status>` returns 404 — not a soft client error. The delete also requires the `settings.statuses` permission grant — moderators without it get HTTP 403, regardless of attached-orders count. See [[settings-statuses-permissions-validation]].

### Built-in statuses are never deletable

Built-in statuses (`custom: false`) are protected from deletion regardless of attached-orders count. The trash icon never renders for them, and the backend rejects the request even if it's manually constructed. Built-in statuses are part of the platform's order workflow and have downstream behaviour wired to them (e.g., the Completed-transition gate on [[orders-status-change-transition-rules]]).

### Deleting a custom status does NOT cascade-delete its orders

If the delete succeeds (because the attached count was 0 at delete time), only the status row is removed. There is no destructive effect on any order in the store. Subsequent attempts to set that status's code on an order via JSON-API v2 will fail validation. See [[settings-statuses-custom-codes]] for the consequences of deleting + re-creating with the same name.

## Related

- [[settings-statuses]] — hub.
- [[settings-statuses-orders-tab]] — where the Delete action lives.
- [[settings-statuses-custom-codes]] — what happens to the code on delete (and on re-create).
- [[settings-statuses-permissions-validation]] — the `settings.statuses` permission grant required for delete; the route-level `type` constraint.
- [[orders]] — the orders list; where the merchant filters by status to find attached orders.
- [[orders-status-change]] — the per-order status change flow used to move orders out of the custom status before deleting.
- [[orders-status-change-transition-rules]] — hard transition gates that may further constrain how the merchant can move orders out.
- [[orders-status-change-fulfillment-gate]] — the carrier-locked fulfillment carve-out (related but distinct).
- [[order]] — entity page; carries the `status` field that holds the custom code.

## Open questions

- Whether the orders list at [[orders]] surfaces a filter / pill specifically for custom statuses, or only via the generic status dropdown. *(verify)*
- Whether the count returned in the 422 body includes archived orders or only non-archived. *(verify)*
