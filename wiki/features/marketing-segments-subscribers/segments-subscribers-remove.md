---
type: feature
nav_path: "Marketing → Segments → Subscribers → Remove subscribers"
route_name: segments.core_new.subscribers
route_path: /admin/marketing-new/segments/:id/subscribers
aliases: ["Remove subscriber from segment", "Detach subscriber from segment", "Why can't I remove this subscriber from the segment", "Премахване на абонат от сегмент"]
tags: [marketing, segments, subscribers, remove]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-segments-subscribers]]. See the hub for the other aspects (list, add, modals, shared data source).

# Subscribers in segment — removing subscribers

## Purpose

The **Remove** action detaches subscribers the merchant previously pinned in by hand. Its single most important rule — and the source of most "why won't this person leave my segment?" tickets — is that it acts **only on manually-added entries**. Rule-matched subscribers cannot be removed by hand; they leave the segment automatically when they stop satisfying its conditions.

## Where to find it

Two entry points on the Subscribers-in-segment page (`/admin/marketing-new/segments/:id/subscribers`):

- **Single-row trash icon** — confirms *"Remove subscriber from segment?"*.
- **Bulk select + Delete** — select rows via checkbox, then the bulk Delete action.

The parent [[marketing-segments]] list spells out the rule in its own confirmation copy: *"Are you sure you want to remove these subscribers from the segment? Only those that were manually added to it will be removed."*

## What the merchant can do here

- Remove a **single manually-added** subscriber via the row trash icon.
- **Bulk-remove** several manually-added subscribers via checkbox selection + Delete.
- See the list refetch automatically after a successful remove.

## What the merchant cannot do here

- **Cannot remove a rule-matched subscriber** — clicking the trash icon on a rule-matched row does not detach them. The deletion only affects entries flagged `manual = 1`; rule-matched rows (`manual = 0`) are skipped silently. Rule-matched subscribers leave only when they stop matching the segment's conditions (edit those via the [[marketing-segments-editor|segment editor]]).
- **Cannot tell from the table which rows are removable** — manual and rule-matched rows look identical (see [[segments-subscribers-list]]). A trash click on a rule-matched row is a silent no-op.

## Settings & fields

The Remove action has no form fields of its own — it operates on the current row or the bulk-selected set:

- Single-row: trash icon → confirmation dialog *"Remove subscriber from segment?"* → confirm.
- Bulk: checkbox selection → Delete → the operation runs against the selected subscriber ids.

After either path succeeds, the table refetches automatically.

## Business rules

### Remove only acts on `manual = 1` entries

The delete operation filters to rows where `manual = 1`. Consequences:

- A manually-added subscriber (added via [[segments-subscribers-add]]) is detached cleanly.
- A rule-matched subscriber (`manual = 0`) is **not** detached — even if the trash icon was clicked and the confirmation accepted, nothing changes for that row. This is by design: removing a rule-matched subscriber would be pointless because they would re-attach on the next segment evaluation.
- A subscriber who is BOTH a rule-match and manually added is governed by the controlling row. The manual flag is what the remove targets; if the rule still matches, they may remain via the rule-matched membership.

### Validation contract (shared with add)

The remove request enforces the same input shape as the add path:

- `ids: required|array`
- `ids.*: required|int|exists:subscribers,id`

A non-existent subscriber id triggers an HTTP 422 with a field-mapped validation error. There is no maximum array size on the bulk remove.

### Refresh on remove

The list refetches after a successful remove; the merchant does not need to reload. While the request is in flight the table shows the inherited loading state.

## Related

- [[marketing-segments-subscribers]] — hub.
- [[segments-subscribers-add]] — the inverse action; sets the `manual = 1` flag that Remove targets.
- [[marketing-segments]] — the manual vs rule-matched distinction and the confirmation copy on the parent list.
- [[marketing-segments-editor]] — edit the conditions to detach rule-matched subscribers.
- [[subscriber]] — entity page.
- [[segment]] — entity page.

## Open questions

No outstanding questions.
