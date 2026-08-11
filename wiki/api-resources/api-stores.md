---
type: api-resource
resource_path: /api/v2/stores
http_methods: [GET]
related_entity: site
related_features: [apps-stores, apps-store-locations, apps-multilang-stores]
aliases: ["Stores API", "JSON-API v2 stores", "API магазини", "/stores", "Shops API", "Locations API"]
tags: [api, json-api-v2, multistore]
plan_gates: [stores]
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Stores (JSON-API v2)

## Purpose

A `stores` resource is one **physical store location / warehouse** the merchant has configured — a row in the `shops` table. These are the pickup points displayed on the storefront's "Locations" page and the warehouse anchors that multi-warehouse stock tracking ([[apps-store-locations]]) hangs stock off of. Each row carries the store's title, URL handle, SEO copy, address line, city, contact email / phone, working hours, GPS coordinates, optional video URL, and a `virtual` flag (which marks a non-physical "store" used as a logical inventory bucket).

This resource is **read-only on JSON-API v2** — physical store CRUD is admin-panel-only on [[apps-stores|Local Pickup (Stores)]]. The API enumerates the result so integrations can wire per-store stock writes via [[api-store-quantity]].

## Endpoint

- **URL base:** `<store-host>/api/v2/stores/`
- **GET collection** — `GET /api/v2/stores`.
- **GET single** — `GET /api/v2/stores/{id}`.
- **GET single by URL handle** — `GET /api/v2/stores?filter[url_handle]=<slug>` — adapter switches to single-record mode.
- **POST / PATCH / DELETE — NOT supported.** Route registered `readOnly` — those verbs return **405 Method Not Allowed**.
- No relationship endpoints declared in routes (the schema does declare `products` and `quantities` hasMany relations for sideloading — see Relationships).
- **App-install requirement:** the route is wrapped in `api_apps_installed:stores` middleware. Without the Stores app installed, every request returns **HTTP 404** with `"stores app not installed"`.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

All attributes are read-only — no PATCH/POST shape to validate. The serializer returns every column on the `shops` table:

| Attribute | Type | Notes |
|---|---|---|
| `id` | integer | Stable store identifier. Use this as the `shop_id` reference for [[api-store-quantity]] writes. |
| `address_id` | integer / null | FK to `customers_shipping_addresses` for the store's structured address. |
| `url_handle` | string | Unique URL slug — filterable as `filter[url_handle]`. |
| `title` | string | Merchant-visible store / warehouse name. |
| `seo_title` | string | SEO meta title for the public store page. |
| `seo_description` | text | SEO meta description. |
| `sort` | integer | Display order. Auto-incremented on create (admin path: `max(sort) + 1`). |
| `active` | tinyint | Whether the store is exposed publicly. |
| `city` | string | City name. |
| `address_text` | string | Free-text address line. |
| `video` | string | Optional video URL for the public store page. |
| `phone` | string | Contact phone. |
| `email` | string | Contact email. |
| `virtual` | string | Marks a virtual / non-physical "store" used as a logical inventory bucket by [[apps-store-locations]]. |
| `worktime` | text | Free-text working hours (see [[apps-stores]] for the structure). |
| `gps_lt` | decimal(15,8) | Latitude — cast to `float` by the model. |
| `gps_ll` | decimal(15,8) | Longitude — cast to `float`. |
| `created_at` / `updated_at` | timestamp | Standard timestamps. |

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `products` | hasMany | products | n/a (read-only) | Every product with at least one stock row at this store (joined through `products_quantities`). |
| `quantities` | hasMany | store-quantity | n/a (read-only) | The per-product / per-variant stock rows AT this store. The writable companion is [[api-store-quantity]]. |

Note: the route layer's `readOnly` registration does NOT expose `relationships(...)` declarations, but the schema does declare the two relationships above — so `?include=products` and `?include=quantities` are accepted as sideloads on the collection / single-resource endpoints.

## Filtering & sorting

**Allowed filtering parameters** — `filter[url_handle]` — `filled|alpha_dash`. When supplied, switches the adapter to single-record mode and returns one resource object. All raw columns on `shops` are auto-allowed (e.g., `filter[active]=1`, `filter[city]=Sofia`, `filter[virtual]=...`).

**Allowed sort parameters** — `id`, `title`, `sort`, `active`, `city`. Prefix with `-` for descending.

**Allowed include paths** — auto-allowed from schema: `products`, `quantities`.

## Side effects on write

