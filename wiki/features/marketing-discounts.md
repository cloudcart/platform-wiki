---
type: feature
nav_path: "Marketing → Discounts"
route_name: discounts-list
route_path: /admin/marketing/discounts, /admin/marketing/discounts/edit/:id
aliases: ["Discounts", "Promo codes", "Coupons", "Coupon codes", "Sales", "Promotions", "Промо кодове", "Отстъпки", "Купони"]
tags: [marketing, discounts, coupons, promo-codes, promotions]
plan_gates: ["total_discounts", "discount_global", "discount_fixed", "discount_coupon", "discount_quantity", "discount_banner", "discount-code-pro", "discount-code-pro-generator"]
created: 2026-05-21
updated: 2026-11-04
source_count: 8
---
# Discounts

## Purpose

The **Discounts** page is the merchant's main promotions toolbox — a catalogue of discount **types** (the **+ Add discount** modal offers 10 cards) that cover virtually every promotion model an online store needs. Compared to the more flexible [[apps-cart-rules]] (composable trigger + action engine), Discounts are simpler **single-condition** rules — one type, one target, one threshold — but cover the most common 80 % of merchant promotions: holiday sales, customer rewards, inventory liquidation, volume incentives, and flash sales.

This page is the **hub** for the entire Discounts area. Each discount **type** has its own per-type detail page (with create-form fields, save-time validation, and a worked example). Cross-cutting topics that apply to every type — lifecycle, eligibility, storefront display, audit trail, known issues — have their own aspect pages inside `marketing-discounts/`.

## Where to find it

**Sidebar → Marketing → Discounts.** The breadcrumb reads "Marketing → Discounts". The route is `/admin/marketing/discounts` (modern Vue UI). The old address `/admin/discounts/` redirects permanently to it; the legacy Smarty discount pages were removed on 2026-10-21.

## What the merchant can do here

From the list view:

- See every discount with name, type, code, date window, uses-count, max-uses limit, and active status. **Uses** on a plain code with uses above 0 opens `/admin/orders?filters[discountCode]=<code>` in a new tab. A barcode-prefix code shows a display form with no copy action.
- **+ Add discount** — opens the **type-picker modal** with 10 cards (listed below). Picking a card opens the matching create form. Only the **Discount code** (PRO) card can show an upgrade panel (*"To create a discount code, you need to upgrade your plan."*); the other cards always open their form.
- Toggle a discount **active / inactive** with the row switch. The change takes effect immediately, any number of times (see [[discounts-lifecycle]]). The switch is locked on discounts created by integrations.
- Bulk-toggle status or bulk-delete via the table action bar.
- Filter / sort by type (**Quantity discount** among them), code, date window (**Exactly**, before, after), uses, active state, etc.
- Drill into per-type sub-pages — Code management ([[marketing-discounts-code-pro]]), Container codes ([[marketing-discounts-codes]]), per-product overrides ([[marketing-discounts-products]]).

Things the merchant CANNOT do:

- Take a promo code off a line that already holds a product discount, unless `code_apply` is on — see [[discount-stacking-code-apply]].
- Tie two Quantity discounts to the same product — see [[discounts-known-issues]].
- See "who changed this discount and when" — there is no internal audit log; see [[discounts-audit-trail]].

## Sub-pages — per-type details

The **+ Add discount** modal offers **10 cards, in this order**. The first opens a separate engine, the last two are visual-only and managed under Products; the rest are the discount **types**, each with its own page (create-form fields, validation, worked example, storefront rendering). The same amount gives a different result depending on the code and the target: see [[discount-stacking-amount-by-target]].

