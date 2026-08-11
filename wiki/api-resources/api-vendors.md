---
type: api-resource
resource_path: /api/v2/vendors
http_methods: [GET, POST, PATCH, DELETE]
related_entity: vendor
related_features: [products-vendors, products-products]
aliases: ["Vendors API", "JSON-API v2 vendors", "API производители", "/vendors"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Vendors (JSON-API v2)

## Purpose

A `vendors` resource is one row in the merchant's brand / manufacturer / vendor catalog — a name + SEO copy + logo image. Each product references at most one vendor via the product's `vendor` relationship (see [[api-products]]). On the storefront, vendors feed the brand filter, the brand-page route (`/vendor/<url_handle>`), the brand-page SEO metadata, and the brand badge on individual product pages.

This is the catalog of available vendors; the per-product link lives on the product, not here.

## Endpoint

- **URL base:** `<store-host>/api/v2/vendors/`
- **GET collection** — `GET /api/v2/vendors`.
- **GET single** — `GET /api/v2/vendors/{id}`.
- **POST** — `POST /api/v2/vendors` — requires `name`.
- **PATCH** — `PATCH /api/v2/vendors/{id}`.
- **DELETE** — `DELETE /api/v2/vendors/{id}`. **Blocked** if any product still references this vendor (see Side effects).
- No relationship endpoints — this resource declares no relationships in its schema.
- No custom action routes.
- No app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **POST: required**, PATCH: optional | min 2 chars. |
| `url_handle` | string | yes | yes | no | `alpha_dash`, max 191 chars, **unique** across vendors. Feeds the storefront brand route `/vendor/<url_handle>`. |
| `description` | text | yes | yes | no | Long description shown on the brand page. |
| `seo_title` | string | yes | yes | no | SEO title for the brand page. |
| `seo_description` | string | yes | yes | no | SEO meta description. |
| `image_url` | string | yes | yes | no | Validation: `url`. Remote logo URL — downloaded server-side after save. **Failures are silently swallowed**. The validator also probes the URL to confirm it points at an actual image and rejects non-images with 422 before the upload step. |
| `background` | char(7) | yes | yes | no | Optional background color. |
| `image` | — | — | — | — | **Read-only.** Internal storage path (set indirectly via `image_url`). |
| `max_thumb_size`, `width`, `height`, `image_processed` | — | — | — | — | **Read-only.** Image-pipeline metadata. |
| `seo_generated_through_spinner` | — | — | — | — | **Read-only / hidden.** Set by background SEO-spinner jobs. |
| `created_at`, `updated_at` | — | — | — | — | **Read-only.** System timestamps. |

**Appended accessor** (always serialised): `image_url` — final image URL for storefront use.

## Relationships

None declared. The vendor-to-product linkage is owned by the product resource — see [[api-products]] `vendor` relationship.

## Filtering & sorting

**Allowed filtering parameters** — `filter[url_handle]` — `filled|alpha_dash`. Triggers single-record mode. Every field on the vendor record is auto-allowed as a filter key (e.g. `filter[name]=...`).

**Allowed sort parameters** — `id`, `name`, `created_at`, `updated_at`. Prefix with `-` for descending.

**Allowed include paths** — none (no relationships in the schema).

## Side effects on write

POST + PATCH:
- **Image download** — when `image_url` is supplied, the upload runs after save. Failures are swallowed silently. Verify by re-GETting and checking the resulting `image_url`.
- **URL-validity probe** — before save, the validator confirms `image_url` points at an actual image and returns 422 `The content at <url> is not a valid image file` for invalid resources.
- **No `vendor.created` / `vendor.updated` webhook from the API path** — the platform's `vendor.created` / `vendor.updated` events fire only from the admin-panel save path, not from the record-save lifecycle the API uses. Integrations should NOT rely on these webhooks firing for API writes.

DELETE:
- **Delete guard** — deletion is blocked (localized message key `vendor.err.cannot_delete_vendor_has_products`) when any product still references the vendor. The API surfaces this as **HTTP 422**.
- **`vendor.deleted` webhook DOES fire** — the delete event is unconditional; subscribers in [[settings-hooks]] receive `vendor.deleted`.

**Audit log** — no dedicated change-log capture beyond model timestamps.

## Plan-feature gating

None.

## Error examples (common 422 cases)

- Missing required `name` on POST:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The name field is required.","source":{"pointer":"/data/attributes/name"}}]}
  ```
- DELETE blocked because the vendor has products:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"You can not delete this vendor because it has products"}]}
  ```
- `image_url` is not a valid image:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The content at https://example.com/foo.html is not a valid image file","source":{"pointer":"/data/attributes/image_url"}}]}
  ```

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (sort, filter)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/vendors?page[size]=50&sort=name"
```

Single-record lookup by URL handle:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/vendors?filter[url_handle]=nike"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/vendors/3"
```

### POST create (minimal)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/vendors" \
     -d '{
       "data": {
         "type": "vendors",
         "attributes": { "name": "Acme Apparel" }
       }
     }'
```

### POST create (richer — with logo + SEO)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/vendors" \
     -d '{
       "data": {
         "type": "vendors",
         "attributes": {
           "name": "Acme Apparel",
           "url_handle": "acme-apparel",
           "description": "Premium activewear.",
           "seo_title": "Acme Apparel | Design",
           "seo_description": "Shop Acme Apparel collection.",
           "image_url": "https://cdn.example.com/brands/acme-logo.png",
           "background": "#f5f5f5"
         }
       }
     }'
