---
type: api-resource
resource_path: /api/v2/property-options
http_methods: [GET, POST, PATCH, DELETE]
related_features: [products-property, products-products]
aliases: ["Property Options API", "JSON-API v2 property-options", "API стойности на характеристики", "/property-options"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Property Options (JSON-API v2)

## Purpose

A `property-options` resource is one **option value** for a [[api-properties|property]] — Cotton / Polyester for a Material property, "1 year" / "2 years" for a Warranty period property. Each option belongs to one property (via `property_id`) and is referenced from products to record their per-product value (Material = Cotton).

This is the resource that integrations attach to products via the product's `property-options` hasMany relationship (see [[api-products]]) — that linkage records "this product has this property value".

## Endpoint

- **URL base:** `<store-host>/api/v2/property-options/`
- **GET collection** — `GET /api/v2/property-options`.
- **GET single** — `GET /api/v2/property-options/{id}`.
- **POST** — `POST /api/v2/property-options` — requires `value` + `property` relationship.
- **PATCH** — `PATCH /api/v2/property-options/{id}`.
- **DELETE** — `DELETE /api/v2/property-options/{id}`.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/property-options/{id}/relationships/property`.
- No custom action routes.
- No app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `value` | string | yes | yes | **POST: required**, PATCH: optional | min 1 char. Unique (case-insensitive, trimmed) within the same `property_id`. |
| `url_handle` | string | yes | yes | no | URL slug used in storefront filter URLs. Unique across `properties_options`. |
| `sort` | integer | yes | yes | no | Display order in the option picker / filter sidebar. |
| `description` | text | yes | yes | no | Long description shown on the filter-result page. |
| `seo_title` | string | yes | yes | no | SEO title for the filter-result page. |
| `seo_description` | string | yes | yes | no | SEO meta description. |
| `image` | string | yes | yes | no | Filename reference for image-display-type properties. |
| `parameter_id` | — | — | — | — | **Read-only.** (Note: a leftover from the variant-options validator pattern — the actual foreign key on this table is `property_id`, set via the `property` relationship.) |
| `max_thumb_size` | — | — | — | — | **Read-only.** Maintained by the image-processing pipeline. |
| `created_at`, `updated_at` | — | — | — | — | **Read-only.** System timestamps. |
| `id` | — | — | — | — | **Hidden** in serialised output (replaced by JSON:API `id`). |

No appendable values.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `property` | hasOne | properties | **required at POST** | The parent property. |

## Filtering & sorting

**Allowed filtering parameters** — no named filters. All raw columns on `properties_options` are auto-allowed (e.g. `filter[property_id]=12`). `filter[name]` triggers single-record mode in the adapter (treated as the search key even though the underlying column is `value`).

**Allowed sort parameters** — none declared. Natural ordering applies.

**Allowed include paths** — auto-allowed from schema: `property`.

## Side effects on write

- **Value uniqueness within property** — the validator runs a case-insensitive `LIKE` comparison against existing options under the same `property_id` (with `trim` on the input). Duplicates return 422 `The value has already been taken.`
- **No dedicated webhook** — no `property-option.*` event exists.
- **No platform-level audit log** beyond model timestamps.
- **Cascade to products** — DELETE cascades to `property_option_to_product` pivot rows. Products previously holding this value silently lose it; the storefront filter facet count refreshes on the next listing rebuild.
- **Storefront filter facet counts** — option creates / deletes affect the property's filter facet counts on category pages (subject to [[apps-listing-engine|Listing Engine]] re-index cadence + CDN cache).
- **URL handle uniqueness** — `url_handle` is used to construct the storefront filter URL (e.g. `/category/shoes?material=cotton`); must be unique across `properties_options`.

## Plan-feature gating

None.

## Error examples (common 422 cases)

- Missing required `value` on POST:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The value field is required.","source":{"pointer":"/data/attributes/value"}}]}
  ```
- Duplicate value within the same property:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The value has already been taken.","source":{"pointer":"/data/attributes/value"}}]}
  ```
- Missing required `property` relationship on POST:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The property field is required.","source":{"pointer":"/data/relationships/property"}}]}
  ```

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (filter by parent property, sideload property)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/property-options?page[size]=50&filter[property_id]=12&include=property"
```

Single-record lookup (the adapter treats `filter[name]` as the search key even though the column is `value`):

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/property-options?filter[name]=Cotton"
```

### GET single (with parent property)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/property-options/201?include=property"
```

### POST create (minimal)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/property-options" \
     -d '{
       "data": {
         "type": "property-options",
         "attributes": { "value": "Cotton" },
         "relationships": {
           "property": { "data": { "type": "properties", "id": "12" } }
         }
       }
     }'
```

### POST create (richer — with URL handle + SEO)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/property-options" \
     -d '{
       "data": {
         "type": "property-options",
         "attributes": {
           "value": "Polyester",
           "url_handle": "polyester",
           "sort": 20,
           "description": "Durable synthetic fabric.",
           "seo_title": "Polyester products",
           "seo_description": "Browse products made from polyester."
         },
         "relationships": {
           "property": { "data": { "type": "properties", "id": "12" } }
         }
       }
     }'
