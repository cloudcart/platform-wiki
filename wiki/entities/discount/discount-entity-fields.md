---
type: entity
nav_path: "Entity → Discount → Fields"
aliases: ["Discount fields", "Discount attributes", "Discount columns"]
tags: [marketing, discounts, entity, fields]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

# Discount — Fields

> Part of [[discount]]. See the hub for related aspects (lifecycle, business rules, stacking, webhooks/API).

## Identity

The verbatim **field set** carried by a Discount row. All money values are stored as integers in cents (`1000` = 10 BGN). Validation strings shown are the exact messages surfaced to the merchant.

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
| `date_start` / `date_end` | date | Discount window. `date_end` null = no expiration. | Start required; end nullable. End cannot be on or before start. |
| `locale` | string | Storefront language this discount is restricted to (when set). | Optional. |

### Type and target

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum | One of 7 types: `flat`, `percent`, `shipping`, `fixed`, `quantity`, `countdown`, `code-pro`. (Plus the Container variant: `is_container = 1` on a `flat` / `percent`.) See [[discount-entity-lifecycle]] for state transitions. |
| `settings` | enum | The target: `all`, `order_over`, `product`, `category`, `vendor`, `category_vendor`, `selection`, `shipping`. Tells the engine WHERE the discount applies. |
| `type_value` | int | The discount amount. For `flat`: cents off (e.g., `1000` = 10 BGN). For `percent`: whole-number % (0-100). For `shipping`: must be empty (the discount IS "free shipping"). For `fixed`: the override price. |
| `order_over` | int | Minimum cart total in cents when `settings = order_over`. |
| `is_container` | bool | When `1`, the discount is a Container holding many auto-generated child [[discount-code|DiscountCode]] codes. |
| `discount_id` | int | Parent discount ID for `code-pro` and Container children — null for top-level discounts. |

### Code (coupon)

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | The literal string the customer types at checkout. Case-insensitive. Null = no code (auto-applies). Required for `code-pro` and code-based types. |
| `code_apply` | bool | When `1`, the code can stack on top of items that already have a per-product discount. When `0` (default), the code is REJECTED if any line already has a discount. See [[discount-entity-stacking-evaluation]]. |
| `code_prefix` | bool | When `1`, treats the `code` as a barcode (works with `code_format = ean13` / `ean8`). |
| `code_format` | enum | `ean13` / `ean8` — barcode format when `code_prefix = 1`. |
| `barcode_prefix` | bool | When `1`, the entered `code` is a prefix and the barcode scanner's scan is matched as `code + scanned-value`. |
| `apply_regular_price` | bool | When `1`, the code re-evaluates against the original catalog price (ignoring already-applied per-product Fixed discounts) if that yields a larger discount. See [[discount-entity-stacking-evaluation]] for the max-of-two filter. |

### Usage caps

| Field | Type | Description |
|-------|------|-------------|
| `uses` | int | Count of orders that have used this discount (only orders in counted statuses). Recomputed (not auto-incremented) on every order status change — see [[discount-entity-lifecycle]]. |
| `max_uses` | int | Total uses across all customers. Null = unlimited. Discount stops firing once `uses >= max_uses`. |
| `maxused_user` | int | Per-customer cap (e.g., one redemption per customer). Null = unlimited. |
| `only_customer` | bool | When `1`, only registered customers can use it (guests blocked). |

### Restrictions

| Field | Type | Description |
|-------|------|-------------|
| `customer_groups[]` | array | Customer-group restriction (set of [[customer-group]] IDs). Empty = all groups. |
| `geo_zone_id` | int | Region restriction — discount applies only when the cart ships to an address inside this [[geo-zone]]. Null = global. |
| `force_save` | bool | When `1`, the discount stays attached to a previously-saved order even if admin-side edits make the cart no longer meet the conditions. Required for `shipping` and `order_over` discounts. |

### Display and visual

| Field | Type | Description |
|-------|------|-------------|
| `hide_discount_price` | bool | Hides the "was X / now Y" struck-through formatting — shows only the discounted price. |
| `msrp` | bool | (Fixed only) When `1`, the catalog price acts as MSRP; the discount price is the "now" price. Cleared by save-time normalisation on any non-`fixed` type — see [[discount-entity-business-rules]]. |
| `position` | enum | (Label / Banner) where on the product card the visual marker shows: top-left / top-right / etc. |
| `timer_list` / `timer_details` | bool | (Countdown only) show the countdown timer in product listings / on the product detail page. |
| `color` / `text_color` | string | (Label / Banner / Countdown) visual colors. |
| `discount_amount_type_in_label` | enum | What to display on a discount label: `in_percent` (-15%), `in_flat` (-10 BGN), or `dont_change` (just the label). |
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
- [[discount-code]] — Container child code row (separate field set).
- [[customer-group]] / [[geo-zone]] — restriction targets.

## Open Questions

None.
