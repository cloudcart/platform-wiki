---
type: api-resource
resource_path: /api/v2/images
http_methods: [GET, POST, DELETE]
related_features: [products-products, products-variants-options]
aliases: ["Images API", "JSON-API v2 images", "API снимки", "/images"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Images (JSON-API v2)

## Purpose

An `images` resource is one row in the merchant's product image gallery — the file metadata for a single image attached to a product. Each row references its parent product (`parent_id`), holds the storage identifier (`image_id`), sort order, optional gallery grouping, and the resized-thumbnail set produced by the async image pipeline. The actual file bytes live on object storage; this resource exposes the database row and URLs only.

Integrations use this endpoint to **upload images for new products** (from a remote URL or as base64 data), to **delete obsolete images**, and to **list a product's image gallery**. Image rows can be attached to per-variant gallery slots via the [[api-variants]] `images` relationship (subject to the "variant must have at least one option" guard).

## Endpoint

- **URL base:** `<store-host>/api/v2/images/`
- **GET collection** — `GET /api/v2/images` — list with sort / page.
- **GET single** — `GET /api/v2/images/{id}`.
- **POST** — `POST /api/v2/images` — requires `src` + the `product` relationship.
- **PATCH** — **NOT supported.** The route is registered with `except('update')` — there is no `PATCH /api/v2/images/{id}`. To replace an image, POST a new one and DELETE the old one. Calls to PATCH return **405 Method Not Allowed**.
- **DELETE** — `DELETE /api/v2/images/{id}`.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/images/{id}/relationships/product`.
- No custom action routes.
- No app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `src` | string | yes | n/a (no PATCH) | **POST: required** | Must be a valid URL **or** a valid base64 image (data-URI form `data:image/...;base64,...` or raw base64). SVG (`image/svg+xml`) is **explicitly blocked**. Allowed MIME types: `image/jpeg`, `image/jpg`, `image/png`, `image/gif`, `image/webp` (per `image.allowed_mimetypes` config). When the value is a URL, the validator calls `exif_imagetype` on the remote resource to confirm it's an image. |
| `name` | string | yes | n/a | no | Image display name. Auto-generated on create as `<slugified-product-name>-<uniqid>` when not provided. |
| `sort_order` | integer | yes | n/a | no | Position in the product's image gallery. |
| `active` | enum `yes`/`no` | yes | n/a | no | Whether the image is shown on the storefront. Database default `yes`. |
| `gallery_id` | integer | yes | n/a | no | Gallery grouping for multi-gallery products. |
| `video_url` | string | yes | n/a | no | Optional video URL associated with the image slot. |
| `background` | char(7) | yes | n/a | no | Optional dominant background color. |
| `image_id` | — | — | — | — | **Read-only.** Storage key auto-assigned as `uniqid("image_")` on create. |
| `parent_id` | — | — | — | — | **Read-only.** The parent product ID — set via the `product` relationship. |
| `last_edited`, `date_added` | — | — | — | — | **Read-only.** System timestamps. |
| `max_thumb_size`, `width`, `height`, `thumbs` | — | — | — | — | **Read-only.** Populated by the async image-processing pipeline — may be empty in the response immediately after POST. |
| `type` | — | — | — | — | **Hidden** in serialised output (internal discriminator). |
| `id` | — | — | — | — | **Hidden** in serialised output (replaced by JSON:API `id`). |

**Appended accessors** (always serialised): `src` (final CDN URL after upload), `thumbs` (map of named thumbnail sizes to URLs).

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `product` | hasOne | products | **required at POST** | The parent product. |

## Filtering & sorting

**Allowed filtering parameters** — no named filters. All raw columns on `images__products` are auto-allowed (e.g. `filter[parent_id]=123`, `filter[active]=yes`, `filter[gallery_id]=5`).

**Allowed sort parameters** — `id`, `name`, `date_added`, `last_edited`, `sort_order`, `parent_id`. Prefix with `-` for descending.

**Allowed include paths** — auto-allowed from schema: `product`.

## Side effects on write

POST:
- **Asynchronous storage upload** — the `creating` hook assigns `image_id = uniqid("image_")`. The `created` hook either downloads from the URL (`uploadFileFromUrlNow($src)`) or decodes the base64 payload (`uploadFileFromBase64`). Thumbnail generation runs in the background — `width`, `height`, `thumbs` may be empty in the immediate response.
- **Filename derivation** — when `name` is omitted, the platform stores it as `<slugified-product-name>-<uniqid>` (slug capped at 155 chars).
- **URL probe** — when `src` is a URL, the validator calls `exif_imagetype($src)` and returns 422 `The content at <url> is not a valid image file` for non-images / unreachable URLs.
- **Base64 validation** — base64 payloads are decoded and passed through `imagecreatefromstring`. SVG MIME-types are rejected explicitly. Invalid base64 returns 422 `The src must be a valid URL or base64 image string.`
- **Audit log** — image creation contributes to the parent product's change log (via the standard observer chain); the actor is recorded as `api` with the request IP.

DELETE:
- Removes the image row + scheduled storage cleanup.
- The parent product's `image_id` is NOT auto-reassigned if you delete the default image — the product is left without a default until the merchant reassigns one.

**Webhooks:** no dedicated `image.*` event in the platform catalogue. Image changes do not trigger `product.updated` from the API (that event is gated to admin-UI saves — see [[api-products]]).

## Plan-feature gating

None on the endpoint itself. Image-count limits may apply per plan (see [[plan-vs-feature-pack]]).

## Error examples (common 422 cases)

- Invalid `src`:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The src must be a valid URL or base64 image string.","source":{"pointer":"/data/attributes/src"}}]}
  ```
- URL doesn't return an image:
  ```json
  {"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The content at https://example.com/not-an-image.html is not a valid image file","source":{"pointer":"/data/attributes/src"}}]}
  ```
- PATCH attempted:
  ```
  HTTP 405 Method Not Allowed
  ```

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (filter by parent product, sort)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/images?page[size]=20&sort=sort_order&filter[parent_id]=42&filter[active]=yes&include=product"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/images/501?include=product"
```

### POST create (from remote URL)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/images" \
     -d '{
       "data": {
         "type": "images",
         "attributes": {
           "src": "https://cdn.example.com/photos/tshirt-front.jpg",
           "sort_order": 1,
           "active": "yes"
         },
         "relationships": {
           "product": { "data": { "type": "products", "id": "42" } }
         }
       }
     }'
```

### POST create (base64 data URI)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/images" \
     -d '{
       "data": {
         "type": "images",
         "attributes": {
           "src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
           "name": "white-pixel",
           "sort_order": 99,
           "background": "#ffffff"
         },
         "relationships": {
           "product": { "data": { "type": "products", "id": "42" } }
         }
       }
     }'
