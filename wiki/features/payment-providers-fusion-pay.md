---
type: feature
nav_path: "Payment Providers → Fusion Pay"
route_name: apps.fusion_pay.overview
route_path: /admin/payment-providers/fusion_pay
aliases: ["Fusion Pay", "TBI Pay", "TBI Bank installment", "TBI BNPL", "TBI лизинг", "ТБИ Пей", "Фюжън Пей"]
tags: [paymentproviders, payment-providers, fusion-pay, tbi-bank, bnpl, installments, bulgaria, romania]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 1
---
# Fusion Pay

## Purpose

**Fusion Pay** is CloudCart's integration with **TBI Bank**'s online installment-loan product (TBI Pay), and the modern live-API replacement for the legacy [[payment-providers-tbi|Tbi]] integration. The merchant signs a reseller contract with TBI Bank, receives a credential triple (`reseller_code`, `reseller_key`, `encryption_key`) for test or live, and TBI Pay then shows at storefront checkout. Customers pick an installment plan (3–60 months), apply for the loan with TBI Bank, and on approval TBI pays the merchant in full.

This page is the entry point. It renders the standard payment-provider overview with three tabs: **Overview**, [[payment-providers-fusion-pay-settings|Settings]] (credentials, periods, free-leasing options, promo button), and [[payment-providers-fusion-pay-schemes|Schemes]] (per-product free-leasing scheme mapping). The integration is richer than DSK or Fibank BNPL — product-page promo buttons, an optional **TBI Calculator** module, promo / 0%-interest schemes, and order-amount gating (`52 ≤ amount ≤ 15000`).

## Where to find it

Sidebar → **Payment Providers** → click **Fusion Pay**. The route is `/admin/payment-providers/fusion_pay`. Three tabs appear at the top: **Overview**, **Settings**, **Schemes**.

## What the merchant can do here

- **Read the overview card** — logo, description, and standard install / activate / deactivate buttons.
- **Install / Uninstall** the `fusion_pay` provider through the overview's standard buttons.
- **Activate** the payment method once credentials are saved.
- **Switch between the three tabs**:
  - [[payment-providers-fusion-pay-settings]] — reseller credentials (test + live), period range (min/max/step), free-leasing title, button tier configuration, currency.
  - [[payment-providers-fusion-pay-schemes]] — map TBI-issued free-leasing schemes (the bank-side "0%" loan products) to specific CloudCart products or categories.

## Settings & fields

This is a hub page — the actual fields live on the two sub-tabs. The overview exposes only the standard payment-provider controls:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button | Adds the `fusion_pay` provider to the store. | Not installed | One-click action. |
| **Active** switch (header) | Turns Fusion Pay ON / OFF for storefront checkout. | OFF | Server refuses activation unless credentials are saved AND TBI accepts the calculation API call on save. |
| **Test mode switch** | Switches between test (`reseller_code_test` etc.) and live (`reseller_code` etc.) credentials. | test | Both sets are saved at once; the switch only changes which set is used. |
| **Amount from / Amount to** | Order-total range in which Fusion Pay shows on checkout. | None | Required. Both `52 ≤ value ≤ 15000`, and **amount_to > amount_from**. TBI Bank loan limits. |
| **Logo / Title / Description** | Customer-facing label and image on checkout. | Provider defaults | Standard. |
| **Discount** | Optional discount applied when the customer picks this method. | None | Standard. |

## Business rules

### How Fusion Pay works for the customer

1. **Cart** — customer adds products and picks Fusion Pay (TBI installment) at checkout.
2. **Calculation** — CloudCart asks TBI for the available installment schemes for the cart amount + product category. Each scheme carries its period, monthly payment, and an `is_promo` flag (0 = interest-bearing, 1 = free-leasing / 0% promo).
3. **Filtering** — schemes are filtered by the merchant's `min_period`, `max_period`, `step_period`, and (for carts with discounted products) the `free_leasing_for_discounted_products` switch. Interest-bearing and (if available) free-leasing plans show separately in the module.
4. **Redirect to TBI** — TBI's calculator takes over the credit application; the customer fills it on TBI's side.
5. **TBI approves or rejects** — payment status updates from TBI's response.

