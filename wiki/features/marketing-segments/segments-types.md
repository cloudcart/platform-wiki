---
type: feature
nav_path: "Marketing → Segments → Types (One-time vs Automated)"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment type", "One-time segment", "Automated segment", "regular segment", "automated segment", "TYPE_REGULAR", "TYPE_AUTOMATED"]
tags: [marketing, segments, types, automation]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-segments]]. See the hub for related aspects (list page, create popup, conditions, rebuild mechanics).

# Segments — One-time vs Automated

## Purpose

This aspect documents the two segment types — **One-time** (`regular`) and **Automated** (`automated`) — chosen at creation and immutable thereafter. The merchant's choice decides whether the segment is a one-shot snapshot or a continuously-reconciled population.

## Where to find it

Chosen on the [[segments-create-popup]] (sub-card under "New segment from scratch"). The chosen value is then immutable for the lifetime of the segment.

## What the merchant can do here

- Pick **One-time** for a snapshot at a moment in time (e.g., "everyone who matched last Friday at 18:00").
- Pick **Automated** for a continuously-synced audience (e.g., "anyone who currently fits 'cart abandoner'").
- Re-generate a One-time segment manually any time — see [[segments-rebuild-mechanics]] § One-time rebuild.

## Settings & fields

### Type values (verbatim)

- **One-time** — frontmatter / API value: `regular`. Constant label: `TYPE_REGULAR`. UI label: "One-time".
- **Automated** — frontmatter / API value: `automated`. Constant label: `TYPE_AUTOMATED`. UI label: "Automated".

Both types live in the same `subscribers_segments` table; the difference is whether event listeners (`SubscribersAddedToSegment`, `SubscribersRemovedFromSegment`, `SetCustomerToSegment`, etc.) re-evaluate per event or wait for manual regeneration.

## Business rules

### One-time (`regular`)

The segment is computed when the merchant clicks "Generate" (or the platform's background sweep runs). It produces a snapshot — subscribers who qualified at that moment. New qualifying subscribers do not automatically join unless the merchant re-generates.

- Manually re-generating runs the same single-segment job again (`set_subscribers_to_single_segment`).
- Saving a conditions edit ALSO triggers an immediate rebuild — there is no separate manual "Generate" trigger needed after editing. See [[segments-rebuild-mechanics]].
- One-time segments are **excluded** from the 5-minute Automated sweep entirely.
- Does **not** count toward the `segments` plan-feature cap (which limits Automated only). See [[segments-api-and-plan-gates]].

### Automated (`automated`)

The segment is continuously kept in sync. Every relevant subscriber/order/cart event triggers a re-evaluation for the affected subscriber, attaching or detaching them from the segment. This is the right choice for "Customers who haven't ordered in the last 60 days" or "Cart abandoners" — segments that need to track lifecycle state in real time.

- Plan-gated by `segments` (numeric cap on the number of Automated segments). See [[segments-api-and-plan-gates]].
- Subject to the 5-minute background sweep AND per-event incremental re-evaluation. See [[segments-rebuild-mechanics]].
- The list-page status icon is a **green pulsing blob** when healthy, **greyed-out blob** when inactive. See [[segments-list-page]].

### Type is immutable after create

There is no UI to change a segment's type after creation. The merchant who needs the other type must delete the segment and create a fresh one (which may be blocked if a campaign references it — see [[marketing-segments]] § Business rules).

Practical consequence for the templates and AI flows in [[segments-create-popup]]: both always produce **One-time** segments, so the merchant who wants an Automated "Cart abandoners" segment must build it from scratch rather than picking the template.

### Choice guidance

- Pick **One-time** when the audience is a one-off send target (a single campaign, a one-time export) and the membership list as of "now" is what matters.
- Pick **Automated** when the audience is a living thing (lifecycle marketing — winback, churn risk, VIP graduation) and the merchant expects new subscribers to flow in / out automatically.

## Related

- [[marketing-segments]] — hub.
- [[segments-create-popup]] — where the merchant picks the type.
- [[marketing-segments-editor]] — opens with the type fixed.
- [[segments-rebuild-mechanics]] — defines the actual rebuild cadence per type.
- [[segments-api-and-plan-gates]] — the `segments` cap counts only Automated.
- [[marketing-campaigns]] — primary consumer; campaign-target picking shows both types.

## Open questions

None.
