---
type: feature
nav_path: "Apps → Fast Order → Settings"
route_name: apps.fast_order.settings
route_path: /admin/apps/fast_order/settings
aliases: ["Fast Order Settings", "Quick Order config"]
tags: [apps, others, fast-order, settings, conversion]
plan_gates: ["checkout"]
created: 2026-05-21
updated: 2026-05-26
source_count: 4
---
# Fast Order → Settings

## Purpose

The **Settings** tab is where the merchant configures the **button title + display behaviour** for the Fast Order one-click-purchase module. See [[apps-fast-order]] for the full feature set.

## Where to find it

Sidebar → Apps → Fast Order → **Settings tab**. Route: `/admin/apps/fast_order/settings`.

## What the merchant can do here

### Configuration

| Field | Notes |
|---|---|
| **Button title** (`button_title`) | The text shown on the storefront's Fast Order button (default: localised `fast_order.info.title`). |
| **Display on product pages** | Toggle the button visibility per page type. |
| **Default order status** | What status to set on new fast-orders (typically Pending). |
| **Default payment method** | Auto-set on new fast-orders (typically COD). |
| **Required fields** | Customer fields required in the fast-order popup (Name / Phone / Address minimum). |

### Render output

Per [[apps-fast-order]] Manager `render`: returns the rendered button view (the platform code template) using the configured `button_title`.

### What the merchant CANNOT do here
- Use Fast Order with online payment providers (designed for COD).
- Display on cart page (product-page only).
- Override fields per-product.

## Settings & fields

Per [[apps-fast-order]]: the configured check validates that `button_title` (or its default fallback) is available.

## Business rules

### Title default fallback

When the merchant hasn't set a custom title, the platform falls back to the localised translation `fast_order.info.title`.

### Fast Order filter on orders list

Orders placed via Fast Order are flagged + can be filtered on [[orders]] list via the "Fast order" filter (Yes / No).

### Permission
Standard apps permission scope.

## Related

- [[apps-fast-order]] — hub.
- [[orders]] — orders list with Fast Order filter.
- [[settings-cart]] — cart settings that interact with this flow.

## How it works (verified against backend)

### Configurable fields — toggles, not full granularity

The merchant can only toggle three optional fields ON/OFF (email is always-required):
- `require_phone` (switch).
- `require_first_name` (switch).
- `require_last_name` (switch).

There is NO per-product override — the field requirements are store-wide.

### Two required button strings

When `active = 1`, BOTH `button_title` AND `finish_button_title` are required to save. The two are different buttons:
- `button_title` — the storefront button on the product page.
- `finish_button_title` — the "Confirm order" button inside the popup.

### Facebook Pixel event configuration

Two configurable Pixel event names:
- **`initiate_checkout_method_name`** — `InitiateCheckout` (default) or `InitiateFastCheckout`.
- **`initiate_purchase_method_name`** — `Purchase` (default) or `FastPurchase`.

This lets the merchant separate Fast Order conversion tracking in their Pixel analytics.

### Rich-text intro shown in the popup

The `fast_order_description` setting (rich text editor in Settings) shows the merchant's custom explanation text at the top of the popup.

### Strictly COD

Per [[apps-fast-order]] — the flow is hard-coded to COD. There is no merchant setting to use Stripe / PayPal / etc.

### Button titles are single-string fields, not per-language

`button_title` and `finish_button_title` are stored as one string each. The settings form does not expose a per-language editor. On multi-language stores, whatever the merchant types appears verbatim on every storefront language; the merchant can leave `button_title` empty to fall back to the localised default (`fast_order.info.title`).

### Two extra fields saved by the settings page

Beyond the documented fields, two more configurable strings are saved:
- **`fast_order_description`** — rich-text intro shown at the top of the popup.
- **`order_made_message`** — message shown to the customer in the success panel after the order is placed (default: blank).

The merchant configures both as rich-text via the settings page; both are saved in the same controller's `$only` whitelist.

### Plan gate at the order endpoint, not at settings save

The settings page itself has NO plan check — the merchant can configure Fast Order settings on any plan. The plan gate (the platform code) fires only when a customer attempts to place a Fast Order. So a frozen / suspended store's Fast Order button still renders but submission fails with *"Checkout disabled"*. See [[apps-fast-order]] § "Plan-tier gate".

### No CAPTCHA / anti-spam in this app

The Fast Order settings page does NOT expose any CAPTCHA toggle, reCAPTCHA configuration, or rate-limit knob. The submit endpoints validate the form fields and the banned-customer state but do not gate on bot-detection. Merchants who need anti-spam protection on this flow should add it upstream (Cloudflare WAF / bot management on their account).

## Open questions

All previously-flagged questions resolved. See body sections.
