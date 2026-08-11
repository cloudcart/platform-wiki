---
type: feature
nav_path: "Marketing → Channels → Channels setup → Logs"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel logs", "Per-channel logs", "Delivery logs", "Message logs", "Send history", "Channel send log", "Channel delivery history", "Логове на канал", "История на изпращания", "История на съобщенията", "Лог на доставките"]
tags: [marketing, channels, logs, delivery, statistics, history]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-05-23
updated: 2026-06-10
source_count: 3
---

# Channel logs

## Purpose

The **Channel logs** modal is the merchant's per-channel **delivery history** — a paginated table of every outbound message attempt the platform made through a marketing channel, with the recipient, the message content / subject, the campaign or system message that triggered it, the segment the recipient was matched on, the current delivery status, and the timestamp of the last status update.

Each of the five marketing channels (Email, SMS MsgHub, SMS NTH, Viber, Web Push) exposes its own Logs view, opened by clicking **Logs** on the channel card on [[marketing-channels|Channels setup]]. This is where a merchant goes to answer questions like:

- *"Did my Black Friday campaign actually reach subscriber X?"*
- *"Why didn't customer Y get the order-confirmation Viber message?"*
- *"How many of last week's emails bounced?"*
- *"Did the abandoned-cart push notification deliver and was it seen?"*

The modal supports drill-down: click the channel icon on any row to **preview the message** exactly as the recipient saw it, or click the subscriber name to open **Subscriber details** with the recipient's full per-channel membership history.

This topic is split into 6 aspect pages — drill into the aspect that matches the question rather than reading every page.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → click any channel card's **Logs** button. The modal opens over the channel list — it has no route of its own. Parent route is `/admin/marketing-new/campaigns/channels`.

The modal title reflects the channel: *"Email - Logs"*, *"Viber Message - Logs"*, *"Web Push - Logs"*, *"SMS Message - Logs"*.

The parent channels page enforces the [[marketing-campaigns-policy|anti-spam policy]] acceptance gate — a merchant who hasn't accepted the policy is redirected to `/admin/marketing-new/campaigns/policy` before they can see the channels list, including any of its Logs modals.

## What the merchant can do here

- **Browse all delivery attempts** for the channel — one row per (subscriber, send attempt).
- **Filter** by free-text search, status, type (campaign vs system message), segment, campaign, date.
- **Sort** by date (default: newest first).
- **Paginate** — 25 rows per page by default.
- **Preview the message** — see exactly what was sent (rendered HTML for Email; mobile-phone-frame card for SMS / Viber / Web Push). See [[channels-logs-message-preview]].
- **Open subscriber details** — see the recipient's per-channel membership flags, segment memberships, and full message history. See [[channels-logs-subscriber-drilldown]].
- **See the segment / campaign chain** that routed each send.

## What the merchant cannot do

- **Cannot delete log rows.** Logs are append-only.
- **Cannot edit message content from the log.** Preview is read-only — see [[channels-logs-message-preview]].
- **Cannot resend a message from the log.** No per-row *Resend* button.
- **Cannot export to CSV / Excel directly from the modal.** The Logs view is browser-only — the underlying status-statistics export exists on the campaign Statistics page, not on the channel log.
- **No bulk operations** — no "mark all as read", no "delete all bounced".

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[channels-logs-table-view]] — the outer Logs modal: columns shown, filter controls, search semantics, pagination, date-filter behaviour.
- [[channels-logs-status-vocabulary]] — the canonical status enum (`SENT`, `DELIVERED`, `SEEN`, `CLICKED`, `UNDELIVERED`, `ERROR`, `BOUNCED`, `HARD_BOUNCED`, `NOT_SENT`, `UNSUBSCRIBED`, `EXPIRED`, `REJECTED`, etc.), pill colours, per-channel status source (Elastic Email, MsgHub DLR, NTH DLR, InfoBip Viber DLR, browser push ack), the `BOUNCED` ⇒ HARD_BOUNCED auto-union.
- [[channels-logs-message-preview]] — the *Message Preview* sub-modal: HTML iframe (Email) vs mobile-phone-frame card (Viber / SMS / Web Push); delivery timestamp fields; line-break handling.
- [[channels-logs-subscriber-drilldown]] — the *Subscriber details* sub-modal; deleted-subscriber rows; the *"Subscriber does not accept marketing"* warning; per-page batched subscriber existence + `accept_marketing` lookup.
- [[channels-logs-row-lifecycle]] — one row per (subscriber, send attempt); the `status_archive` history; pre-flight `NOT_SENT` failures + their explanations; sandbox sends; retention.
- [[channels-logs-system-vs-campaign]] — the Type vocabulary (campaign vs system message); the compound `system-{channel}` filter key; which channels actually expose system messages; SMS-part count (`messages_send`).

