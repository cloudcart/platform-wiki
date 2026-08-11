---
type: feature
nav_path: "Marketing → Discounts → Shipping → Examples"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Free shipping examples", "Free shipping recipes", "Free shipping over X", "VIP free shipping", "Black Friday free shipping", "Free shipping by region"]
tags: [marketing, discounts, shipping, examples, recipes]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, value mechanics, stacking, force-save, other zero-paths, plan gates / API).

# Shipping discount — common merchant scenarios

## Purpose

This page collects the **most-asked Free-shipping configurations** with the exact field combinations the merchant should set. Each recipe is minimum-viable — layer additional restrictions on top as needed. For per-field reference, see [[shipping-discount-eligibility]].

## Where to find it

All recipes are created on the Create / Edit form at `/admin/marketing-new/discounts/create/global` (no-code) or `/admin/marketing-new/discounts/create/code` (coupon). See [[marketing-discounts-shipping]].

## What the merchant can do here

Pick the recipe matching the intended promotion and copy the field values. Adjust restrictions (customer group, geo zone, dates) as needed.

## Settings & fields

Recipes reference the field set documented on [[shipping-discount-eligibility]], [[shipping-discount-value-mechanics]], [[shipping-discount-force-save]], [[shipping-discount-stacking]].

## Business rules

### Recipe 1 — Always-on free shipping (no threshold)

Use case: *"Free shipping for every order, no minimum."*

| Field | Value |
|---|---|
| `type` | `shipping` |
| `type_value` | empty |
| `settings` (Discount target) | `all` |
| `force_save` | 1 |
| `active` | `yes` |
| `name` | "Free shipping" |
| `date_start` | today |
| `no_expire` | ON (or set `date_end`) |
| Customer / region restrictions | Open |

Result: every cart with a non-zero shipping quote gets the shipping line zeroed out. The merchant absorbs whatever the carrier charges. Sets the "has free shipping" flag — receiver-pays hidden on the waybill (see [[shipping-discount-other-zero-paths]]).

### Recipe 2 — Free shipping above a cart total ("Free shipping over 50 EUR")

Use case: *"How do I give customers free shipping above a 50 EUR cart total?"* — the most common Free-shipping campaign.

| Field | Value |
|---|---|
| `type` | `shipping` |
| `type_value` | empty |
| `settings` | `order_over` |
| `order_over` | 5000 (50 EUR — stored in cents) |
| `force_save` | 1 |
| `active` | `yes` |
| `name` | "Free shipping over 50 EUR" |
| `date_start` | today |
| `no_expire` | ON |
| Customer / region restrictions | Open |

Result: carts at or above 50 EUR subtotal get free shipping. Below the threshold, full shipping is charged. The customer-facing label is the discount's `name`.

For a code-based variant (customer types `OVER50` at checkout): set `type=code`, fill `code = OVER50`, decide `code_apply` (block stacking with per-product discounts vs allow). Note the inclusive `>=` check on `order_over` for code-based shipping — a 50.00 EUR cart qualifies (see [[shipping-discount-eligibility]]).

### Recipe 3 — VIP free shipping (customer-group-restricted)

Use case: *"I want to give VIP customers free delivery forever."*

| Field | Value |
|---|---|
| `type` | `shipping` |
| `settings` | `all` |
| `force_save` | 1 |
| `active` | `yes` |
| `name` | "VIP free shipping" |
| `customer_groups_target` | `no` |
| `customer_groups[]` | [VIP group ID from [[customers-custom-groups]]] |
| `only_customer` | 1 (VIPs are by definition registered) |
| `no_expire` | ON |

Result: only logged-in customers in the VIP group get free shipping. Guests + other groups pay full shipping. The discount silently does not apply on guest carts.

### Recipe 4 — Region-only free shipping ("Free shipping inside Bulgaria only")

Use case: *"I cover free shipping in my home country but international customers pay."*

| Field | Value |
|---|---|
| `type` | `shipping` |
| `settings` | `all` |
| `force_save` | 1 |
| `active` | `yes` |
| `name` | "Free shipping inside Bulgaria" |
| `all_regions` | `no` |
| `geo_zone_id` | [Bulgaria geo-zone ID from [[geo-zone]]] |
| `no_expire` | ON |

Result: only carts shipping to an address in the configured geo-zone get the discount. International carts pay full shipping. To extend to multiple countries, the merchant configures a multi-country geo-zone (not multiple discounts).

