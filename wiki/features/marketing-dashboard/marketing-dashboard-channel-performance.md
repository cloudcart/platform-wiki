---
type: feature
nav_path: "Marketing → Dashboard → Channel performance"
route_name: marketing-dashboard
route_path: /admin/marketing-new/dashboard
aliases: ["Channel performance row", "Email Viber SMS Webpush stats", "Per-channel Sent Delivered Revenue", "Activate channel CTA", "Канали — производителност"]
tags: [marketing, dashboard, channels, email, sms, viber, webpush]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-dashboard]]. See the hub for the other aspects (welcome & steps, overview KPIs, quick-launch tiles, campaigns & products, RFM & discounts, data freshness).

# Dashboard — Channel performance

## Purpose

The **Channel performance row** is the four-card strip that breaks the marketing-results numbers down by channel: **Email / Viber / SMS / Web push**. Each card surfaces three numbers — **Sent / Delivered / Revenue** — so the merchant can spot at a glance which channels are pulling their weight and which are silent. Inactive channels show a "Not active" placeholder + an "Activate" CTA that routes the merchant to the Channels setup page. The row carries **its own** date-range picker so the merchant can compare a different window than the Overview row above it without affecting the rest of the dashboard.

## Where to find it

Sidebar → **Marketing** → **Marketing suite** — third row of the dashboard, directly below the Overview / Results row.

## What the merchant can do here

- **Read per-channel Sent / Delivered / Revenue** — one card per channel.
- **Activate an inactive channel** — when a channel's card reads "Not active", clicking **Activate** routes to the Channels page (see [[marketing-channels]]).
- **Pick a custom date range for the channel row** — a separate `MarketingDashboardRangePicker` instance in the row header.
- **Jump to the Channels page** — a "Go to channels" link in the row header.

## Settings & fields

### Channel performance card (per channel)

| Field | Source |
|-------|--------|
| `sent` | Channel send statistics totalled for the channel + range |
| `delivered` | Delivered count from the same statistics |
| `revenue` | Money-formatted revenue from campaign-attributed orders |
| `status` | `active` / inactive — if not active, shows "Activate" CTA |

The four supported channels:

| Card label | Internal channel ID | Backend mapping ID |
|------------|---------------------|--------------------|
| Email | `email` | `email` |
| Viber | `viber` | `viber_message` |
| SMS | `sms_nth_message` | `sms_msghub_message` |
| Web push | `web_push` | `web_push` |

The dashboard maps the short channel IDs to the backend mapping IDs because the campaign system stores them under the longer form (`sms_nth_message` ↔ `sms_msghub_message`, `viber` ↔ `viber_message`).

### Row layout

Each card is a 1/4-width tile on `md+` viewports, stacking to 2-up on `sm` and 1-up on mobile. The row carries its own range picker in the header — separate from the Overview row's picker — so the merchant can compare channels across a different window without changing the Overview's window.

## Business rules

### Channel row uses its OWN range picker

The channel-performance row's range picker is independent of the Overview row's range picker. A merchant can pin the Overview to "Last 7 days" while looking at channel performance over "Last 90 days" to see longer-term channel trends. This is intentional — channels and overview are usefully analysed at different windows.

### Range picker disables while ANY of the four queries is in flight

The channel row's range picker is disabled while any of the four per-channel queries is loading or fetching. This prevents the merchant from kicking off four parallel re-fetches before the first set returns. Once all four cards finish loading, the picker re-enables.

### "Channel performance" only counts merchant's campaigns

The per-channel Sent / Delivered / Revenue numbers count messages sent FROM the merchant's campaigns (regular + automated), **not** transactional emails like order confirmations, shipping notifications, or welcome emails. For transactional volume, the merchant looks at the per-channel logs from the Channels page or [[marketing-omnichannel-mails-list]].

### Inactive channels show "Activate" — no fake zero

An inactive channel doesn't show "0 / 0 / 0" — it shows a "Not active" placeholder + an "Activate" CTA routing to `campaigns-channels`. This prevents the merchant from interpreting a structurally-empty channel as a performance problem.

### Channel-performance numbers cached 10 minutes

The per-channel endpoints (`/channel-performance` and `/channel-performance/{channel}`) are cached **10 minutes** per (site, range) tuple. This sits between the 5-minute general-overview TTL and the 1-hour marketing-results TTL. A campaign that just went out won't reflect on this row for up to 10 minutes. See [[marketing-dashboard-data-freshness]] for the full cache table.

### Channel revenue is attributed, not raw

The Revenue number on a channel card is **campaign-attributed** revenue routed through that channel — the same join logic that drives Marketing sales on [[marketing-dashboard-overview-kpis]], filtered to messages sent via this channel. An order placed by a customer who received both an email AND an SMS for the same campaign attributes only to the channel whose message converted them (verify).

## How it works

The channel-performance row queries `GET /admin/api/core/marketing/channel-performance` (the aggregate) plus four per-channel endpoints — `/channel-performance/email`, `/channel-performance/viber`, `/channel-performance/sms_nth_message`, `/channel-performance/web_push` — so each card can refresh independently and inactive channels can be detected without making the aggregate call wait on a dead channel.

Per-channel stats come from the channel send statistics, combined with campaign, order, subscriber, and customer data at query time. The "Activate" CTA on inactive cards routes to the merchant-facing **Channels** page where the merchant configures the underlying messaging integration (SMTP / SMS gateway / Viber Business account / Web push keys).

## Recommended merchant use

- **Weekly channel review** — pick "Last 7 days" on the channel row, scan for any channel where Delivered < 95% of Sent (deliverability problem).
- **Channel ROI comparison** — pick a longer window (last 30 days) and compare Revenue across channels to decide where to focus campaign budget.
- **Activation troubleshooting** — when a channel reads "Not active" but the merchant believes it should be active, the **Activate** button takes them straight to the Channels page to inspect the integration settings.

## Related

- [[marketing-dashboard]] — hub.
- [[marketing-dashboard-overview-kpis]] — the aggregate Open / Click / Conversion / Marketing sales numbers without the channel split.
- [[marketing-dashboard-data-freshness]] — cache TTL + endpoint enumeration.
- [[marketing-channels]] — the Channels page; target of the "Activate" CTA and the "Go to channels" header link.
- [[marketing-omnichannel-mails-list]] — transactional email templates (NOT counted in this row).
- [[channel]] — Channel entity.
- [[notification-delivery]] — outbound message delivery internals (drives the underlying Sent / Delivered counters).

## Open questions

- Verify whether multi-channel converting customers attribute to first-touch or last-touch channel.
