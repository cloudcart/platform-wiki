---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Logs modal"
route_name: campaigns-statistics
route_path: /admin/marketing-new/campaigns/statistics/:id
aliases: ["Statistics Logs Modal", "Per-step logs modal", "Campaign log modal", "Preview message modal", "Subscriber details modal (campaign log)"]
tags: [marketing, campaigns, statistics, logs, modal]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics]]. See the hub for the other aspects (KPI cards, channel breakdown, step table, attribution, aggregation).

# Campaign statistics — Statistics Logs Modal

## Purpose

When the merchant clicks a step row in the per-step table, the **Statistics Logs Modal** opens — the per-recipient delivery log for that single step, layered on top of the statistics page rather than navigating away. This page documents the modal opened from the statistics page and its two nested sub-modals (view the rendered message, and view the subscriber's profile). It is the bridge from the aggregate per-step row down to the individual recipient records.

## Where to find it

From the Campaign statistics page, click a step row in the per-step table ([[campaigns-stats-step-table]]) — the **Step** column is a clickable link. This opens the Statistics Logs Modal scoped to that step.

(The same per-send log is also reachable as a standalone surface — the broader log feature, its statuses, filters, and storage are documented on the [[marketing-campaigns-statistics-log]] hub. This page covers only the modal as it appears from the statistics page.)

## What the merchant can do here

- **Browse the per-recipient log** for the step — a paginated, filterable table of one row per (recipient, send attempt).
- **Filter** the rows — the filter bar is enabled (status / date / search).
- **View the rendered message** a recipient actually received — click the channel icon (first column) of any row.
- **Open the subscriber's profile** — click the Subscriber column (only when the subscriber is active).
- **Close** the modal — the footer has only a Close button (no save action).

## Settings & fields

**Modal layout:**

- **Title** — `{campaign title} - Logs - Step {N}` (1-based step number).
- **Size** — `xll` (extra-extra-large); switches to full-screen (`size="100"`) when a sub-subscriber modal opens on top.
- **Body** — a table of per-recipient log rows (paginated, filterable). Columns: Channel, Subscriber, Messages, Destination, Segment, Campaign, Status, Type, Date.
- **Filters bar** — enabled (filter by status / date / search).
- **Footer** — Close button only.

**The two nested sub-modals:**

| Sub-modal | Trigger | Purpose |
|---|---|---|
| **Preview-message modal** (`MarketingChannelsLogsPreviewMessageModal`) | Click the channel icon (first column) of any log row | View the rendered message body the recipient actually received — Email HTML, SMS text, Viber body + image, Web Push title + body + image. |
| **Subscriber-details modal** (`MarketingChannelsLogsSubscriberDetailsModal`) | Click the Subscriber column (only if the subscriber is active — `row.subscriber_active && row.subscriber_id`) | Open the subscriber's full detail card inline — channels, RFM, statistics, segments (same component as the subscribers-list detail modal in [[marketing-subscribers]]). |

## Business rules

- **The Subscriber link is conditional.** The Subscriber column is only clickable when the subscriber is active and has an id (`row.subscriber_active && row.subscriber_id`). For inactive / anonymised subscribers, the name renders as plain text.
- **The parent modal shrinks to fit when the subscriber sub-modal opens.** When the subscriber-details sub-modal opens on top, the parent Logs modal resizes to full-screen (`size === '100'`), giving the merchant a layered view of the per-recipient log + the per-subscriber profile simultaneously.
- **The log is read-only.** Rows are immutable delivery records; the modal has no save action, only Close. The full status vocabulary and the storage model are on the [[marketing-campaigns-statistics-log]] hub.
- **Loaded on demand.** The log data is fetched only when the modal opens (the `statisticsLogs` query), not pre-loaded with the rest of the statistics page — see the hub's How-it-works.

## How it works

The modal is populated by the `statisticsLogs` JSON-API query, fetched on-demand when the merchant opens it for a step — paginated and filterable, scoped to the campaign + the specific campaign action (step). Each row is mapped through a per-row formatter (channel icon, subscriber link, status pill, destination, segment, date). Clicking the channel icon opens the preview-message sub-modal (the rendered body lives in a separate document, loaded lazily); clicking an active subscriber opens the subscriber-details sub-modal and resizes the parent to full-screen. The underlying log records, their status values, filter semantics, and storage are all documented on the [[marketing-campaigns-statistics-log]] hub.

## Related

- [[marketing-campaigns-statistics]] — hub.
- [[campaigns-stats-step-table]] — the per-step table whose Step link opens this modal.
- [[marketing-campaigns-statistics-log]] — the full per-send log hub (statuses, filters, storage, surfaces).
- [[marketing-subscribers]] — the subscriber detail card shown by the subscriber sub-modal.
- [[marketing-channels]] — channel-level logs sharing the same data + status vocabulary.

## Open questions

No outstanding questions.
