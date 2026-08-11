---
type: feature
nav_path: "Marketing → Segments → Subscribers → Add subscribers"
route_name: segments.core_new.subscribers
route_path: /admin/marketing-new/segments/:id/subscribers
aliases: ["Add subscribers to segment", "Manually pin subscriber to segment", "Manual segment entry", "Add subscribers panel", "Ръчно добавяне на абонат в сегмент"]
tags: [marketing, segments, subscribers, manual-add]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-segments-subscribers]]. See the hub for the other aspects (list, remove, modals, shared data source).

# Subscribers in segment — adding subscribers by hand

## Purpose

The **Add subscribers** action lets the merchant pin specific subscribers (e.g. three known VIPs) into a segment by hand, regardless of whether they match the segment's conditions. These manual additions are **sticky** — they stay in the segment even if they don't satisfy the rules. This answers the merchant's "let me add these people to this segment myself" need without rewriting the segment's conditions.

## Where to find it

The green **Add subscribers** button sits top-right on the Subscribers-in-segment page (`/admin/marketing-new/segments/:id/subscribers`). Clicking it opens a side popup (size `md`, title "Add subscribers to segment").

## What the merchant can do here

- Open the **Add subscribers** side panel and search the store's entire subscriber population by name or email.
- Pick **one or more** subscribers (multi-select tag-mode picker; type-ahead search runs on each keystroke).
- Click **Add selected (\<count\>)** to attach all picked subscribers in one go.
- Cancel — closes the panel and clears the selection.

## What the merchant cannot do here

- **Cannot add a subscriber who isn't already tracked by the store** — the picker only searches the existing subscriber population. There is no "create new subscriber" path from this panel.
- **Cannot "convert" a rule-matched subscriber to manual** — adding a subscriber who is already in the segment as a rule-match leaves the controlling row at `manual = 0` (see Business rules).
- **Cannot save with nothing selected** — the **Add selected (0)** button is disabled until at least one subscriber is picked.

## Settings & fields

### "Add subscribers" panel

- A single **Select subscribers** picker — tag-mode multi-select with type-ahead search against the store's subscriber population.
- Results render as `<full_name> (<email>)` — the same shape as the customer / subscriber autocomplete elsewhere in the admin.
- The save button has a **custom footer** that overrides the popup's default save: when a request is in flight, the icon swaps from a plus to a spinning spinner (`fa-spinner-third fa-spin`). The `:disabled` flag is bound both to "request in flight" and to the "no subscribers selected" check.
- On success: toast *"Subscribers added to segment successfully."* and the list refetches.
- On failure: toast *"Error adding subscribers to segment."* (or a server-provided message).
- Closing the popup automatically clears the selection — the next open starts empty.

## Business rules

### Add = `manual = 1`; manual additions are sticky

Subscribers added through the panel are written to the segment-subscriber pivot with `manual = 1` (see [[marketing-segments]]). This means they:

- Stay in the segment even if they stop matching the rules (manual additions are sticky — only the **Remove** action detaches them; see [[segments-subscribers-remove]]).
- Show up in the [[marketing-segments-log]] as an `added_to_segment` event with their own subscriber row.
- Count toward the segment's subscriber count on the parent list.

The add operation does **not** disturb rule-matched rows. Adding a subscriber who is already in the segment as a rule-match leaves the pivot row at `manual = 0` — adding does NOT convert them to manual. Practically: the rule-matched row stays as the controlling row, so if the subscriber later stops matching, they leave the segment despite the merchant's "add" click. No pre-existing membership is detached by an add.

### Add triggers a re-evaluation that touches OTHER segments too

When at least one subscriber is picked and saved, the platform queues the **same single-subscriber re-evaluation job** that runs when a real event (signup, order, etc.) fires — not a scoped "add to just this segment" operation. So the just-added subscriber is re-evaluated against **all** active automated segments. Side effects:

- The subscriber's segment-count chip on [[marketing-subscribers]] updates.
- Any other segments they newly qualify for also pick them up.
- A subscribers-added-to-segment event fires.

The job is **single-flighted** per (site, subscriber-set) — multiple rapid adds with the same ids are deduplicated by a hash of site + sorted subscriber ids.

### Validation contract

The add request enforces:

- `ids: required|array`
- `ids.*: required|int|exists:subscribers,id`

A non-existent subscriber id triggers an HTTP 422 with a field-mapped validation error. There is **no maximum array size**, so very large bulk adds are allowed — but each id is validated against the subscribers table (one query per id at validation time). Errors during attach return HTTP 400 with *"Unexpected error. Please try again later"*, logged under the *"Subscriber Segments"* group.

## Related

- [[marketing-segments-subscribers]] — hub.
- [[segments-subscribers-remove]] — the inverse action; only manual entries can be removed.
- [[marketing-segments]] — the manual vs rule-matched (`manual = 1` / `0`) pivot distinction.
- [[marketing-segments-log]] — where `added_to_segment` events are recorded.
- [[marketing-subscribers]] — where the subscriber's segment-count chip updates after an add.
- [[subscriber]] — entity page.
- [[segment]] — entity page.

## Open questions

No outstanding questions.
