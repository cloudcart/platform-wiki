---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → Row lifecycle"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Channel logs row lifecycle", "Channel logs status_archive", "Channel logs pre-flight failures", "Channel logs NOT_SENT", "Channel logs retention", "Channel logs append-only", "NOT_SENT without reason"]
tags: [marketing, channels, logs, lifecycle, retention, preflight]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (table view, status vocabulary, message preview, subscriber drill-down, system vs campaign).

# Channel logs — row lifecycle

## Purpose

This aspect documents what happens to a single log row from the moment it's created (dispatch) through every status update from the provider — plus the two lifecycle edge cases that confuse merchants most often:

1. **Pre-flight failures**, which write **no** row on this Log: their reason goes to the campaign's statistics step log and the subscriber's log.
2. **Retention** — there is currently no documented retention policy; rows are kept indefinitely.

The append-only nature of the log + the `status_archive` history is what makes the "Date" column in the [[channels-logs-table-view|table view]] reflect last-update time rather than the original send time.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → channel card's **Logs** button. Row-lifecycle effects are visible in the table's Date column, the Status pill (see [[channels-logs-status-vocabulary]]), and the *"Subscriber does not accept marketing"* warning on the Destination cell (see [[channels-logs-subscriber-drilldown]]).

## What the merchant can do here

- **Read `NOT_SENT` rows** — every send row starts at `NOT_SENT`; one left there was typically never accepted (Email) or hit a provider error (SMS, Viber, push).
- **Keep historical evidence indefinitely** — no automatic purge happens at the merchant tier.

## What the merchant cannot do

- **Cannot delete log rows.** Append-only — no per-row delete, no bulk delete.
- **Cannot see the `status_archive` history in the UI** — the history lives on the row but isn't surfaced as a timeline panel.
- **Cannot see pre-flight failures here** — they appear only in the campaign's statistics step log and the subscriber's log.

## Settings & fields

### One row per (subscriber, campaign action) send attempt

The platform writes one log row, status `NOT_SENT`, when each send is dispatched (Email, SMS, Viber, Web Push), before the provider call. For **Email** it turns `SENT` only when Elastic Email accepts the message. When the channel provider later reports back via webhook (Elastic Email delivery, Viber DLR, Web Push success, etc.), the platform **updates the same row** by:

- Changing `status` to the new canonical value (see [[channels-logs-status-vocabulary]]).
- Setting one of `delivered_at` / `seen_at` to the webhook timestamp.
- Appending the prior status to a `status_archive` array (so the row keeps the full status timeline).

The merchant doesn't see this archive in the UI, but it explains why a row's "Date" column reflects the most recent status change, not the original send time.

The row count equals **unique sends**, not total delivery events. A campaign that sent to 5,000 subscribers shows 5,000 rows even if each was opened twice and clicked once.

### Pre-flight failures write no `NOT_SENT` row

A subscriber failing a per-channel pre-flight check (unsubscribed, no marketing consent, bounced, unverified; Email texts on [[email-channel-send-pipeline]]) gets a separate campaign-log row with **no** delivery status and no channel, the reason as its message, and is removed from the campaign. That row is **absent from this Log**, which lists only the channel's rows; it shows in the campaign's statistics step log (reason in red under Destination) and in the subscriber's own log. A provider error on SMS, Viber or push leaves the send's `NOT_SENT` row here and writes the reason to the step log the same way.

The *"Subscriber does not accept marketing"* warning on the `Destination` column is a live lookup of the subscriber's current flags, independent of the row's status — see [[channels-logs-subscriber-drilldown]].

### Email: `NOT_SENT` with no reason means never accepted

Pre-flight failures never produce a `NOT_SENT` row. An Email row left at `NOT_SENT` with **no** reason was dispatched but never accepted by Elastic Email, though *Total sent* already counted it. A whole campaign of such rows, with no recorded errors, typically means the store's Elastic Email key is rejected — see [[email-channel-reconnect]].

### Status-archive history is kept indefinitely

Every status update on a log row pushes the prior status onto a `status_archive` JSON array on the same record. The archive entry records `{status, original, date}` for every transition. The UI doesn't display this history (no timeline panel), but it lives on the row forever — heavy-volume rows can accumulate dozens of transitions (`SENT` → `ACCEPTED` → `DELIVERED` → `SEEN` → `CLICKED` → `PURCHASE`). The archive is what makes the "Date" column reflect the latest update rather than the original send time.

### Retention — no documented automatic policy

There is currently **no automatic retention policy** documented on the channel logs collection — log rows are kept indefinitely. Heavy-volume merchants accumulate millions of rows over years; pagination + filters are the merchant's only navigation aid. (verify) Confirm with CloudCart support whether large-tenant pruning is in place.

### `marketing:clear --orphans` cleans content-only records (internal)

A platform maintenance command (`marketing:clear --orphans --batch-size=N`) exists to delete message-content records that have no matching log parent. Run by ops to reclaim space when log purge was incomplete (e.g., partial site deletion). This is a CloudCart-staff-side tool — not exposed to merchants — but explains why the merchant occasionally sees a "preview not available" if they click Preview on a row whose content was previously cleaned.

## Business rules

### No timeout, but Email and Viber are re-checked

If the provider never reports back, nothing times the row out to `UNDELIVERED`. Email and Viber rows still unresolved do get background status checks, which can turn them `ERROR` — see [[channels-logs-status-vocabulary]].

### Pre-flight check semantics are per-channel, not global

A subscriber who is unsubscribed from Email but consented to Viber will:

- Get no row on the Email log (excluded at launch, or a reason row in the campaign's step log).
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
- [[channels-logs-subscriber-drilldown]] — the live *"does not accept marketing"* warning; subscriber deletion preserves the denormalized name on the row.
- [[channels-logs-message-preview]] — `sent_at` is always set because every row is created at dispatch; `delivered_at` / `seen_at` are conditional on webhook events.
- [[marketing-channels]] — hub for the channel cards.
- [[marketing-subscribers]] — source of the per-channel `marketing` / `verified` / `bounced` / `unsubscribed` flags that gate pre-flight.

## Open questions

- Documented retention policy at the merchant tier — currently there isn't one; confirm whether a platform-side pruning policy exists for very large tenants.

