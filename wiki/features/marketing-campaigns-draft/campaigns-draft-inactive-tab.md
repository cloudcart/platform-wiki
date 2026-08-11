---
type: feature
nav_path: "Marketing → Campaigns → Draft → Inactive tab"
route_name: campaigns-inactive
route_path: /admin/marketing-new/campaigns/inactive
aliases: ["Inactive campaigns tab", "Stopped campaigns list", "Paused campaigns", "Спрени кампании", "Неактивни кампании"]
tags: [marketing, campaigns, inactive, list]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Draft tab, entry paths, unsaved-changes guard, pre-flight checks, lifecycle actions).

# Inactive campaigns — the Inactive tab

## Purpose

The **Inactive** tab lists every campaign that WAS started and has now been stopped — `active = 0` AND `archived_at IS NULL`. Inactive campaigns retain their full history: enrolled subscribers, message logs, statistics, mid-funnel `progress` values. The tab answers the merchant question *"what's paused that I should resume?"*

A campaign can land here three ways:

- The merchant flipped the Status toggle from Active to Inactive on the Active tab.
- The channel-suspension cascade auto-stopped it (see [[marketing-channels]] + [[marketing-campaigns-banned-info]]).
- A regular campaign was explicitly inactivated by an admin or by completing its run.

The Inactive tab is the sibling of [[campaigns-draft-tab|the Draft tab]] on the four-tab campaigns list ([[marketing-campaigns]]).

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click the **Inactive** tab.

| Setting | Value |
|---------|-------|
| Route name | `campaigns-inactive` |
| Route path | `/admin/marketing-new/campaigns/inactive` |
| Filter rule | `active = 0` AND `archived_at IS NULL` |

## What the merchant can do here

- See every Inactive campaign in a sortable / filterable table — same table shape as Draft / Active.
- Flip the Status toggle back to Active → re-runs the activation pre-flight (see [[campaigns-draft-preflight-checks]]).
- Open the campaign in [[marketing-campaigns-edit|the editor]] — read-only unless the merchant first re-activates (or until the editor save flow takes over).
- View full historical Statistics ([[marketing-campaigns-statistics]]) and Logs ([[marketing-campaigns-statistics-log]]) — the hourly aggregation job keeps updating these.
- Click the **banned-reason badge** (if present) → opens [[marketing-campaigns-banned-info]] with the channel-suspension explanation.
- Copy a campaign → new Draft via [[marketing-campaigns-copy]].
- Archive → moves to [[marketing-campaigns-archive]] (Inactive rows are the natural archive target).
- Delete → soft-delete with cascade — see [[campaigns-draft-lifecycle-actions]].

## Settings & fields

### Columns rendered

Identical to the Draft tab plus the Status toggle:

| Column key | Label | Behaviour on Inactive tab |
|------------|-------|---------------------------|
| `title` | Campaign title | Click opens editor (read-only unless re-activated). |
| `created_at` | Date added | Creation date. |
| `goal` | Goal | Trigger condition / purpose. |
| `actions_count` | Steps | Number of action steps. |
| `reached` | Reached subscribers | Successfully-sent unique count from the campaign's run history. |
| `orders` | Orders | Historical attributed orders — continues to update hourly. |
| `turnover` | Turnover | Revenue from attributed orders — continues to update hourly. |
| `subscribers_count` | Subscribers | Count of enrolled subscribers (retained). |
| `statistics` | Logs | Link to per-action logs. |
| `status` | Status | **Inactive toggle** — flipping it triggers Inactive→Active pre-flight. |
| `actions` | Actions | Edit, Copy, Archive, Delete. |

### Banned-reason badge

If the campaign was auto-stopped by the channel-suspension cascade (spam / bounce / open / cc_denied — see [[marketing-channels]]), the row carries a banned-reason badge near the title. Clicking the badge opens [[marketing-campaigns-banned-info]] showing the suspension trigger and the channel involved.

The campaign is **not** auto-reactivated when the channel comes back; the merchant must manually flip the toggle (after also clearing the banned reason).

## Business rules

### Order-statistic query runs normally

Unlike the Draft tab, the Inactive tab does NOT short-circuit the order-statistic query — historical orders / turnover / reached counts are read from the same join, so the table reflects the full run history.

### Statistics keep updating after stop

The hourly campaign-statistics aggregation job continues to update `reached` / `orders` / `turnover` for Inactive campaigns as new attribution activity arrives. Example: a customer who received the campaign last week places an order today — the orders count on the Inactive row goes up. The tooltip *"The statistical information is updated every hour"* applies here too.

### Inactive→Active re-runs pre-flight checks

When the merchant flips the Status toggle back to Active, the same pre-flight gate fires as for any activation: channels configured + active + sufficient credits + not-draft. Failing the check keeps the campaign Inactive and surfaces the error. Full check matrix on [[campaigns-draft-preflight-checks]].

### Enrolled subscribers are retained — mid-funnel resume

The `subscriber_to_campaigns` pivot rows stay intact when a campaign flips Active→Inactive. Subscribers mid-funnel (e.g., on Day 2 of a Day-1/Day-3/Day-7 drip) keep their `progress` value. When the campaign is re-activated, **already-enrolled** subscribers do NOT auto-restart from step 1 — they pick up where they were, though timing may shift (the worker re-evaluates next-step delays from the resume moment). New subscribers entering the trigger segment after re-activation join the campaign at step 1 normally. See [[campaigns-draft-lifecycle-actions]] for the full subscriber-retention rules.

### Channel-suspension cascade — Inactive is the destination

When a channel auto-suspends or the merchant turns it off manually, every campaign referencing that channel with `active=1` flips to `active=0` and lands on this tab with a banned-reason badge. See [[campaigns-draft-preflight-checks]] for cascade scope.

### Toggle endpoint trust gap

The `campaigns.update_active` toggle does NOT re-validate that every action template still has a message body filled in — it trusts the existing data. The Vue UI prevents bypass by routing Draft activations through the editor's full save flow, but raw API calls bypass. See [[campaigns-draft-preflight-checks]] for the full toggle-bypass risk.

### Anti-spam policy gate

Required for every campaign endpoint — see [[marketing-campaigns-policy]].

## Related

- [[marketing-campaigns-draft]] — hub.
- [[marketing-campaigns]] — parent four-tab list.
- [[marketing-campaigns-edit]] — editor (read-only on Inactive unless re-activated).
- [[marketing-campaigns-banned-info]] — banned-reason explainer linked from the row badge.
- [[marketing-channels]] — channel setup; channel suspension drops campaigns onto this tab.
- [[marketing-campaigns-archive]] — Archived tab; Inactive rows are the typical archive source.
- [[marketing-campaigns-statistics]] — Statistics screen; continues to update for Inactive.
- [[marketing-campaigns-statistics-log]] — Logs screen.
- [[marketing-campaigns-copy]] — Copy row action (clones to new Draft).
- [[marketing-campaigns-policy]] — anti-spam policy required for every campaign endpoint.

## Open questions

No outstanding questions.
