---
type: api-resource
resource_path: /api/v2/product-to-discount
http_methods: [GET, POST, PATCH, DELETE]
related_entity: discount
related_features: [marketing-discounts-fixed, marketing-discounts]
aliases: ["Product-to-Discount API", "Fixed-discount price overrides API", "JSON-API v2 product-to-discount", "API продукт-към-отстъпка", "/product-to-discount"]
tags: [api, json-api-v2, discounts, fixed-discounts]
plan_gates: ["discount_fixed"]
created: 2026-05-26
updated: 2026-06-10
source_count: 6
---
# Product-to-Discount (JSON-API v2)

## Purpose

`product-to-discount` is the JSON-API v2 resource for the **per-variant price overrides under a Fixed-type discount** — the pivot rows that bind one variant to one Fixed Discount at one override price. Integrations use it to push MSRP overrides from an ERP, bulk-update sale prices, read the active override set, and remove an override when a product is no longer on sale.

Fixed discounts work differently from percent / flat: instead of *"X% off everything"*, a Fixed discount is *"this specific variant now costs exactly Z cents"*. The override price is row-specific — two variants of the same product under the same Fixed Discount can carry different override prices. Each row links three FKs: the parent **Discount** (must be `type = fixed`), the parent **Product** (for grouping), and the specific **Variant** being repriced.

## Endpoint

- **URL base:** `<store-host>/api/v2/product-to-discount/`
- **Methods:** `GET` (collection), `GET /{id}`, `POST`, `PATCH /{id}`, `DELETE /{id}` — full CRUD. Not read-only. No custom routes. No app-installation requirement.

Base URL, auth, headers, and rate limits: see [[json-api-v2]].

```bash
# POST — attach a per-variant override price
curl -X POST 'https://<store-host>/api/v2/product-to-discount' \
  -H 'X-CloudCart-ApiKey: <YOUR_API_KEY>' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Accept: application/vnd.api+json' \
  -d '{ "data": {
      "type": "product-to-discount",
      "attributes": { "price": 2999, "active": 1 },
      "relationships": {
        "discount": { "data": { "type": "discounts", "id": "17" } },
        "product": { "data": { "type": "products", "id": "101" } },
        "variant": { "data": { "type": "variants", "id": "5001" } } } } }'
```

`price: 2999` = the FINAL price for variant 5001 while parent Discount 17 is active (29.99 in cents). Expected `201 Created`. PATCH `/{id}` changes the price (recomputes `save`); DELETE `/{id}` returns `204`.

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes / validation |
|---|---|---|---|---|---|
| `price` | int | yes | yes | POST yes / PATCH `sometimes` | Override price in cents — the FINAL price the customer pays for this variant while the parent is active. NOT a discount amount. On save derives `save = variant.price - price`. |
| `active` | int | yes | yes | no | Per-row enable flag. `0` skips the override (variant returns to catalog price); `1` fires it. |
| `discount_type` | string | **read-only** | **read-only** | — | From the parent's `type`; always `fixed` in practice. Appended accessor on GET. |
| `discount_id` | int | **read-only** | **read-only** | — | Parent Discount FK; set via the `discount` relationship at create. |
| `product_id` | int | **read-only** | **read-only** | — | Set via the `product` relationship at create. |
| `variant_id` | int | **read-only** | **read-only** | — | Set via the `variant` relationship at create. |
| `target_id` | int | **read-only** | **read-only** | — | Internal target-row reference, set on save. |
| `save` | int | **read-only** | **read-only** | — | Snapshot delta `variant.price - price` — the storefront *"you save X"* badge value. Later catalog-price changes do NOT refresh it until the row is PATCHed again. |
| `date_start`, `date_end` | date | **read-only** | **read-only** | — | Captured from the parent's date window on save. |
| `created_at`, `updated_at` | timestamp | **read-only** | **read-only** | — | Standard timestamps. |

A POST missing `price` returns 422 `"The price field is required."` (pointer `/data/attributes/price`).

## Relationships

All three are **required at create** and **immutable thereafter** (the validator marks all three FK columns read-only on update). To re-target an override (different variant / product / parent Discount), DELETE the row and POST a new one.

| Name | Cardinality | Target | Notes |
|---|---|---|---|
| `discount` | `hasOne` | [[api-discounts]] | **MUST point to a Fixed-type Discount.** A non-fixed parent returns 422 *"The discount type of discount {id} is not fixed"* (pointer `/data/relationships/discount`). Missing returns 422 *"The discount field is required."* |
| `product` | `hasOne` | [[api-products]] | The parent product the variant belongs to. |
| `variant` | `hasOne` | [[api-variants]] | The specific variant being repriced. |

## Filtering & sorting

**Filtering** — no named filters declared; the framework auto-allows `filter[<column>]` for every column on the `product_to_discount` table (equality only). Common: `filter[discount_id]` (all overrides under one Fixed Discount), `filter[product_id]`, `filter[variant_id]`, `filter[active]`, `filter[type]` (always `fixed`), `filter[customer_group_id]`, `filter[date_start]`, `filter[date_end]`.

**Sorting** — `id`, `date_start`, `date_end`, `created_at`, `updated_at`; prefix with `-` for descending.

