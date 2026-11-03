---
type: api-resource
resource_path: /api/v2/properties
http_methods: [GET, POST, PATCH, DELETE]
related_entity: category-property
related_features: [products-property, products-categories]
aliases: ["Properties API", "JSON-API v2 properties", "API характеристики", "/properties"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Properties (JSON-API v2)

## Purpose

A `properties` resource is one catalog-wide **spec attribute** that describes a product beyond its variant grid: Material, Country of origin, Screen size, Warranty period. Each property has a name, a display type (`checkbox` / `select` / `radio` / `range`), and a set of [[api-property-options|option values]]. Properties are attached to one or more [[api-categories|categories]] (via the category's `properties` relationship); the per-product VALUE is stored as a [[api-property-options|property-option]] linked to the product via the product's `property-options` relationship.

Properties differ from [[api-variant-parameters|variant parameters]] in scope: variant parameters create the SKU grid (Size × Color = 6 variant rows); properties are spec / attribute fields shown on the product page and surfaced as storefront filter facets ("Show me products with Material = Cotton").

## Endpoint

- **URL base:** `<store-host>/api/v2/properties/`
- **GET collection** — `GET /api/v2/properties`.
- **GET single** — `GET /api/v2/properties/{id}`.
- **POST** — `POST /api/v2/properties` — requires `name` + `display_type`.
- **PATCH** — `PATCH /api/v2/properties/{id}`.
- **DELETE** — `DELETE /api/v2/properties/{id}`.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/properties/{id}/relationships/property-options`.
- No custom action routes.
- No app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **POST: required**, PATCH: optional | min 3, max 191 chars; **unique** across `properties`. |
| `display_type` | enum | yes | yes | **POST: required** | One of `checkbox`, `select`, `radio`, `range`. Controls the storefront filter module. Mapped from the model's `type` column. |
| `sort` | integer | yes | yes | no | Display order in the property management UI. |
| `is_visible` | tinyint (0/1) | yes | yes | no | Whether the property renders on the product page + filter sidebar. Default 1. |
| `active` | tinyint (0/1) | yes | yes | no | Whether the property is enabled for use. Default 1. |
| `url_handle` | string | yes | yes | no | URL slug used in storefront filter URLs (e.g. `/category?material=cotton`). Unique across `properties`. |
| `dec_points` | integer | yes | yes | no | Decimal precision for numeric-valued properties (used by `range` display type). Default 2. |
| `image` | string | yes | yes | no | Filename reference for image-display-type properties. |
| `type` | — | — | — | — | **Hidden** in serialised output — exposed as `display_type`. |

No appendable values.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `property-options` (aliased to `options` on the model) | hasMany | property-options | yes | The option values defined under this property. |

## Filtering & sorting

**Allowed filtering parameters** — no named filters. All raw columns on the `properties` table are auto-allowed (`filter[active]=1`, `filter[is_visible]=1`, `filter[type]=select`). `filter[name]` triggers single-record mode in the adapter.

**Allowed sort parameters** — none declared. Natural ordering applies.

**Allowed include paths** — auto-allowed from schema: `options` (aliased to `property-options` via the adapter's include-path map).

## Side effects on write

- **Uniqueness** — `name` must be unique platform-wide; collision returns 422 `The name has already been taken.`
- **No dedicated webhook** — no `property.*` event in the platform catalogue.
- **No platform-level audit log** beyond model timestamps. Merchants needing an actor trail for property changes must keep their own log.
- **Cascade on delete** — deleting a property cascades at the database level to its `property-options` and to the `property_to_category` pivot rows (per the schema's `ON DELETE CASCADE`). Products that previously carried a value for this property silently lose the value — there is no merchant warning when the delete happens via API.
- **Storefront filter cache** — changes to `is_visible` / `display_type` / `url_handle` only affect storefront listings on the next [[apps-listing-engine|Listing Engine]] re-index pass + CDN refresh.

## Plan-feature gating

None.

## Error examples (common 422 cases)

- Missing required `display_type` on POST:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The display_type field is required.","source":{"pointer":"/data/attributes/display_type"}}]}
  ```
- Duplicate name:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The name has already been taken.","source":{"pointer":"/data/attributes/name"}}]}
  ```
- Invalid display type:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The selected display_type is invalid.","source":{"pointer":"/data/attributes/display_type"}}]}
  ```

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (filter by active, sideload options)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/properties?page[size]=20&filter[active]=1&include=property-options"
```

Single-record lookup by name:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/properties?filter[name]=Material"
```

### GET single (with options)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/properties/12?include=property-options"
```

### POST create (minimal)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/properties" \
     -d '{
       "data": {
         "type": "properties",
         "attributes": {
           "name": "Material",
           "display_type": "select"
         }
       }
     }'
```

### POST create (richer)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/properties" \
     -d '{
       "data": {
         "type": "properties",
         "attributes": {
           "name": "Screen size",
           "display_type": "range",
           "url_handle": "screen-size",
           "sort": 20,
           "is_visible": 1,
           "active": 1,
           "dec_points": 1
         }
       }
     }'
```

### PATCH update (toggle visibility)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/properties/12" \
     -d '{
       "data": {
         "type": "properties",
         "id": "12",
         "attributes": { "is_visible": 0 }
       }
     }'
```

### DELETE (cascades to options + category pivots — verify before running)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/properties/12"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "properties",
      "id": "12",
      "attributes": {
        "name": "Material",
        "display_type": "select",
        "sort": 0,
        "is_visible": 1,
        "active": 1,
        "url_handle": "material",
        "dec_points": 2,
        "image": null
      },
      "relationships": {
        "property-options": { "data": [
          { "type": "property-options", "id": "201" },
          { "type": "property-options", "id": "202" }
        ]}
      }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 } }
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "properties",
    "id": "18",
    "attributes": {
      "name": "Material",
      "display_type": "select",
      "sort": 0,
      "is_visible": 1,
      "active": 1,
      "url_handle": "material",
      "dec_points": 2,
      "image": null
    }
  }
}
```

### Common failures

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The display_type field is required.","source":{"pointer":"/data/attributes/display_type"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The selected display_type is invalid.","source":{"pointer":"/data/attributes/display_type"}}]}
```

