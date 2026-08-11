---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS Msg Hub → Settings & config"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS MsgHub settings", "MsgHub platform config", "MsgHub send request shape", "MsgHub credentials", "MsgHub sandbox"]
tags: [marketing, channels, sms, msghub, settings, config]
plan_gates: ["campaign.channel.sms_msghub_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-sms-msghub]]. See the hub for the other aspects (overview, send pipeline, length & billing, DLR webhook).

# SMS MsgHub — Settings & configuration

## Purpose

Documents the configuration behind the SMS MsgHub channel: the platform-level config CloudCart manages on the merchant's behalf, the request shape and HMAC signing of each send, the small set of per-merchant settings, and how sandbox testing works without spending real credits.

## Where to find it

There is **no Settings modal** for this channel (the Vue settings component returns `null` for `sms_msghub_message` — see the UI matrix on [[sms-msghub-overview]]). The only merchant-touchable configuration is the inline **Sandbox** panel on the channel card. Everything else is platform-managed and invisible to the merchant.

## What the merchant can do here

- Toggle **Sandbox** mode and set the **Webhook post URL** (inline panel on the card).
- Nothing else — no domain, no DNS, no sender-email selection, no credentials. One-click Install (see [[sms-msghub-overview]]) gets the merchant from zero to usable because the platform's MsgHub contract is shared.

## Settings & fields

### Platform-level configuration

Set globally on CloudCart's behalf — the merchant doesn't see or edit these:

| Setting | Value | Notes |
|---------|-------|-------|
| `id` | `1266` | MsgHub service ID for the CloudCart contract. |
| `sc` | `1917` | Sender short code (alphanumeric label "CloudCart"). |
| `api_key` | bcrypt-hashed | Authenticates requests via the MsgHub `x-api-key` header. |
| `api_secret` | bcrypt-hashed | Used to sign every request body with `HMAC-SHA512` in the `x-api-sign` header. |
| `viber` | `"LINK Test"` | Viber Business name on file with Link Mobility for the combined MsgHub-Viber service (see [[sms-msghub-dlr-webhook]] for why this is NOT the marketing-Viber channel). |
| `url_sandbox` | `https://api-test.msghub.cloud/` | Test environment endpoint. |
| `url_production` | `https://api.msghub.cloud/` | Production endpoint. |

### Send request shape

Each SMS goes out as a POST to `{base}/send` with JSON body:

```
{
  "msisdn": "<E.164 phone>",
  "sc": "1917",
  "text": "<message body>",
  "service_id": 1266,
  "callback_url": "<store-specific DLR webhook>"
}
```

Headers: `x-api-key`, `x-api-sign` (`HMAC-SHA512(body, api_secret)`), `Content-Type: application/json`.

The `callback_url` is the per-store delivery-report webhook (`campaigns.channels.channel.sms_msghub_message.webhook?site_id=...`) — MsgHub calls this back with status updates, which the platform records on the matching log row. See [[sms-msghub-dlr-webhook]].

### Per-merchant settings on the channel

| Setting | Default | Effect |
|---------|---------|--------|
| `installed` | `false` | Set to TRUE after the merchant clicks Install. |
| `active` | `false` | Set to TRUE after the merchant toggles the channel on. |
| `sandbox_status` | `false` | When TRUE, sends are mirrored to `sandbox_url` instead of going to MsgHub. |
| `sandbox_url` | null | Webhook URL for sandbox-mode message inspection. |
| `first_install` | (unset) | Set TRUE on first install; controls the one-time confirmation page — see [[sms-msghub-overview]]. |

## Business rules

### Credentials are bcrypt-hashed in the config file

The `api_key` and `api_secret` values are stored as **bcrypt hashes** (`$2y$10$...`) — that's what gets passed to the HTTP request directly. The MsgHub API authenticates by hashing the inbound `x-api-key` against the stored hash on their side, and verifies `x-api-sign = hash_hmac('sha512', body_json, api_secret_hash)`. The merchant **cannot view or modify** these — they're CloudCart-managed at the platform level.

### Sandbox URL is the base in non-prod environments

The client uses the sandbox URL (`https://api-test.msghub.cloud/`) in non-production environments and the production URL otherwise — independent of the per-channel `sandbox_status` flag. If the response status code is outside 2xx, the client throws a MsgHub exception carrying the response code (consumed by the send pipeline — see [[sms-msghub-send-pipeline]]).

### Sandbox testing redirects sends to a webhook

Toggling `sandbox_status = true` and setting `sandbox_url` to a webhook URL (e.g. a webhook.site testing URL) redirects every send to that URL instead of MsgHub. The merchant can inspect the rendered SMS body, the message hash, and the campaign-attribution metadata without spending real credits.

## Related

- [[marketing-channels-sms-msghub]] — hub.
- [[sms-msghub-send-pipeline]] — how the request is built, signed, and POSTed; status mapping.
- [[sms-msghub-dlr-webhook]] — the `callback_url` delivery-report endpoint; Viber-service clarification.
- [[sms-msghub-overview]] — install flow + why there's no Settings modal.

## Open questions

No outstanding questions.
