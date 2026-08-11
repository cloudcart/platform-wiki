---
type: feature
nav_path: "Apps → OLX → Products → Validation"
route_name: apps.olx.products
route_path: /admin/apps/olx/products
aliases: ["OLX product validation", "OLX publish requirements", "OLX Add-advert autocomplete filter"]
tags: [apps, olx, marketplace, products, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX → Products — validation & eligibility

> Part of [[apps-olx-products]]. See the hub for the other aspects (pipeline UI, sync, payload formatting).

## Purpose

This aspect covers **what makes a product eligible to publish to OLX**: the pre-publish validation rules, the per-product OLX state fields, the autocomplete pre-filter that hides ineligible products from the picker, the missing-price error that aborts a publish mid-flight, and how all failures surface in [[apps-olx-history]].

## Where to find it

The **Valid** column on the Products tab (`/admin/apps/olx/products`) shows each product's validation result (checkmark / X). The **+ Add advert** picker (see [[apps-olx-products-pipeline]]) only lists products that already clear the autocomplete pre-filter below.

## What the merchant can do here

- See per-product validation status in the **Valid** column.
- Add a product even when it fails validation — it lands in the pipeline but the **Valid** column shows X and publish stays blocked until fixed.
- Drill into [[apps-olx-history]] to read the exact field-level OLX error after a failed publish.

## Settings & fields

### Per-product OLX state

| Field | Notes |
|---|---|
| **CloudCart product ID** | Source product. |
| **OLX advert ID** | Returned by OLX after a successful publish. |
| **External ID** | OLX-side identifier. |
| **Status** | Pending / Created / Rejected / Expired. |
| **Created date** | First publish date. |
| **Validation errors** | When OLX rejected the product, the reasons. |

### Validation rules (pre-publish)

Before submitting to OLX, CloudCart checks that the product:

- Has a mapped CloudCart category ([[apps-olx-configuration]]).
- Has all required parameters for the OLX category mapped ([[apps-olx-parameters]]).
- Has all parameter values mapped ([[apps-olx-parameters-values]]).
- Has at least one image (meeting OLX size / format requirements).
- Has title length / description length within OLX limits.

Failed validation → the product can be added but the **Valid** column shows X; publish is blocked until the issue is fixed.

## Business rules

### Add-advert autocomplete excludes ineligible products

The picker autocomplete query only surfaces products with `price_to > 0`, `image_id > 0`, AND a matching category mapping (`@app_olx_category_map.site_category = products.category_id`) AND no existing OLX advert (`whereDoesntHave('olxProduct')`). So a product without a price or main image is **impossible to select** — it is pre-filtered out of the dropdown rather than failing later. Already-published products are also hidden, so the same product can't be queued twice.

### Missing price throws an error mid-publish

If a product somehow reaches publish with no price (regular or discounted), the payload formatter throws an `Error` with `__('olx.err.missing_price')`. The exception is caught by the outer upload loop and saved to [[apps-olx-history]]. The merchant has to set a price before retrying. (Price source + promo precedence is on [[apps-olx-products-formatting]].)

### Validation errors are saved to History on failure

When publishing an advert throws, a History row is created with `type=0`, the `product_id`, and the parsed `error_message`. The merchant sees the exact field-level OLX error (e.g., *"title - too short"*, *"category_id - required"*) in the History tab and on the failed product row. When OLX returns a 400/401/403/404/406/429/500, the parsed per-field validation message is stored with the product ID and image.

### The merchant cannot override an OLX rejection

If OLX rejects an advert, there is no force-publish — the underlying CloudCart data (category mapping, parameter, image, title) must be corrected and the product re-published. See [[apps-olx-products-sync]] for the re-publish / re-sync actions.

### Permission

Standard apps permission scope.

## Related

- [[apps-olx-products]] — hub.
- [[apps-olx]] — OLX feature hub.
- [[apps-olx-configuration]] — category mapping (validation prerequisite).
- [[apps-olx-parameters]] — parameter mapping (validation prerequisite).
- [[apps-olx-parameters-values]] — value mapping (validation prerequisite).
- [[apps-olx-history]] — where validation / rejection errors surface.
- [[products-products]] — source CloudCart products (price + image live here).

## Open questions

- Exact OLX title / description length limits per category (title is capped at 70 — see [[apps-olx-products-formatting]]; description limit not yet verified).
