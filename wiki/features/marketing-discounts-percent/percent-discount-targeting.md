---
type: feature
nav_path: "Marketing → Discounts → Percent → Targeting"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Percent discount targeting", "Percent discount settings field", "Percent discount targets"]
tags: [marketing, discounts, percent, targeting]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, stacking, validity, plan gates, programmatic access).

# Percent discount — targeting (`settings` field)

## Purpose

The `settings` field decides **which cart lines** a Percent discount applies to. It is a single enum picked from one of seven values; companion arrays carry the IDs the merchant selected. This page is the lookup for *"what do my chosen targets mean?"*.

## Where to find it

The **Discount target** dropdown lives in the second section of the Percent create / edit form ([[percent-discount-editor]]) — opened via [[marketing-discounts]] → **+ Add discount** → **Global discount** or **Discount with promo code**. Picking a target slides open the matching companion-field block (orders-over input, product picker, category picker, etc.) per the editor's sub-flow table.

## What the merchant can do here

- Pick one of seven `settings` values to choose the cart-line scope (every product in the cart, orders-over, specific products, category, vendor, smart collection, or category+vendor intersection).
- Fill the companion array required for the chosen target (`products[]`, `product_categories[]`, `vendors[]`, `selections[]`, or two arrays for `category_vendor`).
- For `order_over`, set the threshold amount + the optional `force_save` switch.

## Targets the merchant can choose

| Target value (`settings`) | Means | Companion fields |
|---------------------------|-------|------------------|
| `all` — *"For every product in the cart"* / *"За всеки продукт в количката"* | Code: percent off each line. No code: off each unit, as the product's own price. | — |
| `order_over` — *"Orders over"* / *"Поръчки над"* | Cart subtotal must be strictly above `order_over` EUR (see [[percent-discount-validity]]). One amount off the order. | `order_over` amount, optional `force_save`. |
| `product` — *"Specific product/s"* / *"Конкретен продукт/и"* | Only listed products get the percent-off. | `products[]`. |
| `product_category` — *"Product category/categories"* / *"Продуктова категория"* | Only products in the listed [[products-categories]]. | `product_categories[]`. |
| `product_vendor` — *"Product vendor/s"* / *"Марка"* | Only products of the listed [[products-vendors]]. | `vendors[]`. |
| `selection` — *"Smart collection/s"* / *"Колекция"* | Only products in the listed [[products-smart-collections]]. | `selections[]`. |
| `category_vendor` — *"Product category/categories and vendor/s"* / *"Категория и производител"* | Intersection: products in category X **AND** by vendor Y. | Both `product_categories[]` and `vendors[]`. |

## What the percent comes off

See [[discount-stacking-amount-by-target]] for the full table.

- **Target = `all`, code** — the percent comes off each line, shown inside the line, with no row in the totals. Lines with a product discount are skipped while `code_apply` is off.
- **Target = `all`, no code** — off each unit, as the product's own price, listings included. Bundles are left out.
- **Target = `order_over`** — one amount off the order, shown as a row in the totals, when the subtotal is strictly greater than `order_over`. It is not spread across lines.
- **Target = `product` / `product_category` / `product_vendor` / `selection` / `category_vendor`** — only matching lines: per line with a code, per unit as the product's own price without one. Non-matched lines keep their full price.

## Targeting and matching mechanics

At checkout, the discount engine walks the active Percent discounts and for each one:

1. Filters by `customer_groups[]`, `geo_zone_id`, `only_customer`, date window, uses-remaining (see [[percent-discount-validity]]).
2. Reads the `settings` field and matches the cart against the target:
   - `all` — every line matches, except bundle products on a no-code discount, subscription lines set not to combine, and lines whose code was removed in the admin.
   - `order_over` — subtotal must be strictly greater than `order_over` (see [[percent-discount-validity]] for the strictly-greater rule + 99.99 workaround).
   - `product` — only lines with matching `product_id`.
   - `product_category` — only lines whose product category (or any parent) is in the list.
   - `product_vendor` — only lines whose vendor matches.
   - `selection` — only lines whose smart-collection membership matches.
   - `category_vendor` — both category AND vendor must match.
3. Works out the saving, with no rounding fix afterwards. Code on `all` or a specific target: the line total with options, after any product discount, × `type_value / 10000`, rounded per line. No code on `all` or a specific target: the unit price × `type_value / 10000`, rounded per unit, then × quantity, with the price floored at 0. `order_over`: the subtotal × `type_value / 10000`, rounded once (once per VAT group when VAT applies). So 3 × 3.33 EUR at 10% saves 0.99 EUR without a code and 1.00 EUR with one.

## Settings & fields

### Target-related fields

| Field | Backend key | What it does |
|---|---|---|
| **Discount target** | `settings` | The enum picked from the dropdown — `all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`. |
| **Order amount threshold** | `order_over` | Cart-subtotal threshold for `order_over` target. No maximum. |
| **Save the discount on your order** | `force_save` | When ON, the discount stays attached during admin order edits that drop the cart below the threshold. |
| **Products** | `products[]` | Product IDs for `product` target. |
| **Product categories** | `product_categories[]` | Category IDs for `product_category` / `category_vendor`. |
| **Product vendors** | `vendors[]` | Vendor IDs for `product_vendor` / `category_vendor`. |
| **Smart collections** | `selections[]` | Smart-collection IDs for `selection`. |

Full validation strings live on [[percent-discount-fields]].

## `force_save` for `order_over` targets

For Percent discounts with target=`order_over`, the merchant can toggle **Save the discount on your order**. When ON, an admin editing an order that previously qualified for the discount keeps the discount attached EVEN IF the new cart contents fall below the `order_over` threshold. Without `force_save`, the discount stays listed on the order, but its amount stops being deducted while the subtotal is not above the threshold.

## Business rules

- `force_save` lives on the row regardless of target but is meaningful only for `order_over`.
- For specific-product targets, the discount engine attaches to each matched line independently — order-of-evaluation between Percent and Quantity tiers is documented on [[percent-discount-stacking]].
- For `product_category`, the warning info-box in the editor reads *"The discount will only be applied to the main product category"* — secondary category memberships do NOT match.

## Related

- [[marketing-discounts-percent]] — hub.
- [[percent-discount-fields]] — every backend key + validation string.
- [[percent-discount-stacking]] — how matched lines combine with other discounts.
- [[percent-discount-validity]] — strictly-greater `order_over` rule.
- [[products-categories]] / [[products-vendors]] / [[products-smart-collections]] — target-array contents.

## Open questions

None.
