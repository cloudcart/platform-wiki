---
type: feature
nav_path: "Marketing → Segments → Log"
route_name: segments.core_new.log
route_path: /admin/marketing-new/segments/log/:id
aliases: ["Segment log", "Segment audit log", "Segment processing log", "Segment changes log", "Сегмент лог", "История на сегмент"]
tags: [marketing, segments, log, audit, subscribers]
plan_gates: ["segments"]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---
# Segment log

## Purpose

The **Segment log** is the per-segment audit trail showing every subscriber **add / remove / channel change / tag change / identification event** that has occurred against this segment over time. It's the merchant's *"who came in, who went out, and why"* view — combined with the [[marketing-segments]] subscriber count and "Last generated at" timestamp, it answers two recurring questions:

- *"Did my segment update after I changed the conditions?"* — sorting by date descending, the merchant sees the latest batch of additions / removals and confirms the segment ran.
- *"Why did subscriber X end up in (or leave) this segment?"* — each log row links to the subscriber's detail modal where the merchant can inspect their channels, RFM bucket, tags, and order history.

The page is read-only — the merchant cannot edit or delete log rows. The log is a history that grows over the segment's lifetime and is cleared only when the parent segment is deleted.

## Where to find it

From the [[marketing-segments]] list, click the **Log** link on any segment row. The breadcrumb reads "Marketing → Campaigns → Segments → \<segment name\>". The route is `/admin/marketing-new/segments/log/:id`. The header shows the segment's name (truncated to 50 characters if longer) and a chart-bar icon.

## What the merchant can do here

- **See every log entry** for this segment in a paginated table — default sort is **created_at desc** (newest first). See [[segments-log-table-ui]].
- **Click a row's subscriber name** (or action label) to open the **Subscriber details modal** — see [[segments-log-table-ui]] for the modal handshake.
- **Read the action type + channel detail** of each entry — the full vocabulary is on [[segments-log-actions]].
- **Sort by date** and **paginate** at 25 rows per page.

The merchant **cannot** filter the log, export it, delete rows, or edit the segment from here. For details on every constraint, see [[segments-log-table-ui]].

## Settings & fields

The four visible columns (**Action**, **Subscriber**, **Info**, **Date**), their cell rendering, sorting, pagination, and the modal query-string behaviour are documented on [[segments-log-table-ui]]. The complete action-key vocabulary (what each icon / label means and when it fires) plus the channel-label map for the Info column are on [[segments-log-actions]]. This hub carries no fields of its own.

## Business rules

The Segment log is **append-only** — rows are created when an event fires and never edited, purged only when the parent segment is deleted. The underlying history, the snapshot fields it preserves, and the fact that the same collection also feeds the subscriber-detail log are covered on [[segments-log-storage-model]]. The log distinguishes single-event rows from batch-header rows based on a count threshold, and a batch drill-down exists in the backend but is **not exposed on the modern UI** — see [[segments-log-batch-rows]].

Because the Segment log is a sub-view of [[marketing-segments]], it inherits the same plan gate (`segments` feature key). A merchant whose plan doesn't include Segments never sees the list and so cannot reach the log.

## Sub-pages (in this cluster)

- [[segments-log-table-ui]] — the page layout: the four columns, sorting, pagination, the read-only constraints, page-mount URL normalisation, the subscriber-modal query-string handshake, and the 30-second cache.
- [[segments-log-actions]] — the action-key vocabulary that drives each row's icon + label (added / removed / identified / channel / tag / RFM / marketing) plus the channel-label map used in the Info column.
- [[segments-log-storage-model]] — the append-only audit-trail model: what's stored per row, the segment-state and subscriber-identity snapshots, delete-on-segment-delete, and how the same collection feeds the subscriber-detail log.
- [[segments-log-batch-rows]] — `head` vs `single-row` types, the count-based single-vs-batch write path, why batch drill-down is not exposed on the modern UI, and the dedicated single-flighted log queue.

## Related

- [[marketing-segments]] — the parent list; the **Log** column links here per segment.
- [[marketing-subscribers]] — clicking a subscriber row opens this entity's detail modal.
- [[marketing-campaigns]] — campaigns also have their own log (log_group `campaigns`) using the same collection; the action vocabulary partly overlaps.
- [[segment]] — entity page for the segment record.
- [[subscriber]] — entity page for the subscriber records that drive the log.
- [[subscriber-vs-customer]] — concept; the log distinguishes subscriber events from customer-attach events.

## Open questions

No outstanding questions.
