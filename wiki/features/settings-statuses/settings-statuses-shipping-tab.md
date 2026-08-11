---
type: feature
nav_path: "Settings → Statuses → Shipping"
route_name: shipping-statuses
route_path: /admin/settings/statuses/shipping
aliases: ["Shipping statuses tab", "Fulfillment statuses", "not_fulfilled", "fulfilled", "Статуси на доставки"]
tags: [settings, statuses, shipping, fulfillment]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-statuses]]. See the hub for the other taxonomies (orders, payment) and the cross-cutting mechanics (rename, custom codes, delete protection, permissions).

# Statuses — Shipping tab

## Purpose

The Shipping tab of [[settings-statuses]] is the management surface for the **fulfillment (shipping) status taxonomy** — the warehouse-state of an order. It is the smallest of the three taxonomies: exactly **2** built-in statuses, **rename-only** (no Add, no Delete). The merchant uses this tab when they want to customise how "not yet shipped" and "shipped" read on the order list, the customer's notification emails, and exports.

## Where to find it

Sidebar → Settings → **Statuses** → **Shipping** tab. Route: `/admin/settings/statuses/shipping`.

## What the merchant can do here

- See the 2 built-in shipping statuses: `not_fulfilled` and `fulfilled`.
- **Rename** either one by typing inline in the "New status name" column. Per-row Save button appears when the value differs from the saved value; click to commit (no auto-save on blur or Enter — same inline-edit UX as the Orders tab; see [[settings-statuses-orders-tab]]).

What the merchant **cannot** do on this tab:

- **No Add.** The `+ Add status` button is **hidden** on this tab. The shipping taxonomy is platform-defined and cannot be extended — the platform's fulfillment cascade hard-codes the two states. (If the merchant tries to invoke the Add modal anyway via a routing quirk, the client-side defensive check fires toast *"Only order statuses can be created"*; the backend route also returns 404 for `POST /statuses/shipping/create` due to the route-level `->where('type', 'order')` constraint on the Create endpoint — see [[settings-statuses-permissions-validation]].)
- **No Delete.** The Actions column does not render trash icons on this tab — built-in statuses are non-deletable, and there are no custom shipping statuses to delete (since none can be created).
- **No reorder.** The platform's order is fixed (`not_fulfilled` first, `fulfilled` second).
- **Cannot change the status code.** Only the display label.
- **Cannot manually change a shipping status on an order if a carrier-locked integration owns the fulfillment state.** Some shipping providers refuse manual status changes from the order page (the merchant must trigger waybill generation through the carrier app instead). The lang key `err.for_change_fulfillment_status_use_button` = "Моля, генерирайте товарителница за тази поръчка. Смяната на статуса от тук, не е възможен." surfaces this on [[orders-details]]. The taxonomy management here is unaffected — only the per-order change flow is locked. See [[orders-status-change-fulfillment-gate]].

## Settings & fields

| Column | Shows | Editable? | Notes |
|--------|-------|-----------|-------|
| **Current status name** (`translation`) | The original translated label (e.g., "Изпратена" for `fulfilled` in Bulgarian, via `shipping.status_<code>`). | No | Read-only display of the platform's default. |
| **New status name** (`new_name`) | The merchant's custom rename, or empty if unset. | Yes (inline) | Per-row Save button commits via `PATCH /statuses/shipping/update`. No auto-save on blur. |
| **Actions** | _(empty on this tab)_ | n/a | Trash icons not rendered — built-in statuses cannot be deleted. |

No modal. No bulk save. Each rename is its own API call.

## Business rules

### The 2 built-in shipping statuses

- `not_fulfilled` — the order is in the system but has not yet been shipped or handed off to a courier.
- `fulfilled` — the order has been shipped or handed off.

These are the only two values the platform's fulfillment state machine recognises. Apps that integrate with couriers may add finer-grained sub-states *(verify)* but those flow through the carrier app's own data layer, not this taxonomy.

### Why no Add / Delete

The fulfillment cascade is hard-coded throughout the platform — the Completed-transition gate on [[orders-status-change-transition-rules]], the waybill flow on [[orders-shipping-waybill]], the bulk Mark-as-completed action, the customer-email triggers, and the auto-fulfillment for digital goods all check for exactly `fulfilled` / `not_fulfilled`. A custom value would have no behaviour attached.

### Rename is a translation override

Same mechanic as Orders / Payment: the rename stores a row in the status-override table with `(type=shipping, status=<code>, name=<custom>)`. The platform reads this row first; if missing, it falls back to `shipping.status_<code>`. Clearing the field and saving deletes the override row entirely — see [[settings-statuses-rename-mechanic]].

### Rename does NOT affect the underlying code

Webhooks, exports, JSON-API v2 reads, and any code referencing a shipping status sees `fulfilled` / `not_fulfilled` regardless of the rename. Only the human-facing label changes.

### Bulgarian default label sample

- `shipping.status_fulfilled` → "Изпратена"

(`not_fulfilled` default label varies; check `lang/bg/shipping.php` for verification.) *(verify)*

### Backend write path

`PATCH /statuses/shipping/update` is the only mutating endpoint exposed for this tab. The Form Request layer validates: `status` required (the status code being renamed), `type` must be `shipping` (rejected as *"Invalid type"* otherwise). No name uniqueness check, no length cap. Full validation rules on [[settings-statuses-permissions-validation]].

## Related

- [[settings-statuses]] — hub.
- [[settings-statuses-rename-mechanic]] — how renames are stored as overrides.
- [[settings-statuses-permissions-validation]] — server-side validation + the route-level `type` constraint that gates Create / Delete out of this tab.
- [[shipping-status]] — entity page.
- [[orders-status-change-fulfillment-gate]] — the carrier-locked fulfillment-change rule on order details.
- [[orders-shipping-waybill]] — waybill generation drives the transition to `fulfilled`.
- [[order-status-workflow]] — how shipping status transitions interact with the order status workflow.

## Open questions

- The exact default label for `shipping.status_not_fulfilled` in Bulgarian was not captured in the source pass. *(verify)*
- Whether courier apps add any sub-states beyond `fulfilled` / `not_fulfilled` (or surface them only in the carrier app UI without touching this taxonomy). *(verify)*
