---
type: feature
nav_path: "Marketing → Segments → Log → Storage & snapshots"
route_name: segments.core_new.log
route_path: /admin/marketing-new/segments/log/:id
aliases: ["Segment log storage", "Segment log audit trail", "Segment log snapshots", "Segment log retention", "Сегмент лог съхранение"]
tags: [marketing, segments, log, audit, storage]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
> Part of [[marketing-segments-log]]. See the hub for the other aspects (the table UI, the action vocabulary, and batch rows).

# Segment log — storage model & snapshots

## Purpose

This page explains **what the Segment log actually stores and why it can be trusted as an audit trail**: that rows are append-only, that each row snapshots the segment's and subscriber's state at the moment of the event, when the history is purged, and how the same history is also surfaced from the subscriber's own detail panel. It's the page to read when a merchant asks *"why does the log show an old name / old conditions?"* or *"will deleting the segment lose this history?"*.

## Where to find it

The merchant never sees the storage directly — it backs the table at `/admin/marketing-new/segments/log/:id` (see [[segments-log-table-ui]]) and the subscriber-detail log tab on the [[marketing-subscribers]] panel.

## What the merchant can do here

There are no controls — the storage is read-only history. The merchant can only **view** the rows it produces; the relevant behaviours are: trust that the row reflects state-at-event-time, and know that the whole history disappears only on segment delete.

## Settings & fields

### What's stored per log row

Each log row carries:

- `_id`, `type` (`head` / `single-row`), `log_group` (always `segments` on this page).
- `subscriber_id`, `customer_id`, `first_name`, `last_name`, `country`.
- `action` (one of the action keys on [[segments-log-actions]]), `channel`, `channel_identifier`.
- `site_id`, `created_at`, `updated_at`.
- `segment_id`, `segment_name`, `segment_conditions` (snapshot of the conditions at the time of the event), `segment_channel`.
- `customer_first_name`, `customer_last_name`, `customer_email`, `subscribed`, `unsubscribed`.
- `parent_id` (links a `single-row` to its `head` batch — see [[segments-log-batch-rows]]), `rfm`, `tags`, `marketing`, `initiator`, `campaign_id`, `campaign_name`.

Only the merchant-facing columns (Action / Subscriber / Info / Date) are rendered — the rest are used for filtering, drill-down navigation, and downstream analytics.

## Business rules

### Append-only history — never edited, never deleted (except on segment delete)

Each log row is **created when an event fires** and is never modified afterward. The collection (log_group `segments`) holds the rows. It is purged only when the **parent segment is deleted** (the `SegmentDeleted` event triggers the cleanup, alongside removing the `subscribers_segments` pivot rows).

This means the log is a **historical audit trail**, not a live state view. If a subscriber is added today and removed tomorrow, both events stay in the log — the merchant sees the full lifecycle.

### Log row snapshots the segment state at the time

Each log row stores `segment_name`, `segment_conditions` (the `conditions_formatted` text), and `segment_channel` snapshots — so if the merchant later renames or re-conditions the segment, the log preserves what the conditions **were** when the subscriber attached / detached. This is the audit-trail guarantee.

### Subscriber identity at log-write time

The subscriber's `first_name`, `last_name`, and `country` are also snapshotted on the log row. So if the merchant edits the subscriber's profile later, the log still shows the **original** name on the row — but clicking the row opens the **live** subscriber detail modal (which shows the current name). Minor UX implication: a log row can show a slightly stale name while the modal shows the up-to-date data. See [[segments-log-table-ui]] for the modal handshake.

### Customer linkage at log-write time

If the subscriber was linked to a Customer at the moment of the event, `customer_id` and the customer-side fields (`customer_first_name`, `customer_last_name`, `customer_email`) are also captured. This means the row can show the linked-customer info even if the link was later removed.

### Same audit collection feeds Subscriber detail

The subscriber's own marketing-change log (visible from the [[marketing-subscribers]] detail panel) reads from the **same collection** but filters by `subscriber_id` instead of `segment_id`. So the merchant has two lenses on the same data: "what's happened to THIS subscriber across all segments / campaigns" vs. "what's happened to THIS segment across all subscribers". The campaign logs ([[marketing-campaigns]]) also share the collection under log_group `campaigns`.

## Related

- [[marketing-segments-log]] — hub.
- [[marketing-segments]] — deleting the segment from here is what purges the log.
- [[marketing-subscribers]] — the subscriber-detail log reads the same history filtered by subscriber.
- [[subscriber-vs-customer]] — concept; the row captures both subscriber and (when linked) customer identity.
- [[segment]] — entity whose name / conditions are snapshotted onto each row.

## Open questions

No outstanding questions.
