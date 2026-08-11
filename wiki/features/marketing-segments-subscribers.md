---
type: feature
nav_path: "Marketing → Segments → Subscribers"
route_name: segments.core_new.subscribers
route_path: /admin/marketing-new/segments/:id/subscribers
aliases: ["Subscribers in segment", "Segment subscribers", "Who matches this segment", "Members of segment", "Абонати в сегмент", "Абонатите в сегмента"]
tags: [marketing, segments, subscribers, condition-builder]
plan_gates: ["segments"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Subscribers in segment

## Purpose

The **Subscribers in segment** page is the merchant's "who is currently in this segment, right now" view. It opens from the [[marketing-segments]] list when the merchant clicks the subscriber-count number in a segment row, and shows the full list of subscribers that match the segment's conditions — both the **rule-matched** ones (auto-attached because they satisfy every condition) and the **manually added** ones (subscribers the merchant pinned in by hand, regardless of whether they match the rules).

This is the page the merchant uses to answer:

- *"Who's going to receive my next campaign if I target this segment?"*
- *"Did subscriber X end up in this segment — and if not, why isn't my campaign reaching them?"*
- *"How many people qualify for this offer today?"*
- *"Let me add three specific VIPs to this segment by hand."*

Combined with the segment's **Last generated at** timestamp on the parent list, the count of rows here is the merchant's ground-truth audience size for the segment at any given moment. Combined with [[marketing-segments-log]], it answers both *what's in the segment now* and *how did it get there*.

This page is large enough that it is split into focused aspect pages. This hub gives the orientation; drill into the aspect that matches the question.

## Sub-pages (in this cluster)

- [[segments-subscribers-list]] — the paginated subscriber table: columns, the in-segment filters (allow-marketing, tags, country, channel, ghost, signup source), sorting, and what the merchant can / cannot do.
- [[segments-subscribers-add]] — the "Add subscribers" side panel; the `manual = 1` sticky flag; the validation contract; the re-evaluation job that touches OTHER segments too.
- [[segments-subscribers-remove]] — the remove action (single + bulk); why it only detaches manually-added entries and never rule-matched ones.
- [[segments-subscribers-modals]] — the read-only Subscriber details modal + the per-subscriber Subscriber logs modal.
- [[segments-subscribers-data-source]] — the forced one-segment filter, the shared subscribers endpoint, the `segments` plan gate, the `subscribers` processing limit, and the permission gate.

## Where to find it

From the [[marketing-segments]] list, click the subscriber-count number on any segment row. The breadcrumb reads "Marketing → Segments → \<segment name\>". The header reads "Subscribers" with the description "Subscribers in segment: \<segment name\>". The segment name is truncated to 50 characters in the breadcrumb if longer.

The URL is `/admin/marketing-new/segments/:id/subscribers` and carries `filters[segment][]=:id` as a forced filter so the table only ever shows subscribers attached to this one segment (see [[segments-subscribers-data-source]]). The merchant can also bookmark the URL — the segment filter is applied on mount regardless of query string.

## What the merchant can do here

- See **every subscriber** attached to this segment in a paginated table — both rule-matched and manually-added (see [[segments-subscribers-list]]).
- **Filter and sort** within the segment (see [[segments-subscribers-list]]).
- **Add subscribers** to the segment by hand (see [[segments-subscribers-add]]).
- **Remove** manually-added subscribers (see [[segments-subscribers-remove]]).
- **Open the read-only detail / log modals** for any subscriber (see [[segments-subscribers-modals]]).

## Settings & fields

The page's columns, filters, the Add panel, and the two modals are documented on their aspect pages:

- Table columns + filters → [[segments-subscribers-list]].
- "Add subscribers" panel → [[segments-subscribers-add]].
- Subscriber details + logs modals → [[segments-subscribers-modals]].

## Business rules

The detailed rules live on the aspect pages; the load-bearing ones to know up front:

- **Add writes `manual = 1`; manual entries are sticky.** Manually-added subscribers stay even if they stop matching the rules. See [[segments-subscribers-add]].
- **Remove only detaches manual entries.** Rule-matched subscribers (`manual = 0`) cannot be removed by hand — they leave automatically when they stop satisfying conditions. See [[segments-subscribers-remove]].
- **One segment per URL — the filter is forced.** The merchant cannot clear it to see the whole base from this page. See [[segments-subscribers-data-source]].
- **Same data source as [[marketing-subscribers]], just filtered.** Plus a `segments` plan gate and a `subscribers` processing limit. See [[segments-subscribers-data-source]].

## Related

- [[marketing-segments]] — parent list; subscriber-count clicks here drill into this page.
- [[marketing-segments-editor]] — sibling; where the merchant builds the conditions that determine WHO qualifies for the segment displayed here.
- [[marketing-segments-log]] — sibling; the audit trail of add/remove events for this segment over time.
- [[marketing-subscribers]] — the global subscriber list this page is filtered from; clicking a name opens that page's detail modal.
- [[marketing-subscribers-custom-fields]] — custom fields that are settable per subscriber and filterable from segment conditions.
- [[marketing-campaigns]] — campaigns target segments; the count on this page = the campaign's audience size.
- [[subscriber]] — entity page.
- [[segment]] — entity page.
- [[subscriber-vs-customer]] — concept; the list mixes subscribers and customer-linked subscribers.

## Open questions

No outstanding questions.
