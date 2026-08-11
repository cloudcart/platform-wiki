---
type: feature
nav_path: "Marketing → Subscribers → List view"
route_name: subscribers.list
route_path: /admin/marketing-new/subscribers
aliases: ["Subscribers list", "Subscribers table", "Subscribers filters", "Subscribers header"]
tags: [marketing, subscribers, list, filters]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (bulk actions, detail modal, channels, import, settings, lifecycle).

# Subscribers — list view

## Purpose

The list view is the merchant's primary surface for browsing the audience pool. It shows one row per subscriber (across all channels merged onto that subscriber), exposes 9 filter slots above the table, and exposes a 4-control header strip that launches the import wizard, the settings modal, and the limits modal.

## Where to find it

Sidebar → **Marketing** → **Subscribers**. Route `/admin/marketing-new/subscribers`.

## What the merchant can do here

- Browse every subscriber row, sorted by most recent first (default).
- Filter the population down to a target slice (9 filters — see below).
- Search by name, email, country, or channel identifier.
- Click any row's **Name** to open the per-subscriber detail modal (see [[subscribers-detail-modal]]).
- Use the 4 header controls to import CSV, open settings, view plan limits, or read the page header.
- Use per-row actions (Log, Delete, Accepts-marketing toggle) — see [[subscribers-bulk-actions]].

### Page header — 4 controls

The header strip at the top of the page:

| Button / control | Icon | Opens | Purpose |
|---|---|---|---|
| **Import subscribers** | `fa-file-arrow-up` (light) | 2FA challenge → CSV-import wizard | Bulk-load subscribers from CSV. The 2FA gate uses `Cc2FaAction` with action `EXPORT_IMPORT_ACTION_IMPORT_SUBSCRIBERS` — the merchant must satisfy 2FA verification before the wizard opens. Once satisfied, the wizard receives a `hash` and proceeds. See [[subscribers-import]] for the wizard. |
| **Settings** | `fa-gear` | `SubscribersSettingsModal` | Edit cross-store subscriber settings — see [[subscribers-settings]]. |
| **Limits** | `fa-container-storage` | `SubscribersLimitsModal` | View plan-feature limits + "Upgrade" CTAs per feature. Title also shows `Limits · {used} / {limit}`. See [[subscribers-settings]] for the modal contents. |
| (header itself) | — | — | Title *"Subscribers"* + description *"Subscribers Description"*. |

## Settings & fields

### Subscriber list columns

| Column | Source field | Notes |
|--------|--------------|-------|
| Name | `full_name` (first_name + last_name) or channel identifier fallback | Clickable — opens detail modal via `viewRule` on the column. |
| Email / Identifier | Default channel's `channel_identifier` | A small green check icon marks the subscriber's "current communication channel". |
| Country | `country` (ISO-2 → name) | Detected via MaxMind at signup or set explicitly. |
| Channels | List of channels the subscriber accepts | "Emails", "Phone", "Messenger", "Web Push" (per-channel rows). |
| Accept marketing | `marketing` boolean | Per-row toggle; mandatory for sending campaigns. See [[subscribers-bulk-actions]]. |
| Verified | Email `verified` flag | Unverified emails are excluded from most campaign sends unless the email channel has `unconfirmed_send` enabled. |
| Subscribed by | One of the source constants | "Customer login", "Popup and Form builder", "Import", "From system", "API", … — see [[subscribers-lifecycle]]. |
| Tags | Custom tags assigned to subscriber | Merchant-managed taxonomy used in segments and reports. |
| Subscribed on | `created_at` | The moment the subscriber row was first created. |
| Last active on | `last_active_at` | Updated on every storefront interaction; underpins the `last_active` segment condition. |
| Identified on | `identified_at` on the subscriber-channel | When the channel was first matched to a real identifier. |

### Filters bar — 9 filter options

Above the table is the filter bar with these options (each opens a dropdown / search input as appropriate):

| Filter key | Label | Type / source |
|---|---|---|
| `marketing` | Allow marketing | Yes / No |
| `tagged` | Tagged with | Multi-select against `/admin/api/core/customers/tags` |
| `segment` | Segment | Search-select against `/admin/api/core/marketing/segments/search` |
| `campaign` | Campaign | Search-select against `/admin/api/core/marketing/campaigns/search` |
| `country` | Country | Country picker |
| `channel` | Subscribed to | Pick one of: Email / Messenger / Phone / WebPush |
| `channel_only` | Subscribed only for | Pick one of: Email / Messenger / Phone / WebPush — narrower than `channel` (subscriber must NOT have any other channel) |
| `no_channels` | No channels (ghost) | Yes / No — finds "ghost" subscribers with zero channel rows |
| `subscribed_from` | Subscribed from | Pick one of the source constants (Customer login / Import / Order creating / Messenger / etc.) |

`channel_only` is the under-used filter that catches single-channel subscribers — useful when auditing why Email-only contacts don't appear in a Phone campaign's reach.

## Business rules

- **Admin list does NOT apply the plan-cap `max_id` filter.** A merchant whose plan caps at 1,200 subscribers still sees every row in the admin list (including the inactive 1,201st+). Only segment counts and campaign reach apply the cap. See [[subscribers-lifecycle]].
- **The default channel column displays one identifier per row.** When a subscriber has multiple channels (Email + Phone), the column shows the channel marked as the primary communication channel (small green-check icon).
- **Sort order — most-recently-created first.** No merchant-visible toggle to flip this.
- **Filter combinations are ANDed.** Picking `channel = Email` + `country = BG` returns Email subscribers in Bulgaria, not Email-OR-BG.
- **Ghost subscribers (`no_channels = Yes`)** — these are rows with zero `SubscriberChannel` joins, usually created by uuid-only tracking before any identifier was captured. They cannot receive any campaign send. The filter exists primarily to let the merchant prune them.

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-detail-modal]] — the modal opened by clicking a row's name.
- [[subscribers-bulk-actions]] — bulk-action bar + per-row actions.
- [[subscribers-import]] — the CSV-import wizard launched from the header.
- [[subscribers-settings]] — the settings + limits modals launched from the header.
- [[subscribers-lifecycle]] — source taxonomy that drives the "Subscribed by" filter.

## Open questions

None.
