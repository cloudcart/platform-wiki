---
type: feature
nav_path: "Apps → Cart Rules → Cooldowns and lifecycle"
route_name: ""
route_path: ""
aliases: ["Cart rule lifecycle", "Cart rule date window", "Cart rule status", "Cart rule priority", "Cart rule activation", "No per-customer cooldown"]
tags: [apps, cart-rules, marketing, promotions, lifecycle, cooldowns, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects (conditions, actions, scoping, stacking, examples, known issues).

# Cart Rules — Cooldowns, lifecycle, and access

## Purpose

This aspect documents **when a rule is eligible to fire** and **who can manage it**. Three independent gates control eligibility: **status** (Active / Inactive / Draft), the **date window** (`active_from`, `active_to`), and **priority** (`sort_order`).

Critically, Cart Rules have **no per-customer cooldown, no per-cart cooldown, and no usage cap** — once active and in-window, a rule fires on every matching cart, repeatedly, as long as conditions match. The platform also keeps **no audit log** of edits.

## Where to find it

- **Status toggle** — toggle column on the rules list at `/admin/apps/cart-rules/rules`.
- **Date window + No-expire toggle** — rule editor at `/admin/apps/cart-rules/rules/create` (or `/edit/{id}`).
- **`sort_order`** — drag-and-drop on the rules list, or direct integer edit in the editor.
- **Soft-delete** — trash icon on the rules list row. No Restore button.

## What the merchant can do here

- Activate / deactivate a rule with one click (instant — no save step).
- Set a start and / or end date for eligibility.
- Toggle *No expire* to clear `active_to`.
- Reorder rules by drag-and-drop to change priority (normalises `sort_order` to `1..N` — see [[cart-rules-stacking]]).
- Soft-delete a rule via the trash icon.

## Settings & fields

### Status

| Value | Meaning |
|---|---|
| `1` Active | Fires when within its date window. |
| `0` Inactive | Exists but never fires. |
| `2` Draft | Half-built rule; never fires. **Cannot be set through the normal create/update flow** — see [[cart-rules-known-issues]]. |

In practice the lifecycle is **binary (Active / Inactive)** at the merchant level: the standard save payload validates `status` as `[0, 1]` only, and the toggle accepts only Active / Inactive, taking effect immediately with no save step.

### Date window

| Field | Format | Behaviour |
|---|---|---|
| `active_from` | `Y-m-d` | Optional start date. Blank = always-on at the start. |
| `active_to` | `Y-m-d` | Optional end date. Blank, or *No-expire* toggle on = never expires. |

Date comparison uses the **store's timezone**, NOT UTC. An *"active until 2026-05-31"* rule fires through the entire local day 2026-05-31, not until UTC midnight.

### `sort_order`

Integer 0–100,000. Higher = evaluated first. New rules without an explicit `sort_order` are auto-assigned `MAX(sort_order) + 1` — **top priority by default**, so the merchant must consciously lower priority on rules that should run after existing ones. Priority drives which rule consumes overlapping products first (see [[cart-rules-stacking]]).

### Soft-delete

Deleting a rule sets `deleted_at`; the data is preserved but the list and editor exclude trashed rows. There is **no Restore route or button** — recovery requires direct database access by CloudCart support, so **deletion is effectively permanent**. To "pause but keep", set `status` Inactive instead.

## Business rules

### Eligibility: date window pre-gates everything

The cart engine treats a rule as active only when ALL hold: `status = Active (1)`, **AND** `active_from` blank or ≤ today, **AND** `active_to` blank or ≥ today. A rule outside its date window is not evaluated at all, even if Active — so date windows are the right tool for *"this promo is only for Black Friday"*.

### No per-customer cooldown

There is **no per-customer cooldown**. A returning customer triggers the rule every time their cart matches, benefiting from the same promo repeatedly. For "one-time-per-customer" semantics, use a [[marketing-discounts-codes|discount code]] (single-use codes exist there, via the `single_use_per_customer` flag), or move the audience into a [[marketing-segments|Segment]] that removes the customer after one redemption — though this needs offline reconciliation, since Cart Rules don't update segment membership.

### No per-cart cooldown

There is **no per-cart cooldown**. The matcher runs **twice per cart-event** (notifications pass + matches pass — see [[cart-rules-stacking]]), re-evaluating from scratch each time. Every cart mutation re-fires the full matcher.

### No usage cap

Discounts have `max_uses` / `max_per_customer` (see [[marketing-discounts]]); Cart Rules do **not**. A rule fires forever until disabled, expired, or deleted. The per-rule "Used" stat is informational only.

### No A/B testing

There is no split-traffic mechanism — no concept of *"show rule A to 50%, rule B to 50%"*. Two rules with overlapping triggers both **evaluate**, but whether both **apply** depends on cart-level vs product-level stacking (see [[cart-rules-stacking]]). Workaround: define rules narrowly via `customer_group` triggers and split the audience with [[customers-custom-groups]].

### Permission — any admin can access (no per-role gate)

Cart Rules has no entry in the platform's section-permission map, so the access check falls through to "public". Practically, the Owner and any Moderator / Administrator / Custom-role admin can all access it, regardless of which permission sections their role carries. The only gates are (a) being logged in as an admin, and (b) the standard apps gate (the app installed and the plan permits it).

There is **no per-role "discount management" scope**. On multi-admin plans, every staff member with admin access can create, modify, and delete cart rules.

### No audit log of edits

The cart-rule row stores **only** `created_at`, `updated_at`, and `deleted_at` — **no actor identity** (no `created_by` / `updated_by` / `deleted_by`), no diff history, no revision log. If multiple admins edit the same rule, nothing records who changed what when, so *"who disabled this yesterday?"*, *"what was the discount before 5%?"*, and *"restore last week's config"* are all impossible. Merchants needing an audit trail must keep their own change log outside the platform.

### Plan-tier feature gates (four independent caps)

Cart Rules has FOUR separate plan limits, each hit independently:

| Plan feature | What it caps | Save fails at the cap with |
|---|---|---|
| `cart_rules_total` | Total number of rules | *"You have reached the maximum number of cart rules"* — existing rules still editable |
| `cart_rules_range` | Max **rows** per rule (default 20) | *"You may have a maximum of {n} rows"* |
| `cart_rules_conditions` | Max **row-triggers** per row (default 5) | *"You may have a maximum of {n} conditions"* |
| `cart_rules_actions` | Max **action-triggers** per row's action (default 5) | Same error message |

Counts are tracked live — the editor previews current count vs cap. **Each limit is individually expandable via feature packs.** Hitting any limit opens a checkout modal for that limit, where the merchant can buy a `cart_rules_*` pack for it (the cap rises immediately, no reload), upgrade to a tier with a larger base value, or cancel.

Packs follow the standard lifecycle on [[plan-features]] and [[plan-vs-feature-pack]] — they renew on their own cycle, survive plan upgrades / downgrades (the extended quota lasts the pack's remaining billing period), and stack on the plan base (effective cap = plan base + active packs). The four limits are independent: a `cart_rules_total` pack does NOT raise `cart_rules_range`. **Whether packs are purchasable depends on the plan's `enable_feature_pack` flag** — when OFF (typical on the lowest tier), the modal redirects to a plan-upgrade panel instead.

## Related

- [[apps-cart-rules]] — hub.
- [[cart-rule]] — Cart Rule entity; `status`, `active_from`, `active_to`, `sort_order`, `deleted_at` live here.
- [[cart-rules-stacking]] — how `sort_order` priority drives evaluation order + product consumption.
- [[cart-rules-known-issues]] — Draft is API-inaccessible; soft-deleted rules not restorable in UI.
- [[marketing-discounts]] / [[marketing-discounts-codes]] — alternatives with per-customer / per-code usage caps (Cart Rules has none).
- [[plan-features]] / [[plan-vs-feature-pack]] — four `cart_rules_*` caps + feature-pack expansion.
- [[customers-custom-groups]] — workaround for split-audience A/B testing.

## Open questions

None.