**Include paths** — `discount`, `product`, `variant` (auto-merged from the schema's relationships).

**Sparse-field append** — none; `?append[product-to-discount]=...` returns 422. The `discount_type` accessor is appended unconditionally.

```json
// GET /api/v2/product-to-discount/300 → 200 OK
{ "data": {
    "type": "product-to-discount", "id": "300",
    "attributes": {
      "price": 2999, "save": 1000, "active": 1, "discount_type": "fixed",
      "discount_id": 17, "product_id": 101, "variant_id": 5001, "target_id": 9001,
      "date_start": "2026-07-01", "date_end": "2026-09-30",
      "created_at": "2026-05-26T10:14:02+00:00", "updated_at": "2026-06-04T07:22:11+00:00" },
    "relationships": {
      "discount": { "data": { "type": "discounts", "id": "17" } },
      "product": { "data": { "type": "products", "id": "101" } },
      "variant": { "data": { "type": "variants", "id": "5001" } } },
    "links": { "self": "https://<store-host>/api/v2/product-to-discount/300" } } }
```

## Side effects

- **Fixed-only parent validation on EVERY save** (POST and PATCH) — the save hook throws 422 if the parent's `type` isn't `fixed`. Flipping a parent's type via [[api-discounts]] doesn't retroactively invalidate existing rows, but any subsequent PATCH against them then fails.
- **Duplicate-row dedup on save** — after save, any other row with the same `(discount_id, product_id, variant_id)` triple is DELETEd: one active override per variant per Fixed Discount. POSTing the "same" override twice silently replaces the prior row (latest write wins). The DB unique index `uk_insert (variant_id, target_id, discount_id, customer_group_id)` enforces this too.
- **Per-product target materialisation** — on save the platform writes the per-product target row feeding the storefront's "from X / now Y" pricing display.
- **Storefront search re-index** — every save re-indexes the affected `product_id`; the search engine reflects it within a few minutes ([[apps-listing-engine]]). Bulk migrations fire one event per row — pace writes to avoid queue thrashing.
- **No dedicated webhook event** for pivot CRUD. Only `discount.created` / `discount.updated` / `discount.deleted` exist; writes here fire none (the parent's `updated_at` is untouched). See [[settings-hooks]].
- **Plan-feature gate inherited from parent** — the parent's create on [[api-discounts]] consumed the `discount_fixed` slot; this endpoint runs no per-row gate. A failed gate (on a parent create) surfaces as **HTTP 402 Payment Required**, not 403.
- **Discount-uses recompute (parent-level)** — the parent's `uses` counter is recomputed (not incremented) on every related order's status change via a 10-second-delayed job; cancelled orders free the slot — see [[discount-stacking]].
- **No audit log** — no actor, no diff history; only `created_at` / `updated_at`.
- **No-op override allowed** — when the POSTed `price` equals `variant.price`, the platform writes `save = 0` and stores the row anyway. The *"you save X"* badge then won't render. Verify intent before bulk-importing from a tool that may pass already-current prices.

## Equivalent UI

- [[marketing-discounts-fixed]] — admin-panel Fixed discount edit + per-product price-override sub-page (mirrors GET / POST / PATCH / DELETE on this endpoint).
- [[marketing-discounts]] — admin-panel master discount list (set `discount_type = fixed` on [[api-discounts]] for API parity).
- [[discount]] — entity attribute reference (covers Fixed-type semantics).

## Open questions

- Confirm whether the dedup DELETE-then-INSERT (same `discount_id + product_id + variant_id`) preserves the original `created_at` or stamps a fresh one — audit-history continuity may break.
- Confirm whether parent-and-child category Fixed-discount conflict validation (per [[marketing-discounts]]: *"Parent and Child product categories can not be included"*) applies to per-row writes here or only to the parent create-flow on [[api-discounts]].
- Verify whether bulk POSTs trigger one search-re-index event per row or batch, and whether a batch import path that suppresses individual events exists.
- Confirm whether `customer_group_id` (per-segment Fixed pricing) is writable here — the column is in the migration's unique index but not in the validator's rules.
- Verify whether deleting a parent Fixed Discount via [[api-discounts]] cascades through `fk_product_to_discount_discount_id` (`ON DELETE CASCADE`) for integrations holding row IDs from this endpoint.

## Related

- [[json-api-v2]] — API hub.
- [[api-discounts]] — parent Fixed Discount endpoint (set `discount_type = fixed`). Parent creation consumes the `discount_fixed` plan-counter.
- [[api-products]] — product resource (pivot's `product` relationship).
- [[api-variants]] — variant resource (pivot's `variant` relationship). Override prices are per-variant.
- [[discount]] — Discount entity reference (covers Fixed-type semantics).
- [[discount-stacking]] — Fixed discounts attach first in the implicit evaluation order; per-product Fixed + code-based discount + `apply_regular_price` max-of-two interaction.
- [[marketing-discounts-fixed]] — admin-panel Fixed discount edit + per-product override sub-page.
- [[marketing-discounts]] — admin-panel master discount list.
- [[apps-listing-engine]] — search-engine re-index queue triggered by every save.
- [[settings-hooks]] — `discount.*` events (no dedicated `product_to_discount.*` event exists).
