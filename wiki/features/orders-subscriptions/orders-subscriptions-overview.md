---
type: feature
nav_path: "Orders → Subscriptions → Overview list"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Membership subscriptions list", "Subscriptions data-table", "Memberships overview tab", "Subscription filters", "Add Subscription modal", "Additional days modal", "Списък с абонаменти"]
tags: [administration, membership, orders, subscriptions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Subscriptions — overview list, filters & modals

## Purpose

This is the **overview-screen surface** of the Membership app: the data-table the merchant sees after the app is installed, the filters that scope it, and the three modals reachable from it (Add Subscription, Additional days, Delete). It documents *what the screen shows*; the engine that populates it lives in [[orders-subscriptions-auto-lifecycle]] and the admin actions are detailed in [[orders-subscriptions-manual-admin]].

> Part of [[orders-subscriptions]]. See the hub for the other aspects (auto-lifecycle, manual admin, status model, integration).

## Where to find it

Sidebar → **Orders** → **Subscriptions** (after the Membership app is installed). The list is the *Memberships* tab; a *Settings* sub-tab is auto-injected by the shared app-settings shell — see [[orders-subscriptions-settings]].

## What the merchant can do here

The Vue route `apps.membership.overview` mounts the same shell used for an app settings screen, with a top section that shows:

- App active/inactive status row (with activation toggle if not active).
- **+ Create new** button (top-right) — opens the *Add Subscription* modal (manual create — see [[orders-subscriptions-manual-admin]]).
- Tabs row with a single tab labelled *Memberships* (plus the auto-injected Settings tab).
- Below the tabs: the subscriptions data-table.

### Subscriptions data-table

| Column | Type | Notes |
|--------|------|-------|
| **Customer name** | Link | Click → opens customer details in new tab (`/admin/customers/details/<id>`). If the customer was deleted: shows *"Deleted user"*. |
| **Product** | Link | Click → opens product editor in new tab. If the row was created by the admin (no product): shows *"The subscription was created by an administrator"*. If the product was deleted: shows *"Deleted product"*. |
| **Page** | Link | Click → opens page builder in new tab (`/admin/marketing/pages/builder/<id>`). If the page was deleted: shows *"The page has been deleted"*. |
| **Active to** | Date | Formatted using the merchant's date format. If `expired_date` is empty: shows *"Unlimited"*. |
| **Status** | Badge | *Active* (green) when `is_active = true`; *Inactive* (grey) otherwise. Status is COMPUTED from `expired` — there is no stored status field (see [[orders-subscriptions-status-model]]). |
| (Actions) | Buttons | **+ Additional days** (only when `expired_date` is set — hidden for unlimited subscriptions) + **Delete** (X icon, with confirmation). |

Default sort: `id DESC`. The grid uses the shared data-table with mobile-enabled rendering.

### Filters (5)

| Filter key | Type | Operators | Source |
|-----------|------|-----------|--------|
| **Status** | Single-select | — | `Active` (1) / `Disabled` (0). |
| **Date** | Date + operator | `exactly` / `before` / `after` | Compares to the membership's `expired` date. |
| **Customer** | Multi-select (autocomplete) | `Includes` / `Does not include` | `/admin/autocomplete/customer`. |
| **Product** | Multi-select (autocomplete) | `Includes` / `Does not include` | `/admin/api/core/products/search`. |
| **Page** | Multi-select (autocomplete) | `Includes` / `Does not include` | `/admin/autocomplete/pages`. |

Free-text search via the table's query field matches: `id`, customer `email` / `first_name` / `last_name`, and product `name` (server-side `QueryFilter` columns).

Note: the Status filter only accepts Active / Disabled — `expired = NULL` (Unlimited) rows match neither bucket and are silently excluded when the filter is applied. See [[orders-subscriptions-status-model]].

## Settings & fields

The overview screen carries no persistent settings of its own — its controls are the Create / Additional days / Delete actions below. Persistent configuration lives on [[orders-subscriptions-settings]] and the product editor ([[products-products]]).

### Add Subscription modal (manual create)

Opens when the merchant clicks **+ Create new**. Right-side slide-in modal titled *"Add Subscription"*. Three fields, all required:

| Field | Type | Source | Validation |
|-------|------|--------|------------|
| **Select user** | Autocomplete | `/admin/api/core/customers/autocomplete` | Required. Error: *"You have not selected a user"*. |
| **Select page** | Autocomplete | `/admin/api/core/pages/search` | Required. Error: *"You have not selected any pages"*. |
| **Access days** | Number | min `0`, max `3652`, step `1` | Required. Error if blank: *"You have not selected any access days"*. Error if > 3652: *"Maximum number of days you can enter is 3652 (10 years)"*. Tooltip: *"If you want the user to get unlimited access in the field you need to enter 0"*. |

Footer buttons: **Close** (resets form, dismisses) and **Save** (submits to `POST /admin/api/membership/create`; success toast: *"Successfully added a subscription"*). The extend-vs-create semantics of Save are detailed in [[orders-subscriptions-manual-admin]].

### + Additional days modal

Opens when the merchant clicks **+ Additional days** on a row that has an expiry date. Modal titled *"Additional days"*. One field:

| Field | Type | Validation |
|-------|------|------------|
| **Add extra days** | Number | min `0`, max `365`, step `1`. Tooltip: *"Add additional free days to access the selected order pages. If you want the user to get unlimited access in the field you need to enter 0"*. |

Save button is **disabled while the field is empty / 0** (`:disabled="loading || !extra_days"`). The modal blocks backdrop-close during submission. Saving posts to `POST /admin/api/membership/add-extra-days` with `{id, extra_days}`. Success toast: *"You have successfully added additional free days"*. Error toast: *"An error occurred, please try again"*. The modal's 365-day cap is UI-only — see [[orders-subscriptions-manual-admin]].

### Delete confirmation (per-row)

Standard `DeleteComponent` confirmation popover (handled by the shared component, not a custom modal). On confirm calls `DELETE /admin/api/membership/delete/{id}`. Success toast: *"Deleted successfully"*. The row is removed client-side. If the row was the last on a page > 1, the table auto-pages back to the previous page.

## Business rules

### Status badge and date column are derived, not stored

The *Active to* date and *Status* badge are both projected from the single `expired` column. Empty `expired` → *Unlimited* + Active badge; future date → Active; past date → Inactive. There is no separate status field. See [[orders-subscriptions-status-model]].

### Manually-created rows have no product

There is no product picker in the Add Subscription modal — manually-created subscriptions have a NULL `product_id` and display as *"The subscription was created by an administrator"* in the Product column.

## Related

- [[orders-subscriptions]] — hub.
- [[orders-subscriptions-settings]] — the Settings sub-tab beside this list.
- [[products-products]] — product editor where pages + `days` are configured.

## Open questions

(none — per-row detailed management UX is deferred to a dedicated Membership-app page.)
