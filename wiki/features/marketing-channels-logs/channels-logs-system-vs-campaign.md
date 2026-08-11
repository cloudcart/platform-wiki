---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → System vs Campaign"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel logs Type column", "Channel logs campaign vs system", "Channel logs system-message rows", "Channel logs type filter", "system-{channel} filter key", "messages_send SMS-part count"]
tags: [marketing, channels, logs, type, system-messages, campaigns, sms-parts]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (table view, status vocabulary, message preview, subscriber drill-down, row lifecycle).

# Channel logs — system messages vs campaign actions

## Purpose

Every log row is **either** tied to a campaign **or** to a system message. This aspect documents:

- The Type column vocabulary and which row sources fill it.
- Which channels actually expose system-message rows.
- The compound `system-{channel}` filter key.
- The SMS-part count (`messages_send`) carried per-row — relevant because one 3-part SMS counts as 3 sends against the channel cap.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → channel card's **Logs** button. The Type column sits between Status and Date in the [[channels-logs-table-view|table view]]; the Type filter sits in the table's filter dropdown.

## What the merchant can do here

- **See the message source** on every row — *"Campaign action"* or *"System message"*.
- **Filter by message source** — first pick *Campaign message* or *System message*; if System, optionally narrow further to one specific system-message template (e.g., *"Order shipped — Viber"*).
- **Read SMS-part costs** — knowing that one logical SMS body may have counted as 2 or 3 sends against the cap.

## What the merchant cannot do

- **Cannot convert a campaign-action row into a system-message row** or vice versa — the type is determined at send time.
- **Cannot filter on the SMS-part count directly** — `messages_send` is not exposed as a filter (only via the per-channel usage counter on [[marketing-channels-usage]]).
- **Cannot see system-message rows on Email or SMS logs** — those channels' system-templates are managed elsewhere; see the business rules below.

## Settings & fields

### Type vocabulary

| Row source | Type column shows | Identified by |
|---|---|---|
| Campaign step send | *"Campaign action"* | `campaign_id` is set; `type.is_campaign` is true. |
| System-message send | *"System message"* | `campaign_id` is null; `type.is_system` is true. The system-message label being the per-channel event name — *"Order status change"*, *"When customer is created"*, etc. |

The component that renders this is shared with the Status column (different column key on the same renderer).

### Compound `system-{channel}` filter key

The filter "type" accepts two values:

- `campaign` — matches `campaign_id IS NOT NULL`.
- `system-{channel_mapping}` — matches `campaign_id IS NULL` AND optionally `system_message_id = N`.

The combined key like `system-viber_message` lets the merchant pick which channel's system messages to view from the global logs page. When narrowed to a specific system event ID, the filter additionally constrains `system_message_id = value`.

### `messages_send` per-row SMS-part count

Every log-list row carries an extra `messages_send` value computed as `data.smsCount ?? 1` — the number of SMS-parts that a single multi-part SMS was split into:

- Email / Viber / Web Push — always `1`.
- SMS NTH and SMS MsgHub — `n` where the body was split into `n` SMS-parts.

This is the same per-message-count value that increments the channel's send counter (one 3-part SMS = 3 sends counted against the cap). See [[marketing-channels-usage]] for how the counter accumulates against the plan-feature cap.

## Business rules

### Only Viber + Web Push expose system-message rows

System-message rows only appear on the Viber and Web Push logs — those are the only channels that publish per-event system templates managed via [[marketing-channels-system-messages|System messages]].

- **Email logs** — only contain campaign rows. Transactional / event-triggered emails are managed separately via [[marketing-omnichannel-mails-list|Email notifications]] (admin/customer email templates), NOT via this channel's system-messages mechanism.
- **SMS logs (MsgHub + NTH)** — only contain campaign rows. There's no SMS-side system-message catalogue.

So a merchant filtering Email logs by Type = "System message" will see **zero** rows — that's not a bug, that's the platform's separation between marketing-channel system messages (Viber / Web Push) and transactional emails (handled by [[marketing-omnichannel-mails-list]]).

### The Type column derives from `campaign_id IS NULL`

The split is binary at write time. Campaign-step sends always set `campaign_id`. System-message sends never set `campaign_id`. There's no third "manual one-off" type.

### System-message rows still carry segment + status + delivery timestamps

Type doesn't change what other columns mean. A system-message row on the Viber log still gets the full status lifecycle (`SENT` → `DELIVERED` → `SEEN`), still pulls subscriber drill-down (see [[channels-logs-subscriber-drilldown]]), still renders in the [[channels-logs-message-preview|Message Preview]] sub-modal.

### SMS-part count is hidden from the UI but counts against the cap

The merchant cannot see the `messages_send` value in the table — it doesn't have its own column. But the channel's send counter (visible on [[marketing-channels-usage]]) reflects the SUM of `messages_send` across all rows for the period, NOT just the row count. So 1000 single-part SMS rows + 100 three-part SMS rows = 1300 counted sends, not 1100. Merchants approaching their SMS cap should consult the usage page, not just count log rows.

### Segment + campaign filter pre-check applies to system-message rows too

For both campaign rows and system-message rows, the segment / campaign filter autocomplete is fed by the same denormalized name cache (see [[channels-logs-table-view]] for the cache details). System-message rows that aren't tied to a segment leave the Segment column empty and don't contribute to the segment-name autocomplete.

### Filter narrowing — "System" + specific template

When the merchant picks *System message* in the Type filter, a second dropdown appears listing every system-message template that has at least one row on this channel. Selecting one narrows the filter further (`system_message_id = N`). The system-message list is per-channel — the Email log's System branch is always empty (no SMS / Email system templates flow through this mechanism).

## Related

- [[marketing-channels-logs]] — hub.
- [[channels-logs-table-view]] — the Type column + Type filter live here.
- [[channels-logs-status-vocabulary]] — system-message rows go through the same status lifecycle as campaign rows.
- [[channels-logs-row-lifecycle]] — campaign vs system distinction is set at write time and frozen on the row.
- [[channels-logs-message-preview]] — system-message rows render through the same preview component.
- [[marketing-channels-system-messages]] — System messages modal where Viber + Web Push system templates are defined.
- [[marketing-omnichannel-mails-list]] — Email notifications (transactional emails) — NOT logged on the Email channel log.
- [[marketing-channels-usage]] — channel send-counter that consumes `messages_send` (SMS-parts).
- [[marketing-campaigns]] — campaigns generate the "Campaign action" rows.

## Open questions

None.