None — read-only endpoint. POST / PATCH / DELETE return 405. The admin-panel flow on [[apps-stores]] has its own side-effects on store create / edit / delete (cascading the shop's address record and any shipping-provider-address rows referencing the shop as a marketplace), but those are not reachable through this resource.

## Plan-feature gating

Requires the Stores app installed on the merchant's plan. Without it, returns 404. See [[apps-stores]] for install / activation.

## Error examples

- App not installed:
  ```
  HTTP 404 Not Found
  {"errors":[{"status":"404","title":"Not Found","detail":"stores app not installed"}]}
  ```
- POST / PATCH / DELETE attempted:
  ```
  HTTP 405 Method Not Allowed
  ```

## Example requests

Read-only — only GET is supported. All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (sort, filter)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/stores?page[size]=20&sort=sort&filter[active]=1"
```

Filter by city:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/stores?filter[city]=Sofia"
```

Single-record lookup by URL handle:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/stores?filter[url_handle]=sofia-warehouse"
```

### GET single (with sideloaded stock rows)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/stores/2?include=quantities"
```

### Confirm app-install gate

```bash
# When the Stores app is NOT installed, every request returns 404.
curl -s -o - -w "\nHTTP %{http_code}\n" \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/stores"
```

### Blocked verbs (always return 405)

```bash
curl -s -X POST -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     "https://<store-host>/api/v2/stores" \
     -d '{"data":{"type":"stores","attributes":{"title":"New warehouse"}}}'
# HTTP 405 Method Not Allowed
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "stores",
      "id": "2",
      "attributes": {
        "address_id": 17,
        "url_handle": "sofia-warehouse",
        "title": "Sofia Warehouse",
        "seo_title": "Pick up in Sofia",
        "seo_description": "Free pickup at our Sofia warehouse.",
        "sort": 1,
        "active": 1,
        "city": "Sofia",
        "address_text": "ul. Tsar Boris III 100",
        "video": null,
        "phone": "+359 2 999 0000",
        "email": "sofia@example.com",
        "virtual": null,
        "worktime": "Mon-Fri 9-18; Sat 10-14",
        "gps_lt": 42.69774400,
        "gps_ll": 23.32184700,
        "created_at": "2026-01-15 12:00:00",
        "updated_at": "2026-04-22 09:30:00"
      },
      "relationships": {
        "products": { "data": [] },
        "quantities": { "data": [] }
      }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 } }
}
```

### App not installed

```
HTTP 404 Not Found
{"errors":[{"status":"404","title":"Not Found","detail":"stores app not installed"}]}
```

### Blocked verb

```
HTTP 405 Method Not Allowed
```

## Testing checklist

1. `GET /stores` — confirm 200 when the [[apps-stores|Stores]] app is installed; otherwise expect 404 `stores app not installed`.
2. `GET /stores?filter[active]=1` — verify the result is constrained to active stores.
3. `GET /stores?filter[url_handle]=<slug>` — verify the adapter switches to single-resource mode (returns one object, not a list).
4. `GET /stores/{id}?include=quantities` — verify per-store stock rows sideload as `included[]` of type `store-quantity`.
5. `POST /stores` — verify **405 Method Not Allowed**.
6. `PATCH /stores/{id}` — verify **405**.
7. `DELETE /stores/{id}` — verify **405**.

## Equivalent UI

- [[apps-stores]] — install / activate the Stores app to enable this endpoint. Manages physical-store CRUD (UI-only — the API is read-only).
- [[apps-store-locations]] — uses the same `shops` rows as multi-warehouse inventory anchors with geo-zone routing.
- [[apps-multilang-stores]] — adds per-language localisation to store titles + descriptions.
- [[site]] — the site / store-context entity (separate from a physical "shop" row).

## Related

- [[json-api-v2]] — protocol contract.
- [[apps-stores]] — admin UI equivalent (install + manage physical stores).
- [[apps-store-locations]] — geo-zone-driven warehouse routing built on the same `shops` rows.
- [[apps-multilang-stores]] — per-language localisation of store titles + descriptions.
- [[api-store-quantity]] — **the writable companion endpoint.** Per-store stock CRUD for multi-warehouse integrations.
- [[api-products]] — product catalog (the entities you push stock for).
- [[api-variants]] — per-variant master stock (single-warehouse merchants use this; multi-warehouse merchants use `api-store-quantity`).
- [[site]] — separate site / store-context entity.
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm whether the `url_handle` filter is case-sensitive in the single-record-mode lookup.
- The `quantities` hasMany relationship is declared on the schema but the route's `readOnly` registration does not configure relationship endpoints — verify whether `?include=quantities` is fully wired or limited to direct sideloads on the collection / single resource.
- Confirm if the `virtual` flag is filterable beyond the auto-allow-list (`filter[virtual]=...`) in practice (the queryRules only declares `url_handle` explicitly).
