---
type: feature
nav_path: "Marketing → Discounts → Shipping"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Shipping discount", "Free shipping discount", "Free shipping", "Free delivery", "Безплатна доставка", "Отстъпка за доставка", "Безплатна доставка над"]
tags: [marketing, discounts, shipping, free-shipping]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Shipping discount (Free shipping)

## Purpose

The **Shipping discount** is the discount **type** that **removes the shipping cost** from the customer's order at checkout — the most common way merchants run a "Free shipping" promotion. It is binary: it does NOT change any product's storefront price and does NOT take a percentage off the cart; it strikes the shipping line down to zero on carts that meet the conditions.

Two flavours:

- **Global / always-on** — no code; auto-applies whenever the cart meets the conditions. Targets `all` carts ("Free shipping for everyone") or `order_over` ("Free shipping above 50 EUR").
- **Promo-code** — customer enters a code at checkout to trigger free shipping.

Unlike `flat` and `percent` types in [[marketing-discounts]], a shipping discount **carries no `type_value`** — there's no "how much off" number; the discount IS "remove the shipping line". The saved amount equals the cart's shipping quote at the moment of redemption.

> This page is the **hub**. It carries the entry-point answer ("where do I create it") + a catalogue of the sub-pages. Drill into the aspect that matches the question rather than reading every page.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice.

- [[shipping-discount-eligibility]] — when free shipping kicks in: target `all` vs `order_over`, customer-group / region / `only_customer` / date-range / status restrictions, counted statuses for the `uses` counter, auto-disable in UTC.
- [[shipping-discount-value-mechanics]] — how "remove the shipping line" works: paired positive + negative totals lines, no `type_value`, carrier-quote variability (COD surcharges, insurance, per-product surcharges), `description` always null, customer-facing rendering.
- [[shipping-discount-stacking]] — the `code_apply` flag for code-based variants, one-shipping-discount-per-cart selection, no-code pool excludes code variants, code-based inclusive `>=` vs no-code strict `>`, first-match-wins iteration.
- [[shipping-discount-force-save]] — the `force_save` admin-edit guard: required for `type=shipping`, condition re-check bypass on existing orders.
- [[shipping-discount-other-zero-paths]] — the 4 mechanisms that zero a shipping line (Free-shipping discount, Cross-Sell injection, payment-provider waive, OrderModification, Cart Rule); the **"has free shipping"** flag and its effect on the waybill receiver-pays option.
- [[shipping-discount-plan-gates-api]] — `discount_global` vs `discount_coupon` plan-feature quotas, type-picker gating, HTTP 403 at the cap, JSON-API v2 + GraphQL writes, webhook events, no audit-log row, 10-minute activation cooldown.
- [[shipping-discount-examples]] — common merchant scenarios (always-on, threshold, VIP-only, region-only, code campaign, multi-tier via Cart Rules) with the exact field combos to set.

## Where to find it

A "Free shipping" discount is **not a separate type card** in the type-picker — it is always reached *through* one of two cards. From the [[marketing-discounts]] list, click **+ Add discount**, then:

- **Global discount** card (no-code free shipping) — opens the form at `/admin/marketing-new/discounts/create/global` (`type=global`). Inside, set the discount **type** to **Free shipping** (the *Discount type* select offers Fixed amount / Percentage / Free shipping).
- **Discount with code** card (free-shipping coupon) — opens `/admin/marketing-new/discounts/create/code` (`type=code`). Same form plus the **Generate a discount code** and **Regions** blocks; again pick **Free shipping** inside.

The breadcrumb reads "Marketing → Discounts → Create discount".

## What the merchant can do here

- Create a Free-shipping discount (with or without a promo code).
- Pick a **target**: `all` or `order_over` — see [[shipping-discount-eligibility]].
- Restrict to [[customers-custom-groups|customer groups]], registered users, a [[geo-zone|geo zone]], or a date range — [[shipping-discount-eligibility]].
- Use the binary "remove shipping line" value-type — [[shipping-discount-value-mechanics]].
- Configure `force_save` (required for shipping) — [[shipping-discount-force-save]].
- Manage stacking, `code_apply`, one-shipping-discount-per-cart selection — [[shipping-discount-stacking]].
- Manage plan-gate quotas, API, webhooks, the 10-minute cooldown — [[shipping-discount-plan-gates-api]].

### What the merchant CANNOT do here

