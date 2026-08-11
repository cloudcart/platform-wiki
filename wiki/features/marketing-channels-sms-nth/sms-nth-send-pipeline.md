---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS → Send pipeline"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS NTH send pipeline", "NTH queued send", "NTH retry", "NTH pre-flight checks", "NTH job dispatch"]
tags: [marketing, channels, sms, nth, send, queue]
plan_gates: ["campaign.channel.sms_nth_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# SMS NTH — send pipeline

> Part of [[marketing-channels-sms-nth]]. See the hub for the other aspects (overview, settings, length & billing, DLR webhook).

## Purpose

This aspect documents **how an NTH SMS actually gets sent** — the distinguishing **job-queued (asynchronous)** dispatch, the 5x-retry / 2-second-backoff wrapper, the per-subscriber pre-flight checks, the second-line plan-cap check inside the worker, the internal-title format, and phone-number normalisation.

## Where to find it

This is backend send behaviour, not a screen. It runs whenever a [[marketing-campaigns|campaign]] step of type **"SMS (NTH Message)"** (`sms_nth_message`) executes. The merchant observes its results in the **Logs** modal on the SMS channel card (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`).

## What the merchant can do here

- **Observe send results** in the per-channel Logs modal — each row shows the send outcome (SENT / DELIVERED / ERROR / NOT_SENT) and the NTH-side status.
- **Re-attempt is automatic** — a single subscriber send re-tries up to 5 times before giving up; the merchant doesn't trigger this manually.
- **Send a demo message** from the campaign editor to confirm the pipeline before a real blast.

## Settings & fields

There are no merchant-editable fields specific to the send pipeline — its behaviour is fixed in code. The relevant template-level fields (`internal_title`, `sms_nth_message`) are documented on [[sms-nth-settings]].

## Business rules

### Job-queued dispatch — the distinguishing trait vs MsgHub

Unlike [[marketing-channels-sms-msghub|MsgHub]] (which POSTs to the provider synchronously inside the campaign-action thread), NTH uses an **asynchronous job-queued** approach. The campaign action:

1. validates the subscriber's Phone channel row (see pre-flight below),
2. renders the message text and shortens URLs with `cc_campaign` / `cc_subscriber` / UTM params,
3. dispatches the NTH send job onto the campaigns queue wrapped in `retry(5, ..., 2000)` — **5 attempts, 2-second sleep between attempts**,
4. returns `-1` (the special "job dispatched" marker), which the campaign engine treats as success.

Only the queue worker actually POSTs to NTH. Three consequences:

- The campaign-loop thread is **freed immediately** after queuing — multi-channel campaigns don't stall on a slow NTH response.
- A single subscriber send can re-attempt **5 times** before giving up — temporary NTH outages are absorbed without immediate failure.
- The log row is written by the queue worker (not the campaign action), so a freshly-sent SMS may briefly show **"no log yet"** until the worker picks it up.

### Per-subscriber pre-flight checks

Same as MsgHub — the recipient's Phone channel row must satisfy all of:

- `channel_identifier` non-empty,
- `unsubscribed = 0`,
- `marketing = 1`,
- `verified = 1`,
- `bounced = 0`.

Any failure short-circuits the send and writes a log row with the matching error message.

### Plan-cap pre-flight inside the worker (second-line defence)

The queue worker's `sendMessage` runs `checkConsoleAccessDeniedByPlan` **before** the HTTP call. If the plan-cap was exhausted between the campaign-action dispatch and the worker pickup, the send **aborts inside the worker** — no NTH call is made, the log row records the error, and the channel is **auto-deactivated**. This is a second-line defence beyond the campaign-action's own pre-flight check.

### Phone-number normalisation

Identical to MsgHub: NTH normalises phone numbers via `FILTER_SANITIZE_NUMBER_INT` then strips `+`, `-`, and space characters. A subscriber stored with the `+359` prefix becomes `359` in the outbound request body.

### Internal-title format

The saved internal title becomes `{campaign.title} - {template.internal_title}` (or "N/A" if missing) — used in logs and as NTH-side traceability. The `internal_title` field is mandatory and capped at 191 chars; the actual SMS body (`sms_nth_message`) is required at any length (NTH handles concatenation), but a totally-empty body short-circuits the send. Full validation rules are on [[sms-nth-settings]].

### Worker post-send bookkeeping

After a successful POST, the worker: parses the NTH response, writes the channel-log row with the status mapped from NTH's response (see [[sms-nth-dlr-webhook]]), increments the channel-statistics counter, and dispatches a subscriber-statistic update for the recipient.

## Related

- [[marketing-channels-sms-nth]] — hub.
- [[marketing-channels-sms-msghub]] — the synchronous-send counterpart (contrast).
- [[marketing-campaigns]] — campaigns drive the send pipeline.
- [[marketing-subscribers]] — the Phone channel row that pre-flight checks validate.
- [[notification-delivery]] — outbound delivery concept page.

## Open questions

No outstanding questions.
