---
type: feature
nav_path: "Marketing → Campaigns → Subscribers → Columns"
route_name: campaigns.subscribers
route_path: /admin/campaigns/subscribers/{campaign_id}
aliases: ["Campaign subscribers columns", "Campaign subscribers grid", "Progress badge", "Currently step column", "Times completed counter", "Channel pills"]
tags: [marketing, campaigns, subscribers, recipients]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Campaign subscribers — columns

> Part of [[marketing-campaigns-subscribers]]. See the hub for the other aspects (surfaces, progress model, enrolment model).

## Purpose

This page documents the **six columns** of the legacy Campaign-subscribers grid and exactly how each one renders — including the several places where the rendered cell shows less than the underlying data (binary Progress badge, step-NUMBER-only Step badge, icon-only Times-completed counter). A support agent reading "the merchant says the Progress column only shows two states" should land here.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click a campaign's **Subscribers (N)** button → legacy side-panel grid. (The modern Vue redirect uses the standard subscribers-list columns instead — see [[campaigns-subscribers-surfaces]].)

## What the merchant can do here

- Read each subscriber's name, channels, enrolment date, progress, times-completed, and last-seen step from the grid.
- Click a subscriber name to open their full [[marketing-subscribers|profile]].
- Paginate the list (no "show all" option).
- The list is **not** sortable from the UI — all column headers are locked.

## Settings & fields

### Columns

| Column key | Label | What it shows |
|------------|-------|---------------|
| `name` | Name | Subscriber's name (link to their profile) — built from `first_name` + `last_name`. |
| `channels_formatted` | Channels | Pills per subscriber-channel (Email / Phone / WebPush) with status (marketing on/off, verified, bounced, unsubscribed). |
| `created_at_formatted` | Added at | Date+time the subscriber was enrolled in the campaign. |
| `progress` | Progress | The enrolment's current progress state rendered as a tinted badge — **binary** in the UI (see below). |
| `times_completed` | (no label, icon) | How many times this subscriber has completed the campaign — counts cycles for repeating campaigns. |
| `currently_step` | Step | The step the subscriber was last seen on, rendered as a step-NUMBER badge (see below). |

If the campaign has zero enrolled subscribers, the page shows the empty state *"No records yet (Subscribers)"* with an illustration.

### Channels formatting per row

The `channels_formatted` column renders one pill per channel. Each channel pill shows the channel name (Email / Phone / WebPush), the channel identifier (email/phone shown in full, web-push subscription endpoint hash shortened), and status badges: `marketing on/off`, `verified`, `bounced`, `unsubscribed`. Subscribers without a channel for one of the campaign's action types appear without that channel pill — useful for diagnosing "why didn't they get my SMS?" (answer: they don't have a Phone channel).

### Currently step

The `currently_step` cell renders from the subscriber's most-recent action-log entry in this campaign. If there are no log entries yet, the cell is empty (the subscriber is enrolled but hasn't reached an executable step).

## Business rules

### Progress badge is binary — Completed vs Pending

Although the underlying enrolment `progress` field has multiple enum values (`waiting`, `executing`, `completed`, `removed`, etc. — see [[campaigns-subscribers-progress]]), the rendered badge in the **Progress** column is **binary**:

- `completed` → green badge labelled "Completed"
- Anything else (waiting, executing, removed, paused, …) → orange badge labelled "Pending"

So the merchant cannot visually distinguish a subscriber currently executing a step from one already removed — both show "Pending". The granular states are stored but not surfaced individually here; for the exact state, inspect [[marketing-campaigns-statistics-log|the per-send log]] for that subscriber's most recent action.

### Currently-step column shows only the step NUMBER, not the action name

The **Step** column doesn't render an action title like "Step 3 — Email: Welcome offer". It renders just the 1-based step number (the zero-based action order plus one) inside a tinted badge:

- Green badge if the most-recent log entry has `completed_at` set (the step finished for this subscriber).
- Orange badge if the most-recent log entry is still in progress (no completed timestamp).

For a 5-step campaign the merchant sees integers 1–5 colour-coded by completion state. To know what channel/message each number corresponds to, the merchant cross-references the campaign editor's step list in [[marketing-campaigns-edit]].

### "Times completed" column has no header label — icon-only

The **Times completed** column header is empty (no text label); only the cell shows the icon + count. Tooltip on hover: *"Successfully completed"*. The count is incremented each time the subscriber finishes the campaign through to the exit tag. For non-repeating campaigns it's 0 or 1; for repeating Automated campaigns (`repeat=true` in [[marketing-campaigns-edit]]) it accumulates with each re-enrolment cycle.

### Sort is locked — all columns are `data-sort="no"`

Every column header carries `data-sort="no"` — none are sortable. The merchant cannot reorder by enrolment date, progress, or any other column from the UI. The default order is enrolment-date descending (latest first); to find a specific subscriber, the merchant uses the sortable [[marketing-subscribers|full Subscribers list]] (the modern redirect — see [[campaigns-subscribers-surfaces]]).

### Default sort order is dictated by enrolment

With no explicit sort applied, the default order is by the enrolment record's internal ID descending, which approximates enrolment time descending (latest first).

### Always paginates — no "show all" option

The grid uses the platform's default page size (typically 20 or 25, configurable in admin settings). There's no merchant-facing toggle to show all subscribers on one page; even a 10-subscriber campaign shows the pagination control (just disabled).

### Each row builds six column renders

Each subscriber row renders six small column fragments (`name`, `created_at_formatted`, `progress`, `times_completed`, `currently_step`, `channels_formatted`). A 25-row page therefore renders 150+ fragments; the platform caches the channel registry once per page load so the channel pills resolve from that cache rather than re-loading the registry for every row.

### Currently-step lookup is a single bulk lookup

For the visible page (e.g. 25 subscribers), the platform makes ONE additional action-log lookup for all the subscribers on the page at once, then groups the results per subscriber. So even a 100-row page incurs one extra lookup, not 100 per-row lookups — the list stays fast on large campaigns.

## Related

- [[marketing-campaigns-subscribers]] — hub.
- [[campaigns-subscribers-surfaces]] — the legacy side-panel this grid lives in (and the modern column set).
- [[campaigns-subscribers-progress]] — the full `progress` enum behind the binary badge.
- [[marketing-campaigns-edit]] — campaign editor; maps step numbers to channels/messages.
- [[marketing-campaigns-statistics-log]] — per-send log; the exact per-step state behind the binary badge.
- [[marketing-subscribers]] — full subscriber CRM; clicking a name opens the profile.
- [[subscriber]] — Subscriber entity.

## Open questions

No outstanding questions.
