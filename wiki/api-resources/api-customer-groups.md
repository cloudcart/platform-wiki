---
type: api-resource
resource_path: /api/v2/customer-groups
http_methods: [GET, POST, PATCH, DELETE]
related_entity: customer-group
related_features: [customers-custom-groups, customers]
aliases: ["Customer Groups API", "JSON-API v2 customer-groups", "API клиентски групи", "/customer-groups"]
tags: [api, json-api-v2, customers]
plan_gates: ["customer_groups"]
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Customer Groups (JSON-API v2)

## Purpose

Programmatic CRUD on the merchant's customer-group dictionary — loyalty tiers, B2B / wholesale buckets, VIP groups. External integrations use this endpoint to **provision groups from a CRM / ERP** before bulk-assigning customers, to **rename groups**, and to **delete empty groups** as part of a cleanup pipeline.

The group itself is a label; the actual differentiated behaviour (pricing, payment-method visibility, shipping-method visibility, segment membership) lives on the entities that reference the group — see [[customer-group|Customer Group entity]] for the full downstream reach.

## Endpoint

- **URL base:** `/api/v2/customer-groups`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE (full CRUD), with two important guards:
  - **PATCH is blocked on the reserved "Default" and "Guests" groups** — returns HTTP 422 *"Customer group `<name>` is not editable!"*.
  - **DELETE is blocked when the group has customers or referencing discounts** — returns HTTP 422 with the matching message (see *Error examples* below).
- **Custom routes:** none.
- **App requirements:** none beyond the base API key. The `customer_groups` plan-feature key caps how many custom groups the merchant can create.

Auth, headers, content negotiation, pagination — see [[json-api-v2]] hub.

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `name` | string | yes | yes (except on reserved groups) | yes (POST) | **Unique** per store; max 191 chars; **"Default" is reserved** and rejected by the model on create. Empty / duplicate values fail validation with the standard 422 envelope. |

The record has NO `created_at` / `updated_at` columns — only `id` and `name` are stored. The customers count is a derived view (the `customers` relationship), not a stored attribute.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `customers` | hasMany | `customers` | read-only | Customers assigned to this group. Eager loading via `?include=customers` is not wired in the adapter; use [[api-customers]] with `filter[group_id]=<id>` to list members. |

## Allowed filtering parameters

- `filter[name]` — must be a filled string. **Triggers single-record mode** (returns one group matching the name).
- **All resource-table columns** are auto-allowed by the framework — for `customer-groups` that effectively means `filter[id]` and `filter[name]`.

## Allowed sort parameters

- `id`
- `name`

Prefix with `-` for descending (e.g. `sort=-name`). Sorting on any other column returns 422.

## Allowed include paths

`customers`.

(Declared by the schema and merged into the validator's allow-list — but the adapter's `includePaths` array currently does NOT pre-load the relationship, so the included payload may need a follow-up GET via [[api-customers]] in practice.)

## Side effects on write

- **Reserved groups are immutable AND undeletable via this endpoint** — **"Default"** (registered-customer default) and **"Guests"** (the system group every guest checkout falls into). PATCH on either returns HTTP 422 *"Customer group `<name>` is not editable!"*. DELETE on either is rejected by the same bulk-remove path the admin UI uses.
- **Delete blocking on referential integrity** — DELETE returns HTTP 422 in two scenarios:
  - The group still has assigned customers — *"Cannot delete a customer group with customers"*. Bulk-reassign every customer to another group first (via [[api-customers]] PATCH or the bulk-action on [[customers]]).
  - The group is referenced by any [[discount|Discount]] — *"Cannot delete a customer group with discounts"*. Edit each referencing discount to remove the group ID from its customer-group list before deleting.
- **No downstream cascades on rename** — discounts, payment providers, shipping methods, segments, and customers all reference the group by `id`, not by name, so a PATCH that renames the group does NOT require updates to referencing records.
- **Webhooks** — there are no `customer-group.*` webhook events. Group changes do not fire customer-level webhooks either.
- **Audit log** — group changes are recorded with the standard `created_at` / `updated_at` semantics inherited from the model. There is no dedicated per-actor audit trail for customer-group writes (unlike orders, which capture `namespace = "api2"` — see [[json-api-v2]]).

## Plan-feature gating

- **`customer_groups` plan-feature cap** — total number of custom groups the merchant can create. POST that would exceed the cap returns a 422 with a plan-restriction message (the admin UI shows *"Group limit reached"*).
- **HTTP 402 Payment Required** is emitted by the api2 layer when the merchant's plan is expired or past-due — see [[json-api-v2]]. HTTP 403 is not emitted by this resource.

## Filtering & sorting

See the *"Allowed filtering parameters"* and *"Allowed sort parameters"* subsections above.

