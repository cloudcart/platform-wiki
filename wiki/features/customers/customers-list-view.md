---
type: feature
nav_path: "Customers → List view"
route_name: customers-list.new
route_path: /admin/customers-new
aliases: ["Customer list view", "Customers table", "Customers list columns", "Customers header actions"]
tags: [customers, list, columns, header-actions]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers]]. See the hub for the other aspects (filters, bulk actions, create modal, ban flow, flags, lifetime KPIs).

# Customers — List view

## Purpose

The paginated, sortable table that renders every customer in the store. This aspect covers the **list table itself** — its columns, sort behaviour, header actions, per-row inline toggles, the sign-in-as-customer icon, and what the merchant cannot do from this view alone.

## Where to find it

Sidebar → **Customers**. Route: `/admin/customers-new`.

## What the merchant can do here

### Header actions

- **Export customers** — INTENDED: download the customer list (spinner shows during preparation). **In the modern Vue header this button's handler is an unimplemented stub (`console.log('Export customers')`) — clicking it does nothing yet.** See [[customers-export]] for the working (legacy) flow.
- **Import** — INTENDED: bulk-add customers from CSV. **In the modern Vue header this button's handler is an unimplemented stub (`console.log('Import customers')`) — clicking it does nothing yet.** See [[customers-import]] for the working (legacy) flow.
- **+ Add customer** — opens the Create Customer modal — see [[customers-create-modal]]. This one IS wired in the modern build.

### List table

- See all customers in a paginated, sortable, filterable table.
- Sort by Name, Completed orders, Revenue, Added date, Banned status, Marketing flag, Active flag.
- Click any row's name to navigate to the **Customer details** page (`/admin/customers-new/details/:id`) — see [[customers-details]].

### Per-row inline toggles

- **Marketing** — toggle newsletter consent for that customer (changes immediately persist; toast confirms).
- **Active** — toggle whether the account is enabled.

Both toggles save immediately — see [[customers-flags]] for the immediate-save rule and the segment-recompute side effect that follows the Marketing toggle.

### Sign-in-as-customer icon

The Name-column row component (`CustomersTableName.vue`) renders an extra **login-as-customer icon** next to the customer's name when the customer's `group_id !== 2` (i.e., not the Guest group). Clicking the icon opens [[customers-sign-in]] which calls `GET /admin/api/core/customers/sign-in/{customer_id}` → impersonation session created → the merchant is logged in as that customer on the storefront in a new tab. No 2FA gate; permission-gated by `customers`.

### What the merchant CANNOT do here

- See WHICH customers are in a particular customer group from this view alone (use the Customer groups filter — see [[customers-filters]] — then save the URL).
- Reset password by setting a specific new password from this view — see [[customers-change-password]] for that distinct flow; bulk and per-customer "Change password" only sends a reset link.
- Restore deleted customers (no soft-delete recovery from the UI).
- Use the bulk Ban / bulk Change-group / bulk Change-password handlers from the MODERN Vue listing — they are stubs in the current build. See [[customers-bulk-actions]] for the full status.

## Settings & fields

### List columns

| Column | Notes |
|--------|-------|
| **Name** | Full name + email shown below (custom component). Click → Customer details. Sortable. |
| **Completed orders** (`orders_completed`) | Sortable. Pulls from income summary — see [[customers-lifetime-kpis]]. |
| **Revenue** (`orders_completed_price`) | Sortable. Formatted as currency. |
| **Added** (`date_added`) | When the customer record was created. Sortable. |
| **Status** | Banned / Active badge (custom component). Sortable. |
| **Marketing** | Inline toggle (yes/no). Sortable. |
| **Active** | Inline toggle (1/0). Sortable. |

## Business rules

### Customer name + status row component

The Name column uses a custom rendering component that shows the avatar (if any), the full name, the email below, and an inline "Banned" / "Inactive" badge when applicable. So the merchant scanning the list sees status at a glance even without checking the dedicated Status column.

### Inline view of details inherits the modal context

When the merchant is on `/details/:id`, the same wrapper provides the customer's data to the child router-view via Vue provide/inject. So all detail sub-tabs (Overview, Orders, Addresses, etc. — see [[customers-details]]) read from one customer source and stay in sync.

### Sign-in icon is hidden ONLY for guest group (id=2) — verified

The "Login to customer account" icon next to the customer's name renders for every group EXCEPT the platform-reserved Guest group (`group_id = 2`). For all other groups (Regular, custom tiers like VIP/Wholesale), the icon renders unconditionally — no separate permission gate.

## Related

- [[customers]] — hub.
- [[customers-details]] — per-customer detail page reached by clicking a row.
- [[customers-sign-in]] — impersonation reached by the inline login icon.
- [[customers-change-password]] — distinct "set a specific password" flow.
- [[customers-import]] / [[customers-export]] — legacy bulk-IO flows linked from the header.

## Open questions

None.
