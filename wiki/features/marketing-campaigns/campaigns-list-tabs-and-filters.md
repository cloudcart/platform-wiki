---
type: feature
nav_path: "Marketing → Campaigns → Tabs & filters"
route_name: campaigns-active
route_path: /admin/marketing-new/campaigns/active
aliases: ["Campaigns list tabs", "Campaigns channel filter", "Campaigns table columns", "Campaign status enum", "Campaign progress enum"]
tags: [marketing, campaigns, list, filters]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns]]. See the hub for the other aspects (create modal, AI assistant, row actions, types & actions, rules, execution internals).

# Campaigns — tabs, filters, and columns

## Purpose

This aspect catalogues the navigation surface of the Campaigns list page: the four status tabs, the cross-tab channel filter row, the table columns, the status enum, and the progress enum. Every other Campaigns surface (editor, modals, statistics) is launched from this list.

## Where to find it

Sidebar → **Marketing** → **Campaigns**. The base route `/admin/marketing-new/campaigns` redirects to `/admin/marketing-new/campaigns/active`.

## What the merchant can do here

- Switch status tabs (Active / Inactive / Archived / Draft).
- Filter by channel via the bottom tab row.
- Filter, search, and sort the table.
- Click any row to open the editor (`campaigns-edit/{type}/{id}`).

### Status tabs

| Tab | Route | Filter rule |
|-----|-------|-------------|
| **Active** | `campaigns-active` | `active = 1` and not archived |
| **Inactive** | `campaigns-inactive` | `active = 0` and not archived |
| **Archived** | `campaigns-archived` | `archived_at IS NOT NULL` |
| **Draft** | `campaigns-draft` | `active = 2` (draft sentinel) and not archived |

The Active / Inactive / Draft tabs all hide archived rows; the **Archived** tab is the only place to see them again (and to unarchive). The Draft tab does NOT compute order statistics (drafts have no orders).

### Channel filter row (cross-tab)

A horizontal tab row across the bottom of the table — controls the `filters[channel]` query param. The selection persists across status-tab switches.

| Key | Label |
|-----|-------|
| `all` | All — clears `filters[channel]` |
| `email` | Email |
| `sms` | SMS (matches both `sms_nth_message` and `sms_msghub_message` backend channels) |
| `viber` | Viber |
| `web_push` | Web push |

### Table filters (top of table)

- **Type** — Regular / Automated
- **Progress** — Waiting / Waiting Delayed / Delayed / Executing / Completed
- **Has subscribers** — Yes / No
- **Subscribers** — autocomplete
- **Segment** — autocomplete
- **Title search**
- **Sort** — by ID (default desc), title, or subscribers count

## Settings & fields

### Campaign list table columns

| Column key | Label | Notes |
|------------|-------|-------|
| `title` | Campaign title | Locked + fixed first column; click to open editor |
| `created_at` | Date added | |
| `goal` | Goal | The campaign's `trigger_condition` / purpose (e.g., "Makes an order") |
| `actions_count` | Steps | Number of campaign actions (steps) |
| `reached` | Reached subscribers | Successfully-sent unique subscribers; *"Statistical information is updated every hour."* tooltip |
| `orders` | Orders | Orders attributed to this campaign |
| `turnover` | Turnover | Revenue from attributed orders (money-formatted) |
| `subscribers_count` | Subscribers | Count of subscribers currently linked to the campaign |
| `statistics` | Logs | Link to the per-action logs |
| `status` | Status | Active/Inactive toggle — hidden on Archived tab |
| `actions` | Actions | Edit / Copy / Archive / Delete buttons |

### Status enum

| Status | Value | Meaning |
|--------|-------|---------|
| Inactive | `0` | Stopped — not delivering messages |
| Active | `1` | Running — accepting new subscribers + sending messages |
| Draft | `2` | Saved but never started; appears only on Draft tab |

### Progress enum

| Progress | Value | Meaning |
|----------|-------|---------|
| Waiting | `waiting` | Created, no `start_at` set, idle |
| Waiting delayed | `waiting_delayed` | Scheduled in the future (waiting for `start_at`) |
| Delayed | `delayed` | Past `start_at`, still rolling subscribers in |
| Executing | `executing` | Actively running message sends |
| Completed | `completed` | Regular campaign finished + auto-archived |

A Regular campaign auto-archives on completion (sets `progress = completed` AND `archived_at = now`). Automated campaigns can keep running indefinitely.

## Business rules

- **Channel filter is sticky cross-tab.** Switching from Active to Draft preserves `filters[channel]`. The merchant can scope to "all Email campaigns" and then move between status tabs.
- **Bulk actions show only on Archived.** The CcTable wrapper auto-renders a bulk-delete bar only when `routeName === 'campaigns-archived'`. Other tabs hide bulk actions entirely. See [[campaigns-list-row-actions]].
- **`reached` / `orders` / `turnover` lag by up to 60 minutes** — populated by the hourly campaign-statistics aggregation job (tooltip in-product). Live send counts update faster.
- **Banned reasons render in the title cell.** If an action's channel is missing or suspended, the list-row formatter writes a "Missing channel type: {name}" or the suspension reason into the title cell as a badge. See [[marketing-campaigns-banned-info]].

## Related

- [[marketing-campaigns]] — hub.
- [[campaigns-list-row-actions]] — the Status toggle + actions column behaviour.
- [[campaigns-list-execution-internals]] — what populates `reached` / `orders` / `turnover`.
- [[marketing-campaigns-banned-info]] — banned-reason badges in the title cell.
- [[marketing-campaigns-statistics-log]] — destination of the `statistics` (Logs) column link.

## Open questions

None.
