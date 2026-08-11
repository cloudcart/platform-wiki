---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → UpSell List → Row & bulk actions"
route_name: up-sell.list
route_path: /admin/marketing-new/up-sell
aliases: ["UpSell create", "UpSell edit", "UpSell active toggle", "UpSell delete", "UpSell bulk delete", "Действия върху UpSell оферта"]
tags: [marketing, upsell, list, actions, bulk]
plan_gates: ["upsells"]
created: 2026-06-10
updated: 2026-07-13
source_count: 4
---

> Part of [[marketing-up-sell-list]]. See the hub for the other aspects (table, validation, storefront firing, plan budget).

# UpSell List — create, edit & row / bulk actions

## Purpose

This aspect covers the **actions** the merchant takes from the UpSell List: creating a new offer, opening one to edit, toggling its Active state inline, and deleting. **Each offer is independent** — actions apply to a single offer record; there is no offer-chain cascade for status, and no duplicate action.

## Where to find it

All actions originate from the offer table at Sidebar → Marketing → **UpSell** (`/admin/marketing-new/up-sell`). Per-row actions sit on the row (title link, Active switch, delete); a checkbox column enables the table's built-in **bulk delete**.

## What the merchant can do here

### Create a new UpSell offer

The **"Add UpSell"** button (with a remaining-slots counter) opens the **offer editor** for a new offer — the create modal where the merchant picks the trigger product, the offer product, the trigger event, and the styling. See [[marketing-up-sell-diagram]] for the field set and [[upsell-list-plan-budget]] for the remaining-slots counter.

### Edit an existing offer

Click a row's title → the offer's **diagram page** (`/admin/marketing-new/up-sell/diagram/:id`) → the **Edit** button opens the edit modal. There is no separate row-level edit button.

### Toggle active per row

The Active column is a switch; toggling it updates **that single offer's** status (Active ↔ Inactive). It applies only to that offer — there is no chain / subtree cascade.

### Delete

Delete an offer from its row, or select rows with the checkboxes and use the table's **bulk delete**. Deletes confirm before running. Deleting an offer that has legacy child offers attached also removes those children (see Business rules).

### What the merchant CANNOT do here

- **Open an inline create form** — the Add button opens the offer editor (modal).
- **Duplicate an offer** — there is no duplicate action.
- **Bulk activate / deactivate / duplicate** — the only bulk action is delete.
- **Bulk-edit offer fields.**

## Settings & fields

The actions carry no editable settings of their own. The offer fields they create / toggle are documented on [[marketing-up-sell-diagram]] (the edit modal) and validated per [[upsell-list-validation]]; the metric columns are on [[upsell-list-table]].

## Business rules

### Each offer is independent

Status toggles and edits apply to one offer record. Unlike the retired multi-step builder, there is no chain to cascade through — toggling one offer never changes another.

### Delete removes attached legacy children

Deleting a record still removes any child offers wired underneath it (the tree delete hook). This only matters for offers created under the **old chain builder**; offers created in the current UI are standalone, so delete affects just that offer.

### No duplicate

There is no "duplicate offer" action; to make a similar offer the merchant creates a new one.

### Side effects on save

- A new offer becomes live the moment it is saved (if Active and within its active-from / active-to window — see [[upsell-list-validation]]).
- On the first qualifying cart event after save, the customer sees the popup (subject to the storefront gates — see [[upsell-list-storefront-firing]]).
- The `views` / `added_to_cart` / `total_cancel` counters are incremented storefront-side, not by these admin actions — see [[upsell-list-storefront-firing]].

## Related

- [[marketing-up-sell-list]] — hub.
- [[marketing-up-sell-diagram]] — create / edit open here (the offer editor).
- [[upsell-list-table]] — the table these actions operate on.
- [[upsell-list-validation]] — fields created by these actions.
- [[upsell-list-plan-budget]] — the remaining-slots counter on the Add button.

## Open questions

No outstanding questions.