## Testing checklist

1. `GET /properties?include=property-options&page[size]=5` — confirm 200.
2. `POST /properties` with `{"name":"<unique-name>","display_type":"select"}` — capture returned id.
3. `GET /properties/{id}` — verify `display_type == "select"`.
4. `PATCH /properties/{id}` with `{"attributes":{"is_visible":0}}` — confirm 200.
5. `POST /properties` without `display_type` — verify 422 with pointer `/data/attributes/display_type`.
6. `POST /properties` again with the same `name` — verify 422 `The name has already been taken.`
7. `DELETE /properties/{id}` — verify 204.
8. `GET /properties/{id}` — verify 404.

## Equivalent UI

- [[products-property]] — manual property management screen.
- [[products-categories]] — attaching properties to categories.
- [[products-products]] — assigning per-product property values via `property-options`.

## Related

- [[json-api-v2]] — protocol contract.
- [[products-property]] — admin UI equivalent.
- [[api-property-options]] — child option values.
- [[api-categories]] — categories attach properties to control their visibility on the product form.
- [[api-products]] — products attach property-options via their `property-options` relationship.
- [[category-property]] — entity reference for the property-to-category linkage.
- [[apps-listing-engine]] — storefront filter index.
- [[settings-api-keys]] — authentication setup.
- [[settings-hooks]] — webhook subscriptions.

## Open questions

- Verify whether DELETE silently strips values from all referencing products without a warning (the cascade rule suggests yes; admin UI may surface a warning the API skips).
- Confirm whether changing `display_type` (e.g. `checkbox` → `range`) re-validates existing property-options (range expects numeric values; checkbox/select accept arbitrary strings).
- Confirm whether dedicated `property.*` webhooks exist (no events found in the platform catalogue at the time of writing).
