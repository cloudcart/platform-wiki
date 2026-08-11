---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS Msg Hub → DLR webhook"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS MsgHub DLR", "MsgHub delivery report", "MsgHub webhook", "MsgHub Viber clarification", "MsgHub anti-spam policy"]
tags: [marketing, channels, sms, msghub, dlr, webhook]
plan_gates: ["campaign.channel.sms_msghub_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-sms-msghub]]. See the hub for the other aspects (overview, send pipeline, settings, length & billing).

# SMS MsgHub — DLR webhook, Viber clarification & policy gate

## Purpose

Documents the delivery-report (DLR) webhook that MsgHub calls back to confirm carrier delivery, the rules that decide whether a DLR is accepted, the clarification that the MsgHub Viber service is NOT the marketing-Viber channel, and the anti-spam policy gate that precedes any install.

## Where to find it

The DLR webhook is a server-side endpoint, invisible to the merchant. Its effect is visible in the channel-card **Logs** modal (see [[sms-msghub-overview]]), where a row's status updates from the initial send-time value to the carrier-confirmed value once the DLR arrives. The anti-spam policy gate appears as a checkbox on the Install confirmation page.

## What the merchant can do here

Nothing directly with the webhook — it's MsgHub-to-CloudCart machinery. The merchant must **accept the anti-spam policy** before installing (see Business rules). The DLR result is what the merchant reads in the Logs modal.

## Settings & fields

### The DLR endpoint

MsgHub posts back delivery reports to the per-store webhook (`/web-hook/sms-msghub-message?site_id=...`). The status mapping translates the MsgHub status code into CloudCart's canonical states. The DLR webhook is the **source of truth** for "did the message actually reach the carrier and the phone" — it overwrites the initial HTTP-code-derived status set at send time (see [[sms-msghub-send-pipeline]]).

## Business rules

### DLR webhook requires `sms_id` AND `service_id` to be accepted

The webhook handler returns HTTP 400 unless **both** `sms_id` and `service_id` are present in the inbound payload. If both are present but the matching log row doesn't exist (e.g. the log was deleted, or MsgHub posted late), the webhook silently writes a `HooksLog` row with the raw payload + the captured `site_id` for support inspection — no further processing.

### Webhook does NOT bind by the `site_id` route parameter

The DLR webhook does NOT consume `?site_id=...` from the URL. Instead it looks up the matching log row by `channel = 'sms_msghub_message'` and `message_id = sms_id`, which inherently carries the site_id from the original send. So delivery reports route correctly even when the inbound URL doesn't carry the parameter.

### The MsgHub Viber service is NOT the marketing-Viber channel

The `viber = "LINK Test"` platform config value (see [[sms-msghub-settings]]) refers to the Viber Business sender name on file with Link Mobility for the **MsgHub** combined SMS+Viber service. This is **NOT** the same as the platform's separate `viber_message` marketing channel — that one uses InfoBip (see [[marketing-channels-viber]]).

Merchants who want Viber sends through Link Mobility instead of InfoBip do so via the SMS MsgHub channel, but the campaign-action type still says `sms_msghub_message` and the message is routed as an **SMS** in CloudCart's data model.

### Anti-spam policy gate

The merchant must accept the [[marketing-campaigns-policy|anti-spam policy]] before installing any channel. SMS is **particularly regulated** — the merchant has full liability for SMS spam complaints, GDPR compliance, and any per-country opt-out requirements. The gate is enforced on the Install confirmation page (see [[sms-msghub-overview]]).

## How it works

The DLR webhook handler is a separate listener from the send path. It validates the inbound payload (`sms_id` + `service_id` required), resolves the originating log row by `channel` + `message_id`, and updates that row's status using the MsgHub-status-to-canonical-state mapping. Unmatched-but-valid payloads are parked in `HooksLog` for support. Because the lookup keys carry the site context, the webhook is robust to a missing URL `site_id`.

## Related

- [[marketing-channels-sms-msghub]] — hub.
- [[sms-msghub-send-pipeline]] — the send-time status the DLR later overwrites.
- [[sms-msghub-settings]] — the `callback_url` config + the `viber` platform value clarified here.
- [[marketing-channels-viber]] — the separate InfoBip-based marketing-Viber channel.
- [[marketing-campaigns-policy]] — the anti-spam policy required before install.
- [[settings-hooks]] — webhook / HooksLog concept reference.

## Open questions

No outstanding questions.
