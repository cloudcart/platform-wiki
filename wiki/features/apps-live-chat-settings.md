---
type: feature
nav_path: "Apps → Live Chat → Settings"
route_name: apps.live-chat.settings
route_path: /admin/apps/live-chat/settings
aliases: ["Live Chat Settings", "Generic chat module config"]
tags: [apps, others, live-chat, settings, module]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 2
---
# Live Chat → Settings

## Purpose

The **Settings** tab is where the merchant enters their **LiveChat license key** (from livechatinc.com). The integration is LiveChat-specific despite the generic page name — see [[apps-live-chat]] for the full feature set.

## Where to find it

Sidebar → Apps → Live Chat → **Settings tab**. Route: `/admin/apps/live-chat/settings`.

## What the merchant can do here

### Configuration

| Field | Notes |
|---|---|
| **License key** (`live_chat`) | The numeric LiveChat license ID from `my.livechatinc.com`. Required when activating. |

Per [[apps-live-chat]] Manager: the configured check checks the `live_chat` setting is non-empty.

### What the merchant CANNOT do here
- Configure operators, hours, theming — handled in LiveChat's own admin.
- Plug in a different chat platform — the storefront JS hard-codes LiveChat's tracking URL.
- Disable on specific pages — site-wide toggle only.

## Settings & fields

Single text field — `live_chat` (string). Stored as-is and used as `window.__lc.license`.

## Business rules

### Tied to LiveChat (livechatinc.com)

Saving any value here causes the storefront to load `https://cdn.livechatinc.com/tracking.js` with that value as the license. Pasting a snippet from a different platform will not work — the snippet is not echoed verbatim.

### Cookie consent integration

The LiveChat module sets cookies. When [[apps-gdpr-overview]] is active, the merchant should configure consent state inside LiveChat's own admin.

### Permission
Standard apps permission scope.

## Related

- [[apps-live-chat]] — hub.
- [[apps-zopim]] — generic "paste any chat snippet" alternative.
- [[apps-click-to-call]] — alternative customer-contact module (phone-based).
- [[apps-gdpr-cookies]] — cookie consent affects module loading.

## How it works (verified against backend)

### No syntax validation

The license-key value is stored without format checking — any non-empty string passes. If the merchant enters something LiveChat doesn't recognise, the module simply fails to load (no CloudCart-side error message).

### Storefront JS bundle regenerates on save

The Live Chat manager implements `AppJsRegenerate` — saving settings updates the storefront's apps JS so visitors pick up the new license key without a cache bust.

### No multi-snippet field

Exactly one value is stored. There is no second field for an optional secondary snippet or a separate chat-bot script.

### No per-page toggle

The module is loaded site-wide via `window.CCAppsConfig.live_chat` whenever the app is active. Hiding it on checkout or a specific page would require custom storefront code.

### No automatic customer identify call

CloudCart only sets `window.__lc.license`. It does not call LiveChat's identify API to attach the customer's email or name. The merchant must add identify logic themselves via custom theme code if they need it.

## Open questions
