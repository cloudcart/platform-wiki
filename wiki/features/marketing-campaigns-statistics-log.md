---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["Campaign log", "Per-send log", "Delivery log (campaign)", "Recipient status log", "View sent message", "Лог на изпратени съобщения", "Лог на доставка"]
tags: [marketing, campaigns, statistics, logs, delivery]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

# Per-send delivery log

## Purpose

The **Per-send delivery log** is the merchant's per-recipient ground truth for any campaign step — one row per (recipient, send attempt) showing what was sent, who it went to, when, through which channel, what status (DELIVERED / SEEN / CLICKED / UNDELIVERED / BOUNCED / etc.), and — critically — a button to view the exact raw message body the recipient received. This is the merchant's debugger when a customer says *"I didn't get your email"* or when stats look weird (*"why is my bounce rate 30%?"*) — the merchant opens this log, filters by status BOUNCED, and inspects individual recipient records to find the pattern.

Unlike [[marketing-campaigns-subscribers]] (which shows enrolment state per subscriber) and [[marketing-campaigns-statistics-full]] (which shows attributed orders), this page is the **delivery transaction record** — one entry per individual send attempt with full status history.

## Where to find it

There are two entry points:

1. From [[marketing-campaigns-statistics]] (per-campaign stats page) — click on a step row in the per-step table.
2. From the campaigns list (each row has a Logs / chart icon in its statistics column).

The log is exposed in two surfaces depending on which version of the UI the merchant lands on: a modern Vue modal layered on the parent page, or a legacy side-panel deep-linkable at `/admin/campaigns/statistics/{id}/{action_id}`. See [[campaigns-statistics-log-surfaces]] for the full surface comparison and route list.

## What the merchant can do here

- **Filter** the log by status (multi-select), date range (`updated_at`), and free-text search across subscriber + destination — see [[campaigns-statistics-log-filters-table]].
- **Inspect a row's status timeline** — hover the status pill to see the full SENT → DELIVERED → SEEN → CLICKED history with timestamps, see [[campaigns-statistics-log-status-archive]].
- **View the rendered message body** — click the channel icon to open the exact HTML / text / push-tile the recipient received, see [[campaigns-statistics-log-view-message]].
- **Drill into the subscriber profile** — click the subscriber-column link to open the per-subscriber details modal (modern Vue only) — see [[campaigns-statistics-log-surfaces]].
- **Investigate bounce / error reasons** — filter by BOUNCED to surface every failed delivery (auto-includes HARD_BOUNCED — see [[campaigns-statistics-log-email-mapping]]).

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[campaigns-statistics-log-surfaces]] — the two surfaces (modern Vue modal vs legacy side-panel), entry points from the Campaigns list and per-step table, and the four routes that back them.
- [[campaigns-statistics-log-status-values]] — the 20 status values (SENT / DELIVERED / SEEN / CLICKED / BOUNCED / HARD_BOUNCED / etc.), per-channel coverage, colour coding, and the synthetic PURCHASE status.
- [[campaigns-statistics-log-status-archive]] — the `status_archive` timeline (every transition with `original` + `date`), the hover-tooltip surface, and the idempotency rule that protects against stale Sent webhooks.
- [[campaigns-statistics-log-filters-table]] — the filter bar (status / date / search), the table columns, drill-downs (channel icon → view message; subscriber link → details modal), and search-field semantics.
- [[campaigns-statistics-log-view-message]] — the View-message endpoint, the rendered-body store (separate `content` document), and the channel-specific render paths (Email HTML, SMS text, Viber image, Web Push title+body).
- [[campaigns-statistics-log-side-effects]] — what happens to the subscriber when a log row transitions to ERROR / HARD_BOUNCED / ABUSE_REPORT (auto-bounce + auto-remove + auto-unsubscribe) and to SEEN / CLICKED (auto-verify), plus click-through tracking.
- [[campaigns-statistics-log-email-mapping]] — Email-channel-specific behaviour: how Elastic Email's provider statuses map to the platform's canonical statuses, and the "Bounced auto-includes Hard Bounced" filter expansion.
- [[campaigns-statistics-log-storage]] — the slim ~30-field list view, the lazy rendered-body join, the `log_group='campaigns'` global scope, owner / site-scoping, and the absence of automated retention.

