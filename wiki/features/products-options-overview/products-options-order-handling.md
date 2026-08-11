---
type: feature
nav_path: "Products → Options → order-line behaviour"
route_name: apps.product_options.edit.new
route_path: /admin/products/options-new/:type/:id?
aliases: ["Product option order handling", "Option values on order line", "Required option checkout", "Option file uploads", "Опции в поръчка"]
tags: [apps, products, options, orders, customisation]
plan_gates: ["product_options"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-options-overview]]. See the hub for the other aspects (types, pricing, assignment).

# Product Options — order-line behaviour

## Purpose

Explains what happens to a customer's option selections **after** they add the product to the cart: where the values are stored, how Required options gate checkout, what happens to uploaded files when the option is later deleted, how uninstalling the app behaves, and how the same rules apply through JSON-API v2.

## Where to find it

The customer fills options on the storefront product page. The merchant reads the submitted values on the order details screen ([[orders-details]]) when fulfilling. There is no separate admin screen for this behaviour — it is the runtime side of the options configured under Sidebar → Products → **Options**.

## What the merchant can do here

- Read each customer's option values (text, picked value, uploaded file) on the order's line items.
- Download customer-uploaded files for fulfilment.
- Rely on Required options to block checkout until filled.

## Settings & fields

There are no merchant-editable fields on this runtime path — the behaviour is driven by the option's own configuration (its [[products-options-types|type]], [[products-options-pricing|price impact]], required flag, and [[products-options-assignment|assignment scope]]). The merchant-visible surfaces are the storefront product page (input) and the order details line items (output).

## Business rules

### Customer values stored on the order line

When the customer submits an option (e.g. engraving text), the value is stored on the **order line item** — not on the product record and not on the customer record. Each order can carry different option values for the same product. The merchant sees the values on the order details screen during fulfilment.

For non-file option types, the value (text, selected value, etc.) is stored independently of the original option, so deleting the option later does NOT remove the historical order data.

### File uploads — special handling + irreversible cascade

When the customer uploads via a file-type option, the file is stored as a regular cart-item upload (allowed mime types jpg / jpeg / png / bmp / webp). The merchant downloads it from the order details for fulfilment.

**Deleting the file-type option in the admin ALSO deletes every file upload from past orders associated with that option** — the cascade is intentional (the file is meaningless without the option context) but **irreversible**. Merchants should keep file-type options around until every order that used them is fulfilled.

### Required option blocks checkout (not the product page)

Marking an option Required blocks the customer from advancing to the cart with that product UNTIL the option is filled. The validation fires when the customer clicks **Add to cart**; the storefront product page shows the option as required visually (asterisk / label) and the add-to-cart form is blocked. Useful for must-pick-a-font mandatory flows.

### Options never touch stock

A customer's option choice never decrements or splits inventory — the product keeps its single stock count regardless of the option value. Stock lives on the Variant; see [[inventory-variant-model]]. This is the core difference from variants ([[products-variants-options]]).

### Uninstall behaviour

When the `product_options` app is uninstalled, option records and per-product assignments **remain in the database** (so they reappear on reinstall) but the storefront stops rendering them on product pages. JSON-API v2 read access for options is disabled for the duration of the uninstall.

### JSON-API v2 parity

The option data is also readable / writable via **JSON-API v2** — see [[api-product-options]]. The endpoint is **app-gated**: available only when `product_options` is installed, otherwise calls return 404. A POST / PATCH / DELETE through the API enforces the **same** validations as the admin form (name / storefront-name ≤ 191 chars, type one of the 10 supported, mapping one of product / category / vendor / selection, at least one value for select / radio / checkbox) and the **same** side effects — including auto-setting `per_item = 1` for length / weight / square and the irreversible file-upload cascade on delete. See [[json-api-v2]] for the side-effects principle.

## Related

- [[products-options-overview]] — hub.
- [[products-options-types]] — file type + the value the customer submits.
- [[orders-details]] — where the merchant reads submitted option values.
- [[orders]] — orders carry option values on their lines.
- [[api-product-options]] — JSON-API v2 endpoint (same validations + cascade).
- [[json-api-v2]] — API side-effects principle.
- [[inventory-variant-model]] — why options never split stock.
- [[products-variants-options]] — DISTINCT concept (stock-determining choices).

## Open questions

None.
