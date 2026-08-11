---
type: feature
nav_path: "Marketing → Discounts → Percent"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount", "Percentage discount", "% off discount", "Cart percent discount", "Percentage promotion", "-X% off", "Процентна отстъпка", "Процент отстъпка"]
tags: [marketing, discounts, percent]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Percent discount (`-X% off`)

## Purpose

The **Percent discount** is the most-used promotion type in CloudCart: subtract a **percentage** from the cart. It answers the merchant's question: *"I want to give customers 15% off — either off the whole cart, off orders above a threshold, off a category, off a brand, or off a smart collection."*

Together with the **Flat discount** (see [[marketing-discounts-flat]]), Percent is one of the **two most-used discount types** on CloudCart. Examples merchants run daily:

- "20% off everything for Black Friday."
- "15% off orders over 100 EUR."
- "10% off the Electronics category this week."
- "25% off all products from Brand X."
- "30% off with code SPRING30."

A Percent discount is the **`percent` type** in the discount system. It's stored as **whole-percent value × 100** (`type_value` — so 15% is stored as 1500, 100% as 10000), targeted via the `settings` field, and applies to the cart at checkout — either reducing the cart total by the percentage (cart-wide) or reducing matched-line subtotals (category / vendor / selection targets). The same `percent` type powers both **Global** (no code) and **Promo code** discounts — the difference is whether `code` is set; everything else (targeting, validity, customer-group rules) is identical.

Unlike [[marketing-discounts-fixed]] (which writes a per-variant *replacement* price), Percent discounts compute their reduction at **cart-evaluation time** — the catalog price stays unchanged on listing pages; only the cart total goes down.

## Where to find it

**Sidebar → Marketing → Discounts → + Add discount.** The type-picker modal shows ten cards. To create a Percent discount:

- **For a cart-wide / no-code promotion** ("15% off any order"): click the **Global discount** card. The route is `/admin/marketing-new/discounts/create/global`. In the form, set "Discount type" to **Percentage**.
- **For a promo-code-driven discount** ("20% off with code SPRING20"): click the **Discount with promo code** card. The route is `/admin/marketing-new/discounts/create/code`. In the form, set "Discount type" to **Percentage**.

In both cases, the same backend `percent` type is created — the only difference is whether `code` is set. The list view labels the discount with its target-link summary (e.g., "15% off orders over 100 EUR").

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[percent-discount-editor]] — the form's two entry surfaces (Global discount card vs Discount with promo code card), section layout, conditional sub-flows per target, generate-code helper, delete + active-toggle controls.
- [[percent-discount-fields]] — every backend key, field label, default, and validation string across General / Target / Limits / Customer groups / Color / Date / Code blocks.
- [[percent-discount-targeting]] — the seven `settings` target values (`all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`), cross-validation rejects, parent-child rule, the 10,000-combinations cap.
- [[percent-discount-stacking]] — Percent + Flat winner-takes-all on shared `order_over`; the `code_apply` gate; `apply_regular_price` re-evaluation; Cart Rules ordering; Quantity-tier interaction; one-code-at-a-time rule.
- [[percent-discount-validity]] — active-at-checkout gate, date-window rules (`date_start` / `date_end`), UTC auto-disable sweep, 10-minute activation cooldown, strict-greater `order_over` rule, uses-counter statuses, per-customer cap auto-clear.
- [[percent-discount-plan-gates]] — `discount_global` (no-code) vs `discount_coupon` (code-based) quotas, HTTP 403 overflow, the in-product counter as the reliable enforcement point.
- [[percent-discount-programmatic-access]] — JSON-API v2 + GraphQL admin-session writes, same-side-effects principle, `discount.created` / `discount.updated` / `discount.deleted` webhooks, absence of audit-log rows.

## What the merchant can do here

- Configure a no-code or code-driven Percent discount — see [[percent-discount-editor]].
- Pick one of seven targets (cart-wide, orders over, products, category, vendor, smart collection, or category+vendor intersection) — see [[percent-discount-targeting]].
- Cap the percent value at 100 with required `type_value > 0`; set name up to 191 chars; see [[percent-discount-fields]].
- Restrict by customer groups, registered users (`order_over` only), and (for code-variants) geo zone — see [[percent-discount-fields]].
- Stack with Cart Rules, Quantity tiers, Countdown, Free-shipping, and another code-Percent — but NOT with another `order_over` Flat at the same time (winner-takes-all). See [[percent-discount-stacking]].
- Toggle `active` instantly the first time, then live with a 10-minute cooldown — see [[percent-discount-validity]].
- Drive Percent CRUD via JSON-API v2 or GraphQL admin-session and observe `discount.*` webhooks — see [[percent-discount-programmatic-access]].

