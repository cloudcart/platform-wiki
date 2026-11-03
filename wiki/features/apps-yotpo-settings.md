---
type: feature
nav_path: "Apps → Yotpo → Settings"
route_name: apps.yotpo.settings
route_path: /admin/apps/yotpo/settings
aliases: ["Yotpo Settings", "Yotpo config"]
tags: [apps, others, yotpo, reviews, ugc, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 4
---
# Yotpo → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to **Yotpo** — enters API credentials (App Key + Secret) for the review-platform integration. See [[apps-yotpot]] for the full feature set.

(Note: the parent wiki uses slug `apps-yotpot` due to historical typo — cross-reference both.)

## Where to find it

Sidebar → Apps → Yotpo → **Settings tab**. Route: `/admin/apps/yotpo/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **App Key** | Yotpo App Key from the merchant's Yotpo dashboard. |
| **App Secret** | Yotpo App Secret. Encrypted on storage. |

### Display options

| Setting | Notes |
|---|---|
| **Show on product pages** | Toggle Yotpo module on product detail pages. |
| **Show on category listings** | Toggle star-rating display on category cards (renders the star-only variant of the Yotpo module — see [[apps-yotpot]]). |
| **Show on home page** | Toggle homepage testimonials module. |

### Email outreach toggle

Yotpo's email-outreach feature requires permissions toggled here:
- **Auto-request reviews after order** — Yotpo emails customers post-purchase requesting reviews.
- **Days after delivery** — delay before the request email.

### What the merchant CANNOT do here
- Configure Yotpo's own behaviour (moderation rules, email templates) — done in Yotpo's admin.
- Use without an active Yotpo subscription.
- Migrate native reviews to Yotpo via this setting page (manual export/import required).

## Settings & fields

The Yotpo integration (per [[apps-yotpot]]) renders the Yotpo module on a product, with an optional compact star-only mode for listings.

## Business rules

### Replaces / supplements native reviews

When Yotpo is active, the merchant typically disables [[apps-product-review]] (native) to avoid duplicate review modules.

### Data lives on Yotpo's side

All reviews submitted via Yotpo module are stored in Yotpo's database, NOT CloudCart. The merchant manages them in Yotpo's admin.

### Permission
Standard apps permission scope.

## Related

- [[apps-yotpot]] — hub (note slug typo).
- [[apps-product-review]] — alternative native reviews.
- [[products-products]] — products where Yotpo module appears.

## How it works (verified against backend)

### Two required fields: App Key and App Secret

The settings form has exactly two required inputs: **App Key** and **App Secret** from the merchant's Yotpo dashboard. Both are required (errors: *"App Key is required"* / *"App Secret is required"*). There are no separate "show on product page / show on home page / email outreach" toggles — those are all configured in Yotpo's own dashboard, not here. The CloudCart side is purely a credential bridge.

### One listing-mode toggle: `show_in_listing`

The only other setting the merchant manages from this page is `show_in_listing` (boolean, default off). When on, the storefront renders the star-rating-only variant of the Yotpo module on category listings. When off, listings stay clean and Yotpo only loads on product detail pages.

### Side-by-side with native reviews

The Yotpo module renders alongside CloudCart's native [[apps-product-review]] if both apps are active — they do not collide because each module lives in its own template area on the product page. Two review modules stacking on one page is uncommon but supported.

### Photo / video reviews

CloudCart does not control whether photo or video reviews are enabled — that is configured in the merchant's Yotpo account. If the merchant has the corresponding Yotpo plan, their module will allow photo / video uploads when it renders on the storefront.

### Yotpo Loyalty integration

This app only integrates the **Reviews** module. Yotpo Loyalty (separate Yotpo product) is not supported by this CloudCart app — it requires a separate integration that does not ship today.

### GDPR cookie consent

The Yotpo module is loaded async on the product page. CloudCart does not gate Yotpo's script behind the platform's cookie-consent layer ([[apps-gdpr-overview]]) — if the customer rejects social / marketing cookies, the Yotpo module still loads. Merchants in strict GDPR jurisdictions should consider this when choosing between Yotpo and the native [[apps-product-review]] app.

### `app_secret` saved but UNUSED at runtime

The settings page requires both `app_key` and `app_secret` to save, but only `app_key` is actually used by the integration's render and tracking methods. See [[apps-yotpot]] § "`app_secret` collected but UNUSED".

### `show_in_listing` is OFF by default

By default, the listing-star toggle is OFF on first install. Merchants must enable it explicitly if they want star ratings on category pages — preserving listing load speed by default.

### Conversion tracking on order completion

Beyond the on-page review module, the platform also renders a Yotpo `conversion-tracking` pixel on the order-success page, posting order id, customer email, customer name, currency, and per-product data (name, URL, image, description, price, brand, SKU, first tag). This feeds Yotpo's purchase-tracking so it can later email the customer asking for a review. The merchant does not configure this — it fires automatically when the app is active and configured.

### Settings layout — single slide-modal box

The form is a single box edited via a slide-modal:

| Storage key | Label in UI | Type | Help block |
|---|---|---|---|
| `app_key` | "**App Secret**" | string | — |
| `app_secret` | "**App Key**" | string | link: "You don't know your App Key and App Secret?" (Yotpo support page) |
| `show_in_listing` | "Show in products listing" | switch (1/0) | — |

**Labels are SWAPPED in the source code** (`app_key` field shows label "App Secret", `app_secret` field shows label "App Key"). This is a pre-existing bug — the merchant pastes their Yotpo App Key into the field LABELLED "App Secret" because that's the one stored under `app_key` (the value the storefront module actually uses when it renders). Verify with the merchant when troubleshooting.

## Open questions