```

### PATCH update (rename)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/property-options/201" \
     -d '{
       "data": {
         "type": "property-options",
         "id": "201",
         "attributes": { "value": "100% Cotton" }
       }
     }'
```

### DELETE (cascades to all referencing products)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/property-options/201"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "property-options",
      "id": "201",
      "attributes": {
        "value": "Cotton",
        "url_handle": "cotton",
        "sort": 10,
        "description": null,
        "seo_title": null,
        "seo_description": null,
        "image": null,
        "max_thumb_size": null,
        "created_at": "2026-05-10 10:00:00",
        "updated_at": "2026-05-10 10:00:00"
      },
      "relationships": {
        "property": { "data": { "type": "properties", "id": "12" } }
      }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 1, "total": 1, "last-page": 1 } }
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "property-options",
    "id": "303",
    "attributes": {
      "value": "Cotton",
      "url_handle": null,
      "sort": 0,
      "description": null,
      "seo_title": null,
      "seo_description": null,
      "image": null,
      "created_at": "2026-06-05 11:04:21",
      "updated_at": "2026-06-05 11:04:21"
    },
    "relationships": {
      "property": { "data": { "type": "properties", "id": "12" } }
    }
  }
}
```

### Common failures

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The value field is required.","source":{"pointer":"/data/attributes/value"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The value has already been taken.","source":{"pointer":"/data/attributes/value"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The property field is required.","source":{"pointer":"/data/relationships/property"}}]}
```

## Testing checklist

1. `GET /property-options?filter[property_id]={property_id}&include=property` — confirm 200 + the parent property resolves in `included`.
2. `POST /property-options` with `{"value":"<unique>"}` and a valid `property` relationship — capture returned id.
3. `GET /property-options/{id}` — verify `value` matches and `property` relationship is set.
4. `PATCH /property-options/{id}` with `{"attributes":{"sort":99}}` — confirm 200.
5. `POST /property-options` again with the same `value` under the same property — verify 422 `The value has already been taken.`
6. `POST /property-options` without `property` — verify 422 with pointer `/data/relationships/property`.
7. `DELETE /property-options/{id}` — verify 204 (cascade silently strips the value from all products that held it).
8. `GET /property-options/{id}` — verify 404.

## Equivalent UI

- [[products-property]] — manual property + option management screen.
- [[products-products]] — assigning option values to individual products via `property-options`.

## Related

- [[json-api-v2]] — protocol contract.
- [[products-property]] — admin UI equivalent.
- [[api-properties]] — parent property resource.
- [[api-categories]] — categories control which properties (and hence which options) are shown on the product form.
- [[api-products]] — products attach property-options via their `property-options` relationship.
- [[category-property]] — entity reference for category-to-property linkage.
- [[apps-listing-engine]] — storefront filter index.
- [[settings-api-keys]] — authentication setup.
- [[settings-hooks]] — webhook subscriptions.

## Open questions

- The `readOnlyAttributes` list inherits `parameter_id` from the variant-options validator pattern — confirm whether `property_id` is also implicitly read-only or whether direct PATCH on it accidentally works. The expected and safe path is via the `property` relationship.
- Verify whether DELETE silently strips the value from all products without a merchant warning, and whether any webhook fires per affected product or just one cascade-summary event.
- The duplicate-value check uses SQL `LIKE` with the raw input — confirm SQL wildcards are escaped or treated literally.