- **Cart rules** — opens [[apps-cart-rules]] (a separate multi-condition engine, not a discount type).
- **Global discount** — an always-on, no-code discount. One "Discount type" select chooses the flavour: [[marketing-discounts-flat]] (fixed amount off, -10 EUR), [[marketing-discounts-percent]] (percentage off, -15 %), or [[marketing-discounts-shipping]] (Free shipping). Flat and percent target every product or specific products, categories, vendors or smart collections (off each unit, as the product's own price), or **Orders over** (one amount off the order). Free shipping targets all orders or orders over a threshold.
- **Discount with promo code** — a flat, percent or free-shipping discount applied only when the customer enters a code (the single-`code` variant on [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]]). **For every product in the cart**: a flat amount off each line. A specific target: one flat amount split across the matching lines. **Orders over**: one amount off the order.
- **Discount with multiple promo codes - Container** — a discount that takes its value from codes in one store-wide pool (for mail-outs), with the same targets as a promo code. The codes belong to no particular Container and are listed on [[marketing-discounts-codes]].
- **Fixed discount** — a fixed replacement price per product / variant; the target is the products and variants listed on it: [[marketing-discounts-fixed]] + per-product table [[marketing-discounts-products]].
- **Quantity discount** — buy-more-pay-less unit-price tiers; the target is ONE product (up to 12 tiers on the form for a product with one variant): [[marketing-discounts-quantity]].
- **Countdown discount** — flash sale + timer + confetti / fireworks / parade effect. It targets every product or orders over a threshold, and reduces the order as a row in the totals: [[countdown-discount-cart-totals]]. A second one can be saved, but checkout uses only the first active one found: [[marketing-discounts-countdown]].
- **Discount code** (PRO) — multi-code campaign where each code carries its own conditions, each with its own target; the only card that can show an upgrade panel: [[marketing-discounts-code-pro]] (+ [[marketing-discounts-code-pro-generator]], [[marketing-discounts-code-pro-export]]).
- **Label Discount** — a text label on products (visual only, not a price cut), managed under Products → Product labels: [[products-banners-labels]].
- **Visual Label/Image** — a sticker / image badge over products (visual only): [[products-banners-labels]].

## Sub-pages — cross-cutting aspects

Behaviour that applies uniformly across every discount type:

- [[discounts-lifecycle]] — `active`, date window, "No expiration", hourly auto-disable, immediate status switch, counted statuses.
- [[discounts-eligibility]] — customer-group / geo-zone / guest gating, `maxused_user`, `code_apply` stacking, `apply_regular_price`, `force_save`, resolution order.
- [[discounts-storefront-display]] — per-product attachment regen, cache invalidation, strikethrough, countdown timer / popup, smart-collection refresh.
- [[discounts-audit-trail]] — webhooks, per-order discount rows, `uses` mechanics, no internal audit log.
- [[discounts-known-issues]] — Countdown, Quantity per product, strict-greater rules, code lookup, JSON-API 5-type allowlist + HTTP 402.

## Sub-screens (routes)

| Label | Route name | Route path |
|-------|------------|------------|
| Discounts list | `discounts-list` | `/admin/marketing/discounts` |
| Create | `discounts-create` | `/admin/marketing/discounts/create/:type` |
| Edit | `discounts-edit` | `/admin/marketing/discounts/edit/:id` |
| Fixed-discount products | `discounts-products` | `/admin/marketing/discounts/products/:id` |
| Code PRO codes list | `discounts-code_pro-list` | `/admin/marketing/discounts/code-pro/:id` |
| Code PRO bulk generator | `discounts-code_pro-generator` | `/admin/marketing/discounts/code-pro/:id/generator` |
| Code PRO create / edit code | `discounts-code_pro-create` / `-edit` | `/admin/marketing/discounts/code-pro/:id/create` (or `/:codeId`) |
| Container codes list | `discounts-codes_list` | `/admin/marketing/discounts/codes` |

The backend API is namespaced under `admin.api.discounts.*` — CRUD + sub-routes for `products/{id}` (Fixed), `code-pro/{id}` (PRO), and `codes` (Container).


## Settings & fields

The hub does not introduce new fields directly. Field-level documentation lives on the per-type pages (for type-specific fields) and the cross-cutting aspect pages:

