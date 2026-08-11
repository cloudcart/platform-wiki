---
type: feature
nav_path: "Marketing → Channels → Channels setup → Sandbox & pre-flight gates"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel sandbox", "Sandbox mode", "Sandbox URL", "Webhook redirect for testing", "Anti-spam policy gate", "Channel pre-flight check", "Тестов режим канал", "Sandbox канали"]
tags: [marketing, channels, sandbox, testing, anti-spam, pre-flight]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, lifecycle, suspension, plan caps, UI surfaces).

# Channels — sandbox mode & pre-flight gates

## Purpose

The two cross-cutting gates that determine whether a channel-bound action can run at all: (a) the per-channel **Sandbox URL** redirect that lets the merchant test message rendering without spending plan credits or annoying real recipients, and (b) the **anti-spam policy** acceptance gate that blocks the entire Channels setup UI until accepted, plus the per-campaign **pre-flight checks** that fire on campaign launch and produce the merchant-visible "channel is not configured / not active / out of credits" messages.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup**.

- **Sandbox** — collapsible band at the bottom of each channel card; on/off switch + one text input (*"Webhook post url"*) + **Submit** button.
- **Anti-spam policy gate** — if not yet accepted, navigating to the Channels setup route redirects to `/admin/marketing-new/campaigns/policy` ([[marketing-campaigns-policy]]) BEFORE the merchant ever sees the channels page.
- **Pre-flight checks** — surfaced on the [[marketing-campaigns|Campaign]] page during launch, not on the Channels setup page itself.

## What the merchant can do here

- Toggle Sandbox mode on a channel and set the destination URL where messages will be redirected during testing.
- Submit the sandbox config (button disabled until the URL or toggle has changed from the last-saved state).
- Accept the anti-spam policy on first-ever access (one-time, store-wide).
- Read pre-flight error messages on the Campaign page when one or more channels block the campaign.

## Settings & fields

### Sandbox band controls (per channel)

| Control | Visible when | What it does |
|---------|--------------|--------------|
| Sandbox on/off switch | Channel installed | Toggles `sandbox_status` true / false. |
| Webhook post URL | Sandbox switch ON | The destination URL outbound messages are redirected to during sandbox mode. Typically a webhook.site URL or similar inspection tool. |
| Submit | Form dirty | Persists `{sandbox_status, sandbox_url}` to the channel. Disabled until a change is detected. |

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

### How Sandbox redirects work

When `sandbox_status = true` on a channel:

- Outbound messages are **redirected** to the merchant's chosen webhook URL instead of going to the real recipient (subscriber's email / phone / WebPush endpoint).
- The merchant can verify message content, headers, and template-variable substitution without spending plan credits or annoying real customers.
- The redirect uses a Guzzle POST with a **5-second timeout** — separate from the production provider call.
- The sandbox POST does **not** count toward the channel's plan cap (see [[marketing-channels-cross-plan-caps]]).
- The usage-alert 80% threshold check **still runs** even on sandbox sends — accounting tracks the counter regardless.

The recommended workflow:

1. Set the Sandbox URL to a fresh webhook.site (or similar) URL.
2. Toggle Sandbox ON.
3. Launch the campaign as normal.
4. Inspect the captured POSTs at the webhook URL to confirm rendering / variable substitution.
5. Toggle Sandbox OFF before going live.

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

### Sandbox is per-channel, not per-campaign

A merchant cannot put one campaign into sandbox mode while another campaign on the same channel runs live. The sandbox state lives on the channel — once toggled ON, EVERY campaign using that channel redirects to the webhook URL. To test one campaign in isolation, the merchant must either pause all other campaigns on that channel for the duration of the test, or sandbox-test on a non-production store.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-plan-caps]] — sandbox interaction with the usage-alert and cap counter.
- [[marketing-channels-cross-lifecycle]] — the `configured / active` fields the pre-flight checks read.
- [[marketing-channels-cross-magic-vars]] — template variables the merchant verifies via the sandbox POSTs.
- [[marketing-campaigns-policy]] — the anti-spam policy page the gate redirects to.
- [[marketing-campaigns]] — where pre-flight check messages are shown.
- [[marketing-channels-email]] — Email-specific "not configured" sub-state.

## Open questions

- Whether the 5-second sandbox Guzzle timeout is the same value used for actual provider calls (the production call is documented as a 5-second Guzzle timeout in the same source). (verify)
