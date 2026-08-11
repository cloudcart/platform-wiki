---
type: feature
nav_path: "Marketing → Segments → Subscribers → List & filters"
route_name: segments.core_new.subscribers
route_path: /admin/marketing-new/segments/:id/subscribers
aliases: ["Segment subscriber list", "Subscriber table in segment", "Filter subscribers in segment", "Sort segment subscribers", "Таблица с абонати в сегмент"]
tags: [marketing, segments, subscribers, list, filters]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-segments-subscribers]]. See the hub for the other aspects (add, remove, the detail/log modals, and the shared data source).

# Subscribers in segment — list, columns & filters

## Purpose

The subscriber table is the core of the **Subscribers in segment** page — the merchant's "who is currently in this segment, right now" view. It lists every subscriber attached to the segment (both **rule-matched** and **manually-added**), with filtering and sorting so the merchant can drill into the audience that a campaign would reach. The count of rows here = the segment's ground-truth audience size at this moment.

## Where to find it

The table fills the body of `/admin/marketing-new/segments/:id/subscribers`, reached by clicking the subscriber-count number on any segment row in the [[marketing-segments]] list. It paginates at **25 rows per page** by default.

## What the merchant can do here

- See **every subscriber** attached to this segment in a paginated table — rule-matched and manually-added appear identically (no visual distinction).
- **Filter** within the segment by:
  - **Allow marketing** (Yes / No)
  - **Tagged with** (any customer tag — multi-select)
  - **Country**
  - **Subscribed to** (channel: Email, Phone, WebPush — single-select)
  - **No channels (ghost)** (Yes / No — subscribers with no contact channel)
  - **Subscribed from** (signup source — Customer login, Import, Customer address creating, Customer address deleting, Customer creating, Order creating, Messenger, Contacts form, System)
- **Sort** by Name, Subscribed (created_at), Last active, Orders, Turnover, Segments count.
- **Bulk-select** rows via checkbox + the standard table actions inherited from the CloudCart table component.
- **Paginate** through the audience.

## What the merchant cannot do here

- **Cannot distinguish manual vs rule-matched** subscribers from the table — both appear identically. The distinction lives in the underlying data (`manual = 1` vs `manual = 0`) but is not surfaced as a column or filter. See [[segments-subscribers-add]] for what the flag means.
- **Cannot edit** a subscriber's profile inline — clicking the name opens a read-only modal (see [[segments-subscribers-modals]]). To edit, the merchant goes through [[marketing-subscribers]].
- **Cannot export** the list from this page — for an export, go back to [[marketing-segments]] and use the per-row "Generate CSV file" action.
- **Cannot edit the segment's conditions** here — for that, open the [[marketing-segments-editor|segment editor modal]] from the parent list.

## Settings & fields

### Table columns

| Column | What it shows | Sortable | Notes |
|--------|---------------|----------|-------|
| **Name** | Full name (first + last). Click to open the Subscriber details modal. | yes | Locked; always visible. |
| **Channels** | Pills for each accepted channel (Email / Phone / WebPush / Viber / Messenger), with per-channel verified / unsubscribed / bounced indicators. | no | |
| **Country** | The subscriber's country (resolved name). | no | |
| **Subscribed** | When the subscriber was first registered. | yes | Formatted via the store's date-time format. |
| **Last active** | Most-recent activity timestamp (pageview, event, etc.). | yes | |
| **Orders** | Lifetime order count. | yes | Falls back to 0 if no orders. |
| **Turnover** | Lifetime spend. | yes | Formatted with the store's currency. |
| **Segments** | How many segments this subscriber belongs to (total across the store, not just this one). | yes | Clickable on [[marketing-subscribers]]; informational here. |
| **Subscribed from** | The signup source. | no | |
| **Log** | Per-row "Log" button — opens the subscriber's marketing-change log in a modal (see [[segments-subscribers-modals]]). | no | |
| **(trash)** | Per-row remove button (see [[segments-subscribers-remove]]). | no | Confirms: *"Remove subscriber from segment?"* — only manual entries are actually detached. |

## Business rules

### Channels filter is single-select; "No channels" is a separate ghost filter

The **Subscribed to** filter accepts ONE channel at a time (Email / Phone / WebPush). The Messenger option is commented out in the modern UI — only Email, Phone, and WebPush are user-selectable. To find subscribers with NO channel at all, the merchant uses the dedicated **No channels (ghost)** filter (Yes / No) — subscribers tracked anonymously who never identified themselves on a contact channel.

### "Subscribed from" matches the segment's `from` condition vocabulary

The **Subscribed from** filter uses the same source vocabulary as the segment-builder's `subscriber.from` condition — Customer login, Import, Customer address creating, Customer address deleting, Customer creating, Order creating, Messenger (Facebook messenger), Contacts form, System. The labels match those in the [[marketing-segments-editor|segment editor]] for the same condition, so the merchant can drill into a segment by a specific signup source.

### Refresh on save — the list refetches after add/remove

After a successful add or remove, the table refetches; the merchant does not need to manually reload to see the new state. While the request is in flight, the table shows the inherited loading state.

## Related

- [[marketing-segments-subscribers]] — hub.
- [[marketing-segments]] — parent list; subscriber-count clicks drill into this page.
- [[marketing-segments-editor]] — where the conditions that determine WHO qualifies are built.
- [[marketing-subscribers]] — the global subscriber list this view is filtered from.
- [[marketing-subscribers-custom-fields]] — custom fields settable per subscriber and filterable from segment conditions.
- [[subscriber]] — entity page.
- [[segment]] — entity page.

## Open questions

No outstanding questions.
