---
type: feature
nav_path: "Orders → Order details → Customer → Edit → Panel"
route_name: admin.orders.customer.edit
route_path: /admin/orders/action/customer/:order_id/edit
aliases: ["Customer edit panel", "Edit customer side panel", "Customer cog menu", "Edit customer info on this order"]
tags: [orders, customer, edit, smarty, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[orders-customer-change]]. See the hub for the other aspects (snapshot model, propagation, validation).

# Customer edit — the side panel & status gate

## Purpose

The **UI surface** of the customer-edit flow: where the action lives in [[orders-details]], which order statuses expose it, the side-panel layout the merchant interacts with, and what reloads after a successful save. This page is the "what the merchant sees and clicks" reference; the data-model, propagation, and validation rules are on the sibling aspects.

## Where to find it

From [[orders-details]] → **Customer sidebar card** → settings cog → **Edit customer info on this order** (`order.customer_edit`).

The interface is a **side panel** (slides from the right) — the same panel UX as the address-edit flows in [[orders-address-edit]]. Routes:

- `admin.orders.customer.edit` (GET) — opens the panel.
- (same route, POST) — saves.

### Where the cog menu lives — only visible in 3 statuses

The **Edit customer info on this order** action is hidden when the order status is NOT one of `pending`, `paid`, `disputed`. This is enforced in the sidebar template (`{if in_array($order->status, ['pending', 'paid', 'disputed'])}`). So for orders in `completed`, `cancelled`, `refunded`, `authorized`, `abandoned`, or any negative gateway status (failed, voided, etc.), the cog shows ONLY *"View customer profile"* and the merchant CANNOT open the edit panel.

This is a UI gate only — the backend route would still accept a direct call (other than the archived-order block — see [[orders-customer-change-validation]]). But the only way to reach it from the standard UI is via this cog.

### Settings cog dropdown contains 2 actions max

The Customer sidebar's settings cog opens a dropdown with up to two options:

1. **Edit customer info on this order** (`order.customer_edit`) — purple pencil icon. Visible only in `pending` / `paid` / `disputed`.
2. **View customer profile** (`order.customer_view_profile`) — green user icon. Always visible when a customer is linked. Opens [[customers-details]] in a new tab.

When the order has NO linked customer (e.g., a guest checkout that never resolved to a customer record), the settings cog is **hidden entirely** — the customer-info area renders a flat read-only block with just the name + email shown.

## What the merchant can do here

### Side panel structure — what the merchant sees

The panel slides in from the right (`data-ajax-panel="true"`) with this layout:

**Top header bar** (fixed, sticky):
- Left: close X button (`data-dismiss="panel"`).
- Right (top corner): the **Update customer info** switch toggle — Bootstrap "switchButton" with on-label *"Update customer info"* (`order.label.update_customer_info`). When checked, sets the hidden `update_info` input to `"yes"`; when unchecked, sets it to `"no"` (default). What it actually does is on [[orders-customer-change-propagation]].
- Right: **Cancel** button (closes panel) + **Save** button (submits form, primary blue).

**Main fields area** (scrollable body):
- **First name** input — text, name=`customer_first_name`, prefilled with current value, auto-focus on open, placeholder = *"First name"* (`customer.help.first_name`), label *"First name"* (`customer.label.first_name`). Takes left half of the row (`col-xs-6`).
- **Last name** input — text, name=`customer_last_name`, prefilled, placeholder = *"Last name"* (`customer.help.last_name`), label *"Last name"* (`customer.label.last_name`). Takes right half (`col-xs-6`).

**Email block** (below the name row, full-width):
- **Email** input — email type, name=`customer_email`, prefilled, label *"Email"* (`customer.label.email`).
- Help text above the input (`customer.help.email`) — typically renders *"Enter the customer's email"*.
- A hidden `update_info` input — default value `"no"`, JavaScript flips to `"yes"` when the header switch is toggled on.

The panel renders via `\a view lookup (NOT a modal — a legacy commented-out `\a view lookup line indicates it used to be a modal but was migrated to a side panel for consistency with the address-edit flows).

## Settings & fields

Three editable inputs only — `customer_first_name`, `customer_last_name`, `customer_email` — plus the hidden `update_info` toggle field. Field-level semantics live on [[orders-customer-change-snapshot-model]] (what these fields mean) and [[orders-customer-change-validation]] (required + max-191 rules). Phone is NOT in this panel.

## Business rules

### After-save behaviour — partial reloads, not full page refresh

On successful save, the form's JS handler triggers `cc.ajax.reload` on TWO sub-panels of [[orders-details]]:

- `#order_customer` — the entire Customer sidebar card reloads (showing the new name / email).
- `#order_history` — the order history timeline reloads (showing the new `order_customer_edit` entry — see [[orders-history]]).

The panel itself does NOT auto-close after save in the template — the merchant clicks Cancel / X to dismiss it. (The standard `ajaxForm` behaviour may auto-dismiss in some configurations — verify on a live store.)

The success toast reads: *"Customer info edited successfully"* (`order.succ.customer_edit_success`).

### Smarty + jQuery + AJAX panel

- Panel opens via `data-ajax-panel` (slide-from-right).
- Form submits via `ajaxForm`.
- Toggle: jQuery `switchButton` plugin with on/off labels.
- After-save: triggers `cc.ajax.reload` on `#order_customer` and `#order_history` sub-panels.

## Related

- [[orders-customer-change]] — hub.
- [[orders-details]] — parent page (Customer sidebar card, sub-panels `#order_customer` / `#order_history`).
- [[orders-address-edit]] — same side-panel UX; where customer phone is edited.
- [[customers-details]] — opened by "View customer profile" in a new tab.
- [[orders-history]] — `order_customer_edit` entry that appears after save.

## Open questions

None.
