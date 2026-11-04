---
type: feature
nav_path: "Marketing → Discounts → Percent → Fields"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Percent discount fields", "Percent discount validation", "Percent backend keys"]
tags: [marketing, discounts, percent, fields, validation]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, targeting, stacking, validity, plan gates, programmatic access).

# Percent discount — settings & fields

## Purpose

This page catalogues every visible field, backend key, default, and validation string on the Percent create / edit form. It is the field-reference the support Assistant cites most when answering *"why did my save fail?"* / *"what does this field do?"* questions.

## Where to find it

The fields all live on the same admin form documented in [[percent-discount-editor]] — opened via [[marketing-discounts]] → **+ Add discount** → **Global discount** card (no-code, `/admin/marketing/discounts/create/global`) or **Discount with promo code** card (`/admin/marketing/discounts/create/code`). The code-specific block (`code`, `code_format`, `code_apply`, `apply_regular_price`, `geo_zone_id`, `all_regions`) appears only on the "Discount with promo code" entry.

## What the merchant can do here

- Set `active`, `name`, `type = percent`, and `type_value` (0-100 in the UI; stored × 100).
- Pick a target via `settings` + companion arrays — see [[percent-discount-targeting]].
- Cap total uses and per-customer uses (`max_uses`, `maxused_user`): on the no-code form for `all` / `order_over`, on the code form for every target.
- Restrict to specific `customer_groups[]`; for `order_over`, require `only_customer`.
- Customise the storefront label (`color`, `text_color`, `discount_amount_type_in_label`).
- Set the validity window (`date_start`, `date_end`, `no_expire`).
- For code variants: set the `code`, barcode mode, stacking toggles, and region restriction (see fields below).

## Settings & fields

### General settings

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount status** | `active` | Active = fires at checkout. Inactive = configured but skipped. | `yes` / `no`. |
| **Discount name** | `name` | Merchant-facing label. | Required, max 191 chars. *"Name must be less than 191 characters"* / *"Name is required"*. |
| **Discount type** | `type` | Set to **Percentage** = `percent`. | In `flat,percent,shipping,fixed,quantity`. *"Type must be one of: flat, percent, shipping, quantity"*. |
| **Discount value** | `type_value` | The percentage as a **whole number, 0-100** — type `15` for 15% (**not** `0.15`). The form shows the whole percent; it is stored as `percent × 100` (e.g., 15% → 1500). | Required when type=percent. Max **100%** (10000 stored) in the admin form. Min must be > 0: *"The rate must be at least {min}"* fires when value ≤ 0. |

### Discount target

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Discount target** | `settings` | One of `all`, `order_over`, `product`, `product_category`, `product_vendor`, `selection`, `category_vendor`. | *"Settings must be one of: all, order_over, product, product_category, product_vendor, selection, category_vendor"*. See [[percent-discount-targeting]]. |
| **Order amount threshold** | `order_over` | Cart-subtotal threshold for `order_over` target. | Required if settings=order_over; no maximum. *"Order over is required if settings is order over"*. |
| **Save the discount on your order** | `force_save` | When ON, the discount stays attached to a previously-saved order even when admin-side edits drop the cart below the threshold. | 1 / 0. Only shown for `order_over`. |
| **Products** | `products[]` | Product IDs to attach. | Required if settings=product. *"Products is required if settings is product"*. |
| **Product categories** | `product_categories[]` | Category IDs (see [[products-categories]]). | Required if settings=product_category; used with vendors for category_vendor. *"Product categories is required if settings is product category"*. |
| **Product vendors** | `vendors[]` | Vendor IDs (see [[products-vendors]]). | Required if settings=product_vendor; used with categories for category_vendor. *"Vendors is required if settings is product vendor"*. |
| **Smart collections** | `selections[]` | Smart-collection IDs (see [[products-smart-collections]]). | Required if settings=selection. *"Selections is required if settings is selection"*. |

### Discount limits

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Global discount limit** | `max_uses` | Total uses across all customers. NULL = unlimited. | Integer up to 100,000. *"Max uses must be less than 100000"*. No-code form: shown only for `all` and `order_over`; code form: every target. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap for logged-in customers, on codes at entry and on no-code `order_over`. NULL = unlimited. | Integer up to 100,000. *"Max used user must be less than 100000"*. |
| **Unlimited** | (toggle) | Sets the corresponding limit to NULL. | — |

### Customer groups & registered users

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **All groups** | `customer_groups_target` | When ON, applies to every [[customers-custom-groups]]. | `yes` / `no`. |
| **Customer groups** | `customer_groups[]` | When `customer_groups_target=no`, list of group IDs. | Array. |
| **Discount available only to registered users** | `only_customer` | Guests cannot apply. | 1 / 0. Only shown for `order_over` target. |
| **Customers** | `customers[]` | Specific customers who may get a no-code `order_over` discount. | Array of customer IDs. Shown when `only_customer` is on. |

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
| **End date** | `date_end` | Last day. Skipped after this date. | Asked for unless **No expiration** is on (*"The end date is required"*). The form refuses only an end date before the start (*"The end date must be after the start date"*). Today and past dates save. See [[percent-discount-validity]]. |
| **No expiration** | `no_expire` | When ON, sets `date_end` to null. | — |

### Code-specific fields (when `code` is set)

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Promo code** | `code` | The literal code typed at checkout. Case-insensitive. | Required for code-based; max 20 chars; alphanumeric / `.` / `#`; unique across all discounts, checked on create. *"Code must be unique"*. |
| **Code format (barcode)** | `code_format` | `ean13` or `ean8` if the code is a barcode. | In `ean13`, `ean8`. |
| **Barcode prefix mode** | `barcode_prefix` | When ON, scanned value is matched as `code + scanned-suffix`. | 1 / 0. |
| **The discount is applied even when the cart contains discounted products** | `code_apply` | Allows stacking on already-discounted items. | 1 / 0. Defaults OFF. See [[percent-discount-stacking]]. |
| **Apply to the regular price of products, if this discount is greater** | `apply_regular_price` | When ON, the code is worked out on the regular price and replaces the product discount if that price is lower; otherwise the line keeps the product discount and no code. | 1 / 0. Only shown when `code_apply=1`. |
| **Region (Geo zone)** | `geo_zone_id` | Restrict to a specific [[geo-zone]]. | Nullable. |
| **Make it Global** | `all_regions` | When ON, no region restriction. | `yes` / `no`. |

## Business rules

- **`type_value` is the whole percent in the UI, stored as percent × 100** — the merchant types `15` for 15% (**not** the decimal `0.15`); the edit form shows `15` and the stored value is `1500`. The admin form limits it to 100% and requires more than 0. **Via the API this differs**: `createDiscount` / JSON-API v2 store `type_value` exactly as sent (the ×100 is client-side in the form), so programmatically you send the **raw `1500`** for 15%, and neither API limits a percent to 100 — see [[percent-discount-programmatic-access]].

## Related

- [[marketing-discounts-percent]] — hub.
- [[percent-discount-editor]] — form layout + sub-flows.
- [[percent-discount-targeting]] — `settings` enum.
- [[percent-discount-validity]] — date-range / activity gates.
- [[percent-discount-stacking]] — `code_apply` + `apply_regular_price` semantics.
- [[customers-custom-groups]] — `customer_groups[]`.
- [[geo-zone]] — `geo_zone_id`.
- [[products-categories]] / [[products-vendors]] / [[products-smart-collections]] — target arrays.

## Open questions

None.
