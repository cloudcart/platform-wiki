---
type: feature
nav_path: "Marketing → Channels → Channels setup → Pre-flight gates"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Anti-spam policy gate", "Channel pre-flight check", "Channel is not configured", "Channel is not active", "Not enough credits for channel", "Канал не е конфигуриран", "Канал не е активен"]
tags: [marketing, channels, anti-spam, pre-flight]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, lifecycle, suspension, plan caps, UI surfaces).

# Channels — pre-flight gates

## Purpose

The gates that determine whether a channel-bound action can run at all: the **anti-spam policy** acceptance gate that blocks the entire Channels setup UI until accepted, and the per-campaign **pre-flight checks** that fire on campaign launch and produce the merchant-visible "channel is not configured / not active / out of credits" messages.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup**.

- **Anti-spam policy gate** — if not yet accepted, navigating to the Channels setup route redirects to `/admin/marketing/campaigns/policy` ([[marketing-campaigns-policy]]) BEFORE the merchant ever sees the channels page.
- **Pre-flight checks** — surfaced on the [[marketing-campaigns|Campaign]] page during launch, not on the Channels setup page itself.

## What the merchant can do here

- Accept the anti-spam policy on first-ever access (one-time, store-wide).
- Read pre-flight error messages on the Campaign page when one or more channels block the campaign.

## Settings & fields

### Anti-spam policy gate fields

There is **no field on the Channels setup page itself** for the policy — it lives at [[marketing-campaigns-policy]]. The Channels setup route checks the persisted setting `campaigns.anti_spam_policy_accepted` on entry; if falsy, it redirects.

### Channel pre-flight check messages

When a merchant starts a campaign, the platform checks each action's referenced channel:

| Message | Triggered when |
|---------|----------------|
| *"Channel ":name" is not configured"* | `installed = false` OR settings incomplete (for Email: not at `configured = 1`). |
| *"Channel ":name" is not active"* | `installed = 1` but `active = 0`. |
| *"You do not have enough credits for:name"* | Plan cap exhausted (see [[marketing-channels-cross-plan-caps]]) and no self-credentials. |

The campaign won't start until all referenced channels pass these checks. The messages are also documented at [[marketing-campaigns#Channel-level guards]].

## Business rules

### Anti-spam policy is a HARD gate

Both `campaigns-channels` and `campaigns-email-saved-templates` Vue routes enforce a `beforeEnter` guard: if `campaigns.anti_spam_policy_accepted` is falsy, the merchant is redirected to `campaigns-policy` first. The backend additionally enforces this via middleware on every campaign controller — the merchant cannot configure any channel until they've accepted the policy.

Acceptance is **per-store, one-time**. Once accepted, the gate doesn't fire again.

See [[marketing-campaigns-policy]] for the actual policy contents and acceptance UI.

### Pre-flight check ordering

When the merchant clicks "Start campaign", the pre-flight checks run in this order per referenced channel:

1. Is the channel **configured**? (catches Email's not-yet-DKIM-verified state).
2. Is the channel **active**? (catches `active = 0`).
3. Does the channel have **credits**? (catches plan-cap exhaustion).

The first failing check is what the merchant sees — subsequent checks are not evaluated until earlier ones pass. A channel failing all three reports only "not configured".

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-plan-caps]] — the credits behind the third check.
- [[marketing-channels-cross-lifecycle]] — the `configured / active` fields the pre-flight checks read.
- [[marketing-campaigns-policy]] — the anti-spam policy page the gate redirects to.
- [[marketing-campaigns]] — where pre-flight check messages are shown.
- [[marketing-channels-email]] — Email-specific "not configured" sub-state.


## Open questions

- None.
