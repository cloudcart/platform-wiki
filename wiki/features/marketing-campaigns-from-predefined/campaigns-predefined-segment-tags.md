---
type: feature
nav_path: "Marketing → Campaigns → Create campaign → From template → Segment & tags"
route_name: admin.api.campaigns.create
route_path: /admin/api/core/marketing/campaigns/create/automated/{id}
aliases: ["Predefined segment handling", "Predefined tag auto-add", "Segment auto-create on clone", "Шаблонна кампания — сегмент и тагове"]
tags: [marketing, campaigns, predefined, templates, segments, tags]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
> Part of [[marketing-campaigns-from-predefined]]. See the hub for the other aspects (catalog UI, clone flow, channel gate, curation).

# Predefined campaigns — segment & tag handling

## Purpose

A predefined template references its trigger audience and its exit / conditional tags **by definition, not by ID** — because segment and tag IDs differ on every store. This page documents how the clone resolves the trigger segment (reuse an existing match or auto-create a new one) and how it auto-adds every tag the template references to the store's tag library. Both happen inside the single clone transaction ([[campaigns-predefined-clone-flow]]).

## Where to find it

These behaviours run server-side during the clone (`/admin/api/core/marketing/campaigns/create/automated/{id}`) — there is no separate screen. After the clone, the merchant sees the results on:

- [[marketing-segments]] — the resolved or newly-created trigger segment.
- [[marketing-subscribers]] — the auto-added tags in the store's tag library.

## What the merchant can do here

- **Rely on the trigger segment being wired automatically** — no need to pre-build the audience for a template.
- **Rename or refine the segment afterwards** in [[marketing-segments]] — the auto-created segment gets a machine-generated name the merchant will usually want to humanise.
- **Skip pre-creating tags** — every tag the template references is created for them on clone.

## Settings & fields

### Segment resolution

Predefined templates often reference an "ideal" segment by its **conditions**, not by ID. On clone the platform:

- If the template includes `data.segment.conditions`, it first searches the store for an EXISTING segment with the SAME conditions.
- **If found:** that segment is wired into the new campaign's `trigger_segment`.
- **If not found:** a NEW segment is created with the template's conditions and wired in.

### Segment auto-creation details

When no existing store segment matches, the new segment is created with `channel = 'cloudcart'`, the template's conditions, `processing = 1`, `active = 1`, and a name that is the condition manager's `toText` rendering — typically a humanised condition summary like *"Has products in cart"* rather than a marketing-friendly name. The audience-build job is queued via `set_subscribers_to_single_segment`; until it completes, the segment shows as **Processing** in [[marketing-segments]]. The merchant can rename or refine it later.

### Tag auto-add

Every tag the template references is auto-added to the store's customer-tag library on clone:

- The exit / membership tags in `customers_tags`.
- Every action's conditional tags — `tags_for_overdue_if` and `tags_for_overdue_else`.

If any of these name tags the store doesn't yet have, the clone inserts them so they exist. The merchant doesn't need to pre-create any tags in [[marketing-subscribers]] — they appear there after the clone.

## Business rules

### Both run inside the all-or-nothing transaction

Segment resolution / creation and tag auto-add both execute inside the single clone DB transaction. If either fails, the whole clone rolls back — no campaign, no segment, no tags — and the merchant can safely retry. See [[campaigns-predefined-clone-flow]] for the transaction boundary.

### Existing segment reuse avoids duplicates

Because the platform matches on condition tree first, cloning two templates that target the same audience reuses the one segment rather than creating duplicates — keeping [[marketing-segments]] clean.

### Tags are added, never removed

The clone only inserts missing tags; it never deletes or renames existing store tags. A tag the store already has is left untouched and simply reused.

## Related

- [[marketing-campaigns-from-predefined]] — hub.
- [[campaigns-predefined-clone-flow]] — the clone transaction that contains both behaviours.
- [[marketing-segments]] — where the resolved / auto-created trigger segment appears.
- [[marketing-subscribers]] — where the auto-added tags land in the tag library.

## Open questions

None.
