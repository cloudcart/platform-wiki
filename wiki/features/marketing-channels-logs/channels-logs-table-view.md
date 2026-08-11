---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → Table view"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel logs table", "Channel logs columns", "Channel logs filters", "Channel logs search", "Channel logs pagination", "Channel logs date filter"]
tags: [marketing, channels, logs, table, filters, search]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (status vocabulary, message preview, subscriber drill-down, row lifecycle, system vs campaign).

# Channel logs — table view

## Purpose

The outer Logs modal is a paginated `CcTable` of every outbound message attempt the platform made through the selected channel. This aspect documents the columns shown, the filter controls, the search semantics, the date-filter behaviour, and the pagination rules.

The body binds to a query whose filter state lives in **URL params** (via `useQueryParams`) — so log filters persist on the URL and survive page refresh. Every query change re-fetches.

Modal size: `xll` by default; expands to full-screen (`100`) while the [[channels-logs-subscriber-drilldown|Subscriber details]] sub-modal is open. Cancel button: *"Close"*. No Save button (read-only view).

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → click the channel card's **Logs** button.

## What the merchant can do here

- **Browse all delivery attempts** — one row per (subscriber, send attempt).
- **Filter** via the standard CcTable filter framework (`:filters="true"`).
- **Sort** by date (default: newest first); none of the columns are sortable beyond date.
- **Paginate** — 25 rows per page by default; the merchant can jump pages and change the per-page count via the standard CcTable pagination controls.
- **Drill down** — clicking the channel icon opens [[channels-logs-message-preview|Message Preview]]; clicking the subscriber name opens [[channels-logs-subscriber-drilldown|Subscriber details]].

## What the merchant cannot do

- **No Export button on the Logs modal.** Heavy-volume merchants who need exports request them through CloudCart support.
- **No sortable column other than date** — Subscriber / Campaign / Segment columns are not sortable.

## Settings & fields

### Columns shown in the logs table

Left-to-right:

| Column | What it shows |
|--------|---------------|
| **Channel** | Channel-icon cell. Tooltip *"Preview message"*. Clicking the icon opens [[channels-logs-message-preview]] with that row's data. |
| **Subscriber** | Full name (first + last) of the recipient. *"N/A"* if no subscriber linked. *"Deleted Subscriber (ID: ...)"* if the subscriber was deleted after the send — see [[channels-logs-subscriber-drilldown]]. Click handler opens *Subscriber details* (disabled for deleted / missing). |
| **Destination** | The channel identifier — email address (Email), phone in E.164 (SMS / Viber), push endpoint URL or browser fingerprint (Web Push). Shows the *"Subscriber does not accept marketing"* warning below the identifier when `accept_marketing = 0`. |
| **Segment** | Name of the segment the recipient was matched on when the send was triggered (empty for sends not tied to a segment). Compact text styling. |
| **Campaign** | Name of the campaign that triggered the send (empty for system-message sends — those have only a system-message label, see [[channels-logs-system-vs-campaign]]). |
| **Status** | Coloured status pill — see [[channels-logs-status-vocabulary]] for the full vocabulary + colour mapping. |
| **Type** | *"Campaign action"* (linked to a campaign) or *"System message"* (transactional, event-triggered) — see [[channels-logs-system-vs-campaign]]. |
| **Date** | Row's last-updated timestamp (typically the most recent status change, not the original send time). Default sort: newest first. Rendered with the store's date format. |

### Filter controls

Available via the table's filter dropdown:

| Filter | Type | Notes |
|--------|------|-------|
| Search query | Free text | Matches against campaign name, segment name, channel identifier (recipient destination), subscriber first name, subscriber last name. |
| Status | Dropdown | Pick any one canonical status — see [[channels-logs-status-vocabulary]]. Filtering by `BOUNCED` automatically includes `HARD_BOUNCED` rows. |
| Type | Dropdown + value | Two-step: pick *Campaign message* or *System message*. When System, a second dropdown lets the merchant pick the specific system-message template — see [[channels-logs-system-vs-campaign]]. |
| Segment | Free text / autocomplete | Limited to segment names that have at least one log row on this channel. |
| Campaign | Free text / autocomplete | Limited to campaign names that have at least one log row on this channel. |
| Date | Operator + date | Operators: *exactly* (date = day), *before* (older than), *after* (newer than). Date format follows the store's preferred date format. |

## Business rules

### Free-text search semantics

The query splits on whitespace; each keyword is wrapped in `%word%` and `OR`-ed across five indexed fields: `campaign_name`, `segment_name`, `channel_identifier` (recipient destination), `subscriber_first_name`, `subscriber_last_name`. Multiple keywords `AND` together: searching `john acme` returns rows where (name OR campaign OR segment OR destination matches `john`) AND (matches `acme`).

There is **no fuzzy / typo-tolerant matching, no full-text index** — case-insensitive substring only. `%smith%` does match `Smithson`. Each keyword is sanitized before substitution.

### Filter session-persistence is OFF for API calls (verify)

When the API receives an empty filter set, it explicitly clears any legacy session-stored filters. The API never "remembers" the merchant's last filter across requests. Every page load with no filters returns the full list — unlike the legacy admin panel which used to persist filters between visits. (verify)

### Segment + campaign filters require an existing row (verify)

The segment and campaign filters perform a pre-check — they look up at least one log row matching the given name BEFORE applying the where clause. If no row exists for that segment / campaign name on the channel, the filter is silently dropped (no constraint applied). So a typo in the segment name won't produce an empty result — it produces the full unfiltered result. Merchants relying on autocomplete avoid this trap. (verify)

### Date filter operates on the row's last-updated timestamp

The date filter compares against the row's last-update time (when the status was last changed), NOT the original send timestamp. A message sent on day 1, then marked as opened on day 5, will match an "after day 4" filter. This follows from the row-lifecycle rule — see [[channels-logs-row-lifecycle]] for how rows get updated.

### Channel-log filter autocomplete is fed by a denormalized name cache (verify)

The page-load endpoint returns a `filters.campaigns` + `filters.segments` list pulled from a denormalized cache of campaign / segment names that have ever appeared on this channel's log. New names are inserted when log rows are created; the cache populates the filter autocomplete. A merchant who has used 50 campaign names sees those 50 as filter options; deletion of a campaign doesn't immediately remove the name from the filter list. (verify)

### Pagination

Default page size: **25**. The CcTable pagination controls allow the merchant to jump pages and to change the per-page count. The total count is loaded with the response.

## Related

- [[marketing-channels-logs]] — hub.
- [[channels-logs-status-vocabulary]] — the Status column's full enum + colour mapping.
- [[channels-logs-system-vs-campaign]] — the Type column's vocabulary and compound filter key.
- [[channels-logs-message-preview]] — click the channel icon to open the preview.
- [[channels-logs-subscriber-drilldown]] — click the subscriber name; "Deleted Subscriber" rendering; `accept_marketing = 0` warning.
- [[channels-logs-row-lifecycle]] — why the "Date" column is last-updated, not original send.
- [[marketing-channels]] — parent channels hub.

## Open questions

None.
