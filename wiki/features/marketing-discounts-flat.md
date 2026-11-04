---
type: feature
nav_path: "Marketing → Discounts → Flat"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global, /admin/marketing/discounts/create/code
aliases: ["Flat discount", "Fixed amount discount", "Amount-off discount", "Cart amount discount", "Money-off promotion", "-X EUR off", "Сума отстъпка", "Фиксирана сума отстъпка"]
tags: [marketing, discounts, flat]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-05-23
updated: 2026-11-04
source_count: 4
---
# Flat-amount discount (`-X EUR off`)

## Purpose

The **Flat discount** takes a **fixed currency amount** off. What the amount comes off depends on the target and on whether there is a code: see [[discount-stacking-amount-by-target]]. It answers the merchant's question: *"I want to give customers 20 EUR off — off every product, off orders above 100 EUR, off a specific category, or off a specific brand."*

Together with the **Percentage discount** (see [[marketing-discounts-percent]]), Flat is one of the **two most-used discount types** on CloudCart. A Flat discount is the **`flat` type** in the discount system — stored as an **amount in cents** (`type_value`) and targeted via the `settings` field. The same `flat` type powers both **Global** (no code) and **Promo code** discounts — the difference is whether `code` is set, and that changes how the amount is applied. Unlike [[marketing-discounts-fixed]] (which writes a per-variant *replacement* price), Flat subtracts an amount. Without a code, on `all` or a specific target, it comes off each unit as the product's own price, listings included. With a code, or on `order_over`, the catalog price stays as it is.

## Where to find it

**Sidebar → Marketing → Discounts → + Add discount.** The type-picker modal shows ten cards.

- **For a no-code promotion** ("20 EUR off orders over 100 EUR"): click the **Global discount** card. The route is `/admin/marketing/discounts/create/global`. In the form, set "Discount type" to **Fixed amount**.
- **For a promo-code-driven discount** ("20 EUR off with code WELCOME20"): click the **Discount with promo code** card. The route is `/admin/marketing/discounts/create/code`. In the form, set "Discount type" to **Fixed amount**.

In both cases, the same backend `flat` type is created — the difference is whether `code` is set. The list view labels the discount with its target-link summary (e.g., "10 EUR off orders over 50 EUR").

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[flat-discount-form-entry]] — entry surfaces (Global discount vs Discount with promo code), form blocks, sliding sub-forms, code generator, row toggle / delete.
- [[flat-discount-targeting]] — the `settings` enum (`all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`), what the amount comes off, multi-line distribution + cent-fix, `force_save`.
- [[flat-discount-value-mechanics]] — `type_value` cents storage, no maximum amount, an amount larger than the subtotal, matched-subtotal gating, strictly-greater `order_over` check, per-customer cap clearing the code.
- [[flat-discount-eligibility]] — date window, customer groups, geo zone, `only_customer`, `max_uses` / `maxused_user`, counted statuses, plan checks, hourly UTC auto-disable sweep.
- [[flat-discount-stacking]] — `code_apply` default-off block per target, `apply_regular_price` comparison, highest threshold wins among no-code `order_over` discounts, order against [[apps-cart-rules]] / Quantity tiers.
- [[flat-discount-programmatic-access]] — JSON-API v2 (`<store>/api/v2/discounts`), GraphQL mutations, what each path validates, `discount.created` / `discount.updated` webhooks, absence of an audit-log row.

## What the merchant can do here

- **Create** a no-code Flat discount or a code-driven Flat discount — see [[flat-discount-form-entry]].
- **Target** the discount at every product in the cart, an order-value threshold, specific products, a category, a vendor, a smart collection, or a category+vendor intersection — see [[flat-discount-targeting]].
- **Set the amount** in EUR (stored as cents on `type_value`) — see [[flat-discount-value-mechanics]].
- **Restrict eligibility** by customer group, geo zone, registered-users-only, date window, total uses, per-customer uses — see [[flat-discount-eligibility]].
- **Control stacking** with `code_apply` and `apply_regular_price` for code-based variants — see [[flat-discount-stacking]].
- **Create / update / toggle / delete** via JSON-API v2 or GraphQL — see [[flat-discount-programmatic-access]].
- **Toggle active status** inline from the list row; it takes effect immediately.
- **Customise the storefront label** colour and amount-display format (no-code form) — the radio offers two choices, **As percent** (`in_percent`) or **As fixed amount** (`in_flat`).

## Settings & fields

Top-level fields on the Flat discount form. Per-field validation and detailed semantics live in the aspect pages.