- **Set a numeric Discount value** — `type_value` must be empty (*"Type value must be empty"*). See [[shipping-discount-value-mechanics]].
- **Target a specific product / category / vendor / smart collection** — only `all` and `order_over` are supported (*"Type is not valid for products or product category targets"*).
- **Discount shipping by a percentage** ("50% off shipping") — binary only. Use [[apps-cart-rules|Cart Rules]] for partial-shipping promos.
- **Stack a code-based free-shipping discount on a discounted cart** without `code_apply = 1` — see [[shipping-discount-stacking]].

## Settings & fields

Field-by-field tables are deferred to the aspect pages so each table can stay close to its rules. Quick index:

| Field family | Detail page |
|---|---|
| `type` + `type_value` (binary, no value) | [[shipping-discount-value-mechanics]] |
| `settings` (target `all` / `order_over`) + `order_over` threshold | [[shipping-discount-eligibility]] |
| `active`, `name`, `date_start` / `date_end` / `no_expire` | [[shipping-discount-eligibility]] |
| `only_customer`, `customers[]`, `customer_groups[]`, `all_regions`, `geo_zone_id` | [[shipping-discount-eligibility]] |
| `max_uses`, `maxused_user`, counted statuses (`discounts_used_statuses`) | [[shipping-discount-eligibility]] |
| `force_save` (required for `type=shipping`) | [[shipping-discount-force-save]] |
| `code`, `code_format`, `barcode_prefix`, `code_apply` (code variant only) | [[shipping-discount-stacking]] |
| Plan-feature quotas (`discount_global`, `discount_coupon`) | [[shipping-discount-plan-gates-api]] |

### Endpoints

| Action | Route path |
|--------|------------|
| Create form (global / no-code) | `/admin/marketing-new/discounts/create/global` |
| Create form (code-based) | `/admin/marketing-new/discounts/create/code` |
| Edit form | `/admin/marketing-new/discounts/edit/{id}` |
| Save (admin API) | `POST /admin/api/discounts` |
| JSON-API v2 CRUD | `<store>/api/v2/discounts` (resource [[api-discounts]]) |

## Business rules

The hub keeps two summary rules. Everything else lives on the aspects.

### Free shipping = "remove the shipping line" — not a discount amount

A shipping discount **does not produce a `type_value`**. At cart totals time, the platform reads the cart's shipping quote and renders a NEGATIVE totals line of exactly that amount alongside the shipping line — effectively zeroing it out. Net shipping is zero; the merchant absorbs whatever the courier charges. Full mechanics on [[shipping-discount-value-mechanics]].

### One shipping discount per cart at checkout

The cart's discount-applicator picks at most **ONE** shipping-type discount per cart at totals time. Code-based shipping coupons reach the cart through a different path than no-code shipping; the no-code pool query explicitly excludes code variants. Selection rules + the misnamed "sorted by `order_over DESC`" myth are on [[shipping-discount-stacking]].

### Permissions

The form and CRUD endpoints are scoped under the standard `marketing.discounts` permission.

## Related

- [[marketing-discounts]] — parent feature; the Shipping discount type lives there alongside flat / percent / fixed / quantity / countdown / code-pro.
- [[marketing-discounts-codes]] — Container codes (a different code-based discount type; codes can also be `shipping`-typed via Container generation).
- [[marketing-discounts-code-pro]] — Code PRO multi-code campaigns; each PRO code can independently be a `shipping` condition.
- [[marketing-discounts-fixed]] — Fixed-price discount (compare: shipping changes the shipping line, Fixed changes the product price).
- [[marketing-discounts-countdown]] — Countdown timer discount (a different visual-urgency style).
- [[apps-cart-rules]] — for partial-shipping discounts (e.g., "10% off shipping" — which Discounts cannot do — use Cart Rules).
- [[geo-zone]] — region restriction via `geo_zone_id`; very common with shipping discounts.
- [[customers-custom-groups]] — customer-group restriction (e.g., "Free shipping for VIPs only").
- [[settings-hooks]] — `discount.created` / `updated` / `deleted` webhooks.
- [[settings-statuses]] — `discounts_used_statuses` setting controls which statuses count toward `max_uses`.
- [[shipping]] — store's shipping providers; the free-shipping discount zeroes out the provider's quote.
- [[orders-shipping-waybill]] — the waybill picker that hides the receiver-pays option when "has free shipping" is set.
- [[analytics-top-order-discounts]] — analytics dashboard surfacing top order-level discounts including shipping discounts.
- [[discount]] — entity page for the underlying Discount record.
- [[discount-stacking]] — cross-discount stacking matrix + the per-type 10-minute-cooldown table.

## Open questions

No outstanding questions at the hub level. Per-aspect open questions live on the aspect pages.
