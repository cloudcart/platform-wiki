---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS Msg Hub → Send pipeline"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS MsgHub send pipeline", "MsgHub synchronous send", "MsgHub status mapping", "MsgHub pre-flight checks", "MsgHub plan-cap pre-flight"]
tags: [marketing, channels, sms, msghub, send]
plan_gates: ["campaign.channel.sms_msghub_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-sms-msghub]]. See the hub for the other aspects (overview, settings, length & billing, DLR webhook).

# SMS MsgHub — Send pipeline

## Purpose

Documents what happens between a campaign step firing and MsgHub receiving the SMS request — the synchronous-send model that distinguishes this channel from every other, the HTTP-code-based status mapping, the per-subscriber pre-flight checks, the plan-cap pre-flight, and the internal-title format used in the logs.

## Where to find it

The send pipeline is invisible to the merchant — it runs server-side after a campaign step (action type **"SMS (msghub)"**, mapping `sms_msghub_message`) fires. The merchant observes the **result** via the channel's Logs modal (see [[sms-msghub-overview]]) and the campaign stats screens. The eventual carrier-confirmed status arrives later via [[sms-msghub-dlr-webhook]].

## What the merchant can do here

Nothing directly — this aspect documents the under-the-hood pipeline so support can answer "why didn't my SMS send?" questions. Merchant-facing controls live on [[sms-msghub-overview]] and [[sms-msghub-settings]].

## Settings & fields

### Channel-manager constants

| Constant | Value | Effect |
|----------|-------|--------|
| Channel ID | `sms_msghub_message` | The channel mapping key. |
| Group | `phone` | Groups with NTH and Viber under the Phone subscriber-channel category. |
| Subscriber channel | Phone | Recipient identity is the verified phone number. |
| UTM medium | `sms` | Applied to shortened URLs in the message body. |
| Gates | `installed` AND `active` | Both must be on for sends to fire. |

### Status mapping (HTTP-code based, not text-state)

MsgHub responds with `meta.code` containing the HTTP-status-class code; the platform maps **the numeric code only** (the `status_msg` text is not parsed):

| MsgHub `meta.code` | CloudCart status |
|---|---|
| `200` | `SENT` |
| `202` | `DELIVERED` (MsgHub treats accepted-for-delivery as already delivered) |
| `400`–`599` | `ERROR` (any 4xx / 5xx) |
| other | passed through as-is |

The full response object IS stored in the log row's `data` field for debugging.

## Business rules

### Synchronous send is the platform-distinguishing trait

MsgHub is the **only** marketing channel that POSTs to the provider inside the campaign-action thread — every other channel (Email, NTH, Viber, Web Push) queues a per-recipient job. Practical consequences:

- A slow MsgHub response **blocks** the campaign worker, slowing throughput on the campaign queue while the call is in flight.
- The log row is created with full response data inline (`message_id = sms_id`, `data = full JSON response`, `execution_time = seconds`) — no second-pass enrichment.
- The `TOTAL_SENT` and `SUCCESSFULLY_SENT` channel-statistics counters are incremented inline before the loop moves to the next subscriber.
- After the inline send completes, a subscriber-statistic update job is dispatched with `retry(5, ..., 1000)` — 5 attempts with 1-second backoff. Failures here are silent (caught and logged).

### Per-subscriber pre-flight checks before sending

For each SMS send, the platform checks the recipient's Phone channel row:

- `channel_identifier` must be non-empty (the subscriber has a phone number).
- `unsubscribed` must be 0.
- `marketing` must be 1.
- `verified` must be 1 (the phone number was verified — typically via the OTP flow at signup or by setting verified-on-import).
- `bounced` must be 0 (no prior delivery errors).

Any failure short-circuits the send and writes a log row with the matching error message.

### Phone-number normalisation strips +, -, spaces

Before sending, the phone number is run through `FILTER_SANITIZE_NUMBER_INT` then has `+`, `-`, and space chars removed — so `+359 88 123 4567` becomes `359881234567`. The merchant doesn't need to pre-format, **but** the subscriber's `channel_identifier` must include the country code (no leading 0; no national format).

### Plan-cap pre-flight can auto-deactivate the channel

The send short-circuits to a plan-cap check BEFORE making the HTTP call. If the merchant's cap is exhausted (`plan_remaining <= 0`, and MsgHub doesn't support self-credentials), the channel is **auto-deactivated** (`active` set to false) and a queue-attached access-denied exception is recorded for the audit log. The merchant sees this on the channel card as the banned-reason. The cap accounting and Buy-more-credits flow are on [[sms-msghub-length-billing]].

### Per-message internal title format

The Internal title saved on the channel-action template becomes `{campaign.title} - {template.internal_title}` (or "N/A" if `internal_title` is empty) — used as the title in the channel's Logs view and on MsgHub's side for traceability.

### Auto-suspend triggers rarely fire

The MsgHub channel inherits the abstract's spam/bounce/open auto-suspend logic, but in practice the SMS channel doesn't get reputation data back from the provider, so those triggers rarely fire. The `cc_denied` manual suspend (a CloudCart employee blocking the merchant for policy violations) is the more common path here.

## How it works

The campaign action validates subscriber channel state, renders the message body, shortens URLs with `utm_medium=sms` campaign-attribution params, then POSTs synchronously to `{base}/send` (request shape + HMAC signing on [[sms-msghub-settings]]). It increments the channel-statistics counters and writes the channel-log row immediately, then dispatches the subscriber-statistic update job. Status is derived from the HTTP code per the mapping above; the DLR webhook later overwrites the same row with the carrier-confirmed state — see [[sms-msghub-dlr-webhook]].

## Related

- [[marketing-channels-sms-msghub]] — hub.
- [[sms-msghub-settings]] — the `/send` request shape, HMAC signing, sandbox routing.
- [[sms-msghub-dlr-webhook]] — what overwrites the log row after the carrier confirms.
- [[sms-msghub-length-billing]] — the plan-cap accounting behind the pre-flight auto-deactivate.
- [[marketing-subscribers]] — the Phone subscriber-channel row checked in pre-flight.

## Open questions

No outstanding questions.
