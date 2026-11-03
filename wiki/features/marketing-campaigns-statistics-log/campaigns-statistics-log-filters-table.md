---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → Filters & table"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["Campaign log filter bar", "Per-send log columns", "Status filter multi-select", "Log search box", "Date range filter (logs)", "Channel icon drill-down"]
tags: [marketing, campaigns, statistics, logs, ui]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (surfaces, status values, status archive, view-message, side-effects, Email mapping, storage).

# Per-send log — filters, table, and drill-downs

## Purpose

The log UI's job is to let the merchant narrow ~hundreds-of-thousands of rows down to the handful they actually need to inspect (the bounced ones, the unopened ones, the specific customer asking for support). This page documents the filter bar (Status / Date / Search), the table columns the merchant sees, the per-row drill-downs (channel icon → view message; subscriber link → details), and the exact semantics of each filter input — including the gotchas (the date filter compares `updated_at` not `sent_at`; the Search box ANDs words across 5 fields).

## Where to find it

Inside the [[marketing-campaigns-statistics-log|per-send delivery log]] — the filter bar sits at the top of the modal / side-panel and the table fills the body. See [[campaigns-statistics-log-surfaces]] for the modal vs side-panel chrome that wraps this view.

## What the merchant can do here

- **Filter** the log by status (multi-select), date range (`updated_at`), or text search across subscriber + destination.
- **Sort** by `updated_at` (default desc) to find the most-recently-changed rows.
- **Drill down per row** — click the channel icon to view the rendered message body, click the subscriber link to open per-subscriber details, hover the status pill to see the transition timeline.
- **Read at-a-glance** — colour-coded status pill, SMS chunk count, destination identifier, segment, and campaign name on every row.

## Settings & fields

### Top of the panel

- **Title** with campaign name + step number.
- **Filter bar** — allows filtering log entries by status, channel, and date / text search.
- **Close** button (X) to dismiss.

### Filter inputs

| Filter | Type | Notes |
|--------|------|-------|
| **Status** | multi-select | All channel statuses: SENT / DELIVERED / SEEN / CLICKED / UNDELIVERED / BOUNCED / HARD_BOUNCED / UNSUBSCRIBED / ABUSE_REPORT / EXPIRED / ERROR / NOT_SENT / REJECTED / UNDELIVERABLE / ACCEPTED / COMPLETED / PENDING. See [[campaigns-statistics-log-status-values]] for full catalogue. |
| **Date range** | date + operator | `updated_at` between two dates. Operators: `exactly` (=), `before` (<), `after` (>). |
| **Search** | text | Substring match across subscriber email / phone / name / destination identifier. |

### Table columns

| Column key | Label | What it shows |
|------------|-------|---------------|
| `channel` | Channel | Icon + name of the channel that sent this log row (Email, SMS, Viber, Web Push). Clickable — opens view-message. |
| `subscriber` | Subscriber | Link to the recipient's subscriber profile + name. |
| `messages_send` | Messages | For SMS, the number of SMS chunks (`data.smsCount`). Defaults to 1 for non-SMS. |
| `channel_identifier` | Destination | The actual destination (email address, phone number, web-push endpoint hash) — what the message was sent TO. |
| `segment_name` | Segment | The segment that enrolled this subscriber. |
| `campaign_name` | Campaign | The campaign name (helpful when multiple campaigns share an action ID context). |
| `status` | Status | Colour-coded status pill. Hover shows the status-archive timeline. |
| `type` | Type | Message type (campaign vs system; here always "campaign"). |
| `updated_at` | Date | When the log was last updated (each status change updates this column). |

### Drill-downs

- Click the **channel icon** (first column) → opens the view-message panel showing the rendered message body. See [[campaigns-statistics-log-view-message]] for the channel-specific render paths.
- Click the **Subscriber** column (modern Vue only — gated on `subscriber_active && subscriber_id`) → opens the per-subscriber detail modal nested inside the parent. When it opens, the parent logs-modal shrinks to make room — see [[campaigns-statistics-log-surfaces]].
- Click the **status** pill → status-archive tooltip with the timeline (SENT at T1 → DELIVERED at T2 → SEEN at T3 → CLICKED at T4). See [[campaigns-statistics-log-status-archive]].
- Click **View message** (legacy side-panel only — per row) → opens the legacy view-message route in its own side-panel.

### Empty state

If there are zero log entries for this step (e.g., the campaign just launched and no sends have happened yet), the empty state shows the standard *"No records yet (Logs)"* illustration.

## Business rules

- **Filtering by "Bounced" auto-includes Hard Bounced.** Selecting `BOUNCED` expands the query to `WHERE status IN ('BOUNCED', 'HARD_BOUNCED')` — soft AND hard bounces returned together. There's no separate "Hard Bounced" filter option. See [[campaigns-statistics-log-email-mapping]] for the category mapping.
- **Search spans 5 fields with substring matching.** Runs against `campaign_name`, `segment_name`, `channel_identifier`, `subscriber_first_name`, `subscriber_last_name`. The merchant can search by partial email ("@gmail" finds all Gmail recipients), partial phone, partial name. Multi-word searches AND-combine: each word must match at least one field.
- **Date filter compares against `updated_at`, not `sent_at`.** "Logs from yesterday" returns rows whose LAST status update was yesterday — regardless of when originally sent. By design — the merchant typically wants recently-changed deliveries.
- **Date operator semantics.** `exactly` = start-of-day to end-of-day UTC. `before` = earlier than start-of-day (exclusive). `after` = later than end-of-day (exclusive).
- **Default sort: `updated_at` desc.** Most-recently-updated rows surface at the top — useful when investigating a current incident.
- **Multiple-campaign log dedup.** A subscriber enrolled in multiple campaigns gets one log row PER (campaign, step, send). The per-step filter (`campaign_action_id = X`) ensures only rows for the specific step are shown.
- **No bulk export.** No built-in CSV export. For analytics-grade extracts the merchant uses [[marketing-channels|channel logs]] (cross-campaign view) or an API extract.
- **View-message icon is the channel icon, not a separate column.** Clicking the channel icon opens the side-panel / nested modal. If the row's `execute_message` flag is true (the message hit an exception), the icon is tinted red.

## How it works

The grid query is paginated (typical 25 rows / page). The filter object is built from the request and applied before the slim list view is read (see [[campaigns-statistics-log-storage]] for the field set). The Status filter passes through an expansion step (BOUNCED → BOUNCED + HARD_BOUNCED) before being added to the `WHERE`.

The Search filter splits input on whitespace; each word becomes an AND-clause that OR-matches across the 5 fields. (verify "AND across words" vs "OR across words" against the latest implementation.) Each row is then mapped through the per-row formatter (channel icon, subscriber link, destination identifier, segment name, colour-coded status pill with the archive timeline as tooltip data, formatted `updated_at`). The `messages_send` cell defaults to 1 for non-SMS rows; for SMS it reads `data.smsCount`.

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[campaigns-statistics-log-status-values]] — the values the Status filter exposes.
- [[campaigns-statistics-log-status-archive]] — the hover-tooltip timeline data.
- [[campaigns-statistics-log-view-message]] — the channel-icon drill-down target.
- [[campaigns-statistics-log-email-mapping]] — why BOUNCED includes HARD_BOUNCED.
- [[campaigns-statistics-log-surfaces]] — the modal vs side-panel chrome that wraps this table.
- [[marketing-subscribers]] — the target of the Subscriber-column link.

## Open questions

- Verify the multi-word search semantics — AND across words OR across words within a row?
