---
type: feature
nav_path: "Marketing → Channels → Channels setup → Email → Settings"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Email channel settings modal", "Sending emails to unverified subscribers", "unconfirmed_send", "Email channel unverified send", "Изпращане на имейли към непотвърдени абонати"]
tags: [marketing, channels, email, settings, unverified, unconfirmed-send]
plan_gates: ["campaign.channel.email"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-email]]. See the hub for the other aspects (setup wizard, DNS records, Elastic Email sub-account, webhook feedback, send pipeline, suspend thresholds).

# Email channel — Settings pane

## Purpose

The **Settings - Email** modal (`MarketingChannelsSettingsModalEmail`) exposes a single, per-Email-channel switch: *"Sending emails to unverified subscribers"* (`unconfirmed_send`). This is the merchant's deliberate choice to trade verification quality (subscriber confirmed their email) for reach (every subscriber gets the campaign). The setting affects the per-recipient pre-flight check in the send pipeline ([[email-channel-send-pipeline]]).

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** → **Email** channel card → **Settings** (sliders icon). Title — *"Settings - Email"*. The modal contains a single `CcCard` with one switch.

This is **separate** from the Configuration wizard ([[email-channel-setup-wizard]]). The Configuration modal (cog icon) and the Settings modal (sliders icon) are distinct buttons on the Email card's Actions band.

## What the merchant can do here

- Toggle **Sending emails to unverified subscribers** (`unconfirmed_send`) — default OFF.
- Save the change — persists immediately on click. Toast: *"Saved successfully"* + modal closes.

## Settings & fields

### The single switch

| Setting | Default | Effect when ON | Effect when OFF |
|---|---|---|---|
| `unconfirmed_send` | `false` (OFF) | Campaign emails are sent even to subscribers whose `single_channel.verified = 0`. | Unverified subscribers are skipped with the log error: *"No message will be sent to this email because it has not been verified."* |

Footer Save button persists immediately on click → toast *"Saved successfully"* + modal closes.

## Business rules

### Default OFF protects sender reputation

Default OFF means: until the merchant explicitly opts in, campaign emails to unverified subscribers are skipped with the log error *"No message will be sent to this email because it has not been verified."* and the campaign's reached-count does NOT increment for those subscribers. This is the per-recipient pre-flight check `verified` step on [[email-channel-send-pipeline]].

The reasoning: sending to unverified addresses is a top driver of hard-bounces and spam complaints. The default OFF protects the merchant's sender reputation — which in turn protects them from the auto-suspend thresholds in [[email-channel-suspend-thresholds]] (`SUSPENDED_SPAM`, `SUSPENDED_BOUNCED`).

### Turning ON trades reach for risk

When ON, every subscriber on the list receives the campaign regardless of `verified` state. The merchant gets full list reach, but:

- Hard-bounce rate rises (unverified addresses often don't exist).
- Spam-complaint rate rises (typos / hostile signups arriving via subscribe forms).
- Both metrics feed the auto-suspend thresholds — see [[email-channel-suspend-thresholds]].

Recommended use: turn ON only on small, fresh lists where the merchant has high confidence the addresses are real, or on a one-shot re-engagement / verify campaign.

### Engagement events flip `verified = 1` retroactively

Once a subscriber **opens** or **clicks** an email, the [[email-channel-webhook-feedback|feedback webhook]] sets their Email channel `verified = 1`. So a merchant who turns ON `unconfirmed_send` and sends to a fresh list will see unverified subscribers flip to verified as they engage — the unverified pool shrinks naturally over time even without the merchant running a dedicated verify campaign.

### `unconfirmed_send` survives Reset configuration

Two settings persist across **Reset configuration** (see [[email-channel-elastic-email-account]]): `unconfirmed_send` and `manual_allowed_suspended`. So a merchant's send-to-unverified preference does not get wiped if they have to reset the Elastic Email binding.

### No other settings live on this modal

Currently this modal contains exactly one switch. The other per-channel knobs (sender mailbox, profile, domain) are not duplicated here — they live on the Configuration wizard ([[email-channel-setup-wizard]]).

## Related

- [[marketing-channels-email]] — hub.
- [[email-channel-send-pipeline]] — `unconfirmed_send` gates the per-recipient `verified` pre-flight check.
- [[email-channel-webhook-feedback]] — opens / clicks retroactively flip `verified = 1`, gradually shrinking the unverified pool.
- [[email-channel-suspend-thresholds]] — sending to unverified addresses pushes the bounce / spam rates that drive the auto-suspend triggers.
- [[email-channel-elastic-email-account]] — `unconfirmed_send` is one of the two settings that survive Reset configuration.
- [[marketing-subscribers]] — per-subscriber Email channel `verified` flag this setting overrides.

## Open questions

None.
