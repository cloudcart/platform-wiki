---
type: feature
nav_path: "Marketing → Channels → Channels setup → Plan caps & credits"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel plan caps", "Channel send quota", "Usage alert", "Buy more credits", "Self-credentials", "Viber self-credentials", "Кредити канал", "Лимит канал"]
tags: [marketing, channels, plan-caps, credits, usage, self-credentials]
plan_gates: ["campaign.channel.email", "campaign.channel.sms_msghub_message", "campaign.channel.sms_nth_message", "campaign.channel.web_push", "viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, lifecycle, suspension, sandbox, UI surfaces).

# Channels — plan caps, usage alerts & self-credentials

## Purpose

How a channel's send volume is metered against the merchant's plan, when the 80% usage-alert notification fires, what the merchant sees when a cap is reached, the Buy-more-credits flow that lets the merchant raise the cap inside the billing cycle, and the Viber-only **self-credentials** override that bypasses CloudCart's metering entirely. This is the layer that turns "this channel is active" into "this channel is allowed to send the next message".

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup**. Each card shows:

- **Usage** button (all five channels) → opens the [[marketing-channels-usage]] modal with the live counter vs cap.
- **Restrictions band** (yellow info-box) that appears only when the plan cap is exhausted or self-credentials are not configured.
- **Buy more** button on the Restrictions band → opens the [[plan-features]] PlanFeature purchase modal scoped to this channel's `plan_feature_key`.
- For Viber: the Settings modal exposes the **self-credentials** toggle ([[marketing-channels-viber]]).

## What the merchant can do here

- See current period send count vs plan cap per channel.
- Receive an Admin Notification when sends cross 80% of the cap.
- Purchase additional credits (feature pack) to extend the current cycle's cap.
- For Viber, switch to their own InfoBip credentials to bypass CloudCart's cap entirely.

## Settings & fields

### Per-channel plan-feature keys

Every channel has the plan-feature key documented in [[marketing-channels-cross-catalog]]. The plan defines two layered allowances per key:

- A **one-time allowance** (the platform code) — e.g., emails-included with the plan tier.
- A **subscription allowance** (the platform code) — e.g., recurring monthly quota.

**Effective cap** = one-time + subscription. The merchant's send counter for the cycle is metered against this combined cap.

### Usage-alert threshold

The platform emits the **Usage alert notification** when sends cross the `USAGE_ALERT_PERCENTAGE = 80`% threshold (verify). The alert surfaces:

- In the [[settings-admin-notifications|Admin Notifications]] panel.
- Via the `campaign.channel.usage.{mapping}` notification group (configurable per channel under [[settings-admin-notifications]]).

The 80% threshold fires once per cycle per channel — repeated sends across 80% don't re-trigger.

### "Cap reached" merchant state

When the cap is reached and the merchant doesn't have self-credentials enabled (Viber only), the channel's `banned_reason` flips to the **feature-limit-reached** message. The Restrictions band on the card surfaces:

*"You have reached your channel limit. Your plan limit is {limit}. You need to purchase more to continue the use of this channel."*

With a **Buy more** button that opens the `PlanFeature` purchase modal scoped to this channel's `plan_feature_key`. Campaigns using the channel pause until either:

1. The cap is raised (upgrade plan or buy a feature pack), OR
2. The next billing cycle resets the counter.

The pause is **soft** — already-scheduled campaign actions stop being processed; the campaign itself is not stopped (unlike the deactivation cascade in [[marketing-channels-cross-lifecycle]]). Once the cap is raised, processing resumes from where it stopped.

## Business rules

### Self-credentials override (Viber only)

For **Viber**, the merchant can supply their own InfoBip Viber Business Messages credentials (username, password, scenario key) instead of using CloudCart's shared pool. When `self_credentials_active = true`:

- Sends use the merchant's InfoBip contract → the merchant is **billed directly by InfoBip**, not by CloudCart.
- The CloudCart plan-cap for Viber **doesn't apply** — sends are unlimited (from CloudCart's perspective).
- The Viber Business sender ID is the **merchant's own**, not "CloudCart".

This requires the merchant to have a paid InfoBip account with a registered Viber Business sender — see [[marketing-channels-viber]] for the activation flow.

**SMS NTH and SMS MsgHub do not currently expose merchant-supplied credentials in the UI.** Email uses a CloudCart-managed Elastic Email sub-account per store (not a merchant-supplied API key), so there is no Email self-credentials path either — only Viber.

### Usage-alert and sandbox interaction

Sandbox sends (see [[marketing-channels-cross-sandbox]]) still **run the 80%-threshold check** even though the actual destination is a webhook URL. However, **plan-cap accounting itself is NOT incremented for sandbox sends** — the sandbox POST is a separate Guzzle call with a 5-second timeout, not the production provider call. The merchant can sandbox-test heavily without burning real credits, but the usage-alert system still tracks the counter for accounting purposes.

### Feature-pack purchase flow

Clicking **Buy more** on the Restrictions band opens the same [[plan-features|PlanFeature]] modal CloudCart uses across the admin for upsell purchases. The modal is scoped to the channel's `plan_feature_key` — only feature packs that increase THIS channel's cap are shown. The purchase takes effect immediately on confirmation: the cap rises mid-cycle and queued sends resume.

### What "cap" means is per-cycle, not per-channel

The plan-cap counter is per **billing cycle**, not per channel lifetime. Renewing the subscription resets each channel's counter automatically. Crossing the 80% threshold in cycle N does NOT re-fire in cycle N+1 unless the merchant crosses it again in the new cycle.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-catalog]] — the plan-feature key column tells you which key to look at per channel.
- [[marketing-channels-cross-sandbox]] — sandbox sends and how they interact with the cap counter.
- [[marketing-channels-usage]] — the Usage modal that shows the live counter.
- [[marketing-channels-viber]] — the Viber self-credentials activation flow.
- [[plan-features]] — the PlanFeature purchase modal opened by Buy more.
- [[plan-gates]] — the feature-key registry used by the platform code.
- [[settings-admin-notifications]] — where the 80% usage alert appears.
- [[merchant-subscription-lifecycle]] — billing-cycle boundaries that reset the cap counter.

## Open questions

None.
