---
type: entity
nav_path: "Entity → Marketing Campaign → Attributes & Schema"
aliases: ["Campaign attributes", "Campaign schema", "Campaign columns", "Campaign status field", "Campaign active column", "Campaign progress column", "Campaign counters", "Атрибути на кампания"]
tags: [entity, marketing, campaigns, schema, attributes]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[campaign]]. See the hub for the other aspects (types, lifecycle, relationships, consent gating, attribution & statistics).

# Campaign — Attributes & Schema

## Identity

The Campaign record is the merchant-visible row that carries the campaign's identity, scheduling state, and aggregate counters. This page is the **column-level reference** — every attribute the merchant configures plus every underlying state / counter column that surfaces in list filters, the Statistics screen, or the editor sidebar.

The attributes split into three groups:

1. **Identity & configuration** — name, type, segment, schedule, channel actions.
2. **State columns** — `status` / `active` / `archived_at` / `banned_reason` / `progress` — the columns that drive the list-page tabs and progress filter.
3. **Aggregate counter columns** — `total_sent`, `successfully_sent`, `seen_message`, `opened_url`, etc. — written by an hourly aggregation job and read directly by the Statistics screen.

## Aliases

- **Attribute** / **field** / **column** — used interchangeably depending on whether the conversation is about the editor UI (attribute), the API representation (field), or the underlying record (column).
- **`active` column** — three-valued integer (0/1/2), NOT a boolean. Easy to confuse with **"Active" status tab** on the list page.
- **`progress` column** — campaign-level dispatch state. NOT the same as `subscriber_to_campaigns.progress` (the per-subscriber funnel state).

## Key Attributes

### Identity & configuration

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (`name`) | Required, max 191 chars | Internal label; not surfaced in the message itself. Used to find the campaign in the list. |
| **Type** (`type`) | `regular` / `automated` | Set at create time via the Create-campaign modal. Cannot be switched after creation. See [[campaign-entity-types-regular-automated]]. |
| **Segment** (`segment_id`) | Required — the target audience | Points to a [[segment|Subscriber Segment]] managed on [[marketing-segments]]. |
| **Channel actions** (`actions`) | One per channel + step | A campaign's "actions" are the actual messages. Regular: one action per channel; Automated: many actions across steps + channels. See [[campaign-entity-relationships]] for the relation. |
| **Schedule** | Immediate / Delayed / Triggered | Regular: immediate send OR scheduled future date / time. Automated: triggered by event, with per-step delays. See [[campaign-entity-types-regular-automated]]. |

### State columns

| Column | Values | Meaning |
|--------|--------|---------|
| **Status** (`status`) — list tab | `active` / `inactive` / `draft` / `archived` | The four status tabs on [[marketing-campaigns]]. **Note:** "Archived" tab is independent — it's the `archived_at` timestamp being non-null, not a status value. |
| **`active` column** (raw value) | `0` / `1` / `2` | Backed by integer column: `0 = Inactive`, `1 = Active`, `2 = Draft`. |
| **`archived_at`** | timestamp or NULL | Soft-archive timestamp. Distinct from `deleted_at` (true soft-delete). A campaign can be both Active AND Archived (rare — happens automatically when a Regular campaign auto-completes; the status stays Active even though `archived_at` is now set). |
| **`type`** column | `'regular'` / `'automated'` | Literal string stored directly in the DB. No enum check at the DB level, but the create flow only emits these two values. |
| **`trigger_condition`** | Free-form string | Auto-set to `'gets_in_segment'` on creating a Regular campaign (boot hook). For Automated, set by the merchant via the editor — `'gets_in_segment'`, `'place_order'`, `'cart_abandoned'`, `'inactivity'`. |
| **`progress`** column | `'waiting'` / `'waiting_delayed'` / `'delayed'` / `'executing'` / `'completed'` | The campaign's overall dispatch state. Distinct from per-subscriber progress on the `subscriber_to_campaigns` pivot. Used as a list filter. |
| **Banned reason** (`banned_reason`) | NULL or string | Populated when anti-spam moderation flags the campaign. The merchant cannot send while populated. See [[campaign-entity-consent-gating]]. |
| **Date created** / **Updated at** | timestamps | Sortable list columns. |

### Aggregate counter columns

These columns are written by an hourly aggregation job and read directly by the merchant-facing Statistics screen — **NOT recomputed at view time**. There is a delay of up to one hour between actual delivery / opens / clicks and the merchant seeing the updated counts.

| Column | What it counts |
|--------|----------------|
| `total_sent` | Total deliveries attempted across the campaign. |
| `successfully_sent` | Deliveries acknowledged by the channel provider. |
| `seen_message` | Opens (Email + Web Push). |
| `opened_url` | Clicks on links inside campaign messages. |
| `unsubscribed` | Recipients who clicked unsubscribe from this campaign. |
| `abuse` | Recipients who filed an abuse / spam complaint. |
| `bounced` | Hard-bounce count. |
| `reached` | Distinct recipients reached (deduplicated). |

See [[campaign-entity-attribution-statistics]] for how the hourly job populates these and the click-attribution chain that drives the order-revenue rollup.

## Where it appears

- [[marketing-campaigns]] — the master list page reads `status` / `active` / `archived_at` / `progress` / `type` for tab and filter rendering.
- [[marketing-campaigns-edit]] — the campaign editor screen reads / writes `name`, `segment_id`, `actions`, schedule fields, `status` (toggle), and channel-level message bodies.
- [[marketing-campaigns-statistics]] — reads the aggregate counter columns directly to display the per-campaign Statistics screen.
- [[campaign-entity-lifecycle]] — the state-machine page; this aspect is the column-level companion.

### `active` column vs "Active" status tab — the common confusion

The `active` column is an integer with three values (`0` = Inactive, `1` = Active, `2` = Draft). The **list-page tab labelled "Active"** filters to rows with `active = 1`. The **"Archived" tab** filters by `archived_at IS NOT NULL` — it is NOT a value in the `active` column. This means a campaign can show on the **"Archived"** tab while still having `active = 1` (and being shown as "Active status" in the row's status badge). See [[campaign-entity-lifecycle]] for when this dual state arises (Regular auto-archive).

### `progress` column vs `subscriber_to_campaigns.progress` (verified against backend)

There are TWO `progress` columns in the campaign ecosystem and they mean different things:

- **`campaigns.progress`** — the campaign-level dispatch state for the whole campaign (`waiting` / `executing` / `completed` etc.). Used as a list filter on [[marketing-campaigns]].
- **`subscriber_to_campaigns.progress`** — the per-subscriber funnel state on the pivot row (waiting / executing / completed / removed). One row per (subscriber, campaign, re-enrolment cycle). See [[campaign-entity-relationships]] for the pivot semantics.

The merchant-facing list-filter dropdown only shows the campaign-level values.

## Related

- [[campaign]] — hub.
- [[campaign-entity-types-regular-automated]] — `type` and `trigger_condition` semantics.
- [[campaign-entity-lifecycle]] — `status` / `active` / `archived_at` state transitions.
- [[campaign-entity-relationships]] — how `segment_id`, `actions`, and the subscriber pivot connect.
- [[campaign-entity-attribution-statistics]] — how the aggregate counter columns are populated.
- [[marketing-campaigns]] — the list page reading these columns for tabs / filters.
- [[marketing-campaigns-statistics]] — reads `total_sent`, `successfully_sent`, etc., directly.

## Open Questions

- ⏸️ The exact validation rules on `trigger_condition` for Automated campaigns — whether the platform restricts to an enum at write time or accepts any string the editor emits. `(verify)`
