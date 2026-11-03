---
type: api-resource
resource_path: /api/v2/units
http_methods: [GET]
related_entity: product
related_features: [apps-grocery-store-overview-new, apps-grocery-store-settings, products-products]
aliases: ["Units API", "Grocery units API", "JSON-API v2 units", "API мерни единици", "/units", "Measurement units API"]
tags: [api, json-api-v2, multistore, grocery, units]
plan_gates: [grocery-store]
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Units (JSON-API v2)

## Purpose

A `units` resource is one **unit of measure** the merchant has configured for use with the [[apps-grocery-store-overview-new|Grocery Store]] app — kilogram, gram, litre, millilitre, piece, pack. Units form a parent / child conversion tree (e.g., gram is a child of kilogram with a 1000-step conversion); each unit holds a name, short name (storefront label), plural name, conversion `steps` to its parent, and number of decimal places to display.

This resource is **read-only on JSON-API v2** — units are managed admin-only via the Grocery Store app's UI (or auto-installed from defaults on first activation). Integrations consume the catalog for picker UIs, label rendering, and to resolve `unit_id` references on [[api-products|products]] / [[api-variants|variants]].

## Endpoint

- **URL base:** `<store-host>/api/v2/units/`
- **GET collection** — `GET /api/v2/units`.
- **GET single** — `GET /api/v2/units/{id}`.
- **POST / PATCH / DELETE — NOT supported.** Route registered `readOnly` — those verbs return **405 Method Not Allowed**.
- No relationship endpoints declared in routes.
- No custom action routes.
- **App-install requirement:** the route is wrapped in `api_apps_installed:grocery_store` middleware. Without the Grocery Store app installed, every request returns **HTTP 404** with `"grocery_store app not installed"`.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

All attributes are read-only. The serializer returns every column on the `products_units` table:

| Attribute | Type | Notes |
|---|---|---|
| `id` | integer | Stable unit identifier. Referenced by `products.unit_id` / `variants.unit_id`. |
| `parent_id` | integer / null | Parent unit in the conversion tree (e.g., `gram.parent_id = kilogram.id`). NULL for top-level units. The admin-side `saving` hook forces `parent_id = null` when empty AND sets `steps = 1` for top-level units. |
| `name` | string | Full unit name (e.g., `kilogram`, `gram`, `litre`). |
| `short_name` | string / null | Storefront-facing short label (e.g., `kg`, `g`, `l`). |
| `multiple_name` | string / null | Plural name (e.g., `kilograms`). |
| `steps` | double(8,2) | Conversion factor to the parent unit (e.g., `gram.steps = 1000` because 1 kilogram = 1000 grams). Top-level units have `steps = 1`. |
| `decimals` | tinyint | Number of decimal places displayed for quantities in this unit (e.g., `kg` typically uses 3: "0.300 kg"; `piece` uses 0). |
| `created_at`, `updated_at` | timestamp | System timestamps. |

**Appended accessor** (always serialised): `storefront_name` — returns `short_name` when set, otherwise falls back to `name`. This is what storefront templates render.

Hidden on the model (not serialised): `child`, `main`.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `parent` | hasOne | units | n/a (read-only) | The parent unit in the conversion tree. NULL for top-level units. The model also defines a `child` relation for the inverse, but the schema hides it. |

## Filtering & sorting

**Allowed filtering parameters** — no named filters declared. All raw columns on `products_units` are auto-allowed (e.g. `filter[parent_id]=5`).

**Allowed sort parameters** — `id`. Prefix with `-` for descending. (Intentionally minimal — the catalog is small.)

**Allowed include paths** — `parent` (declared explicitly in the validator; the schema also lists it).

## Side effects on write

None — read-only endpoint. POST / PATCH / DELETE return 405.

The admin-panel flow on [[apps-grocery-store-overview-new]] has its own side-effects on unit edit / delete (the model's `deleting` hook NULLs `products.unit_id` + `variants.unit_id` for every reference AND cascade-deletes the unit's child unit), but those are not reachable through this resource. The platform pre-installs a default set of units on first activation via the platform code.

## Plan-feature gating

Requires the Grocery Store app installed on the merchant's plan. Without it, returns 404. See [[apps-grocery-store-overview-new]].

## Error examples

- App not installed:
  ```
  HTTP 404 Not Found
  {"errors":[{"status":"404","title":"Not Found","detail":"grocery_store app not installed"}]}
  ```
- POST / PATCH / DELETE attempted:
  ```
  HTTP 405 Method Not Allowed
  ```

## Example requests

Read-only — only GET is supported. All examples use `<store-host>` and `<YOUR_API_KEY>`. Requires the [[apps-grocery-store-overview-new|Grocery Store]] app.

