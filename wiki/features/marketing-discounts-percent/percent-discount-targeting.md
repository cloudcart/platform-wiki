---
type: feature
nav_path: "Marketing → Discounts → Percent → Targeting"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount targeting", "Percent discount settings field", "Percent discount targets"]
tags: [marketing, discounts, percent, targeting]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, stacking, validity, plan gates, programmatic access).

# Percent discount — targeting (`settings` field)

## Purpose

The `settings` field decides **which cart lines** a Percent discount applies to. It is a single enum picked from one of seven values; companion arrays carry the IDs the merchant selected. This page is the lookup for *"what do my chosen targets mean?"*, *"why can't I combine these two?"*, and *"what is the 10,000-combinations limit?"*.

## Where to find it

The **Discount target** dropdown lives in the second section of the Percent create / edit form ([[percent-discount-editor]]) — opened via [[marketing-discounts]] → **+ Add discount** → **Global discount** or **Discount with promo code**. Picking a target slides open the matching companion-field block (orders-over input, product picker, category picker, etc.) per the editor's sub-flow table.

## What the merchant can do here

- Pick one of seven `settings` values to choose the cart-line scope (cart-wide, orders-over, specific products, category, vendor, smart collection, or category+vendor intersection).
- Fill the companion array required for the chosen target (`products[]`, `product_categories[]`, `vendors[]`, `selections[]`, or two arrays for `category_vendor`).
- For `order_over`, set the threshold amount + the optional `force_save` switch.
- Combine targets within validation limits — see the cross-validation matrix below.

## Targets the merchant can choose

| Target value (`settings`) | Means | Companion fields |
|---------------------------|-------|------------------|
| `all` — *"For every product in the cart"* | Cart-wide percent off. | — |
| `order_over` — *"Orders over"* | Cart subtotal must be ≥ `order_over` EUR (strict greater at evaluation — see [[percent-discount-validity]]). | `order_over` amount, optional `force_save`. |
| `product` — *"Specific product/s"* | Only listed products get the percent-off. | `products[]`. |
| `product_category` — *"Product category/categories"* | Only products in the listed [[products-categories]]. | `product_categories[]`. |
| `product_vendor` — *"Product vendor/s"* | Only products of the listed [[products-vendors]]. | `vendors[]`. |
| `selection` — *"Smart collection/s"* | Only products in the listed [[products-smart-collections]]. | `selections[]`. |
| `category_vendor` — *"Product category/categories and vendor/s"* | Intersection: products in category X **AND** by vendor Y. | Both `product_categories[]` and `vendors[]`. |

## Whole-cart vs targeted reduction

- **Target = `all`** — The percent reduces the **whole cart** subtotal. 20% off a 100 EUR cart → customer pays 80 EUR.
- **Target = `order_over`** — Same as `all`, but only applies when cart subtotal is strictly greater than `order_over`. The discount itself is still cart-wide.
- **Target = `product` / `product_category` / `product_vendor` / `selection` / `category_vendor`** — The percent reduces the **matched lines** individually. Each matched line's unit price drops by the percent. Non-matched lines keep their full price.

## Cross-validation matrix (what you cannot combine)

- **Combine `products` and `order_over`** — rejected: *"The field products can not be used with orders over"*.
- **Combine `product_categories` and `products` / `order_over` / `selections`** — each pair has its own validation reject (*"The field product_categories can not be used with orders over"*, etc.).
- **Use parent and child categories at the same time** — rejected: *"Parent and Child product categories, can not be included"*.

## Targeting and matching mechanics

At checkout, the discount engine walks the active Percent discounts and for each one:

1. Filters by `customer_groups[]`, `geo_zone_id`, `only_customer`, date window, uses-remaining (see [[percent-discount-validity]]).
2. Reads the `settings` field and matches the cart against the target:
   - `all` — every line matches.
   - `order_over` — subtotal must be strictly greater than `order_over` (see [[percent-discount-validity]] for the strictly-greater rule + 99.99 workaround).
   - `product` — only lines with matching `product_id`.
   - `product_category` — only lines whose product category (or any parent) is in the list.
   - `product_vendor` — only lines whose vendor matches.
   - `selection` — only lines whose smart-collection membership matches.
   - `category_vendor` — both category AND vendor must match.
3. For each matched line, multiplies the line's effective price by `type_value / 10000` to get the per-line discount amount.
4. For target=`all` / `order_over`, the percent applies to the **whole cart subtotal**; the engine then distributes the reduction across lines.

## Maximum combinations cap (10,000)

When the Percent discount targets the **intersection of many dimensions**, the platform multiplies the array sizes (products × categories × customer_groups × selections) and rejects if the total exceeds 10,000:

> *"The maximum combinations allowed is 10,000, current: :count"*

Typically only triggers on large `category_vendor` / `selection` discounts with many customer groups.

## Settings & fields

### Target-related fields

| Field | Backend key | What it does |
|---|---|---|
| **Discount target** | `settings` | The enum picked from the dropdown — `all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`. |
| **Order amount threshold** | `order_over` | Cart-subtotal threshold for `order_over` target (max 10,000 EUR / 1,000,000 cents). |
| **Save the discount in the order** | `force_save` | When ON, the discount stays attached during admin order edits that drop the cart below the threshold. |
| **Products** | `products[]` | Product IDs for `product` target. |
| **Product categories** | `product_categories[]` | Category IDs for `product_category` / `category_vendor`. |
| **Product vendors** | `vendors[]` | Vendor IDs for `product_vendor` / `category_vendor`. |
| **Smart collections** | `selections[]` | Smart-collection IDs for `selection`. |

Full validation strings live on [[percent-discount-fields]].

## `force_save` for `order_over` targets

For Percent discounts with target=`order_over`, the merchant can toggle **Save the discount in the order**. When ON, an admin editing an order that previously qualified for the discount keeps the discount attached EVEN IF the new cart contents fall below the `order_over` threshold. Without `force_save`, editing such an order removes the discount.

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
