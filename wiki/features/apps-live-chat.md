---
type: feature
nav_path: "Apps → Live Chat"
route_name: apps.live-chat.overview
route_path: /admin/apps/live-chat
aliases: ["Live Chat", "Generic Live Chat", "Chat module", "Чат на живо"]
tags: [apps, others, chat, support, conversion]
plan_gates: []
created: 2026-05-22
updated: 2026-05-26
source_count: 2
---
# Live Chat (generic chat module)

## Purpose

**Live Chat** integration — embeds the **LiveChat (livechat.com / livechatinc.com)** module on the storefront. The merchant supplies their LiveChat **license key** (a numeric ID from LiveChat's dashboard) and CloudCart loads the LiveChat tracking script (`cdn.livechatinc.com/tracking.js`) on every storefront page.

Despite the generic name, this integration is hard-wired to LiveChat specifically — not a paste-any-snippet field. For pasting an arbitrary chat snippet, see [[apps-zopim]] (which despite its name accepts any embed code).

## Where to find it

Sidebar → Apps → install → **Live Chat**. See [[apps-live-chat-settings]] for configuration.

## What the merchant can do here

- Enter their **LiveChat license key** (the numeric ID from `https://my.livechatinc.com/`).
- Activate / deactivate.

### What the merchant CANNOT do here
- Configure operators, availability, branding, or theming — those live in LiveChat's own admin at `my.livechatinc.com`.
- Use a non-LiveChat chat product through this integration — the JS hard-codes `cdn.livechatinc.com/tracking.js`.
- Pre-identify logged-in customers (no automatic identify call from CloudCart).

## Settings & fields

Manager exposes:
- the configured check — checks the `live_chat` setting is non-empty (the license key).

Single field. Validation message: *"License key is required"* (when activating without a key).

## Business rules

### Tied to LiveChat (livechatinc.com)

The integration only works with LiveChat. The JS sets `window.__lc.license` to the merchant's key, tags `integration_name = "cloudcart"`, and loads LiveChat's tracking.js asynchronously.

### Cookie consent integration

Chat modules typically set cookies. When [[apps-gdpr-overview]] is active, the merchant should ensure their chat platform respects consent state (configured in the platform's admin, not here).

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-live-chat-settings]] — settings sub-page.
- [[apps-zopim]] — generic "paste your chat snippet" alternative (works with any chat platform).
- [[apps-click-to-call]] — alternative customer-contact module (phone-based).
- [[apps-gdpr-overview]] — cookie consent affects chat module loading.

## How it works (verified against backend)

### Single field: LiveChat license key

The merchant enters one value — the LiveChat license number. CloudCart accepts whatever non-empty string is given; there is no format validation beyond "not blank when active". Validation message *"License key is required"* fires only if the merchant activates the app without a value.

### Storefront loads LiveChat tracking.js async

When the app is active, CloudCart's storefront bundle assigns `window.__lc = { license: <key>, integration_name: "cloudcart", product_name: "livechat" }` and then injects a `<script>` pointing at `https://cdn.livechatinc.com/tracking.js`. The module loads on every storefront page.

### No per-page toggle, no checkout exclusion

The integration is binary — on for the whole storefront, or off. There is no UI to hide the module on specific pages (including checkout).

### No automatic customer identification

CloudCart does not call LiveChat's identify methods on behalf of logged-in customers. The visitor appears anonymously to the agent unless they fill in the module's pre-chat form themselves.

### Loads asynchronously, regenerated on settings change

The Live Chat manager implements `AppJsRegenerate` — saving settings triggers a regeneration of the storefront's combined apps JS so the new license key is picked up without a manual cache flush.

### Field naming inconsistency: setting is `live_chat` (not `license_key`)

The setting stored in the database is keyed `live_chat`, not the more obvious `license_key` or `livechat_license`. The settings form labels it as "License key" to the merchant, but the underlying field is just `live_chat` — a vestige from when the integration was named differently. Merchants writing automation against the settings API need the `live_chat` key.

### No multi-snippet support

There is exactly one stored value (`live_chat`). Chat platforms requiring two or three separate scripts cannot be wired in through this app.

## Open questions