### What the merchant CANNOT do here

- Set `type_value` above 100 — validator rejects with *"The rate must not be greater than 100"*. See [[percent-discount-fields]].
- Combine incompatible target arrays (e.g. `products` + `order_over`) — see [[percent-discount-targeting]].
- Reuse a `code` string across discounts — *"Code already taken"*. See [[percent-discount-fields]].
- Reactivate a no-code Percent within 10 minutes of the last toggle — see [[percent-discount-validity]].
- Apply a Percent code to a cart with any line on a per-product discount unless `code_apply = 1` — see [[percent-discount-stacking]].

## Settings & fields

Per-aspect breakdown:

- General settings (`active`, `name`, `type`, `type_value`), Target (`settings`, `order_over`, `force_save`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]`), Limits (`max_uses`, `maxused_user`), Customer groups + registered users (`customer_groups_target`, `customer_groups[]`, `only_customer`, `customers[]`), Color (`color`, `text_color`, `discount_amount_type_in_label`), Date range (`date_start`, `date_end`, `no_expire`), and Code-specific fields (`code`, `code_format`, `barcode_prefix`, `code_apply`, `apply_regular_price`, `geo_zone_id`, `all_regions`) — see [[percent-discount-fields]].

## Business rules

Cross-cutting summary; detail lives on the aspect pages:

- **Percent cap is 100, min > 0**; `type_value` stored as `percent × 100`. See [[percent-discount-fields]].
- **Whole-cart vs targeted reduction** — `all` / `order_over` reduce the whole cart subtotal; specific targets reduce only matched lines. See [[percent-discount-targeting]].
- **`code_apply` + `apply_regular_price` semantics** — default-off code stacking on `order_over` carts with already-discounted lines; `apply_regular_price = 1` picks the bigger saving. See [[percent-discount-stacking]].
- **Percent + Flat winner-takes-all on shared `order_over` no-code**; other combos (Quantity, Countdown, Cart Rules, code-Percent, free-shipping) stack. Cart Rules see the cart total AFTER the Percent reduction. See [[percent-discount-stacking]].
- **Strictly-greater `order_over` check**, UTC auto-disable sweep (~27 h lag), 10-minute activation cooldown (no-code Percent only), `uses` counter only at `discounts_used_statuses`, per-customer cap auto-clears the code on hit. See [[percent-discount-validity]].
- **`force_save` keeps the discount attached** during admin order edits that drop the cart below the threshold. See [[percent-discount-targeting]].
- **One code at a time on the cart** — switching codes overwrites the previous. See [[percent-discount-stacking]].
- **Plan-gating** — `discount_global` (no-code) and `discount_coupon` (code) quotas; HTTP 403 on overflow. See [[percent-discount-plan-gates]].
- **JSON-API v2 + GraphQL writable**, same side effects as admin save; no audit-log row captured `(verify)`. See [[percent-discount-programmatic-access]].

## Related

- [[marketing-discounts]] — parent hub; Percent is one of seven discount types.
- [[marketing-discounts-flat]] — sister type (flat amount-off). Same form, same rules, different `type_value` semantics.
- [[marketing-discounts-fixed]] — different model (per-product fixed *price*, not subtract percent).
- [[marketing-discounts-shipping]] — Free-shipping sibling.
- [[marketing-discounts-codes]] — Container codes; mass-generated single-use coupons that can be flat or percent.
- [[marketing-discounts-code-pro]] — multi-code campaigns where each code has its own flat / percent terms.
- [[marketing-discounts-quantity]] — Quantity-tier discount; stacks with Percent code per per-line interaction in [[percent-discount-stacking]].
- [[marketing-discounts-countdown]] — Countdown discount type.
- [[apps-cart-rules]] — multi-condition rules engine. Evaluated AFTER Percent discount.
- [[customers-custom-groups]] — customer-group restriction via `customer_groups[]`.
- [[geo-zone]] — region restriction via `geo_zone_id`.
- [[products-categories]] — target via `product_categories[]`.
- [[products-vendors]] — target via `vendors[]`.
- [[products-smart-collections]] — target via `selections[]`.
- [[settings-hooks]] — fires `discount.created` / `discount.updated` / `discount.deleted` webhooks.
- [[settings-statuses]] — `discounts_used_statuses` determines what counts toward `max_uses`.
- [[analytics-top-order-discounts]] — analytics: most-used order-level discounts.
- [[discount]] — entity page.
- [[discount-stacking]] — cross-type cooldown table + stacking ladder.
- [[plan-gates]] — `discount_global` + `discount_coupon` plan mechanics.
- [[json-api-v2]] — API authentication + same-side-effects principle.

## Open questions

None at the hub level — see each aspect's `## Open questions` for unresolved items.