## Settings & fields

The log itself has no merchant-editable settings — log rows are immutable audit records. The merchant interacts via the filter bar (Status / Date range / Search) and the drill-down actions on each row. See [[campaigns-statistics-log-filters-table]] for the filter inputs and column list. The status values that appear are documented in [[campaigns-statistics-log-status-values]].

## Business rules

The high-level rules — detailed in the sub-pages:

- **Log entries are immutable.** Each row is created at send time; only the `status` field is updated as provider webhooks arrive. The merchant cannot delete log rows from the UI. The full transition history is preserved in `status_archive` — see [[campaigns-statistics-log-status-archive]].
- **Site-scoped via a global filter.** Every query is limited to the current site by an owner filter, and additionally to `log_group='campaigns'` — see [[campaigns-statistics-log-storage]] for the multi-tenant isolation details.
- **Multiple-campaign log dedup.** A subscriber enrolled in multiple campaigns gets one log row PER (campaign, step, send). The per-step filter ensures the merchant only sees rows for the step they opened — see [[campaigns-statistics-log-filters-table]].
- **Bounce / abuse propagation.** When a row becomes HARD_BOUNCED or ABUSE_REPORT, the subscriber's channel record is updated (bounced / unsubscribed flags), AND the subscriber is auto-removed from the active campaign — see [[campaigns-statistics-log-side-effects]] for the full removal flow.
- **Status update lag.** Provider webhooks arrive asynchronously — DELIVERED in seconds, SEEN / CLICKED potentially hours or days later. The `updated_at` column reflects the most recent status change, not the original send time — see [[campaigns-statistics-log-status-archive]].
- **Permission + anti-spam gate.** Standard campaign permission applies, and the route is behind the campaign anti-spam policy gate (the same gate that protects every campaigns endpoint).
- **No bulk export.** There's no built-in CSV export from this page. For analytics-grade analysis, use [[marketing-channels|channel logs]] (cross-campaign view of the same delivery log) or request an API extract.

## How it works

When the merchant opens the log (either from the per-step table in [[marketing-campaigns-statistics]] or from the chip in the campaigns list), the surface resolves the campaign + the campaign action, builds the filter object from the request, and renders a paginated grid of channel-log rows scoped to `campaign_id` AND `campaign_action_id`. Each row is mapped through a per-row formatter (channel icon, subscriber link, status pill, destination identifier, segment, date) for display.

The grid fetches only the ~30 fields needed for the list view — the rendered message body lives in a separate record and is loaded lazily on demand by the View-message action. See [[campaigns-statistics-log-storage]] for the storage split and field details.

Provider webhooks (Elastic Email's SMTP feedback, MsgHub's DLRs, Viber's read receipts, Web Push acks) update the `status` field on existing log rows. Every status change appends to `status_archive` and may trigger side-effects on the subscriber — see [[campaigns-statistics-log-side-effects]].

## Related

- [[marketing-campaigns]] — parent hub; the Logs chip on each campaign row.
- [[marketing-campaigns-statistics]] — per-campaign stats; the per-step row in the table links here.
- [[marketing-campaigns-statistics-full]] — per-order revenue list; complementary view.
- [[marketing-campaigns-subscribers]] — per-subscriber funnel state.
- [[marketing-subscribers]] — full subscriber profile; subscriber name links here.
- [[marketing-channels]] — channel-level logs (cross-campaign view of the same data).
- [[marketing-channels-email]] — Email log details.
- [[marketing-channels-sms-msghub]] — MsgHub SMS log.
- [[marketing-channels-sms-nth]] — NTH SMS log.
- [[marketing-channels-viber]] — Viber log.
- [[marketing-channels-webpush]] — Web Push log.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
