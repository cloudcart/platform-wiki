---
type: feature
nav_path: "Marketing → Channels → Channels setup → Viber → Settings"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Viber settings", "Viber settings modal", "Viber sender settings", "different_sender", "allow_self_credentials", "allow_promo_messages", "settings_type"]
tags: [marketing, channels, viber, settings]
plan_gates: ["viber_messages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-channels-viber]]. See the hub for the other aspects (self-credentials, send pipeline, DLR, system messages, plan cap, message format).

# Viber channel — Settings modal

## Purpose

The **Settings modal** for the Viber card is where the merchant configures *who the message appears to come from*. It is the only Viber settings surface (logs, usage, and system messages each have their own modals). The modal renders in **one of two branches**, picked by the platform based on the merchant's Viber contract.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → **Viber** card → **Settings** button. Title: *"Settings - Viber Message"*. The sub-component is `MarketingChannelsSettingsModalViber` rendered inside `MarketingChannelsSettingsModal`.

The settings payload is fetched via `GET /admin/api/core/marketing/campaigns/channels/viber-message/settings` and saved via the same path with a POST. The shape returned (`getUserSettings`) is **dual** — both `regular.*` and `self_credentials.*` are always present, plus metadata flags. The Vue front-end picks which panel to render off the metadata.

## What the merchant can do here

- Switch the sender name shown to the recipient (default `"CloudCart"`).
- Toggle **Use self profile** to opt into a non-default sender configuration.
- For eligible merchants only: enter their own InfoBip account credentials so sends route through their contract instead of CloudCart's shared pool — see [[viber-channel-self-credentials]] for the full lifecycle.

## Settings & fields

### Metadata flags (returned by `getUserSettings`)

| Flag | Default | What it means |
|------|---------|---------------|
| `allow_self_credentials` | computed | TRUE only for specific merchants — currently isZora OR `site_id = 17305` (mohana.bg) `(verify — special-client carve-out, do not document client names elsewhere)`. Decides whether Branch B is shown. |
| `allow_promo_messages` | computed | TRUE only for specific merchants — currently isZora OR `site_id = 30585` `(verify)`. Unlocks Image + Button cards in [[viber-channel-system-messages]] and the campaign-editor promo path. |
| `settings_type` | computed | `'self_credentials'` when self-creds are active and allowed; `'regular'` otherwise. |

The frontend picks which panel to display from these flags. Both shape's fields are always present in the API payload.

### Branch A — Regular settings (most merchants, `allow_self_credentials = false`)

| Field | Default | Effect |
|-------|---------|--------|
| `regular.different_sender` | `false` | When TRUE, sends try to use a non-default Viber sender via CloudCart's InfoBip account (premium service). |
| `regular.from` | `"CloudCart"` from `config('campaigns.viber.infobip.channels.viber.from')` | The Viber Business sender name shown to the recipient. |

A yellow warning banner reads:

> *"To send Viber messages from your own channel, you need to first contact your account manager to provide more information about this feature."*

The flag alone is not enough — the platform also gates `different_sender = true` on `getPlanSubscriptionValue` being truthy at send time `(verify)`. If the merchant flips the toggle without an active Viber-credits subscription, the channel silently falls back to the platform default sender even though the toggle is on.

### Branch B — Self-credentials settings (eligible merchants only)

Visible only when `allow_self_credentials = true`. See [[viber-channel-self-credentials]] for the activation lifecycle, scenario provisioning, and audit trail.

| Field | Notes |
|-------|-------|
| `self_credentials.active` | Toggle Self-credentials mode on/off. When ON, sends route through the merchant's own InfoBip contract — bypasses the CloudCart `viber_messages` plan cap (see [[viber-channel-plan-cap]]). |
| `self_credentials.username` | The merchant's InfoBip account username. |
| `self_credentials.password` | The merchant's InfoBip account password (masked input). |
| `self_credentials.host` | Optional override of the InfoBip API host. |
| `self_credentials.from` | The merchant's own Viber Business sender ID (must be pre-registered with InfoBip). |

A disclaimer banner is shown:

> *"In order to correctly report statistics for sent and read messages, you need to send the following webhook to your sales representative in Infobip: https://hooks.ccdev.info/messages/viber-campaign"*

### Save payload shape

The POST payload depends on the branch:

- **Self-credentials ON** — `{ self_credentials_active, username, password, host, 'channels.viber.from' }`.
- **Self-credentials OFF** — `{ different_sender, 'channels.viber.from' }`.

The `'channels.viber.from'` key is constant — the sender field is stored at the same setting path regardless of branch, but the source is `regular.from` vs `self_credentials.from` in the UI.

## Business rules

- **`different_sender` is a "premium sender" path, NOT full self-credentials.** It tells CloudCart to create / reuse a dedicated InfoBip scenario for the merchant's chosen sender name, but billing still flows through CloudCart's `viber_messages` plan cap. The `(verify)` plan-subscription gate on `getPlanSubscriptionValue` means a toggled-on `different_sender` may still send under the default sender if the merchant doesn't have the matching plan entitlement.
- **`allow_self_credentials` and `allow_promo_messages` are server-computed per merchant.** The merchant can't toggle these from the UI — they reflect the merchant's contract with CloudCart / InfoBip.
- **Both shapes are always returned.** The dual-shape payload exists so the frontend can switch branches reactively without a second API call when the metadata flips.

## Related

- [[marketing-channels-viber]] — hub.
- [[viber-channel-self-credentials]] — the full Self-credentials activation flow, scenario provisioning, audit trail.
- [[viber-channel-system-messages]] — the `allow_promo_messages` flag unlocks Image + Button cards in the system-message editor.
- [[viber-channel-plan-cap]] — `viber_messages` plan-feature key; self-credentials bypasses it.
- [[marketing-channels-cross-ui-surfaces]] — the shared per-channel modal layout pattern.

## Open questions

- Are the `isZora` / `site_id 17305` / `site_id 30585` carve-outs still in force as of 2026-06? Verify against current production code before quoting in support answers — the wiki rule is "do not document special-client carve-outs as general behaviour".
