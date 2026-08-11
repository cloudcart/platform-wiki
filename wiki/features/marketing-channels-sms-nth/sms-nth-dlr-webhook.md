---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS → DLR webhook"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS NTH DLR", "NTH webhook", "NTH delivery report", "NTH status mapping", "NTH anti-spam policy"]
tags: [marketing, channels, sms, nth, dlr, webhook, status]
plan_gates: ["campaign.channel.sms_nth_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# SMS NTH — DLR webhook & status mapping

> Part of [[marketing-channels-sms-nth]]. See the hub for the other aspects (overview, send pipeline, settings, length & billing).

## Purpose

This aspect documents **how NTH reports delivery back to CloudCart**: the DLR (delivery-report) webhook, its accept/reject conditions, the mapping from NTH's rich status vocabulary to CloudCart's canonical statuses (including the pass-through of unknown values), and the anti-spam policy gate that the merchant must accept before install.

## Where to find it

The DLR webhook is a backend endpoint — NTH posts to the per-store URL (`/web-hook/sms-nth-message?site_id=...`), not a screen. The merchant observes the **resulting statuses** in the **Logs** modal on the SMS channel card under Sidebar → **Marketing** → **Channels** → **Channels setup** (`campaigns-channels`, `/admin/marketing-new/campaigns/channels`). The anti-spam policy prompt appears in the **Install** flow on that same card.

## What the merchant can do here

- **Read per-message delivery status** in the Logs modal — DLR updates flip a row from SENT → DELIVERED / SEEN / EXPIRED / etc. as NTH posts back.
- **Accept the anti-spam policy** during install (a one-time gate).
- The merchant **cannot** configure the webhook URL — it's CloudCart-managed per store.

## Settings & fields

There are no merchant-editable DLR fields. The DLR webhook URL is derived per store (`campaigns.channels.channel.sms_nth_message.webhook?site_id=...`) and passed to NTH as `dlrUrl` in every send request — see [[sms-nth-settings]].

## Business rules

### Webhook accept / reject conditions

The NTH DLR webhook returns **HTTP 400** unless **both** `messageId` AND nested `status.code` are present in the payload. Successful payloads dispatch a `SmsNthWebHookProcess` job (a queue-deferred update of the matching log row's status).

### Status mapping — NTH's rich vocabulary → CloudCart

NTH's status nomenclature is richer than MsgHub's numeric HTTP codes. The channel manager maps:

| NTH status | CloudCart status |
|------------|------------------|
| `PENDING` | (null — keep current status; DOESN'T overwrite — let the next DLR transition update it) |
| `ACCEPTED` | SENT |
| `DELIVERED`, `DELIVRD`, `RECEIVED` | DELIVERED |
| `SEEN` | SEEN |
| `EXPIRED` | EXPIRED |
| `UNDELIVERED`, `UNDELIVERABLE` | UNDELIVERED |
| `REJECTED` | REJECTED |
| `ERROR` | ERROR |
| `USER_BLOCKED` | ABUSE_REPORT |
| (anything else uppercase) | the uppercase status string passes through as-is |
| (null / empty) | NOT_SENT |

These map to the canonical `STATUS_*` constants and surface in the per-channel Logs view.

### Forgiving status handling (vs MsgHub's strict codes)

Beyond the documented mappings, the platform is **deliberately forgiving**:

- `PENDING` returns null — it does **not** overwrite the existing log status, so a transient PENDING never clobbers a real outcome.
- Any **unknown uppercase** value passes through as-is (becomes the new status string), so new NTH statuses are still recorded for forensics even if CloudCart hasn't mapped them.
- Empty / null status → `STATUS_NOT_SENT`.

This more-forgiving approach (vs [[marketing-channels-sms-msghub|MsgHub]]'s strict HTTP-code mapping) means NTH logs can show provider-side codes the platform doesn't formally know about — useful in support cases.

### Anti-spam policy gate

Same as MsgHub — the merchant must accept the [[marketing-campaigns-policy|anti-spam policy]] before installing. SMS opt-out, GDPR consent, and per-country regulations are the **merchant's responsibility**, not CloudCart's. SMS is heavily regulated and the merchant carries full liability for the content and recipient consent.

## Related

- [[marketing-channels-sms-nth]] — hub.
- [[marketing-channels-sms-msghub]] — the strict-HTTP-code counterpart (status-mapping contrast).
- [[marketing-campaigns-policy]] — anti-spam policy required before installation.
- [[settings-hooks]] — webhook concept (the DLR endpoint is a per-store webhook).
- [[notification-delivery]] — outbound delivery concept page.

## Open questions

No outstanding questions.
