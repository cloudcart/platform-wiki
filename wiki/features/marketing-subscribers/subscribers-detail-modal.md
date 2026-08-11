---
type: feature
nav_path: "Marketing → Subscribers → Detail modal"
route_name: subscribers.list
route_path: /admin/marketing-new/subscribers
aliases: ["Subscriber details", "Subscriber detail modal", "Subscriber view", "Subscriber details panel"]
tags: [marketing, subscribers, detail, modal]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (list view, bulk actions, channels, import, settings, lifecycle).

# Subscribers — detail modal

## Purpose

The per-subscriber side modal is the merchant's drill-down view: every fact CloudCart knows about a single subscriber, grouped into 7 lazy-loaded cards (channel performance, statistics, details + tags, active channels, UUIDs, segments, linked customers), plus the per-channel edit form that overrides flags or triggers the merge flow.

## Where to find it

Click any row's **Name** in the [[subscribers-list-view]] (the `viewRule` on the `full_name` column). The route updates with `?modal=view&id=N` so the open state survives browser refresh and the back button. Closing the modal strips the query params.

Adjacent server-side routes (used by the modal cards):

- `admin.subscribers.channels` — Channels tab data.
- `admin.subscribers.details.customers` — linked Customer accounts.
- `admin.subscribers.details.segments` — Segments the subscriber belongs to.
- `admin.subscribers.details.uuids` — tracking UUIDs.
- `admin.subscribers.details.statistic` — engagement totals.
- `admin.subscribers.details.channelStatistic` — per-channel breakdown.
- `admin.subscribers.log` — Activity log (per subscriber).
- `admin.subscribers.rfm.log` — global RFM recalculation history.

## What the merchant can do here

- See per-channel send performance (one box per registered channel — Email / SMS / Viber / WebPush).
- See aggregate engagement totals (sent / opened / clicked / converted).
- Edit tags on the subscriber (autocomplete, create-option, save-on-dirty).
- Browse active channels and click one to open the per-channel edit form.
- Remove a channel from the subscriber (per-row remove icon on the channels table).
- See identified devices (tracking-cookie UUIDs with browser / OS / device decoded).
- See which segments the subscriber currently belongs to.
- See linked customer accounts with order totals.

## Settings & fields

### Modal frame

- Component: `SubscribersDetailsModal`. Width: `size=xll` (modal-as-side-panel).
- Header: subscriber's `full_name` or *"Subscriber details"* fallback, plus a small RFM badge if the subscriber has an RFM bucket (Champ → "update" variant; Churned → "critical" variant; etc.).
- Body: `MarketingSubscriberDetails` — a stack of 7 cards loading 7 separate API queries in parallel. While any of the 7 queries is loading, the modal body shows a `CcLoader` placeholder.

### The 7 cards

| Card / section | API endpoint | What it shows |
|---|---|---|
| **Per-channel performance** | `subscribers/{id}/channel-statistic` | A row of channel performance boxes (one per registered channel — Email / SMS / Viber / WebPush) with `total_sent` + `successfully_sent` counts. Same component used on the [[marketing-campaigns-statistics\|campaign statistics page]]. |
| **Statistics row** | `subscribers/{id}/statistics` | Aggregate engagement counters (sent / opened / clicked / converted). |
| **Details + Tags** | `subscribers/{id}/details` | Two-column card: left side is a list of `{label}: {value}` rows (subscriber attributes, optionally clickable links); right side is a tag editor (`CcSelect` with `mode=tags`, `create-option=true`, API-autocomplete against `/admin/api/core/customers/tags`). Save / Cancel buttons appear when tags are dirty. |
| **Active channels** | `subscribers/{id}/channel` | Expandable card with a table of per-channel rows: Channel, Channel identifier, Verified, Accepts marketing, Bounced, Unsubscribed, plus a per-row remove icon. Clicking the channel name opens `MarketingChannelsLogChannelEditModal` (see below). |
| **UUIDs** | `subscribers/{id}/uuid` | List of tracking-cookie UUIDs (identified devices) with browser / OS / device decoded. |
| **Segments** | `subscribers/{id}/segments` | Segments the subscriber currently belongs to (one row per segment, clickable). |
| **Customers** | `subscribers/{id}/customers` | Linked [[customer|Customer]] accounts with order totals. |

### Detail-view tabs (server-side route equivalents)

The same data the cards load corresponds to the per-tab the platform code actions:

| Tab | Route | What it shows |
|-----|-------|----------------|
| Channels | `admin.subscribers.channels` | List of all per-channel subscription rows for this subscriber, with verified / bounced / unsubscribed / marketing flags. |
| Customers | `admin.subscribers.details.customers` | Linked customer accounts (a subscriber can map to multiple customers — typically via shared email). Shows order totals + income. |
| Segments | `admin.subscribers.details.segments` | Which segments this subscriber currently belongs to. |
| UUIDs | `admin.subscribers.details.uuids` | Tracking-cookie UUIDs (identified devices) attached to this subscriber. |
| Statistic | `admin.subscribers.details.statistic` | General engagement totals (sent / opened / clicked / converted). |
| Channel Statistic | `admin.subscribers.details.channelStatistic` | Per-channel breakdown of the same. |

### Per-channel edit side-modal — `MarketingChannelsLogChannelEditModal`

Opened from the Active channels table → click channel name. Lets the merchant override per-channel state:

- **Channel identifier** (email / phone / PSID — editable text input).
- **Verified** toggle.
- **Accepts marketing** toggle.
- **Bounced** toggle (admin override; usually flipped on by the system).
- **Unsubscribed** toggle.

When changing the identifier to one already in use by another subscriber, the platform offers the **merge** flow — see [[subscribers-channels]] for the full merge mechanics.

## Business rules

- **The modal URL state survives refresh.** `?modal=view&id=N` means the merchant can paste the URL to a colleague and they land on the same drawer-open state. Closing the modal cleans the query string.
- **All 7 cards fetch in parallel.** Slow cards do not block fast cards. The `CcLoader` overlay covers only the still-loading cards, not the modal as a whole.
- **The Channels card is the merchant's edit surface for per-channel flags.** Toggling `verified` / `marketing` / `bounced` / `unsubscribed` from here writes to that channel only (not to other channels on the same subscriber). For cross-channel marketing flips, use the bulk action — see [[subscribers-bulk-actions]].
- **Channels card → remove icon → deletes the channel row, NOT the subscriber.** A subscriber with all channels removed becomes a "ghost" (queryable via `no_channels = Yes` on the list filter). The subscriber row itself only disappears via explicit delete or GDPR erasure.
- **Tag edits in the Details card are NOT optimistic.** Save and Cancel buttons appear once the tag list is dirty; the merchant must explicitly Save. (Compare to the row-level inline marketing toggle, which IS optimistic — see [[subscribers-bulk-actions]].)
- **RFM badge in the header is informational only.** Clicking it does nothing — the bucket assignment is recomputed by the 12-hour background sweep; see [[subscribers-settings]].

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-list-view]] — the row that opens this modal.
- [[subscribers-channels]] — channel model + the merge flow triggered from the channel-edit form.
- [[subscribers-bulk-actions]] — bulk marketing / tag / delete on the list.
- [[subscribers-settings]] — RFM bucket source + cadence (drives the header badge).
- [[marketing-campaigns-statistics]] — shares the per-channel-performance component.
- [[customer]] — entity for the Customers card.
- [[marketing-segments]] — entity for the Segments card.

## Open questions

None.
