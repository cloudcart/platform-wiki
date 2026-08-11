---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → Row lifecycle"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel logs row lifecycle", "Channel logs status_archive", "Channel logs pre-flight failures", "Channel logs NOT_SENT", "Channel logs sandbox", "Channel logs retention", "Channel logs append-only"]
tags: [marketing, channels, logs, lifecycle, retention, sandbox, preflight]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (table view, status vocabulary, message preview, subscriber drill-down, system vs campaign).

# Channel logs — row lifecycle

## Purpose

This aspect documents what happens to a single log row from the moment it's created (dispatch) through every status update from the provider — plus the three lifecycle edge cases that confuse merchants most often:

1. **Pre-flight failures** that produce `NOT_SENT` rows with a human-readable explanation BEFORE the platform ever talks to the provider.
2. **Sandbox sends** that get redirected to a merchant-configured URL but are still logged normally.
3. **Retention** — there is currently no documented retention policy; rows are kept indefinitely.

The append-only nature of the log + the `status_archive` history is what makes the "Date" column in the [[channels-logs-table-view|table view]] reflect last-update time rather than the original send time.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → channel card's **Logs** button. Row-lifecycle effects are visible in the table's Date column, the Status pill (see [[channels-logs-status-vocabulary]]), and the *"Subscriber does not accept marketing"* warning on the Destination cell (see [[channels-logs-subscriber-drilldown]]).

## What the merchant can do here

- **Browse `NOT_SENT` rows** — the platform writes a row with a merchant-readable error when a pre-flight check fails.
- **See sandbox-redirected sends** in the log as normal-looking rows (the sandbox flag is internal-only).
- **Keep historical evidence indefinitely** — no automatic purge happens at the merchant tier.

## What the merchant cannot do

- **Cannot delete log rows.** Append-only — no per-row delete, no bulk delete.
- **Cannot see the `status_archive` history in the UI** — the history lives on the row but isn't surfaced as a timeline panel.
- **Cannot opt out of the `NOT_SENT` writes** — every pre-flight failure is logged for audit, even though the message was never sent.

## Settings & fields

### One row per (subscriber, campaign action) send attempt

The platform writes one log row when each send job is dispatched (status set to `SENT`). When the channel provider later reports back via webhook (Elastic Email delivery, Viber DLR, Web Push success, etc.), the platform **updates the same row** by:

- Changing `status` to the new canonical value (see [[channels-logs-status-vocabulary]]).
- Setting one of `delivered_at` / `seen_at` to the webhook timestamp.
- Appending the prior status to a `status_archive` array (so the row keeps the full status timeline).

The merchant doesn't see this archive in the UI, but it explains why a row's "Date" column reflects the most recent status change, not the original send time.

The row count equals **unique sends**, not total delivery events. A campaign that sent to 5,000 subscribers shows 5,000 rows even if each was opened twice and clicked once.

### Pre-flight failures show as `NOT_SENT` with an explanation

If the subscriber fails one of the per-channel pre-flight checks, the platform writes a row with `status = NOT_SENT` and an `error` field describing the reason. The checks gate on the per-channel `SubscriberChannel` flags:

- `unsubscribed = 1` → *"This subscriber is unsubscribed."*
- `marketing = 0` (no consent) → *"You haven't consented to marketing"*
- `bounced = 1` (prior hard bounce) → the recipient is blocked for that channel.
- `verified = 0` AND `unconfirmed_send` is OFF → *"No message will be sent to this email because it has not been verified."*

The `Destination` column on `NOT_SENT` rows also shows the *"Subscriber does not accept marketing"* warning when the live `accept_marketing` flag is 0 — see [[channels-logs-subscriber-drilldown]]. The two indicators (`NOT_SENT` status + warning) overlap but aren't identical — the warning is a live lookup; the `NOT_SENT` status is set at send time.

### Sandbox sends are logged too

When the channel is in sandbox mode (a sandbox URL is set on the channel), outbound messages get redirected to the merchant's chosen webhook URL but are **still logged** — `sandbox = 1` and `sandbox_url` is populated on the row. The merchant sees normal log rows; the visual distinction is on the Sandbox setting itself (on [[marketing-channels|Channels setup]]), not on the log.

### Status-archive history is kept indefinitely

Every status update on a log row pushes the prior status onto a `status_archive` JSON array on the same record. The archive entry records `{status, original, date}` for every transition. The UI doesn't display this history (no timeline panel), but it lives on the row forever — heavy-volume rows can accumulate dozens of transitions (`SENT` → `ACCEPTED` → `DELIVERED` → `SEEN` → `CLICKED` → `PURCHASE`). The archive is what makes the "Date" column reflect the latest update rather than the original send time.

### Retention — no documented automatic policy

There is currently **no automatic retention policy** documented on the channel logs collection — log rows are kept indefinitely. Heavy-volume merchants accumulate millions of rows over years; pagination + filters are the merchant's only navigation aid. (verify) Confirm with CloudCart support whether large-tenant pruning is in place.

### `marketing:clear --orphans` cleans content-only records (internal)

A platform maintenance command (`marketing:clear --orphans --batch-size=N`) exists to delete message-content records that have no matching log parent. Run by ops to reclaim space when log purge was incomplete (e.g., partial site deletion). This is a CloudCart-staff-side tool — not exposed to merchants — but explains why the merchant occasionally sees a "preview not available" if they click Preview on a row whose content was previously cleaned.

## Business rules

### `SENT` is sticky when the webhook never fires

If the channel provider's webhook never reports back (provider outage, lost network), the row stays in `SENT` indefinitely. The platform does NOT timeout `SENT` rows. See the same point in [[channels-logs-status-vocabulary]].

### Pre-flight check semantics are per-channel, not global

A subscriber who is unsubscribed from Email but consented to Viber will:

- Produce `NOT_SENT` rows on the Email log (with the unsubscribed explanation).
- Produce normal sends + delivery rows on the Viber log.

The checks read the per-channel `SubscriberChannel` flags, NOT the global subscriber-level marketing flag.

### The denormalized recipient name survives subscriber deletion

When a row is written, the platform copies the subscriber's `first_name` / `last_name` onto the row itself. Later subscriber deletion does NOT delete the log row. The denormalized name is what the table shows under the *"Deleted Subscriber (ID: ...)"* label — the live subscriber record is gone but the historical identity is preserved. See [[channels-logs-subscriber-drilldown]].

### Row updates do NOT create new rows — they overwrite

The row's `updated_at` advances on every status change. There is one row per send — even with 6 status transitions, the row count stays at 1. Counters that compare "rows shown" to "messages dispatched" are stable.

## Related

- [[marketing-channels-logs]] — hub.
- [[channels-logs-status-vocabulary]] — the values that pass through the `status` field + `status_archive`.
- [[channels-logs-table-view]] — the Date column reflects the last status update, NOT the original send time, because of the row-lifecycle rules here.
- [[channels-logs-subscriber-drilldown]] — `NOT_SENT` interacts with the *"does not accept marketing"* warning; subscriber deletion preserves the denormalized name on the row.
- [[channels-logs-message-preview]] — `sent_at` is always set because every row is created at dispatch; `delivered_at` / `seen_at` are conditional on webhook events.
- [[marketing-channels]] — sandbox configuration lives on the channel card here.
- [[marketing-subscribers]] — source of the per-channel `marketing` / `verified` / `bounced` / `unsubscribed` flags that gate pre-flight.

## Open questions

- Documented retention policy at the merchant tier — currently there isn't one; confirm whether a platform-side pruning policy exists for very large tenants.

