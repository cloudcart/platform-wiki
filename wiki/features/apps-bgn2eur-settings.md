---
type: feature
nav_path: "Apps → BGN to EUR → Settings"
route_name: apps.bgn2eur.settings
route_path: /admin/apps/bgn2eur/settings
aliases: ["BGN to EUR Settings", "Bgn2eur config", "Currency transition settings"]
tags: [apps, administration, bgn2eur, currency, bulgaria, settings]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# BGN to EUR → Settings

## Purpose

The **Settings** tab is where the merchant configures **dual-currency display** for the Bulgarian BGN → EUR transition, and where the one-time **Convert store prices to Euro** action lives. For the conversion mechanics, rate, currency gating and end-of-transition behaviour, see the hub [[apps-bgn2eur]] — this page covers only what the Settings tab itself exposes.

## Where to find it

Sidebar → Apps → BGN to EUR → **Settings tab**. Route: `/admin/apps/bgn2eur/settings`.

## What the merchant can do here

- Set `display_mode` — where dual currency renders (Storefront / Admin Panel / Both).
- Edit the conversion-message text and toggle its three storefront positions (checkout / cart / footer).
- Run the one-time **Convert store prices to Euro** action via a confirm modal.

### What the merchant CANNOT do here
- Change the conversion rate (fixed at 1 EUR = 1.95583 BGN — see [[apps-bgn2eur]]).
- Pick which currency is "primary" — that follows the **site currency**, not a setting here (see below).
- Use dual display outside a BGN/EUR store (currency gating, see [[apps-bgn2eur]]).

## Settings & fields

Two `CcSettingsBox` rows, both `editMethod: inline` (fully expanded, no Edit click):

| Box | Title | Fields |
|---|---|---|
| **BGN 2 EUR Settings** | Display config | `display_mode` (select: Storefront / Admin Panel / Both), `conversion_message` (text), `conversion_message_position_footer` / `_cart` / `_checkout` (3 switches). |
| **Convert store prices to Euro** | (no title) | Slot rendering the Convert button + status text. Box description: *"Here you can convert the store prices from BGN to Euro."* |

Setting keys, accepted values and defaults are tabled in [[apps-bgn2eur]].

## Business rules

- **Defaults make the app work on install.** The configured check returns true unconditionally; the shipped defaults (`display_mode = both`, official conversion message, all three positions on) are enough, so the merchant need not set anything for the app to start working.
- **Display-mode change is presentational only.** It does not write to product prices, taxes or shipping — see [[apps-bgn2eur]] for what the Convert action rewrites.
- **Cache flush, currency gating, past-order display** — all inherited from the hub [[apps-bgn2eur]]; not re-stated here.
- **Permission:** standard apps permission scope.

## Related

- [[apps-bgn2eur]] — hub (rate, conversion mechanics, currency gating, end-of-transition).
- [[settings-general]] — store country (Bulgaria requirement for app activation).
- [[orders-shipping-waybill]] — waybill EUR variant hard-block after 2026-01-01.
- [[orders-details]] — "Convert prices to EUR" sidebar button.

## How it works (verified against backend)

### `display_mode` controls WHERE dual rendering happens, not which currency is "primary"

The three accepted values decide the surface, not the lead currency:

- **`storefront`** — dual rendering on the customer-facing site and theme builder; admin panel stays single-currency.
- **`admin_panel`** — dual rendering in the admin panel and builder; the customer-facing site stays single-currency.
- **`both`** — dual rendering everywhere.

Validation rejects anything else (*"Display mode must be one of: storefront, admin_panel, both"*). Earlier drafts that listed "BGN primary / EUR primary / Single currency" were wrong. Which currency is "first" follows the **site currency** (`site('currency')`), not this setting: a BGN store leads with BGN, and the order reverses automatically after the [[apps-bgn2eur]] Convert action flips the site currency to EUR.

The shipped default is `both` (set in the install defaults). A separate fallback of `storefront` applies only when no setting exists at all, so new installs always start with dual rendering in admin + storefront + builder.

### Conversion message: text + three positions

The **Currency conversion message** is free text up to 1,000 characters (validation: *"Currency conversion message cannot exceed 1000 characters"*), defaulting to *"1 EUR = 1.95583 BGN"*. Merchants commonly rewrite it with a longer Bulgarian reassurance text. It renders alongside dual prices at three independently-toggled positions, each defaulting on:

- **Checkout** — `conversion_message_position_checkout`.
- **Cart** — `conversion_message_position_cart`.
- **Footer** — `conversion_message_position_footer`.

### Client-side dual rendering needs `storefront` or `both`

In `admin_panel` mode the storefront JS does **not** include live dual rendering for variant pickers, quantity updates or discounted-price overlays. Choose `storefront` or `both` to make those render dual values live. Note the JS dual-render check inspects only currency + display mode and does **not** re-check that the app is active — so if a merchant disables the app while the JS bundle is still cached, dual currency may keep rendering client-side until the bundle regenerates.

### Convert-to-Euro button + confirm modal

The Convert box (second row on this page) hosts the one-time **Convert store prices to Euro** action:

1. The button is **disabled** when `convert2eur > 0` (already started or completed) — preventing duplicate runs.
2. Clicking opens a confirm modal titled "Convert store prices to Euro", body *"Are you sure you want to convert your store prices to Euro?"*, with the warning *"Conversion job of your store prices to Euro will be started. Your store will be unavailable during the conversion. You will be notified by email when the conversion is completed. This action cannot be undone."*
3. Cancel closes it; OK fires the migrate-to-euro mutation.
4. On success `convert2eur` flips to 1 and the inline note turns yellow: *"Conversion job of your store prices to Euro has been started..."*.
5. When the backend completes, the value becomes 2 (sticky) and the note turns green: *"Conversion of your store prices to Euro has been completed successfully."*.

Once `convert2eur` is 1 or 2 the modal cannot reopen and the button stays disabled. What the conversion actually rewrites, the maintenance-mode flow and the no-undo rule are documented in [[apps-bgn2eur]].

## Open questions
