---
type: entity
nav_path: "Entity → Segment → Lifecycle"
aliases: ["Segment lifecycle", "Segment states", "Segment rebuild", "segments queue", "500-row chunks", "Inactive segment", "Segment generate", "Жизнен цикъл на сегмент", "Преизграждане на сегмент"]
tags: [entity, marketing, segments, lifecycle, queue]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[segment]]. See the hub for the other aspects (attributes schema, types, membership, relationships, API access).

# Segment — Lifecycle

## Identity

A [[segment|Segment]] moves through a sequence of states from creation to deletion, with an asynchronous rebuild step in the middle that evaluates the rule tree against the subscriber population. This page maps those states, the rebuild mechanics (the `segments` queue, 500-row chunks), and what the Inactive state does to recalculation and campaign picking.

## Aliases

- **Building** — the async rebuild phase (`processing = 1`).
- **Rebuild** / **Regenerate** — re-evaluation of the full rule tree against all subscribers.
- **Inactive** — `active = no`; recalculation paused.

## Key Attributes

### The state sequence

1. **Created** — the merchant clicks Add Segment on [[marketing-segments]], picks a type, names it, and starts building the rule on [[marketing-segments-editor]]. At create time, `subscribers_count = 0` and `last_generated_at = null` ("Not generated yet").
2. **Built** — the merchant has finished the rule tree. For an Automated segment, the platform immediately enqueues a full rebuild job; for a One-time segment, the merchant clicks Generate to start the rebuild. (Type semantics: [[segment-entity-types-onetime-automated]].)
3. **Building** (async) — the rebuild job runs on the `segments` queue, evaluating the rule tree against the subscriber population in 500-row chunks. While `processing = 1` the list shows the *"Your subscribers are currently being filtered, please check again later"* placeholder. Progress is visible in [[marketing-segments-log]]. For large stores, this can take seconds to minutes.
4. **Ready** — `last_generated_at` is set and `subscribers_count` reflects the current matching membership. Automated segments stay in this state and update incrementally on subscriber-side events; One-time segments stay frozen until the next Generate click.
5. **Updated** — conditions or membership changed. Conditions edits trigger a full rebuild on save. Subscriber-side events that match an Automated segment's rule trigger an incremental attach (add the subscriber) or detach (remove the subscriber if they no longer match — but only if the row is NOT manual). Manual hand-adds and hand-removes are immediate — see [[segment-entity-membership]].
6. **Inactive** — `active = no`. Rebuild jobs skip this segment; campaign target pickers exclude it; existing campaign references see the frozen membership. The merchant can toggle back to Active to resume.
7. **Archived / Deleted** — deletion is blocked when `campaigns_count > 0` with the message "You cannot delete a segment that has a campaign attached to it. To delete a segment, you must first delete a campaign". Detach or delete the campaigns first; then the segment can be removed — see [[segment-entity-relationships]].

### Rebuild via the `segments` queue in 500-row chunks

The full-rebuild job (triggered by Generate, by condition edits, or by a manual rebuild for Automated segments) runs on the `segments` queue. The platform paginates the subscriber population in **500-subscriber chunks** to avoid long-running database transactions. Large stores (millions of subscribers) may see the rebuild take minutes; the rebuild log surfaces progress. The merchant experiences this as a delay between clicking Generate and the `subscribers_count` updating — the placeholder text is shown throughout.

### Inactive segments don't rebuild and aren't pickable

When the merchant toggles `active = no`:

- Rebuild jobs skip the Segment.
- The Campaign target picker hides it.
- Existing Campaigns that reference the Segment continue to see the frozen membership (so an in-flight Campaign isn't broken).

Toggling back to Active triggers an immediate rebuild. Note: toggling Inactive does **not** free a plan-cap slot — only deletion does (see [[segment-entity-relationships]]).

### Self-disable on a broken condition

A Segment can auto-move to Inactive if a condition becomes unevaluable (e.g. the app that contributed a condition is uninstalled). The error strings land in `inactive_errors` and are surfaced via the disabled-segment message — see [[segment-entity-attributes-schema]].

## Where it appears

- [[marketing-segments]] — the list with the Active toggle, the Generate action, the manual rebuild trigger, and the `processing` placeholder.
- [[marketing-segments-log]] — the per-rebuild attach/detach progress trail.
- [[marketing-segments-editor]] — editing conditions here triggers a full rebuild on save.

## Related

- [[segment]] — hub.
- [[subscriber]] — the population evaluated during a rebuild.
- [[campaign]] — Inactive segments are hidden from the campaign target picker.
- [[marketing-segments-log]] — rebuild progress + audit.

## Open Questions

No outstanding questions.
