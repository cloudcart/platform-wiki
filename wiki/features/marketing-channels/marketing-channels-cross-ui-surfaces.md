---
type: feature
nav_path: "Marketing → Channels → Channels setup → UI surfaces"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Channels page UI", "Channel card layout", "Channels modals", "Deactivation confirmation modal", "Lazy-load channel stats", "UI канали"]
tags: [marketing, channels, ui, modals, card-layout]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels]]. See the hub for related aspects (catalog, lifecycle, suspension, plan caps, sandbox, magic vars).

# Channels — UI surfaces (cards, modals, lazy-load)

## Purpose

The on-page UI of the Channels setup screen: the four-band card layout used per channel, the seven overlay modals the page mounts and binds to a shared `channelData` ref, the deactivation confirmation dialog and what it shows, and the lazy-load pattern the page uses to avoid blocking the initial render on per-channel detail calls. This is the "what does the merchant actually see, click, and read on this page" reference.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup**. The whole page is a single scrollable list of channel cards plus a stack of overlay modals that open on demand from each card's action row.

## What the merchant can do here

- Read the per-channel status badge.
- Toggle Active / Inactive (with a confirm dialog on Deactivate when campaigns are affected).
- Install / Uninstall the channel.
- Click into one of seven overlay modals: System Message, Configuration, Settings, Reputation, Usage, Log, PlanFeature (Buy more).
- Navigate to the Saved Templates page (Email only) — this is a route navigation, not a modal.

## Settings & fields

### Per-channel card — four-band layout (top to bottom)

| Band | Visible when | What it contains |
|------|--------------|------------------|
| 1. **Header band** | Always | Channel icon + name + status badge (*"Active"* / *"Inactive"* / *"Suspended"* / *"Configuration required"*) + Active toggle switch + Install or Uninstall button. Below the name, installed channels show inline usage stats (sends today / opens / clicks). |
| 2. **Actions band** | `is_installed = true` | Slide-up reveal of available action buttons. Possible buttons: **System Message** (Viber, Web Push), **Configuration** (Email — opens the 4-step wizard), **Settings** (Email, Viber, Web Push), **Reputation** (Email only), **Usage** (all five), **Log** (all five), **Saved Templates** (Email only — routes to `campaigns-email-saved-templates`). |
| 3. **Restrictions band** | `plan.allow_execute = false` OR `plan_remaining = 0` (and `plan_value != null`) | Yellow info-box with *"You have reached your channel limit. Your plan limit is {limit}. You need to purchase more to continue the use of this channel."* + **Buy more** button. See [[marketing-channels-cross-plan-caps]]. |
| 4. **Sandbox band** | `sandbox.available = true` (all five installed channels) | Collapsible card with Sandbox on/off switch + Submit button + *"Webhook post url"* text input. See [[marketing-channels-cross-sandbox]]. |

The buttons in the Actions band render only when their `presets.{key}.available` is TRUE for the channel — so Email's Actions band shows {Configuration, Settings, Reputation, Usage, Log, Saved Templates} but NOT {System Message}; Viber's shows {System Message, Settings, Usage, Log} but NOT {Configuration, Reputation, Saved Templates}.

### Deactivation confirmation modal

When the merchant flips the Active switch OFF and the backend responds with `requires_confirmation = true`, a confirm dialog opens:

| Field | Value |
|-------|-------|
| Title | *"Disable channel"* |
| Message | *"There are campaigns that are ':name'. They will be automatically stopped"* (server-supplied text listing the campaign names that will be cascade-stopped). |
| Yes button | *"Confirm"* — resubmits the deactivate with a confirmed flag. The channel toggles off AND every dependent campaign flips to stopped in a single DB transaction. |
| No button | *"Cancel"* — switch animates back to ON, no API call made. |

**Activating** a channel never shows this modal — only deactivation cascades. See [[marketing-channels-cross-lifecycle]] for the cascade semantics.

### Seven overlay modals mounted on the page

The page mounts these modals at the root, all bound to a shared `channelData` ref that the actions band populates when a button is clicked:

| Modal | Channels that open it | Wiki page |
|-------|----------------------|-----------|
| Email Configuration (4-step wizard) | Email | [[marketing-channels-email]] |
| Settings (routes to per-channel sub-component by mapping) | Email, Viber, Web Push | [[marketing-channels-email]] / [[marketing-channels-viber]] / [[marketing-channels-webpush]] |
| System Messages (with nested template editor) | Viber, Web Push | [[marketing-channels-system-messages]] |
| Logs (with nested Preview + Subscriber-Details modals) | All five | [[marketing-channels-logs]] |
| Reputation | Email only | [[marketing-channels-reputation]] |
| Usage | All five | [[marketing-channels-usage]] |
| PlanFeature (global purchase modal) | All five (opened via Restrictions / Usage's Buy-credit button) | [[plan-features]] |

The action-band button click sets `channelData` to a deep clone of the current channel and flips the matching modal's open state — the modal does NOT re-fetch the channel registry, only its own per-modal endpoint (settings / config / logs / reputation / usage / system-messages).

## Business rules

### Lazy-load pattern for per-card usage stats

On page mount, the main channels list query returns each channel's `info`, `actions`, and `presets` immediately — but each channel row has `plan` and `usage` set to `null`. A second per-channel detail call fires for EACH non-skipped channel mapping **in parallel** (8-second timeout per request, with a per-channel loading state tracked individually).

While the per-channel call is in flight:

- The header band shows a loader spinner on that card.
- Usage stats (sends today / opens / clicks) are blank.

If the call errors out, the loader exits silently and the stats fall back to `0`. The user can still operate Install / Toggle / Uninstall without waiting for the detail call.

### Three "skip" mappings filtered out of the card list

The mappings `set_customer_group`, `set_tags`, `remove_tags` are filtered out from the Channels setup card list because they are NOT real channels — they are campaign-action helpers. The Channels setup page renders only the five active marketing channels documented in [[marketing-channels-cross-catalog]].

### Sandbox band Submit button gating

The Sandbox band's Submit button is **disabled** until the merchant changes either the URL or the toggle from the last-saved state. This prevents accidental no-op saves. On Submit, a PATCH posts `{sandbox_status, sandbox_url}` to the channel.

### Reputation card error state — "Reset configuration"

When the Email-channel Reputation read throws an "expired" error during card hydration, the platform replaces the Reputation button with a **Reset configuration** button at that moment. Clicking it re-initialises the provider account binding (verify — full reset semantics on [[marketing-channels-email]]).

### Buy-more modal scoping

The Buy-more button on the Restrictions band opens the global [[plan-features|PlanFeature]] purchase modal scoped to **this channel's** `plan_feature_key`. Only feature packs that raise THIS channel's cap are shown — the merchant can't accidentally buy SMS credits while trying to top up Email.

## Related

- [[marketing-channels]] — hub.
- [[marketing-channels-cross-catalog]] — the `mapping` keys filtered by the three skip-rules.
- [[marketing-channels-cross-lifecycle]] — what the Deactivate-confirm modal references.
- [[marketing-channels-cross-plan-caps]] — what the Restrictions band surfaces.
- [[marketing-channels-cross-sandbox]] — what the Sandbox band controls.
- [[marketing-channels-logs]] — Logs modal deep-dive.
- [[marketing-channels-usage]] — Usage modal deep-dive.
- [[marketing-channels-reputation]] — Reputation modal deep-dive.
- [[marketing-channels-system-messages]] — System Messages modal deep-dive.
- [[marketing-channels-email]] — Email Configuration wizard.
- [[plan-features]] — PlanFeature purchase modal.

## Open questions

None.
