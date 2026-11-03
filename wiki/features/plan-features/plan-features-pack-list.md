---
type: feature
nav_path: "Plan → Feature pack → Pack list"
route_name: admin.plan.feature
route_path: /admin/plan/feature/{mapping}
aliases: ["Pack list table", "Available feature packs", "+100 products", "+500 products", "+1000 products", "Custom amount pack", "Dynamic pricing ladder"]
tags: [plans, plan-feature, feature-pack, pack-list, dynamic-pricing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-features]]. See the hub for the other aspects (warning banners, purchase flow, restrictions & limits, subscription lifecycle, modern Vue grid, middleware mappings).

# Plan features — pack list

## Purpose

The **pack list** is the table of available feature packs the merchant can buy for the one feature they hit a limit on. Each row is a self-contained offer — pack name, per-cycle price, and a **Buy** button that triggers the purchase action. There is no quantity selector on the list itself — quantities are baked into each pack row.

## Where to find it

- Rendered on `/admin/plan/feature/{mapping}` below the warning note (see [[plan-features-warning-banners]]).
- Visible only when the merchant's plan **allows** feature-pack purchases for this feature (see [[plan-features-restrictions-limits]]). If not, the restriction banner shows instead.

## What the merchant can do here

- Browse the list of available packs for this one feature.
- Click **Buy** on a row to start checkout for that pack (see [[plan-features-purchase-flow]]).
- For dynamic-pricing features, see the **continuous price ladder** (multiple quantity steps) with volume discounts already applied — pick the step that fits.

## Settings & fields

### Pack list table — columns

| Column | What it shows |
|--------|---------------|
| **Pack name** | Localised pack name; for dynamic-pricing features, the name includes the quantity (e.g. *2000 products*) |
| **Price** | Per-cycle price (e.g. *10.00 EUR / month*, *50.00 EUR / year*), VAT excluded |
| **Buy button** | Action button — clicking it triggers the purchase action + redirect to checkout (see [[plan-features-purchase-flow]]) |

Below the table: *"The quoted prices are exclusive of VAT"*.

### Fixed-price pack examples

- *+100 products*
- *+500 products*
- *+1000 products*
- *+5 GB storage*
- *+1000 newsletter sends / month*

### Dynamic-pricing pack examples

For features with `dynamic_pricing = 1`, the pack name on each row includes the quantity:

- *500 products*
- *1000 products*
- *2000 products*
- *5000 products*

The merchant sees discrete steps along a server-generated ladder, **not** a free-form slider.

### Empty state

If no packs are available (and the feature isn't fully restricted by plan), the area renders the localised string **"No results found"** in place of the table. See [[plan-features-warning-banners]] for the banner shown above.

## Business rules

### Pack list is filtered by `dynamic_pricing` flag matching

Packs surface only when their `dynamic_pricing` flag matches the feature's `dynamic_pricing` flag — the two MUST align. So a feature with `dynamic_pricing = 0` only shows fixed packs; a feature with `dynamic_pricing = 1` only shows dynamic-pricing packs. **The two pack types don't mix on the same screen.** (verify)

### Dynamic ladder is server-generated up to `max_value`

For dynamic-pricing features, the ladder isn't a fixed *small / medium / large* set — it's a continuous price ladder generated from the pack's base `value` step, ending when either the per-unit price stops decreasing (flat curve) or the feature's `max_value` cap is reached. See [[plan-features-restrictions-limits]] for the formula + cap.

### No quantity / spinner UI on this screen

Quantities are baked into each pack row. To buy *2× +100 products* the merchant would have to buy *+200 products* (or repeat the buy flow). The merchant picks **ONE pack at a time** — the cart is replaced on each *Buy* click.

### No discounts / promo codes on this screen

Pricing comes from the catalog (for fixed packs) or from the dynamic-pricing formula (for dynamic packs). The merchant cannot enter a discount code, apply a promo, or override the price here. Any promotion happens on the checkout page the merchant is redirected to (see [[plan-features-purchase-flow]]).

### Mapping URL is the route key

The route URL pattern `/admin/plan/feature/{mapping}` accepts the feature mapping verbatim — examples:
- `/admin/plan/feature/products`
- `/admin/plan/feature/customers`
- `/admin/plan/feature/storage`
- `/admin/plan/feature/discount-code-pro`
- `/admin/plan/feature/support_meetings`
- `/admin/plan/feature/custom_hostname`

Some pack mappings are **aliased internally** before being handed to the subscription / app-activation step (e.g. `shipping_payment_sync` → `omniship`). The URL the merchant sees uses the public mapping; the alias only matters server-side. See [[plan-features-middleware-mappings]].

## Related

- [[plan-features]] — hub.
- [[plan-features-warning-banners]] — what's rendered above the list.
- [[plan-features-purchase-flow]] — what the *Buy* button does.
- [[plan-features-restrictions-limits]] — the `max_value` cap + dynamic-pricing formula that shape the ladder.
- [[plan-features-middleware-mappings]] — mapping aliases for `omniship` / `cloudio` / `campaigns`.
- [[plan-vs-feature-pack]] — pack-vs-upgrade decision.

## Open questions

None.
