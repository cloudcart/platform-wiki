---
type: entity
nav_path: "Entity → Segment → One-time vs Automated"
aliases: ["One-time segment", "Automated segment", "Regular segment", "Segment type", "AND-only conditions", "OR disabled", "Automated segment triggers", "Еднократен сегмент", "Автоматизиран сегмент"]
tags: [entity, marketing, segments, automation, conditions]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[segment]]. See the hub for the other aspects (attributes schema, lifecycle, membership, relationships, API access).

# Segment — One-time vs Automated

## Identity

Every [[segment|Segment]] is one of two shapes set by its `type` field: **One-time** (`regular`) or **Automated**. Both shapes share the exact same condition vocabulary and rule-tree structure — they differ only in **WHEN** the rule is evaluated against the subscriber population. This page covers that distinction, the AND-only composition limit, and the full list of subscriber-side events that drive an Automated segment's incremental re-evaluation.

## Aliases

- **One-time** = **Regular** = `regular` — a snapshot list, regenerated on demand.
- **Automated** = `automated` — a live list that tracks subscriber state continuously.
- **AND-only** — the current composition mode; OR is held back.

## Key Attributes

### One-time (`regular`) vs Automated

- **One-time** (`regular`): the merchant clicks **Generate** to evaluate the rule. Membership is a snapshot. Editing conditions does NOT auto-regenerate — the merchant must click Generate again. Useful when the merchant wants a stable list for a one-off campaign without per-event churn.
- **Automated**: the platform listens to subscriber-side events (registration, order placed, address change, opt-in change, segment-eligibility event) and re-evaluates the matching condition incrementally. Used for ongoing nurture flows where the audience should always reflect current state.

Both types support the same condition vocabulary; they differ only in WHEN evaluation runs. The lifecycle states they pass through are shared — see [[segment-entity-lifecycle]].

### AND-only composition (OR is currently disabled)

The condition builder composes rules with **AND only**. The UI has an OR toggle that is currently disabled — the merchant cannot create a rule like "Country = Bulgaria OR Country = Romania" in a single Segment. The workaround is two Segments (one per condition) and target both campaigns. The OR toggle is held back in the current release. Each condition is a `<field> <operator> <value>` triple; the full rule tree is authored only in the visual builder on [[marketing-segments-editor]] (the API does not expose it — see [[segment-entity-api-access]]).

### Automated segment event triggers (full list)

Each event class is mapped to a listener that incrementally evaluates the affected subscriber against the segment's conditions:

- **Customer events** — create / update / delete, marketing-opt-in change, tag change, custom-field create, billing-address create / delete, shipping-address create / delete, login / register / guest-register.
- **Order events** — create + post-create, status change, payment sync, product add / edit / remove, shipping change, fulfillment add / remove, product discount add / remove, modification remove.
- **Cart events** — cart create / update, cart item create / update / delete.
- **Catalog cascade events** — vendor delete, category delete.

### No fixed cron for Automated segments

There is **no fixed cron** for Automated segments — they rely entirely on these incremental events. Full rebuilds run only on **Generate** click (for One-time segments) or on conditions-edit (for both types). The merchant can manually trigger a full rebuild from [[marketing-segments]]. The mechanics of that rebuild (the `segments` queue, 500-row chunks) are on [[segment-entity-lifecycle]].

## Where it appears

- [[marketing-segments]] — the type is chosen at create time and shown as a column; the Generate button is the One-time evaluator.
- [[marketing-segments-editor]] — the conditions builder (AND-composed rule tree).
- [[marketing-segments-log]] — the per-event attach/detach trail for Automated segments — see [[segment-entity-membership]].

## Related

- [[segment]] — hub.
- [[subscriber]] — the records evaluated against the rule; the source of the trigger events.
- [[customer]] — Customer-side events (orders, addresses, tags) trigger Automated re-evaluation.
- [[order]] — order events are a major Automated trigger source.
- [[marketing-segments-editor]] — the conditions UI.

## Open Questions

No outstanding questions.
