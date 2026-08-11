---
type: feature
nav_path: "Marketing → Segments → Log → Table & navigation"
route_name: segments.core_new.log
route_path: /admin/marketing-new/segments/log/:id
aliases: ["Segment log table", "Segment log columns", "Segment log pagination", "Segment log subscriber modal", "Таблица на сегмент лог"]
tags: [marketing, segments, log, audit, ui]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
> Part of [[marketing-segments-log]]. See the hub for the other aspects (the action vocabulary, the storage model, and batch rows).

# Segment log — table, columns & navigation

## Purpose

This is the screen the merchant actually looks at: the paginated table that lists the Segment log entries, plus the read-only navigation around it. It lets the merchant scan "who came in / who went out" newest-first, click into any subscriber, and bookmark / share a specific subscriber view — all without being able to mutate the log.

## Where to find it

The table fills the body of `/admin/marketing-new/segments/log/:id`, reached by clicking the **Log** link on a segment row in the [[marketing-segments]] list. The header shows the segment name (truncated to 50 characters) and a chart-bar icon.

## What the merchant can do here

- **See every log entry** for this segment in a paginated table — default sort is **created_at desc** (newest first).
- **Click a row's subscriber name** (or the action label) to open the **Subscriber details modal** — the same modal used on the [[marketing-subscribers]] list. The modal opens via a URL query (`?modal=view&id=:subscriber_id`) so it survives refreshes and back/forward navigation.
- **Sort by date** ascending or descending (the Date column is the only sortable column).
- **Paginate** with 25 rows per page (default `perpage=25` is forced into the URL on first render).
- **Refresh the table** by reloading the page — server cache is 30 seconds.

The merchant **cannot**:

- Filter the log by action type, channel, or date range — there are no filters on this page (the table renders with `:filters="false"`).
- Export the log to CSV — no export action is available here. For subscriber-list export, see [[marketing-segments]] → "Generate CSV file".
- Delete individual log entries — log rows are immutable (see [[segments-log-storage-model]]).
- Edit the segment from here — the merchant must navigate back to [[marketing-segments]] to edit.

## Settings & fields

### Log columns

| Column | What it shows |
|--------|---------------|
| **Action** | The event type as an icon + a translated label. Clicking the action label opens the subscriber modal. The full icon / label set is on [[segments-log-actions]]. |
| **Subscriber** | The subscriber's full name (first + last). Clickable — opens the subscriber details modal at `?modal=view&id=<id>`. If no name, shows "—". |
| **Info** | Free-form HTML info for the row — typically the channel + channel identifier (e.g., `Emails: john@example.com`, `Phone: +359...`). For RFM and marketing rows it carries the group-change or consent string. The channel-label map and per-action detail strings are on [[segments-log-actions]]. |
| **Date** | The event timestamp formatted via the store's date-time format. Default sort is descending. |

For `head` (batch-header) rows the Subscriber cell renders as the dash — see [[segments-log-batch-rows]].

## Business rules

### Page-mount URL normalisation

On mount, the page ensures `page=1` and `perpage=25` are in the URL — if not, it replaces the route with those query defaults. This keeps the URL canonical for sharing / bookmarking and avoids unbounded result fetches.

### Modal query-string handshake

Opening a subscriber modal pushes `?modal=view&id=<subscriber_id>` into the URL. Closing the modal removes those two params (other query params like `page` / `perpage` are preserved). This makes the modal state shareable and survives back/forward navigation. The modal-related query params are **filtered out** of the table-data fetch, so opening / closing the modal does not refetch the list.

When the URL is opened with `?modal=view&id=:id` already present (e.g., a shared link from a colleague), the page automatically:

1. Reads the `id` query param and converts it to a number.
2. Looks up the matching row in the currently loaded log data (`data.value.data.find(r => r.subscriber_id === id)`).
3. Captures `full_name` from that row (if found, otherwise `null`).
4. Opens the `SubscribersDetailsModal` with `{subscriber_id, full_name}`.

The modal itself is `SubscribersDetailsModal` (NOT the `MarketingSubscriberDetails` component used on [[marketing-segments-subscribers]]) — it includes RFM-status display via a `subscriber-rfm-status` prop. The modal's own log tab reads the same audit history filtered by `subscriber_id` (see [[segments-log-storage-model]]).

### Cache — 30-second `staleTime`

Log fetches are cached for **30 seconds** (`staleTime: 30 * 1000`). The page **does not** refetch on mount or window focus — to see new entries, the merchant reloads the page (or waits 30 seconds + interacts with pagination / sort to re-trigger the query). Because the log is written asynchronously, a freshly-rebuilt segment may show its "Last generated at" timestamp on the parent list slightly before the matching log row appears here — see [[segments-log-batch-rows]].

## Related

- [[marketing-segments-log]] — hub.
- [[marketing-segments]] — the parent list; the **Log** column links here.
- [[marketing-subscribers]] — the subscriber whose detail modal opens from a row.
- [[marketing-segments-subscribers]] — uses a different detail component than this page's modal.

## Open questions

No outstanding questions.
