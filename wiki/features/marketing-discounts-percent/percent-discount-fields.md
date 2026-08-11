---
type: feature
nav_path: "Marketing → Discounts → Percent → Fields"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount fields", "Percent discount validation", "Percent backend keys"]
tags: [marketing, discounts, percent, fields, validation]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, targeting, stacking, validity, plan gates, programmatic access).

# Percent discount — settings & fields

## Purpose

This page catalogues every visible field, backend key, default, and validation string on the Percent create / edit form. It is the field-reference the support Assistant cites most when answering *"why did my save fail?"* / *"what does this field do?"* questions.

## Where to find it

The fields all live on the same admin form documented in [[percent-discount-editor]] — opened via [[marketing-discounts]] → **+ Add discount** → **Global discount** card (no-code, `/admin/marketing-new/discounts/create/global`) or **Discount with promo code** card (`/admin/marketing-new/discounts/create/code`). The code-specific block (`code`, `code_format`, `code_apply`, `apply_regular_price`, `geo_zone_id`, `all_regions`) appears only on the "Discount with promo code" entry.

## What the merchant can do here

- Set `active`, `name`, `type = percent`, and `type_value` (0-100 in the UI; stored × 100).
- Pick a target via `settings` + companion arrays — see [[percent-discount-targeting]].
- Cap total uses and per-customer uses (`max_uses`, `maxused_user`) on `all` / `order_over` targets.
- Restrict to specific `customer_groups[]`; for `order_over`, require `only_customer`.
- Customise the storefront label (`color`, `text_color`, `discount_amount_type_in_label`).
- Set the validity window (`date_start`, `date_end`, `no_expire`).
- For code variants: set the `code`, barcode mode, stacking toggles, and region restriction (see fields below).

## Settings & fields

### General settings

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount status** | `active` | Active = fires at checkout. Inactive = configured but skipped. | `yes` / `no`. |
| **Discount name** | `name` | Merchant-facing label. | Required, max 191 chars. *"The discount name must not be more than 191 characters"* / *"The discount name is required"*. |
| **Discount type** | `type` | Set to **Percentage** = `percent`. | Required, in `flat,percent,shipping,fixed,quantity,countdown,code-pro`. *"The selected type is invalid"*. |
| **Discount value** | `type_value` | The percentage as a **whole number, 0-100** — type `15` for 15% (**not** `0.15`). The form shows the whole percent; it is stored as `percent × 100` (e.g., 15% → 1500). | Required when type=percent. *"The percentage value can not be empty"*. Max **100%** (10000 stored). *"The rate must not be greater than 100"*. Min must be > 0. *"The rate must be at least"* (with `min` placeholder) fires when value ≤ 0. |

### Discount target

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount target** | `settings` | One of `all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`. | Required. *"The field settings is required"*. See [[percent-discount-targeting]]. |
| **Order amount threshold** | `order_over` | Cart-subtotal threshold for `order_over` target. | Required if settings=order_over; max **10,000 EUR** (1,000,000 cents). *"The field orders over can not be empty"*. |
| **Save the discount in the order** | `force_save` | When ON, the discount stays attached to a previously-saved order even when admin-side edits drop the cart below the threshold. | 1 / 0. Only shown for `order_over`. |
| **Products** | `products[]` | Product IDs to attach. | Required if settings=product. *"Please choose a product"*. Cannot combine with `order_over` / `product_categories`: *"The field products can not be used with orders over"* / *"The field products can not be used with product categories"*. |
| **Product categories** | `product_categories[]` | Category IDs (see [[products-categories]]). | Required if settings=product_category or category_vendor. *"Please choose a product category"*. Parent + child rejected: *"Parent and Child product categories, can not be included"*. Cross-validation rejects against `order_over`, `products`, `selections` with parallel messages. |
| **Product vendors** | `vendors[]` | Vendor IDs (see [[products-vendors]]). | Required if settings=product_vendor or category_vendor. |
| **Smart collections** | `selections[]` | Smart-collection IDs (see [[products-smart-collections]]). | Required if settings=selection. |

