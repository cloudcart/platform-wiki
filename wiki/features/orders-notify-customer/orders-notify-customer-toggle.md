---
type: feature
nav_path: "Orders → Order details → Notify customer → Toggle"
route_name: admin.orders.notify-customer
route_path: /admin/orders/action/other/:order_id/notify-customer
aliases: ["Notify customer toggle", "notify_customer switch", "Customer email switch", "Уведомявай клиента превключвател"]
tags: [orders, notification, customer, email, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[orders-notify-customer]]. See the hub for the other aspects (suppression scope, send-URL flow, manual re-send).

# Notify customer — the toggle

## Purpose

The toggle itself: the switch in the Customer sidebar card that flips the order's `notify_customer` boolean. This page covers the UI mechanic, where the switch sits on screen, its default states across the different order-creation paths, persistence, the lack of a bulk equivalent, and the lack of a history audit entry. What the flag actually suppresses is on [[orders-notify-customer-suppression-scope]].

## Where to find it

From [[orders-details]] → **Customer sidebar card** → **Notify customer** toggle.

Within the sidebar card, the toggle is in the `customer-mailbox` section (below the customer-info area, above the income / orders-total stat tiles). Layout is a `stack` with:
- Left (`stack-main`): label *"Notify customer"* + a Glyphicon info-sign tooltip.
- Right (`stack-addon`): the Bootstrap-switch styled checkbox.

The tooltip text is the localised `order.notify_customer_help` string — typically *"When OFF, the customer won't receive any automated emails about this order"*. The merchant can read it on hover without leaving the page.

Above the toggle, the same sidebar card hosts a **settings cog** (gear icon) whose dropdown exposes **Edit customer info on this order** ([[orders-customer-change]], visible only when status is `pending`, `paid`, or `disputed`) and **View customer profile** ([[customers-details]]). The toggle and the customer-edit action are two different entry points on the same card — the toggle is always visible, the edit action is status-conditional.

## What the merchant can do here

- **Flip the switch ON / OFF.** Click → AJAX GET to the `notify-customer` route → server saves `notify_customer = yes/no` → toggle re-renders with the new state. No confirmation dialog, no preview — it's instant.

The merchant CANNOT:
- **Bulk-set the flag** from the [[orders]] list. There is no bulk action for `notify_customer`. To silence many orders the merchant must click into each one individually, OR disable the notification at [[settings-statuses]] level (which affects ALL orders).
- **Suppress an already-fired email.** The toggle gates FUTURE notifications only.

## Settings & fields

### Field: `notify_customer`

| Value | Effect |
|-------|--------|
| **yes** | This order's status changes email the customer (subject to the other two gates — see [[orders-notify-customer-suppression-scope]]). |
| **no** | This order's automated emails are suppressed. |

Default state depends on how the order was created:

| Creation path | Default | Why |
|---|---|---|
| Storefront order (customer checkout) | **yes** | The customer expects confirmations. |
| Admin **Add order** flow ([[orders-add]]) | **no** | A test / manual order shouldn't accidentally email the customer just by saving. The flag flips to `1` only when the merchant explicitly sends a notification or commits a draft via the online-payment send flow — see [[orders-notify-customer-send-url]]. |
| Draft order | toggle **disabled** | Drafts have no customer-facing existence yet (see Business rules). |

## Business rules

### Per-order, persistent flag

The flag saves to the order and persists for its lifetime. Setting it OFF on a test order means NO status change on that order will ever fire an email. To silence ALL customer notifications globally (not per order), the merchant deactivates the status-change template or flips the store-wide kill switch on [[marketing-omnichannel-mails-list]] (see [[orders-notify-customer-suppression-scope]]) — a different, store-wide approach.

### Draft orders are disabled

The toggle carries a `disabled` attribute when the order has `is_draft = 1`. Drafts are NOT visible to the customer until "Created", so there is nothing to notify about. When the merchant commits a draft via the online-payment send flow, the platform flips `notify_customer = 1` so the customer receives the checkout-link email — see [[orders-notify-customer-send-url]].

### No history audit entry

Unlike status changes (which write to [[orders-history]] AND status-history), the toggle just updates the `notify_customer` column silently. There is no dedicated history entry — the merchant cannot later audit when the flag was flipped or by whom. So "why wasn't the expected email sent?" cannot be answered from the order timeline alone; the merchant must reason from the flag's current value plus the other two gates.

### Toggle UI mechanic — `data-ajax-bool` + GET request

The toggle is a Bootstrap-switch styled checkbox bound to:
- `name="notify_customer"` and `value="1"`.
- `checked` reflecting the current `order->notify_customer` value.
- `data-ajax-bool="{route('admin.orders.notify-customer', ['order_id' => $order->id])}"` — fires an AJAX GET when toggled.
- `disabled` when the order has `is_draft = 1`.

The route signature is `/admin/orders/action/other/{order_id}/notify-customer/{status?}` (status defaults to null). The `data-ajax-bool` framework appends the new boolean state to the URL and fires a no-body GET — no form payload, no confirm dialog. The response returns `{status: success, active: true|false}`, which the framework uses to update the checked state.

### Stat tiles below the toggle

Below the toggle the sidebar shows two read-only informational tiles: an **Income tile** (total income from this customer + completed-orders count) and an **Orders-total tile** (total orders price + count). Both are pulled from the customer record; clicking does nothing.

## Related

- [[orders-notify-customer]] — hub.
- [[orders-details]] — parent page; Customer sidebar card hosts the toggle.
- [[orders-customer-change]] — customer-edit action exposed by the same sidebar cog.
- [[customers-details]] — customer profile linked from the same cog.
- [[orders-add]] — Site-CP add-order flow defaults the flag to OFF.
- [[orders-history]] — confirms the flip is NOT recorded.
- [[orders]] — the list; has no bulk toggle for this flag.
- [[order]] — entity page.

## Open questions

None.
