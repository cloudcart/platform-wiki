---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber → DLR & status"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber DLR", "Viber delivery report", "Viber status mapping", "InfoBip DLR webhook", "Viber SEEN status", "Cascade-to-prior-pending"]
tags: [marketing, channels, viber, dlr, status, webhook]
plan_gates: ["viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-viber]]. See the hub for the other aspects (settings, self-credentials, send pipeline, system messages, plan cap, message format).

# Viber channel — DLR & status mapping

## Purpose

Documents what happens **after** a Viber send leaves CloudCart. InfoBip posts back delivery reports (DLRs) to a per-store webhook; the platform normalises the InfoBip status vocabulary into CloudCart's, updates the log row, and fires status-change events for downstream stats. Viber's DLR is also the basis for the `message_read` / `message_not_read` campaign-step conditions — Viber is one of only two channels (the other is Email) whose DLR exposes a `SEEN` state.

## Where to find it

The DLR endpoint is server-side (not in the admin UI). The **merchant-visible result** appears on:

- The per-channel **Logs** modal — see [[marketing-channels-logs]].
- The Viber column on the campaign step's statistics drilldown.
- The Campaign branching evaluator (when a step's "wait" condition is `message_read` / `message_not_read`).

The DLR endpoint itself is `/web-hook/viber-message?site_id=...` — InfoBip is configured to POST results to it for CloudCart's shared sender; Self-credentials merchants must register the same URL with their own InfoBip sales rep (see [[viber-channel-self-credentials]]).

## What the merchant can do here

- Read the per-message status on the Logs modal.
- Use `message_read` / `message_not_read` conditions in a campaign step to branch the funnel (see "Conditional branching" below).
- Inspect malformed inbound webhooks — failures get logged so support can investigate.

## Settings & fields

### InfoBip → CloudCart status mapping

| InfoBip status | CloudCart status | Notes |
|---------------|------------------|-------|
| `PENDING` | (null — keep current) | InfoBip hasn't decided yet. |
| `DELIVERED` | `SENT` | Note the rename — InfoBip's `DELIVERED` maps to CloudCart's `SENT`. |
| `SEEN` | `SEEN` | Recipient has opened the Viber message — may never happen. |
| `EXPIRED` | `EXPIRED` | InfoBip gave up trying. |
| `UNDELIVERED` | `UNDELIVERED` | |
| `UNDELIVERABLE` | `UNDELIVERED` | Both InfoBip variants collapse to one CloudCart status. |
| `REJECTED` | `REJECTED` | E.g., sender not registered. |
| (anything else) | `NOT_SENT` | Catch-all for unknown statuses. |

The Viber channel uses the same status-vocabulary table as the other channels — see [[channels-logs-status-vocabulary]] for the cross-channel reference.

### Conditional-branching capabilities

Viber is the **only channel besides Email** that exposes the `message_read` / `message_not_read` campaign-step conditions — because Viber's DLR includes a `SEEN` status. The campaign editor lets the merchant branch the funnel:

> "If recipient saw the Viber → Step A; if they didn't see it → Step B (typically an SMS or Email fallback after a delay)."

The other available conditional, `link_clicked` / `link_not_clicked`, requires the message body to contain at least one URL. The platform shortens URLs and instruments them with click-tracking attribution params (`utm_medium=viber`) before send — see [[viber-channel-send-pipeline]].

## Business rules

### DLR webhook receives bulk results

The endpoint accepts an inbound `results[]` array — InfoBip can batch DLR posts. The controller iterates `array_map` over each result, normalises the payload via `statusResultTransform`, and dispatches one `CampaignViberMessageWebHookProcess` job per result.

### Malformed webhooks return HTTP 400

Bad-shape webhooks (no `results` array) get logged as a `HooksLog` row for support inspection and return HTTP 400. The merchant doesn't see this directly — it's a support troubleshooting artifact.

### Status update has cascade-to-prior-pending behavior

When a Viber log status changes (e.g., `DELIVERED` arrives → log is marked `SENT` on CloudCart's side), the platform looks for **other** logs with the same `(site_id, channel, channel_identifier)` whose `created_at <= this.created_at` AND status is null (for incoming `SENT`) OR status is null OR `SENT` (for incoming `DELIVERED` / `SEEN`). All matching prior pending logs get updated to the new status, with separate `ViberMessageStatusChange` events fired for each.

**Merchant-visible effect**: this catches the case where an earlier message's DLR was lost — the new DLR retroactively marks the older message as delivered too. The Usage / Logs screens then show consistent delivered-counts.

### `SEEN` requires the recipient to open the message

The actual `SEEN` state requires the recipient to open the Viber message — which they may never do. A high `DELIVERED → SEEN` conversion typically means the message is interesting enough that the customer tapped the notification. A low conversion is normal for transactional sends.

### Sandbox testing

Like other channels, `sandbox_status = true` + `sandbox_url` redirects Viber sends to a webhook URL for inspection. Useful for verifying the rendered message body, image URL, button URL, and attribution params. See [[marketing-channels-cross-sandbox]] for the cross-channel sandbox pattern.

## How it works

InfoBip posts DLR batches to `/web-hook/viber-message?site_id=...`. The controller validates the shape, normalises each result row, then queues a per-result processing job. The processing job:

1. Looks up the originating log row by InfoBip's `messageId`.
2. Maps the InfoBip status through the table above.
3. Updates the log row's status.
4. Fires a `ViberMessageStatusChange` event so downstream listeners (campaign-step branching, statistics aggregation, system-message counter increments) can react.
5. Runs the cascade-to-prior-pending sweep for older pending logs on the same `(site_id, channel, channel_identifier)`.

System-message counters increment on this path: each Viber system message tracks its `sent_count`, incremented when a DLR moves the log to `DELIVERED`, `SENT`, `SEEN`, or `CLICKED`. See [[viber-channel-system-messages]].

## Related

- [[marketing-channels-viber]] — hub.
- [[viber-channel-send-pipeline]] — the outbound path that creates the log row this DLR updates.
- [[viber-channel-system-messages]] — system-message `sent_count` increments on DLR events.
- [[viber-channel-self-credentials]] — Self-credentials merchants must register the DLR URL with their InfoBip sales rep.
- [[channels-logs-status-vocabulary]] — cross-channel reference for the status table above.
- [[marketing-channels-logs]] — Logs modal where the merchant sees per-message status.
- [[marketing-channels-cross-sandbox]] — cross-channel sandbox testing pattern.

## Open questions

- Confirm the exact event name fired on Viber DLR (the wiki rule forbids quoting class names; the merchant-visible side-effect is what matters here).
- How long does InfoBip retry DLR posts before giving up? `(verify)`
