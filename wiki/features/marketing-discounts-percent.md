---
type: feature
nav_path: "Marketing → Discounts → Percent"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global, /admin/marketing/discounts/create/code
aliases: ["Percent discount", "Percentage discount", "% off discount", "Cart percent discount", "Percentage promotion", "-X% off", "Процентна отстъпка", "Процент отстъпка"]
tags: [marketing, discounts, percent]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-05-23
updated: 2026-11-04
source_count: 4
---
# Percent discount (`-X% off`)

## Purpose

The **Percent discount** is the most-used promotion type in CloudCart: take a **percentage** off. It answers the merchant's question: *"I want to give customers 15% off — off every product, off orders above a threshold, off a category, off a brand, or off a smart collection."*

Together with the **Flat discount** (see [[marketing-discounts-flat]]), Percent is one of the **two most-used discount types** on CloudCart. Examples merchants run daily:

- "20% off everything for Black Friday."
- "15% off orders over 100 EUR."
- "10% off the Electronics category this week."
- "25% off all products from Brand X."
- "30% off with code SPRING30."

A Percent discount is the **`percent` type** in the discount system. It's stored as **whole-percent value × 100** (`type_value` — so 15% is stored as 1500, 100% as 10000) and targeted via the `settings` field. What it comes off depends on the target and on whether there is a code: see [[discount-stacking-amount-by-target]]. The same `percent` type powers both **Global** (no code) and **Promo code** discounts — the difference is whether `code` is set, and that changes how the percent is applied.

Unlike [[marketing-discounts-fixed]] (which writes a per-variant *replacement* price), Percent subtracts a share of the price. Without a code, on `all` or a specific target, it comes off each unit as the product's own price, listings included. With a code, or on `order_over`, the catalog price stays as it is.

## Where to find it

**Sidebar → Marketing → Discounts → + Add discount.** The type-picker modal shows ten cards. To create a Percent discount:

- **For a no-code promotion** ("15% off orders over 100 EUR"): click the **Global discount** card. The route is `/admin/marketing/discounts/create/global`. In the form, set "Discount type" to **Percentage**.
- **For a promo-code-driven discount** ("20% off with code SPRING20"): click the **Discount with promo code** card. The route is `/admin/marketing/discounts/create/code`. In the form, set "Discount type" to **Percentage**.

In both cases, the same backend `percent` type is created — the difference is whether `code` is set. The list view labels the discount with its target-link summary (e.g., "15% off orders over 100 EUR").

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[percent-discount-editor]] — the form's two entry surfaces (Global discount card vs Discount with promo code card), section layout, conditional sub-flows per target, generate-code helper, delete + active-toggle controls.
- [[percent-discount-fields]] — every backend key, field label, default, and validation string across General / Target / Limits / Customer groups / Color / Date / Code blocks.
- [[percent-discount-targeting]] — the seven `settings` target values (`all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`), what each target's percent comes off, rounding.
- [[percent-discount-stacking]] — highest threshold wins among no-code `order_over`; the `code_apply` gate; `apply_regular_price` comparison; Cart Rules ordering; Quantity-tier interaction; one-code-at-a-time rule.
- [[percent-discount-validity]] — active-at-checkout gate, date-window rules (`date_start` / `date_end`), hourly UTC auto-disable sweep, strict-greater `order_over` rule, uses-counter statuses, per-customer cap auto-clear.
- [[percent-discount-plan-gates]] — what each path checks on create: admin form (HTTP 403), JSON-API v2 quotas `discount_global` / `discount_coupon` (HTTP 402), GraphQL.
- [[percent-discount-programmatic-access]] — JSON-API v2 + GraphQL writes, what each path validates, `discount.created` / `discount.updated` / `discount.deleted` webhooks, absence of audit-log rows.

## What the merchant can do here

- Configure a no-code or code-driven Percent discount — see [[percent-discount-editor]].
- Pick one of seven targets (every product in the cart, orders over, products, category, vendor, smart collection, or category+vendor intersection) — see [[percent-discount-targeting]].
- Keep the percent value at 100 or below, with required `type_value > 0`; set name up to 191 chars; see [[percent-discount-fields]].
- Restrict by customer groups, registered users (`order_over` only), and (for code-variants) geo zone — see [[percent-discount-fields]].
- Stack a no-code `order_over` with Cart Rules, Quantity tiers, Countdown, Free-shipping, and a code — but NOT with another no-code `order_over` (the highest threshold wins). See [[percent-discount-stacking]].
- Toggle `active` from the list; it takes effect immediately.
- Drive Percent CRUD via JSON-API v2 or GraphQL and observe `discount.*` webhooks — see [[percent-discount-programmatic-access]].