## Settings & fields

The hub itself has no controls — every field, column, filter, and sub-modal lives on one of the aspect pages:

- **Table columns + filters + search + pagination** — see [[channels-logs-table-view]].
- **Status pill + canonical enum + per-channel status source** — see [[channels-logs-status-vocabulary]].
- **Message Preview sub-modal (Email iframe / phone-frame for SMS-Viber-Web Push) + delivery timestamps** — see [[channels-logs-message-preview]].
- **Subscriber details sub-modal + deleted-subscriber rendering + accept_marketing warning** — see [[channels-logs-subscriber-drilldown]].
- **Row lifecycle (status_archive, pre-flight `NOT_SENT`, sandbox, retention)** — see [[channels-logs-row-lifecycle]].
- **Type vocabulary (campaign action vs system message) + SMS-part count (`messages_send`)** — see [[channels-logs-system-vs-campaign]].

## Business rules

Cluster-level rules — each aspect page documents its own rules in detail.

- **One row per (subscriber, send attempt)** — the platform writes one row at dispatch and **updates the same row** as the provider reports back via webhook. The row count equals **unique sends**, not total delivery events. See [[channels-logs-row-lifecycle]].
- **`BOUNCED` filter is a soft + hard union** — filtering by status `BOUNCED` returns both `BOUNCED` AND `HARD_BOUNCED` rows. To see hard bounces only, filter by `HARD_BOUNCED` directly. See [[channels-logs-status-vocabulary]].
- **Pre-flight failures show as `NOT_SENT`** with a merchant-readable error explaining why (unverified subscriber, no marketing consent, unsubscribed, soft-bounced). See [[channels-logs-row-lifecycle]].
- **Sandbox sends are still logged** — when a channel is in sandbox mode, the message is redirected to the merchant's sandbox URL but the log row is written normally (with a `sandbox = 1` flag the merchant doesn't see in the UI).
- **The "Date" column is last-updated, not original send time** — date filters compare against the most recent status change, NOT the dispatch time. See [[channels-logs-table-view]].
- **System-message rows only appear on Viber + Web Push logs** — Email + SMS logs only contain campaign rows. Transactional emails are managed separately via [[marketing-omnichannel-mails-list|Email notifications]]. See [[channels-logs-system-vs-campaign]].
- **Channel-status vocabulary is shared across channels** — a `BOUNCED` row on Email and a `BOUNCED` row on Viber show the same coloured pill via one shared `translateStatus` mapping. See [[channels-logs-status-vocabulary]].

## Related

- [[marketing-channels]] — parent channels hub. Logs is one of the modals reachable from each channel card.
- [[marketing-channels-system-messages]] — System messages modal; system-message sends appear in this log with Type *"System message"*.
- [[marketing-channels-email]] — Email channel reference.
- [[marketing-channels-sms-msghub]] — SMS via MsgHub (Link Mobility).
- [[marketing-channels-sms-nth]] — SMS via NTH Mobile.
- [[marketing-channels-viber]] — Viber Business Messages.
- [[marketing-channels-webpush]] — Web Push channel.
- [[marketing-channels-usage]] — channel send-counter; the per-row `messages_send` value is what counts SMS parts against the cap.
- [[marketing-campaigns]] — campaigns generate most of the rows in this log; the "Campaign" column links each message to its campaign.
- [[marketing-subscribers]] — destination of the Subscriber details drill-down; the per-channel `marketing` / `verified` / `bounced` / `unsubscribed` flags drive the pre-flight check that produces `NOT_SENT` rows.
- [[marketing-campaigns-policy]] — anti-spam policy acceptance gate that precedes any Logs modal opening.
- [[notification-delivery]] — platform-wide outbound delivery concept page.

## Open questions

No outstanding questions.
