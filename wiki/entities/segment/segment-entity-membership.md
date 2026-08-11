---
type: entity
nav_path: "Entity → Segment → Membership"
aliases: ["Segment membership", "Manual hand-add", "Manual hand-remove", "Segment manual flag", "Segment rebuild log", "Manual remove does not survive rebuild", "Segment CSV export", "Членство в сегмент", "Ръчно добавяне към сегмент"]
tags: [entity, marketing, segments, subscribers, membership]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[segment]]. See the hub for the other aspects (attributes schema, types, lifecycle, relationships, API access).

# Segment — Membership

## Identity

A [[segment|Segment]]'s membership is the set of [[subscriber|Subscribers]] currently attached via the `segment_subscribers` pivot. Two kinds of rows coexist on the same pivot: **rule-matched** (auto-attached, auto-detached when the subscriber stops qualifying) and **manual** (hand-added by the merchant, never auto-detached). This page covers the manual hand-add / hand-remove behaviour, the critical asymmetry that a manual *remove* does NOT survive a rebuild, the rebuild log, and CSV export.

## Aliases

- **Manual row** — a pivot row with `manual = 1`, immune to rebuild detach.
- **Hand-add** / **Hand-remove** — merchant actions on [[marketing-segments-subscribers]].
- **Rebuild log** — the per-attach/detach audit trail on [[marketing-segments-log]].

## Key Attributes

### Manual hand-adds and hand-removes

On top of the rule output, the merchant can manually add a subscriber to a Segment via the [[marketing-segments-subscribers]] screen (Add Subscriber to Segment button). The pivot row is flagged `manual = yes`. **Manual rows are immune** to rebuild — they stay in the Segment even if they don't match the rule. The merchant can also manually remove a subscriber; if the row was rule-matched, the platform recreates it on the next rebuild; if it was manual, it stays removed. The `manual` flag lives on the pivot row — see [[segment-entity-attributes-schema]].

### Manual hand-remove does NOT survive a rebuild

This is the most-misunderstood membership rule. If the merchant removes a subscriber from a **rule-matched** segment, the next full rebuild **re-attaches** them — the pivot flag protecting manual edits only covers manual **ADDS**, not manual **REMOVES**. To permanently exclude a rule-matched subscriber, the merchant must adjust the segment's rule (e.g., add an exclusion condition) rather than hand-remove the row.

### Rebuild log records only add/remove, not the matching condition

The rebuild log (on [[marketing-segments-log]]) captures only the fact of add / remove (segment ID, subscriber ID, action) — NOT the specific condition that started or stopped matching. To debug "why was this subscriber removed?", the merchant must inspect the current condition tree against the subscriber's current profile. The log is the first place to check for "why didn't this subscriber receive the campaign?" tickets.

### CSV export of segment subscribers

The segment list row has a Generate CSV File action that exports the current membership as CSV — useful for one-off marketing exports to external tools, ESP imports, or compliance audits. The export reflects the membership at the moment of export (a snapshot), not a live feed.

### Incremental vs full membership changes

- **Full rebuild** (Generate / conditions-edit) — re-evaluates every subscriber in 500-row chunks; see [[segment-entity-lifecycle]].
- **Incremental** (Automated segments only) — a subscriber-side event attaches or detaches a single subscriber; see [[segment-entity-types-onetime-automated]] for the full event-trigger list.
- **Manual** — immediate; bypasses both paths; the `manual` flag governs survival.

## Where it appears

- [[marketing-segments-subscribers]] — the per-segment subscriber list; Add / Remove Subscriber actions.
- [[marketing-segments-log]] — the attach/detach audit trail.
- [[marketing-segments]] — the Generate CSV File action and the `subscribers_count` link.

## Related

- [[segment]] — hub.
- [[subscriber]] — the membership elements; M2M via `segment_subscribers`.
- [[campaign]] — campaigns send to the membership; the rebuild log explains non-delivery.
- [[marketing-segments-subscribers]] — manual add/remove screen.

## Open Questions

No outstanding questions.
