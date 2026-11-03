---
type: feature
nav_path: "Customers → Customer groups → Manage groups"
route_name: customers-custom-groups
route_path: /admin/customers/groups
aliases: ["Manage customer groups", "Add customer group", "Edit customer group", "Customer group modal", "Управление на клиентски групи"]
tags: [customers, groups, loyalty, tiers, crud]
plan_gates: ["customer_groups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Customer groups — manage (list + Add/Edit modal)

> Part of [[customers-custom-groups]]. See the hub for the other aspects (system groups, plan gating, integration, API).

## Purpose

The interactive surface of the Customer groups screen: the page header, the list table with its filter and sort, and the tiny Add / Edit modal where the merchant creates a group or renames an existing one. A group has exactly one editable field — its **Name** — so this is intentionally lightweight CRUD.

## Where to find it

Sidebar → Customers → **Customer groups** (`/admin/customers/groups`). The modal opens from the **+ Add customer group** header button or by clicking any row's **Name** cell.

## What the merchant can do here

### Header

- **X of Y groups used** chip — usage indicator. Y becomes ∞ when the merchant's plan tier has no cap. (Cap mechanics: [[customers-custom-groups-plan-gating]].)
- **Upgrade plan** button — opens the standard upgrade flow when more groups are needed.
- **+ Add customer group** button — opens the create modal. Disabled while the page is loading; if the merchant has hit the cap, clicking it opens the upgrade modal instead.

### List table

- All groups in a paginated table with **Name** (sortable, click to edit) and **Customers** count.
- Filter: **Has customers** — Yes / No (find empty groups for cleanup, or busy groups).
- Default sort: ID descending (newest first).
- Bulk-select rows for bulk delete (with layered protection — see [[customers-custom-groups-system-groups]]).

### Add / Edit group modal

A tiny **centred modal** (md size) with no header and no footer — the whole layout sits in the body as a single row. ESC-close is blocked, and backdrop-close is blocked while the modal is in its loading state.

| Element | Notes |
|---------|-------|
| Title row | *"Add Group"* — the same title for both Add and Edit (no edit-specific variant). |
| **Name** input | Required. Placeholder: *"E.g. Loyal, VIP"*. Must be unique. Server error surfaces inline below the input. |
| Horizontal rule | Separates form from buttons. |
| **Cancel** button | Ghost. Closes the modal and resets the form (clears the name, clears errors). Disabled during submit. |
| **Save** button | Primary. Shows a spinner during submit. On success: reload table + toast *"Saved successfully"* + close modal. |

Validation errors surfaced inline:

- *"Group name is required"* (empty).
- *"Group name already exists"* (duplicate, case-insensitive).
- *"Group name must not exceed 100 characters"* (server-side `max:100`).
- *"Group limit reached"* (plan-cap hit — see [[customers-custom-groups-plan-gating]]).
- *"Group name is reserved"* / *"Cannot edit default group"* (reserved-name + system-group protection — see [[customers-custom-groups-system-groups]]).

### How the Edit modal pre-fills

Clicking a row's **Name** passes that row's data to the page, which opens the modal pre-filled with the existing group name (and the group's id, so Save issues an update rather than a create). Closing the modal clears the staged row data back to empty, so the next **+ Add** opens a blank form.

## Settings & fields

### Per-row columns

| Column | Notes |
|--------|-------|
| **Name** | Sortable. Click → Edit modal. |
| **Customers** | Count of customers in the group. |

### Group model fields

| Field | Notes |
|-------|-------|
| **Name** | Required, unique (case-insensitive), max 100 characters. |
| (no other configurable fields on the group itself) | The group's behavioural effects come from cross-references in [[marketing-discounts]], [[marketing-segments]], and [[customers]] filters. |

## Business rules

- **Name is the only editable attribute.** There are no per-group settings beyond the name on this screen.
- **Uniqueness is case-insensitive** — *"VIP"* and *"vip"* collide.
- **Save side effect** — a created group is immediately available in the Customer-group dropdowns across the platform (Add Customer, discount targeting, segment rules, customer filter). See [[customers-custom-groups-integration]].
- **Legacy Vue page** — this is a legacy Vue page using a data-table and a BootstrapVue modal with the platform's settings wrapper; standard CRUD operations.
- **Permission** — Customers permission section; create / edit / delete require the corresponding write grant (see [[settings-staff]]).

## Related

- [[customers-custom-groups]] — hub.
- [[customers]] — parent list; bulk reassignment of customers between groups lives here.
- [[customer-group]] — entity page.
- [[marketing-discounts]] — discount targeting by customer group.
- [[marketing-segments]] — segment rules can use customer group as a field.
- [[settings-staff]] — moderator permission grants.

## Open questions

None.
