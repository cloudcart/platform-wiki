---
type: entity
nav_path: "Entity → Segment → Relationships"
aliases: ["Segment relationships", "Segment and Campaign", "Segment and Subscriber", "Segment deletion blocked", "Segment plan cap", "segments plan gate", "Segment cached counts", "Връзки на сегмент"]
tags: [entity, marketing, segments, relationships, plan-gates]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[segment]]. See the hub for the other aspects (attributes schema, types, lifecycle, membership, API access).

# Segment — Relationships

## Identity

A [[segment|Segment]] sits at the centre of the marketing graph: it has a membership of [[subscriber|Subscribers]], it is targeted by [[campaign|Campaigns]] and [[discount|Discounts]], and it reads through [[customer|Customer]] data for order-based conditions. This page maps each relation, the deletion-blocked-by-campaigns rule, the cached counts, and the `segments` plan cap.

## Aliases

- **Attached campaign** — a campaign whose `campaign.segment_id` points at this segment; counted in `campaigns_count`.
- **Plan cap** — the `segments` plan-feature key capping the number of segments.

## Key Attributes

### What a Segment relates to

A Segment:

- **Has many** [[subscriber|Subscribers]] via the `segment_subscribers` pivot — the membership. Two kinds of rows coexist (rule-matched vs `manual`); see [[segment-entity-membership]].
- **Has many** [[campaign|Campaigns]] via `campaign.segment_id` — every campaign points to exactly one Segment as its audience. A Segment can be the target of any number of campaigns. When a segment is in use, deletion is blocked (below).
- **Has many** rebuild-log entries — see [[marketing-segments-log]]. Each entry records a subscriber added to or removed from the segment, with the timestamp and the trigger event. Used for audit and to debug "why didn't this subscriber receive the campaign?".
- **References** the [[customer|Customer]] indirectly: a Subscriber that matches a Customer's email shares behaviour data; segment rules that reference order data (e.g., "spent more than 100 BGN") read through the Customer record.

A Segment is targeted by:

- [[campaign|Campaigns]] (`campaign.segment_id`) — the campaign send list.
- [[discount|Discounts]] where the merchant restricts a discount to a specific Segment.

### Deletion is blocked by attached campaigns

A Segment with at least one attached [[campaign|Campaign]] cannot be deleted. The platform returns the message "You cannot delete a segment that has a campaign attached to it. To delete a segment, you must first delete a campaign". The merchant must detach the campaigns (point them at a different segment) or delete the campaigns first. (Deletion itself is a soft-delete — `deleted_at` — see [[segment-entity-attributes-schema]].)

### Cached counts (`subscribers_count`, `campaigns_count`)

`subscribers_count` and `campaigns_count` are cached on the Segment row, not live-computed. They update during rebuilds and on campaign-pivot changes. The merchant clicks the count to expand the actual rows.

- **`subscribers_count`** is refreshed by the rebuild pipeline — see [[segment-entity-lifecycle]].
- **`campaigns_count`** is maintained via the `campaigns` relation's count query. When a Campaign is deleted, the next list-page load re-queries and reflects the lower count. The cached value is also recomputed on rebuild and on campaign-pivot changes, so the count is generally fresh within seconds of the delete.

### Plan gate: `segments`

The platform's `segments` plan-feature key caps the number of Segments the merchant can create. When the cap is hit, the Add Segment button still opens the dialog but save fails with a plan-upgrade prompt.

The cap counts **ALL** Segments — active AND inactive. There is no distinction. To free up cap headroom, the merchant must **delete** unused inactive Segments; toggling a Segment to Inactive alone does NOT free its slot (the Inactive state is covered on [[segment-entity-lifecycle]]).

## Where it appears

- [[marketing-segments]] — the list showing `subscribers_count`, `campaigns_count`, and the deletion-blocked message.
- [[marketing-campaigns]] — campaign creation picks a Segment; this is what populates `campaigns_count`.
- [[marketing-discounts]] — discount restriction to a Segment.
- [[marketing-segments-log]] — rebuild-log relation.

## Related

### Related entities

- [[segment]] — hub.
- [[subscriber]] — the membership; M2M via `segment_subscribers`.
- [[campaign]] — every Campaign targets exactly one Segment; attached campaigns block deletion.
- [[customer]] — order-based conditions read through the Customer record.
- [[discount]] — Discounts can be restricted to a Segment.

### Cross-cutting concepts

- [[plan-gates]] — the `segments` count cap.
- [[subscriber-vs-customer]] — Segments select Subscribers, not Customers.

## Open Questions

No outstanding questions.
