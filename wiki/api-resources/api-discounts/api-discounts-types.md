---
type: api-resource
resource_path: /api/v2/discounts
http_methods: [POST, PATCH]
related_entity: discount
related_features: [marketing-discounts, marketing-discounts-flat, marketing-discounts-percent, marketing-discounts-shipping, marketing-discounts-fixed, marketing-discounts-code-pro]
aliases: ["Discounts API types", "discount_type validation", "discounts plan-feature gating", "discounts 422 errors"]
tags: [api, json-api-v2, discounts]
plan_gates: ["discount_global", "discount_coupon", "discount_fixed", "discount-code-pro"]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Discounts API — types, validation & plan gating

> Part of [[api-discounts]]. See the hub for the other aspects (attributes & target object, side effects, examples).

## Purpose

This aspect covers the **five accepted `discount_type` values**, the type-specific required fields, the mutually-exclusive validation rules enforced at create + update, the plan-feature gate (and why it returns HTTP 402 rather than 403), and the common 422 error shapes. For the full attribute table and the `target` object, see [[api-discounts-attributes]].

## Endpoint

- **URL base:** `<store-host>/api/v2/discounts/`
- **Methods covered here:** `POST` (create-time validation + gating), `PATCH /{id}` (update-time validation; PATCH is NOT plan-gated).

Base URL, auth, headers: see [[json-api-v2]].

## Attributes

The accepted `discount_type` values and their type-specific required fields:

| `discount_type` | Required fields | Notes |
|---|---|---|
| `flat` | `type_value` (cents), `target` | Flat amount off; `type_value` is the amount in cents. |
| `percent` | `type_value` (`0`–`100`), `target` | Percentage off; can be a Container parent (`is_container = 1`). |
| `shipping` | `target` | Free-shipping discount; `type_value` left empty. |
| `fixed` | — | Per-variant override parent; prices via [[api-product-to-discount]]. `target` and `code` rejected/ignored. |
| `code-pro` | — | Per-code campaign parent; child codes via [[api-discount-codes-pro]]. `code` rejected. |

The DB enum also contains `quantity`, `countdown`, `volume`, `leasing`, `banner`, `label`, but the JSON-API validator's accept-list excludes them — POSTing any of those returns 422 *"Invalid discount type. List of valid discount types: flat, percent, shipping, fixed, code-pro"*. Those types are admin-panel-only.

## Relationships

This resource declares no JSON-API relationships; the type drives which **companion resource** holds the children: `fixed` → [[api-product-to-discount]], `code-pro` → [[api-discount-codes-pro]], percent-with-`is_container` → [[api-discount-codes]]. See [[api-discounts-attributes]].

## Filtering & sorting

Not applicable to this aspect (validation / gating only). For the filter / sort reference, see [[api-discounts-side-effects]].

## Side effects

### Mutually-exclusive validation (enforced at create + update)

- `discount_type = fixed` with `code` set → 422 *"Cannot use discount code when discount type is fixed."*
- `discount_type = code-pro` with `code` set → 422 *"Cannot use discount code when discount type is code-pro. Codes are managed via the discount-codes-pro resource."*
- `is_container = 1` with any `discount_type` other than `percent` → 422 *"The is_container field can be used only with discount_type percent."*
- `discount_type` outside the validator's accept-list → 422 *"Invalid discount type. List of valid discount types: flat, percent, shipping, fixed, code-pro"*.
- `target.type` outside its accept-list → 422 *"Invalid target type. List of valid target types: all, product, category, vendor, category_vendor, selection, order_over"*.
- `type_value` missing on `percent` / `flat` → 422 *"The type value field is required when discount type is percent."* (or `flat`).
- `order_over` missing when `target.type = order_over` → 422 *"The order over field is required when target.type is order_over."*

The code-on-non-allowed-type rule rejects ONLY `fixed` / `code-pro`; `flat` / `percent` / `shipping` accept a `code`.

### Plan-feature gating (CREATE time only)

The adapter runs a plan-feature gate at CREATE time only (PATCH is not gated). The selected counter depends on the type and whether a `code` is set:

| `discount_type` + `code` | Counter consumed |
|---|---|
| `fixed` | `discount_fixed` |
| `code-pro` | `discount_coupon` (and the `discount-code-pro` plan-feature must be ON for the type to be reachable from the admin UI) |
| Any other type WITH a non-null `code` | `discount_coupon` |
| Any other type WITH no `code` | `discount_global` |

When the counter is over cap, the api2 exception handler returns **HTTP 402 Payment Required** with a `detail` echoing the plan-feature mapping string — **not** HTTP 403 (despite older wiki phrasing claiming 403, the handler explicitly returns 402, the same status used for plan-expired). HTTP 403 is not emitted by this resource at all.

## Equivalent UI

- [[marketing-discounts]] — admin-panel type picker (mirrors the `discount_type` accept-list).
- [[marketing-discounts-fixed]] — Fixed parent edit (`discount_type = fixed`).
- [[marketing-discounts-code-pro]] — Code PRO parent edit (`discount_type = code-pro`).
- [[discount]] — entity attribute reference.

## Related

- [[api-discounts]] — hub.
- [[json-api-v2]] — API hub: status-code conventions (402 vs 403).
- [[api-discounts-attributes]] — full attribute table + `target` object.
- [[api-product-to-discount]] — `fixed` child overrides.
- [[api-discount-codes-pro]] — `code-pro` child codes.
- [[api-discount-codes]] — Container child codes (`is_container = 1` percent parent).
- [[plan-gates]] — `discount_global` / `discount_coupon` / `discount_fixed` / `discount-code-pro` counters.
- [[discount-stacking]] — downstream stacking rules per type.

## Open questions

- Confirm `quantity` / `countdown` are strictly admin-panel-only — the validator's accept-list excludes them, so POSTing those types returns 422. Document whether a future migration would lift this restriction.
