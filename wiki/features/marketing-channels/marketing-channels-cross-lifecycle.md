---
type: feature
nav_path: "Marketing → Channels → Channels setup → Channel lifecycle"
route_name: campaigns-channels
route_path: /admin/marketing/campaigns/channels
aliases: ["Channel lifecycle", "Channel states", "Install activate suspend", "Deactivation cascade", "Жизнен цикъл канал", "Активиране на канал"]
tags: [marketing, channels, campaigns, lifecycle, install, activate]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, suspension, plan caps, pre-flight, UI surfaces).

# Channels — channel lifecycle

## Purpose

The five lifecycle phases every channel moves through on a given store, the two operational transitions the merchant drives directly (Install / Uninstall and Activate / Deactivate), the cascade that auto-stops dependent campaigns when a channel is deactivated, and what re-activating does (and does NOT) bring back. This is the operational "what state is my channel in right now" model.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup**. State is surfaced on each card via the status badge and the Active / Inactive toggle switch. A reputation-suspended channel shows only **Disabled** — there is no Suspended badge (see [[marketing-channels-cross-suspension]]).

## What the merchant can do here

- **Install** a channel that is dormant on this store.
- **Uninstall** an installed channel (keeps its settings and history, blocks future sends).
- **Activate / Deactivate** an installed channel with the inline toggle.
- See the channel's current lifecycle state via the status badge.
- Confirm a deactivation that will cascade-stop campaigns referencing the channel.

## Settings & fields

The state badge on each card derives from a combination of the per-channel state fields documented in [[marketing-channels-cross-catalog]]. The transitions the merchant controls:

| Transition | Trigger | Resulting state field change |
|---|---|---|
| Install | Card's **Install** button (Viber, SMS, Web Push) | `installed` and `first_install` set (per-channel) |
| Uninstall | Trash-can icon → confirm dialog | `installed` removed; settings and logs kept; new sends blocked |
| Activate | Card's Active toggle ON | `active = 1`; campaign pre-flight checks now pass for this channel |
| Deactivate | Card's Active toggle OFF (+ confirm modal when a campaign step uses the channel) | `active = 0`; dependent campaigns auto-stopped (see below) |
| Configure (Email only) | Multi-step wizard | `configured = 1` when all four steps complete |

## Business rules

### The five lifecycle phases

A channel goes through these phases on each store:

1. **Dormant** — exists in the platform catalog but has no `installed` setting on this store. No campaigns can target it.
2. **Installed but inactive** — credentials present, `installed = 1`, but `active = 0`. Set up but turned off (e.g., paused for the season).
3. **Configured (Email only)** — Email additionally needs `firstName` → `domain` → `verify` (DNS records OK) → `configured` (sender email confirmed) to actually send. An Email channel that's installed-but-not-configured is treated as **not configured** by campaign pre-flight checks even if `active = 1`.
4. **Active** — `installed = 1`, `active = 1`, plus any channel-specific "configured" requirement satisfied. Campaign actions can target this channel.
5. **Suspended** — the reputation sync switched the channel off (`active = 0`) and recorded a `suspended_by` reason. Campaigns are not touched; each later step on the channel drops itself, and campaign rows show the reason. It does not lift by itself — see [[marketing-channels-cross-suspension]] for the four triggers and staff recovery.

### Switching a channel off cascades to campaigns

When any campaign step uses the channel, switching it off asks for confirmation first. The modal is titled **Disable channel**, with **Confirm** and **Cancel**; its message names the **channel**, with no list of campaigns:

*"There are campaigns that are ":name". They will be automatically marked as stopped"* (BG: *„Има кампании които са ":name". Те ще бъдат автоматично маркирани като спрени“*)

On confirm, **every** [[marketing-campaigns|campaign]] with a step on that channel is set inactive (`active = 0`) — automated flows (e.g. abandoned cart), drafts (which become inactive and read-only) and archived ones included.

**Switching the channel back on reactivates nothing.** Automated campaigns can be switched on again one by one; Regular campaigns cannot be re-activated from the UI.

Only this **manual** switch-off changes campaigns. Reputation auto-suspension, a rejected Email key ([[email-channel-reconnect]]), or reaching the plan cap do **not** change any campaign's state.

Activating a channel never shows the confirm modal — only deactivation cascades.

### Uninstall vs deactivate — when to use which

| Operation | Effect | Use when |
|-----------|--------|----------|
| **Deactivate** | Channel keeps credentials + settings + reputation; just won't send | Temporary pause (seasonal, maintenance, testing) |
| **Uninstall** | Removes only the `installed` setting: blocks sends, keeps the channel's settings and historical logs / counts | Taking the channel off the channels page |

Re-installing does not ask for the settings again. The channel's state survives a page reload.

Install and Uninstall exist only for channels the channels page offers them on: Viber, SMS and Web Push. E-mail, tags and customer group are always on. Any other channel answers *"Channel not found"*.

### Configuration-required state (Email only)

Email is the only channel with a multi-step configuration; the wizard runs Profile → Domain → DKIM/SPF/Tracking/DMARC verify → Sender email. Until all four steps complete, the channel sits in **Configured (Email only)** sub-phase and pre-flight checks on campaigns referencing it report *"Channel ":name" is not configured"*. See [[marketing-channels-email]] for the wizard.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-catalog]] — the per-channel state fields surfaced by the lifecycle.
- [[marketing-channels-cross-suspension]] — auto-suspension triggers that move a channel into the Suspended phase.
- [[marketing-channels-cross-preflight]] — anti-spam policy gate that must be accepted before installing any channel.
- [[marketing-campaigns]] — campaigns are what get cascade-stopped on deactivation.
- [[marketing-channels-email]] — the configuration wizard (only channel with the extra sub-phase).
- [[marketing-channels-logs]] — historical logs preserved across Uninstall.

## Open questions

None.
