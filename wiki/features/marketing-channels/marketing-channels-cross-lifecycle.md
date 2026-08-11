---
type: feature
nav_path: "Marketing → Channels → Channels setup → Channel lifecycle"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channel lifecycle", "Channel states", "Install activate suspend", "Deactivation cascade", "Жизнен цикъл канал", "Активиране на канал"]
tags: [marketing, channels, campaigns, lifecycle, install, activate]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, suspension, plan caps, sandbox, UI surfaces).

# Channels — channel lifecycle

## Purpose

The five lifecycle phases every channel moves through on a given store, the two operational transitions the merchant drives directly (Install / Uninstall and Activate / Deactivate), the cascade that auto-stops dependent campaigns when a channel is deactivated, and what re-activating does (and does NOT) bring back. This is the operational "what state is my channel in right now" model.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup**. State is surfaced on each card via the status badge (Active / Inactive / Suspended / Configuration required) and the Active / Inactive toggle switch.

## What the merchant can do here

- **Install** a channel that is dormant on this store.
- **Uninstall** an installed channel (preserves history, blocks future sends).
- **Activate / Deactivate** an installed channel with the inline toggle.
- See the channel's current lifecycle state via the status badge.
- Confirm a deactivation that will cascade-stop campaigns referencing the channel.

## Settings & fields

The state badge on each card derives from a combination of the per-channel state fields documented in [[marketing-channels-cross-catalog]]. The transitions the merchant controls:

| Transition | Trigger | Resulting state field change |
|---|---|---|
| Install | Card's **Install** button | `installed = 1` (per-channel) |
| Uninstall | Trash-can icon → confirm dialog | `installed = 0`; existing logs preserved; new sends blocked |
| Activate | Card's Active toggle ON | `active = 1`; campaign pre-flight checks now pass for this channel |
| Deactivate | Card's Active toggle OFF + confirm modal | `active = 0`; dependent campaigns auto-stopped (see below) |
| Configure (Email only) | Multi-step wizard | `configured = 1` when all four steps complete |

## Business rules

### The five lifecycle phases

A channel goes through these phases on each store:

1. **Dormant** — exists in the platform catalog but `installed = 0` on this store. No campaigns can target it.
2. **Installed but inactive** — credentials present, `installed = 1`, but `active = 0`. Set up but turned off (e.g., paused for the season).
3. **Configured (Email only)** — Email additionally needs `firstName` → `domain` → `verify` (DNS records OK) → `configured` (sender email confirmed) to actually send. An Email channel that's installed-but-not-configured is treated as **not configured** by campaign pre-flight checks even if `active = 1`.
4. **Active** — `installed = 1`, `active = 1`, plus any channel-specific "configured" requirement satisfied. Campaign actions can target this channel.
5. **Suspended** — `installed = 1`, `active = 1`, but `suspended_by` is non-null. New sends are blocked. The campaign using this channel shows the banned-reason badge until the merchant fixes the underlying issue — see [[marketing-channels-cross-suspension]] for the four triggers.

### Deactivating a channel cascades to campaigns

When the merchant toggles a channel OFF (or when the platform auto-suspends it via [[marketing-channels-cross-suspension]]), the platform searches for any [[marketing-campaigns|Campaign]] whose actions reference the channel and **automatically marks each one as stopped** (`active = 0`).

The merchant-visible message before flipping:

*"There are campaigns that are ':name'. They will be automatically marked as stopped"*

After confirmation, the cascade runs in a single transaction together with the channel state change. The merchant is shown the list of campaign names that will be stopped on the confirm dialog.

**Re-activating the channel later does NOT auto-restart the stopped campaigns** — the merchant must turn each affected campaign back on manually. This is intentional: a channel may have been deactivated for cleanup reasons, and the merchant should review each campaign before resuming sends.

Activating a channel never shows the confirm modal — only deactivation cascades.

### Uninstall vs deactivate — when to use which

| Operation | Effect | Use when |
|-----------|--------|----------|
| **Deactivate** | Channel keeps credentials + settings + reputation; just won't send | Temporary pause (seasonal, maintenance, testing) |
| **Uninstall** | Removes credentials reference, blocks sends, preserves historical logs / counts | Switching providers, decommissioning the channel for good |

Uninstall is destructive of credentials — re-installing requires re-entering provider settings.

### Configuration-required state (Email only)

Email is the only channel with a multi-step configuration; the wizard runs Profile → Domain → DKIM/SPF/Tracking/DMARC verify → Sender email. Until all four steps complete, the channel sits in **Configured (Email only)** sub-phase and pre-flight checks on campaigns referencing it report *"Channel ":name" is not configured"*. See [[marketing-channels-email]] for the wizard.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-catalog]] — the per-channel state fields surfaced by the lifecycle.
- [[marketing-channels-cross-suspension]] — auto-suspension triggers that move a channel into the Suspended phase.
- [[marketing-channels-cross-sandbox]] — anti-spam policy gate that must be accepted before installing any channel.
- [[marketing-campaigns]] — campaigns are what get cascade-stopped on deactivation.
- [[marketing-channels-email]] — the configuration wizard (only channel with the extra sub-phase).
- [[marketing-channels-logs]] — historical logs preserved across Uninstall.

## Open questions

None.
