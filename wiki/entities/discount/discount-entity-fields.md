---
type: entity
nav_path: "Entity → Discount → Fields"
aliases: ["Discount fields", "Discount attributes", "Discount columns"]
tags: [marketing, discounts, entity, fields]
created: 2026-06-10
updated: 2026-11-04
source_count: 6
---

# Discount — Fields

> Part of [[discount]]. See the hub for related aspects (lifecycle, business rules, stacking, webhooks/API).

## Identity

The verbatim **field set** carried by a Discount row. All money values are stored as integers in cents (`1000` = 10 EUR); the admin form takes euros, not cents. Validation strings shown are the exact messages surfaced to the merchant.

## Aliases

- "Discount fields" / "Discount attributes" — common merchant-facing references in support tickets.

## Key Attributes

### Identity and lifecycle

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `name` | string | Merchant-facing label used in the discounts list, reports, and analytics. Internal — not shown to customers. | Required, max 191 chars. |
| `title` | string | Customer-facing display title (when applicable — e.g., countdown banners). | Free string. |
| `description` | string | Optional customer-facing description shown at checkout. | Free string. |
| `active` | enum | `yes` / `no` — discount is evaluated only when `yes`. | `yes` / `no`. |
| `date_start` / `date_end` | date | Discount window. `date_end` null = no expiration. | The form refuses only an end date before the start, and asks for one unless No expiration is on. Past dates and today save. |
| `locale` | string | Storefront language this discount is restricted to (when set). | Optional. |

### Type and target

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum | One of `flat`, `percent`, `shipping`, `fixed`, `quantity`, `code-pro`. Container (`is_container = 1`) and Countdown (timer settings) are variants of `flat` / `percent`. See [[discount-entity-lifecycle]] for state transitions. |
| `settings` | enum | The target: `all`, `order_over`, `product`, `category`, `vendor`, `category_vendor`, `selection`, `shipping`. Tells the engine WHERE the discount applies; see [[discount-stacking-amount-by-target]]. |
| `type_value` | int | The discount amount. For `flat`: cents off (e.g., `1000` = 10 EUR). For `percent`: hundredths of a percent (e.g., `1000` = 10%), so decimals are possible. For `shipping`: must be empty (the discount IS "free shipping"). For `fixed`: the override price. |
| `order_over` | int | Minimum cart total in cents when `settings = order_over`. |
| `is_container` | bool | When `1`, the discount is a Container that takes its value from codes in the store-wide pool ([[discount-code|Container codes]]). |

### Code (coupon)

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | The literal string the customer types at checkout. Case-insensitive. Null = no code (auto-applies). Required for `code-pro` and code-based types. |
| `code_apply` | bool | When `1`, the code also applies to lines holding a product discount. When `0` (default), an Orders-over, free-shipping or Code PRO code is refused if any line holds one, and a code for every product or a specific target skips those lines. See [[discount-entity-stacking-evaluation]]. |
| `code_prefix` | bool | When `1`, treats the `code` as a barcode (works with `code_format = ean13` / `ean8`). |
| `code_format` | enum | `ean13` / `ean8` — barcode format when `code_prefix = 1`. |
| `barcode_prefix` | bool | When `1`, the entered `code` is a prefix and the barcode scanner's scan is matched as `code + scanned-value`. |
| `apply_regular_price` | bool | When `1`, the code is worked out on the regular price and compared with the current discounted price; if the code's price is lower, it replaces the product discount. See [[discount-entity-stacking-evaluation]]. |

### Usage caps

| Field | Type | Description |
|-------|------|-------------|
| `uses` | int | Count of orders that have used this discount (only orders in counted statuses). Recomputed (not auto-incremented) on every order status change — see [[discount-entity-lifecycle]]. |
| `max_uses` | int | Total uses across all customers. Null = unlimited. Discount stops firing once `uses >= max_uses`. |
| `maxused_user` | int | Per-customer cap. Null = unlimited. See [[discount-stacking-uses-counter]]. |
| `only_customer` | bool | When `1`, limits the discount to registered customers: enforced for codes at entry and for no-code Orders over and Countdown. |

### Restrictions

| Field | Type | Description |
|-------|------|-------------|
| `customer_groups[]` | array | Customer-group restriction (set of [[customer-group]] IDs). Empty = all groups. |
| `geo_zone_id` | int | Region restriction — discount applies only when the cart ships to an address inside this [[geo-zone]]. Null = global. |
| `force_save` | bool | When `1`, the discount stays attached to a previously-saved order even if admin-side edits make the cart no longer meet the conditions. The merchant's own switch, *"Save the discount on your order"*. |

### Display and visual

| Field | Type | Description |
|-------|------|-------------|
| `hide_discount_price` | bool | Hides the "was X / now Y" formatting. Not available on standard stores. |
| `msrp` | bool | (Fixed only) Shows MSRP as the "was" price. Not available on standard stores. |
| `position` | enum | (Label / Banner) where on the product card the visual marker shows: top-left / top-right / etc. |
| `timer_list` / `timer_details` | bool | (Global and Fixed forms) show the end-date timer in product listings / on the product detail page. |
| `color` / `text_color` | string | (Label / Banner / Global and Fixed forms) visual colors. |
| `discount_amount_type_in_label` | enum | What to display on a discount label: `in_percent` (-15%), `in_flat` (-10 EUR), or `dont_change` (just the label). |
| `countdown_minutes` | int | (Countdown only) timer duration. |
| `countdown_popup_effect` | enum | (Countdown only) `confetti` / `fireworks` / `school_pride` / null. |

## Where it appears

- [[marketing-discounts]] — the master list and primary CRUD screen where all of these fields are exposed.
- Per-type editors expose the relevant subset: [[marketing-discounts-flat]], [[marketing-discounts-percent]], [[marketing-discounts-shipping]], [[marketing-discounts-fixed]], [[marketing-discounts-quantity]], [[marketing-discounts-countdown]], [[marketing-discounts-code-pro]].
- [[api-discounts]] — JSON-API v2 exposes the same field set (see [[discount-entity-webhooks-api]]).

## Related

- [[discount]] — hub.
- [[discount-entity-lifecycle]] — state transitions on the `active`, `date_start`, `date_end`, `uses` fields.
- [[discount-entity-business-rules]] — validation rules + save-time normalisation that touch these fields.
- [[discount-entity-stacking-evaluation]] — how `code_apply` and `apply_regular_price` interact at checkout.
- [[discount-code]] — Container and Code PRO code rows (separate field sets).
- [[customer-group]] / [[geo-zone]] — restriction targets.

## Open Questions

None.
