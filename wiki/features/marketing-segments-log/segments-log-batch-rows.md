---
type: feature
nav_path: "Marketing → Segments → Log → Batch vs single rows"
route_name: segments.core_new.log
route_path: /admin/marketing-new/segments/log/:id
aliases: ["Segment log batch rows", "Segment log head rows", "Segment log drill-down", "Segment log single vs batch", "Сегмент лог пакетни записи"]
tags: [marketing, segments, log, audit, batch]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
> Part of [[marketing-segments-log]]. See the hub for the other aspects (the table UI, the action vocabulary, and the storage model).

# Segment log — batch (`head`) vs single rows

## Purpose

This page explains **why a 1,000-subscriber rebuild shows up as one "Added subscribers to customer segment" line instead of 1,000 rows**, what the two physical row types are, and why there's no expand / drill-down button on the modern page. It's the page to read when a merchant asks *"the segment added a thousand people but the log only shows one entry — where are the rest?"*.

## Where to find it

These row types render in the **Action** / **Subscriber** columns of the Segment log table at `/admin/marketing-new/segments/log/:id` — see [[segments-log-table-ui]]. A `head` row shows the batch label and a dash in the Subscriber column.

## What the merchant can do here

- **See the batch-header line** for any bulk regeneration that touched 2+ subscribers.
- **See an individual row** for any event that touched exactly one subscriber.
- The merchant **cannot** expand a batch header to its child rows on the modern UI (the per-subscriber children are not browseable here). To inspect which specific subscribers a rebuild affected, use the [[marketing-segments-subscribers]] log per subscriber.

## Settings & fields

### Two row types — `head` (batch header) and `single-row`

The log distinguishes between two physical row types shown on the list:

- **`head`** — a batch header row created when the platform processes a bulk add / remove (e.g., a regeneration run added 1,200 subscribers at once). The header carries no individual subscriber and renders as "Added subscribers to customer segment:name" / "Removed subscribers from customer segment:name". For `head` rows, the `name` (Subscriber) column is **explicitly nulled** so the cell renders as the dash.
- **`single-row`** — an individual event tied to one subscriber (joined / left / channel change / etc.).

The list view filters to only these two row types (`whereIn('type', ['head', 'single-row'])`). The per-subscriber children of a `head` batch are stored separately (with `type = 'row'` and a `parent_id` referencing the header) and are **not** shown on the main list.

## Business rules

### Single vs batch write path — count-based threshold

The platform decides "single-row" vs "head + batch" based on the **count of subscribers in the event**:

- **Exactly 1 subscriber** in the add / remove event → ONE `single-row` log entry, no parent.
- **2 or more subscribers** → ONE `head` row (`type = 'head'`, action `begin_added_to_segment` / `begin_removed_from_segment` — see [[segments-log-actions]]) PLUS one `type = 'row'` child per subscriber, each linked via `parent_id` to the head.

So a 1,000-subscriber rebuild produces 1 head + 1,000 child rows in storage, but only the head shows on the list.

### Drill-down into a batch is NOT exposed on the modern UI

A legacy `viewList` endpoint exists on the backend that returns rows filtered by `parent_id` (i.e., the children of a chosen `head`), but the modern Vue page does **not** call it — there is no Drill-down button, no expansion arrow, and no per-`head` modal in the current build. The batch drill-down is a legacy feature. To inspect which specific subscribers were affected in a batch, the merchant must use the [[marketing-segments-subscribers]] log per subscriber. (The list-data formatter projects each row through `formatCpList`, rendering `name`, `action`, `info`, and `created_at`; the `name` is nulled for `head` rows.)

### Log writes run on a dedicated, single-flighted queue

The segment log-write job runs on a dedicated queue (separate from the main segment processing) and is **single-flighted** — meaning only one log-writer runs at a time per site, so concurrent rebuilds queue up rather than competing for the collection. The log is written asynchronously, so the "Last generated at" timestamp on the parent segment list may update slightly **before** the log row appears — which, combined with the 30-second cache on [[segments-log-table-ui]], is why a freshly-rebuilt segment's newest entries can take a moment to show.

## Related

- [[marketing-segments-log]] — hub.
- [[marketing-segments-subscribers]] — the per-subscriber log is the substitute for the missing batch drill-down.
- [[marketing-segments]] — a regeneration run on this list is what produces a batch.

## Open questions

The modern UI never exposes batch drill-down; whether CloudCart intends to re-add it on the Vue page is unknown `(verify)`.
