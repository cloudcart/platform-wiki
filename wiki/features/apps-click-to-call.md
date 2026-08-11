---
type: feature
nav_path: "Apps → Click to Call"
route_name: apps.click-to-call.overview
route_path: /admin/apps/click-to-call
aliases: ["Click to Call", "Phone module", "Call button", "Натисни за обаждане", "enable disable button", "app active toggle"]
tags: [apps, marketing, conversion, phone, module]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# Click to Call (phone module)

## Purpose

**Click to Call** integration — adds a floating phone-button module to the storefront. When a customer clicks it, their browser / phone opens a dialer with the merchant's contact number pre-filled. Used by merchants who:

- Want to capture customers who prefer phone orders over digital checkout.
- Run high-touch sales (custom-quote items, B2B negotiations).
- Want a fast support contact path for new customers who get stuck.

The module is a floating circular button, customisable per position (left / right) and colour. The customer sees the merchant's text (e.g., "Call us") + a phone icon.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so it can be switched off without uninstalling it. A disabled app stops working while keeping its settings.

## Where to find it

Sidebar → Apps → install → **Click to Call**. Two sub-pages:

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.click-to-call.overview` |
| Settings | `apps.click-to-call.settings` |

## What the merchant can do here

### Settings

| Field | Notes |
|-------|-------|
| **Contact phone number** | Phone input with country code picker. The phone the button dials. |
| **Position** | Radio: Left / Right — which side of the screen the floating button anchors to. |
| **Text** | Custom button text (e.g., "Call us", "Свържи се"). |
| **Background color** | Button color theme. |
| **Live preview** | Shows the button as it will render on the storefront. |

### Overview
Activate / deactivate the module.

### What the merchant CANNOT do here
- Use multiple phone numbers per language / segment — single number per store.
- Track call analytics inside CloudCart (no built-in call tracking — the merchant uses external call-tracking software).

## Settings & fields

Manager exposes the configured check — verifies phone number is set and valid.

The Vue settings page uses `CcSettingsBox` with a custom `#btnPreview` slot for live button preview.

## Business rules

### Floating module injected via app activation

Once activated, the module injects on EVERY storefront page (not just the checkout). The merchant can disable it from Overview to remove it everywhere.

### Phone input validation

The `CcPhoneInput` component validates the number format (country code + valid digits). Invalid numbers can't be saved.

### Position is global

Left / Right setting applies to the entire storefront. No per-language / per-page override.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-mailchimp]] / [[apps-bumpcart]] — sister Marketing apps.
- [[settings-brand]] — brand colours that the merchant may want to match.
- [[settings-translations]] — translatable button text per storefront language.

## How it works (verified against backend)

### 6 required settings

ALL SIX must be non-empty for the module to render:
- `text` — button text (e.g., "Call us").
- `background_color` — module background color (hex).
- `button_background_color` — call-to-action button background color.
- `button_font` — button font choice.
- `phone` — the phone number to call.
- `position` — module screen position (e.g., bottom-right).

So the merchant MUST fully style the module AND provide a phone number before the app activates. **No graceful defaults** — the integration is binary: fully configured or inactive.

### Storefront-only module integration

The integration is minimal — just an install/uninstall lifecycle plus the configured-check. The module renders via a Smarty/Vue template directly consuming the settings.

### Sensible default colours and position before saving

Although the configured check requires all six fields, the Manager pre-fills four sensible defaults:

- `background_color` → white (`#ffffff`).
- `button_background_color` → black (`#000000`).
- `button_font` → 12 px.
- `position` → `left`.

So in practice the merchant only needs to type their phone number and button text — the styling defaults render a usable module immediately. Font size is clamped to **10–25 px** in the settings UI.

### Color pickers (not raw hex)

Both colour fields render as proper colour-picker inputs in the settings UI (`type: 'color'` in the Vue settings schema), not raw hex text boxes. The merchant clicks a swatch and picks visually.

### Single phone number, single button text, single position — global to the storefront

There is one phone number, one button text, one position, one colour scheme per store. Click-to-Call is intentionally minimalist and does not expose:

- Per-language button text (the text is stored as one string; switching the storefront's language does not change it).
- Mobile-vs-desktop hide / show toggles (the module renders the same way on every device).
- Operating-hours scheduling (no "auto-hide outside business hours" — the merchant has to deactivate the app manually).
- Click analytics inside CloudCart (the platform does not log how many visitors tapped the button; merchants who need call analytics must use an external call-tracking number).
- Multiple phone numbers per language / segment / store location.

If the merchant needs WhatsApp / Viber / Messenger instead of a phone call, they use a separate app (Live Chat / Facebook Messenger integration), not this one.

### Uninstall wipes ALL settings — different from disable

Calling Uninstall on Click-to-Call runs `emptySettings` + `setInactive` — the merchant's phone number, position, colours, and button text are ALL deleted. Re-installing means re-typing everything. Compare to other apps (Live Chat, Mailchimp) which preserve settings across uninstall/install for one-click re-enable.

### App JS bundle regenerated on every settings save

Click-to-Call implements `AppJsRegenerate` — saving any setting (even just changing the position from left to right) regenerates the storefront's combined apps JS bundle. Visitors get the new config without a cache flush.

### Phone number stored as plain string

The `phone` setting stores whatever the merchant types — there's NO server-side phone-format validation in the SettingsRequest. The validation happens in the Vue `CcPhoneInput` component (country code + format check). A merchant who bypasses the Vue UI (e.g., through a custom API call) can save a non-numeric string, and the storefront's `tel:` link will fail when clicked.

## Open questions
