---
type: feature
nav_path: "Marketing → Segments → List page"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segments list", "Segment table", "Segment list view"]
tags: [marketing, segments, list, polling]
plan_gates: ["segments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-segments]]. See the hub for related aspects (create popup, types, conditions, rebuild mechanics, etc.).

# Segments — list page

## Purpose

This aspect documents the **list view** itself — what each column shows, the per-row actions, the status/type icon, the polling / websocket refresh behaviour, and the Rename modal. The editor is on [[marketing-segments-editor]]; the create popup is on [[segments-create-popup]].

## Where to find it

Sidebar → **Marketing** → **Segments**. Route `/admin/marketing-new/segments`.

## What the merchant can do here

- Toggle a segment Active/Inactive via the **Active** switch.
- Click the **Subscribers** count to open [[marketing-segments-subscribers]].
- Click the **Campaigns** count to drop a list of campaign names that target this segment.
- Click the **Log** action to open [[marketing-segments-log]].
- Click **Generate CSV file** per row to export the segment's subscribers.
- Click the segment name to open [[marketing-segments-editor]].
- Click **Rename** to relabel the segment without opening the editor (see below).
- Delete a segment via the trash action (blocked if a campaign references it — see [[marketing-segments]] § Business rules).
- Filter, search, sort, paginate.

## Settings & fields

### Segment list columns

| Column | What it shows | Notes |
|--------|---------------|-------|
| Segment's name | The merchant-given name + type icon (One-time vs Automated). | Required at create time. |
| Subscribers | Count of subscribers currently attached to this segment. | Clickable — opens the subscriber list. |
| Campaigns | Count of campaigns using this segment as trigger. | Clickable — drops a list of campaign names. |
| Last generated at | When the rule was last evaluated (or "Not generated yet"). | Automated segments update on every qualifying event. |
| Generate CSV file | Per-row export action. | Generates a CSV of the current subscribers. |
| Active | On/Off switch. | Inactive segments aren't recalculated. |
| Log | Link to the segment's audit log. | Preserves the full added/removed history. |

### Per-row actions

Each segment row exposes two actions on the right edge:

- **Log** button (with a chart-bar icon and the label "Log") — routes to `/admin/marketing-new/segments/log/:id` (see [[marketing-segments-log]]). The Log query param is pre-populated with `page=1&perpage=25` so the URL is canonical from the start.
- **Delete** button — with the confirmation copy *"Delete row?"*. Clicking confirms and removes the segment. On success the row disappears (optimistic remove). On failure (typically because a campaign references the segment), the toast surfaces the server message *"You can't delete the segment because it is used in campaigns: :names"*.

There is **no inline Edit pencil button** on the segment row — clicking the **segment name** opens [[marketing-segments-editor]]. The row's status badge (icon left of the name) clicks through to nothing — it's a visual indicator only.

### Status / type indicator

The left-hand icon of each row tells the merchant the segment's state at a glance:

- **Spinning orange spinner** (`processing = true`) — the segment is currently re-evaluating; the list polls every 3 seconds while at least one row has `processing = true` (otherwise no polling — see "Re-evaluation polling" below).
- **Green pulsing blob** (Automated + active) — the segment is healthy and listening for events.
- **Greyed-out blob** (Automated + inactive) — the segment is disabled (either manually or by an inactive-error — see [[segments-inactive-errors]]).
- **Green check on light-green background** (One-time + active) — the segment is current.
- **Red warning triangle** (One-time + inactive) — the segment has an inactive error; hovering the row shows the `inactive_errors` joined into a tooltip.

The segment name itself is rendered as a click-to-edit link; the tooltip on the name shows either the type label ("Automated" / "One-time") or — when `active = false` — the full `inactive_errors` content prefixed with *"The segment is disabled due to the following error:"*.

### Rename modal

A dedicated small modal (separate from the conditions editor) relabels a segment:

- Title: *"Rename segment"*.
- Field: **Segment title** — text input, placeholder *"Enter segment title"*, pre-filled with the segment's current `title` (falling back to its auto-generated `name`).
- Save endpoint: `PUT /admin/api/core/marketing/segments/:id/rename` with `{title: 'new name'}`.
- Validation: empty trimmed title → inline error *"Enter segment name"* under the field.
- Toast on success: *"Segment renamed successfully."*; toast on error uses the parsed API error message.

Renaming updates the `title` column on the segment row; the conditions-derived `name` (auto-summary) remains the fallback when `title` is empty. This is the only way to give a segment a merchant-chosen label — the editor itself doesn't expose a name field.

## Business rules

### Re-evaluation polling

The segment list query polls the API **every 3 seconds** while at least one row has `processing = true` (i.e., a rebuild is in flight). Once all rows are `processing = false`, polling stops automatically. Polling does not run in the background tab (`refetchIntervalInBackground: false`).

In parallel, the page subscribes to **four broadcast events** over the cc-websocket pipeline: `SegmentPopulated`, `SegmentCreated`, `SegmentUpdated`, `SegmentDeleted`. When any of them fires, the list refetches (debounced 500ms). A 4-second suppression window prevents a manual save from triggering both the optimistic cache patch AND a duplicate websocket-driven refetch.

### Optimistic remove

Successful delete removes the row from the local list immediately, before the server confirms. On failure the row reappears and a toast surfaces the campaign-attachment error from [[marketing-segments]] § Business rules.

## Related

- [[marketing-segments]] — hub.
- [[marketing-segments-editor]] — opened by clicking the segment name.
- [[marketing-segments-subscribers]] — opened by clicking the Subscribers count.
- [[marketing-segments-log]] — opened by clicking the Log action.
- [[segments-create-popup]] — opened by clicking **Create segment** (sibling aspect).
- [[segments-inactive-errors]] — drives the red-triangle indicator and the greyed-blob state.
- [[segments-rebuild-mechanics]] — defines when `processing = true` flips back to `false` and which events trigger the websocket refetches.

## Open questions

None.
