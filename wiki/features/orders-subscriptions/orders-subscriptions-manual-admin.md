---
type: feature
nav_path: "Orders → Subscriptions → Manual admin actions"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Manual subscription create", "VIP subscription", "Gift subscription", "Add Extra Days", "Add additional days", "Double-days quirk", "Unlimited flip"]
tags: [administration, membership, orders, subscriptions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Subscriptions — manual admin actions (create, extra days)

## Purpose

This page covers the **admin-initiated** subscription paths: manually creating a subscription (VIP / gift cases) and adding bonus days to an existing one (compensation). Both bypass the automatic order-driven engine in [[orders-subscriptions-auto-lifecycle]]. It also documents the two surprising behaviours support is most likely to be asked about — the same-customer "double-days" effect and the unlimited-flip edge.

> Part of [[orders-subscriptions]]. See the hub for the other aspects (overview list, auto-lifecycle, status model, integration).

## Where to find it

Both actions live on the overview list ([[orders-subscriptions-overview]]):

- **+ Create new** (top-right) → *Add Subscription* modal.
- **+ Additional days** (per row, only when the row has an expiry date) → *Additional days* modal.

## What the merchant can do here

- Manually grant a customer access to a page for a chosen number of days (VIP / gift / compensation), without the customer placing an order.
- Add extra bonus days to a customer's existing subscription.

The modal fields and validation/toast strings are documented on [[orders-subscriptions-overview]]; this page covers what the actions *do* to the underlying record.

## Settings & fields

| Action | Endpoint | Inputs | Notes |
|--------|----------|--------|-------|
| Manual create | `POST /admin/api/membership/create` | `customer_id`, `page_id`, `days` (max 3652 = 10 years) | No product picker → `product_id` is NULL. |
| Add extra days | `POST /admin/api/membership/add-extra-days` | `id`, `extra_days` (UI cap 365) | Backend has no 365 cap. |

## Business rules

### Manual VIP / gift creation — same-customer extend semantics

When the merchant manually creates a subscription via the **Create** action:

- Required fields: `customer_id`, `page_id`, `days` (max 3652 = 10 years).
- If the customer already has a subscription for that (customer + page):
  - If expired → resets expiry to today + days.
  - If still active → EXTENDS expiry by days.
- If `days = 0` → creates an UNLIMITED subscription (expiry = NULL — see [[orders-subscriptions-status-model]]).

### The double-days quirk on an existing subscription

Hidden quirk in the create endpoint: when the customer already has a row for the same `(customer_id, page_id)`, the controller adds the days TWICE — once into the local Carbon variable and once on the update. Net effect: a manual create on an already-active subscription adds `days * 2`, not `days`. Merchants noticing *"I added 10 days and got 20"* should re-issue a smaller bump or use **Add Extra Days** instead. (verify — quirk observed in the create flow; reconfirm against current backend before quoting to a merchant.)

### Add-extra-days — admin-only bonus

The Add Extra Days action:

- `extra_days = 0` → clears the expiry → flips to UNLIMITED.
- `extra_days > 0` → adds to the existing expiry (or starts from today if no expiry was set).
- `extra_days < 0` (negative) → accepted at the API level; the UI's `min=0` blocks it via the form, but a direct API call subtracts days.

### The unlimited-flip is developer-only via the UI

The Additional days modal's Save button stays disabled when the field is `0` (falsy in JS), so the "flip to unlimited" path (`extra_days = 0`) is NOT reachable through the modal — only via a direct API call. From the merchant's perspective the unlimited flip is a developer-only feature; to grant unlimited access through the UI, the merchant uses the manual **Create** action with `days = 0` instead.

### The modal cap is UI-only

The Additional days modal caps a single bump at 365 days, but the backend enforces no such cap — API integrators can send larger values. The manual Create action caps at 3652 days (10 years) both in the UI and the validation.

## Related

- [[orders-subscriptions]] — hub.
- [[orders-subscriptions-overview]] — the modals + validation/toast strings these actions use.
- [[orders-subscriptions-auto-lifecycle]] — the order-driven engine that shares the same extend semantics.
- [[orders-subscriptions-status-model]] — what `expired = NULL` (unlimited) means downstream.

## Open questions

- The `days * 2` double-count on same-customer manual create is flagged `(verify)` — reconfirm against current backend before quoting a merchant.
