---
type: api-resource
resource_path: /api/v2/discounts
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount
related_features: [marketing-discounts, marketing-discounts-flat, marketing-discounts-percent, marketing-discounts-shipping]
aliases: ["Discounts API attributes", "discounts target object", "discounts attribute reference", "/discounts attributes"]
tags: [api, json-api-v2, discounts]
plan_gates: ["discount_global", "discount_coupon", "discount_fixed", "discount-code-pro"]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Discounts API — attributes & target object

> Part of [[api-discounts]]. See the hub for the other aspects (types & validation, side effects, examples).

## Purpose

This aspect is the **attribute reference** for the `discounts` resource: every writable / read-only field on the parent promotion record, plus the polymorphic `target` object that scopes a discount to specific products / categories / vendors / collections. For which fields are required per discount type and the mutually-exclusive validation rules, see [[api-discounts-types]]. For worked request / response shapes, see [[api-discounts-examples]].

## Endpoint

- **URL base:** `<store-host>/api/v2/discounts/`
- **Methods covered here:** `GET` (collection), `GET /{id}`, `POST`, `PATCH /{id}`, `DELETE /{id}`.

Base URL, auth, headers: see [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes / validation |
|---|---|---|---|---|---|
| `name` | string | yes | yes | POST yes / PATCH `sometimes` | `min:2, max:191`. Merchant-facing label; not shown to customers. |
| `discount_type` | enum | yes | yes (`sometimes`) | POST yes | One of `flat`, `percent`, `shipping`, `fixed`, `code-pro`. Other DB-enum values (`quantity`, `countdown`, `volume`, `leasing`, `banner`, `label`) are rejected by the validator — those types are admin-panel-only. Stored internally as the model's `type` column; renamed `discount_type` on the wire. See [[api-discounts-types]]. |
| `date_start` | date `Y-m-d` | yes | yes (`sometimes`) | POST yes | When the discount window opens. |
| `date_end` | date `Y-m-d` | yes | yes | no | When the window closes. NULL = no expiration. |
| `type_value` | int | yes | yes | required when `discount_type` is `percent` OR `flat` | For `flat`: amount in cents (e.g., `1000` = 10.00). For `percent`: whole percent `0`–`100`. For `shipping`: leave empty (the discount IS free shipping). For `fixed` and `code-pro`: leave empty (per-variant prices live on [[api-product-to-discount]]; per-code terms live on [[api-discount-codes-pro]]). |
| `order_over` | int | yes | yes (`sometimes`) | required when `target.type = order_over` | Minimum cart total in cents for the discount to fire. |
| `max_uses` | int | yes | yes (`sometimes`) | no | Total redemptions cap across all customers. NULL = unlimited. Once `uses >= max_uses` the discount stops applying. |
| `code` | string | yes | yes | no | Coupon string the customer types at checkout. `alpha_num`, `max:20`, **unique on `discounts.code` platform-wide** (one namespace across every merchant). Stored case-insensitively. **Cannot be set when `discount_type` is `fixed` OR `code-pro`** — those types use companion resources for their codes (see [[api-discounts-types]]). |
| `code_apply` | enum `1` / `0` | yes | yes (`sometimes`) | no | Stacking flag on code-based discounts. `1` = code applies even when the cart already has another discount on lines. `0` (default) = code is REJECTED if any line already carries a discount. See [[discount-stacking]] for the full rule + the shipping-coupon + `order_over` carve-out that always applies regardless. |
| `active` | enum `yes` / `no` | yes | yes | no | Live on the storefront. Flipping is throttled in the admin panel to once per 10 minutes per discount to prevent thrashing the per-product attachment regeneration — verify whether the same cooldown applies on JSON-API v2 writes. |
| `timer_list` | enum `1` / `0` | yes | yes (`sometimes`) | no | Render the countdown timer on category / listing pages. |
| `timer_details` | enum `1` / `0` | yes | yes (`sometimes`) | no | Render the countdown timer on product-detail pages. |
| `is_container` | enum `1` / `0` | yes | yes (`sometimes`) | no | Only valid with `discount_type = percent`. Marks the parent as a Container that hosts many bulk-generated single-use codes (see [[marketing-discounts-codes]] and [[api-discount-codes]]). |
| `discount_amount_type_in_label` | enum | yes | yes (`sometimes`) | no | One of `dont_change`, `in_flat`, `in_percent`. How the discount amount renders in storefront price labels. |
| `target` | object | yes | yes | required when `discount_type` is `flat`, `percent`, OR `shipping` | Polymorphic target descriptor — see Target object below. Ignored for `fixed` and `code-pro`. |
| `uses` | int | **read-only** | **read-only** | — | Running redemption counter. **Recomputed (not incremented)** on every related order's status change via a 10-second-delayed job. Cancelled / refunded orders automatically free the slot back up — see [[api-discounts-side-effects]]. |
| `settings` | string | **read-only** | **read-only** | — | Internal target-type column written by the adapter from the `target.type` you sent. Returned on GET; not directly writable. |
| `created_at`, `updated_at` | timestamp | **read-only** | **read-only** | — | Standard timestamps. |

### Target object

The `target` object is required for `flat`, `percent`, and `shipping` discounts. Each target type validates the referenced IDs exist BEFORE the discount is created — invalid IDs return 422 with the corresponding `target.products` / `target.categories` / etc. pointer (see [[api-discounts-types]]).

| `target.type` | Additional required keys | Effect |
|---|---|---|
| `all` | — | Cart-wide / whole-order. |
| `product` | `target.products[]` (product IDs) | These specific products. |
| `category` | `target.categories[]` (category IDs) | Products in these categories. |
| `vendor` | `target.vendors[]` (vendor IDs) | Products from these vendors. |
| `category_vendor` | `target.categories[]` + `target.vendors[]` | Products matching BOTH a category AND a vendor. |
| `selection` | `target.selections[]` (Smart Collection IDs — see [[products-smart-collections]]) | Products in these merchant-curated selections. |
| `order_over` | (uses top-level `order_over`) | Whole order when cart total ≥ threshold. |

A `fixed` discount IGNORES `target` entirely (per-variant overrides live on [[api-product-to-discount]]), so sending a `target` block on a `fixed` parent does not error — it is silently dropped at save time.

## Relationships

This resource declares **no JSON-API relationships**. The companion resources that link back to a Discount each have their own top-level endpoint:

- [[api-discount-codes]] — Container child codes (a percent Discount with `is_container = 1` hosts these).
- [[api-discount-codes-pro]] — Code PRO codes (each links to a `code-pro` parent via the `discount` relationship on that resource).
- [[api-product-to-discount]] — per-variant Fixed-price overrides (each links to a `fixed` parent via the `discount` relationship on that resource).

Because there are no schema relationships, `?include=` is not usable on this resource — to fetch child codes / per-product overrides, call the companion endpoints directly.

## Filtering & sorting

This aspect documents attributes only. For the full filter / sort / include reference and worked queries, see [[api-discounts-side-effects]].

## Side effects

Writing attributes here triggers webhooks, attachment regeneration, listing-engine re-index, and a `uses` recompute on related order status changes. Full catalogue: see [[api-discounts-side-effects]].

## Equivalent UI

- [[marketing-discounts]] — admin-panel master discount list (mirrors these attributes across the per-type edit screens).
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] — per-type edit screens.
- [[discount]] — entity attribute reference.

## Related

- [[api-discounts]] — hub.
- [[json-api-v2]] — API hub.
- [[api-discounts-types]] — required fields per type + mutually-exclusive validation.
- [[api-product-to-discount]] — per-variant Fixed-price overrides (`target` ignored on `fixed`).
- [[discount]] — full Discount entity reference.
- [[discount-stacking]] — `code_apply` stacking rule + `uses` recompute.
- [[products-smart-collections]] — target type `selection`.

## Open questions

- Verify whether the `target` polymorphic descriptor is reflected verbatim in the GET response or whether reads only expose the internal `settings` column (forcing integrators to reconstruct the target shape from `settings` + the related products / categories tables).
- Confirm whether the `force_save` and `apply_regular_price` columns are writable through this endpoint — neither appears in the validator rules block, so they would silently be ignored on POST/PATCH today. `(verify)`
