---
type: feature
nav_path: "Marketing → Channels → Channels setup → SMS Msg Hub → Overview"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["SMS MsgHub overview", "SMS MsgHub install", "SMS MsgHub channel card", "MsgHub UI surfaces", "MsgHub vs NTH"]
tags: [marketing, channels, sms, msghub, install]
plan_gates: ["campaign.channel.sms_msghub_message"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-sms-msghub]]. See the hub for the other aspects (send pipeline, settings, length & billing, DLR webhook).

# SMS MsgHub — Overview, install & UI surfaces

## Purpose

This aspect covers how the merchant adds, activates, and removes the SMS MsgHub channel, what the channel card actually shows (and what it deliberately leaves out), and how to decide between MsgHub and the alternative SMS provider, NTH.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → the **SMS Msg Hub** channel card. The card's actions open modals over the channels page rather than navigating to separate routes.

Channel mapping key: `sms_msghub_message`. Actions hit the channels API (base `/admin/api/core/marketing/campaigns/channels`): activate/deactivate via `POST /{type}/status`, usage via `GET /{type}/usage`, logs via `/{mapping}/logs-list`, settings via `/{type}/settings`. Install/uninstall is handled through the applications API (`/admin/api/core/applications`).

The channel is **not installed by default** for new stores. After install it's immediately usable — no domain or credentials to set up (the MsgHub contract is shared, see [[sms-msghub-settings]]).

## What the merchant can do here

- **Install** the channel — adds the merchant's site to the MsgHub-enabled channels list. The merchant must accept the [[marketing-campaigns-policy|anti-spam policy]] first.
- **Activate / Deactivate** with the inline toggle after install.
- **Uninstall** — removes the channel and stops new sends through MsgHub.
- **View Usage / Logs** — see [[sms-msghub-length-billing]] and the Logs modal below.

## Settings & fields

### Channel-card UI surface matrix

The SMS MsgHub card has the **least UI surface** of all five marketing channels — no Configuration wizard, no Settings modal, no System Messages list. After install, only **three buttons** appear (**Usage**, **Log**, plus the toggle switch and the Uninstall icon in the header). The Sandbox panel is exposed inline below the action buttons (shared across all channels).

| Surface | Available? | Notes |
|---|---|---|
| Configuration multi-step wizard | NO | Email-only — MsgHub uses shared platform credentials, no merchant-side config. |
| Settings modal | NO | The Vue settings-modal component returns `null` for `sms_msghub_message` — no Settings button on the card. No `unconfirmed_send` toggle, no sender-name edit. |
| System Messages | NO | MsgHub is a **campaign-only** channel — no per-event transactional templates. |
| Reputation | NO | MsgHub doesn't report reputation telemetry back. |
| Usage modal | YES | Shared `MarketingChannelsUsageModal`. Title becomes empty-prefix + date range — see [[marketing-channels-usage]]. |
| Logs modal | YES | Shared `MarketingChannelsLogsModal`. Title falls through to a default empty string for `sms_msghub_message` (not in the explicit title-map switch — minor UI consistency issue). The SMS-row preview uses the mobile-phone-frame component with the body rendered as a chat bubble. |
| Saved Templates | NO | Email-only. |
| Sandbox panel | YES | Inline collapsible card — Webhook post URL input + on/off switch + Submit. See [[sms-msghub-settings]]. |
| Install button | YES | Pre-install state shows "Install" + help text (channel-row `help_text` from the campaign_channels table). |
| Uninstall icon | YES | Header-band trash icon with an "Are you sure? / Uninstall" confirm dialog. |
| Active toggle | YES | Standard switch; deactivation cascades to dependent campaigns (see [[marketing-channels]]). |

## Business rules

### Install confirmation page (legacy the application framework) — shown once

The `Install` route is the only non-shared screen. It first checks the `first_install` setting. If unset, it shows a one-page the application framework confirmation (the platform code view) listing the MsgHub provider terms BEFORE flipping `installed = true`. The merchant must explicitly accept; after confirmation `first_install = true` AND `installed = true` are set together, and the screen redirects back to the Channels list with a success toast.

A subsequent **Uninstall** removes ONLY `installed` (not `first_install`), so re-installing the same channel **skips** the confirmation page.

### When to pick MsgHub vs NTH

The two SMS providers are interchangeable for most merchants. Typical decision factors:

- **MsgHub (Link Mobility)** — proven Bulgarian aggregator, strong DLR coverage, integrated with the Viber Business product on Link Mobility's side (relevant if the merchant also uses Viber — but note the clarification in [[sms-msghub-dlr-webhook]]).
- **NTH Mobile** — alternative Bulgarian aggregator, slightly different pricing and routing. See [[marketing-channels-sms-nth]].

If both channels are installed, the campaign editor lets the merchant pick which to use per step (action type is explicit: `sms_msghub_message` vs `sms_nth_message`). Most stores activate just one. Both share the **Phone** `SubscriberChannel` group, so a subscriber's phone number works with whichever provider the campaign uses.

## Related

- [[marketing-channels-sms-msghub]] — hub.
- [[marketing-channels-sms-nth]] — alternative SMS provider (the MsgHub-vs-NTH choice).
- [[marketing-channels-usage]] — shared Usage modal.
- [[marketing-channels-logs]] — shared Logs modal.
- [[marketing-campaigns-policy]] — anti-spam policy required before install.
- [[marketing-channels]] — parent hub; deactivation-cascade behaviour.

## Open questions

No outstanding questions.
