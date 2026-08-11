---
type: feature
nav_path: "Orders → Abandoned → Plan gates"
route_name: admin.abandoned.list
route_path: /admin/abandoned
aliases: ["Abandoned plan gates", "Abandoned plan features", "abandoned_orders gate", "abandoned_notification gate", "test_mail gate", "Лимити на изоставени поръчки"]
tags: [orders, abandoned, plan-gates, cart-recovery]
plan_gates: ["abandoned_orders", "abandoned_orders_info", "abandoned_notification", "test_mail"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (list view, detail view, eligibility, restore link, auto-recovery, cart lifecycle).

# Abandoned carts — Plan gates

## Purpose

The abandoned-cart cluster is gated by **four plan-feature keys**: three specific to abandoned recovery (`abandoned_orders`, `abandoned_orders_info`, `abandoned_notification`) plus the cross-cutting `test_mail` feature. This page is the catalogue of each gate's shape, effect, and behaviour on cap exhaustion — including the rarely-documented detail that the send counter is a **permanent setting** and does NOT reset on plan renewal.

## Where to find it

Not a screen. The gates apply on:

- The route `/admin/abandoned` (hidden when `abandoned_orders` fires).
- The Send action across [[orders-abandoned-list-view]], [[orders-abandoned-detail-view]], and [[orders-abandoned-auto-recovery]] (gated by `abandoned_notification`).
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
| `abandoned_notification` | Numeric (sends / period; cap counted via `plan.count.email.abandoned_notification`) | The **Send restore link** action across all entry points (manual single-cart, bulk, and the scheduled 3-minute auto-job) checks the platform code BEFORE dispatching the email. When the cap is exhausted, the merchant sees a plan-upgrade prompt with the feature name and current usage count instead of the email being sent. |
| `test_mail` | Boolean (per-cart Send button + global mail suppression) | On [[orders-abandoned-detail-view]], the per-cart Send button is REPLACED with a disabled button styled in purple with a tooltip explaining the plan limit and listing the eligible plans (`order.send_abonded_order_error` + the platform code). The `test_mail` plan feature ALSO acts as a **global mail-suppression gate** at the email-send layer: when disabled, ALL customer-facing emails to addresses other than the store's `site_email` are silently dropped. So even if the merchant somehow triggered the abandoned-cart email via the API on a `test_mail = no` plan, the customer would NOT receive it. |

## Business rules

### The dashboard counter (Abandoned count: X)

The counter at the top of [[orders-abandoned-list-view]] (*"Abandoned count: X"*) and the dashboard tile both read from the same value as `plan.count.email.abandoned_notification`. The counter is the running total of restore-link emails sent — manual + bulk + auto-job combined.

### Plan counter persists even when plan resets

The `plan.count.email.abandoned_notification` counter is stored as a **permanent setting**, NOT bound to the plan period. So when the merchant's plan renews or upgrades, the counter does NOT reset to zero — it keeps incrementing across the lifetime of the store.

The plan quota check compares the configured cap against this running total. (To reset the counter requires platform-staff intervention.) This surprises merchants who expect "monthly quota" semantics — for stores at the cap, upgrading the plan doesn't automatically unblock sends unless the new plan's `abandoned_notification` cap exceeds the existing counter value.

The counter persistence is shared with [[apps]] — when external recovery providers (e.g., Mobica) integrate into the plan-feature flow, their sends also increment the same counter and respect the same cap.

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

### Bulk + auto-job + per-cart all increment the same counter

Every path that emits a restore-link email increments `plan.count.email.abandoned_notification` by 1 per email actually sent (not per cart attempted):

- Bulk Send from [[orders-abandoned-list-view]] → increments by the number of carts that pass eligibility and aren't already in `date_sent`.
- Per-cart Send from [[orders-abandoned-detail-view]] → increments by 1 on success (resends count too, since the per-cart endpoint bypasses the `date_sent` check).
- Scheduled auto-job from [[orders-abandoned-auto-recovery]] → increments by 1 per cart sent per cycle.

The counter does NOT increment when eligibility fails and the cart is silently deleted — only successful Send + queue dispatch counts.

## Plan gates

(This page IS the plan-gates catalogue.) See `plan_gates` in frontmatter.

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-list-view]] — sees the counter + the bulk Send cap check.
- [[orders-abandoned-detail-view]] — `test_mail` gating of the per-cart Send button.
- [[orders-abandoned-restore-link]] — the action that increments the counter.
- [[orders-abandoned-auto-recovery]] — the scheduled job that also checks the cap.
- [[plan-features]] — upsell landing the `abandoned_orders` gate redirects to.
- [[plan-gates]] — model of how plan-feature keys gate behaviour.
- [[plan-vs-feature-pack]] — feature packs that extend numeric caps without a full plan upgrade.
- [[orders]] — dashboard tile controlled by `abandoned_orders_info`.

## Open questions

None.
