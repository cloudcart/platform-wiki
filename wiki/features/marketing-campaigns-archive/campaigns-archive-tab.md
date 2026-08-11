---
type: feature
nav_path: "Marketing → Campaigns → Archived → The tab"
route_name: campaigns-archived
route_path: /admin/marketing-new/campaigns/archived
aliases: ["Archived tab", "Archived campaigns list", "Archived tab columns", "Status column hidden archived"]
tags: [marketing, campaigns, archive, archived, list]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-archive]]. See the hub for the other aspects (actions, triggers, unarchive/restore, delete cascade).

# Archived campaigns — the tab

## Purpose

This page documents the **Archived tab** as a list view: what it shows, which columns appear (and which is hidden), what happens when the merchant clicks a row, and the two systemic facts about archived campaigns that surprise merchants — their statistics still lag on the hourly statistics refresh, and they are invisible to both the trigger-enrolment pipeline and the marketing dashboard.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **Archived** tab.

The tab is the route `campaigns-archived` at `/admin/marketing-new/campaigns/archived`, rendering the shared campaigns list page. It pulls only campaigns that have an archive date set, each row showing title, dates, action counts, and reached / orders / turnover from the latest statistics aggregate.

## What the merchant can do here

- See **all archived campaigns** — both auto-archived (Regular campaigns that completed) and manually-archived ones. How a campaign lands here is on [[campaigns-archive-triggers]].
- **Click a row** to open the campaign in [[marketing-campaigns-edit|the editor]] in a read-only view (archived campaigns are inactive).
- Read each row's list columns (title, date, goal, step count, reached, orders, turnover, subscribers, logs, actions).
- **Filter, search, sort, paginate** the archived table just like the active list.
- Reach **Statistics** ([[marketing-campaigns-statistics]]) and **Logs** ([[marketing-campaigns-statistics-log]]) — preserved for archived campaigns and useful for end-of-quarter reporting.

The row-action icons (Unarchive / Delete / bulk-delete) are covered on [[campaigns-archive-actions]].

## Settings & fields

### Table columns (same as the rest of the list, minus Status)

| Column key | Label | Notes |
|------------|-------|-------|
| `title` | Campaign title | Locked + fixed first column; click to open the editor. |
| `created_at` | Date added | When the campaign was first created (NOT when archived). |
| `goal` | Goal | Trigger condition / purpose. |
| `actions_count` | Steps | Number of campaign actions. |
| `reached` | Reached subscribers | Successfully-sent unique subscribers. |
| `orders` | Orders | Orders attributed. |
| `turnover` | Turnover | Revenue from attributed orders. |
| `subscribers_count` | Subscribers | Count enrolled. |
| `statistics` | Logs | Link to per-action logs. |
| `actions` | Actions | Unarchive + Delete. |

### Status column hidden on Archived

The status column (the Active/Inactive switch or Draft badge) is explicitly omitted from the column array when the Archived tab is active. So the tab doesn't expose any inline way to flip a campaign back to active — the merchant must Unarchive first, then toggle (see [[campaigns-archive-unarchive-restore]]).

## Business rules

### Statistics lag still applies

The reached / orders / turnover / subscribers counts on archived rows are pulled from the same hourly-refreshed statistics aggregates as the rest of the campaigns list. The tooltip *"The statistical information is updated every hour"* applies here too — though archived campaigns are unlikely to see new activity, so their numbers are usually stable.

### Archived campaigns are invisible to the trigger pipeline AND the dashboard

The job that enrolls new subscribers into automated campaigns only considers campaigns that are active and not archived, so an archived campaign never re-enrolls a subscriber even if the segment rules match them again. Similarly, the [[marketing-dashboard]] Top / Recent campaign modules only consider active campaigns — archived campaigns never appear in dashboard cards or charts.

### Channel-suspension cascade does NOT touch archived campaigns

When a channel is auto-suspended (see [[marketing-channels]] business rules), only Active campaigns referencing the channel get auto-stopped — archived campaigns are not touched. They were already stopped.

### Anti-spam policy gate and permission

This tab, like all campaign endpoints, is behind the campaign anti-spam policy gate ([[marketing-campaigns-policy]]). Standard campaign permission applies.

## Related

- [[marketing-campaigns-archive]] — hub.
- [[marketing-campaigns]] — parent campaign list; the Archived tab is one of four status tabs.
- [[marketing-campaigns-edit]] — editor; opens read-only for archived rows.
- [[marketing-campaigns-statistics]] — statistics accessible from the Logs / Statistics column.
- [[marketing-campaigns-statistics-log]] — per-send logs, preserved.
- [[marketing-dashboard]] — Top / Recent modules; never shows archived campaigns.
- [[marketing-channels]] — channel-suspension cascade; skips archived campaigns.
- [[marketing-campaigns-policy]] — anti-spam policy gate.
- [[campaign]] — Campaign entity carrying the `archived_at` timestamp.

## Open questions

None.
