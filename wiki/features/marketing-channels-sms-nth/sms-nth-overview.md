---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS → Overview"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS NTH overview", "SMS NTH card", "SMS NTH UI surfaces", "NTH vs MsgHub", "SMS NTH install"]
tags: [marketing, channels, sms, nth, lifecycle, ui]
plan_gates: ["campaign.channel.sms_nth_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# SMS NTH — overview & lifecycle

> Part of [[marketing-channels-sms-nth]]. See the hub for the other aspects (send pipeline, settings, length & billing, DLR webhook).

## Purpose

This aspect covers the **channel-card UI surface** of SMS NTH — what the merchant clicks to install / activate / uninstall, which modals exist and which are deliberately absent, where NTH SMS message content is actually edited, and the **MsgHub-vs-NTH decision** that helps a merchant pick between the two SMS providers.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (`campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → the **SMS** channel card. All actions open as modals over the channels page; there are no separate routes.

## What the merchant can do here

- **Install** the channel — adds the merchant's site to the NTH-enabled channels list for this store. First install shows a confirmation the application framework view (the platform code).
- **Activate / Deactivate** after install.
- **Uninstall** — removes the channel and stops any new sends through NTH. Re-install skips the confirmation (see `first_install` note below).
- **View Usage** — sent-count vs plan cap.
- **View Logs** — per-message delivery status (destination, body, NTH status code, send time, DLR updates).
- **Use this channel in a campaign step** — the campaign editor offers action type **"SMS (NTH Message)"** (`sms_nth_message`).
- **Send a demo message** to a test number from the campaign editor before launching.

## Settings & fields

### Channel-card UI surface matrix

The SMS NTH card has the same minimal UI as [[marketing-channels-sms-msghub|SMS MsgHub]] — **no Configuration wizard, no Settings modal, no System Messages list**. Only Usage and Logs surface as in-page modals; the inline Sandbox panel renders on the card itself.

| Surface | Available? | Notes |
|---|---|---|
| Configuration wizard | NO | Email-only feature. |
| Settings modal | NO | The Vue settings-modal component returns `null` for the `sms_nth_message` mapping. |
| System Messages | NO | Campaign-only channel. |
| Reputation | NO | NTH doesn't feed reputation back. |
| Usage modal | YES | Title becomes *"SMS Message Usage - {date_start} - {date_end}"* (NTH IS in the explicit title-map switch, unlike MsgHub which falls through to an empty prefix). |
| Logs modal | YES | Title *"SMS Message - Logs"*. The Logs preview uses the mobile-phone-frame component (`MarketingChannelMobilePhonePreview`) rendering the SMS body as a chat bubble; `\r\n` and `\n` line breaks are converted to `<br/>` for display. |
| Saved Templates | NO | Email-only. |
| Sandbox panel | YES | Inline collapsible card with Webhook post URL + on/off + Submit. |
| Install / Uninstall / Active toggle | YES | Same lifecycle as MsgHub. |

### Install-confirmation gate + first_install

Initial install shows the confirmation view (the platform code); after confirmation the channel goes `installed = 1` + `first_install = 1` in one shot. A subsequent uninstall preserves `first_install`, so re-install **skips** the confirmation and immediately turns the channel back on.

### Where the merchant edits NTH SMS message content

NTH SMS templates aren't editable through a per-channel Settings modal — the merchant edits them inside the **campaign editor** (when adding an "SMS (NTH Message)" action to a [[marketing-campaigns|campaign]]). The campaign-action editor uses the `MarketingChannelsSystemMessagesConfiguration` component (with `showCampaignFields = true` and `isCampaign = true`), which surfaces:

- an **Internal title** input (required, max 191 chars — the merchant's reference label, not sent);
- a variable-aware pill editor for the SMS body (with Add-variable dropdown + Write-with-AI button);
- a live character + SMS-part counter (see [[sms-nth-length-billing]]);
- a warning note: *"The calculated message length is approximate. When using variables, the actual length may vary significantly."*

## Business rules

### When to pick MsgHub vs NTH

| Factor | MsgHub | NTH |
|--------|--------|-----|
| Send dispatch | Synchronous (inline) | Queued (asynchronous) — see [[sms-nth-send-pipeline]] |
| Provider | Link Mobility / MsgHub Bulgaria | NTH Mobile |
| Sender ID | "LINK Test" / from MsgHub config | "CloudCart" |
| DLR status vocabulary | Numeric HTTP codes (200, 202, 4xx, 5xx) | Rich text states (ACCEPTED, DELIVERED, EXPIRED, etc.) — see [[sms-nth-dlr-webhook]] |
| Authentication | x-api-key + HMAC-SHA512 sign | HTTP Basic Auth |
| Sandbox | Supports sandbox URL | Supports sandbox URL |

Most merchants pick one and stick with it. The decision is usually driven by:

- **Existing relationships** — merchants with a prior Link Mobility account often prefer MsgHub for consistency.
- **DLR coverage** — NTH's richer status vocabulary gives more granular per-send insight.
- **Reliability** — having both channels installed lets the merchant manually swap providers if one has an outage (there is **no automatic failover** — the merchant must edit each campaign).

### site_id 402 send-count carve-out

The channel's `count` override returns `0` for `site_id = 402` when not on the channel usage route — a legacy internal exclusion (likely a test/staging store) that doesn't affect merchant-facing accounting on real stores. Mentioned only for completeness; not merchant-visible behaviour.

## Related

- [[marketing-channels-sms-nth]] — hub.
- [[marketing-channels-sms-msghub]] — the other SMS provider (same minimal card UI).
- [[marketing-campaigns]] — where NTH SMS message content is edited.
- [[marketing-campaigns-policy]] — anti-spam policy required before installation.
- [[marketing-channels]] — parent hub (all marketing channels).

## Open questions

No outstanding questions.
