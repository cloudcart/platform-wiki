---
type: feature
nav_path: "Orders → Order details → Status → Status pill"
route_name: admin.orders.status.load
route_path: /admin/orders/action/status-load/:order_id
aliases: ["Order status pill", "Status badge", "Status dropdown", "Status chip", "Промяна на статус — chip"]
tags: [orders, status, ui, badge, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-status-change]]. See the hub for the other aspects (transition rules, side effects, notification, fulfillment gate, bulk, API).

# Order status change — Status pill

## Purpose

The colour-coded status chip in the breadcrumb of [[orders-details]] is the merchant's primary status-change surface. It does two things: it **displays** the current status (colour signals the status family at a glance) and it **opens** a Select2 dropdown that lists the available targets when clicked. The dropdown is lazy-loaded so the order-detail page renders fast — the merchant sees the badge immediately but the dropdown HTML is fetched only on click.

## Where to find it

Top of [[orders-details]], in the breadcrumb area — between the order number / date and the right-hand toolbar. Always present on non-draft orders; for draft orders the pill shows the "Draft" badge instead and clicking it offers only one transition (Cancelled).

The lazy fetch uses `data-box-ajax="{route('admin.orders.status.load')}"` on the pill container — the dropdown HTML is requested on demand. The 3-dot dropdown on the same page exposes one-click **Mark as completed** and **Cancel order** for the two most common transitions (see [[orders-status-change]] for visibility rules); both route through the same change-status endpoint.

## What the merchant can do here

### Read the current status at a glance

The pill colour signals the status family without reading text:

| Status | Colour |
|--------|--------|
| **completed** | Green (`badge-green`) |
| **paid** | Green (`badge-green`) |
| **pending** + fulfilled | Purple (`badge-purple`) |
| **pending** (not fulfilled) | Orange (`badge-orange`) |
| **cancelled** | Red (`badge-red`) |
| Archived | Gray (`badge-gray`) |
| Draft (`is_draft = 1`) | Gray (badge labelled "Draft") |
| Other (custom statuses) | Blue (`badge-blue`) |

Custom statuses always fall to `badge-blue`. There is NO UI in [[settings-statuses]] to override the badge colour for a custom status — the colour mapping is hard-coded per canonical-status name. `(verify)` if a future update exposes custom badge colours.

### Click to change status

Clicking the pill toggles the Select2 dropdown. The current status is pre-selected. Picking a new option fires the AJAX call to `admin.orders.change-status` immediately — there is no separate "save" step. After the change, the surrounding panels (summary, status, action buttons) reload.

### Dropdown contents — what the merchant actually sees

The dropdown renders these options (alphabetical):

- **Authorized** (`authorized`)
- **Cancelled** (`cancelled`)
- **Completed** (`completed`)
- **Fulfilled** (`fulfilled`) and **Not fulfilled** (`not_fulfilled`) — fulfillment statuses appended into the SAME dropdown
- **Paid** (`paid`)
- **Pending** (`pending`)
- **Refunded** (`refunded`)
- Plus every merchant-defined custom status from [[settings-statuses]] (type = `order`) not already in the canonical list above

The dropdown EXPLICITLY EXCLUDES five gateway-driven statuses: `chargebacked`, `disputed`, `timeouted`, `failed`, `voided`. These are removed via `unset` after the array is built — they're owned by the payment-provider integration and can't be set manually. So the merchant CAN flip an order to `authorized` or `fulfilled` manually from this dropdown, but CANNOT manually flip it to `failed` / `voided` / `disputed` / `chargebacked` / `timeouted`.

### Draft-order dropdown — only one option

For draft orders (`is_draft = 1`), the dropdown renders ONLY one option: **Cancelled**. The merchant can confirm-by-cancel a draft directly from the pill — no other transitions are offered until the draft is "Created" via the dedicated draft flow on [[orders-add]].

## Settings & fields

The pill itself owns no settings — it renders against:

- The canonical status-dropdown source (built-in 11 canonical statuses minus the 5 gateway-driven ones).
- Custom statuses from [[settings-statuses]] (the merchant adds / edits these in Settings → Statuses).
- The hard-coded colour mapping per canonical status name.

## Business rules

- The pill is read-only for moderators with read-only orders permission — the dropdown won't function (the change-status endpoint rejects the request). See [[settings-staff]] for the orders permission scope.
- Custom statuses bypass the badge-colour mapping and render as `badge-blue`. The colour cannot be changed.
- Fulfillment statuses appearing in the same dropdown as order statuses is intentional — the merchant can flip fulfillment from here on orders WITHOUT an external shipping provider, but the path is blocked for orders with a waybill attached. See [[orders-status-change-fulfillment-gate]].
- Picking the same status the order is already in is a no-op (no history row, no notification, no side effects).
- The dropdown does NOT enforce transition rules client-side — every option appears clickable. Hard gates are enforced on the SERVER and surface as an error toast. See [[orders-status-change-transition-rules]] for the gate catalogue.

## Programmatic access

The dropdown surface is admin-only. To change status programmatically use the JSON-API v2 PATCH endpoint — see [[orders-status-change-api]]. The API exposes the same set of valid targets the dropdown does (canonical statuses minus the 5 gateway-driven ones, plus custom statuses).

## Related

- [[orders-status-change]] — hub.
- [[orders-details]] — parent page hosting the pill.
- [[orders-details-header]] — header surface where the pill lives.
- [[settings-statuses]] — status taxonomy + custom statuses.
- [[orders-status-change-transition-rules]] — server-side gates the dropdown does NOT preview.
- [[orders-status-change-fulfillment-gate]] — why Fulfilled / Not fulfilled may be rejected for some orders.
- [[settings-staff]] — moderator permission scope.

## Open questions

- Whether merchants can override custom-status badge colours in a future update `(verify)`.