### Recipe 5 — Time-boxed Black Friday free shipping

Use case: *"Black Friday: free shipping on everything for 3 days."*

| Field | Value |
|---|---|
| `type` | `shipping` |
| `settings` | `all` |
| `force_save` | 1 |
| `active` | `yes` |
| `name` | "Black Friday free shipping" |
| `date_start` | 2026-11-27 |
| `date_end` | 2026-11-29 |
| `no_expire` | OFF |

Result: free shipping fires on every cart between the dates. Note the UTC-based auto-disable — the row may remain "active" for ~27 hours after the merchant's local end-of-day before the daily UTC sweep flips the flag (see [[shipping-discount-eligibility]]). Storefront cart-engine checks DO use store timezone, so the customer's checkout stops applying the free shipping at the expected local time — only the admin-list row lags.

### Recipe 6 — Code-based "Free shipping with WELCOME"

Use case: *"Send a welcome email with a code that gives free shipping on the first order."*

| Field | Value |
|---|---|
| Type-picker card | Discount with code |
| `type` | `shipping` |
| `code` | `WELCOME` (regex `/^[a-z0-9\#\.]+$/i`, max 20, unique) |
| `settings` | `all` (or `order_over` with threshold) |
| `force_save` | 1 |
| `code_apply` | 1 (if you want to allow stacking on carts with per-product discounts) |
| `maxused_user` | 1 (one redemption per customer — first-order semantic) |
| `name` | "Welcome discount — free shipping" |

Result: customer types `WELCOME` at checkout; free shipping applies. With `maxused_user = 1`, each customer can redeem once. Counted only when the order reaches the counted statuses (`paid`, `completed`, `fulfilled` by default — see [[shipping-discount-eligibility]]).

### Recipe 7 — Multi-tier free shipping (NOT this feature — use Cart Rules)

Use case: *"Free standard shipping over 50 EUR, free express shipping over 100 EUR."*

This recipe is **not** achievable with the native Free-shipping discount, because:

- Only ONE shipping discount applies per cart at totals time (first-match-wins, undefined order — see [[shipping-discount-stacking]]).
- Stacking two no-code `order_over` shipping discounts produces undefined behaviour.

The correct solution is [[apps-cart-rules|Cart Rules]] (supports tier ladders) or [[settings-shipping]] per-method *"Free shipping threshold"* (per-courier-method, runs at quote time). The merchant should NOT create two overlapping Free-shipping discounts hoping the higher-threshold one wins — there is no `order_over DESC` sort.

### Recipe 8 — Partial-shipping discount (NOT this feature — use Cart Rules)

Use case: *"50% off shipping on orders over 30 EUR."*

Not achievable with this feature — shipping discounts are binary (free or nothing). Use [[apps-cart-rules]] which can re-quote shipping at a custom amount.

Note: a Cart Rule with `free_shipping` action also zeroes the shipping line, but **does NOT set the "has free shipping" flag** — receiver-pays stays visible on the waybill picker (see [[shipping-discount-other-zero-paths]]). If the waybill side switch matters, the Native Free-shipping discount is the way.

### Common gotchas — quick reference

- `force_save = 0` for `type=shipping` → form rejects (required).
- `type_value` set to any number → *"Type value must be empty"*.
- Target = product / category / vendor / smart-collection → *"Type is not valid for products or product category targets"*.
- Plan-feature cap reached → HTTP 403 *"Not supported by plan"*.
- Toggling no-code `active` twice within 10 min → *"You've already activated this discount..."*.
- Discount not applying → check shipping quote > 0, subtotal ≥ `order_over`, customer group / region / dates / `only_customer`, `uses` not exhausted.

## Related

- [[marketing-discounts-shipping]] — hub.
- [[shipping-discount-eligibility]] — all condition fields referenced in the recipes.
- [[shipping-discount-stacking]] — why multi-tier shipping doesn't work as overlapping discounts.
- [[shipping-discount-other-zero-paths]] — Cart Rules + waybill receiver-pays comparison.
- [[apps-cart-rules]] — partial-shipping + multi-tier shipping alternative.
- [[settings-shipping]] — per-method *"Free shipping threshold"* alternative.
- [[customers-custom-groups]] — VIP group definition.
- [[geo-zone]] — region-restriction zone definition.

## Open questions

None.
