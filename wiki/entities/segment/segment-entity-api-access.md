---
type: entity
nav_path: "Entity → Segment → API access"
aliases: ["Segment API", "Segments JSON-API", "Segment read-only API", "Segment API hidden fields", "Programmatic segment audience", "Tag-based segment workaround", "API сегменти"]
tags: [entity, marketing, segments, api, json-api-v2]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[segment]]. See the hub for the other aspects (attributes schema, types, lifecycle, membership, relationships).

# Segment — API access

## Identity

[[segment|Segments]] are exposed via **JSON-API v2** at [[api-segments]] — but **read-only**. The resource is registered as `readOnly`, so an external integration can enumerate segments and read membership, but cannot author or edit them. This page documents the supported methods, the fields the schema hides, and the tag-based workaround for building programmatic audiences.

## Aliases

- **Segments API** — the [[api-segments]] resource at `/api/v2/segments`.
- **Read-only resource** — no POST / PATCH / DELETE.
- **Tag-based audience** — the supported pattern for API-driven targeting.

## Key Attributes

### Read-only endpoint surface

| Method | Path | Supported |
|---|---|---|
| GET | `/api/v2/segments` | Yes — list. |
| GET | `/api/v2/segments/{id}` | Yes — fetch one. |
| GET | `/api/v2/segments/{id}/subscribers` | Yes — current membership. |
| POST / PATCH / DELETE | — | **Not supported.** Author via [[marketing-segments-editor]]. |

### Hidden fields

The schema **hides** `conditions`, `conditions_formatted`, `inactive_errors`, `processing`, `deleted_at` from responses. The rule tree is a deeply nested payload the API does not expose — the visual builder on [[marketing-segments-editor]] is the only authoring surface because it gates conditions by installed apps, applies parent-scoped resolution for ambiguous keys, and runs each value through a per-condition validator. The exposed fields are the merchant-meaningful ones (`name`, `title`, `type`, `subscribers_count`, `campaigns_count`, `active`, `last_generated_at`/`last_execute`) — defined on [[segment-entity-attributes-schema]].

### What integrations use it for

Integrations use [[api-segments]] to:

- enumerate segments for an external picker,
- read membership for downstream targeting,
- monitor `subscribers_count` / `campaigns_count`,
- check `active` state.

### Workaround for programmatic audiences

Because the API can't author segments, integrations build audiences indirectly: POST subscribers + tags via [[api-subscribers]] + [[api-subscribers-tags]], then a merchant defines an **Automated** Segment with a tag-based rule. The tag is the API contract; the rule tree stays in the visual builder. The Automated segment then attaches matching subscribers incrementally as tags arrive — see [[segment-entity-types-onetime-automated]] for the event-driven attach behaviour.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

## Where it appears

- [[api-segments]] — the read-only JSON-API v2 resource page.
- [[api-subscribers]] / [[api-subscribers-tags]] — the write surfaces used in the tag-based workaround.
- [[marketing-segments-editor]] — the only authoring surface for the rule tree.

## Related

- [[segment]] — hub.
- [[api-segments]] — the resource page.
- [[subscriber]] — membership read via `/segments/{id}/subscribers`.
- [[json-api-v2]] — auth, rate limits, side-effects.
- [[plan-gates]] — the `segments` cap still applies to API-created tag-based audiences (the segment itself is created in the UI).

## Open Questions

No outstanding questions.
