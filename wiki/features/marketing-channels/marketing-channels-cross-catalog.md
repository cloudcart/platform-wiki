---
type: feature
nav_path: "Marketing → Channels → Channels setup → Channel catalog"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel catalog", "Channel mapping table", "Channel registry", "Каталог канали", "Списък канали"]
tags: [marketing, channels, campaigns, catalog, mapping]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (lifecycle, suspension, plan caps, sandbox, magic vars, UI surfaces).

# Channels — channel catalog

## Purpose

The five active outbound marketing channels on every store, the verbatim mapping keys the rest of the platform uses to address them, the per-channel state fields the merchant sees on the Channels setup card, and the channel-specific "from" identity. The mapping keys are the single source of truth across campaign actions, subscriber-channel rows, routes, logs, and the plan-feature gating layer.

## Where to find it

Sidebar → **Marketing** → **Channels** (dropdown) → **Channels setup**. The catalog is the list of cards rendered on this page; one card per channel.

## What the merchant can do here

- Read the channel name, provider, and per-channel sender identity.
- Read the plan-feature key that gates this channel's send volume (used by [[marketing-channels-cross-plan-caps]]).
- Identify which channel a campaign action targets by its `mapping` key.

## Settings & fields

### The five active marketing channels

| Mapping | Name | Group | Subscriber channel | Provider | Plan-gate feature key |
|---------|------|-------|--------------------|----------|----------------------|
| `email` | Email | `email` | `Email` | Elastic Email (CloudCart-managed sub-account per store) | `campaign.channel.email` |
| `sms_msghub_message` | SMS Msg Hub | `phone` | `Phone` | Link Mobility / MsgHub Bulgaria | `campaign.channel.sms_msghub_message` |
| `sms_nth_message` | SMS | `phone` | `Phone` | NTH Mobile | `campaign.channel.sms_nth_message` |
| `viber_message` | Viber | `phone` | `Phone` | InfoBip Viber Business Messages | `viber_messages` |
| `web_push` | Web Push | `web_push` | `WebPush` | Browser native (VAPID) | `campaign.channel.web_push` |

The `mapping` column is the **key** used everywhere — in campaign action types, in [[marketing-subscribers#Channels - Email, Phone, Messenger, WebPush|SubscriberChannel]] rows, in routes, in logs, and in the plan-feature lookup. The merchant rarely sees these keys directly — they are surfaced through the channel cards' display name.

The catalog itself lives in a global table read by every store; merchants do not add new channel TYPES, only configure which of the five they want active. Other channels (Messenger, Voice) exist in the catalog but are disabled (`status = 0`) — they do NOT show on the Channels setup page.

### Per-channel state fields (visible on each card)

| Field | Source | Meaning |
|-------|--------|---------|
| `installed` | per-channel setting | Provider account / credentials set up. Required before activating. |
| `active` | per-channel setting | Merchant has toggled the channel ON — campaign actions can target it. |
| `configured` | per-channel setting (Email) | The full multi-step setup is complete (profile + domain + DKIM + sender). |
| `verify` | per-channel setting (Email) | Sender domain DNS records (SPF, DKIM, Tracking CNAME, DMARC) have been verified. |
| `suspended_by` | per-channel setting | If non-null, the channel is auto-suspended by reputation / spam / bounce / open thresholds OR by a CloudCart employee — see [[marketing-channels-cross-suspension]]. |
| `banned_reason` / `clear_banned_reason` | computed | Merchant-visible label explaining why a campaign using this channel is broken. |

### Sender identity per channel

The "from" semantics differ per channel — the merchant doesn't pick this per campaign for SMS / Viber. It is the channel-wide sender ID set during channel setup.

| Channel | Sender identity | Verified how |
|---------|-----------------|--------------|
| Email | Email address on a domain the merchant owns | DNS records (SPF, DKIM, Tracking CNAME, DMARC) |
| SMS MsgHub | `LINK Test` short code / alphanumeric (per Link Mobility / MsgHub contract) | MsgHub side; CloudCart-shared sender |
| SMS NTH | `CloudCart` alphanumeric sender | NTH side; CloudCart-shared sender |
| Viber | `CloudCart` Viber Business sender ID (or merchant's own when self-credentials active) | InfoBip + Viber business registration |
| Web Push | Domain origin (the storefront URL the customer subscribed from) | Browser-enforced via VAPID public key |

For Email the sender is the merchant's verified domain's mailbox. For Web Push the browser binds the subscription to the storefront origin — a subscription taken at one domain cannot be re-used for another. SMS NTH and SMS MsgHub do **not** currently expose merchant-supplied sender IDs in the UI — sends go through CloudCart's shared sender. See [[marketing-channels-cross-plan-caps]] for how self-credentials change this for Viber.

## Business rules

### Caching of the channel registry

The catalog read is cached under `campaign.active.channels` for **1 day**. The cache is busted whenever a row in the global channel table is updated. Newly-released channels won't appear on the Channels setup page until the cache flushes or a channel row is touched (verify).

### Three "skip" mappings that look like channels but aren't

The merchant may see action types named `set_customer_group`, `set_tags`, and `remove_tags` referenced in a campaign builder. These are NOT channels — they are campaign-action helpers that mutate the subscriber's state. The Channels setup page filters them out of the card list.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-lifecycle]] — how an entry in this catalog progresses dormant → installed → active.
- [[marketing-channels-cross-plan-caps]] — how each `plan_feature_key` in the catalog gates send volume.
- [[marketing-channels-email]] — Email channel configuration deep-dive.
- [[marketing-channels-sms-msghub]] — SMS MsgHub channel.
- [[marketing-channels-sms-nth]] — SMS NTH channel.
- [[marketing-channels-viber]] — Viber channel.
- [[marketing-channels-webpush]] — Web Push channel.
- [[marketing-subscribers]] — `SubscriberChannel` rows referenced by the `Subscriber channel` column.
- [[plan-gates]] — feature-key system the channels plug into.

## Open questions

None.
