---
type: feature
nav_path: "Customers → List view"
route_name: customers-list
route_path: /admin/customers
aliases: ["Customer list view", "Customers table", "Customers list columns", "Customers header actions", "Customer wallet balance column", "Reason for customer ban"]
tags: [customers, list, columns, header-actions]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers]]. See the hub for the other aspects (filters, bulk actions, create modal, ban flow, flags, lifetime KPIs).

# Customers — List view

## Purpose

The paginated, sortable table that renders every customer in the store. This aspect covers the **list table itself** — its columns, sort behaviour, header actions, per-row inline toggles, the sign-in-as-customer icon, and what the merchant cannot do from this view alone.

## Where to find it

Sidebar → **Customers**. Route: `/admin/customers`.

## What the merchant can do here

### Header actions

- **Export customers** — opens the two-factor confirmation, then exports the list with the filters that are applied. See [[customers-export]].
- **Import** — opens the two-factor confirmation, then the import window. See [[customers-import]].
- **+ Add customer** — opens the Add customer panel. See [[customers-create-modal]].

On mobile **Add customer** takes the full row, and export and import sit under the **…** menu.

### List table

- See all customers in a paginated, sortable, filterable table: newest first, 25 per page by default.
- Sort by Name, Completed orders, Revenue, Added date, Status, Marketing flag, Active flag.
- Click a customer's name to navigate to the **Customer details** page (`/admin/customers/details/:id`) — see [[customers-details]].

### Per-row inline toggles

- **Marketing** — toggle newsletter consent for that customer (changes immediately persist; toast confirms).
- **Active** — toggle whether the account is enabled.

Both toggles save immediately — see [[customers-flags]] for the immediate-save rule and the segment-recompute side effect that follows the Marketing toggle.

### Sign-in-as-customer icon

A **login icon** (tooltip *"Login to customer account"*) shows next to the customer's name for every customer outside the Guests group. Clicking it opens [[customers-sign-in]] at `GET /admin/api/core/customers/sign-in/{customer_id}`, and the merchant is logged in as that customer on the storefront in a new tab.

### Ban reason popup

On a banned row, click the **Banned** badge in the **Status** column. A popup titled *"Reason for customer ban"* shows the reason, with a **Close** button.

### What the merchant CANNOT do here

- Set a specific password from this view. That is on the customer's page, see [[customers-change-password]]. The bulk **Change password** action sends reset links.
- Restore deleted customers (no soft-delete recovery from the UI).

## Settings & fields

### List columns

| Column | Notes |
|--------|-------|
| **Name** | Full name as a link to Customer details, the login icon, the email below, and the customer group as a badge. Sortable. |
| **Completed orders** (`orders_completed`) | Sortable. Pulls from income summary — see [[customers-lifetime-kpis]]. |
| **Revenue** (`orders_completed_price`) | Sortable. Formatted as currency. |
| **Wallet balance** | The customer's [[virtual-wallet|Virtual Wallet]] balance. |
| **Added** (`date_added`) | When the customer record was created. Sortable. |
| **Status** | *Not banned* (green) or *Banned* (red, with an info icon that leads to the reason popup). Sortable. |
| **Marketing** | Inline toggle (yes/no). Sortable. |
| **Active** | Inline toggle (1/0). Sortable. |

## Business rules

### One customer record across the tabs

The customer's page loads the record once, and all its tabs (Overview, Orders, Addresses, etc. — see [[customers-details]]) read from it, so they stay in sync.

### Sign-in icon is hidden only for the Guests group

The "Login to customer account" icon next to the customer's name renders for every group except the platform-reserved Guests group (`group_id = 2`), including custom tiers like VIP or Wholesale.

## Related

- [[customers]] — hub.
- [[customers-details]] — per-customer detail page reached by clicking a row.
- [[customers-sign-in]] — impersonation reached by the inline login icon.
- [[customers-change-password]] — distinct "set a specific password" flow.
- [[customers-import]] / [[customers-export]] — the import and export opened from the header.

## Open questions

None.
