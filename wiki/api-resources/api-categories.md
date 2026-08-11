---
type: api-resource
resource_path: /api/v2/categories
http_methods: [GET, POST, PATCH, DELETE]
related_entity: category
related_features: [products-categories, products-products]
aliases: ["Categories API", "JSON-API v2 categories", "API категории", "/categories"]
tags: [api, json-api-v2, products]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 4
---
# Categories (JSON-API v2)

## Purpose

A `categories` resource is one node in the merchant's category tree — the primary navigation backbone of the storefront and the foundation for storefront filtering. Each category carries name, URL handle, SEO copy, optional image / icon / color, parent pointer (for the tree), and the list of [[api-properties|properties]] attached to it (which controls which property filters appear on the category page and which property values become picker-able on products in this category).

Categories are unique among catalog resources in that they fire **all three lifecycle webhooks** on API writes (`category.created`, `category.updated`, `category.deleted`) — unlike [[api-products|products]], where only `product.deleted` fires from the API path.

## Endpoint

- **URL base:** `<store-host>/api/v2/categories/`
- **GET collection** — `GET /api/v2/categories`.
- **GET single** — `GET /api/v2/categories/{id}`.
- **POST** — `POST /api/v2/categories` — requires `name`.
- **PATCH** — `PATCH /api/v2/categories/{id}`.
- **DELETE** — `DELETE /api/v2/categories/{id}` — returns 204 on success (a subsequent GET then returns 404). On rejection (e.g. category still has child categories or products), returns 422 `Not Deletable` with the exception message in `detail`.
- **Relationship endpoints** — `GET / POST / PATCH / DELETE /api/v2/categories/{id}/relationships/<rel>` for `parent`, `properties`.
- No custom action routes.
- No app-install requirement.

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

| Attribute | Type | Writable POST | Writable PATCH | Required | Notes |
|---|---|---|---|---|---|
| `name` | string | yes | yes | **POST: required**, PATCH: optional | min 2 chars. |
| `url_handle` | string | yes | yes | no | `alpha_dash`, max 191 chars, **unique** across categories. Auto-generated from `name` when not provided. Changing it records a 301 redirect (see Side effects + [[marketing-seo-301-redirects]]). |
| `description` | text | yes | yes | no | Long description shown on the category page. |
| `order` | integer | yes | yes | no | Sort order among siblings. |
| `seo_title` | string | yes | yes | no | SEO title for the category page. |
| `seo_description` | string | yes | yes | no | SEO meta description. |
| `color` | varchar(7) | yes | yes | no | Hex color used in admin / menus. |
| `icon` | string | yes | yes | no | Icon identifier. |
| `icon_data` | text | yes | yes | no | Inline icon data (SVG / glyph metadata). |
| `image_url` | string | yes | yes | no | Validation: `url`. Remote URL downloaded server-side after save (see Side effects). Verify success by re-GETting the resulting `image` field. |
| `bnp_type_id` | integer | yes | yes | no | Buy-now-pay-later type linkage. |
| `ucf_cop` | string | yes | yes | no | UCF / COP commodity code. |
| `make_interval` | integer | yes | yes | no | Background-job interval setting. |
| `taxonomy_id` | bigint | yes | yes | no | External taxonomy linkage (Google Shopping, etc.). |
| `display_child` | tinyint (0/1) | yes | yes | no | Whether subcategories render as children on the parent page. |
| `background` | char(7) | yes | yes | no | Optional background color. |
| `parent_id` | — | — | — | — | **Read-only.** Set via the `parent` relationship. |
| `image` | — | — | — | — | **Read-only.** Internal storage path (set indirectly via `image_url` upload). |
| `max_thumb_size`, `width`, `height`, `image_processed` | — | — | — | — | **Read-only.** Image-pipeline metadata. |
| `seo_generated_through_spinner` | — | — | — | — | **Read-only.** Set by background SEO-spinner jobs (also hidden from output). |
| `created_at`, `updated_at` | — | — | — | — | **Read-only.** System timestamps. |
| `id`, `active`, `status` | — | — | — | — | **Hidden** in serialised output. |

**Appended accessor** (always serialised): `image_url` — the final image URL for storefront use.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `parent` | hasOne | categories | yes | Parent category in the tree. Use this relationship to move a category (do NOT try to PATCH `parent_id` — it is read-only). |
| `properties` | hasMany | properties | yes | Properties attached to this category — determines storefront filter facets + per-product property pickers (see [[category-property]]). Adding via the relationship endpoint is idempotent; existing links are skipped. |

## Filtering & sorting

**Allowed filtering parameters** — `filter[url_handle]` — `filled|alpha_dash`. When present, the response returns a single resource object. All category columns are also auto-allowed (e.g. `filter[parent_id]=5`, `filter[order]=10`).

**Allowed sort parameters** — `id`, `name`, `created_at`, `updated_at`, `order`. Prefix with `-` for descending.

**Allowed include paths** — auto-allowed from schema: `parent`, `properties`. Additional nested paths from validator: `properties.options`.

## Side effects on write

POST:
- **`category.created` webhook** fires — one of the few resources where API writes DO trigger the lifecycle webhook (see [[settings-hooks]]).
- **Image download** — if `image_url` is set, the image is fetched server-side after save; failures are **silently swallowed**.
- The category tree's ancestor index is rebuilt for the new node.

