---
type: api-resource
resource_path: /api/v2/products
http_methods: [GET, POST, PATCH, DELETE]
related_entity: product
related_features: [products-products, products-inventory, products-variants-options]
aliases: ["Products API examples", "products curl examples", "products testing checklist", "products request response payloads", "API продукти примери"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Products API — worked examples & testing checklist

> Part of [[api-products]]. See the hub for the other aspects (attributes & relationships, filtering & sorting, side effects).

## Purpose

This aspect collects **copy-paste curl requests, the JSON responses they return, and a CRUD testing checklist** for the `products` resource. For the field meanings, see [[api-products-attributes]]; for query parameters, see [[api-products-filtering]]; for what each write triggers, see [[api-products-side-effects]].

## Endpoint

- **URL base:** `<store-host>/api/v2/products/`
- **Methods exercised here:** `GET` (collection + single), `POST`, `PATCH /{id}`, `DELETE /{id}`.

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`), `<YOUR_API_KEY>` (64-char uppercase), and a numeric resource id. Auth / headers: see [[json-api-v2]].

## Attributes

The payloads below write the attributes documented on [[api-products-attributes]] — only `name` + the `category` relationship are required at POST.

## Relationships

The richer POST example sends `category`, `categories`, `vendor`, `parameter1`, `parameter2` — see [[api-products-attributes]] for the full relationship table and the parameter-ordering rules.

## Filtering & sorting

The GET collection examples below combine `page`, `sort`, `filter`, and `include` — full reference in [[api-products-filtering]].

## Example requests

### GET collection (list, sort, filter, sideload)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products?page[size]=10&page[number]=1&sort=-date_added&filter[active]=yes&include=variant,category,vendor"
```

Filter by SKU (joined against variants):

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products?filter[sku]=SKU-100-RED-M&include=variants"
```

Single-record lookup by URL handle (returns one resource object, not a collection):

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products?filter[url_handle]=red-t-shirt"
```

### GET single (with includes + append)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products/42?include=variants,images,category,property-options.property&append[products]=meta,discount&append[variants]=discount"
```

### POST create (minimal required-only)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products" \
     -d '{
       "data": {
         "type": "products",
         "attributes": {
           "name": "API Test Product"
         },
         "relationships": {
           "category": { "data": { "type": "categories", "id": "1" } }
         }
       }
     }'
```

### POST create (richer payload + parameters + vendor + property-options)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products" \
     -d '{
       "data": {
         "type": "products",
         "attributes": {
           "name": "Cotton T-Shirt",
           "url_handle": "cotton-t-shirt",
           "active": "yes",
           "new": "yes",
           "tracking": "yes",
           "shipping": "yes",
           "continue_selling": "no",
           "minimum": 1,
           "description": "100% organic cotton.",
           "short_description": "Soft, breathable.",
           "seo_title": "Cotton T-Shirt | Design",
           "seo_description": "Buy our organic cotton T-shirt.",
           "sort_order": 100
         },
         "relationships": {
           "category": { "data": { "type": "categories", "id": "1" } },
           "categories": { "data": [{ "type": "categories", "id": "1" }, { "type": "categories", "id": "2" }] },
           "vendor": { "data": { "type": "vendors", "id": "3" } },
           "parameter1": { "data": { "type": "variant-parameters", "id": "5" } },
           "parameter2": { "data": { "type": "variant-parameters", "id": "6" } }
         }
       }
     }'
```

### PATCH update (flip flags / rename)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products/42" \
     -d '{
       "data": {
         "type": "products",
         "id": "42",
         "attributes": {
           "active": "no",
           "sale": "yes"
         }
       }
     }'
```

