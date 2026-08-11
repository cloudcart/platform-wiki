---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS → Settings"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS NTH settings", "NTH config", "NTH request shape", "NTH Basic Auth", "NTH validation rules", "NTH sandbox"]
tags: [marketing, channels, sms, nth, settings, config]
plan_gates: ["campaign.channel.sms_nth_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# SMS NTH — settings & configuration

> Part of [[marketing-channels-sms-nth]]. See the hub for the other aspects (overview, send pipeline, length & billing, DLR webhook).

## Purpose

This aspect documents the **configuration** behind SMS NTH: the platform-level (CloudCart-managed) config, the `/v1/omni-channel/message` send-request shape, the HTTP Basic Auth scheme, the limited per-merchant settings, the message validation rules, and sandbox testing.

## Where to find it

Platform-level config lives in the platform code (env-driven) and is **not merchant-visible**. The per-merchant settings (install / active / sandbox) live on the **SMS** channel card under Sidebar → **Marketing** → **Channels** → **Channels setup** (`campaigns-channels`, `/admin/marketing-new/campaigns/channels`). There is **no** per-channel Settings modal — see the UI-surface matrix on [[sms-nth-overview]].

## What the merchant can do here

- **Toggle sandbox mode** via the inline Sandbox panel on the card (set `sandbox_url` + on/off + Submit).
- **Install / Activate** (sets `installed` / `active`) — see [[sms-nth-overview]].
- The merchant **cannot** edit host, port, credentials, or the sender ID — those are CloudCart-managed.

## Settings & fields

### Platform-level configuration (the platform code, env-driven)

| Setting | Source | Notes |
|---------|--------|-------|
| `host` | `env('SMSNTH_HOST')` | NTH's omni-channel API host (developers.nth.ch). |
| `port` | `env('SMSNTH_PORT')` | API port (NTH uses a non-standard port). |
| `encoding` | `env('SMSNTH_ENCODING')` | Character encoding for the SMS body. |
| `system_type` | `env('SMSNTH_SYSTEM_TYPE')` | NTH-side account type. |
| `username` | `env('SMSNTH_USERNAME')` | CloudCart's NTH account login. |
| `password` | `env('SMSNTH_PASSWORD')` | CloudCart's NTH account password. |
| `sender` | `"CloudCart"` | Alphanumeric sender ID — hard-coded (NOT env-driven). What the recipient sees in the SMS "From". |

All values are CloudCart-managed; merchants don't see or edit them. The `sender` value is **hard-coded** to `'CloudCart'` in the platform code — the merchant cannot override it; every NTH SMS goes out with sender "CloudCart".

### Send request shape

Each SMS goes out as a POST to `{host}:{port}/v1/omni-channel/message` with this JSON body:

```
{
  "channels": ["SMS"],
  "messagePriority": "NORMAL",
  "dlr": true,
  "dlrUrl": "<per-store DLR webhook URL>",
  "destinations": [
    { "phoneNumber": "<E.164>" }
  ],
  "sms": {
    "sender": "CloudCart",
    "text": "<rendered message body>"
  }
}
```

The base URL combines `host` + `:port`. The `dlrUrl` is the per-store webhook for delivery reports (`campaigns.channels.channel.sms_nth_message.webhook?site_id=...`) — see [[sms-nth-dlr-webhook]]. NTH's response includes a `resultDescription` field that must be `"OK"` to proceed — anything else raises an NTH exception.

### Authentication — plain HTTP Basic (not signed)

Unlike [[marketing-channels-sms-msghub|MsgHub]] (which signs with HMAC-SHA512), NTH uses **plain HTTP Basic Auth** with the platform-level `username` + `password`. The request carries an `Authorization: Basic base64(user:pass)` header.

### Per-merchant settings on the channel

| Setting | Default | Effect |
|---------|---------|--------|
| `installed` | `false` | Set TRUE after the merchant clicks Install. |
| `active` | `false` | Set TRUE after the merchant toggles the channel on. |
| `sandbox_status` | `false` | When TRUE, redirects sends to `sandbox_url` instead of NTH. |
| `sandbox_url` | null | Webhook URL for sandbox-mode message inspection. |

No domain selection, no sender-email picker — installation is one click.

### Message validation rules

| Field | Validation |
|-------|------------|
| `internal_title` | `required\|string\|max:191` |
| `sms_nth_message` | `required\|string` (the rendered SMS body itself) |

The validator rejects template saves missing or over 191 chars on `internal_title` (used only as the merchant's reference label, never sent to NTH). The SMS body is required at any length.

## Business rules

### Channel configuration constants

- Channel ID: `sms_nth_message`.
- Group: `phone`.
- Subscriber channel: Phone.
- UTM medium: `sms`.
- Both `installed` and `active` gates apply before the channel can send.

### Sandbox testing

`sandbox_status = true` redirects sends to the merchant's chosen `sandbox_url` instead of NTH. The merchant inspects message body, attribution metadata, and target phone number **without spending credits**. This is the safe way to validate placeholder rendering before a real blast.

## Related

- [[marketing-channels-sms-nth]] — hub.
- [[marketing-channels-sms-msghub]] — the HMAC-signed counterpart (auth contrast).
- [[marketing-campaigns]] — where the validated message template is authored.
- [[settings-hooks]] — webhook concept (the `dlrUrl` is a per-store DLR webhook).
- [[channel]] — Channel entity reference.

## Open questions

No outstanding questions.
