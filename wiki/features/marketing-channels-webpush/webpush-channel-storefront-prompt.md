---
type: feature
nav_path: "Marketing → Channels → Channels setup → Web Push → Settings"
route_name: campaigns-channels
route_path: /admin/marketing-new/campaigns/channels
aliases: ["Web Push popup", "Web Push prompt", "WebPush opt-in popup", "Subscription prompt only on successful purchase page", "Two-stage push prompt", "Уеб пуш попъп", "Уеб пуш покана"]
tags: [marketing, channels, web-push, popup, prompt, storefront, ux]
plan_gates: ["campaign.channel.web_push"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-channels-webpush]]. See the hub for the other aspects (subscription flow, VAPID config, send pipeline, DLR webhook, system messages, browser support).

# Web Push channel — Storefront permission prompt

## Purpose

The **Settings - Web Push** modal (`MarketingChannelsSettingsModalWebPush`) controls **how and when** the storefront asks a visitor to subscribe to push notifications. Web Push has the most merchant-visible UX configuration of any channel — because the prompt the customer sees is heavily customisable. The pane drives a **two-stage prompt**: a CloudCart-custom popup (the "pre-prompt") that fires first, then the native browser permission prompt if the customer clicks Allow.

The two-stage design is deliberate. The native browser prompt is **one-shot per user** — once dismissed, browsers will not show it again until the user manually resets it in browser settings. The pre-prompt lets the customer dismiss CloudCart's UI without burning the native prompt, preserving the merchant's ability to re-prompt later.

## Where to find it

Sidebar → **Marketing** → **Channels** → **Channels setup** (route `campaigns-channels`, `/admin/marketing-new/campaigns/channels`) → **Web Push** channel card → **Settings** (sliders icon). Title — *"Settings - Web Push"*. Body stacks **three `CcCards`** vertically (Checkout-only mode / Overlay / Popup).

## What the merchant can do here

