---
type: feature
nav_path: "Marketing → Segments → Subscribers → Data source & gating"
route_name: segments.core_new.subscribers
route_path: /admin/marketing-new/segments/:id/subscribers
aliases: ["Segment subscriber data source", "Forced segment filter", "Segment subscribers plan limit", "Subscriber limit on segment", "Why is my segment audience capped", "Заключен филтър по сегмент"]
tags: [marketing, segments, subscribers, plan-gating, data-source]
plan_gates: ["segments", "subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-segments-subscribers]]. See the hub for the other aspects (list, add, remove, modals).

# Subscribers in segment — data source, plan limit & permissions

## Purpose

This aspect explains where the Subscribers-in-segment table gets its data, why it can only ever show one segment, and the two gates that govern whether it works at all: the `segments` plan feature and the `subscribers` plan limit. It answers merchant questions like *"why is my segment audience smaller than my total subscriber count?"* and support questions about why a staff user sees an empty list.

## Where to find it

The behaviours here are not buttons — they govern the page at `/admin/marketing-new/segments/:id/subscribers` as a whole. The plan-limit notice appears on the [[marketing-segments-editor|segment editor modal]]; the forced segment filter is applied on mount whenever the page loads.

## What the merchant can do here

- Bookmark the page URL and trust that it always shows only this one segment — the segment filter is re-applied on mount regardless of query string.
- Read the plan-limit notice (when at/above the subscriber limit) to understand why only the first `:limit` subscribers feed campaign sends.

## What the merchant cannot do here

- **Cannot clear the segment filter** to see the whole subscriber base from this page — clearing it either no-ops (URL preserved) or is re-applied on the next fetch.
- **Cannot raise the subscriber processing limit** here — that is a plan-level limit; upgrading the plan is the only path.
- **Cannot access the page without the right permission** — staff users lacking the segment permission get a 403 on the underlying API calls and see an empty list.

## Settings & fields

This aspect has no merchant-editable fields. The governing values are:

- **`segments`** plan feature — whether the page is reachable at all (inherited from [[marketing-segments]]).
- **`subscribers`** plan limit — the maximum number of subscribers eligible for segment-based campaign sends.
- The **`customers.customer_segments`** API permission (alongside the `marketing` permission group) — gates every API call the page makes.

## Business rules

### One segment per URL — the segment filter is forced

The page always applies `filters[segment][]=:id` to the subscribers list. On mount it checks the URL for `filters[segment][]` or `filters[segment]`; if present, it uses it, otherwise it injects the route's `:id` before the table fetches. The merchant therefore cannot accidentally clear the segment filter and see the whole subscriber base from this page.

### Same data source as [[marketing-subscribers]] — just filtered

The list endpoint here is the same one that powers [[marketing-subscribers]], with `filters[segment][]=:id` enforced. So all the behaviour merchants know from that page — sortable columns, channel pills, country resolution, the orders/turnover/segments numbers — works identically here. The only differences: the segment filter is locked on, and the toolbar exposes "Add subscribers" (see [[segments-subscribers-add]]) + the segment-scoped remove action (see [[segments-subscribers-remove]]).

### Plan-gating + subscriber-count limit

The page is reachable only if the merchant's plan includes the **`segments`** feature (inherited from [[marketing-segments]]). Separately, on stores at or above the **`subscribers`** plan limit, the merchant sees a plan-limit notice on the editor modal:

> *"You have reached your subscriber limit. At the moment, the system can process the first {limit} subscribers from your list, the rest are not processed and are not included in your segments. The total number of subscribers you have is {total}."*

The subscriber list itself still renders in full, but only the first `:limit` subscribers are eligible for segment-based campaign sends — see [[marketing-segments]] → "Plan-gated feature with subscriber-count limit". This is the usual cause of "my segment audience is smaller than my subscriber count" questions.

### Permission gate

The whole page is gated by the `customers.customer_segments` API permission (alongside the `marketing` group). Staff users without it see a 403 on the underlying API calls and an empty list in the UI.

## Related

- [[marketing-segments-subscribers]] — hub.
- [[marketing-segments]] — parent list; source of the `segments` plan gate and the subscriber-limit notice copy.
- [[marketing-subscribers]] — the global subscriber list this view shares its endpoint with.
- [[marketing-segments-editor]] — where the plan-limit notice surfaces.
- [[segments-subscribers-add]] — the add toolbar action this page exposes on top of the shared endpoint.
- [[segments-subscribers-remove]] — the segment-scoped remove action.
- [[marketing-campaigns]] — campaigns target segments; the processed-subscriber limit caps the audience.
- [[subscriber]] — entity page.
- [[segment]] — entity page.

## Open questions

No outstanding questions.
