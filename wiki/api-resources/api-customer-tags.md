---
type: api-resource
resource_path: /api/v2/customer-tags
http_methods: [GET, POST, PATCH, DELETE]
related_entity: customer
related_features: [customers, customers-details]
aliases: ["Customer Tags API", "JSON-API v2 customer-tags", "API етикети клиенти", "/customer-tags"]
tags: [api, json-api-v2, customers, tags]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Customer Tags (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's customer-tag dictionary. Customer tags are **free-form labels** the merchant attaches to customers for segmentation, filtering, and admin-side organisation (e.g. *"VIP"*, *"Tech-savvy"*, *"Sofia office"*, *"Wholesale-prospect"*).

Tags differ from [[customer-group|Customer Groups]] in two ways: tags are **many-per-customer**, and tags carry **no behavioural side effects** (no pricing, no payment / shipping gating) — they exist purely as merchant-controlled labels for filtering and segment-builder conditions. External integrations use this endpoint to **provision a controlled tag vocabulary** before tagging customers in bulk via the admin UI or via the inline `tags` string on [[api-customers]].

## Endpoint

- **URL base:** `/api/v2/customer-tags`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE (full CRUD).
- **Custom routes:** none.
- **App requirements:** none beyond the base API key.

Auth, headers, content negotiation, pagination — see [[json-api-v2]] hub.

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `tag` | string | yes | yes | yes (POST — non-empty) | The display label. The bulk-assignment flow on [[api-customers]] caps the tag string at **191 chars** when assigning a comma-separated list. |
| `url_handle` | string | yes (echoed; not in model fillable) | yes (echoed; not in model fillable) | no | URL-safe slug used for filter URLs and segment-condition references. Model fillable is restricted to `tag` only — `url_handle` rides through validation but may be ignored on save depending on the model's mass-assignment policy. |

The resource has **no explicit attribute validation rules** at the v2 layer — validation lives in the model layer. The model-level check rejects POST when `tag` is empty.

## Relationships

This resource has **no relationships** exposed via JSON-API v2. The customer ↔ tag link is tracked in a separate pivot table (`tags__customers__items`) populated through the admin-panel bulk-tag flow on [[customers-details]] (and the parsing path inside the customer's create flow when a `tags` comma-separated string is supplied on POST).

To attach a tag to a customer programmatically, use the **inline `tags` string** on [[api-customers]] POST / PATCH — direct pivot-row manipulation is not exposed via v2.

## Allowed filtering parameters

- **No custom `filter[*]` parameters are defined** on this resource.
- **All resource-table columns** are auto-allowed by the framework — so `filter[id]`, `filter[tag]`, `filter[url_handle]` are accepted (equality-only).

## Allowed sort parameters

- `tag`
- `url_handle`

Prefix with `-` for descending. Sorting on any other column returns 422.

## Allowed include paths

None — the schema declares no relationships.

## Side effects on write

- **Empty-tag rejection on POST** — POST with an empty `tag` attribute is rejected before the row is inserted. Integrations should validate non-empty client-side before POSTing.
- **No referential blocking on delete** — DELETE removes the tag definition; existing customer ↔ tag pivot rows for this tag are dropped from the merchant's filterable view, but historical orders and audit records that mention the tag string by name remain in place.
- **No order-snapshot cascade** — tags are not snapshotted onto orders. Deleting a tag does not affect any order record.
- **Webhooks** — there are no `customer-tag.*` webhook events. Tag changes do not fire `customer.updated` either, unless the change is also accompanied by a customer save (e.g. when [[api-customers]] POST carries a `tags` string and the resulting customer save triggers `customer.created`).
- **Audit log** — there is no dedicated per-actor audit trail for tag writes (unlike orders, which capture `namespace = "api2"` — see [[json-api-v2]]).

## Plan-feature gating

- **No plan-feature cap** specific to customer tags. Tags are not plan-gated.
- **HTTP 402 Payment Required** is emitted by the api2 layer when the merchant's plan is expired or past-due — see [[json-api-v2]]. HTTP 403 is not emitted by this resource.

## Filtering & sorting

See the *"Allowed filtering parameters"* and *"Allowed sort parameters"* subsections above.

## Error examples (common 422 cases)

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The sort parameter is invalid.", "source": { "parameter": "sort" } }] }
```

For the empty-`tag` POST short-circuit, the response surface is currently a raw connection terminate at the controller layer rather than the standard 422 JSON-API envelope — integrations should validate non-empty client-side to avoid the ambiguous response.

Other statuses (401 / 402 / 404 / 405 / 415 / 422 / 429) follow the canonical envelope on [[json-api-v2]].

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-tags?page[size]=50&sort=tag"
```

### POST create

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-tags" \
     -d '{
       "data": {
         "type": "customer-tags",
         "attributes": {
           "tag": "VIP",
           "url_handle": "vip"
         }
       }
     }'
```

(`url_handle` is echoed back but the model fillable is restricted to `tag` only — explicit `url_handle` may be ignored depending on the mass-assignment policy.)

### PATCH rename

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-tags/7" \
     -d '{
       "data": {
         "type": "customer-tags",
         "id": "7",
         "attributes": {
           "tag": "VIP-Tier-1"
         }
       }
     }'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-tags/7"
```

No referential blocking — DELETE drops the tag definition AND the customer ↔ tag pivot rows for this tag. Check the dictionary usage in [[customers]] filter pill first to avoid surprising the merchant.

## Example responses

### GET collection success

```json
{
  "data": [
    { "type": "customer-tags", "id": "5", "attributes": { "tag": "Sofia office", "url_handle": "sofia-office" } },
    { "type": "customer-tags", "id": "7", "attributes": { "tag": "VIP", "url_handle": "vip" } },
    { "type": "customer-tags", "id": "9", "attributes": { "tag": "Wholesale-prospect","url_handle": "wholesale-prospect" } }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 3, "total": 3, "last-page": 1 }
  }
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "customer-tags",
    "id": "7",
    "attributes": {
      "tag": "VIP",
      "url_handle": "vip"
    }
  }
}
```

### Common failures

```
HTTP 401 Unauthorized
{"errors":[{"status":"401","title":"Unauthenticated"}]}
```

```
HTTP 404 Not Found
{"errors":[{"status":"404","title":"Not Found"}]}
```

(Empty-`tag` POST short-circuits at the controller layer before producing a standard 422 envelope — validate non-empty client-side.)

## Testing checklist

1. `GET /customer-tags?sort=tag` — confirm 200 and the current tag dictionary.
2. `POST /customer-tags` with `{"attributes":{"tag":"Test-Tag-2026"}}` — capture `data.id`.
3. `PATCH /customer-tags/{id}` with `{"attributes":{"tag":"Test-Tag-Renamed"}}` — confirm 200.
4. Tag a customer by `POST /customers` (or `PATCH`) with an `attributes.tags` comma-separated string that includes `"Test-Tag-Renamed"` — the customer save attaches the matching tag-dictionary row via the pivot table.
5. `GET /customers/{customer-id}` and verify the tag appears in the customer's tag list (via the admin UI panel — there is no JSON-API relationship endpoint for the pivot).
6. `DELETE /customer-tags/{id}` — expect 204. Verify the tag is gone from [[customers]] filter pill and the customer no longer carries the label.

## Equivalent UI

- [[customers]] — the customer list's filter pill exposes the tag vocabulary for filtering.
- [[customers-details]] — the tag-edit modal on the customer detail view (assigns tags from the dictionary or adds new ones inline).

## Related

- [[json-api-v2]] — API hub.
- [[api-customers]] — manage customers (and the comma-separated `tags` string on POST / PATCH for the inline-assign flow).
- [[customer]] — customer entity reference (the *"belongs to many tags"* relationship).
- [[customer-group]] — distinct concept: groups are exactly-one-per-customer and carry behaviour; tags are many-per-customer and label-only.
- [[settings-hooks]] — no `customer-tag.*` events are defined; `customer.*` events fire from [[api-customers]] writes.

## Open questions

- Whether tags can be attached / detached to a specific customer via a JSON-API relationship endpoint (e.g. `/api/v2/customers/{id}/relationships/tags`) or whether the only programmatic path is the inline `tags` string on [[api-customers]] POST / PATCH.
- Whether the platform deduplicates tag dictionary entries (case-insensitive uniqueness?) or whether duplicate POSTs of the same `tag` create duplicate rows.
- The `url_handle` auto-generation rule — whether POST without `url_handle` auto-slugifies `tag`, or whether `url_handle` is left null until explicitly set.
- The exact HTTP response surface of the empty-`tag` short-circuit — raw connection drop vs. structured error — affects integration retry / error-handling.
