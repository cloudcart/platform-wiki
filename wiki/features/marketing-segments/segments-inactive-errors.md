---
type: feature
nav_path: "Marketing → Segments → Inactive errors"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Inactive segment", "Segment auto-disabled", "inactive_errors", "Segment disabled due to error"]
tags: [marketing, segments, errors, notifications]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-segments]]. See the hub for related aspects (list page, conditions, rebuild mechanics).

# Segments — inactive errors

## Purpose

This aspect documents the **auto-disable flow**: a segment can self-disable mid-rebuild if it references something that no longer exists or works (deleted customer custom field, uninstalled app's condition). This page covers the trigger conditions, the `inactive_errors` field, the merchant-facing banners, and the notification path.

## Where to find it

Surfaced on [[segments-list-page]] (red triangle / greyed-out blob icon, plus tooltip) and in the admin marketing-app notifications sidebar.

## What the merchant can do here

- Hover the row on [[segments-list-page]] to see the joined `inactive_errors` content in a tooltip.
- Read the full error in the banner shown when opening [[marketing-segments-editor]] on a disabled segment.
- Re-enable the segment by toggling **Active** — but if the underlying cause is not fixed, the segment will re-disable on the next rebuild.
- Fix the underlying cause (e.g., restore the deleted custom field, reinstall the app), then re-enable — the segment now stays active.

## Settings & fields

### `inactive_errors` (populated mid-rebuild)

A list of human-readable error messages. Surfaced verbatim in three places:

- **Tooltip on the list row** ([[segments-list-page]]): the joined messages, prefixed with *"The segment is disabled due to the following error:"*.
- **Banner in the editor** ([[marketing-segments-editor]]): the full list, rendered.
- **Marketing-app notification** in the admin sidebar (see Business rules below).

### Banner copy (singular vs plural)

- Singular error: *"The segment is disabled due to the following error: :errors"*.
- Plural errors: *"The segment has been disabled due to the following errors: :errors"*.

## Business rules

### What triggers auto-disable

When the segment evaluator runs, it ALSO checks whether the segment is disabled by any of its conditions. If the result is non-empty, the segment is **auto-disabled mid-rebuild**:

- `active` flips to `0`.
- `inactive_errors` is populated with the formatted messages.
- `last_execute` updates to the timestamp of the failed rebuild.
- A `SegmentPopulated` event fires.

Common causes:

- A referenced customer custom field was deleted from [[customers-custom-fields]] (verify).
- A condition contributed by an installed app is no longer available because the app was uninstalled (e.g., the `apps.others.product_review.subscriber_segments.*` family from [[apps-product-review]]).
- An allowed-combinations rule that previously held has been broken (e.g., a condition that `subscriber.missing_product` was paired with was removed — see [[segments-conditions]]).

The merchant then sees the segment greyed out with the banner on next page load. This means a segment can self-disable **between two scheduled rebuilds without any merchant action**.

### Notification path

The model's `updating` boot hook detects an `active: 1 → 0` flip while `inactive_errors` is populated and dispatches a campaign-channel-apps notification (`notify('subscriber_segments_apps', …)`) with the formatted error messages. This surfaces as a marketing-app notification in the admin sidebar — the merchant gets a passive notice that one of their segments stopped working.

### Re-enabling without fixing the cause

Toggling **Active** back on while the underlying cause is still broken results in the segment being **re-disabled on the next rebuild**. The merchant must fix the dependency (restore the field, reinstall the app, adjust the conditions) first.

### Saving a disabled segment

Saving the editor with `active = false` while `inactive_errors` is populated re-triggers the campaign-channel-apps notifier. This is the case where the merchant has acknowledged the error but not yet fixed it.

### Mid-rebuild auto-disable applies to both types

Both [[segments-types|One-time and Automated]] segments can self-disable mid-rebuild — the check runs on every rebuild path (5-minute sweep, on-save single-segment rebuild, per-event incremental job).

## Related

- [[marketing-segments]] — hub.
- [[segments-list-page]] — shows the red-triangle / greyed-blob indicator.
- [[marketing-segments-editor]] — shows the full banner.
- [[segments-conditions]] — the source of conditions whose dependencies can break.
- [[segments-rebuild-mechanics]] — defines when the check runs and which event fires.
- [[customers-custom-fields]] — deleting a referenced custom field is a common trigger (verify).
- [[apps-product-review]] — uninstalling triggers auto-disable on segments using its conditions.

## Open questions

- 📡 **Custom-field deletion behaviour.** Whether deleting a customer custom field referenced by a segment auto-disables the segment immediately or only on the next rebuild (verify).