### What the merchant CANNOT do here

- Set `type_value` above 100 in the admin form. See [[percent-discount-fields]].
- Reuse a `code` string when creating a discount — *"Code must be unique"*. See [[percent-discount-fields]].
- Apply a Percent code on `order_over` to a cart with any line on a product discount unless `code_apply = 1` — see [[percent-discount-stacking]].

## Settings & fields

Per-aspect breakdown:

- General settings (`active`, `name`, `type`, `type_value`), Target (`settings`, `order_over`, `force_save`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]`), Limits (`max_uses`, `maxused_user`), Customer groups + registered users (`customer_groups_target`, `customer_groups[]`, `only_customer`, `customers[]`), Color (`color`, `text_color`, `discount_amount_type_in_label`), Date range (`date_start`, `date_end`, `no_expire`), and Code-specific fields (`code`, `code_format`, `barcode_prefix`, `code_apply`, `apply_regular_price`, `geo_zone_id`, `all_regions`) — see [[percent-discount-fields]].

## Business rules

Cross-cutting summary; detail lives on the aspect pages:

- **Percent cap is 100 in the admin form, min > 0**; `type_value` stored as `percent × 100`. See [[percent-discount-fields]].
- **What the percent comes off** — `all` and specific targets: per line with a code, per unit as the product's own price without one. `order_over`: one amount off the order. See [[discount-stacking-amount-by-target]].
- **`code_apply` + `apply_regular_price` semantics** — off: a code on `order_over` is refused on a cart with product-discounted lines, a code on `all` or a specific target skips those lines. `apply_regular_price = 1`: the code replaces the product discount if its price is lower, otherwise the line keeps the product discount and no code. See [[percent-discount-stacking]].
- **Several no-code `order_over`**: the highest threshold the subtotal passes wins, flat or percent. Order-level kinds stack with each other and with line discounts; product-level discounts on one line never add up. Cart Rule conditions see the total after product discounts and line-level codes, before order-level discounts. See [[percent-discount-stacking]].
- **Strictly-greater `order_over` check**, hourly UTC auto-disable sweep, `uses` counter only at `discounts_used_statuses`, per-customer cap auto-clears the code on hit. See [[percent-discount-validity]].
- **`force_save` keeps the discount attached** during admin order edits that drop the cart below the threshold. See [[percent-discount-targeting]].
- **One code at a time on the cart** — switching codes overwrites the previous. See [[percent-discount-stacking]].
- **Plan-gating** — the admin form checks on create whether that kind is enabled on the plan (HTTP 403, no numeric limit). JSON-API v2 compares usage with `discount_global` / `discount_coupon` (HTTP 402). See [[percent-discount-plan-gates]].
- **JSON-API v2 + GraphQL writable**, each with its own validation; no audit-log row captured. See [[percent-discount-programmatic-access]].

## Related

- [[marketing-discounts]] — parent hub; Percent is one of seven discount types.
- [[marketing-discounts-flat]] — sister type (flat amount-off). Same form, same rules, different `type_value` semantics.
- [[marketing-discounts-fixed]] — different model (per-product fixed *price*, not subtract percent).
- [[marketing-discounts-shipping]] — Free-shipping sibling.
- [[marketing-discounts-codes]] — Container codes; one store-wide pool of generated percent codes, reusable until turned off or deleted.
- [[marketing-discounts-code-pro]] — multi-code campaigns where each code has its own flat / percent terms.
- [[marketing-discounts-quantity]] — Quantity-tier discount; stacks with Percent code per per-line interaction in [[percent-discount-stacking]].
- [[marketing-discounts-countdown]] — Countdown discount type.
- [[apps-cart-rules]] — multi-condition rules engine. Its conditions see the total after product discounts and line-level codes.
- [[customers-custom-groups]] — customer-group restriction via `customer_groups[]`.
- [[geo-zone]] — region restriction via `geo_zone_id`.
- [[products-categories]] — target via `product_categories[]`.
- [[products-vendors]] — target via `vendors[]`.
- [[products-smart-collections]] — target via `selections[]`.
- [[settings-hooks]] — `discount.*` webhooks; [[percent-discount-programmatic-access]] says when they fire.
- [[settings-statuses]] — `discounts_used_statuses` determines what counts toward `max_uses`.
- [[analytics-top-order-discounts]] — analytics: most-used order-level discounts.
- [[discount]] — entity page.
- [[discount-stacking]] — cross-type stacking ladder.
- [[plan-gates]] — `discount_global` + `discount_coupon` plan mechanics.
- [[json-api-v2]] — API authentication.

## Open questions

None at the hub level — see each aspect's `## Open questions` for unresolved items.
