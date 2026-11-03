---
type: feature
nav_path: "Profile → Choose plan → {Plan} → Purchase → Billing cycle"
route_name: admin.plan.purchase
route_path: /admin/plan/{mapping}/purchase
aliases: ["Plan billing cycle", "Plan billing variant", "Monthly vs yearly plan", "Plan period selection", "Billing cycle radio", "Период на плана", "Месечен срещу годишен план"]
tags: [plans, pricing, billing, subscription, purchase]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans-purchase]]. See the hub for the other aspects (recommended add-ons, plan detail view, checkout panel, business rules, subscription outcomes, discount codes).

# Plans purchase — billing cycle picker

## Purpose

The billing-cycle picker is the **first decision** the merchant makes on the plan-purchase screen — *which billing period of this plan are you buying?* Monthly, yearly, every-2-years (where available). The picker is a radio group: exactly one variant can be chosen, and one is always pre-selected so the running total is never empty.

## Where to find it

Inside the purchase flow at `/admin/plan/{mapping}/purchase` (e.g. `/admin/plan/cc-pro/purchase`, `/admin/plan/business/purchase`, `/admin/plan/startup/purchase`). The picker sits at the top of the panel, above the recommended-add-ons blocks and the totals summary.

Plan `{mapping}` values are stable slugs: `startup`, `basic`, `cc-pro`, `business`, `enterprise`, `unicorn`.

## What the merchant can do here

- Switch between active billing variants of the plan.
- See the per-variant savings inline (e.g. *save 24.00 EUR*) versus monthly.
- Watch the running total update live as they switch — no page refresh.

## Settings & fields

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Billing-cycle radio** (per variant) | Selects which billing-cycle variant to purchase | Middle variant (typically yearly) is pre-selected | Variants are ordered as defined in the catalog. |
| **Variant label** | *<plan-name> <billing-period>* + description (price + period + savings) | — | Template: `'{plan_name} {plan_price} {plan_period} {plan_save}'`. Example: *Plan Pro Yearly — 199.00 EUR per year (save 49.00 EUR)*. |
| **Variant period** | Billing interval | — | Typically: monthly = 1 month, yearly = 12 months, *every 2 years* = 24 months. (verify exact period strings per plan in catalog) |
| **Variant savings** | Inline savings vs the monthly rate | — | Only rendered when the variant has a positive `plan_save` value. |
| **VAT disclaimer** | *"The quoted prices are exclusive of VAT"* | — | Shown twice — under the variant block and below the totals. |

## Business rules

### Exactly one variant per purchase

The picker is a radio (not a checkbox). The cart accepts a single `plan_details` ID per cart — the merchant cannot buy *both* monthly *and* yearly at once. To switch billing cycles later, they re-enter this screen.

### Middle variant pre-selected

The middle option (typically yearly) is pre-selected on entry. This guarantees the cart always has exactly one plan variant from first render, so the totals are computed and the **Proceed to checkout** button can be enabled immediately.

### Variant availability comes from the catalog

If CloudCart hasn't priced a monthly variant for this plan (some plans are sold yearly-only, etc.), it doesn't appear at all. The merchant cannot choose a variant that isn't published. If the plan has **no** priced variants, the purchase URL throws a not-found error (the catalog also filters those out — see [[plans]]).

### Live total computation is client-side

The subtotal / VAT / total values are computed in the browser as the merchant toggles the radio, using `data-price-without-vat` / `data-price-vat` attributes on each radio option. No server round-trip until checkout submission.

### Currency follows invoicing country, not store currency

The currency sign + decimal formatting are determined by the merchant's invoicing-country setup, not by the store's storefront currency. A merchant whose store sells in BGN but is invoiced by the BG entity sees plan prices in BGN; a DE-invoiced store sees EUR. The merchant cannot override the currency on this screen — see [[billing-invoicing]] for managing the invoicing country.

### Pricing is read-only

Every figure (price, original price, discount, period text, currency, VAT) is read from the plan-details catalog row. The merchant cannot override any of them — the only choice is *which* variant to pick.

### Switching billing cycles — no proration

There is NO proration logic when switching between Monthly and Yearly. When a merchant on Pro Monthly switches to Pro Yearly through the **Current plan** option on the purchase screen, they pay a FULL new term and their old monthly subscription is cancelled. Any unused monthly time is not credited back. Merchants should switch at the end of a billing cycle to avoid losing time. See [[plans-purchase-business-rules]] for the full set of cart-entry rules.

## Related

- [[plans-purchase]] — hub.
- [[plans]] — the plan catalog the merchant arrives from.
- [[plan-details]] — the entity carrying per-variant pricing (`plan_save`, `plan_period`, etc.).
- [[plans-purchase-recommended-addons]] — the optional services/apps blocks rendered below this picker.
- [[plans-purchase-business-rules]] — cart-reset, single-variant, no-proration rules in detail.
- [[billing-invoicing]] — invoicing-country setup that determines the displayed currency.

## Open questions

None.
