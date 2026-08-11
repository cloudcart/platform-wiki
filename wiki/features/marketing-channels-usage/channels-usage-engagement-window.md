---
type: feature
nav_path: "Marketing → Channels → Channels setup → Usage → Engagement window"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["30-day engagement window", "Clicks Opened window", "opened_url seen_message aggregation", "UTC day boundary", "Title date range", "format.date display", "Прозорец на ангажираност", "30 дни"]
tags: [marketing, channels, usage, engagement, clicks, opens, date-range]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-usage]]. See the hub for the other aspects (metric cards, counter model, plan limit, buy-credit flow, alerts).

# Channel usage — Engagement window

## Purpose

Two of the five Usage modal cards — **Clicks** and **Opened** — are scoped to a fixed **30-day window**. The other three cards (Limit, Remaining, Total sent) are cumulative / current-state. This page documents the engagement-window aggregation, why the modal-title date range can show a 1-day discrepancy from the underlying server window, and why transactional messages are excluded from the two engagement counters.

The window is the source of most *"why are my Clicks zero?"* support tickets — merchants expect a configurable date range, but the Usage modal is a snapshot tool, not a reporting tool.

## Where to find it

- The engagement counters render on Sidebar → **Marketing** → **Channels** → **Channels setup** → on any channel card → click **Usage** → **Clicks** and **Opened** cards.
- The modal title shows the **display** date range (locale-formatted) at the top.
- For richer time-bounded engagement reporting, the merchant must use the channel's **Logs** view (see [[marketing-channels-logs]]).

## What the merchant can do here

- **See clicks and opens** for campaign-action messages on this channel over the last 30 days.
- **Read the date range** in the modal title (e.g., `Email Usage - 23.04.2026 - 23.05.2026`) to confirm the window.
- **Use the Logs view** as a deeper engagement-investigation tool for messages outside the 30-day window.

## What the merchant cannot do here

- **Cannot change the engagement window** — there is no date picker, no calendar input, no preset shortcuts. The 30-day window is hard-coded on the server.
- **Cannot count transactional / system-message engagement** in these two cards — the aggregation explicitly filters to messages with a non-null `campaign_id`. Order-confirmation email opens do not appear in Opened.
- **Cannot see engagement before 30 days ago** from this modal — for older data, use Logs.
- **Cannot reconcile the title range and the data range to the day** — they round to the same calendar month but the underlying data window is computed in UTC; merchants in non-UTC timezones may see a 1-day discrepancy at midnight in their local time.

## Settings & fields

### Title date range (display only)

The modal title is built as: `{Channel title prefix} - {date_start} - {date_end}` where:

- `date_end` = today, locale-formatted via the store's `format.date` server setting.
- `date_start` = today − 1 month (calendar-month subtraction).

This is the **display** range — purely cosmetic. The underlying engagement data uses a different formula (see below).

### Underlying engagement window (data range)

The server-side aggregate that produces `opened_url` and `seen_message` uses:

| Bound | Computation |
|-------|-------------|
| `start` | now in UTC, minus 30 **days**, snapped to start-of-day in UTC. |
| `end` | now in UTC, snapped to end-of-day in UTC. |

This is **a fixed 30-day window** in UTC days, not the calendar-month window shown in the title. For most stores the two match within hours, but a merchant in a non-UTC timezone may see a 1-day discrepancy at midnight local time.

### Aggregation filters

The statistics-store aggregation matches on:

| Filter | Value |
|--------|-------|
| `site_id` | The merchant's store ID. |
| `channel` | The current channel mapping (e.g., `email`, `viber_message`). |
| `created_at` | Between `start` and `end` above. |
| `campaign_id` | `!= null` (excludes transactional / system messages). |

The aggregate sums the per-message statistic rows' `opened_url` and `seen_message` fields and returns the totals.

## Business rules

### Engagement counters use a fixed 30-day window

The `Clicks` (`opened_url`) and `Opened` (`seen_message`) counts come from an aggregate over the per-message statistics records filtered on the four criteria above. The window is **exactly 30 days, UTC, regardless of the modal title's calendar-month label**. Engagement events outside the window do not surface here.

### Only campaign-tied messages are counted

The `campaign_id != null` filter is the key business rule: transactional / system-message engagement is **excluded** from these two figures. Consequence:

- A store with active order-confirmation emails but no marketing campaigns sees Total sent grow while Clicks and Opened stay at 0.
- Migrating a system message to a campaign action makes its engagement start counting here.
- For transactional engagement, use the per-system-message logs under [[marketing-channels-system-messages]].

### Display range vs data range can disagree by a day

The title's calendar-month subtraction (`today − 1 month`) and the server's day-based subtraction (`today UTC − 30 days, start of day`) both round to "the last month" but differ in two ways:

- **Calendar vs fixed days** — March has 31 days, February 28. The title range can span 28–31 days; the data range is always 30.
- **Timezone** — title is client-locale, data is UTC-day. A merchant in UTC+3 viewing the modal at 01:00 local sees the title range starting one calendar day later than the data range.

For most cases the difference is invisible. When merchants ask *"why does my Clicks number not include yesterday?"*, the UTC end-of-day boundary is usually the answer.

### Open and click counts come from webhook callbacks, not send jobs

Per-message statistic rows have `opened_url` and `seen_message` fields that are **incremented by upstream provider webhooks** (Elastic Email open-pixel reads, Web Push interaction events, etc.) — **not** by the send job. So engagement counts can rise hours or days after Total sent moved. See [[channels-usage-counter-model]] for the send-time vs delivery-time split on `total_sent`.

### Open is `seen_message`, Clicks is `opened_url`

The naming is verbatim from the backend stat fields and surfaces unchanged in the API:

- **Opened** card → `seen_message` field → open events (email open-pixel reads, push interaction confirmations).
- **Clicks** card → `opened_url` field → link-click events tracked via the channel's redirect / tracking layer.

Both counters default to 0 when the API returns no events.

### Web Push counters depend on the device replying

Web Push `seen_message` and `opened_url` require the subscriber's browser to fire the engagement event back to the platform. Subscribers who silently ignore the push (no click, no dismissal interaction) produce no engagement events and do not increment these counters.

## Related

- [[marketing-channels-usage]] — hub.
- [[channels-usage-metrics]] — the Clicks and Opened cards.
- [[channels-usage-counter-model]] — Total sent counter side; explains why send and engagement counts can disagree in time.
- [[marketing-channels-logs]] — per-recipient drill-down for engagement outside the 30-day window.
- [[marketing-channels-system-messages]] — transactional traffic excluded from these two counters.
- [[marketing-campaigns]] — campaign-action messages are what these counters track.
- [[marketing-channels]] — channel-setup hub.

## Open questions

No outstanding questions.
