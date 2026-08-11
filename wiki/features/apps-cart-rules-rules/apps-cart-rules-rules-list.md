---
type: feature
nav_path: "Apps → Cart Rules → Rules"
route_name: apps.cart-rules.settings
route_path: /admin/apps/cart-rules/rules
aliases: ["Cart Rules list", "Rules list", "Cart rules table", "Reorder cart rules", "Toggle cart rule"]
tags: [apps, marketing, automation, rules-engine, list]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---

# Cart Rules — the list table

> Part of [[apps-cart-rules-rules]]. See the hub for the other aspects (editor, AI generation, plan limits).

## Purpose

The **Cart Rules list** is the merchant's home for every promotional rule configured for [[apps-cart-rules]]. From this single table the merchant sees all rules at a glance, controls their evaluation order, toggles them on / off, opens any rule for editing, and reads per-rule performance stats. It is the landing screen of the Cart Rules app and the starting point for both manual rule creation and AI-assisted generation.

## Where to find it

**Sidebar → Apps → Cart Rules → Rules tab.**

Route: `/admin/apps/cart-rules/rules` (route name `apps.cart-rules.settings`). List data loads from GET `/api/cart-rules` (paginated, filterable).

## What the merchant can do here

- See all rules with name, status, date window, priority order, and per-rule stats.
- Reorder priority via drag-and-drop.
- Toggle a rule active / inactive without opening it.
- Open a rule for editing (click its name).
- Soft-delete a rule (with confirmation).
- Start a new rule manually (**+ New rule**) or via AI / template (**+ Generate with AI** — see [[apps-cart-rules-rules-ai]]).
- Standard filter / search / pagination.

### What the merchant CANNOT do here

- **Bulk-edit** multiple rules — there is no multi-select column or bulk-action toolbar (verified — no bulk-deactivate, bulk-set-date-window, or bulk-delete for seasonal cleanup).
- **Restore** a soft-deleted rule from the UI (`deleted_at` is set but recovery requires support / direct DB).
- **Duplicate / clone** a rule — neither the list nor the editor exposes a Clone affordance (verified). A variant must be rebuilt from scratch via **+ New rule**.
- **Export / import** rules between stores.
- **Preview** a rule against a fake cart — there is no simulator (verified). Workaround: save as Draft → briefly switch to Active → place a test order → switch back to Draft.

## Settings & fields

### The table

The rules are listed in **priority order**: highest `sort_order` at the top, evaluated first at checkout. Each row shows:

| Column | What it shows |
|---|---|
| **Name** | The merchant's internal label (`name`) + the customer-facing title (`title`). |
| **Stats** | Per-rule performance metrics (see below). |
| **Switch** | Instant active / inactive toggle. |
| **Delete** | Soft-delete with confirmation. |

### Top-level buttons

- **+ New rule** — opens the manual rule constructor (see [[apps-cart-rules-rules-editor]]).
- **+ Generate with AI** — opens the AI generation popup (see [[apps-cart-rules-rules-ai]]).
- Standard filter / search / pagination controls.

### Stats column

The tooltip on the chart icon displays three metrics (verified against backend):

- **Used** — number of times the rule has been triggered.
- **Orders amount** — total value of orders that matched the rule (money-formatted).
- **Discounted amount** — total discount given through this rule (money-formatted).

The date range can be adjusted via the page's date-range picker; the default is the standard period the picker presents on load. Stats accumulate after the rule is activated.

## Business rules

- **Drag-and-drop reorder is instant.** Dropping a rule fires POST `/api/cart-rules/sort` with the new order and persists immediately — no save step.
- **Sort order is normalized on every drag** (verified). The sort endpoint REVERSES the incoming ID list, then assigns `sort_order = index + 1` to each rule. After any drag-reorder, sort_order values are flattened to a clean 1, 2, 3, … sequence (highest at the top). Manually-edited sort_order gaps disappear after the first reorder.
- **Status switch is instant.** The toggle fires PUT `/api/cart-rules/{id}/status/{0|1}` immediately — no save step.
- **Soft-delete keeps the rule's data** (sets `deleted_at`) but it stops firing. Recovery requires support / direct DB.
- **Bulk actions are a feature gap** (verified). Every rule must be toggled, edited, or deleted individually.
- **Creating a new rule can be blocked at the plan cap.** When the merchant attempts a Create-new that would exceed `cart_rules_total`, a feature-upgrade modal opens instead of the editor — see [[apps-cart-rules-rules-plan-limits]].

## Related

- [[apps-cart-rules-rules]] — hub.
- [[apps-cart-rules]] — engine overview with complete taxonomy + business rules + examples.
- [[apps]] — App Store hub.
- [[marketing-discounts]] — simpler discount feature.
- [[cart-rule]] — the underlying rule entity.

## Open questions

None — all previously-flagged items resolved.
