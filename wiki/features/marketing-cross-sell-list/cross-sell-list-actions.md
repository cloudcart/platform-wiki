---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → Cross-Sell List → Actions & UI"
route_name: cross-sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross-Sell list actions", "Cross-Sell bulk actions", "Cross-Sell add button", "Cross-Sell status filter", "Cross-Sell list UI surfaces"]
tags: [marketing, cross-sell, list, bulk, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-cross-sell-list]]. See the hub for the other aspects (grid & metrics, validation, plan budget).

# Cross-Sell List — actions & UI surfaces

## Purpose

This aspect documents **everything the merchant DOES from the list**: creating an offer, editing one, the per-row Active toggle, bulk delete, the status filter, the empty state, and the full inventory of UI surfaces (in-app navigations and confirm dialogs — the sub-flows open the offer's diagram page rather than in-page modals).

## Where to find it

Sidebar → Marketing → **Cross-Sell** (`/admin/marketing-new/cross-sell`). All actions live on the list page itself — the Add button (top-right), the per-row controls, the checkbox column (for bulk delete), and the filter bar.

## What the merchant can do here

### Create a new Cross-Sell offer

The "**Add Cross Sell**" button in the top-right (label *"Add Cross Sell"* + a remaining-slots counter) opens the **offer editor** for a new offer. A Cross-Sell offer configures **6 selectable trigger events** (`add_to_cart`, `cart`, `checkout`, `checkout_select_payment`, `checkout_select_shipping`, `return_page`) plus target and action conditions — see [[marketing-cross-sell]] for the full field set and [[cross-sell-list-validation]] for the required fields.

### Edit an existing offer

Click the row title → opens the offer's **diagram page** (`/admin/marketing-new/cross-sell/diagram/:id`) — a summary card of that single offer (its target-condition groups + action groups). Editing happens via the **Edit** button there, which opens the offer's edit modal (see [[marketing-up-sell-diagram]] for the page shape). Each offer is standalone — there is no tree of mixed nodes to edit.

### Toggle active per row

The per-row Active switch flips that offer's activity flag (a status update on the single offer record). Each offer is independent — there is no tree/subtree cascade.

### Bulk delete

Ticking rows enables the table's **bulk delete** (with a confirmation prompt). This is the only bulk action — there is **no** bulk activate / deactivate / duplicate. Deleting an offer that has legacy child offers attached also removes those children (the Tree delete hook); offers created in the current UI are standalone, so delete affects just that offer.

### Filter the list

The only filter exposed is **Status**: *"-- All --"* (default), **Active** (`filter.active`), **Inactive** (`filter.inactive`), plus an **Event** filter (the 6 trigger events). There is no target-product filter and no date-range filter on the list.

### Empty state

Shows the title *"You haven't added any Cross Sell yet"* (`global.notify.no_records_yet`), the info line *"Add your first Cross Sell to get started"* (`global.notify.no_records_info`), and a help link pointing at the merchant's support URL.

### What the merchant CANNOT do here

- **Open an inline create form** — the Add button opens the offer editor.
- **See which products an offer targets** at a glance — must open the offer to inspect its targets / actions.
- **Bulk activate / deactivate / duplicate** — the only bulk action is delete.
- **Inline-edit row data** — the row is fully read-only.
- **Export the list** — no export button.

## Settings & fields

This aspect carries no editable settings of its own — every offer field is configured inside the diagram editor and validated per [[cross-sell-list-validation]]. The only list-page control with a value is the **Status filter** dropdown (All / Active / Inactive).

## Business rules

### UI surfaces — page-level navigations, not modals

The Cross-Sell List is a **single-page list view**; its sub-flows are in-app navigations (to the diagram editor) or dropdown menus rather than modals:

| Surface | Where | Notes |
|---|---|---|
| **Add Cross Sell** button | Top-right (with remaining-slot counter) | Opens the offer editor for a new offer. |
| **Filter bar** | Top of grid | Status + Event dropdowns. |
| **Bulk delete** | After ticking rows | Delete only, with a confirmation prompt. |
| **Row title link** | Each row | Opens the offer's diagram page. |
| **Active toggle** | Status column | Single-record status update — no cascade, no modal. |
| **Empty state** | Whole page when list is empty | Title / info / help link. |

### Delete confirmation

Bulk delete shows a confirmation dialog (*"Are you sure you want to delete the selected records?"*) before running. Deleting a record also removes any legacy child offers attached under it (the Tree delete hook).

### Remaining-slot counter

The "(N remaining)" label in the Add button is fed by an AJAX call to `admin.common.remaining/cross_sell` on page load. When 0, server-side save still rejects new Cross-Sell creates with a plan-limit error — see [[cross-sell-list-plan-budget]].

## Related

- [[marketing-cross-sell-list]] — hub.
- [[marketing-cross-sell]] — the engine reached via the Add / row-title diagram links (events, targets, actions).
- [[marketing-up-sell-diagram]] — the visual diagram editor the Add button and row title route into.
- [[marketing-up-sell-list]] — sister list with the same bulk / filter / empty-state pattern.

## Open questions

No outstanding questions.
