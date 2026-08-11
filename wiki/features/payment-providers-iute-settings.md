---
type: feature
nav_path: "Payment Providers → Iute → Settings"
route_name: apps.iute.settings
route_path: /admin/payment-providers/iute/settings
aliases: ["Iute Settings", "Iute Credit settings", "Настройки Iute", "Иуте настройки"]
tags: [paymentproviders, payment-providers, iute, bnpl, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Settings

## Purpose

The Settings tab for Iute is the credential surface — the merchant picks their **country** (one of five), enters two API keys per environment (storefront + admin), and optionally turns ON a **product-page promo button** that injects Iute's `iutepay.js` module on every product page. The mode switch (test vs live) flips between the two credential sets but doesn't erase the inactive one.

## Where to find it

Sidebar → **Payment Providers** → **Iute** → **Settings** tab.

The route is `/admin/payment-providers/iute/settings`. The page renders `SettingsFormPayments` with the `iute` provider key and three settings boxes: **Iute live settings** (or **Iute test settings**, depending on mode), and **Iute promo button settings**.

## What the merchant can do here

- Pick the **Country** Iute operates the merchant under (BG / AL / BA / MK / MD).
- Toggle the **Test mode switch** to flip between editing live and test credentials. The inactive box is hidden.
- Enter **API key** (storefront-scoped) for the active mode.
- Enter **Admin API key** (catalog-management-scoped) for the active mode.
- Toggle **Show button in product page** (`promo_button`) — when ON, Iute's promo module is rendered on every product detail page.

## Settings & fields

### Credentials (per environment)

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Country** | Determines the API base URL: `ecom.iutecredit.{country_tld}`. | None | Required (server message: `"Country is required"`). Searchable dropdown — literal display names in the picker: `Bulgaria` (BG), `Albania` (AL), `Bosnia and Herzegovina` (BA), `Macedonia` (MK — labelled just "Macedonia" in the picker, though the country is officially "North Macedonia"), `Moldova` (MD). The country field renders in BOTH the live and test settings boxes (whichever is visible based on the active mode). |
| **API key** (live or `_test`) | Storefront-scoped key. Sent as `x-iute-api-key` HTTP header in calculation requests. | Empty | Required in the active mode (`required_if`). Server message: `"Api key is required"`. On save, CloudCart calls Iute's calculation endpoint with a dummy 250-amount sample to verify the key; if Iute returns a an error the merchant sees `"Invalid api key"`. |
| **Admin API key** (live or `_test`) | Catalog-management-scoped key. Sent as `x-iute-admin-key` HTTP header in loan-product / mapping / status requests. | Empty | Required in the active mode (`required_if`). Server message: `"Admin api key is required"`. On save, CloudCart calls Iute's `/api/v1/eshop/management/loan-product` endpoint to verify the key; if it fails the merchant sees `"Invalid admin api key"`. |
| **Test mode switch** | Toggles which credential set is active. | test | Both sets saved simultaneously. |

### Promo button

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Show button in product page** (`promo_button`) | Injects Iute's `iutepay.js` module on every product page, showing "from {monthly} / month" + a clickable button that starts Iute's fast-checkout flow. | OFF | Switch (`trueValue: 1`, `falseValue: 0`). |

## Business rules

### Credential validation on every save

On save, the platform validates the API key and admin API key separately:

- API key — POSTs to `/api/v1/eshop/client/eshop-product/-/calculation?monthly=true` with a sample payload `[{id: 1, sku: 1, amount: 250}]`.
- Admin API key — GETs `/api/v1/eshop/management/loan-product`.

A failure on either call adds an error to the respective field. The merchant cannot save unusable credentials.

### Base URL is derived from country + mode

The base URL is constructed as:

```
'https://ecom' . (mode == test ? '-stage' : '') . '.iutecredit.' . country_tld
```

Country TLDs: `bg`, `al`, `ba`, `mk`, `md` (uppercase in the config; lowercased for the URL). Anything else falls back to `bg`. The `mode` config controls whether the URL includes the `-stage` suffix.

### Mode switch keeps both sets

Switching modes does NOT erase the inactive credential set — both `api_key` / `admin_api_key` and `api_key_test` / `admin_api_key_test` are stored simultaneously. The mode just changes which is sent to Iute.

### Default test configuration is empty

There are no default test credentials shipped — the merchant must request a test key pair from Iute to use the test mode at all.

### Promo button — runtime effects

When ON, the storefront theme renders `creditor_pricing_table.blade.php` on the product page, which:

1. Includes Iute's CSS + JS from `ecom{-stage}.iutecredit.{tld}/iutepay.js`.
2. Renders an `<div id="iute-trigger" class="iute-as-low-as">` with the product ID + price as data attributes.
3. Calls `iute.openPromoWindowModal($btn[0])` so clicking the trigger opens Iute's modal.
4. Registers `iute.onFastCheckout` — on completion, appends `leasing-options-provider=iute` + `payment_variant_id=3` to the add-to-cart form and submits.

The merchant doesn't need to add any HTML to their theme — CloudCart's storefront engine inserts the right snippets when `promo_button = 1`.

### Plan-gating

Not plan-gated by CloudCart subscription tier.

## Related

- [[payment-providers-iute]] — parent hub for Iute.
- [[payment-providers-iute-schemes]] — per-product loan-product mappings on Iute's catalog.
- [[payment-providers]] — top-level Payment Providers area.
- [[payment-providers-klear-settings]] — Klear's equivalent (public + private API key per environment, similar shape).

## Open questions

- ⏸️ Whether a single Iute reseller relationship can span multiple country endpoints — a commercial Iute-side question not encoded in CloudCart. Each country (BG, AL, BA, MK, MD) hits a different Iute endpoint domain, so credentials are issued per-country.
- ⏸️ Country-specific variant ID mapping for the promo button — the default `payment_variant_id=3` aligns with Iute's "3 installments" variant in the standard catalogue, but Iute may publish different variant IDs per country. If the wrong default variant appears, contact Iute for country-specific mapping.
