---
type: api-resource
resource_path: /api/v2/customer-shipping-address
http_methods: [GET, POST, PATCH, DELETE]
related_entity: customer
related_features: [customers-details-shipping-addresses, customers-details]
aliases: ["Customer Shipping Address API", "JSON-API v2 customer-shipping-address", "API адреси доставка", "/customer-shipping-address"]
tags: [api, json-api-v2, customers, addresses]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Customer Shipping Address (JSON-API v2)

## Purpose

Programmatic CRUD on a customer's shipping-address book. External integrations use this endpoint to **import shipping addresses** from a CRM / ERP, to **bulk-update post codes / phone numbers**, and to **delete stale addresses** during account cleanup.

A customer can have many shipping addresses, but exactly one is the **default** (referenced by the customer's `default_address_id`) — the default is what pre-fills at checkout. This endpoint manages the saved address book ONLY; for the per-order shipping snapshot see [[api-order-shipping-address]].

## Endpoint

- **URL base:** `/api/v2/customer-shipping-address`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE — full CRUD. DELETE is blocked when the address is the customer's default (HTTP 422; see *Side effects*).
- **Custom routes:** none. **App requirements:** none beyond the base API key.

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `first_name` | string | yes | yes | yes (POST) | 2-191 chars. |
| `last_name` | string | yes | yes | yes (POST) | 2-191 chars. |
| `phone_country_iso2` | string | yes | yes | yes (POST) | Exactly 2 chars; must be a valid ISO 3166-1 alpha-2 code. |
| `phone` | string | yes | yes | yes (POST) | National-format phone; validated against `phone_country_iso2`. On save, derives `phone_international`, `phone_e164`, `phone_national`, `phone_rfc3966`. |
| `country_iso2` | string | yes | yes | yes (POST) | Exactly 2 chars; ISO 3166-1 alpha-2. On save, auto-fills `country_iso3` + `country_name` (localised to the store language) when the value changes. |
| `city_name` | string | yes | yes | yes (POST) | City. |
| `street_name` | string | yes | yes | yes (POST) | Street name. |
| `street_number` | string | yes | yes | yes (POST) | Street number. |
| `post_code` | string | yes | yes | yes (POST) | Post / ZIP code. |
| `state_name` | string | yes | yes | no | State / province (free text). |

**Read-only attributes** (returned by GET, rejected with HTTP 422 on POST / PATCH):

- `customer_id` — set via the `customer` relationship, not the attribute.
- `country_name`, `country_iso3`, `state_iso2`, `geo_name_city_id`, `timezone` — derived / locale-resolved from `country_iso2`.
- `text` — the formatted address string (re-rendered on every save).
- `latitude`, `longitude` — geocoder output (when geocoding is enabled for the store).
- `phone_international`, `phone_e164`, `phone_national`, `phone_rfc3966` — derived from `phone` + `phone_country_iso2`.
- `full_name` — `first_name + last_name`.

**Always hidden from output** (noise reduction): `integration`, `country_id`, `state_id`, `city_id`, `quarter_id`, `quarter_name`, `street_id`, `office_id`, `office_name`, `marketplace_id`, `marketplace_name`, `address1`, `address2`, `address3`, `building`, `entrance`, `floor`, `apartment`, `city_ascii_name`, `neighborhood`, `locality`, plus the nested `quarter`, `office`, `marketplace`, `country`, `state`, `city`, `street`, `company`, `company_yes_no`, `company_name`, `company_vat` accessors.

A shipping address does NOT carry company-billing fields — those live on [[api-customer-billing-address]].

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `customer` | hasOne | `customers` | yes (POST) | **Required at create.** The owning customer. See [[api-customers]]. |

## Filtering & sorting

- **Filtering:** no custom `filter[*]` params are defined, but all resource-table columns are auto-allowed — `filter[id]`, `filter[customer_id]`, `filter[country_iso2]`, `filter[post_code]`, etc. (equality-only, no comparison operators). To list one customer's addresses, prefer `GET /api/v2/customers/{id}?include=shipping-addresses` over `filter[customer_id]` — the canonical pattern.
- **Sorting:** `id`, `customer_id`, `country_iso2`. Prefix with `-` for descending. Any other column returns 422.
- **Includes:** `customer`. The `included[]` payload may be empty for nested-customer requests; fetch the parent via [[api-customers]] directly if needed.
- **Pagination / auth / headers:** see [[json-api-v2]] hub.

## Side effects

- **First-address auto-default** — a POST that creates the customer's *first* shipping address writes the new ID to the customer's `default_address_id`. Subsequent addresses do NOT auto-promote — PATCH the customer to set a new default.
- **Default address cannot be deleted** — DELETE on the address matching `default_address_id` returns HTTP 422 *"Cannot delete customer default address."*. Promote a different address first, then delete.
- **Save-time normalization** — see the *Attributes* save-hook notes: `country_iso2` regenerates `country_iso3` + `country_name`; `phone` re-validates and refreshes the derived `phone_*` fields; every save rewrites `text` to the canonical formatted-address string.
- **No order-snapshot cascade** — editing a saved address does NOT change addresses on existing orders. Order addresses are snapshotted at order-create time (see [[order|Order]]) as independent records.
- **Webhooks** — no `customer-shipping-address.*` events. A default change writes `default_address_id` on the customer, which fires `customer.updated` — listen to that (see [[api-customers]], [[settings-hooks]]).
- **Audit log** — no dedicated per-actor trail for address writes.
- **Plan gating** — no cap specific to shipping addresses; the parent `customers` cap applies indirectly. HTTP 402 is emitted by the api2 layer when the plan is expired or past-due (see [[json-api-v2]]); 403 is not emitted here.

## Error examples (common 422 cases)

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The first name must be at least 2 characters.", "source": { "pointer": "/data/attributes/first_name" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The selected country iso2 is invalid.", "source": { "pointer": "/data/attributes/country_iso2" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The phone field is required.", "source": { "pointer": "/data/attributes/phone" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The phone field must be a valid number.", "source": { "pointer": "/data/attributes/phone" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The customer field is required.", "source": { "pointer": "/data/relationships/customer" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "Cannot delete customer default address." }] }
```

Other statuses (401 / 402 / 404 / 405 / 415 / 422 / 429) follow the canonical envelope on [[json-api-v2]].

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (filtered by customer)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-shipping-address?filter[customer_id]=87&sort=id"
```

(Canonical alternative: `GET /api/v2/customers/87?include=shipping-addresses`.)

### POST create — first address, auto-promoted to default

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-shipping-address" \
     -d '{
       "data": {
         "type": "customer-shipping-address",
         "attributes": {
           "first_name": "Ivan",
           "last_name": "Petrov",
           "phone_country_iso2": "BG",
           "phone": "087 123 4567",
           "country_iso2": "BG",
           "city_name": "Sofia",
           "street_name": "Vitosha",
           "street_number": "12",
           "post_code": "1000",
           "state_name": "Sofia-grad"
         },
         "relationships": {
           "customer": { "data": { "type": "customers", "id": "87" } }
         }
       }
     }'
```

When this is the customer's **first** shipping address, the new ID is automatically written to the customer's `default_address_id`. Subsequent addresses are NOT auto-promoted — set the default explicitly via the parent customer record afterwards.

### PATCH update (change street)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-shipping-address/311" \
     -d '{
       "data": {
         "type": "customer-shipping-address",
         "id": "311",
         "attributes": {
           "street_name": "Tsar Osvoboditel",
           "street_number": "8"
         }
       }
     }'
```

### DELETE

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-shipping-address/311"
```

Rejected with HTTP 422 if `311` is still the customer's `default_address_id` — promote a different address first.

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "customer-shipping-address",
      "id": "311",
      "attributes": {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "full_name": "Ivan Petrov",
        "phone": "087 123 4567",
        "phone_country_iso2": "BG",
        "phone_e164": "+359871234567",
        "phone_international": "+359 87 123 4567",
        "country_iso2": "BG",
        "country_iso3": "BGR",
        "country_name": "Bulgaria",
        "city_name": "Sofia",
        "street_name": "Vitosha",
        "street_number": "12",
        "post_code": "1000",
        "state_name": "Sofia-grad",
        "text": "Ivan Petrov, Vitosha 12, 1000 Sofia, Bulgaria"
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 10, "from": 1, "to": 1, "total": 1, "last-page": 1 }
  }
}
```

### POST 201 Created

```json
{
  "data": {
    "type": "customer-shipping-address",
    "id": "311",
    "attributes": {
      "first_name": "Ivan",
      "last_name": "Petrov",
      "full_name": "Ivan Petrov",
      "phone": "087 123 4567",
      "phone_country_iso2": "BG",
      "phone_e164": "+359871234567",
      "country_iso2": "BG",
      "country_iso3": "BGR",
      "country_name": "Bulgaria",
      "city_name": "Sofia",
      "street_name": "Vitosha",
      "street_number": "12",
      "post_code": "1000",
      "text": "Ivan Petrov, Vitosha 12, 1000 Sofia, Bulgaria"
    }
  }
}
```

(After this create, `GET /api/v2/customers/87` will show `default_address_id: 311` — first-address auto-promotion.)

### 422 — delete attempt on the default address

```
HTTP 422 Unprocessable Entity
{"errors":[{"status":"422","title":"Unprocessable Entity","detail":"Cannot delete customer default address."}]}
```

### Common failures

```
HTTP 401 Unauthorized
{"errors":[{"status":"401","title":"Unauthenticated"}]}
```

## Testing checklist

1. On a customer with no addresses, `POST /customer-shipping-address` (with `relationships.customer`) — capture `data.id`.
2. `GET /customers/{id}` — `default_address_id` should match the new ID (first-address auto-promotion).
3. `POST` a second address — `default_address_id` should be **unchanged**.
4. `DELETE` the first address — expect **422** *"Cannot delete customer default address."*.
5. Reassign the customer's default, then retry the `DELETE` — expect 204.
6. `PATCH` a `city_name` / `post_code` — verify `text` re-renders with the new values.

## Equivalent UI

- [[customers-details-shipping-addresses]] — the per-customer shipping-address sub-tab (mirrors GET filtered by `customer_id` + POST / PATCH / DELETE through the modal).
- [[customers-details]] — the parent customer wrapper.

## Related

- [[json-api-v2]] — API hub.
- [[api-customers]] — manage the parent customer (and the `default_address_id` field).
- [[api-customer-billing-address]] — the billing-address counterpart (separate book; carries the company / VAT fields).
- [[api-order-shipping-address]] — per-order shipping address snapshot (read-only; distinct table; NOT linked to this resource after order creation).
- [[customer]] — customer entity reference.
- [[settings-hooks]] — `customer.updated` fires when `default_address_id` changes.

## Open questions

- Whether the geocoder (latitude / longitude) runs synchronously on save or via a queued job — the address may be returned without coordinates immediately after POST.
- Whether the merchant-facing pickup-point picker data (Speedy / Econt / DPD office IDs) can be set via this endpoint, or whether the office-related hidden fields are populated only through the integration-specific picker UI at checkout.
