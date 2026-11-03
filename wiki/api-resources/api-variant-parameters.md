---
type: api-resource
resource_path: /api/v2/variant-parameters
http_methods: [GET, POST, PATCH, DELETE]
related_features: [products-variants-options, products-products]
aliases: ["Variant Parameters API", "JSON-API v2 variant-parameters", "API параметри на варианти", "/variant-parameters"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Variant Parameters (JSON-API v2)

## Purpose

A `variant-parameters` resource is one catalog-wide **dimension** a product can vary in: Size, Color, Capacity, Material. Each parameter holds a merchant-facing name + a display type that controls how its options render on the storefront variant picker (dropdown, radio, color swatch, image swatch, 2D grid, numeric alpha). Parameters are reused across products — a product attaches up to three via [[api-products|products]]'s `parameter1` / `parameter2` / `parameter3` relationships, and each [[api-variants|variant]] then binds one [[api-variant-options|option]] per attached parameter.

This is the **catalog dimension**, not the per-product binding. Integrations create parameters once, then reuse them when pushing variant grids for new products.

## Endpoint

- **URL base:** `<store-host>/api/v2/variant-parameters/`
- **GET collection** — `GET /api/v2/variant-parameters` — list with filter / sort / include / page.
- **GET single** — `GET /api/v2/variant-parameters/{id}`.
- **POST** — `POST /api/v2/variant-parameters` — requires `name` + `display_type`.
- **PATCH** — `PATCH /api/v2/variant-parameters/{id}`.
- **DELETE** — `DELETE /api/v2/variant-parameters/{id}`. Blocked while any product references the parameter.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/variant-parameters/{id}/relationships/variant-options`.
- No custom action routes.
- No app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **POST: required**, PATCH: optional | min 3, max 191 chars; **unique** across `products_parameters`. |
| `display_type` | enum | yes | yes | **POST: required** | One of `select`, `radio`, `image`, `color`, `2d`, `numeric_alpha`. Controls storefront rendering. Mapped from the model's `type` column. |
| `sort` | integer | yes | yes | no | Display order in the variant-parameters list. |
| `visible` | tinyint (0/1) | yes | yes | no | Whether the parameter shows up on the storefront. Default 1. |
| `in_listing` | tinyint (0/1) | yes | yes | no | Whether the parameter is exposed as a filter in product listings. Default 0. |
| `show_label` | tinyint (0/1) | yes | yes | no | Whether the parameter label renders next to its selected value. Default 0. |
| `next_update` | timestamp | yes | yes | no | Internal scheduling field used by background sync. |
| `type` | — | — | — | — | **Hidden** in serialised output — exposed as `display_type`. |
| `description` | — | — | — | — | **Hidden** in serialised output. |

No appendable values.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `variant-options` (aliased to `options` on the model) | hasMany | variant-options | yes | The option values (Small / Medium / Large) defined under this parameter. |

## Filtering & sorting

**Allowed filtering parameters** — no named filters in the validator. All raw columns on the `products_parameters` table are auto-allowed (e.g. `filter[visible]=1`, `filter[id]=5`). `filter[name]` is treated as a single-record lookup — when present, the adapter switches to single-record mode and returns one resource object.

**Allowed sort parameters** — none declared. Natural ordering applies (typically `id` ASC).

**Allowed include paths** — auto-allowed from schema: `options` (aliased to `variant-options` on the wire via the adapter's include-path map).

## Side effects on write

- **Uniqueness** — `name` must be unique platform-wide; collision returns 422 `The name has already been taken.`
- **No dedicated webhook** — no `variant-parameter.*` event in the platform catalogue. Subscribe to `product.*` to react when products start referencing a new parameter.
- **No platform-level audit log** for this resource beyond the standard model timestamps (`created_at` / `updated_at` are not exposed in serialised attributes — the framework treats the underlying table as untimestamped). Merchants needing an actor trail for parameter changes must keep their own log.
- **Delete guard** — DELETE returns 422 `Cannot delete a variant parameter which is in use by a products resource.` if any product references this parameter as its `p1_id`, `p2_id`, or `p3_id`. Detach the parameter from all products first.
- **Cascade behaviour on the database** — child [[api-variant-options|variant options]] under this parameter have an `ON DELETE CASCADE` rule on `parameter_id`, but the API delete is blocked before that point — so options are never silently lost via this endpoint.
- **Storefront re-render** — flipping `visible` / `in_listing` does not invalidate caches by itself; CDN-cached listings refresh on next regeneration (see [[apps-listing-engine]]).

## Plan-feature gating

None.

## Error examples (common 422 cases)

- Duplicate name:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The name has already been taken.","source":{"pointer":"/data/attributes/name"}}]}
  ```
- Delete blocked because products reference the parameter:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Cannot delete a variant parameter which is in use by a products resource.","source":{"pointer":"/data"}}]}
  ```
- Invalid display type:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The selected display_type is invalid.","source":{"pointer":"/data/attributes/display_type"}}]}
  ```

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (filter by visibility, sideload options)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-parameters?page[size]=20&filter[visible]=1&include=variant-options"
```

Single-record lookup by name (adapter switches to single-resource mode):

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-parameters?filter[name]=Size"
```

### GET single (with child options)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-parameters/5?include=variant-options"
```

### POST create (minimal)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-parameters" \
     -d '{
       "data": {
         "type": "variant-parameters",
         "attributes": {
           "name": "Size",
           "display_type": "select"
         }
       }
     }'
```

### POST create (richer — color swatch parameter)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-parameters" \
     -d '{
       "data": {
         "type": "variant-parameters",
         "attributes": {
           "name": "Color",
           "display_type": "color",
           "sort": 10,
           "visible": 1,
           "in_listing": 1,
           "show_label": 1
         }
       }
     }'