- Toggle **Subscription prompt only on successful purchase page** (`checkout`) — when ON, the popup only appears on the post-checkout return page.
- Toggle **Popup** master switch (`popup_status`) — when OFF, the CloudCart pre-prompt never appears (so the native prompt also never fires, since it's gated on the popup).
- Edit **Overlay caption** (`message`) — informational text shown above the native browser permission prompt.
- Edit **Popup message** (`popup_text`), **Consent button text** (`popup_ok_button`), **Decline button text** (`popup_discard_button`), and **Image** (`popup_image`).
- Save — all settings persist immediately. Toast *"Saved successfully"* + modal closes.

## Settings & fields

### Card 1 — Checkout-only mode

| Setting | Default | Effect |
|---|---|---|
| `checkout` | `0` (OFF) | When TRUE, the permission prompt only appears on the post-checkout return page (`route.checkout.return` with `status != 'cancel'`). When FALSE, prompt logic falls back to `popup_status`. |

### Card 2 — Overlay (caption above the native browser prompt)

| Setting | Default | Effect |
|---|---|---|
| `message` | *"Click on Allow button and subscribe to the push notifications"* | The **overlay** caption shown above the native browser permission prompt — an informational hint to nudge the customer to click Allow. Textarea, 2 rows. |

### Card 3 — Popup (the CloudCart-custom pre-prompt)

| Setting | Default | Effect |
|---|---|---|
| `popup_status` | `true` | Master toggle for whether the pre-prompt popup appears at all (site-wide). |
| `popup_text` | *"Never miss an offer! Would you like to receive news and notifications about the latest products?"* | Long-form body text inside the popup. |
| `popup_ok_button` | *"ALLOW"* | Label on the "Yes, prompt me" button. |
| `popup_discard_button` | *"NO THANKS"* | Label on the "No, ignore" button. |
| `popup_image` | Store logo (via the `logo` helper) | Image shown in the popup. Empty state shows a cloud-upload icon + *"Click to upload"*; clicking opens `CcImageModal`. Below the thumbnail sit **rotate** (re-pick) and **trash** (clear) icon-buttons. Label below: *"Image (80px * 80px)"*. |

### Card 3 — read-only at the UI level

| Setting | Default | Effect |
|---|---|---|
| `cookie_life_time` | `7` days | How many days to wait before re-showing the popup to a customer who dismissed it. Clamped to `[1, 365]` — values outside fall back to 7. **Not exposed in the Settings form** — support can override via direct setting update. |

VAPID keys are NOT surfaced anywhere in this modal — the platform manages one shared key pair across all stores (see [[webpush-channel-vapid-config]]). There are no show / regenerate / test-push buttons in this pane.

## Business rules

### `PushAllow` precedence — exact resolution order

The Smarty/Vue init block computes a `PushAllow` boolean on every storefront page load:

- If `checkout = true` → `PushAllow` is true ONLY when the active route is `checkout.return` AND the status param is not `cancel`. The popup is invisible on every other page.
- If `checkout = false` → `PushAllow` falls back to `popup_status`. The popup can fire on any storefront page.

Set `checkout = true` when the merchant wants to ask only buyers (best signal-to-noise — converts have just committed). Leave `checkout = false` (default) for site-wide opt-in.

### `popup_status = false` disables both the popup AND the native prompt

Because the popup is the **only** trigger for the native browser prompt, switching `popup_status` to OFF effectively disables Web Push subscription on the storefront — no popup shown, no native prompt fired, no new subscribers. Existing subscribers continue to receive messages; the merchant has just turned off acquisition.

### `cookie_life_time` survives clamping

Values ≤ 0 or > 365 silently fall back to 7 days. Setting it to e.g. 30 means a customer who clicked **NO THANKS** sees the popup again after 30 days. The cookie is browser-side, so a customer clearing cookies / using incognito starts fresh.

### Cookie vs native permission state — independent

The `cookie_life_time` setting controls only the **CloudCart popup's** re-display cadence. It does NOT override the **native browser permission state**. If the customer DENIED the native prompt, the CloudCart popup may re-show but the native prompt will not appear again until the user resets it in browser settings.

### Already-subscribed visitors don't see the popup

When a customer subscribes successfully, the storefront sets the `_cc_wp = 1` cookie for 86400 seconds (24 hours). While that cookie is present, the popup is suppressed for that browser — see [[webpush-channel-subscription-flow]]. After the cookie expires, the subscription itself is still valid; the cookie just gates the popup, not the subscription.

### Storefront init payload — exact shape

When the channel is configured and active, the platform injects this `renderSf` payload into every storefront page:

```
{
  VapKey: "<platform VAPID public key>",
  PushAllow: <bool — derived from checkout/popup_status logic>,
  CookieLifeTime: <int — clamped to [1, 365]>,
  overlay: { PushMessage: "<message text>" },
  popup: {
    image: "<popup_image or logo>",
    text: "<popup_text>",
    discardButton: "<popup_discard_button>",
    okButton: "<popup_ok_button>"
  }
}
```

The storefront's service worker reads this config and orchestrates the popup → native-prompt → subscribe-endpoint POST flow.

### Settings persist across channel reinstall

The popup settings (`checkout`, `popup_status`, `popup_text`, etc.) are stored under the channel's user settings and persist across channel uninstall/reinstall — uninstalling the Web Push channel does not wipe the merchant's popup configuration (verify).

## Related

- [[marketing-channels-webpush]] — hub.
- [[webpush-channel-subscription-flow]] — what happens after the customer clicks Allow on both prompts.
- [[webpush-channel-vapid-config]] — the `VapKey` public key injected into the init payload.
- [[webpush-channel-browser-support]] — which browsers / OS combos honour the native prompt at all.
- [[checkout-flow]] — the `checkout.return` route is where the popup fires when `checkout = true`.
- [[marketing-channels]] — parent channels hub.

## Open questions

- ⏸️ Whether resetting the channel (uninstall → reinstall) wipes the popup settings — assumed preserved like Email's `unconfirmed_send`, but not directly verified.
