---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → Storage model"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["log_group campaigns scope", "owner site_id scope", "content document split", "No log retention", "Log store bloat"]
tags: [marketing, campaigns, statistics, logs, storage]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (surfaces, status values, status archive, filters & table, view-message, side-effects, Email mapping).

# Per-send log — storage model and scopes

## Purpose

Behind the log UI sits a delivery-log store that can grow to millions of rows over the life of an active store. The platform applies several efficiency and isolation techniques: a fixed set of slim fields that keeps the list-query payload small, a separate content record that holds the heavy rendered body (lazy-loaded only on View Message), a global filter that limits the view to the campaigns-only log group, and an owner / site scope that enforces multi-tenant isolation. There's also a deliberate non-decision: no automated retention. This page documents these mechanics — relevant when investigating list-query performance, multi-tenant isolation, or long-running-store log bloat.

## Where to find it

The storage layer is internal — the merchant doesn't navigate to it. Its **effects** show up indirectly:

- The View-message panel is the one place where the lazy content-document join becomes visible to the merchant — see [[campaigns-statistics-log-view-message]].
- The cross-campaign view at [[marketing-channels]] reads the same delivery log without the per-campaign filter — that surface is the most useful for the merchant when investigating "every send I've ever made on this channel".

## What the merchant can do here

There are no merchant actions specific to storage. Practical merchant context:

- **No bulk export** from the log UI — for analytics-grade extracts, use the channel-level log surface or request an API extract.
- **No log retention** — logs accumulate indefinitely, so the merchant can always look up a delivery from years ago.
- **Multi-tenant isolation is automatic** — even if multiple sites share the underlying log store, each admin only sees their own site's logs.

## Settings & fields

There are no merchant-editable settings for storage — everything described here is platform-internal mechanics. The relevant data:

- **Delivery log store** — one shared store holds rows for every campaign, every channel, every site. Each row carries `_id`, `log_group`, `status`, `status_archive`, `message_id`, `campaign_id`, `subscriber_id`, `channel`, `channel_identifier`, `subject`, `from`, `data`, `sandbox`, `updated_at`, `site_id`, and ~20 other fields.
- **Rendered-body store** — a separate store holds the rendered message body keyed by the log row's `_id`, exposed on the log row as its `content`.
- **Slim list view** — the list query reads ~30 fixed fields (the metadata needed for the grid), explicitly excluding heavyweight fields.

## Business rules

### The slim list view limits the fields fetched

The grid reads a fixed set of ~30 fields: `_id`, `log_group`, `status`, `status_archive`, `message_id`, `campaign_id`, `subscriber_id`, `channel`, `channel_identifier`, `subject`, `from`, `data`, `sandbox`, `updated_at`, etc. Larger fields like the rendered HTML body are NOT in that set — they're fetched lazily only on the View Message action. See [[campaigns-statistics-log-view-message]].

The slim list keeps the list-query payload tractable even for busy campaigns — a page of 25 rows fetches ~25 small records instead of 25 records each containing a 100kB rendered HTML body.

### Per-recipient body stored in a separate record

The rendered message body lives in a related record keyed by the log row's ID, exposed as the row's `content`. This split is for storage efficiency:

- The list query fetches metadata only (1 small record per log) without touching the body store.
- Only the View Message action loads the content record.
- Bulk operations on log rows (status updates from provider webhooks) don't have to rewrite the body — they only touch the metadata record.

### Site-scoped via a global owner filter

The delivery log applies a per-request owner filter limiting every read to `site_id = current_site_id`. Both the per-campaign log query and the view-message action enforce this scope. So even if the log store physically contains logs from multiple sites, each site's admin only sees its own logs.

### `log_group='campaigns'` global scope

The same log store physically holds `log_group='campaigns'` (marketing sends — this surface), `log_group='system'` (transactional / notifications), and possibly other groups. The per-campaign log queries automatically exclude transactional logs because of the global filter.

### `sent_by` further differentiates

Within `log_group='campaigns'`, rows carry `sent_by`: `'campaign'` (the marketing engine — typical) vs `'system'` (transactional reusing channel infrastructure). The per-campaign log view filters by `campaign_id` so it auto-excludes system messages. Querying [[marketing-channels]] cross-campaign would show both.

### No automated retention / purge

There's no scheduled job to delete old logs. They accumulate indefinitely. The trade-off: audit-trail benefit is high (the merchant can look up a delivery from years ago); cost is log-store bloat. (verify whether an offline archival / pruning process exists outside the codebase.)

### Status-archive entries are unbounded

The `status_archive` array grows on every status change — typically 3-5 entries per row in practice. There's no archive-trimming logic. See [[campaigns-statistics-log-status-archive]].

### View-message scope enforcement

The view-message action applies the same owner / site scope as the list. A forged `log_id` returns 404 (not "forbidden"; the row simply isn't found in the site-scoped query).

## How it works

The log-list grid query builds a request with: `log_group='campaigns'` (global filter), `site_id=<current>` (owner filter), `campaign_id` + `campaign_action_id` (per-step filter), filter clauses from the request (see [[campaigns-statistics-log-filters-table]]), sort by `updated_at` desc, pagination, and the slim field set (explicitly excluding `content`). The result is a paginated page of slim metadata records — no extra query per row needed because everything the formatter consumes is already in the list view.

When the merchant clicks the channel icon, the view-message action runs a separate query that loads ONE log row (same scopes) AND its `content` record (one join to the rendered-body store). See [[campaigns-statistics-log-view-message]] for the channel-specific render paths.

Provider webhooks updating row statuses bypass the slim list view — they're targeted single-row updates found by `message_id` lookup, then a single write setting the new status. The status-archive append fires automatically whenever the status changes.

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[campaigns-statistics-log-view-message]] — the lazy-load that joins to the rendered-body store.
- [[campaigns-statistics-log-filters-table]] — the list query that uses the slim field set.
- [[campaigns-statistics-log-status-archive]] — the unbounded archive array on each row.
- [[marketing-channels]] — channel-level cross-campaign view of the same delivery log (no `campaign_id` filter).

## Open questions

- Verify whether an offline pruning / archival process exists for very old log rows.
- Verify the exact slim-field list against the latest backend.