### Order amount limits — 52 to 15000

`amount_from` / `amount_to` are **TBI Bank's regulatory limits** for the online loan: minimum 52, maximum 15000 (in the merchant's currency). The merchant can narrow this range but not widen it — form validation refuses out-of-range values (`"Amount from must be at least 52"`, `"Amount from must be at most 15000"`, etc.).

### Period configuration (months)

Three period parameters in Settings:

- **Min period** (`min_period`) — minimum months (TBI default 3, valid range 3–60).
- **Max period** (`max_period`) — maximum months (TBI default 60).
- **Step period** (`step_period`) — increments; e.g. `step_period = 3` filters TBI's variants to multiples of 3 months above `min_period`.

When the **TBI Calculator** module is ON, these period fields are hidden — the calculator handles period selection in its own iframe.

### Promo buttons — three tiers on the product page

Fusion Pay offers a per-product-page promo button with up to three price tiers. Enabling **TBI tiers** (`promo_button` switch) fetches TBI's tier multipliers and lets the merchant configure:

- Tier 1 (default 12 months) — applies up to `tier1_max` amount, monthly rate per TBI's `tier1_multiplier`.
- Tier 2 (default 48 months) — applies between `tier1` and `tier2` amounts.
- Tier 3 (default 60 months) — applies between `tier2` and `tier3` amounts.

Each tier shows the maximum order amount it applies up to (auto-formatted as currency) and the monthly interest rate (`{rate}`). The merchant also picks one of four product-page **button styles** (orange, black, white, etc.).

### Free leasing (0% interest)

Fusion Pay supports 0%-interest installment plans ("free leasing") that TBI pre-defines per merchant; these return from the calculation API with `is_promo = 1`. The merchant configures:

- **Title for interest-free leases** — heading shown above 0% offers in the customer's pricing table.
- **Discounted products switch** (`free_leasing_for_discounted_products`) — when ON, products that already carry a CloudCart discount are EXCLUDED from free-leasing offers (so the merchant doesn't double up the promo).

The [[payment-providers-fusion-pay-schemes|Schemes tab]] maps TBI's `is_promo = 1` schemes to specific products / categories via the `mapping` configuration — so a given scheme applies only to a curated product set.

### Refund handling

Refunds are NOT exposed in CloudCart's admin for Fusion Pay — the merchant handles refunds through TBI's portal.

### Country + currency

Currency is merchant-configurable between **EUR and RON** only — the settings UI lists no BGN option. A Bulgarian (BGN) store cannot run Fusion Pay against BGN-priced carts directly; it must set the provider currency to EUR and let the platform convert the cart total at checkout. Fusion Pay is positioned as the Romanian and Eurozone rail; Bulgarian merchants needing a TBI-style installment loan typically use the legacy [[payment-providers-tbi|Tbi]] integration or the merchant-side email flow.

### Plan-gating

Not gated by CloudCart plan.

### Fusion Pay vs the old Tbi integration

The legacy [[payment-providers-tbi|Tbi]] integration is a simpler, pre-API, pre-redirect provider — it shows installment plans calculated locally with a configured `percentPerMonth` rate but does not call TBI's API; the merchant follows up via email (`the provider's support address`). Fusion Pay is the live-API replacement, with real-time calculation, redirect-to-TBI checkout, and free-leasing schemes. **New merchants should install Fusion Pay, not Tbi.** Both can coexist on a store, but the legacy Tbi provider is effectively superseded.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-fusion-pay-settings]] — reseller credentials, periods, button tiers, free-leasing options.
- [[payment-providers-fusion-pay-schemes]] — per-product free-leasing scheme mapping.
- [[payment-providers-tbi]] — the legacy TBI integration, superseded by Fusion Pay.
- [[payment-providers-tbi-bank]] — the parallel `tbi_bank` provider for card-style purchases via TBI's gateway (different product, not the installment loan).
- [[payment-providers-iute]] — Iute credit, another EU consumer-loan provider with a similar product-page module pattern.

## Open questions

_None._
