---
type: feature
nav_path: "Payment Providers → Iute → Schemes"
route_name: apps.iute.schemes
route_path: /admin/payment-providers/iute/schemes
aliases: ["Iute Schemes", "Iute product mappings", "Iute loan products", "Схеми Iute", "Иуте схеми"]
tags: [paymentproviders, payment-providers, iute, bnpl, schemes]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Schemes

## Purpose

The Schemes tab for Iute is the merchant's view into Iute's **product mappings** — each row binds one CloudCart product (by SKU = the CloudCart product ID) to one Iute "loan product" ID (typically representing a specific months / rate combination Iute defines on their side). When the customer has that product in their cart, Iute's calculation API returns the loan terms attached to the mapped loan product. Without a mapping, Iute applies its default catalog terms to the product (or hides it if the product isn't in their default catalog).

The mapping list lives entirely on Iute's servers, accessed via Iute's admin API (`/api/v1/eshop/management/product-mapping`). The merchant manages it through this CloudCart screen — Add, Delete, Export to Excel, Import from Excel.

## Where to find it

Sidebar → **Payment Providers** → **Iute** → **Schemes** tab.

The route is `/admin/payment-providers/iute/schemes`. The page renders a `data-table` of product mappings paginated by Iute's API. Backend endpoints proxy through `/admin/api/payment_providers/iute/`.

## What the merchant can do here

- See the full paginated list of CloudCart products mapped to Iute loan products. Each row shows:
  - Product name + image (resolved from the CloudCart catalog via SKU).
  - The Iute loan-product name.
  - **Red "Not Found"** if the SKU on Iute's side doesn't correspond to a current CloudCart product (the merchant likely deleted it).
- Click **Add Schema** to add new mappings — pick an Iute loan product, multi-select CloudCart products to bind to it.
- Click delete on a row, or select multiple via the bulk checkbox and click **Delete** to remove mappings.
- **Export** all mappings to an Excel file via the **Export** button.
- **Import** mappings in bulk from an Excel file via the **Import** button (file picker → CloudCart calls `IuteImport`).

## Settings & fields

### The Add Scheme modal

Clicking **Add Schema** opens a right-side slide-out modal at size `lg`. Header has **Cancel** + **Save** buttons (Save disabled while products are loading or a submit is in flight). On open, the modal calls `GET /admin/api/payment_providers/iute/products` to fetch the list of Iute loan products and shows a loading spinner until that returns. The body has a single card with two fields:

| Field | What it does | Validation / notes |
|-------|--------------|--------------------|
| **Select Scheme** (single-select dropdown) | The Iute loan product ID this mapping binds to. Options are loaded from `GET /admin/api/payment_providers/iute/products` — only loan products Iute has defined for the merchant appear. | Required. Field-level error binds to `schemeId`. |
| **Discount target - Product/s** (multi-select tag picker, AJAX search) | Multi-select tag picker searching CloudCart's catalog via `/admin/api/core/products/search`. Each picked product becomes one mapping row on Iute (productId = scheme ID; sku = CloudCart product ID). | Required (array). Field-level error binds to `products`. |

On Save, the modal POSTs `{ schemeId, products: [...] }` to `/admin/api/payment_providers/iute/schemes` (which the Iute backend translates into multiple `(productId, sku)` rows posted to Iute's `/api/v2/eshop/management/product-mapping?batch=true`). On success the modal closes and re-fetches the parent table; field-level errors from Iute (e.g., "scheme not active", duplicate sku) surface as inline errors on the matching input.

### Mapping row fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Iute loan product** (modal label: *Select Scheme*) | The Iute loan product ID this mapping binds to. Comes from Iute's `getLoanProducts` API. | None | Required. Dropdown of all loan products defined for the merchant on Iute. |
| **Products** (modal label: *Discount target - Product/s*) | Multi-select of CloudCart products to bind to this loan product. | None | Required, array. Each picked product becomes one mapping row on Iute (productId = scheme ID; sku = CloudCart product ID). |

## Business rules

### Mappings are stored on Iute's servers

This screen is NOT a CloudCart DB table — it's a proxy view over Iute's `product-mapping` admin API. CRUD goes:

- `GET /admin/api/payment_providers/iute/schemes` → Iute's `/api/v1/eshop/management/product-mapping`.
- `POST /admin/api/payment_providers/iute/schemes` → Iute's `/api/v2/eshop/management/product-mapping?batch=true` with one row per (loan_product_id, sku) pair.
- `DELETE /admin/api/payment_providers/iute/schemes` → Iute's `DELETE /api/v1/eshop/management/product-mapping?batch=true`.

Network or authentication errors from Iute surface as validation errors with the response body attached.

### "Not Found" SKUs

When CloudCart fetches the mapping list and joins it back to the local product catalog, if a SKU stored on Iute doesn't match any CloudCart product, the row's `name` is set to `<span style="color: red">Not Found</span>` and `img` / `url` are null. The merchant typically gets these after deleting a product from CloudCart but not from Iute — the recommended fix is to delete the orphan mapping via this screen.

### Bulk import / export

Export downloads an Excel file with one row per mapping, columns including the Iute loan product ID and the CloudCart product SKU. Import accepts the same shape and upserts mappings into Iute via the same `product-mapping?batch=true` endpoint.

### Loan products vs schemes

In this UI the term **"scheme"** is used interchangeably with **Iute loan product** — an Iute loan product is a specific (months, monthly rate, terms) combination the merchant agreed with Iute. The product's name typically encodes the months (e.g., "6 months 0%", "12 months 9% APR"). The merchant does NOT create loan products from CloudCart — those are defined on Iute's side; CloudCart only manages which CloudCart products bind to which loan product.

### Compound row ID

The `id` field on each row is constructed as `{productId}|{sku}` (loan-product-id pipe SKU) so the merchant can multi-select rows for bulk delete and the controller can split them back out.

### Plan-gating

Inherits the parent provider's gating — none beyond a valid Iute admin API key.

### Permissions / endpoints

- `GET schemes` — paginated list.
- `POST schemes` — create mappings.
- `DELETE schemes` — bulk delete mappings.
- `GET products` — list available Iute loan products for the Add dialog.
- `GET export` — Excel download.
- `POST import` — Excel upload.

## Related

- [[payment-providers-iute]] — parent hub for Iute.
- [[payment-providers-iute-settings]] — country, mode, API keys, promo-button switch.
- [[payment-providers-dsk-bnpl-promotions]] — DSK BNPL has a similar "per-product mapping to bank-side loan IDs" pattern but maps to DSK Bank's promotion IDs.
- [[product]] — CloudCart products being mapped.
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

- ⏸️ Whether Iute filters the loan-products list server-side to "active periods only" — Iute-side decision, not encoded in CloudCart. The Add-mapping dialog shows whatever Iute returns.

## Verified — "delete all mappings"

A "delete ALL mappings" client method exists in the integration (it would call Iute's `DELETE /api/v1/eshop/management/product-mapping?all=true`), but **no admin UI calls it** — there is no "wipe all" button in the Schemes tab. The merchant must select rows and click the bulk-delete action; there is no one-click reset. This is intentional: a one-click wipe would be destructive and easy to misclick.
