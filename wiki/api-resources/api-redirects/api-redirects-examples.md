---
type: api-resource
resource_path: /api/v2/redirects
http_methods: [GET, POST, PATCH, DELETE]
related_entity: seo-redirect
related_features: [marketing-seo-301-redirects, apps-domain-redirect]
aliases: ["Redirects API examples", "redirects curl examples", "redirects POST example", "redirects testing checklist", "redirects JSON response"]
tags: [api, json-api-v2, content, seo]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Redirects API — examples & testing checklist

> Part of [[api-redirects]]. See the hub for the other aspects (attributes & relationship, side effects & plan gating).

## Purpose

This aspect collects **worked curl requests and JSON responses** for every common operation on the redirects resource — list, filter, create an entity-typed rule, create a plain URL→URL rule, update a destination, and delete — plus the **end-to-end CRUD testing checklist** an integrator runs to confirm a fresh integration. For the attribute / filter reference these payloads use, see [[api-redirects-attributes]]; for what each write triggers behind the scenes, see [[api-redirects-side-effects]].

## Endpoint

All examples use `<store-host>` and `<YOUR_API_KEY>`. **Every rule is 301 (permanent)** — the API does not expose 302 / temporary redirects, so a filter by status code is N/A here (all rows are 301).

- **URL base:** `<store-host>/api/v2/redirects`
- **Methods covered here:** GET, POST, PATCH, DELETE.

Base URL, auth, headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

The payloads below set `redirect_type`, `old_url`, `new_url`, and the `item` relationship. For the full writable / read-only attribute table, see [[api-redirects-attributes]].

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/redirects?page[size]=50&include=item"
```

To list only entity-typed product redirects:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/redirects?filter[location]=product"
```

(`location` is the internal column name for `redirect_type` — the auto-merged column filter described in [[api-redirects-attributes]].)

### POST polymorphic `item` — product target

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/redirects" \
     -d '{
       "data": {
         "type": "redirects",
         "attributes": {
           "redirect_type": "product",
           "old_url": "/old-shoes/sneaker-v1"
         },
         "relationships": {
           "item": { "data": { "type": "products", "id": "412" } }
         }
       }
     }'
```

`item` targets are polymorphic — substitute the relationship target for any allowed type: `products`, `categories`, `vendors`, `blogs` (Blog Categories — see [[api-blogs]]), or `posts` (Blog Articles — see [[api-posts]]). `redirect_type` must match the relationship target (`product` → `products`, `category` → `categories`, etc.).

### POST plain URL → URL (no `item`)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/redirects" \
     -d '{
       "data": {
         "type": "redirects",
         "attributes": {
           "redirect_type": "manual",
           "old_url": "/promo/spring",
           "new_url": "/promo/summer"
         }
       }
     }'
```

Use `redirect_type: "external"` to redirect off the current store host — `new_url` may be a full URL like `https://other-domain.com/page`. If the scheme is missing, the platform auto-prepends `http://` (see the parsing side effect in [[api-redirects-side-effects]]).

### PATCH change destination

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/redirects/88" \
     -d '{
       "data": {
         "type": "redirects",
         "id": "88",
         "attributes": {
           "new_url": "/promo/autumn"
         }
       }
     }'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/redirects/88"
```

(Returns 204. Saving the last redirect flips the site setting `has_301_redirects` to `false`, which disables the redirect middleware entirely on the storefront — saving a DB query per request until the next rule is created. See [[api-redirects-side-effects]].)

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "redirects",
      "id": "88",
      "attributes": {
        "redirect_type": "manual",
        "old_url": "/promo/spring",
        "new_url": "/promo/summer",
        "full_new_url": "https://<store-host>/promo/summer"
      }
    },
    {
      "type": "redirects",
      "id": "92",
      "attributes": {
        "redirect_type": "product",
        "old_url": "/old-shoes/sneaker-v1",
        "new_url": null,
        "full_new_url": "https://<store-host>/product/sneaker-v2"
      },
      "relationships": {
        "item": { "data": { "type": "products", "id": "412" } }
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 2, "total": 2, "last-page": 1 }
  }
}
```

### GET single success

```json
{
  "data": {
    "type": "redirects",
    "id": "88",
    "attributes": {
      "redirect_type": "manual",
      "old_url": "/promo/spring",
      "new_url": "/promo/summer",
      "full_new_url": "https://<store-host>/promo/summer"
    }
  }
}
```

### POST 201 Created — product target

```json
{
  "data": {
    "type": "redirects",
    "id": "92",
    "attributes": {
      "redirect_type": "product",
      "old_url": "/old-shoes/sneaker-v1",
      "new_url": null,
      "full_new_url": "https://<store-host>/product/sneaker-v2"
    },
    "relationships": {
      "item": { "data": { "type": "products", "id": "412" } }
    }
  }
}
```

### 422 — `old_url` path conflict (already taken)

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","source":{"pointer":"/data/attributes/old_url"},"detail":"The old url has already been taken"}]}
```

### 422 — `redirect_type = product` without `item` relationship

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","source":{"pointer":"/data/relationships/item"},"detail":"The item field is required unless redirect type is in manual, external"}]}
```

The full table of 422 conditions is in [[api-redirects-side-effects]].

## Relationships

The product-target examples above exercise the polymorphic `item` relationship. For its cardinality, allowed target types, and the `redirect_type`-must-match rule, see [[api-redirects-attributes]].

## Filtering & sorting

The `filter[location]=product` and `include=item` query parameters in the GET examples above are the practical filter / include forms. For the full filter / sort / include reference (auto-merged column filters, sortable columns), see [[api-redirects-attributes]].

## Side effects

Step 5 of the checklist below depends on the `redirects301` cache flush firing on save, and step 6 depends on the `has_301_redirects` flip on delete — both documented in [[api-redirects-side-effects]].

## Testing checklist

1. `GET /redirects` — confirm read. (May return an empty list — that's a valid state.)
2. `POST /redirects` with `redirect_type=product` + polymorphic `item` relationship targeting a real product — capture `data.id`.
3. `POST /redirects` plain `redirect_type=manual` rule with `old_url` + `new_url` (no `item`).
4. `PATCH /redirects/{id}` — change `new_url`.
5. Hit `https://<store-host><old_url>` from a clean session — verify the storefront actually serves a 301 to the configured target. (The `redirects301` cache is flushed on every save.)
6. `DELETE /redirects/{id}` — expect 204. Deleting the last rule flips `has_301_redirects` to `false` (storefront middleware short-circuits future requests).

## Equivalent UI

- [[marketing-seo-301-redirects]] — the admin create/edit modal produces the same rows these examples create; a rule created via the API appears in that list and vice-versa.
- [[apps-blog-csv-import]] — CSV import that auto-creates the same kind of redirect rows for renamed blog content.

## Related

- [[api-redirects]] — hub.
- [[json-api-v2]] — API hub: auth headers, status codes, pagination `meta.page` shape.
- [[api-redirects-attributes]] — attribute table + the `filter[location]` / `include=item` reference these examples use.
- [[api-redirects-side-effects]] — what the POST / PATCH / DELETE examples trigger (cache flush, `has_301_redirects` flip).
- [[api-products]] — entity target used in the product-redirect POST example.
- [[api-blogs]] / [[api-posts]] — other polymorphic `item` targets.
- [[marketing-seo-301-redirects]] — admin UI mirror.
- [[settings-api-keys]] — where to obtain `<YOUR_API_KEY>`.

## Open questions

- Add a worked example of replacing the `item` target via the dedicated relationship endpoint `/api/v2/redirects/{id}/relationships/item` once the request shape is verified end-to-end.
