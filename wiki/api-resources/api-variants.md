---
type: api-resource
resource_path: /api/v2/variants
http_methods: [GET, POST, PATCH, DELETE]
related_entity: variant
related_features: [products-variants-options, products-inventory, products-products]
aliases: ["Variants API", "JSON-API v2 variants", "API варианти", "/variants"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Variants (JSON-API v2)

## Purpose

A `variants` resource is one purchasable SKU row under a [[api-products|product]] — one combination of up to three [[api-variant-parameters|variant parameters]] (e.g., Size = M × Color = Red) carrying its own price, stock quantity, SKU, barcode, weight, optional shipping modifier, and (with the Grocery Store app) per-unit metadata. A product with no parameters still has one "phantom" default variant holding its price + stock — that row has all `vN_id` NULL and can never carry per-variant images.

This is the canonical endpoint for ERP / WMS integrations pushing real-time SKU-level stock and price. Multi-warehouse merchants push per-warehouse stock via [[api-store-quantity]] and treat `variants.quantity` as a single-warehouse total.

## Endpoint

- **URL base:** `<store-host>/api/v2/variants/`
- **GET collection** — `GET /api/v2/variants` — filter / sort / include / page.
- **GET single** — `GET /api/v2/variants/{id}`.
- **POST** — `POST /api/v2/variants` — create. Requires `product` + matching `option1` / `option2` / `option3` per the product's parameter count.
- **PATCH** — `PATCH /api/v2/variants/{id}`.
- **DELETE** — `DELETE /api/v2/variants/{id}`.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/variants/{id}/relationships/<rel>` for `images`, `product`, `option1`, `option2`, `option3`. The `images` endpoint also enforces the "must have at least one option" guard (see Side effects).
- No custom action routes; no app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `quantity` | numeric (decimal 20,3) | yes | yes | no | Total stock (single-warehouse). Multi-warehouse stores write [[api-store-quantity]] instead. |
| `price` | integer | yes | yes | no | Price in **minor units** (stotinki / cents — storefront price × 100). Changing it recomputes the parent's default variant. |
| `delivery_price` | integer | yes | yes | no | Per-variant shipping modifier, minor units. |
| `weight` | integer | yes | yes | no | Weight in grams. |
| `sku` | string | yes | yes | no | Stock-keeping unit (max 191). Natural key for most warehouse / accounting integrations. |
| `barcode` | string | yes | yes | no | EAN / UPC (max 191). |
| `minimum` | numeric (decimal 20,3) | yes | yes | no | Per-variant minimum order qty. Default `1.000`. |
| `unit_value` | numeric (decimal 20,3) | yes | yes | no | Grocery Store unit value (e.g. 0.300 for a 300 g piece). |
| `unit_text` | string | yes | yes | no | Unit display label. |
| `unit_id` | integer | yes | yes | no | Reference to a [[api-units\|units]] row. Usually set indirectly via `unit_short_name`. |
| `base_unit_value` | numeric | yes | yes | no | Grocery Store base-unit value. Default `1.000`. |
| `base_unit_id` | integer | yes | yes | no | Grocery Store base unit reference. |
| `unit_type` | string | yes | yes | no | Grocery Store unit type (`measured` by default). |
| `item_id` | — | — | — | — | **Read-only.** Parent product ID — set via `product` relationship. |
| `v1`, `v2`, `v3` | — | — | — | — | **Read-only.** Option labels snapshotted from `option1` / `option2` / `option3`. |
| `v1_id`, `v2_id`, `v3_id` | — | — | — | — | **Read-only.** Option IDs — set via `option1` / `option2` / `option3`. |

**Appended accessors** (always serialised): `unit_name`, `unit_short_name`, `unit_value_formatted` — computed from `unit_id` + `unit_value` when the Grocery Store app is installed.

**Appendable on the parent products request:** `?append[variants]=discount` returns each sideloaded variant's effective discount block.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `product` | hasOne | products | **required at POST** | The parent product; source of `item_id`. |
| `images` | hasMany | images | yes | Per-variant images. **Blocked** when all `vN_id` are NULL (phantom default variant); attach to the product's `image` / `images` instead. |
| `option1` | hasOne | variant-options | required when product has `parameter1` | Variant-option for slot 1. |
| `option2` | hasOne | variant-options | required when product has `parameter2` | Variant-option for slot 2. |
| `option3` | hasOne | variant-options | required when product has `parameter3` | Variant-option for slot 3. |

## Filtering & sorting

- **Filter** — allow-list: `has_images`; plus all raw `products_variants` columns auto-allowed (e.g. `filter[sku]=ABC`, `filter[barcode]=...`, `filter[item_id]=12`).
- **Sort** — `id`, `quantity`, `price`, `weight` (prefix `-` for descending).
- **Include** — `images`, `product`, `option1`, `option2`, `option3`; plus nested `option1.parameter`, `option2.parameter`, `option3.parameter`.

## Side effects

No plan-feature gate; variant saves do not affect the parent's plan-slot accounting (active / hidden products, bundles).

- **Option-count consistency** — populated `option*` count must match the parent's parameter count. Mismatch → 422 `You are trying to save variant with N options, but your product requires M`.
- **Option-to-parameter binding** — each `optionN` must belong to the matching parameter. Mismatch → 422 `Variant option '<v>' does not belongs to variant parameter '<p>'`.
- **Phantom-variant duplicate guard** — POST with all `vN_id` NULL is rejected if the product already has a NULL-options variant.
- **Image-attach guard** — attaching images is rejected with 422 when all `vN_id` are NULL: `Images can only be attached to variants that have at least one option (option1, option2 or option3). Use the product `image_id` instead.`
- **Default-variant recompute** — changing `price` recomputes the product's default variant (lowest-priced, ID-tiebroken) and re-applies product discounts.
- **Cascade on every save** — re-checks the full variant set, refreshes per-option counts when `v*_id` changes, bumps the parent's timestamp, invalidates caches, re-prices bundles, and re-indexes for storefront search.
- **Per-variant change log** — a per-attribute diff is logged with `initiator = "api"` plus the API key's id + name (visible in the merchant's change history).
- **No dedicated webhook** — variant writes fire no `variant.*` webhook (no such event exists). Subscribe to `product.*` instead (note `product.created` / `product.updated` are gated to admin-UI saves only — see [[api-products]] Side effects).

DELETE: removes the variant row; the parent is touched, re-priced, and its default-variant pointer re-computed. If the product has parameters and the delete would leave it with no variants, the validation re-run rejects it (see [[products-variants-options]]).

## Example requests

### GET collection (filter, sort, sideload)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variants?page[size]=20&sort=-id&filter[item_id]=42&include=product,option1,option2,images"
```

### POST create (product with parameter1 Size + parameter2 Color)

For a no-parameter product, omit the `option*` relationships and send only `product` + attributes — the row becomes the phantom default variant.

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variants" \
     -d '{
       "data": {
         "type": "variants",
         "attributes": {
           "price": 2499,
           "delivery_price": 0,
           "weight": 220,
           "quantity": 25,
           "sku": "TSHIRT-M-RED",
           "barcode": "5012345678900",
           "minimum": 1
         },
         "relationships": {
           "product": { "data": { "type": "products", "id": "42" } },
           "option1": { "data": { "type": "variant-options", "id": "11" } },
           "option2": { "data": { "type": "variant-options", "id": "21" } }
         }
       }
     }'
