---
type: feature
nav_path: "Marketing → Campaigns → Archived"
route_name: campaigns-archived
route_path: /admin/marketing-new/campaigns/archived
aliases: ["Archived campaigns", "Old campaigns", "Campaign archive", "Archive campaign", "Unarchive campaign", "Архивирани кампании", "Архив на кампании"]
tags: [marketing, campaigns, archive, archived]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

# Archived campaigns

## Purpose

The **Archived** tab is where the merchant goes to see campaigns they've put away — campaigns that ran their course, ones they deliberately retired, or ones that auto-archived themselves on completion. Archived campaigns aren't deleted (they keep their full history, statistics, message templates, and subscriber records intact) — they just live outside the active rotation. From here the merchant can resurrect a campaign (unarchive), permanently delete it, or just look at its statistics and logs for record-keeping.

This tab + the `archive` / `unarchive` actions are what give the campaign list its lifecycle hygiene: instead of accumulating dozens of inactive campaigns in the Inactive tab forever, the merchant can park them out of the way once they're done with them. Distinct from the Draft / Inactive states — see [[marketing-campaigns-draft|Draft and Inactive campaigns]].

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **Archived** tab.

The page is a separate tab on the campaigns list (route `campaigns-archived`, path `/admin/marketing-new/campaigns/archived`, rendering `MarketingCampaignsListPage`). Selecting it shows only campaigns whose `archived_at` is non-null. All four list tabs (Active / Inactive / Archived / Draft) render the same list component; clicking a tab swaps the URL and re-queries.

## What the merchant can do here

- See the list of **all archived campaigns** — both auto-archived (Regular campaigns that completed) and manually-archived ones. See [[campaigns-archive-tab]].
- **Unarchive** a campaign to move it back to the rotation. It returns as Inactive — the merchant must manually re-Activate it. See [[campaigns-archive-unarchive-restore]].
- **Delete** a campaign permanently — only available on this tab. See [[campaigns-archive-delete-cascade]].
- **Bulk-delete** multiple archived campaigns at once. See [[campaigns-archive-delete-cascade]].
- **Drill into Statistics** ([[marketing-campaigns-statistics]]) and **Logs** ([[marketing-campaigns-statistics-log]]) — both preserved for archived campaigns.
- **Filter, search, sort, paginate** the archived table just like the active list.

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[campaigns-archive-tab]] — the Archived tab itself: route, table columns (Status toggle hidden), read-only editor on row click, statistics-lag tooltip, invisibility to the trigger pipeline and the dashboard.
- [[campaigns-archive-actions]] — the actions-column affordances: Archive / Unarchive icons (no confirm), the single `archive/{id}/{action}` endpoint with action code 1/0, the inline delete-confirm prompt, and the Archived-tab-only bulk-delete bar.
- [[campaigns-archive-triggers]] — how a campaign lands on this tab: manual archive (no status check; the dead legacy "stop first" error string), auto-archive on Regular-campaign completion (silent, atomic), and why Automated campaigns never auto-archive.
- [[campaigns-archive-unarchive-restore]] — why unarchive resurrects to **Inactive**, not Active; `progress` and statistics left untouched; the completed-Regular-campaign "clone to restart" caveat.
- [[campaigns-archive-delete-cascade]] — the soft-delete → permanent-delete two-phase pattern, the related-data cleanup (actions / templates / logs / subscriber enrolment), why the campaign delivery + statistics logs survive, and why only permanent delete frees a plan-tier campaign slot.

## Settings & fields

Archived rows show the standard list columns (title, date, goal, step count, reached subscribers, orders, turnover, subscribers, logs, actions). The **Status toggle column is hidden** on this tab — archived campaigns are not toggle-able active/inactive (they must be unarchived first). Full column table on [[campaigns-archive-tab]].

The Actions column shows three icons on this tab (Unarchive, Delete, and a Copy that is generally hidden for archived rows) instead of the Active tab's two — see [[campaigns-archive-actions]].

## Business rules

- **Archive is available on every non-archived tab** — there is no status check preventing an Active campaign from being archived directly. The legacy *"You must stop the campaign before you can archive it"* string is dead text. See [[campaigns-archive-triggers]].
- **Regular campaigns auto-archive on completion** — silently, in the same step that sets `progress = completed`. Automated campaigns never auto-archive. See [[campaigns-archive-triggers]].
- **Unarchive resurrects to Inactive, not Active** — intentional, to force a deliberate restart. See [[campaigns-archive-unarchive-restore]].
- **Delete is only callable on archived campaigns** — the path is Stop → Archive → Delete. See [[campaigns-archive-delete-cascade]].
- **Archive does NOT free a plan-tier campaign slot; permanent delete does** — see [[campaigns-archive-delete-cascade]].
- **The campaign delivery + statistics logs are NOT auto-cleaned on delete** — retained for forensic / audit purposes. See [[campaigns-archive-delete-cascade]].
- **Anti-spam policy gate** — this tab, like every campaign endpoint, requires [[marketing-campaigns-policy|anti-spam policy]] acceptance. Standard campaign permission applies.
- **Archived campaigns are invisible to the trigger pipeline and the dashboard** — see [[campaigns-archive-tab]].

## Related

- [[marketing-campaigns]] — parent hub; the Archived tab is one of four status tabs.
- [[marketing-campaigns-draft]] — sibling Draft / Inactive tabs; Inactive campaigns can move here.
- [[marketing-campaigns-edit]] — editor opens for archived campaigns in read-only mode.
- [[marketing-campaigns-statistics]] — archived campaign statistics still accessible from the Logs / Statistics column.
- [[marketing-campaigns-statistics-log]] — per-send logs, preserved for archived campaigns.
- [[marketing-campaigns-subscribers]] — per-subscriber funnel state, preserved for archived campaigns.
- [[marketing-campaigns-policy]] — anti-spam policy required for every campaign endpoint.
- [[marketing-channels]] — channel-suspension cascade; does not touch archived campaigns.
- [[marketing-dashboard]] — Top / Recent modules; archived campaigns never appear.
- [[campaign]] — Campaign entity carrying the `archived_at` and `deleted_at` timestamps.

## Open questions

(All previously listed questions have been resolved — see the aspect pages.)