```

### PATCH update (rename / toggle visibility)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-parameters/5" \
     -d '{
       "data": {
         "type": "variant-parameters",
         "id": "5",
         "attributes": {
           "in_listing": 0
         }
       }
     }'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/variant-parameters/5"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "variant-parameters",
      "id": "5",
      "attributes": {
        "name": "Size",
        "display_type": "select",
        "sort": 0,
        "visible": 1,
        "in_listing": 0,
        "show_label": 0
      },
      "relationships": {
        "variant-options": { "data": [
          { "type": "variant-options", "id": "11" },
          { "type": "variant-options", "id": "12" }
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
    "type": "variant-parameters",
    "id": "7",
    "attributes": {
      "name": "Color",
      "display_type": "color",
      "sort": 10,
      "visible": 1,
      "in_listing": 1,
      "show_label": 1
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
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Cannot delete a variant parameter which is in use by a products resource.","source":{"pointer":"/data"}}]}
```

## Testing checklist

1. `GET /variant-parameters?include=variant-options` — confirm 200 + at least one parameter (typically pre-installed Size / Color).
2. `POST /variant-parameters` with `{"name":"<unique-name>","display_type":"select"}` — capture returned id.
3. `GET /variant-parameters/{id}` — verify the resource exists and `display_type` matches.
4. `PATCH /variant-parameters/{id}` with `{"attributes":{"visible":0}}` — confirm 200 + value change.
5. `POST /variant-parameters` again with the same `name` — verify 422 `The name has already been taken.`
6. `POST /variant-parameters` with `display_type: "blah"` — verify 422 `The selected display_type is invalid.`
7. `DELETE /variant-parameters/{id}` (while no product references it) — verify 204.
8. `GET /variant-parameters/{id}` — verify 404.

## Equivalent UI

- [[products-variants-options]] — manual variant-parameters management screen.
- [[products-products]] — picking `parameter1` / `parameter2` / `parameter3` on a product.

## Related

- [[json-api-v2]] — protocol contract.
- [[products-variants-options]] — admin UI equivalent.
- [[api-variant-options]] — child option values.
- [[api-variants]] — per-product variant rows.
- [[api-products]] — products bind parameters via `parameter1` / `parameter2` / `parameter3`.
- [[variant]] — variant entity reference.
- [[settings-api-keys]] — authentication setup.
- [[settings-hooks]] — webhook subscriptions.

## Open questions

- Confirm whether the storefront variant picker respects an updated `display_type` change live, or whether a CDN flush is needed.
- Verify the `next_update` field's purpose — its semantics are not obvious from the model and may relate to a background re-index job.
- Confirm whether `visible` and `in_listing` are exposed as `0/1` integers or as enum strings — the model defines them as `tinyint(1)` but admin UIs sometimes coerce.
