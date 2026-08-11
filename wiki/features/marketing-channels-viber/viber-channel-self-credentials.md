---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber → Self-credentials"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber self-credentials", "Self-credentials Viber", "Merchant InfoBip account", "Custom Viber Business sender", "self_credentials_active", "Scenario provisioning"]
tags: [marketing, channels, viber, self-credentials, infobip]
plan_gates: ["viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-viber]]. See the hub for the other aspects (settings, send pipeline, DLR, system messages, plan cap, message format).

# Viber channel — Self-credentials

## Purpose

**Self-credentials** is the path where a merchant with their own InfoBip Viber Business contract plugs their account into CloudCart. When active, every Viber send routes through the merchant's InfoBip pool — InfoBip bills the merchant directly, the CloudCart `viber_messages` plan cap stops applying, and the recipient sees the merchant's own Viber Business sender (not `"CloudCart"`).

This is Viber's distinguishing feature in the channel catalog — Viber is **the only marketing channel that supports merchant-supplied credentials** `(verify)`. SMS, Email, and Web Push do not expose this path.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → **Viber** card → **Settings** button → Branch B of the modal (visible only when `allow_self_credentials = true`). See [[viber-channel-settings]] for the parent modal layout and the metadata flag that decides whether this branch is shown.

## What the merchant can do here

- Activate Self-credentials by toggling `self_credentials.active` on and filling in their InfoBip credentials.
- Override the InfoBip API host (`self_credentials.host`) if they're on a non-default InfoBip cluster.
- Set their own Viber Business sender ID (`self_credentials.from`) — must already be registered with InfoBip / Viber Business.
- Deactivate Self-credentials to fall back to CloudCart's shared pool — the saved credentials are kept in audit storage for later re-activation.

## Settings & fields

The fields are documented in [[viber-channel-settings]] under "Branch B". This page documents what happens **when the merchant saves with `self_credentials.active = true`**.

## Business rules

### Activation calls InfoBip directly

When the merchant saves with `self_credentials.active = true`, the platform:

1. Optionally overrides the InfoBip host from `credentials['host']`.
2. Calls the platform code against the merchant's InfoBip account — InfoBip checks for an existing scenario matching the channel + sender name and reuses it, otherwise creates a new scenario via `POST omni/1/scenarios/`. `(verify — endpoint path is from InfoBip's API; not under CloudCart's control)`
3. Stores the returned **scenario key** alongside the credentials in channel settings.
4. Writes a credentials-type audit row to the application-history log (group `campaigns`, key `campaigns.viber_message`, type `credentials`).

The audit row guarantees CloudCart support can recover merchant-supplied InfoBip credentials even if channel settings are reset.

### Plan-cap is bypassed

When Self-credentials is active, the `viber_messages` plan-feature cap doesn't apply — the remaining-quota display returns `'global.unlimited'` instead of a number. See [[viber-channel-plan-cap]].

### Promo-routing is automatically disabled

The platform's promo-vs-service routing (see [[viber-channel-send-pipeline]]) only kicks in when the current username matches `env('INFOBIP_USERNAME')` (CloudCart's default account). Merchants on Self-credentials have a different username, so the runtime `setUsePromo` check forces `promo = false` — **Self-credentials sends cannot accidentally route through CloudCart's promo channel**.

This means a Self-credentials merchant who sends a Viber with image + button still goes through their own scenario, billed by InfoBip to them. They have to register that scenario as promo-capable directly with InfoBip if InfoBip itself differentiates.

### DLR webhook URL is unchanged

DLRs still come back to CloudCart's per-store DLR endpoint (`/web-hook/viber-message?site_id=...`). The disclaimer banner shown in the modal reminds the merchant to register this webhook with their InfoBip sales rep:

> *"In order to correctly report statistics for sent and read messages, you need to send the following webhook to your sales representative in Infobip: https://hooks.ccdev.info/messages/viber-campaign"*

Without this step, CloudCart never receives delivery / seen status for the merchant's Viber sends — see [[viber-channel-dlr-status]].

### Sender registration is the merchant's responsibility

The `self_credentials.from` sender ID must be **pre-registered** with Viber Business via InfoBip. CloudCart doesn't validate this — it just passes the value to InfoBip on each send. If the sender isn't registered, InfoBip rejects with `REJECTED` and the log row shows the underlying error.

## How it works

Behind the scenes, when Self-credentials is ON, the InfoBip client is instantiated with the merchant's credentials instead of CloudCart's. The send job (`CampaignViberMessageSend`) sees the per-site config layer and routes through `{merchant_host}/omni/1/advanced` with the merchant's scenario key in the JSON body. The bulk-ID convention (`{site_id}_{microtime}`) is preserved, so DLR reconciliation still works. See [[viber-channel-send-pipeline]] for the full pipeline.

The credentials-audit row is written separately from the channel-settings save — it survives even if the channel settings are wiped (e.g., re-installation of the channel).

## Related

- [[marketing-channels-viber]] — hub.
- [[viber-channel-settings]] — the parent settings modal; documents the Branch B fields the merchant fills in.
- [[viber-channel-send-pipeline]] — how the per-message routing picks self-credentials vs CloudCart's account.
- [[viber-channel-plan-cap]] — `viber_messages` plan-feature key is bypassed for Self-credentials.
- [[viber-channel-dlr-status]] — DLR webhook configuration the merchant must register with InfoBip.
- [[marketing-channels-cross-plan-caps]] — cross-channel plan-cap reference (Viber's self-credentials override is unique here).

## Open questions

- Does the saved-credentials audit row survive channel uninstall, or only channel-settings reset? `(verify)`
- What happens if the merchant deactivates Self-credentials while there are in-flight DLRs from their InfoBip account — do those still reconcile correctly? `(verify)`
