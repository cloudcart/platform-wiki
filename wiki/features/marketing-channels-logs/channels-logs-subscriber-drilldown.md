---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → Subscriber details"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel logs subscriber drill-down", "Channel logs subscriber details", "Deleted subscriber log row", "Subscriber does not accept marketing warning", "accept_marketing warning", "SubscriberChannel flags from log"]
tags: [marketing, channels, logs, subscribers, drilldown]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (table view, status vocabulary, message preview, row lifecycle, system vs campaign).

# Channel logs — subscriber drill-down

## Purpose

The **Subscriber details** sub-modal opens when the merchant clicks the subscriber name on a log row. It shows the recipient's full subscriber profile — per-channel membership flags, segment memberships, message history across all channels, tags, custom fields. Same component used on the standalone subscriber-detail page at [[marketing-subscribers]].

This aspect also documents the two related row-level renderings that interact with subscriber state:

- **Deleted-subscriber rows** — when the recipient subscriber has been deleted after the send, the row still appears but the drill-down is disabled.
- **The *"Subscriber does not accept marketing"* warning** — a visual cue on the Destination cell when the recipient's current `accept_marketing` flag is 0.

Modal size: `xll`. Title — *"Subscriber details"*. Cancel button: *"Close"*. No Save button.

While this sub-modal is open, the outer Logs modal's size flips from `xll` to `100` (full-screen) so the merchant gets maximum drill-down real-estate.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → channel card's **Logs** button → click the **Subscriber name** column on any row (only for active, non-deleted subscribers).

## What the merchant can do here

- **See the recipient's full subscriber profile** — same component as the standalone subscriber page.
- **See per-channel `SubscriberChannel` rows** — Email / Phone / WebPush channels and per-channel `marketing` / `verified` / `bounced` / `unsubscribed` flags.
- **See segment memberships** — every segment the recipient is currently in.
- **See message history across all channels** — not just the channel the log was opened from.
- **See tags + custom fields** — the merchant-maintained customer attributes.

## What the merchant cannot do

- **Cannot edit subscriber data from here** — the embedded `MarketingSubscriberDetails` opens in read-mode in this context. To edit, the merchant goes to the standalone [[marketing-subscribers|Subscribers]] page.
- **Cannot drill into a deleted subscriber.** Rows labelled *"Deleted Subscriber (ID: ...)"* render as non-clickable text — the drill-down link is disabled.
- **Cannot drill into rows without a linked subscriber** — *"N/A"* rows (no `subscriber_id` recorded) are likewise non-clickable.

## Settings & fields

### Drill-down click handler — gated by two conditions

The click handler on the Subscriber-name cell opens the sub-modal only when **BOTH**:

- `subscriber_active = true` — the subscriber has not been deleted.
- `subscriber_id` is set — the row was written with a subscriber link in the first place.

If either is false, the cell renders as plain text (no underline, no cursor pointer).

### Deleted-subscriber row rendering

When a recipient subscriber has been deleted after the send was logged, the row stays — but the Subscriber column shows the label `Deleted Subscriber (ID: <id>)` instead of the name link. The historical first / last name is preserved on the log row itself via denormalized `first_name` / `last_name` columns, but the drill-down is disabled because the underlying subscriber record no longer exists.

### `accept_marketing = 0` Destination-cell warning

If the recipient subscriber's `accept_marketing` flag is 0 at the time of the log read, the row's Destination cell shows a red warning *"Subscriber does not accept marketing"* below the channel identifier. The warning is rendered **only for active (non-deleted) subscribers** where the flag is currently 0.

This is a **live lookup**, not a snapshot from send time — a recipient who consented at the time of send but later toggled off marketing will retroactively show the warning. The warning serves as a quick visual cue for "this recipient is now opted out" without forcing the merchant to open Subscriber details.

## Business rules

### Subscriber existence check is batched per page

For every page of log rows, the platform extracts all unique `subscriber_id` values and issues **ONE** batched lookup to mark which subscriber IDs still exist, plus **ONE** batched lookup for the `accept_marketing` flag map. Rows whose `subscriber_id` is in neither list render as *"Deleted Subscriber (ID: ...)"* with disabled drill-down.

This means: rows are stable even if subscribers are deleted later. The historical recipient name is preserved via the row's denormalized `first_name` / `last_name`, but the live drill-down + accept-marketing warning reflect the CURRENT subscriber state.

### Embedded subscriber-detail component mounts only when modal is open

The sub-modal's body uses `v-if="modal"` so the `MarketingSubscriberDetails` component is only mounted when the modal is actually open — preventing unnecessary fetches when the merchant is just scrolling the log table.

### Outer log modal expands to full-screen when this sub-modal is open

When the merchant drills into a subscriber, the outer Logs modal flips its size from `xll` to `100` (full-screen). On close of the inner sub-modal, the outer modal returns to `xll`. This is purely a UI-real-estate optimization — no data change.

### Deleted subscribers do NOT remove their log rows

Deleting a subscriber from [[marketing-subscribers]] does NOT cascade-delete that subscriber's log rows on any channel. The rows stay (append-only, see [[channels-logs-row-lifecycle]]) and continue to appear with the *"Deleted Subscriber"* label. This is intentional — the merchant retains historical delivery evidence even after subscriber lifecycle changes.

### `accept_marketing` warning is per-channel-aware (verify)

The Destination warning checks the per-channel `accept_marketing` flag, not the global subscriber flag. So a subscriber who has opted out of Email marketing but kept Viber marketing will show the warning on Email log rows but NOT on Viber log rows. (verify)

## Related

- [[marketing-channels-logs]] — hub.
- [[channels-logs-table-view]] — the Subscriber column hosts the drill-down click; the Destination column renders the `accept_marketing` warning.
- [[channels-logs-message-preview]] — sibling sub-modal opened from the channel-icon click.
- [[channels-logs-row-lifecycle]] — `NOT_SENT` rows for pre-flight failures use the SAME per-channel `marketing` / `verified` / `bounced` / `unsubscribed` flags.
- [[marketing-subscribers]] — destination of the drill-down; same component used on the standalone subscriber-detail page. Editing happens here, not in the embedded view.

## Open questions

- Whether the `accept_marketing = 0` warning checks the per-channel subscription flag specifically, or the global subscriber-level marketing flag.

