---
type: api-resource
resource_path: /api/v2/variant-options
http_methods: [GET, POST, PATCH, DELETE]
related_features: [products-variants-options, products-products]
aliases: ["Variant Options API", "JSON-API v2 variant-options", "API стойности на варианти", "/variant-options"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Variant Options (JSON-API v2)

## Purpose

A `variant-options` resource is one **option value** that belongs to a [[api-variant-parameters|variant parameter]] — Small / Medium / Large for a Size parameter, Red / Blue / Green for a Color parameter. Each option is permanently bound to one parameter (via `parameter_id`) and is the assignable value on individual [[api-variants|variants]] (`option1`, `option2`, `option3`).

For Color / image / 2D display-type parameters, the option also carries per-option metadata (`color` hex, `image` filename, dimensions) — the storefront swatch picker reads from here.

## Endpoint

- **URL base:** `<store-host>/api/v2/variant-options/`
- **GET collection** — `GET /api/v2/variant-options` — list across all parameters.
- **GET single** — `GET /api/v2/variant-options/{id}`.
- **POST** — `POST /api/v2/variant-options` — requires `name` + `parameter` relationship.
- **PATCH** — `PATCH /api/v2/variant-options/{id}`.
- **DELETE** — `DELETE /api/v2/variant-options/{id}`. Blocked while any variant references the option.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/variant-options/{id}/relationships/parameter`.
- No custom action routes.
- No app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **POST: required**, PATCH: optional | min 1 char. Unique (case-insensitive, trimmed) within the same `parameter_id`. |
| `sort` | integer | yes | yes | no | Display order in the option picker. |
| `image` | string | yes | yes | no | Image filename (for image / 2D display-type parameters). Upload itself happens through the admin file pipeline; this attribute stores the path reference. |
| `color` | char(6) | yes | yes | no | 6-character hex color (no `#`), used when the parent parameter's `display_type` is `color`. |
| `visible` | tinyint (0/1) | yes | yes | no | Whether the option is selectable on the storefront. Default 1. |
| `parameter_id` | — | — | — | — | **Read-only.** Set via the `parameter` relationship. |
| `max_thumb_size` | — | — | — | — | **Read-only.** Maintained by the image-processing pipeline. |
| `created_at`, `updated_at` | — | — | — | — | **Read-only.** System timestamps. |
| `id`, `settings` | — | — | — | — | **Hidden** in serialised output. |

No appendable values.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `parameter` | hasOne | variant-parameters | **required at POST** | The parent parameter this option belongs to. |

## Filtering & sorting

**Allowed filtering parameters** — no named filters. All raw columns on the `products_parameters_options` table are auto-allowed (e.g. `filter[parameter_id]=5`, `filter[visible]=1`). `filter[name]` triggers single-record mode in the adapter.

**Allowed sort parameters** — none declared. Natural ordering applies.

**Allowed include paths** — auto-allowed from schema: `parameter`.

## Side effects on write

- **Uniqueness within parameter** — the validator runs a case-insensitive `LIKE` comparison against existing options under the same `parameter_id` (with `trim` on the input). Duplicates return 422 `The name has already been taken.`
- **Delete guard** — DELETE returns 422 `Cannot delete a variant option which is in use by a variants resource.` if any variant references this option as `v1_id`, `v2_id`, or `v3_id`. Reassign the variants first.
- **No dedicated webhook** — no `variant-option.*` event exists. Subscribe to `product.*` for parent-level notifications.
- **No platform-level audit log** beyond model timestamps. Merchants needing an actor trail for option changes must keep their own log.
- **Storefront swatch picker** — changes to `color`, `image`, `visible` affect the next category-page render (subject to CDN cache).
- **Variant-option stat refresh** — editing the option itself does NOT trigger the parent product's `updateOptionsStat` job; that job runs when variants are saved, not when option metadata changes.

## Plan-feature gating

None.

## Error examples (common 422 cases)

- Duplicate name within the same parameter:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The name has already been taken.","source":{"pointer":"/data/attributes/name"}}]}
  ```
- Delete blocked by referencing variants:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Cannot delete a variant option which is in use by a variants resource.","source":{"pointer":"/data"}}]}
  ```
- Missing required `parameter` relationship on POST:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The parameter field is required.","source":{"pointer":"/data/relationships/parameter"}}]}
  ```

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (filter by parent parameter, sideload parent)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-options?page[size]=50&filter[parameter_id]=5&include=parameter"
```

Single-record lookup by name (adapter switches to single-resource mode):

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-options?filter[name]=Red"
```

### GET single (with parent parameter)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-options/11?include=parameter"
```

### POST create (minimal — text option)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-options" \
     -d '{
       "data": {
         "type": "variant-options",
         "attributes": { "name": "Medium" },
         "relationships": {
           "parameter": { "data": { "type": "variant-parameters", "id": "5" } }
         }
       }
     }'