PATCH:
- **`category.updated` webhook** fires; image download behaves as for POST when `image_url` is supplied.
- **URL redirect history** — changing `url_handle` writes a 301 redirect (old → new) into the merchant's redirect history.
- The ancestor index is recomputed if `parent_id` changed (via the `parent` relationship).

DELETE:
- **`category.deleted` webhook** fires.
- **Delete guard** — a category with products cannot be deleted; violation returns 422 `Not Deletable` with the message (localized key `category.err.cannot_delete_category_has_products`).
- **Cascade** — ancestor-index rows and category restrictions are deleted.
- **Property pivots** — the category-to-property links are not auto-removed by this resource (verify by re-GETting properties).

**Audit log** — no dedicated change-log capture for categories beyond system timestamps. The actor identity is NOT recorded in a queryable way; the webhook payload includes the category's current state.

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (sort, filter by parent, sideload properties)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories?page[size]=50&sort=order&filter[parent_id]=0&include=parent,properties"
```

Single-record lookup by URL handle:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories?filter[url_handle]=shirts"
```

### GET single (with parent + properties.options)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories/1?include=parent,properties,properties.options"
```

### POST create (minimal)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories" \
     -d '{
       "data": {
         "type": "categories",
         "attributes": { "name": "Shirts" }
       }
     }'
```

### POST create (richer — child category with image)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories" \
     -d '{
       "data": {
         "type": "categories",
         "attributes": {
           "name": "T-Shirts",
           "url_handle": "t-shirts",
           "description": "All our T-shirts.",
           "order": 10,
           "seo_title": "T-Shirts | Design",
           "seo_description": "Browse all T-shirts.",
           "image_url": "https://cdn.example.com/category-images/tshirts.jpg",
           "color": "#000000",
           "display_child": 1
         },
         "relationships": {
           "parent": { "data": { "type": "categories", "id": "1" } }
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
     "https://<store-host>/api/v2/categories/15" \
     -d '{
       "data": {
         "type": "categories",
         "id": "15",
         "attributes": {
           "name": "T-Shirts (Updated)",
           "order": 5
         }
       }
     }'
```

### Move a category (use the `parent` relationship — `parent_id` is read-only)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories/15/relationships/parent" \
     -d '{ "data": { "type": "categories", "id": "3" } }'
```

### Attach a property to a category

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories/15/relationships/properties" \
     -d '{ "data": [{ "type": "properties", "id": "12" }] }'
```

### DELETE (blocked if the category has products)

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/categories/15"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "categories",
      "id": "15",
      "attributes": {
        "name": "T-Shirts",
        "url_handle": "t-shirts",
        "description": "All our T-shirts.",
        "order": 10,
        "seo_title": "T-Shirts | Design",
        "seo_description": "Browse all T-shirts.",
        "color": "#000000",
        "icon": null,
        "image_url": "https://cdn.cloudcart.com/<store>/categories/15.jpg",
        "display_child": 1,
        "background": null,
        "created_at": "2026-05-30 12:00:00",
        "updated_at": "2026-06-04 16:22:11"
      },
      "relationships": {
        "parent": { "data": { "type": "categories", "id": "1" } },
        "properties": { "data": [{ "type": "properties", "id": "12" }] }
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
    "type": "categories",
    "id": "22",
    "attributes": {
      "name": "Shirts",
      "url_handle": "shirts",
      "description": null,
      "order": 0,
      "seo_title": null,
      "seo_description": null,
      "color": null,
      "image_url": null,
      "display_child": 1,
      "created_at": "2026-06-05 11:06:00",
      "updated_at": "2026-06-05 11:06:00"
    },
    "relationships": {
      "parent": { "data": null }
    }
  }
}
```

### Common failures (422)

```
Missing required name on POST:
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The name field is required.","source":{"pointer":"/data/attributes/name"}}]}

DELETE blocked — category has products:
{"errors":[{"status":"422","title":"Not Deletable","detail":"You can not delete this category because it has products in it"}]}

image_url is not a valid image:
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"The content at https://example.com/foo.html is not a valid image file","source":{"pointer":"/data/attributes/image_url"}}]}
```

## Equivalent UI

- [[products-categories]] — manual category create / edit / delete / tree management.
- [[products-products]] — assigning categories to products.

## Related

- [[json-api-v2]] — protocol contract.
- [[products-categories]] — admin UI equivalent.
- [[category]] — full category entity reference.
- [[category-property]] — entity reference for the category-to-property pivot.
- [[api-properties]] — properties attached to categories.
- [[api-products]] — products assigned to categories.
- [[marketing-seo-301-redirects]] — where URL-handle changes write 301 redirects.
- [[apps-listing-engine]] — storefront filter / listing rebuild.
- [[settings-hooks]] — webhook subscriptions (subscribe to `category.created`, `category.updated`, `category.deleted`).
- [[settings-api-keys]] — authentication setup.

## Open questions

- Confirm the exact delete-blocking rules — the admin UI rule is "must have no products"; whether siblings / children also block is verified empirically only.
- Verify whether the `image_url` swallow extends to non-image responses (e.g. a 404 URL silently leaves the category imageless) or only to specific exceptions.
- Confirm cascade on `parent` change — moving a category with a subtree under a new parent; does the API re-validate `url_handle` uniqueness across the new siblings?
