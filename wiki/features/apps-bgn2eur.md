---
type: feature
nav_path: "Apps → BGN to EUR"
route_name: apps.bgn2eur.overview
route_path: /admin/apps/bgn2eur
aliases: ["BGN2EUR", "BGN to EUR", "Currency transition", "Dual currency Bulgaria", "enable disable button", "app active toggle"]
tags: [apps, administration, currency, bulgaria, transition, plan-gated]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# BGN to EUR (Bulgaria currency transition)

## Purpose

**BGN to EUR** integration — Bulgaria-specific tool for the **BGN → EUR currency transition** (Bulgaria adopts EUR in 2026). The app does two things:

- **Dual-currency display** — shows storefront prices in BOTH BGN and EUR at the fixed official rate.
- **One-time conversion** — rewrites every BGN price in the store as EUR and switches the site currency.

Required for Bulgarian merchants during the transition window. Only operates when the store currency is BGN or EUR. After 2026-01-01, BGN waybills are hard-blocked, so merchants must convert orders to EUR — see [[orders-shipping-waybill]].

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so it can be switched off without uninstalling it. A disabled app stops working while keeping its settings.

## Where to find it

Sidebar → Apps → install → **BGN to EUR**. Two sub-pages:

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.bgn2eur.overview` |
| Settings | `apps.bgn2eur.settings` |

## What the merchant can do here

- Activate dual-currency display.
- Choose where dual currency renders (storefront, admin panel, or both).
- Toggle the conversion message position (checkout / cart / footer).
- Override the conversion-message text.
- Run the one-time **Convert store prices to Euro** action (Settings page).

### What the merchant CANNOT do here
- Change the conversion **rate** — it is the official fixed rate, not market-floating.
- Disable BGN before the official switch date.
- Revert prices after running the one-time conversion (there is no undo).

## Settings & fields

| Setting key | Purpose | Default |
|---|---|---|
| `display_mode` | Where dual currency renders. | `both` at install |
| `conversion_message` | Storefront info text about the conversion period. | `1 EUR = 1.95583 BGN` |
| `conversion_message_position_checkout` | Show message at checkout. | `1` (on) |
| `conversion_message_position_cart` | Show message in cart. | `1` (on) |
| `conversion_message_position_footer` | Show message in footer. | `1` (on) |
| `convert2eur` | One-time conversion state — `0` not started, `1` started, `2` completed (sticky). | `0` |

`display_mode` accepts three values: `storefront` (customer-facing pages + theme builder), `admin_panel` (merchant admin + builder), `both` (everywhere). At a fresh install the default is `both`, so dual currency renders everywhere until the merchant narrows it.

## Business rules

### Hardcoded BGN→EUR rate

Bulgaria's official conversion rate is fixed at **1 EUR = 1.95583 BGN**. The app uses this rate for all conversions — no market-rate fluctuation.

### Currency gating

Dual currency renders only when the app is active **and** the site currency is `BGN` or `EUR`. Other currencies are silently skipped — so Romania (`RON`) is unaffected, while a Greek (`EUR`) store will show dual currency where applicable.

### Three display modes

The merchant chooses where dual currency renders via `display_mode` (`storefront` / `admin_panel` / `both`). Client-side dual rendering — both currencies updating live when the customer picks a variant on the product page — only runs in `storefront` and `both` modes; in `admin_panel` mode prices are rendered dual server-side only, with no live JS price updates.

### Storefront cache flush

Changing display or conversion settings flushes the storefront cache so customers see updated prices on next page load.

### Customer preference

There is no customer-facing currency picker. The shopper sees whatever the merchant configured, plus both prices side-by-side in dual mode. There is no "show only EUR / only BGN" shopper toggle.

### After 01.01.2026 — BGN sunset

After 2026-01-01, generating BGN waybills is blocked (see [[orders-shipping-waybill]]); merchants must complete orders in EUR. The app helps customers shop in EUR pricing while the merchant runs analytics in mixed currency until everything converts.

## Related

- [[apps]] — App Store.
- [[apps-bgn2eur-settings]] — settings sub-page.
- [[settings-general]] — store country (Bulgaria requirement).
- [[orders-shipping-waybill]] — waybill EUR variant hard-block after 2026-01-01.
- [[orders-details]] — "Convert prices to EUR" sidebar button related to this app.

## How it works (verified against backend)

### "Convert to EUR" is a one-time hard switch, not a toggle

Beyond dual display, the **Settings page** hosts a **Convert store prices to Euro** button (a second box below the display-mode form, with a confirmation modal) that rewrites every BGN price in the store as EUR at the fixed rate. Once confirmed, the platform:

1. Refuses to run if conversion was already started (`convert2eur=1`) or completed (`convert2eur=2`) — *"Conversion has already been started or completed"*.
2. Refuses to run if the store currency is not BGN — *"Conversion is only available for sites with BGN currency"*.
3. Puts the store into **maintenance mode** (storefront returns the maintenance page; checkout is blocked while conversion runs).
4. Waits for in-flight background jobs to finish, then runs the conversion in one database transaction.
5. Updates the site currency from BGN to EUR.
6. Regenerates the storefront catalog data and rebuilds the variant search index.
7. Sends an in-platform success notification (`bgn2eur_conversion_completed`).
8. Exits maintenance mode.

After it finishes the store IS in EUR and **cannot be reverted** — there is no undo. A per-record before/after price log is preserved for audit, but live data is now EUR.

### What gets converted

The conversion rewrites every monetary field so the merchant does not have to fix them by hand: product variant prices and delivery prices; product price-from / price-to (recomputed from variant prices); discounts, flat-price discounts, discount codes and pro targets; quantity-discount steps; cart-rule action and trigger prices; smart-collection price-range filters; bundle prices; cross-sell prices; form-field and form-field-option prices; shipping-rate prices; flat tax amounts; and payment-provider fee amounts plus their configured currency code.

### Rounding

Every price is converted as `price ÷ 1.95583`, rounded half-up to the same minor-unit (cents) granularity it was stored in. Sub-cent fractions are not preserved.

### Taxes: percentages unchanged, flat amounts converted

Percentage tax rates (e.g. 20% VAT) are untouched — they apply equally in either currency. Only flat tax components (a fixed money amount per order) are converted.

### Past orders are NOT re-rendered

The conversion does not touch any order data. Orders placed in BGN stay in BGN in the merchant's history; only new orders after conversion are in EUR. Invoicing apps that produce a PDF (e.g. [[apps-fgo]]) read each order's stored currency, so pre-conversion orders invoice in BGN and post-conversion orders in EUR. The app does not retroactively re-issue invoices.

### Cache + search index

After conversion the platform automatically regenerates the storefront catalog data and rebuilds the variant search index — no manual cache clearing needed.

### End-of-transition uninstall

Once conversion completes, the merchant can keep the app installed (it then only powers the "1 EUR = 1.95583 BGN" reference message). Uninstalling removes the dual-display and the conversion-message banner; it does not revert prices. The Convert button stays disabled because `convert2eur=2` is sticky.

## Open questions