```

### PATCH — NOT supported (returns 405)

```bash
# Will return: HTTP 405 Method Not Allowed.
# To "edit" an image: POST a new one + DELETE the old one.
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     "https://<store-host>/api/v2/images/501" \
     -d '{"data":{"type":"images","id":"501","attributes":{"sort_order":5}}}'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/images/501"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "images",
      "id": "501",
      "attributes": {
        "parent_id": 42,
        "image_id": "image_64a1f2e7b3c1d",
        "name": "cotton-t-shirt-64a1f2e7b3c1d",
        "sort_order": 1,
        "active": "yes",
        "gallery_id": null,
        "video_url": null,
        "background": null,
        "last_edited": "2026-06-01 09:13:01",
        "date_added": "2026-06-01 09:13:01",
        "width": 1200,
        "height": 1600,
        "max_thumb_size": "1600",
        "src": "https://cdn.cloudcart.com/<store>/products/image_64a1f2e7b3c1d.jpg",
        "thumbs": {
          "small": "https://cdn.cloudcart.com/<store>/products/image_64a1f2e7b3c1d_small.jpg",
          "medium": "https://cdn.cloudcart.com/<store>/products/image_64a1f2e7b3c1d_medium.jpg",
          "large": "https://cdn.cloudcart.com/<store>/products/image_64a1f2e7b3c1d_large.jpg"
        }
      },
      "relationships": {
        "product": { "data": { "type": "products", "id": "42" } }
      }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 } }
}
```

### POST 201 Created (thumbs may still be empty — background pipeline)

```json
{
  "data": {
    "type": "images",
    "id": "612",
    "attributes": {
      "parent_id": 42,
      "image_id": "image_6566aa11bb223",
      "name": "cotton-t-shirt-6566aa11bb223",
      "sort_order": 1,
      "active": "yes",
      "date_added": "2026-06-05 11:05:00",
      "last_edited": "2026-06-05 11:05:00",
      "src": "https://cdn.cloudcart.com/<store>/products/image_6566aa11bb223.jpg",
      "thumbs": []
    },
    "relationships": {
      "product": { "data": { "type": "products", "id": "42" } }
    }
  }
}
```

### Common failures

```
HTTP 405 Method Not Allowed
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The content at https://example.com/not-an-image.html is not a valid image file","source":{"pointer":"/data/attributes/src"}}]}
```

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The src must be a valid URL or base64 image string.","source":{"pointer":"/data/attributes/src"}}]}
```

## Testing checklist

1. `GET /images?filter[parent_id]={product_id}&page[size]=5` — confirm 200.
2. `POST /images` with a valid remote `src` URL — capture returned id.
3. `GET /images/{id}` — verify `parent_id` matches the product; `thumbs` may be empty immediately after create (re-GET after a few seconds to see them).
4. `PATCH /images/{id}` — confirm **405 Method Not Allowed**.
5. `POST /images` with `src = "https://example.com/index.html"` — verify 422 `not a valid image file`.
6. `POST /images` with `src = "data:image/svg+xml;base64,..."` — verify 422 (SVG blocked).
7. `DELETE /images/{id}` — verify 204.
8. `GET /images/{id}` — verify 404.

## Equivalent UI

- [[products-products]] — image upload via the product edit form's image gallery.
- [[products-variants-options]] — per-variant image attach (handled via [[api-variants]]).

## Related

- [[json-api-v2]] — protocol contract.
- [[products-products]] — admin UI equivalent (the product edit form's image gallery).
- [[api-products]] — parent product resource (`image` / `images` relationships expose these rows).
- [[api-variants]] — per-variant image attachment.
- [[product]] — product entity reference.
- [[settings-api-keys]] — authentication setup.
- [[settings-hooks]] — webhook subscriptions.

## Open questions

- Confirm the maximum allowed base64 payload size — large images may hit PHP `post_max_size` / `upload_max_filesize` before the validator runs.
- Verify whether `sort_order` is editable via the parent product's `images` relationship endpoint, given PATCH is unsupported on the resource directly.
- Confirm whether image deletion triggers immediate CDN invalidation or only on the next product cache flush.