### DELETE (soft delete)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/products/42"
```

## Example responses

### GET collection success (`X-Show-Links: 1` adds the links block)

```json
{
  "data": [
    {
      "type": "products",
      "id": "42",
      "attributes": {
        "name": "Cotton T-Shirt",
        "url_handle": "cotton-t-shirt",
        "active": "yes",
        "draft": "no",
        "sale": "no",
        "new": "yes",
        "tracking": "yes",
        "shipping": "yes",
        "price_from": 1999,
        "price_to": 2499,
        "product_type": "simple",
        "date_added": "2026-06-01 09:12:33",
        "date_modified": "2026-06-04 14:02:11"
      },
      "relationships": {
        "category": { "data": { "type": "categories", "id": "1" } },
        "vendor": { "data": { "type": "vendors", "id": "3" } }
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 10, "from": 1, "to": 10, "total": 137, "last-page": 14 }
  },
  "links": {
    "first": "https://<store-host>/api/v2/products?page[number]=1&page[size]=10",
    "prev": null,
    "next": "https://<store-host>/api/v2/products?page[number]=2&page[size]=10",
    "last": "https://<store-host>/api/v2/products?page[number]=14&page[size]=10"
  }
}
```

### GET single success (with included)

```json
{
  "data": {
    "type": "products",
    "id": "42",
    "attributes": {
      "name": "Cotton T-Shirt",
      "url_handle": "cotton-t-shirt",
      "active": "yes",
      "price_from": 1999,
      "price_to": 2499,
      "p1": "Size",
      "p2": "Color"
    },
    "relationships": {
      "category": { "data": { "type": "categories", "id": "1" } },
      "variants": { "data": [
        { "type": "variants", "id": "101" },
        { "type": "variants", "id": "102" }
      ]}
    }
  },
  "included": [
    { "type": "variants", "id": "101", "attributes": { "sku": "TSHIRT-M-RED", "price": 1999, "quantity": 25 } },
    { "type": "categories", "id": "1", "attributes": { "name": "Shirts", "url_handle": "shirts" } }
  ]
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "products",
    "id": "143",
    "attributes": {
      "name": "API Test Product",
      "url_handle": "api-test-product",
      "active": "no",
      "draft": "no",
      "sale": "no",
      "new": "no",
      "tracking": "no",
      "shipping": "no",
      "minimum": 1,
      "product_type": "simple",
      "price_from": 0,
      "price_to": 0,
      "date_added": "2026-06-05 11:00:01"
    },
    "relationships": {
      "category": { "data": { "type": "categories", "id": "1" } }
    }
  }
}
```

### Common failures

```
HTTP 401 Unauthorized
{"errors":[{"status":"401","title":"Unauthenticated"}]}
```

```
HTTP 404 Not Found
{"errors":[{"status":"404","title":"Not Found"}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The category field is required.","source":{"pointer":"/data/relationships/category"}}]}
```

## Side effects

The POST / PATCH / DELETE examples above each trigger the save pipeline (variant validation, change-log entry, search re-index) and, for DELETE only, the `product.deleted` webhook. Full catalogue: see [[api-products-side-effects]].

## Testing checklist

1. `GET /products?page[size]=1&sort=-date_added` — confirm 200 + `meta.page.total` > 0.
2. `POST /products` with the minimal payload above — capture `data.id` from the 201 response.
3. `GET /products/{id}?include=category` — verify `attributes.name == "API Test Product"` and the category relationship resolves.
4. `PATCH /products/{id}` with `{"attributes":{"active":"yes"}}` — confirm 200 and the updated attribute.
5. `GET /products/{id}` again — verify `active == "yes"`.
6. `POST /products` with NO `category` relationship — verify 422 with pointer `/data/relationships/category`.
7. `POST /products` with `parameter2` but no `parameter1` — verify 422 `Missing Parameter Relationship`.
8. `DELETE /products/{id}` — verify 204 No Content.
9. `GET /products/{id}` — verify 404 (soft-delete invisible to GET).

## Equivalent UI

- [[products-products]] — the manual create / edit / delete flow the API mirrors.
- [[products-inventory]] — bulk per-variant edits equivalent to writing the `variants` relationship.

## Related

- [[api-products]] — hub.
- [[json-api-v2]] — auth header, `Accept` / `Content-Type` requirements, status-code reference.
- [[api-products-attributes]] — fields used in the payloads.
- [[api-products-filtering]] — query parameters used in the GET examples.
- [[api-products-side-effects]] — what each write triggers.
- [[settings-api-keys]] — where to obtain `<YOUR_API_KEY>`.

## Open questions

None.