- Scheduling fields (`date_start`, `date_end`, `max_uses`, timer switches) → [[discounts-lifecycle]].
- Eligibility / stacking fields (`customer_groups[]`, `geo_zone_id`, `only_customer`, `maxused_user`, `code_apply`, `apply_regular_price`, `force_save`) → [[discounts-eligibility]].
- Display fields (`color`, `text_color`, `discount_amount_type_in_label`, `position`, `countdown_popup_effect`) → [[discounts-storefront-display]].
- Targeting fields (`type`, `type_value`, `settings`, `order_over`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]`) → the per-type page.
- Code / barcode fields (`code`, `code_format`, `code_prefix`, `barcode_prefix`) → the per-type page (code variants) and [[marketing-discounts-code-pro]].

## Business rules

All cross-cutting rules live on the aspect pages:

- **Active = `active=yes` AND in date window AND `max_uses > uses`** → [[discounts-lifecycle]].
- **Customer-group / region / guest gating; `code_apply` stacking; ONE no-code `order_over` winner (highest threshold passed); Cart Rules run after line-level discounts and before order-level discounts** → [[discounts-eligibility]].
- **Per-product attachment regen + cache invalidation + countdown rendering** → [[discounts-storefront-display]].
- **`discount.created` / `discount.updated` / `discount.deleted` webhooks; no internal audit log** → [[discounts-audit-trail]].
- **Edge cases (Countdown, Quantity per product, strict-greater `order_over`, code lookup, JSON-API 5-type allowlist + HTTP 402)** → [[discounts-known-issues]].

## Plan gates

Plan counters on discounts track how many discounts of a kind a store has, surfaced as the "used / limit" figure in the panel (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]). Usage counts discounts whether active or not; only deleting lowers it:

- `total_discounts` — aggregate figure across all discounts, displayed and not enforced.
- `discount_global` — no-code Flat / Percent / Shipping with `code_apply` off, which includes Countdown and Container discounts.
- `discount_coupon` — discounts holding their own code.
- `discount_fixed` — Fixed per-product discounts.
- `discount_quantity` — Quantity discounts.
- `discount_multi_coupon` — Container discounts. (verify)
- `discount_banner` / `discount_labels` — visual Banner / Label (see [[products-banners-labels]]).
- `discount-code-pro` (boolean) — whether Code PRO is available at all.
- `discount-code-pro-generator` (numeric) — max codes per bulk-generator run.

What is enforced depends on the path. The admin form, on create only, checks whether that kind of discount is enabled on the plan (`discount-<type>`) and otherwise returns **HTTP 403** with *"This feature is not enabled for your plan. To access it, please upgrade your plan."*, with no numeric limit. JSON-API v2, on create only, compares usage with `discount_global`, `discount_fixed` or `discount_coupon` and returns **HTTP 402 Payment Required**. GraphQL `createDiscount` checks only the Fixed and Quantity quotas; updates are not checked.

## Programmatic access

Discount creation, code generation, and product / category linkage can be driven via [[json-api-v2]] — see [[api-discounts]], [[api-discount-codes]], [[api-discount-codes-pro]], [[api-product-to-discount]]. Saving a discount sends the same `discount.created` / `discount.updated` webhooks as the form. API allowlist is **5 types** (`percent`, `flat`, `fixed`, `shipping`, `code-pro`); Quantity and Countdown are created in the admin panel or through the Admin GraphQL API. See [[discounts-known-issues]].

## Related

- [[marketing]] — parent hub.
- [[discount-stacking]] — how multiple discounts / codes / cart-rules combine (the cross-cutting model behind this screen).
- [[discount-stacking-amount-by-target]] — what a flat or percent amount comes off for each target, with and without a code.
- [[order-totals-pipeline]] — where discounts land in the order total (stage 2: before shipping + VAT).
- [[apps-cart-rules]] — composable multi-condition rules engine (runs after product discounts and line-level codes, before order-level discounts).
- [[apps-cart-rules-rules]] — Cart Rules sub-page.
- [[marketing-cross-sell]] — conditional product recommendations (different system).
- [[products-banners-labels]] — visual-only Label / Banner type.
- [[products-smart-collections]] — auto-curated lists; referenced by `selection`-target discounts.
- [[customers-custom-groups]] — `customer_groups[]` restriction.
- [[geo-zone]] — `geo_zone_id` restriction.
- [[settings-hooks]] — discount webhooks.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[analytics-top-order-discounts]] / [[analytics-top-order-product-discounts]] — analytics dashboards.
- [[marketing-segments]] — segment conditions reference discount usage.
- [[marketing-campaigns]] — campaigns can include dynamic-code replacements via PRO codes.
- [[apps-up-cross-sell]] — Cross-sell app references discounts in its conditional offers.
- [[discount]] / [[discount-code]] — entity pages.
- [[products-products]] / [[products-categories]] / [[products-vendors]] — discount targets reference these.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
