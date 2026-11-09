---
type: feature
nav_path: "Orders → Abandoned → Plan gates"
route_name: admin.abandoned.list
route_path: /admin/abandoned
aliases: ["Abandoned plan gates", "Abandoned plan features", "abandoned_orders gate", "abandoned_notification gate", "test_mail gate", "Лимити на изоставени поръчки"]
tags: [orders, abandoned, plan-gates, cart-recovery]
plan_gates: ["abandoned_orders", "abandoned_orders_info", "abandoned_notification", "test_mail"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (list view, detail view, eligibility, restore link, auto-recovery, cart lifecycle).

# Abandoned carts — Plan gates

## Purpose

The abandoned-cart cluster is gated by **four plan-feature keys**: three specific to abandoned recovery (`abandoned_orders`, `abandoned_orders_info`, `abandoned_notification`) plus the cross-cutting `test_mail` feature. This page is the catalogue of each gate's shape, effect, and behaviour on cap exhaustion — including how the send counter runs **per plan year**.

## Where to find it

Not a screen. The gates apply on:

- The route `/admin/abandoned` (hidden when `abandoned_orders` fires).
- The Send action on [[orders-abandoned-detail-view]] and the job on [[orders-abandoned-auto-recovery]] (gated by `abandoned_notification`).
- The detail-view Send button (additionally gated by `test_mail`).
- The dashboard tile (controlled by `abandoned_orders_info` — see [[orders]]).

## What the merchant can do here

Nothing on this page directly — observing gate effects:

- Upgrade plan to unlock `abandoned_orders` access (when the route-level redirect fires).
- Upgrade plan or buy a feature pack to extend `abandoned_notification` capacity (numeric gate; see [[plan-vs-feature-pack]]).
- Toggle `test_mail` indirectly via plan upgrade — `test_mail` is part of every paid plan; it's primarily disabled on free / starter plans.

## Settings & fields

### The four gate keys (verbatim)

| Key | Shape | What it controls |
|---|---|---|
| `abandoned_orders` | Access gate (URL `abandoned`) | The `/admin/abandoned` route. Registered under `restrict.access` in the platform code. When the merchant's plan lacks this feature, the platform's plan middleware blocks the page entirely and redirects to [[plan-features]] for upsell. The sidebar entry is hidden. The platform's abandoned-cart controller ALSO defensively re-runs the plan check via `planMessage('abandoned_orders')` before rendering the list, so a direct URL hit produces the same redirect. |
| `abandoned_orders_info` | Boolean (dashboard counter only) | Controls the abandoned-orders count badge on the admin dashboard (in [[orders]] dashboard tile). When disabled, the dashboard's abandoned tile is null / hidden — does NOT affect this list page directly. |
| `abandoned_notification` | Numeric (sends per plan year; counted in `plan.count.email.abandoned_notification`) | The single-cart **Send** action and the scheduled 3-minute auto-job check the remaining allowance BEFORE dispatching the email. When the cap is exhausted, the single-cart Send shows a plan-upgrade prompt with the feature name and current usage count; the auto-job stops sending, and the reminder is later switched off (see below). |
| `test_mail` | Boolean (per-cart Send button + global mail suppression) | On [[orders-abandoned-detail-view]], the per-cart Send button is REPLACED with a disabled button styled in purple with a tooltip explaining the plan limit and listing the eligible plans (`order.send_abonded_order_error` + the platform code). The `test_mail` plan feature ALSO acts as a **global mail-suppression gate** at the email-send layer: when disabled, ALL customer-facing emails to addresses other than the store's `site_email` are silently dropped. So even if the merchant somehow triggered the abandoned-cart email via the API on a `test_mail = no` plan, the customer would NOT receive it. |

## Business rules

### The list counter (Total sent messages: X)

The counter at the top of [[orders-abandoned-list-view]] (*"Total sent messages: X"*, BG *"Общо изпратени съобщения: X"*) shows the count for the current plan year, the same value the plan limit is checked against.

### The counter runs per plan year

The allowance is **yearly on every billing period**, monthly plans included. The year runs from the plan purchase date (bought 15 March: 15 March to 15 March). A store with no plan subscription (free, trial) counts by calendar year.

The count restarts from zero once a later plan year starts; no scheduled job resets it, the count is matched to the current plan year whenever it is read or a send is counted. A plan renewal alone does not reset it. Buying a different plan keeps the same year and the same count, and the new plan's `abandoned_notification` cap applies to the count so far: for a store at the cap, an upgrade unblocks sends only when the new cap exceeds the count. Full rules: [[abandoned-cart-plan-quota]].

The limit is the plan's `abandoned_notification` value plus any paid feature packs for it.

### At the cap the reminder is switched off

A platform plan check runs every 12 hours. When the allowance is used up and **Abandoned cart reminder** is ON, it switches the reminder OFF ([[settings-cart-abandoned-reminder]]) and posts an Important alert in [[notifications]]. Nothing turns it back on: after a new plan year or a feature pack, the merchant must switch it on again. Details: [[abandoned-cart-plan-quota]].

### Numeric vs access — different upsell paths

- **Access gate `abandoned_orders`** fires → merchant lands on [[plan-features]] for upsell. The remediation is a plan upgrade.
- **Numeric gate `abandoned_notification`** fires → merchant sees a plan-prompt naming the feature + current usage. The remediation is a plan upgrade OR a feature pack purchase ([[plan-vs-feature-pack]]).
- **Dashboard gate `abandoned_orders_info`** — boolean dashboard-counter only; doesn't impact send behaviour.
- **`test_mail` gate** — when OFF, the per-cart Send button is disabled with a tooltip; no upsell page renders.

### Plan-disabled landing page (legacy fallback)

When the merchant's plan does NOT have `abandoned_orders`, the platform has a dedicated plan-upsell page (`abandoned/disabled.tpl`) that COULD be served INSTEAD of the list. The page shows:

- Heading: *"To use Abandoned cart you need to upgrade to Advanced or Professional"* (`order.to_use_abandoned_upgrade_advanced_or_professional`).
- Secondary message: *"Your current plan does not support this feature"* (`order.plan_does_not_support_abandoned`).
- An **Upgrade plan** button (green).
- A help-box at the bottom: *"Need help?"* with a link to the manual.

This disabled-page template exists in the codebase but the controller's plan middleware (`abandoned_orders` gate) typically redirects to [[plan-features]] for upsell instead — the disabled page is a fallback for legacy gating paths and rarely renders in practice.

### What the counter counts

`plan.count.email.abandoned_notification` goes up by 1 per email actually sent (not per cart attempted):

- Per-cart Send from [[orders-abandoned-detail-view]] → increments by 1 on success (resends count too, since the per-cart endpoint skips the `date_sent` check).
- Scheduled auto-job from [[orders-abandoned-auto-recovery]] → increments by 1 per cart sent per cycle.
- The Admin GraphQL `sendRestoreEmail` mutation → increments by 1 on success.
- Bulk **Send restore link** from the list → does **not** increment and does not check the allowance.

A cart dropped without sending (no e-mail, no products, already ordered) does not count.

## Plan gates

(This page IS the plan-gates catalogue.) See `plan_gates` in frontmatter.

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-list-view]] — shows the counter.
- [[orders-abandoned-detail-view]] — `test_mail` gating of the per-cart Send button.
- [[orders-abandoned-restore-link]] — the action that increments the counter.
- [[orders-abandoned-auto-recovery]] — the scheduled job that also checks the cap.
- [[plan-features]] — upsell landing the `abandoned_orders` gate redirects to.
- [[plan-gates]] — model of how plan-feature keys gate behaviour.
- [[abandoned-cart-plan-quota]] — the plan-year counter in full.
- [[plan-vs-feature-pack]] — feature packs that extend numeric caps without a full plan upgrade.
- [[orders]] — dashboard tile controlled by `abandoned_orders_info`.

## Open questions

None.
