---
type: feature
nav_path: "Apps → Brands Distribution"
route_name: apps.brands-distribution.overview
route_path: /admin/apps/brands-distribution
aliases: ["Brands Distribution", "Brands Distribution ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["brands-distribution_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# Brands Distribution (ERP)

## Purpose

**Brands Distribution** is a fashion drop-shipping catalogue integration. BrandsDistribution is a major Italy-based pan-European fashion / clothing distributor that acts as the supplier: CloudCart imports their catalogue (products, stock, prices) and shows it on the storefront, so the merchant resells without holding inventory. Orders go through CloudCart's standard checkout; the merchant then relays them to BrandsDistribution externally.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Brands Distribution**. App key: **brands_distribution**.

The app has these tabs: **Overview** (install card), **Settings** (credentials + catalogue + pricing + name constructor), **Categories mapping** (optional manual BD-category ↔ CloudCart-category mapping), **Status** (Start / Stop the import), **Products** (BD-imported products, with a connect modal), and **Import history** (per-run log).

## What the merchant can do here
- Enter BrandsDistribution account credentials and pick the licensed catalogue to import.
- Choose the description language, pricing, markup, name composition, and gender-to-category mapping for imported products.
- Start / Stop the catalogue import and review per-run import history.
- Remove all imported BrandsDistribution products on demand.

### What the merchant CANNOT do here
- Use the app without an active BrandsDistribution account / licence.
- Trigger per-order BrandsDistribution actions from the order detail page — the integration is import-only (catalogue + stock + price), with no per-order push.

## Settings & fields

**Credentials**
- **Email** (`email`) — BrandsDistribution account email. Required.
- **Password** (`password`) — BrandsDistribution account password (masked). Required. Wrong credentials show "Invalid credentials".
- **User catalog** (`user_catalog`) — the catalogue the merchant is licensed to import. **Required to save.** Options are fetched from BrandsDistribution at runtime after credentials validate, so the merchant only sees catalogues their account is authorised for.

**Description language** — one of a fixed list of 22 options (Italian, English, French, German, Spanish, Romanian, Dutch, Polish, Portuguese, Czech, Slovak, Slovenian, Swedish, Hungarian, Estonian, Russian, Lithuanian, Danish, Finnish, Bulgarian, Greek). Default `en_US`. Product titles and descriptions import in the chosen language. The list carries both `cz_CZ`/`cs_CZ` for Czech and both `sl_SI`/`sk_SK` for Slovenian/Slovak — relics of historical locale codes.

**Pricing** — the merchant picks ONE of three price fields from the BrandsDistribution feed for the live storefront price, and (independently) one of the same three for the "Old / compare-at" price (`use_price_discount`):
- `streetPrice` (default) — street / retail price.
- `suggestedPrice` — MSRP / suggested retail.
- `taxable` — distributor / wholesale price.

A typical setup uses the distributor price as the buy-it-now price and the suggested price as the strikethrough.

**Markup** — two markups apply simultaneously and stack: `price_percent` (0–500%, integer) then `upPrice` (flat amount in store currency, up to 1,000,000). Final price = (feed price × (1 + `price_percent`/100)) + `upPrice`. Both default to 0; leave one at 0 to use the other in isolation.

**Name constructor** — product names are assembled from up to 7 components, in the order chosen: `category`, `subcategory`, `name`, `brand`, `gender`, `color`, `season`. Default is `[name]` (just the Name/SKU field). E.g. `[brand, gender, category, season, color]` yields "Adidas Men's T-Shirt Spring Black".

**Gender-to-category mapping** (`gender_to_category`) — when ON, products carrying a "Gender" attribute are auto-placed under a top-level category whose name matches the gender value (`Men`, `Women`, `Kids`, etc.). The **Categories mapping** tab fine-tunes this manually.

**Update toggles**
- **Update existing products category** (`update_category`, paired with `gender_to_category`) — when ON, re-imports also move existing products into the matching gender category.
- **Update product name** (`update_name`) — OFF (default): manual edits to product names survive re-imports. ON: every re-import resets the name to whatever the name constructor produces.

**Discount** — when a CloudCart discount is set, every imported product that has a promo price is grouped under that single discount, so the merchant manages all BrandsDistribution promo pricing centrally rather than per-product.

## Business rules

- **Drop-shipping, not a standard ERP.** BrandsDistribution is the supplier; CloudCart imports its catalogue rather than syncing the merchant's own ERP records.
- **Product cap.** The plan-feature `brands-distribution_total_products` is a numeric global cap on imported products. Once the cap is hit, additional products are skipped on subsequent imports. There is no install-level access gate — the app can be installed on any plan, but the cap applies during import. See [[plan-gates]], [[plan-features]], and [[plan-vs-feature-pack]] for downgrade rules.
- **Gender-to-category requires exact names.** Auto-mapping only works when CloudCart categories are named to match BrandsDistribution's gender values exactly; otherwise the product is silently skipped from auto-placement.
- **Import runs in the background.** Start/Stop on the Status tab controls a recurring import that runs as a background task; progress is visible in Import history. Removing all imported products is a separate on-demand background task.
- **Sync events in order history.** Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message — both visible in [[orders-history]].
- **Uninstalling** removes the recurring import and the remove-all-products task.

## Related
- [[apps]] — App Store.
- [[orders-history]] — sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.
- [[apps-suppliers]] — alternative supplier mapping.

## Open questions

_None — all questions answered above._
