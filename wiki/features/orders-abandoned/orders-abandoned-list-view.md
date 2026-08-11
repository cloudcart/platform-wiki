---
type: feature
nav_path: "Orders → Abandoned → List view"
route_name: admin.abandoned.list
route_path: /admin/abandoned
aliases: ["Abandoned list", "Abandoned cart list view", "Abandoned grid", "Abandoned empty state", "Списък с изоставени поръчки"]
tags: [orders, abandoned, cart-recovery, smarty, list-view]
plan_gates: ["abandoned_orders"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (detail view, eligibility, restore link, auto-recovery, plan gates, cart lifecycle).

# Abandoned carts — List view

## Purpose

The list grid at `/admin/abandoned` — the merchant's main entry point into the abandoned-cart cluster. Renders all abandoned carts that match the inactivity threshold, with filtering, sorting, bulk selection, and a dedicated empty-state when the store has zero abandoned carts.

## Where to find it

Sidebar → **Orders** → **Abandoned**.

## What the merchant can do here

### Header

- Page breadcrumb: *"Orders → Abandoned orders"*.
- Counter (top-right): *"Abandoned count: X"* — running total of restore-link emails sent since plan-feature tracking began (the same value as `plan.count.email.abandoned_notification`; see [[orders-abandoned-plan-gates]]).

### List columns (4)

| Column | Sortable | Notes |
|--------|----------|-------|
| **Abandoned #** | No | Cart ID + customer / subscriber summary (name + group + total orders count). Clickable — opens [[orders-abandoned-detail-view]]. |
| **Date updated** | Yes | When the cart was last touched. Used by the recovery threshold timer. |
| **Products** | No | How many distinct line items in the cart. |
| **Quantity** | No | Total quantity across all line items. |

**Sort fields — only 1 sortable column.** Despite 4 visible columns, only **Date updated** is sortable (header has `sorting` class). The other three carry `data-sort="no"`. Default sort is `id DESC` (newest first) — the grid mapping converts the URL field `abandoned` to the DB column `id`, and `date_last_updated` to `updated_at`.

### Filters (4)

| Filter | Operator | Notes |
|--------|----------|-------|
| **Customer** | Autocomplete | Pick from the customer list — useful for "did this customer leave a cart recently?". |
| **Customer group** | Autocomplete | Filter by customer-group membership. |
| **Date added** | Exactly / Before / After | Date picker (no time, day-level). |
| **Date updated** | Exactly / Before / After | Date picker — when was the cart LAST modified. |

A **Total price** filter exists in the template but is commented out — not exposed to the merchant.

### Bulk actions — exactly 2

The merchant selects one or multiple carts via checkboxes, then chooses from the bulk dropdown:

| Action | What it does |
|--------|--------------|
| **Send restore link** | Calls `admin.abandoned.sendBulk` POST with selected IDs. No confirm dialog. Returns *"X emails sent"* (`order.succ.abandoned_%d_emails_sent`) or *"No emails were sent"* (`order.err.abandoned_no_emails_sent`). Silently skips carts that fail eligibility or already have a `date_sent` value — see [[orders-abandoned-eligibility]] + [[orders-abandoned-restore-link]]. |
| **Delete** | Calls `admin.bulk.delete` POST with the `abandoned` namespace. Confirm dialog: *"Are you sure you want to delete the selected abandoned cart(s)?"* (`order.abandoned.confirm.delete`). Soft-deletes the underlying cart record. |

There is NO bulk action to mark-as-converted, no bulk export, no bulk-set-status. The merchant either restores or deletes.

### Empty state

When the store has zero abandoned carts, the page does NOT show the filters / table at all. Instead it renders a dedicated empty-state screen with:

- A heading: *"No abandoned carts yet"* (`order.notify.abandoned_no_records_yet`).
- A description paragraph explaining the feature (`order.notify.abandoned_no_records_info`).
- A help-box at the bottom with a life-ring icon and a link: *"Need help getting started?"* — opens the CloudCart support URL in a new tab.

The merchant only sees the filter bar + grid + bulk actions once at least one abandoned cart exists.

### What the merchant CANNOT do here

- Edit the cart contents from this list — the cart is the customer's session state, not editable by the admin.
- Convert an abandoned cart to a manual order in one click — the merchant uses [[orders-add]] for that and references the cart manually.
- Bulk-export abandoned carts to CSV from this page — abandoned data is operational, not part of the orders export.
- Filter by total price (the operator UI is commented out in the template).
- Filter by which channel identified the subscriber (email vs Messenger).

## Settings & fields

The list itself has no per-page configuration. Behaviour is driven by:

- `abandoned_remainder_interval` — controls which carts qualify (see [[orders-abandoned-cart-lifecycle]]).
- `abandoned_orders` plan gate — controls whether the page renders at all (see [[orders-abandoned-plan-gates]]).

## Business rules

- **List query — joins, not a separate table.** The page reads from the platform's cart table, filtered to carts that haven't converted to orders. There is no separate "abandoned cart" table — the list applies a scope query against active carts.
- **Permission.** Standard `orders` permission section. Sidebar entry visible to admin/moderator roles with orders access.
- **Side effects** —
  - Send restore link → enqueues an outbound email via the notification system; increments `plan.count.email.abandoned_notification`. See [[orders-abandoned-restore-link]].
  - Delete → removes the cart record (the underlying cart entry is soft-deleted).
  - Filter / sort → read-only, no side effects.

## Plan gates

- `abandoned_orders` — Access gate. When the merchant's plan lacks it, the platform's plan middleware blocks the page entirely and redirects to [[plan-features]] upsell; the sidebar entry is hidden. See [[orders-abandoned-plan-gates]] for the full picture (including the legacy `abandoned/disabled.tpl` upsell template).

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-detail-view]] — clicking a row opens the cart in this view.
- [[orders-abandoned-eligibility]] — what blocks a Send when the merchant bulk-selects.
- [[orders-abandoned-cart-lifecycle]] — controls which carts appear in the grid.
- [[orders]] — parent module.
- [[plan-features]] — upsell page when the access gate fires.

## Open questions

None.
