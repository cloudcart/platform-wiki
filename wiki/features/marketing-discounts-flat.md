---
type: feature
nav_path: "Marketing → Discounts → Flat"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Flat discount", "Fixed amount discount", "Amount-off discount", "Cart amount discount", "Money-off promotion", "-X EUR off", "Сума отстъпка", "Фиксирана сума отстъпка"]
tags: [marketing, discounts, flat]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Flat-amount discount (`-X EUR off`)

## Purpose

The **Flat discount** is the simplest cart-side promotion the merchant can run: subtract a **fixed currency amount** from the cart. It answers the merchant's question: *"I want to give customers 20 EUR off — either off everything in the cart, off orders above 100 EUR, off a specific category, or off a specific brand."*

Together with the **Percentage discount** (see [[marketing-discounts-percent]]), Flat is one of the **two most-used discount types** on CloudCart. A Flat discount is the **`flat` type** in the discount system — stored as an **amount in cents** (`type_value`), targeted via the `settings` field, and applied at cart-evaluation time. The same `flat` type powers both **Global** (no code) and **Promo code** discounts — the difference is whether `code` is set; everything else (targeting, validity, customer-group rules) is identical. Unlike [[marketing-discounts-fixed]] (which writes a per-variant *replacement* price), Flat discounts subtract their amount at cart-evaluation time — the catalog price stays unchanged on listing pages; only the cart total goes down.

## Where to find it

**Sidebar → Marketing → Discounts → + Add discount.** The type-picker modal shows ten cards.

- **For a cart-wide / no-code promotion** ("20 EUR off any order"): click the **Global discount** card. The route is `/admin/marketing-new/discounts/create/global`. In the form, set "Discount type" to **Fixed amount**.
- **For a promo-code-driven discount** ("20 EUR off with code WELCOME20"): click the **Discount with promo code** card. The route is `/admin/marketing-new/discounts/create/code`. In the form, set "Discount type" to **Fixed amount**.

In both cases, the same backend `flat` type is created — the only difference is whether `code` is set. The list view labels the discount with its target-link summary (e.g., "10 EUR off orders over 50 EUR").

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[flat-discount-form-entry]] — entry surfaces (Discount vs Discount with code), form blocks, sliding sub-forms, code generator, row toggle / delete.
- [[flat-discount-targeting]] — the `settings` enum (`all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`), mutual-exclusion validation, multi-line distribution + cent-fix, `force_save`.
- [[flat-discount-value-mechanics]] — `type_value` cents storage, the practically-uncapped amount validator, matched-subtotal gating, strictly-greater `order_over` check, per-customer cap silently clearing the code.
- [[flat-discount-eligibility]] — date window, customer groups, geo zone, `only_customer`, `max_uses` / `maxused_user`, counted statuses, plan-feature quotas, UTC auto-disable sweep, 10-minute activation cooldown.
- [[flat-discount-stacking]] — `code_apply` default-off block (silent-rejection per target), `apply_regular_price` re-evaluation, winner-takes-all when Global Flat + Global Percent both target `order_over`, slot ordering against [[apps-cart-rules]] / Quantity tiers, 10,000-combinations cap.
- [[flat-discount-programmatic-access]] — JSON-API v2 (`<store>/api/v2/discounts`), admin-session GraphQL mutations, shared side-effects pipeline, `discount.created` / `discount.updated` webhooks, absence of an audit-log row.

## What the merchant can do here

- **Create** a no-code cart-wide Flat discount or a code-driven Flat discount — see [[flat-discount-form-entry]].
- **Target** the discount at the whole cart, an order-value threshold, specific products, a category, a vendor, a smart collection, or a category+vendor intersection — see [[flat-discount-targeting]].
- **Set the amount** in EUR (stored as cents on `type_value`) and rely on the engine's matched-subtotal gating — see [[flat-discount-value-mechanics]].
- **Restrict eligibility** by customer group, geo zone, registered-users-only, date window, total uses, per-customer uses — see [[flat-discount-eligibility]].
- **Control stacking** with `code_apply` and `apply_regular_price` for code-based variants — see [[flat-discount-stacking]].
- **Create / update / toggle / delete** via JSON-API v2 or admin-session GraphQL — see [[flat-discount-programmatic-access]].
- **Toggle active status** inline from the list row, subject to the 10-minute per-discount cooldown (see [[flat-discount-eligibility]]).
- **Customise the storefront label** colour and amount-display format — the radio offers two choices, **As percent** (`in_percent`) or **As fixed amount** (`in_flat`).

## Settings & fields

Top-level fields on the Flat discount form. Per-field validation and detailed semantics live in the aspect pages.