```

### PATCH update (rename / change SEO)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/vendors/3" \
     -d '{
       "data": {
         "type": "vendors",
         "id": "3",
         "attributes": { "seo_title": "Acme — Activewear" }
       }
     }'
```

### DELETE (blocked while any product references the vendor)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/vendors/3"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "vendors",
      "id": "3",
      "attributes": {
        "name": "Acme Apparel",
        "url_handle": "acme-apparel",
        "description": "Premium activewear.",
        "seo_title": "Acme Apparel | Design",
        "seo_description": "Shop Acme Apparel collection.",
        "image_url": "https://cdn.cloudcart.com/<store>/vendors/3.png",
        "background": "#f5f5f5",
        "width": 300,
        "height": 120,
        "image_processed": 1,
        "created_at": "2026-04-21 09:00:00",
        "updated_at": "2026-06-04 10:11:12"
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
    "type": "vendors",
    "id": "11",
    "attributes": {
      "name": "Acme Apparel",
      "url_handle": "acme-apparel",
      "description": null,
      "seo_title": null,
      "seo_description": null,
      "image_url": null,
      "background": null,
      "created_at": "2026-06-05 11:07:00",
      "updated_at": "2026-06-05 11:07:00"
    }
  }
}
```

### Common failures

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The name field is required.","source":{"pointer":"/data/attributes/name"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"You can not delete this vendor because it has products"}]}
```

## Testing checklist

1. `GET /vendors?page[size]=5&sort=name` — confirm 200.
2. `POST /vendors` with `{"name":"<unique-name>"}` — capture returned id.
3. `GET /vendors/{id}` — verify the resource exists.
4. `PATCH /vendors/{id}` with `{"attributes":{"seo_title":"New title"}}` — confirm 200.
5. `POST /vendors` without `name` — verify 422 with pointer `/data/attributes/name`.
6. `POST /vendors` with `image_url = "https://example.com/index.html"` — verify 422 `not a valid image file`.
7. `DELETE /vendors/{id}` (while no product references it) — verify 204.
8. `GET /vendors/{id}` — verify 404.

## Equivalent UI

- [[products-vendors]] — manual vendor list / create / edit / delete.
- [[products-products]] — selecting a vendor on the product create / edit form.
- [[vendor]] — full vendor attribute reference.

## Related

- [[json-api-v2]] — protocol contract.
- [[products-vendors]] — admin UI equivalent.
- [[vendor]] — full vendor entity reference.
- [[api-products]] — products reference a vendor via their `vendor` relationship.
- [[api-categories]] — sibling catalog resource.
- [[settings-hooks]] — webhook subscriptions (only `vendor.deleted` fires reliably for API writes).
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm whether `vendor.created` / `vendor.updated` should fire at the record-save layer so API writes can subscribe; current behaviour fires them only from the admin code path.
- Confirm whether `image_url` swallowing extends to non-image responses (e.g. a 404 URL silently leaves the vendor logoless).
- Verify whether `url_handle` changes produce a 301 redirect entry (the admin side does, and the API path appears to inherit the same behaviour).
