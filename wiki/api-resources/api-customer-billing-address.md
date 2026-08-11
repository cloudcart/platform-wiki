---
type: api-resource
resource_path: /api/v2/customer-billing-address
http_methods: [GET, POST, PATCH, DELETE]
related_entity: customer
related_features: [customers-details-billing-addresses, customers-details]
aliases: ["Customer Billing Address API", "JSON-API v2 customer-billing-address", "API адреси фактуриране", "/customer-billing-address"]
tags: [api, json-api-v2, customers, addresses, billing, vat]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Customer Billing Address (JSON-API v2)

## Purpose

Programmatic CRUD on a customer's billing-address book. Integrations use it to **import billing addresses** from a CRM / ERP / accounting system, **provision company / VAT data** for B2B customers, and **bulk-update billing details** before invoice generation.

A customer can have many billing addresses, but exactly one is the **default** (the customer's `default_billing_address_id`) — the default pre-fills as the invoice address at checkout. Billing addresses differ from shipping addresses by carrying **company name** + **VAT** fields. This endpoint manages the saved address book ONLY; for the per-order billing snapshot see [[api-order-billing-address]].

## Endpoint

- **URL base:** `/api/v2/customer-billing-address`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE (full CRUD), with one guard: **DELETE is blocked on the customer's default billing address** — HTTP 422 *"Cannot delete customer default billing address."*. Promote a different address first by PATCHing `default_billing_address_id` on the parent customer.
- **Custom routes:** none. **App requirements:** none beyond the base API key.

Auth, headers, content negotiation, pagination — see [[json-api-v2]] hub.

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `first_name` | string | yes | yes | yes (POST) | 2-191 chars. |
| `last_name` | string | yes | yes | yes (POST) | 2-191 chars. |
| `phone_country_iso2` | string | yes | yes | required with `phone` | Exactly 2 chars; ISO 3166-1 alpha-2. |
| `phone` | string | yes | yes | required with `phone_country_iso2` | National-format; validated against `phone_country_iso2`. Save hook derives `phone_international` / `phone_e164` / `phone_national` / `phone_rfc3966`. |
| `country_iso2` | string | yes | yes | yes (POST) | Exactly 2 chars; ISO 3166-1 alpha-2. Save hook auto-fills `country_iso3` + `country_name`. |
| `city_name` | string | yes | yes | yes (POST) | City. |
| `street_name` | string | yes | yes | yes (POST) | Street name. |
| `street_number` | string | yes | yes | no (validator commented out) | Street number. |
| `post_code` | string | yes | yes | no (validator commented out) | Post / ZIP code. |
| `state_name` | string | yes | yes | no | State / province. |
| `company_name` | string | yes | yes | **required with `company_vat`** | Company / legal-entity name for the invoice. |
| `company_vat` | string | yes | yes | **required with `company_name`** | VAT / tax-ID number. Triggers VIES validation at save-time for EU country codes (see Side effects). |

**Read-only attributes** (returned by GET, rejected with HTTP 422 on POST / PATCH): `customer_id` (set via the `customer` relationship); `country_name`, `country_iso3`, `state_iso2`, `geo_name_city_id`, `timezone`, `text`, `latitude`, `longitude` (derived on save); `phone_international`, `phone_e164`, `phone_national`, `phone_rfc3966` (derived from `phone` + `phone_country_iso2`); `full_name` (`first_name + last_name`).

**Always hidden from output** (noise reduction): `integration`, `country_id`, `state_id`, `city_id`, `quarter_id`, `quarter_name`, `street_id`, `office_id`, `office_name`, `marketplace_id`, `marketplace_name`, `address1`, `address2`, `address3`, `building`, `entrance`, `floor`, `apartment`, `city_ascii_name`, `neighborhood`, `locality`, the nested `quarter` / `office` / `marketplace` / `country` / `state` / `city` / `street` accessors, and the legacy `company` / `company_yes_no` / `company_bulstat` / `company_mol` accessors. The Bulgarian-market `company_bulstat` / `company_mol` are accepted on write but suppressed from output.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `customer` | hasOne | `customers` | yes (POST) | **Required at create.** The owning customer. See [[api-customers]]. |

## Filtering & sorting

- **Filter:** no custom `filter[*]` params are defined; all resource-table columns are auto-allowed, so `filter[id]`, `filter[customer_id]`, `filter[country_iso2]`, `filter[company_vat]`, etc. are accepted (equality-only, no comparison operators). To list one customer's addresses, prefer `GET /api/v2/customers/{id}?include=billing-addresses` over `filter[customer_id]` — the canonical pattern.
- **Sort:** `id` only (prefix `-` for descending); any other column returns 422.
- **Include:** `customer`. (The adapter's `includePaths` does NOT pre-load `customer`, so the `included[]` payload may be empty for nested-customer requests; fetch the parent via [[api-customers]] directly if needed.)

## Side effects on write

- **First-address auto-default** — a POST that creates the customer's first billing address writes the new ID to the customer's `default_billing_address_id`. Subsequent addresses do NOT promote — PATCH the customer to change the default.
- **Default billing address cannot be deleted** — DELETE on the address matching `default_billing_address_id` is rejected with HTTP 422 *"Cannot delete customer default billing address."*. Promote a different address first, then delete.
- **VIES VAT validation runs at save-time** — when `company_vat` is supplied for an EU country code, the platform calls the EU VIES service and caches the result for **7 days** in the address's `vies` JSON column. Invalid numbers fail validation; valid responses store the returned company name + address for reconciliation. See [[customer|Customer]] for the cache lifecycle.
- **`company_name` ↔ `company_vat` pair rule** — one without the other returns 422. If neither is supplied, the address is personal-billing (no VAT processing).
- **Save-time normalization** — when `country_iso2` is dirty, the save hook uppercases it, regenerates `country_iso3`, and re-resolves `country_name` for the store's display language; `text` is always rewritten to the canonical formatted-address string used in admin displays and invoice templates. Phone normalization follows the shipping-address pattern (see [[api-customer-shipping-address]]).
- **No order-snapshot cascade** — updating a saved billing address does NOT change existing orders; order billing-address records are snapshotted at order-create time (see [[order|Order]]).
- **No webhooks / audit trail** — there are no `customer-billing-address.*` events; listen to `customer.updated` for `default_billing_address_id` changes (see [[api-customers]], [[settings-hooks]]). There is no dedicated per-actor audit trail (unlike orders — see [[json-api-v2]]).
- **Invoice impact** — when this address is the default and the merchant generates an invoice, `company_name` / `company_vat` populate the invoice header. Validate VIES BEFORE the order is placed if downstream invoicing requires verified VAT.

## Plan-feature gating

No plan-feature cap specific to billing addresses; the parent `customers` gate applies indirectly. HTTP 402 Payment Required is emitted when the merchant's plan is expired or past-due (see [[json-api-v2]]); HTTP 403 is not emitted by this resource.

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
  "detail": "The company name field is required when company vat is present.", "source": { "pointer": "/data/attributes/company_name" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The company vat field is required when company name is present.", "source": { "pointer": "/data/attributes/company_vat" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "The customer field is required.", "source": { "pointer": "/data/relationships/customer" } }] }
```

```json
{ "errors": [{ "status": "422", "title": "Unprocessable Entity",
  "detail": "Cannot delete customer default billing address." }] }
```

Statuses 401 / 402 / 404 / 405 / 415 / 422 / 429 follow the canonical envelope on [[json-api-v2]].

## Example requests

### GET collection (filtered by customer)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-billing-address?filter[customer_id]=87&sort=id"
```

(Canonical alternative: `GET /api/v2/customers/87?include=billing-addresses`.)

### POST create — company billing (`company_name` + `company_vat` paired)

For personal billing, omit the `company_name` / `company_vat` pair.

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-billing-address" \
     -d '{
       "data": {
         "type": "customer-billing-address",
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
           "company_name": "Acme EOOD",
           "company_vat": "BG123456789"
         },
         "relationships": {
           "customer": { "data": { "type": "customers", "id": "87" } }
         }
       }
     }'
```

EU-prefixed `company_vat` triggers VIES validation (cached 7 days); a first address auto-promotes to `default_billing_address_id`.

### PATCH update (change street)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customer-billing-address/188" \
     -d '{
       "data": {
         "type": "customer-billing-address",
         "id": "188",
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
     "https://<store-host>/api/v2/customer-billing-address/188"
```

Rejected with HTTP 422 if `188` is still the `default_billing_address_id`.

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "customer-billing-address",
      "id": "188",
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
        "company_name": "Acme EOOD",
        "company_vat": "BG123456789",
        "text": "Acme EOOD (BG123456789), Ivan Petrov, Vitosha 12, 1000 Sofia, Bulgaria"
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
    "type": "customer-billing-address",
    "id": "188",
    "attributes": {
      "first_name": "Ivan",
      "last_name": "Petrov",
      "phone": "087 123 4567",
      "phone_country_iso2": "BG",
      "country_iso2": "BG",
      "country_iso3": "BGR",
      "country_name": "Bulgaria",
      "city_name": "Sofia",
      "street_name": "Vitosha",
      "street_number": "12",
      "post_code": "1000",
      "company_name": "Acme EOOD",
      "company_vat": "BG123456789",
      "text": "Acme EOOD (BG123456789), Ivan Petrov, Vitosha 12, 1000 Sofia, Bulgaria"
    }
  }
}
```

(After this create, `GET /api/v2/customers/87` shows `default_billing_address_id: 188` — auto-promotion.) For 422 envelopes see *Error examples* above.

## Equivalent UI

- [[customers-details-billing-addresses]] — per-customer billing-address sub-tab (GET filtered by `customer_id` + POST / PATCH / DELETE via the modal).
- [[customers-details]] — parent customer wrapper.

## Related

- [[json-api-v2]] — API hub.
- [[api-customers]] — parent customer (and the `default_billing_address_id` field).
- [[api-customer-shipping-address]] — shipping-address counterpart (separate book; no company / VAT fields).
- [[api-order-billing-address]] — per-order billing-address snapshot (read-only; distinct table).
- [[customer]] — customer entity reference.
- [[settings-hooks]] — `customer.updated` fires when `default_billing_address_id` changes.

## Open questions

- Whether non-EU country codes skip VIES entirely or use a different route (UK / Switzerland / Norway are not part of VIES).
- The exact shape of the cached `vies` JSON column — which fields a CRM can rely on for sync.
- Whether a force-revalidate flag (overriding the 7-day cache) is exposed to the API client, or cache invalidation is admin-only.
- Whether a VIES failure on save returns a hard 422 or a soft warning that still saves — affects integration error-handling.
