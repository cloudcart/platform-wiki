---
type: entity
nav_path: "Entity → Segment"
aliases: ["Segment", "Customer segment", "Subscriber segment", "Audience", "Mailing list", "List", "Сегмент", "Клиентски сегмент", "Аудитория"]
tags: [entity, marketing, customers, segments, subscribers]
plan_gates: ["segments"]
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---

# Segment

## Identity

A **Segment** is a saved query — a named rule the merchant defines once that selects a dynamic group of [[subscriber|Subscribers]] (and through them, customers and storefront visitors) matching specified conditions. Examples: "All subscribers in Bulgaria who spent more than 100 BGN in the last 30 days", "Subscribers who opted in this week but haven't ordered yet", "Customers who viewed Shoes category 3+ times". The platform stores the segment's rule tree and the list of subscribers that currently match; the count and the membership change as subscribers' behaviour changes (and, for One-time segments, when the merchant explicitly regenerates).

A Segment is the **primary audience-selection object** for marketing on the platform. Every [[campaign|Campaign]] in [[marketing-campaigns]] targets a Segment to decide who receives the send; [[discount|Discounts]] can be restricted to a Segment; cross-sell and recommendation flows can trigger on Segment membership. Segments come in two flavours — **One-time** (`regular`) and **Automated** — and on top of the rule output the merchant can hand-add or hand-remove individual subscribers. See [[marketing-segments]] for the management screen and [[marketing-segments-editor]] for the rule builder.

The Segment does NOT directly own its subscribers — the membership lives in the `segment_subscribers` / `subscriber_to_segments` pivot (M2M between [[subscriber|Subscriber]] and Segment). The pivot row carries the `manual` flag (hand-added vs rule-matched) and the `resend` flag used by campaign retry flows — see [[segment-entity-membership]].

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[segment-entity-attributes-schema]] — every key attribute the merchant configures (`name`, `title`, `type`, `conditions`, cached counts, `active`, `processing`, `inactive_errors`, `channel`, soft-delete) + the pivot row fields.
- [[segment-entity-types-onetime-automated]] — One-time (`regular`) vs Automated; AND-only composition (OR disabled); the full Automated event-trigger list; the no-fixed-cron rule.
- [[segment-entity-lifecycle]] — Created → Built → Building → Ready → Updated → Inactive → Deleted; rebuild on the `segments` queue in 500-row chunks; what Inactive does.
- [[segment-entity-membership]] — manual hand-add / hand-remove; why a manual remove does NOT survive a rebuild; the rebuild log (add/remove only); CSV export of the membership.
- [[segment-entity-relationships]] — Subscribers / Campaigns / Customers / Discounts; deletion blocked by attached campaigns; cached `subscribers_count` / `campaigns_count`; the `segments` plan cap.
- [[segment-entity-api-access]] — JSON-API v2 read-only surface, the hidden rule-tree fields, and the tag-based workaround for programmatic audiences.

## Aliases

- **Segment** — the canonical merchant-facing term in the admin UI, in [[marketing-segments]], and in campaign targeting pickers.
- **Customer segment** — used by merchants who think of the audience as "their customers"; technically a segment selects Subscribers, some of whom are also Customers.
- **Subscriber segment** — the more precise term; the segment's pivot is `segment_subscribers`.
- **Audience** / **Mailing list** / **List** — informal merchant phrasing imported from other marketing tools.
- **Сегмент** / **Клиентски сегмент** / **Аудитория** — Bulgarian terms used interchangeably.

## Key Attributes

The merchant-controlled identity of a Segment — the minimum to make it targetable. Each attribute is detailed (with column-level fidelity) on [[segment-entity-attributes-schema]].

| Attribute | What the merchant controls | Pointer |
|-----------|----------------------------|---------|
| **Name / Title** | Auto-summary `name` (from the rule) vs explicit `title` set via Rename. | [[segment-entity-attributes-schema]] |
| **Type** | `regular` (One-time) vs `automated`. Decides WHEN evaluation runs. | [[segment-entity-types-onetime-automated]] |
| **Conditions** | The AND-composed rule tree (OR currently disabled). | [[segment-entity-types-onetime-automated]] |
| **Active** | On/Off. Inactive segments don't rebuild and aren't pickable. | [[segment-entity-lifecycle]] |
| **Subscribers count** | Cached membership size; click to open the subscriber list. | [[segment-entity-relationships]] |
| **Campaigns count** | Cached count of attached campaigns; > 0 blocks deletion. | [[segment-entity-relationships]] |

## Where it appears

- [[marketing-segments]] — the master list of segments (create, activate, delete, regenerate, export).
- [[marketing-segments-editor]] — the rule builder for the conditions tree.
- [[marketing-segments-subscribers]] — the per-segment subscriber list (manual add/remove + view who matches).
- [[marketing-segments-log]] — the per-segment audit log of attach/detach events.
- [[marketing-campaigns]] — campaign creation picks a Segment as the audience.
- [[marketing-discounts]] — discounts can be restricted to a Segment.
- [[api-segments]] — the read-only JSON-API v2 surface.

## Related

### Related entities

- [[subscriber]] — the elements of a Segment's membership. M2M via `segment_subscribers`.
- [[customer]] — Customers and Subscribers can share an email; segment conditions on order data read through the Customer's stats.
- [[campaign]] — every Campaign targets exactly one Segment; a Segment can host any number of Campaigns.
- [[discount]] — Discounts can be restricted to a Segment.

### Cross-cutting concepts

- [[subscriber-vs-customer]] — Segments select Subscribers, not Customers; the two are independent records.
- [[notification-delivery]] — how Segment membership feeds into the channel-by-channel delivery decision.
- [[plan-gates]] — `segments` count cap.

### Settings & feature pages

- [[marketing-segments]] — primary admin screen.
- [[marketing-segments-editor]] — conditions UI.
- [[marketing-segments-log]] — rebuild audit log.
- [[marketing-segments-subscribers]] — manual hand-add / hand-remove.

## Open Questions

No outstanding questions — all items resolved or distributed to sub-pages.
