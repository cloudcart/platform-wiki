---
type: feature
nav_path: "Payment Providers → Fusion Pay → Settings"
route_name: apps.fusion_pay.settings
route_path: /admin/payment-providers/fusion_pay/settings
aliases: ["Fusion Pay Settings", "TBI Pay settings", "TBI tiers settings", "Настройки Fusion Pay", "ТБИ Пей настройки"]
tags: [paymentproviders, payment-providers, fusion-pay, tbi-bank, bnpl, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Settings

## Purpose

The Settings tab for Fusion Pay is the deepest configuration surface among CloudCart's BNPL integrations — the merchant manages **two parallel credential sets** (test + live), an **installment period range** (min/max/step), a **promotional product-page button** with up to three custom-period tiers, and free-leasing display options. The reseller credentials come from TBI Bank at reseller sign-up; the period and button settings shape what customers see on product pages and in checkout.

## Where to find it

Sidebar → **Payment Providers** → **Fusion Pay** → **Settings** tab. Route: `/admin/payment-providers/fusion_pay/settings`.

Controls are grouped into boxes: **TBI live settings**, **TBI test settings**, **TBI period settings**, **TBI free lease settings**, and **TBI tiers** (promo-button configuration).

## What the merchant can do here

- Toggle the **Test mode switch** (top of the page) to edit test or live credentials — only the active mode's box is shown.
- Enter the active mode's **Reseller code**, **Reseller key**, **Encryption Key**, plus the live-set **Currency** (EUR or RON).
- Set the **Amount from / Amount to** order-total range and either the **TBI Calculator** module or the **Min / Max / Step period** for installment plans.
- Enter a **Title for interest-free leases** and toggle **Discounted products** and **TBI tiers** (`promo_button`).

See the field tables below for defaults and validation.

## Settings & fields

### Credentials (test or live, depending on mode)

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode switch** | Switches which credential set is active. | test | Both sets are saved — switching only changes which is used. |
| **Reseller code** (live or `_test`) | Identifier for the merchant in TBI's reseller registry. | Empty | Required in the active mode. Message: `"Reseller code is required"`. |
| **Reseller key** (live or `_test`) | Authentication key paired with the reseller code. | Empty | Required in the active mode. Message: `"Reseller key is required"`. |
| **Encryption key** (live or `_test`) | Used by TBI to sign or verify requests. | Empty | Required in the active mode. Message: `"Encryption key is required"`. |
| **Currency** (live mode only) | Settlement currency the merchant works in with TBI. | None | Required. Dropdown of `EUR` and `RON`. |

### Order amount range (shared with the overview tab)

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Amount from** | Minimum order total at which Fusion Pay shows on checkout. | None | Required. Between **52** and **15000** (TBI's regulatory limits). Messages: `"Amount from must be at least 52"` / `"Amount from must be at most 15000"`. |
| **Amount to** | Maximum order total at which Fusion Pay shows on checkout. | None | Required. Between **52** and **15000**, and **greater than Amount from**. |

### Period range — when TBI Calculator is OFF

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **TBI Calculator** | When ON, TBI's iframe module handles period selection and the three fields below are hidden. | OFF | Switch. Hides `min_period` / `max_period` / `step_period`. |
| **Min period** | Lower bound (months) of the period range. | Empty | Required when calculator is OFF. Min 3, max 60. |
| **Max period** | Upper bound (months) of the period range. | Empty | Required when calculator is OFF. Min 3, max 60. |
| **Step period** | Increment between selectable periods; only periods where `(period − min_period) mod step_period = 0` are offered. | Empty | Required when calculator is OFF. Min 3, max 60. |

### Free leasing

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Title for interest-free leases** | Heading the customer sees above the 0%-interest plans block in the pricing table. | Empty | Required when calculator is OFF. Plain text. |
| **Discounted products** | When ON, products with an active CloudCart discount are excluded from free-leasing offers (TBI's `is_promo = 0` plans only). | OFF | Switch. |

### TBI tiers (promo button on product page)

The tier section is a **mini-wizard inside the Settings tab**. Flipping the `promo_button` switch ON makes CloudCart fetch TBI's tier multipliers and add one number-input per returned tier (`tier_1`, `tier_2`, `tier_3`), each labelled with the live TBI data.

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **TBI tiers** (`promo_button`) | Master switch — when ON, fetches TBI's tier multipliers and renders tier inputs; OFF hides them. | OFF | Switch (`trueValue: 1`, `falseValue: 0`). |
| **"No predefined leasing schemes" warning** | If `promo_button` is ON but TBI returns zero tiers, a slide-up panel renders: *"There are no predefined leasing schemes added to the account."* with an **Update leasing schemes** button to retry. | Hidden | Usually means TBI hasn't activated the tier feature on the merchant's reseller account; the merchant contacts TBI. |
| **Period for button (tier N)** (one per returned tier) | Months that tier's button uses. Label: *"Period for button (to {amount_format}) — Monthly interest rate: {percent}"*, where `{amount_format}` is the TBI max order amount for the tier and `{percent}` its monthly multiplier. | TBI's recommended period (typically 12 / 48 / 60 for tiers 1 / 2 / 3) | Number input. Range 3-60. Visible only when `promo_button` = 1; auto-populated from TBI. |
| **Select button for product page** (`promo_button_id`) | Picks one of four button visual styles, shown as a radio group with mock-up previews ("Buy with [Fusion Pay logo] / 3 installments of BGN 123.40"): orange background (white logo), black background (white logo), white background (black logo), and a tinted variant. | None | Radio. Visible only when `promo_button` = 1. Saved as `configuration.promo_button_id`. |

## Business rules

### Two parallel credential sets

The merchant maintains both test and live credentials simultaneously. The **mode** switch picks which set is active for the storefront. Switching modes does NOT erase the inactive set — the merchant can flip back. This is the same pattern as Revolut / Stripe in CloudCart.

### Tier multipliers are re-fetched on save

On save, CloudCart re-fetches the tier data (saved as `tierSettings`) whenever **any** of the three tier periods (`tier_1`, `tier_2`, `tier_3`) is present in the submitted configuration — not only when `promo_button` is on, so changing a period value alone triggers a fresh fetch. The `promo_button` flag only controls whether the storefront button renders. TBI returns per-tier max order amounts and monthly-rate multipliers (as percentages), cached so the button shows amount/rate labels without re-calling TBI on every page load. _(verified)_

### Period filtering at checkout

At checkout, CloudCart filters TBI's returned variants by:

1. `amount_min ≤ price ≤ amount_max`
2. `period ≥ min_period` and `period ≤ max_period` (each if configured)
3. `(period − min_period) mod step_period = 0` (if `step_period` configured)
4. Category match (the product's category must be in the variant's eligible-categories list)

If `free_leasing_for_discounted_products = 1` and any cart product has an active discount, the filter additionally drops `is_promo = 1` variants (so the customer can't double-stack a coupon discount with TBI's 0% promo).

### Endpoint and plan-gating

Both `live` and `test` endpoints share the same TBI base URL — the mode switch only changes which credential triple is sent. Not plan-gated.

## Related

- [[payment-providers-fusion-pay]] — parent hub for Fusion Pay.
- [[payment-providers-fusion-pay-schemes]] — per-product TBI free-leasing scheme mapping.
- [[payment-providers-tbi]] — the legacy TBI integration (no API, local rate calculation only).
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

_None._