## Error examples (common 422 cases)

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The name field is required.", "source": { "pointer": "/data/attributes/name" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The name has already been taken.", "source": { "pointer": "/data/attributes/name" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Not Editable",
  "detail": "Customer group Default is not editable!" }] }
```

```json
{ "errors": [{ "status": "422", "title": "Not Deletable",
  "detail": "Cannot delete a customer group with customers" }] }
```

```json
{ "errors": [{ "status": "422", "title": "Not Deletable",
  "detail": "Cannot delete a customer group with discounts" }] }
```

Other statuses (401 / 402 / 404 / 405 / 415 / 422 / 429) follow the canonical envelope on [[json-api-v2]].

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-groups?page[size]=20&sort=name"
```

Single-record lookup by name (returns one resource object, not a collection):

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-groups?filter[name]=VIP"
```

### POST create

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-groups" \
     -d '{
       "data": {
         "type": "customer-groups",
         "attributes": {
           "name": "Wholesale-2026"
         }
       }
     }'
```

### PATCH rename

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-groups/12" \
     -d '{
       "data": {
         "type": "customer-groups",
         "id": "12",
         "attributes": {
           "name": "Wholesale-Q3-2026"
         }
       }
     }'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-groups/12"
```

(Deletes only when the group is **not Default / not Guests**, has **no assigned customers**, and is **not referenced by any discount**. Bulk-reassign customers via [[api-customers]] PATCH first, and edit referencing discounts to drop the group-ID, before retrying.)

## Example responses

### GET collection success

```json
{
  "data": [
    { "type": "customer-groups", "id": "1", "attributes": { "name": "Default" } },
    { "type": "customer-groups", "id": "2", "attributes": { "name": "Guests" } },
    { "type": "customer-groups", "id": "4", "attributes": { "name": "VIP" } },
    { "type": "customer-groups", "id": "12", "attributes": { "name": "Wholesale-2026" } }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 4, "total": 4, "last-page": 1 }
  }
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "customer-groups",
    "id": "12",
    "attributes": { "name": "Wholesale-2026" }
  }
}
```

(Note: no `created_at` / `updated_at` are stored on this resource.)

### 422 — delete attempt on reserved Default group

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Not Editable","detail":"Customer group Default is not editable!"}]}
```

### 422 — delete attempt on group with customers

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Not Deletable","detail":"Cannot delete a customer group with customers"}]}
```

### 422 — delete attempt on group referenced by a discount

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Not Deletable","detail":"Cannot delete a customer group with discounts"}]}
```

### Common failures

```
HTTP 401 Unauthorized
{"errors":[{"status":"401","title":"Unauthenticated"}]}
```

## Testing checklist

1. `GET /customer-groups?sort=name` — confirm **Default** and **Guests** appear in the list.
2. `POST /customer-groups` with `{"attributes":{"name":"Test-Group-2026"}}` — capture `data.id`.
3. `PATCH /customer-groups/{id}` with `{"attributes":{"name":"Test-Group-Renamed"}}` — confirm 200.
4. `PATCH /customer-groups/1` (the Default group) — expect 422 *"Customer group Default is not editable!"*.
5. `POST /customers` with `relationships.group` pointing at the new group — confirm 201.
6. `DELETE /customer-groups/{id}` while a customer is still attached — expect 422 *"Cannot delete a customer group with customers"*.
7. Reassign the customer (`PATCH /customers/{id}` setting `group` to the Default group), then retry DELETE — expect 204.
8. Optional: attach the group to a [[api-discounts|discount]], retry DELETE — expect 422 *"Cannot delete a customer group with discounts"*.

## Equivalent UI

- [[customers-custom-groups]] — manual create / rename / delete of groups (the merchant-facing page).
- [[customers]] — bulk-action *"Set group"* modal (mirrors PATCH on `customers` with the `group` relationship, NOT this endpoint).

## Related

- [[json-api-v2]] — API hub.
- [[api-customers]] — assign a customer to a group via the `group` relationship.
- [[customer-group]] — full group entity reference (downstream discount-eligibility / payment-method / shipping-method gating rules).
- [[customer]] — customers consume the group via `group_id`.
- [[plan-vs-feature-pack]] — `customer_groups` plan-feature gating and pack purchases.
- [[settings-hooks]] — webhook subscriptions (no `customer-group.*` events are defined, but customer-level events fire from [[api-customers]] writes).

## Open questions

- Whether the reserved-name check (`Default` / `Guests`) is locale-sensitive — stores in non-English locales may display translated labels while the underlying check is case-insensitive against the English literals.
- Whether `?include=customers` actually returns the membership list in `included[]` despite the adapter's commented-out `includePaths`, or whether the validator's allow-merge is the only enforcement and the include resolves to an empty payload.
