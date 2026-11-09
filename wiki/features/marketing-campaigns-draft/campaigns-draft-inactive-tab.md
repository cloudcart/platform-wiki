---
type: feature
nav_path: "Marketing → Campaigns → Draft → Inactive tab"
route_name: campaigns-inactive
route_path: /admin/marketing/campaigns/inactive
aliases: ["Inactive campaigns tab", "Stopped campaigns list", "Paused campaigns", "Спрени кампании", "Неактивни кампании"]
tags: [marketing, campaigns, inactive, list]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Draft tab, entry paths, unsaved-changes guard, pre-flight checks, lifecycle actions).

# Inactive campaigns — the Inactive tab

## Purpose

The **Inactive** tab lists every campaign that WAS started and has now been stopped — `active = 0` AND `archived_at IS NULL`. Inactive campaigns retain their full history: enrolled subscribers, message logs, statistics, mid-funnel `progress` values. The tab answers the merchant question *"what's paused that I should resume?"*

A campaign can land here three ways:

- The merchant switched an **Automated** campaign off with its Status switch (Regular campaigns have no switch).
- The merchant switched off a channel the campaign uses — every campaign with a step on that channel is set inactive, drafts included (see [[marketing-channels-cross-lifecycle]]). Reputation auto-suspension does **not** move campaigns here.
- A regular campaign was explicitly inactivated by an admin. (Completing its run does not: a completed Regular campaign keeps `active = 1` and is auto-archived.)

The Inactive tab is the sibling of [[campaigns-draft-tab|the Draft tab]] on the four-tab campaigns list ([[marketing-campaigns]]).

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click the **Inactive** tab.

| Setting | Value |
|---------|-------|
| Route name | `campaigns-inactive` |
| Route path | `/admin/marketing/campaigns/inactive` |
| Filter rule | `active = 0` AND `archived_at IS NULL` |

## What the merchant can do here

- See every Inactive campaign in a sortable / filterable table — same table shape as Draft / Active.
- Switch an **Automated** campaign back on with its Status switch → re-runs the activation pre-flight (see [[campaigns-draft-preflight-checks]]). A **Regular** campaign has no switch and cannot be re-activated from the UI.
- Open the campaign in [[marketing-campaigns-edit|the editor]] — read-only, as for any non-draft campaign.
- View full historical Statistics ([[marketing-campaigns-statistics]]) and Logs ([[marketing-campaigns-statistics-log]]) — the hourly aggregation job keeps updating these.
- Click the **banned-reason badge** (if present) → opens [[marketing-campaigns-banned-info]] with the channel-suspension explanation.
- Copy a campaign → new Draft via [[marketing-campaigns-copy]].
- Archive → moves to [[marketing-campaigns-archive]] (Inactive rows are the natural archive target).
- Delete is **not** offered here — delete works only on an archived campaign, so archive first (see [[campaigns-draft-lifecycle-actions]]).

## Settings & fields

### Columns rendered

Identical to the Draft tab plus the Status column:

| Column key | Label | Behaviour on Inactive tab |
|------------|-------|---------------------------|
| `title` | Campaign title | Click opens editor (read-only). |
| `created_at` | Date added | Creation date. |
| `goal` | Goal | Trigger condition / purpose. |
| `actions_count` | Steps | Number of action steps. |
| `reached` | Reached subscribers | Successfully-sent unique count from the campaign's run history. |
| `orders` | Orders | Historical attributed orders — continues to update hourly. |
| `turnover` | Turnover | Revenue from attributed orders — continues to update hourly. |
| `subscribers_count` | Subscribers | Count of enrolled subscribers (retained). |
| `statistics` | Logs | Link to per-action logs. |
| `status` | Status | **Automated**: off switch — switching it on runs the Inactive→Active pre-flight. **Regular**: read-only progress badge, no switch. |
| `actions` | Actions | Copy, Archive. |

### Banned-reason badge

If a channel the campaign uses is suspended (spam / bounce / open / cc_denied — see [[marketing-channels]]), the row carries a banned-reason badge near the title. Clicking the badge opens [[marketing-campaigns-banned-info]] showing the suspension trigger and the channel involved. A suspension does not itself change the campaign's status.

Switching a channel back on reactivates nothing: an Automated campaign can be switched on again one by one; a Regular one cannot.

## Business rules

### Order-statistic query runs normally

Unlike the Draft tab, the Inactive tab does NOT short-circuit the order-statistic query — historical orders / turnover / reached counts are read from the same join, so the table reflects the full run history.

### Statistics keep updating after stop

The hourly campaign-statistics aggregation job continues to update `reached` / `orders` / `turnover` for Inactive campaigns as new attribution activity arrives. Example: a customer who received the campaign last week places an order today — the orders count on the Inactive row goes up. The tooltip *"The statistical information is updated every hour"* applies here too.

### Inactive→Active re-runs pre-flight checks

When the merchant switches an Automated campaign back on, the same pre-flight gate fires as for any activation: channels configured + active + sufficient credits + not-draft. Failing the check keeps the campaign Inactive and surfaces the error. Full check matrix on [[campaigns-draft-preflight-checks]].

### Enrolled subscribers are retained — dropped steps are not resumed

The `subscriber_to_campaigns` pivot rows stay intact when a campaign flips Active→Inactive. But steps that came due while the campaign was stopped (or while its channel was off) were dropped and are **not** re-created, so after re-activation the campaign stays *"Executing"* without sending them. Subscribers who already completed a step are never re-sent it. New subscribers entering the trigger segment after re-activation join the campaign at step 1 normally. See [[campaigns-draft-lifecycle-actions]].

### Channel switch-off — Inactive is the destination

When the merchant switches a channel off manually, every campaign with a step on that channel is set `active=0` — drafts (which become inactive and read-only) and archived ones included (archived ones stay on the Archived tab). Reputation auto-suspension, a rejected Email key, or reaching the plan cap change no campaign's state. See [[marketing-channels-cross-lifecycle]].

### Toggle endpoint trust gap

The `campaigns.update_active` toggle does NOT re-validate that every action template still has a message body filled in — it trusts the existing data. The Vue UI prevents bypass by routing Draft activations through the editor's full save flow, but raw API calls bypass. See [[campaigns-draft-preflight-checks]] for the full toggle-bypass risk.

### Anti-spam policy gate

Required for every campaign endpoint — see [[marketing-campaigns-policy]].

## Related

- [[marketing-campaigns-draft]] — hub.
- [[marketing-campaigns]] — parent four-tab list.
- [[marketing-campaigns-edit]] — editor (read-only for any non-draft campaign).
- [[marketing-campaigns-banned-info]] — banned-reason explainer linked from the row badge.
- [[marketing-channels]] — channel setup; a manual channel switch-off drops campaigns onto this tab.
- [[marketing-campaigns-archive]] — Archived tab; Inactive rows are the typical archive source.
- [[marketing-campaigns-statistics]] — Statistics screen; continues to update for Inactive.
- [[marketing-campaigns-statistics-log]] — Logs screen.
- [[marketing-campaigns-copy]] — Copy row action (clones to new Draft).
- [[marketing-campaigns-policy]] — anti-spam policy required for every campaign endpoint.

## Open questions

No outstanding questions.
