---
type: feature
nav_path: "Apps → Zopim → Settings"
route_name: apps.zopim.settings
route_path: /admin/apps/zopim/settings
aliases: ["Zopim Settings", "Zendesk Chat config"]
tags: [apps, others, zopim, chat, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 2
---
# Zopim → Settings

## Purpose

The **Settings** tab is where the merchant enters their **Zopim (Zendesk Chat) account ID** for module injection. See [[apps-zopim]] for the full feature set.

## Where to find it

Sidebar → Apps → Zopim → **Settings tab**. Route: `/admin/apps/zopim/settings`.

## What the merchant can do here

### Configuration

| Field | Notes |
|---|---|
| **Code** (`code`) | The merchant pastes the **entire Zopim / Zendesk Chat embed snippet** (the `<script>` block Zopim provides). Required when the app is activated. |

There is no separate "account ID" field, no position/colour picker, no display-preferences UI on the CloudCart side — those live in Zendesk's own admin.

### Validation

- *"Code is required"* — when activating the app without pasting any snippet.

There is no syntactic validation of the snippet itself — it is stored as-is and echoed straight into `main.tpl` of the storefront.

### What the merchant CANNOT do here
- Configure operator availability / scheduling / branding (in Zendesk's admin).
- Add multiple Zopim instances on one store.

## Settings & fields

Per [[apps-zopim]]: single setting `code`, which holds the full Zopim embed JavaScript.

## Business rules

### Identical mechanic to [[apps-live-chat]]

This is the same "paste JS snippet" pattern as the generic [[apps-live-chat]] integration — the only difference is branding/copy. Functionally there is no Zopim-specific account-ID flow.

### Cookie consent integration

Zopim sets cookies. The merchant configures Zendesk's consent state to respect [[apps-gdpr-cookies]].

### Permission
Standard apps permission scope.

## Related

- [[apps-zopim]] — hub.
- [[apps-live-chat]] — generic alternative.
- [[apps-click-to-call]] — alternative phone-based contact.
- [[apps-gdpr-cookies]] — cookie consent.

## How it works (verified against backend)

### One free-form textarea, injected unescaped

The Settings UI exposes the single `code` field. Whatever the merchant pastes is stored verbatim and echoed into the storefront layout with `nofilter` (Smarty's "no HTML escaping"). The embed runs on every storefront page that uses `main.tpl`.

### No pre-identification of logged-in customers

CloudCart does not call Zopim's `$zopim.livechat.setName/setEmail` on behalf of logged-in customers. If the merchant wants pre-fill, they need to add the Zendesk identify code into their pasted snippet manually.

### No order-context push

When a customer opens the chat, CloudCart does not pass the current cart, last viewed product, or order ID to the Zendesk agent. The integration is purely a script tag.

### Settings page is a single textarea — no preview, no validation

The Zopim settings UI only exposes the `code` textarea. There is no:
- Snippet preview rendering before save.
- Validation that the pasted text is a valid `<script>` block.
- Test-connection action (since there's no Zendesk API call involved).

The merchant saves whatever they paste; verification happens on the storefront when they visit it.

### Operating-hours behaviour is Zopim-controlled

Auto-hide outside business hours is configured inside Zendesk Chat's own scheduler. CloudCart's settings have no scheduling controls.

## Open questions