| Field group | Backend keys | Documented in |
|-------------|--------------|---------------|
| **Status / name / type** | `active`, `name` (max 191), `type=flat` | [[flat-discount-form-entry]] |
| **Discount value** | `type_value` (entered EUR, stored cents) | [[flat-discount-value-mechanics]] |
| **Target enum** | `settings` ∈ `all` / `order_over` / `product` / `product_category` / `product_vendor` / `selection` / `category_vendor` | [[flat-discount-targeting]] |
| **Target arrays + threshold** | `order_over`, `force_save`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]` | [[flat-discount-targeting]] |
| **Use limits** | `max_uses`, `maxused_user` (no-code form: only `all` / `order_over`; code form: every target) | [[flat-discount-eligibility]] |
| **Audience** | `customer_groups_target`, `customer_groups[]`, `only_customer`, `customers[]` | [[flat-discount-eligibility]] |
| **Date window** | `date_start`, `date_end`, `no_expire` | [[flat-discount-eligibility]] |
| **Region (code variant)** | `geo_zone_id`, `all_regions` | [[flat-discount-eligibility]] |
| **Label appearance (no-code form)** | `color`, `text_color`, `discount_amount_type_in_label` (radio: `in_percent` / `in_flat`; auto-defaults `in_flat` for Flat) | [[flat-discount-form-entry]] |
| **Promo code** | `code` (max 20 chars, unique, case-insensitive), `code_format` (`ean13` / `ean8`), `barcode_prefix` | [[flat-discount-form-entry]] |
| **Stacking toggles (code)** | `code_apply` (defaults OFF), `apply_regular_price` (visible when `code_apply=1`) | [[flat-discount-stacking]] |

## Business rules

Cluster-wide rules summary. Detail (matrices, error strings, edge cases) lives in the named aspect.

- **Cents storage, no maximum amount** — see [[flat-discount-value-mechanics]].
- **What the amount comes off** — code on `all`: the full amount off every line. `order_over`: one amount off the order. Code on a specific target: one amount split over the matching lines, rounding difference on the first. No code on `all` or a specific target: per unit, as the product's own price — see [[discount-stacking-amount-by-target]].
- **Matched-subtotal gate** — a Flat code on `all` or a specific target is refused at entry unless the matching lines add up to at least `type_value`. `order_over`, with or without a code, requires the subtotal **strictly above** the threshold; a code on `order_over` does not compare the amount with the subtotal — see [[flat-discount-value-mechanics]].
- **Eligibility predicates** — `active=yes` AND date window AND uses-remaining AND customer-group / geo-zone / registered-user match — see [[flat-discount-eligibility]].
- **UTC auto-disable** — an hourly sweep flips `active=no` at its first run after 00:00 UTC on the day after `date_end`; storefront gating uses store TZ — see [[flat-discount-eligibility]].
- **`code_apply` default OFF** — a code on `order_over` is refused with a message on a cart with any product-discounted line; a code on `all` or a specific target skips those lines. With `apply_regular_price=1` the code replaces the product discount if its price is lower, otherwise the line keeps the product discount and no code — see [[flat-discount-stacking]].
- **Several no-code `order_over`** — the highest threshold the subtotal passes wins, whatever it saves, flat or percent. Product-level discounts on one line never add up. Order-level kinds do not exclude each other — see [[flat-discount-stacking]].
- **Cart Rules ordering** — [[apps-cart-rules]] conditions see the total after product discounts and line-level codes, before order-level discounts such as `order_over`.
- **Uses counter** — counts only orders reaching `discounts_used_statuses` (defaults `paid`, `completed`, `fulfilled`) — see [[flat-discount-eligibility]].
- **Plan gates** — the admin form checks on create whether that kind is enabled on the plan (HTTP 403, no numeric limit). JSON-API v2 compares usage with `discount_global` / `discount_coupon` (HTTP 402) — see [[flat-discount-eligibility]].
- **Separate validation per source** — admin, JSON-API v2 and GraphQL each validate on their own; no audit-log row — see [[flat-discount-programmatic-access]].

## Related

- [[marketing-discounts]] — parent hub; the Flat type is one of seven discount types.
- [[marketing-discounts-percent]] — the sister type (percentage-off). Same form, same rules, different `type_value` semantics.
- [[marketing-discounts-fixed]] — different model (per-product fixed *price*, not subtract amount).
- [[marketing-discounts-codes]] — Container codes; one store-wide pool of generated percent codes, reusable until turned off or deleted.
- [[marketing-discounts-code-pro]] — multi-code campaigns where each code has its own flat / percent terms.
- [[apps-cart-rules]] — multi-condition rules engine. Its conditions see the total after product discounts and line-level codes.
- [[customers-custom-groups]] — customer-group restriction via `customer_groups[]`.
- [[geo-zone]] — region restriction via `geo_zone_id`.
- [[products-categories]] — target via `product_categories[]`.
- [[products-vendors]] — target via `vendors[]`.
- [[products-smart-collections]] — target via `selections[]`.
- [[settings-hooks]] — `discount.*` webhooks; [[flat-discount-programmatic-access]] says when they fire.
- [[settings-statuses]] — `discounts_used_statuses` determines what counts toward `max_uses`.
- [[analytics-top-order-discounts]] — analytics: most-used order-level discounts.
- [[discount]] — entity page.

## Open questions

No outstanding questions.