### Discount limits

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Global discount limit** | `max_uses` | Total uses across all customers. NULL = unlimited. | Integer 1-100,000. *"Maximum usage can be up to 100000"*. Only shown for `all` and `order_over` targets. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap. NULL = unlimited. | Integer 1-100,000. |
| **Unlimited** | (toggle) | Sets the corresponding limit to NULL. | — |

### Customer groups & registered users

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **All groups** | `customer_groups_target` | When ON, applies to every [[customers-custom-groups]]. | `yes` / `no`. |
| **Customer groups** | `customer_groups[]` | When `customer_groups_target=no`, list of group IDs. | Array. |
| **Discount available only to registered users** | `only_customer` | Guests cannot apply. | 1 / 0. Only shown for `order_over` target. |
| **Customers** | `customers[]` | Specific customer IDs that can use the discount. | Array of customer IDs. |

### Color & label appearance

| Field | Backend key | What it does |
|-------|-------------|--------------|
| **Background color** | `color` | Hex color for the discount badge / label on storefront. |
| **Text color** | `text_color` | Hex color for the label text. |
| **Show discount amount in label as** | `discount_amount_type_in_label` | Radio with two choices: `in_percent` or `in_flat`. Defaults to `in_percent` for Percent-type discounts. (`dont_change` is a valid backend value but is not offered in the radio.) |

### Date range

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Start date** | `date_start` | First day the discount applies. | Required. |
| **End date** | `date_end` | Last day. Skipped after this date. | Nullable. End must be after start. The `date_end` validator uses a strict "less-than" check against end-of-today in store timezone — so a `date_end` value equal to today IS accepted. See [[percent-discount-validity]]. |
| **No expiration** | `no_expire` | When ON, sets `date_end` to null. | — |

### Code-specific fields (when `code` is set)

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Promo code** | `code` | The literal code typed at checkout. Case-insensitive. | Required for code-based; max 20 chars; alphanumeric / `.` / `#`; unique across all discounts. *"Code already taken"*. |
| **Code format (barcode)** | `code_format` | `ean13` or `ean8` if the code is a barcode. | In `ean13`, `ean8`. |
| **Barcode prefix mode** | `barcode_prefix` | When ON, scanned value is matched as `code + scanned-suffix`. | 1 / 0. |
| **Apply discount even if the cart contains products with a discount** | `code_apply` | Allows stacking on already-discounted items. | 1 / 0. Defaults OFF. See [[percent-discount-stacking]]. |
| **Apply to the regular price of products, if this discount is greater** | `apply_regular_price` | When ON, re-evaluates against the catalog price (ignoring per-product Fixed discounts) if that would yield a bigger discount. | 1 / 0. Only shown when `code_apply=1`. |
| **Region (Geo zone)** | `geo_zone_id` | Restrict to a specific [[geo-zone]]. | Nullable. |
| **Make it Global** | `all_regions` | When ON, no region restriction. | `yes` / `no`. |

## Business rules

- **`type_value` is the whole percent in the UI, stored as percent × 100** — the merchant types `15` for 15% (**not** the decimal `0.15`); the edit form shows `15` and the stored value is `1500`. Validation runs on the stored value: cap 10,000 (= 100%), min implicitly > 0. **Via the API this differs**: `createDiscount` / JSON-API v2 store `type_value` exactly as sent (the ×100 is client-side in the form), so programmatically you send the **raw `1500`** for 15% — see [[percent-discount-programmatic-access]].
- **Maximum combinations cap of 10,000**: rejects when `products × product_categories × customer_groups × selections` exceeds 10,000 — *"The maximum combinations allowed is 10,000, current: :count"*. See [[percent-discount-targeting]].

## Related

- [[marketing-discounts-percent]] — hub.
- [[percent-discount-editor]] — form layout + sub-flows.
- [[percent-discount-targeting]] — `settings` enum + cross-validation matrix.
- [[percent-discount-validity]] — date-range / activity gates.
- [[percent-discount-stacking]] — `code_apply` + `apply_regular_price` semantics.
- [[customers-custom-groups]] — `customer_groups[]`.
- [[geo-zone]] — `geo_zone_id`.
- [[products-categories]] / [[products-vendors]] / [[products-smart-collections]] — target arrays.

## Open questions

None.
