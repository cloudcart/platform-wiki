---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → Status vocabulary"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Channel logs status", "Channel logs status enum", "Channel logs status pill", "Channel logs status colour", "BOUNCED vs HARD_BOUNCED", "DELIVERED status", "Channel logs delivery status", "translateStatus"]
tags: [marketing, channels, logs, status, vocabulary]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (table view, message preview, subscriber drill-down, row lifecycle, system vs campaign).

# Channel logs — status vocabulary

## Purpose

Every log row carries one canonical **status** value drawn from a shared vocabulary across every channel (Email, SMS MsgHub, SMS NTH, Viber, Web Push). The status is surfaced both as a coloured pill (the Status column on the [[channels-logs-table-view|table view]]) and as a filter option. This aspect catalogues the full enum, the colour mapping, the per-channel status source (which provider reports which status), and the `BOUNCED` ⇒ HARD_BOUNCED filter auto-union.

The colour and label come from the abstract channel manager's shared `translateStatus` + `colorStatus` helpers — one mapping table for every channel, so a `BOUNCED` row on Email and a `BOUNCED` row on Viber show the same coloured pill.

## Where to find it

The Status pill appears in the Status column of the [[channels-logs-table-view|Channel logs table]] and in the Status field of the [[channels-logs-message-preview|Message Preview]] sub-modal.

## What the merchant can do here

- **Read the row's delivery state** at a glance via the pill colour (green = success, orange = in-progress, red = failure).
- **Filter rows** by any single canonical status from the table's filter dropdown.

## What the merchant cannot do

- **Cannot change a row's status** — statuses are written by the platform on dispatch and updated by provider webhooks. The merchant has no override.
- **Cannot filter by status colour** — only by the exact enum value. (Choosing `BOUNCED` is the closest to "show me all email failures" — see the auto-union rule below.)

## Settings & fields

### Canonical status enum (verbatim values)

The platform stores every send's status in one of the following values — surfaced both as a coloured pill and via filter:

| Status | Meaning (merchant-facing) | Pill colour |
|--------|---------------------------|-------------|
| `SENT` | Handed off to the channel provider; not yet confirmed delivered. | Orange |
| `ACCEPTED` | Channel provider acknowledged receipt of the request. | Orange |
| `PENDING` | Provider is retrying (e.g., Elastic Email *WaitingToRetry*). Has no label: the pill reads "N/A". | Red |
| `DELIVERED` | Recipient device / inbox received the message. | Green |
| `SEEN` (alias: Opened for Email) | Recipient opened / saw the message. | Green |
| `CLICKED` | Recipient clicked a link inside the message. | Green |
| `CREATED` | Web Push subscription was created from this push. | Green |
| `PURCHASE` | Attributable purchase made after this send. | Green |
| `COMPLETED` | Provider workflow finished (intermediate states resolved). | Green |
| `UNDELIVERED` | Provider attempted but could not deliver (recipient offline / unreachable). | Red |
| `EXPIRED` | Provider TTL elapsed without delivery (common for Viber when recipient offline). | Red |
| `REJECTED` | Provider rejected (e.g., Viber number is not a Viber user). | Red |
| `UNDELIVERABLE` | Provider classifies the destination as permanently undeliverable. | Red |
| `NOT_SENT` („Неизпратен“) | Status every send row is written with at dispatch, before the provider call. Email turns `SENT` on acceptance; left with no reason = never accepted. SMS / Viber / push: left after a provider error. Pre-flight failures never appear here. See [[channels-logs-row-lifecycle]]. | Red |
| `ERROR` | Generic delivery error from the provider. | Red |
| `BOUNCED` | Soft bounce (Email). | Red |
| `HARD_BOUNCED` | Hard bounce (Email — permanent failure). | Red |
| `UNSUBSCRIBED` | Recipient unsubscribed in response to this send. | Red |
| `ABUSE_REPORT` | Recipient flagged this send as spam (Email AbuseReport hook). | Red |

Values that don't apply to a given channel will simply never appear on that channel's log (e.g., `SEEN` is meaningless for SMS NTH which has no read-receipt; `CREATED` only applies to Web Push).

### Per-channel status source

Each channel's status updates flow from a different provider:

| Channel | Status source | What it reports |
|---------|---------------|------------------|
| Email | Elastic Email webhook | Sent, Opened (→ `SEEN`), Clicked, Unsubscribed, Error → `HARD_BOUNCED`, AbuseReport → `ABUSE_REPORT`, WaitingToRetry → `PENDING`. |
| SMS MsgHub | MsgHub DLR webhook | `DELIVERED`, `UNDELIVERED`, `EXPIRED`, `REJECTED`, `NOT_SENT`. |
| SMS NTH | NTH DLR webhook | `DELIVERED`, `UNDELIVERED`, `REJECTED`, `EXPIRED`. |
| Viber | InfoBip DLR webhook | `DELIVERED`, `SEEN` (Viber's read-receipt), `UNDELIVERED`, `EXPIRED`, `REJECTED`. |
| Web Push | Browser push service ack | `CREATED` (subscription), `SENT` (request sent), `DELIVERED` when the notification is shown, `CLICKED` when tapped. `SEEN` never occurs. |

Email and Viber also get background status checks (below).

## Business rules

### Status filter for `BOUNCED` auto-unions `HARD_BOUNCED`

When the merchant filters by status `BOUNCED`, the query is `WHERE status IN ('BOUNCED', 'HARD_BOUNCED')` — both soft and hard bounces are returned, since most merchants want "all failed-to-deliver emails". For hard bounces only, filter by `HARD_BOUNCED`.

### Status pill colour groups are fixed (verify)

The colour mapping is hard-coded: green = `notification-green` ("enabled"-style) for success states (`SENT` / `DELIVERED` / `SEEN` / `CLICKED` etc.); red = `notification-red` ("required"-style) for failure states; orange = `notification-orange` for in-progress states. The merchant cannot customise these. (verify)

### Background status checks (Email, Viber)

Nothing times a row out to `UNDELIVERED`, but two channels re-check unresolved rows:

- **Email** — an hourly background status check. A failed lookup (e.g. a dead key) sets `ERROR` *"Empty status message"*, which is not a real bounce.
- **Viber** — rows still pending, older than 4 hours and younger than 7 days, are checked up to 10 times and may become `ERROR` *"No status information for message"*.

### `NOT_SENT` is the platform's own status — not a provider value

The platform writes `NOT_SENT` on every send row at dispatch, before the provider call (Email, SMS, Viber, Web Push). An Email row turns `SENT` when Elastic Email accepts it; one left at `NOT_SENT` with no reason was never accepted, typically a rejected key — see [[email-channel-reconnect]]. For SMS, Viber and push, a provider error leaves the row at `NOT_SENT` and puts the reason in the campaign's step log. Pre-flight failures (unsubscribed, unverified, no consent) write no row here — see [[channels-logs-row-lifecycle]].

### `SEEN` semantics are channel-specific

- **Email** — provider open-pixel beacon fired (means: the email client downloaded images, which most modern clients defer or block, so undercounts).
- **Viber** — Viber's native read-receipt (most reliable).
- **Web Push** — `SEEN` never occurs (`DELIVERED` when shown, `CLICKED` when tapped).
- **SMS (both MsgHub + NTH)** — `SEEN` never appears (SMS has no read-receipt).

### `PURCHASE` is an attribution status, not a delivery status

When a recipient places an order within an attribution window after a marketing send, the platform may write `PURCHASE` onto the row. This is a marketing-attribution mark, not a delivery confirmation. (verify) It supplements (rather than replaces) the prior delivery status via the `status_archive` history — see [[channels-logs-row-lifecycle]].

## Related

- [[marketing-channels-logs]] — hub.
- [[channels-logs-table-view]] — where the Status pill is rendered + filtered.
- [[channels-logs-row-lifecycle]] — how `status_archive` keeps the history of transitions; how `NOT_SENT` is written.
- [[channels-logs-message-preview]] — Status field on the preview sub-modal mirrors the table row.
- [[marketing-channels-email]] — Email channel + Elastic Email webhook source.
- [[marketing-channels-sms-msghub]] — SMS via MsgHub + MsgHub DLR webhook.
- [[marketing-channels-sms-nth]] — SMS via NTH + NTH DLR webhook.
- [[marketing-channels-viber]] — Viber + InfoBip DLR webhook.
- [[marketing-channels-webpush]] — Web Push + browser push service ack.
- [[notification-delivery]] — platform-wide outbound-delivery concept page.

## Open questions

None.