```

### POST create (richer — color swatch with hex)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-options" \
     -d '{
       "data": {
         "type": "variant-options",
         "attributes": {
           "name": "Red",
           "sort": 10,
           "color": "ff0000",
           "visible": 1
         },
         "relationships": {
           "parameter": { "data": { "type": "variant-parameters", "id": "7" } }
         }
       }
     }'
```

### PATCH update (rename + reorder)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-options/11" \
     -d '{
       "data": {
         "type": "variant-options",
         "id": "11",
         "attributes": { "sort": 99 }
       }
     }'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-options/11"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "variant-options",
      "id": "11",
      "attributes": {
        "name": "M",
        "sort": 10,
        "image": null,
        "color": null,
        "visible": 1,
        "max_thumb_size": null,
        "created_at": "2026-05-12 14:00:00",
        "updated_at": "2026-05-12 14:00:00"
      },
      "relationships": {
        "parameter": { "data": { "type": "variant-parameters", "id": "5" } }
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
    "type": "variant-options",
    "id": "33",
    "attributes": {
      "name": "Red",
      "sort": 10,
      "image": null,
      "color": "ff0000",
      "visible": 1,
      "created_at": "2026-06-05 11:02:33",
      "updated_at": "2026-06-05 11:02:33"
    },
    "relationships": {
      "parameter": { "data": { "type": "variant-parameters", "id": "7" } }
    }
  }
}
```

### Common failures

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The name has already been taken.","source":{"pointer":"/data/attributes/name"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The parameter field is required.","source":{"pointer":"/data/relationships/parameter"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Cannot delete a variant option which is in use by a variants resource.","source":{"pointer":"/data"}}]}
```

## Testing checklist

1. `GET /variant-options?filter[parameter_id]={parameter_id}&include=parameter` — confirm 200 + child options for the parameter.
2. `POST /variant-options` with `{"name":"<unique>"}` and a valid `parameter` relationship — capture returned id.
3. `GET /variant-options/{id}` — verify `parameter` relationship matches.
4. `PATCH /variant-options/{id}` with `{"attributes":{"visible":0}}` — confirm 200 + value change.
5. `POST /variant-options` again with the same `name` under the same parameter — verify 422 `The name has already been taken.`
6. `POST /variant-options` without `parameter` — verify 422 with pointer `/data/relationships/parameter`.
7. `DELETE /variant-options/{id}` (when no variant references it) — verify 204.
8. `GET /variant-options/{id}` — verify 404.

## Equivalent UI

- [[products-variants-options]] — option management screen (per-parameter list of options).
- [[products-products]] — option picker shown when editing a variant on the product form.

## Related

- [[json-api-v2]] — protocol contract.
- [[products-variants-options]] — admin UI equivalent.
- [[api-variant-parameters]] — parent parameter resource.
- [[api-variants]] — variant rows that bind options to a product.
- [[api-products]] — products that use variant parameters + options.
- [[variant]] — variant entity reference.
- [[settings-api-keys]] — authentication setup.
- [[settings-hooks]] — webhook subscriptions.

## Open questions

- Confirm whether the option's `image` upload runs through this resource or only through a separate admin file pipeline (the column accepts a filename reference; the upload step is not exposed here).
- The duplicate-name check uses SQL `LIKE` with the raw input — confirm SQL wildcards are escaped or treated literally.
- Verify the cascade behaviour when a variant option's parent parameter is deleted at the database level (FK `ON DELETE CASCADE` exists, but the API blocks parameter deletes when in use, so this code path may be unreachable).