```

### PATCH update (stock + price)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variants/101" \
     -d '{
       "data": {
         "type": "variants",
         "id": "101",
         "attributes": {
           "quantity": 100,
           "price": 1899
         }
       }
     }'
```

DELETE is `DELETE /api/v2/variants/{id}` with the auth header (see Endpoint).

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "variants",
      "id": "101",
      "attributes": {
        "item_id": 42,
        "sku": "TSHIRT-M-RED",
        "barcode": "5012345678900",
        "price": 1999,
        "delivery_price": 0,
        "weight": 220,
        "quantity": 25,
        "minimum": 1,
        "v1": "M", "v2": "Red", "v3": null,
        "v1_id": 11, "v2_id": 21, "v3_id": null,
        "unit_name": null, "unit_short_name": null, "unit_value_formatted": null
      },
      "relationships": {
        "product": { "data": { "type": "products", "id": "42" } },
        "option1": { "data": { "type": "variant-options", "id": "11" } },
        "option2": { "data": { "type": "variant-options", "id": "21" } }
      }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 } }
}
```

A successful POST returns `201 Created` with the same shape (one `data` object, `v*` / `v*_id` from the supplied options).

### Common failures (422 / 404)

```
HTTP 422 — {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"You are trying to save variant with 1 options, but your product requires 2","source":{"pointer":"/data/relationships/product"}}]}

HTTP 422 — {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Variant option 'Red' does not belongs to variant parameter 'Size'","source":{"pointer":"/data/relationships/option1"}}]}

HTTP 422 — {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Images can only be attached to variants that have at least one option (option1, option2 or option3). Use the product `image_id` instead.","source":{"pointer":"/data/relationships/images"}}]}

HTTP 404 — {"errors":[{"status":"404","title":"Not Found"}]}
```

## Equivalent UI

- [[products-variants-options]] — manual variants editor (table at the bottom of the product edit screen).
- [[products-inventory]] — bulk per-variant stock + price edits in the inventory listing.
- [[products-products]] — variant creation through the product create / edit form.

Use these to map a "stock changed unexpectedly" ticket to an API-vs-UI actor.

## Related

- [[json-api-v2]] — protocol contract.
- [[variant]] — full variant attribute reference.
- [[api-products]] — parent product resource.
- [[api-variant-parameters]] — parameter (Size, Color) definitions.
- [[api-variant-options]] — option (Small, Red) values referenced via `option1` / `option2` / `option3`.
- [[api-images]] — image creation endpoint (image IDs created there can be attached to variants here).
- [[api-store-quantity]] — per-warehouse stock for multi-store merchants.
- [[api-units]] — units catalog referenced by `unit_id`.
- [[settings-api-keys]] — authentication setup.
- [[settings-hooks]] — webhook subscriptions.

## Open questions

- Whether `product.updated` ever fires for an API variant write (the timestamp bump should not trip the admin-UI-only webhook gate, but unverified).
- The upper bound — the admin UI documents 500 variants/product as a soft limit; server-side enforcement for variant POSTs is unconfirmed.
- Per-variant `minimum` vs product `minimum`: when both are set the larger applies (documented admin behaviour, API path not traced).