| Field group | Backend keys | Documented in |
|-------------|--------------|---------------|
| **Status / name / type** | `active`, `name` (max 191), `type=flat` | [[flat-discount-form-entry]] |
| **Discount value** | `type_value` (entered EUR, stored cents) | [[flat-discount-value-mechanics]] |
| **Target enum** | `settings` ∈ `all` / `order_over` / `product` / `product_category` / `product_vendor` / `selection` / `category_vendor` | [[flat-discount-targeting]] |
| **Target arrays + threshold** | `order_over`, `force_save`, `products[]`, `product_categories[]`, `vendors[]`, `selections[]` | [[flat-discount-targeting]] |
| **Use limits** | `max_uses`, `maxused_user` (only `all` / `order_over`) | [[flat-discount-eligibility]] |
| **Audience** | `customer_groups_target`, `customer_groups[]`, `only_customer`, `customers[]` | [[flat-discount-eligibility]] |
| **Date window** | `date_start`, `date_end`, `no_expire` | [[flat-discount-eligibility]] |
| **Region (code variant)** | `geo_zone_id`, `all_regions` | [[flat-discount-eligibility]] |
| **Label appearance** | `color`, `text_color`, `discount_amount_type_in_label` (radio: `in_percent` / `in_flat`; auto-defaults `in_flat` for Flat) | [[flat-discount-form-entry]] |
| **Promo code** | `code` (max 20 chars, unique, case-insensitive), `code_format` (`ean13` / `ean8`), `barcode_prefix` | [[flat-discount-form-entry]] |
| **Stacking toggles (code)** | `code_apply` (defaults OFF), `apply_regular_price` (visible when `code_apply=1`) | [[flat-discount-stacking]] |

## Business rules

Cluster-wide rules summary. Detail (matrices, error strings, edge cases) lives in the named aspect.

- **Cents storage + character-capped validator** (verify) — see [[flat-discount-value-mechanics]].
- **Distribution** — `all` / `order_over` cart-wide; per-target subtracts from matched-line subtotal with a cent-fix on the first matched line — see [[flat-discount-targeting]].
- **Matched-subtotal gate** — Flat code rejected unless matched subtotal ≥ `type_value`; `order_over` requires **strictly greater than** threshold — see [[flat-discount-value-mechanics]].
- **Eligibility predicates** — `active=yes` AND date window AND uses-remaining AND customer-group / geo-zone / registered-user match — see [[flat-discount-eligibility]].
- **UTC auto-disable** — daily sweep flips `active=no` after `date_end + 1 day` in UTC; storefront gating uses store TZ — see [[flat-discount-eligibility]].
- **10-minute activation cooldown** — per-discount throttle on no-code Flat / Percent / Shipping / Fixed — see [[flat-discount-eligibility]].
- **`code_apply` default OFF** — code-based Flat silently rejected on a cart with any discounted line unless `code_apply=1`; `apply_regular_price=1` then picks the basis that maximises saving — see [[flat-discount-stacking]].
- **Winner-takes-all** — Global Flat + Global Percent both on `order_over` → only larger absolute saving wins. All other combinations stack — see [[flat-discount-stacking]].
- **Cart Rules ordering** — Discounts apply first; [[apps-cart-rules]] evaluate on the post-Flat total.
- **Uses counter** — increments only on orders reaching `discounts_used_statuses` (defaults `paid`, `completed`, `fulfilled`) — see [[flat-discount-eligibility]].
- **Plan gates** — `discount_global` (no-code) / `discount_coupon` (code-based); overflow returns HTTP 403 *"Not supported by plan"* (verify) — see [[flat-discount-eligibility]].
- **Same pipeline regardless of source** — admin / JSON-API v2 / GraphQL run identical validation + side-effects + webhooks; no audit-log row — see [[flat-discount-programmatic-access]].

## Related

- [[marketing-discounts]] — parent hub; the Flat type is one of seven discount types.
- [[marketing-discounts-percent]] — the sister type (percentage-off). Same form, same rules, different `type_value` semantics.
- [[marketing-discounts-fixed]] — different model (per-product fixed *price*, not subtract amount).
- [[marketing-discounts-codes]] — Container codes; mass-generated single-use coupons that can be flat or percent.
- [[marketing-discounts-code-pro]] — multi-code campaigns where each code has its own flat / percent terms.
- [[apps-cart-rules]] — multi-condition rules engine. Evaluated AFTER Flat discount.
- [[customers-custom-groups]] — customer-group restriction via `customer_groups[]`.
- [[geo-zone]] — region restriction via `geo_zone_id`.
- [[products-categories]] — target via `product_categories[]`.
- [[products-vendors]] — target via `vendors[]`.
- [[products-smart-collections]] — target via `selections[]`.
- [[settings-hooks]] — fires `discount.created` / `discount.updated` / `discount.deleted` webhooks.
- [[settings-statuses]] — `discounts_used_statuses` determines what counts toward `max_uses`.
- [[analytics-top-order-discounts]] — analytics: most-used order-level discounts.
- [[discount]] — entity page.

## Open questions

No outstanding questions.