### GET collection (sort, filter, sideload parent unit)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/units?page[size]=50&sort=id&include=parent"
```

Filter by parent (e.g., all child units of kilogram):

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/units?filter[parent_id]=1"
```

Top-level units only:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/units?filter[parent_id]=0"
```

### GET single (with parent)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/units/2?include=parent"
```

### Confirm app-install gate

```bash
# When the Grocery Store app is NOT installed, every request returns 404.
curl -s -o - -w "\nHTTP %{http_code}\n" \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/units"
```

### Blocked verbs (always return 405)

```bash
curl -s -X POST -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     "https://<store-host>/api/v2/units" \
     -d '{"data":{"type":"units","attributes":{"name":"ounce"}}}'
# HTTP 405 Method Not Allowed
```

## Example responses

### GET collection success (typical pre-installed defaults)

```json
{
  "data": [
    {
      "type": "units",
      "id": "1",
      "attributes": {
        "parent_id": null,
        "name": "kilogram",
        "short_name": "kg",
        "multiple_name": "kilograms",
        "steps": 1.00,
        "decimals": 3,
        "storefront_name": "kg",
        "created_at": "2026-01-01 00:00:00",
        "updated_at": "2026-01-01 00:00:00"
      },
      "relationships": { "parent": { "data": null } }
    },
    {
      "type": "units",
      "id": "2",
      "attributes": {
        "parent_id": 1,
        "name": "gram",
        "short_name": "g",
        "multiple_name": "grams",
        "steps": 1000.00,
        "decimals": 0,
        "storefront_name": "g",
        "created_at": "2026-01-01 00:00:00",
        "updated_at": "2026-01-01 00:00:00"
      },
      "relationships": { "parent": { "data": { "type": "units", "id": "1" } } }
    },
    {
      "type": "units",
      "id": "5",
      "attributes": {
        "parent_id": null,
        "name": "piece",
        "short_name": "piece",
        "multiple_name": "pieces",
        "steps": 1.00,
        "decimals": 0,
        "storefront_name": "piece"
      },
      "relationships": { "parent": { "data": null } }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 3, "total": 3, "last-page": 1 } }
}
```

### App not installed

```
HTTP 404 Not Found
{"errors":[{"status":"404","title":"Not Found","detail":"grocery_store app not installed"}]}
```

### Blocked verb

```
HTTP 405 Method Not Allowed
```

## Testing checklist

1. `GET /units` — confirm 200 when the [[apps-grocery-store-overview-new|Grocery Store]] app is installed; otherwise expect 404 `grocery_store app not installed`.
2. `GET /units?filter[parent_id]=0` — verify only top-level units (those with `parent_id == null`) come back.
3. `GET /units/{id}?include=parent` — verify the `parent` relationship resolves (or is `null` for a top-level unit).
4. `POST /units` — verify **405 Method Not Allowed**.
5. `PATCH /units/{id}` — verify **405**.
6. `DELETE /units/{id}` — verify **405**.
7. Use the `short_name` from any returned row as `unit_short_name` on a [[api-products|products]] POST/PATCH and confirm the platform resolves it into `unit_id` (the Grocery Store app must be installed).

## Equivalent UI

- [[apps-grocery-store-overview-new]] — install / activate the Grocery Store app to enable this endpoint. The admin UI manages the unit tree.
- [[apps-grocery-store-settings]] — settings + defaults.
- [[products-products]] — product edit form. The product's `unit_id` is set via the unit picker on this screen (when Grocery Store is installed).

## Related

- [[json-api-v2]] — protocol contract.
- [[apps-grocery-store-overview-new]] — the Grocery Store app (hard prerequisite).
- [[apps-grocery-store-settings]] — Grocery Store settings + defaults.
- [[api-products]] — product catalog. `products.unit_id` references this resource (the master per-product unit). Read-only on [[api-products]] — set indirectly via `unit_short_name` on POST/PATCH there.
- [[api-variants]] — variant catalog. `variants.unit_id` + `unit_value` reference this resource on the per-variant level.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Document the exact mapping between `unit_id` / `unit_value` on a variant and the rendered storefront label (e.g. "0.300 kg, 5.99 BGN" / "1 piece, 1.20 BGN"). Storefront rendering rules live in [[apps-grocery-store-overview-new]] business rules but the API exposes only the raw fields.
- Confirm whether the catalog is per-site or platform-wide (currently appears per-site since the model has no site filter in the adapter).
- Verify whether DELETE on a unit at the admin-panel level cascades to NULL-out `products.unit_id` / `variants.unit_id` (the `deleting` hook NULLs both) and whether this is observable through subsequent API reads.
