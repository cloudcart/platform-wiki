---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs → Status vocabulary"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel logs status", "Channel logs status enum", "Channel logs status pill", "Channel logs status colour", "BOUNCED vs HARD_BOUNCED", "DELIVERED status", "Channel logs delivery status", "translateStatus"]
tags: [marketing, channels, logs, status, vocabulary]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-logs]]. See the hub for the other aspects (table view, message preview, subscriber drill-down, row lifecycle, system vs campaign).

# Channel logs — status vocabulary

## Purpose

Every log row carries one canonical **status** value drawn from a shared vocabulary across all five channels (Email, SMS MsgHub, SMS NTH, Viber, Web Push). The status is surfaced both as a coloured pill (the Status column on the [[channels-logs-table-view|table view]]) and as a filter option. This aspect catalogues the full enum, the colour mapping, the per-channel status source (which provider reports which status), and the `BOUNCED` ⇒ HARD_BOUNCED filter auto-union.

The colour and label come from the abstract channel manager's shared `translateStatus` + `colorStatus` helpers — one mapping table for all five channels, so a `BOUNCED` row on Email and a `BOUNCED` row on Viber show the same coloured pill.

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
| `PENDING` | Provider is retrying (e.g., Elastic Email *WaitingToRetry*). | Orange |
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
| `NOT_SENT` | Platform skipped the send (subscriber failed pre-flight checks — unsubscribed, unverified, marketing = 0). See [[channels-logs-row-lifecycle]]. | Red |
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
| Web Push | Browser push service ack | `CREATED` (subscription), `SENT` (request sent), `DELIVERED` / `SEEN` when the browser confirms. Most push services don't report `SEEN` reliably. |

If the webhook never fires (provider downtime, network failure, etc.), the row stays in `SENT` indefinitely — the platform doesn't speculatively flip it.

## Business rules

### Status filter for `BOUNCED` auto-unions `HARD_BOUNCED`

When the merchant filters by status `BOUNCED`, the query is `WHERE status IN ('BOUNCED', 'HARD_BOUNCED')` — both soft and hard bounces are returned. This is intentional merchant-friendly behaviour — most merchants don't care about the soft/hard distinction; they want to see "all failed-to-deliver emails". The hard-bounce-only view requires filtering by `HARD_BOUNCED` directly.

### Status pill colour groups are fixed (verify)

The colour mapping is hard-coded: green = `notification-green` ("enabled"-style) for success states (`SENT` / `DELIVERED` / `SEEN` / `CLICKED` etc.); red = `notification-red` ("required"-style) for failure states; orange = `notification-orange` for in-progress states. The merchant cannot customise these. (verify)

### `SENT` is sticky when the webhook never fires

If a channel provider's webhook never reports back (provider downtime, lost network, misconfigured destination), the row stays at `SENT` indefinitely. The platform does NOT timeout `SENT` rows or speculatively flip them to `UNDELIVERED`. A merchant looking for "is delivery confirmation slow or never coming?" should check the channel-provider dashboard, not assume the platform will retry the status check.

### `NOT_SENT` is the platform's own status — not a provider value

`NOT_SENT` is written by the platform itself when the subscriber fails one of the per-channel pre-flight checks BEFORE the send is even attempted. See [[channels-logs-row-lifecycle]] for the full pre-flight rules and the `error` field that explains why.

### `SEEN` semantics are channel-specific

- **Email** — provider open-pixel beacon fired (means: the email client downloaded images, which most modern clients defer or block, so undercounts).
- **Viber** — Viber's native read-receipt (most reliable).
- **Web Push** — depends on the browser push service; many don't report `SEEN` at all.
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
