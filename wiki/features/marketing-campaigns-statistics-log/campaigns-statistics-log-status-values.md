---
type: feature
nav_path: "Marketing → Campaigns → Statistics → Log → Status values"
route_name: admin.api.campaigns.statistics.logs
route_path: /admin/api/core/marketing/campaigns/{campaign}/statistics/{action}/logs
aliases: ["Campaign log status enum", "SENT DELIVERED SEEN CLICKED", "BOUNCED HARD_BOUNCED", "Status pill colour-coding", "Channel status catalogue"]
tags: [marketing, campaigns, statistics, logs, statuses]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-statistics-log]]. See the hub for the other aspects (surfaces, status archive, filters & table, view-message, side-effects, Email mapping, storage).

# Per-send log — status values

## Purpose

Every row in the per-send delivery log carries a **status** — the current state of the send attempt. The status drives both the table display (colour-coded pill) and the Status filter (multi-select). This page documents the full set of 20 status values, what each one means, which channels can produce it, and the colour coding the merchant sees. It is also the catalogue the merchant uses when interpreting the status pill or building filters to investigate specific delivery problems.

## Where to find it

Status values are visible everywhere the log is — on each row of the [[campaigns-statistics-log-filters-table|log table]] (colour-coded pill in the Status column) and inside the Status multi-select on the filter bar. The full per-row transition timeline (hover the pill) is on [[campaigns-statistics-log-status-archive]].

## What the merchant can do here

This page is a reference catalogue — no merchant actions specific to "the status values" themselves. What the merchant DOES with the statuses:

- **Filter** by status to narrow the log (e.g., select BOUNCED to find every failed delivery).
- **Read the pill** to know a row's current state at a glance via colour.
- **Hover the pill** to see the full transition history via [[campaigns-statistics-log-status-archive]].

## Settings & fields

The complete set of status values channels can record:

| Status | Meaning | Channel coverage |
|--------|---------|------------------|
| `SENT` | The platform handed the message to the provider successfully. | All |
| `DELIVERED` | The provider confirmed delivery to the recipient's inbox / handset / device. | Email (via Elastic Email webhook), SMS (provider DLR), Viber, Web Push (FCM/APNs ack). |
| `SEEN` | The recipient opened the message. | Email (tracking pixel), Viber (read receipt), Web Push (interaction). |
| `CLICKED` | The recipient clicked a tracked link in the message. | Email, SMS (short-URL click), Viber. |
| `UNDELIVERED` | The provider rejected delivery (transient — could be temporary). | Email, SMS, Viber, Web Push. |
| `NOT_SENT` | The platform decided not to send (e.g., subscriber unsubscribed at the last second). | All. |
| `ERROR` | An exception thrown during send. | All. |
| `BOUNCED` | Soft bounce — server temporarily rejected. | Email mostly. |
| `HARD_BOUNCED` | Hard bounce — address is permanently invalid. | Email mostly. |
| `UNSUBSCRIBED` | The recipient unsubscribed from this message (clicked unsubscribe link). | All. |
| `ABUSE_REPORT` | The recipient marked the message as spam. | Email mostly. |
| `EXPIRED` | The message's delivery window expired (some providers age out queued sends). | Viber, Web Push. |
| `REJECTED` | The provider rejected the send pre-flight (e.g., invalid format). | All. |
| `UNDELIVERABLE` | A definitive non-deliverable state. | All. |
| `ACCEPTED` | The provider accepted the send but hasn't confirmed delivery. | All. |
| `COMPLETED` | Final terminal state (used by some channels). | Channel-dependent. |
| `PENDING` | Waiting for a status update from the provider. | All. |
| `PURCHASE` | Synthetic status — a recipient placed an order attributed to this send. | All. |
| `CREATED` | The log row was created but no status assigned yet. | All. |

## Business rules

- **Colour coding is by severity, not by name.** Typically green for SEEN / CLICKED / PURCHASE; yellow for SENT / DELIVERED / PENDING; red for BOUNCED / HARD_BOUNCED / ERROR / REJECTED / UNDELIVERABLE; grey for NOT_SENT / EXPIRED / UNSUBSCRIBED. (verify exact colour mapping per status.)
- **`PURCHASE` is synthetic — not a delivery state.** It's appended when the platform attributes a purchase to a send. The recipient still has a separate delivery status (SENT / DELIVERED / SEEN / CLICKED) in `status_archive`. PURCHASE is the terminal "this send made money" signal. See [[campaigns-statistics-log-status-archive]] for how it appears in the timeline.
- **`CREATED` should rarely appear in the merchant view.** It's the brief state between row insertion and the send attempt. Any log stuck in CREATED indicates a queue failure — the send job that should have transitioned it to SENT / NOT_SENT never ran.
- **`BOUNCED` and `HARD_BOUNCED` are different.** Soft bounce = temporary server rejection (e.g., mailbox full); hard bounce = permanent (mailbox doesn't exist). Only hard bounces propagate to the subscriber's channel as `bounced=1` — see [[campaigns-statistics-log-side-effects]]. Filtering by "Bounced" auto-includes hard bounces — see [[campaigns-statistics-log-email-mapping]].
- **`PENDING` is the "no answer yet" state.** Used when the platform has handed off but the provider hasn't returned a DLR / webhook yet. Most messages move out of PENDING within seconds; if a row sits in PENDING for hours, the provider's webhook is delayed or failed.
- **`ACCEPTED` vs `SENT`.** Subtle distinction — ACCEPTED means the provider has the message but hasn't tried to deliver it (queued at the provider); SENT means the platform handed it to the provider. Some channels skip ACCEPTED entirely and move SENT → DELIVERED.
- **`NOT_SENT` carries a reason on the action-log.** When the platform decides not to send (the subscriber unsubscribed, the segment-membership check failed, the channel verification turned off), the corresponding action-log row carries the reason key. The log status itself is just NOT_SENT — the reason is in the parallel campaign-action-log surface.

## How it works

Each log row's `status` field holds the current state. When provider webhooks arrive, the channel-specific status mapping converts the provider's status string into one of the canonical values above and updates the row. See [[campaigns-statistics-log-email-mapping]] for the Email-channel-specific mapping table (Elastic Email's status strings → platform statuses).

Status transitions are recorded in `status_archive` — see [[campaigns-statistics-log-status-archive]] for the timeline format and the idempotency rule that protects against stale Sent webhooks arriving after SEEN / CLICKED.

Some statuses trigger downstream side-effects on the subscriber's channel — auto-bounce, auto-unsubscribe, auto-verify. See [[campaigns-statistics-log-side-effects]].

## Related

- [[marketing-campaigns-statistics-log]] — hub.
- [[campaigns-statistics-log-status-archive]] — the per-row transition history (when each status was set).
- [[campaigns-statistics-log-email-mapping]] — Elastic Email's provider statuses → platform statuses.
- [[campaigns-statistics-log-side-effects]] — which statuses trigger auto-bounce / auto-unsubscribe / auto-verify.
- [[campaigns-statistics-log-filters-table]] — the Status multi-select filter.
- [[marketing-channels]] — channel-level logs share the same status vocabulary.

## Open questions

- Verify the exact colour-pill mapping per status against the latest UI.
