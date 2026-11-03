---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → Surfaces & routes"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["Campaign log modal", "Campaign log side-panel", "Per-send log entry points", "Logs modal route"]
tags: [marketing, campaigns, statistics, logs, routes]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (status values, status archive, filters & table, view-message, side-effects, Email mapping, storage).

# Per-send log — surfaces and routes

## Purpose

The per-send delivery log is exposed in **two surfaces** depending on which version of the Campaigns UI the merchant lands on — a modern Vue modal and a legacy side-panel. Both display the same underlying data (one row per recipient × send attempt, with full status history) but differ in how they're opened, what URL surfaces, and how the View-message and Subscriber-details drill-downs are rendered. This page documents the entry points, the four routes, and the chrome behaviour that differs between the two surfaces.

## Where to find it

There are two entry points from the merchant's perspective:

1. From [[marketing-campaigns-statistics]] (per-campaign stats page) — click on a step row in the per-step table.
2. From the campaigns list (each row has a Logs / chart icon in its statistics column).

The behaviour after the click depends on which surface is active:

| Surface | Trigger | Behaviour |
|---------|---------|-----------|
| **Modern Vue modal** (`MarketingCampaignStatisticsLogsModal`) | Click any step-row in the modern Vue Campaign-Statistics page's per-step table | Opens as a modal (`size="xll"`) on top of the statistics page. Modal title: `{campaign title} - Logs - Step {N}`. The modal shrinks automatically (`size="100"` / full-screen) when the user drills into a nested per-subscriber detail modal. |
| **Legacy side-panel** (Smarty route) | Used by the legacy Smarty campaign list + legacy stats page | Opens as a wide side-panel at `/admin/campaigns/statistics/{id}/{action_id}`. Header: `{campaign title} Logs - Step {N}`. |

## What the merchant can do here

This surface is output-only — there are no actions specific to "the chrome" beyond opening the log and drilling into rows. The actual interactions (filtering, sorting, viewing messages, opening subscriber details) are documented on the inner-content aspect pages:

- See [[campaigns-statistics-log-filters-table]] for filter inputs and per-row drill-downs.
- See [[campaigns-statistics-log-view-message]] for the channel-icon → rendered-body drill-down.
- See [[campaigns-statistics-log-status-archive]] for the status-pill hover-tooltip timeline.

## Settings & fields

There are no merchant-editable settings on the surface itself — both modal and side-panel are output-only. The four routes that back them:

| Route name | Method | Route path | Purpose |
|------------|--------|------------|---------|
| `admin.api.campaigns.statistics.logs` (modern) | GET | `/admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs` | Paginated per-recipient log data for the modern Vue modal. The Vue component uses `apiMarketingCampaigns.statisticsLogs.useQuery({campaign, action, query})` to fetch. |
| `campaigns.statistics.log` (legacy) | GET | `/admin/campaigns/statistics/{id}/{action_id}` | Open the log panel for a campaign step (legacy Smarty). |
| `campaigns.statistics.log.get` (legacy) | POST | `/admin/campaigns/statistics/{id}/{action_id}/list` | Paginated AJAX data fetch (legacy). |
| `campaigns.statistics.log.view-message` (legacy) | GET | `/admin/campaigns/statistics/view-message/{log_id}` | View the raw rendered message for one log entry (legacy). |

In the modern Vue modal the data is fetched directly via the `statisticsLogs` API query — no separate panel-chrome / AJAX-body round-trip. The View-message and Subscriber-details panels are also modals nested inside the parent modal (not separate URLs). In the legacy side-panel each is a separate URL.

## Business rules

- **Modal-shrink on nested drill-down.** When the merchant opens a nested per-subscriber-details modal from inside the modern Vue logs modal, the **parent** logs-modal shrinks to `size="100"` (full-screen) to make room for the child. When the child closes, the parent restores to its default `size="xll"`. This is a UI affordance unique to the modern surface.
- **Both surfaces require the campaign-permission gate.** Standard campaign permission applies, and both routes are behind the campaign anti-spam policy gate (the same gate that protects every campaigns endpoint).
- **The modal title and side-panel header use slightly different formats.** Modal: `{campaign title} - Logs - Step {N}`. Side-panel: `{campaign title} Logs - Step {N}` (no surrounding hyphens around "Logs"). (verify) This is a cosmetic difference between the two surfaces.
- **No deep-linkable URL on the modern modal.** The modern Vue modal is stacked on top of the parent stats page — there's no URL that opens directly to the log modal. The legacy side-panel route IS deep-linkable.

## How it works

Modern Vue path: the parent stats page contains a `MarketingCampaignStatisticsLogsModal` component instance. When the merchant clicks a step row, the parent calls `.show(campaign, action)` on the modal ref, which dispatches the `apiMarketingCampaigns.statisticsLogs.useQuery` query against the modern API route and renders the resulting page of rows in a grid. The query re-runs when the merchant changes filters or pagination.

Legacy Smarty path: the merchant's click sends them to the GET log route, which loads the campaign and the campaign action, sets up the filter object, and renders the panel template with the campaign + action + filters context. The Smarty template renders the panel chrome (header + filter bar + grid table thead) and the grid body loads via the POST listing endpoint as a second request. The View-message link is its own route.

Both back-ends ultimately read from the same delivery log — see [[campaigns-statistics-log-storage]] for the slim field set and scoping that's applied to both.

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[marketing-campaigns]] — parent campaigns feature.
- [[marketing-campaigns-statistics]] — per-campaign stats page; the primary entry point.
- [[campaigns-statistics-log-filters-table]] — the filter bar and table columns shown in both surfaces.
- [[campaigns-statistics-log-view-message]] — the drill-down to view the rendered message body.

## Open questions

None.
