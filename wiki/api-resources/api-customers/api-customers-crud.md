---
type: api-resource
resource_path: /api/v2/customers
http_methods: [GET, POST, PATCH, DELETE]
related_entity: customer
related_features: [customers, customers-details, customers-import, customers-export]
aliases: ["Customers API attributes", "Customers API CRUD", "Customer API fields", "JSON-API v2 customers attributes"]
tags: [api, json-api-v2, customers]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[api-customers]]. See the hub for the write-side pipeline (side effects) and the testing / UI-mapping aspect.

# Customers API — attributes, relationships & querying

## Purpose

This aspect is the **field reference** for the Customers JSON-API v2 resource: which attributes are writable on POST vs PATCH, which are read-only or hidden, which relationships can be set, and how a caller filters / sorts / includes when reading. For the consequences of a successful write (emails, webhooks, KPI recalc, delete cascade) see [[api-customers-side-effects]].

## Endpoint

- **URL base:** `/api/v2/customers`
- **HTTP methods:** GET (collection + single), POST, PATCH, DELETE (full CRUD).
- **Custom routes:** none.
- **App requirements:** none beyond the base API key. The `customers` plan-feature cap restricts how many customers (registered + guests) can exist on the store; POSTs that would exceed it return a plan-restriction error — see [[api-customers-side-effects]] and [[plan-vs-feature-pack]].

Auth, headers, content negotiation, pagination, rate limits, error envelope — see [[json-api-v2]] hub.

## Attributes

| Attribute | Type | Writable on POST? | Writable on PATCH? | Required? | Notes / validation |
|---|---|---|---|---|---|
| `email` | string | yes | yes | yes (POST) | Valid email, **unique** across customers, max 191 chars. PATCH that changes `email` stages the new value in `email_for_confirmation`, flips `email_confirmed → no`, and triggers a fresh confirmation email. The customer continues logging in with the OLD email until they confirm. |
| `first_name` | string | yes | yes | no | Free text; admin-form bound to 2-191 chars. |
| `last_name` | string | yes | yes | no | Free text; admin-form bound to 2-191 chars. |
| `alternative_phone` | string | yes | yes | no | Backup phone used for admin-side contact. |
| `password` | string | yes | yes | no | Plain-text input — hashed on save. Storefront password-change requires the old password; admin / API does NOT. |
| `active` | enum `yes` / `no` | yes | yes | no | Storefront login enabled / blocked. Past orders unaffected. |
| `banned` | enum `yes` / `no` | yes | yes | no | Disciplinary lock — blocks login AND order placement. Banning requires `banned_reason`; unban clears `banned`, `banned_reason`, `date_banned` together. |
| `banned_reason` | string | yes | yes | when `banned = yes` | Free text; preserved for audit. |
| `is_activated` | enum `yes` / `no` | yes | yes | no | Whether the account is activated. Affects whether the welcome email is sent on create. |
| `marketing` | enum `yes` / `no` | yes | yes | no | Customer-level marketing consent. Cascades to whether marketing campaign sends include this customer (see [[notification-delivery]]). |
| `newsletter` | enum `yes` / `no` | yes | yes | no | Legacy newsletter flag. |
| `email_confirmed` | enum `yes` / `no` | yes | yes | no | Whether the email is verified. The admin / API CAN set this directly (skipping the confirmation-link flow). |
| `email_for_confirmation` | string | yes | yes | no | Pending new email awaiting confirmation. Set automatically by the email-change re-confirmation flow above. |
| `note` | string | yes | yes | no | Admin-only internal note. NEVER visible to the customer. |
| `timezone_id` | integer | yes | yes | no | FK to the platform's timezones table. |
| `imported` | enum `yes` / `no` | yes | yes | no | Flag for customers brought in via the bulk-import wizard ([[customers-import]]). |

**Read-only attributes** (returned by GET, rejected with HTTP 422 on POST / PATCH):

- `group_id` — set via the `group` relationship, not the attribute.
- `default_address_id`, `default_billing_address_id` — managed automatically when shipping / billing addresses are created (see [[api-customer-shipping-address]] / [[api-customer-billing-address]]).
- `date_added` — created-at timestamp.
- `updated_at` — last-modified timestamp.
- `date_banned` — written automatically when `banned = yes`; cleared on unban.

**Always hidden from output** (security): `epay_one_touch`, `stripe`, `mypos`, `remember_token`. Saved-payment-gateway tokens and the persistent-login token are never exposed via this API.

**Aggregate KPI columns** (returned but maintained by a queued income-recalc job — see [[api-customers-side-effects]]): `income`, `completed_orders`, `orders_total`, `orders_total_price`, `last_order_date`, `income_updated_at`. PATCHing them is technically possible (they are fillable on the model) but will be overwritten on the next order-status change that triggers the recalc.

## Relationships

| Name | Type | Target | Writable | Notes |
|---|---|---|---|---|
| `group` | hasOne | `customer-groups` | yes | Set at POST (auto-fills the **Default** group if omitted). PATCH may reassign. See [[api-customer-groups]]. |
| `shipping-address` | hasOne | `customer-shipping-address` | read-only | The default shipping address (mirrors `default_address_id`). |
| `billing-address` | hasOne | `customer-billing-address` | read-only | The default billing address (mirrors `default_billing_address_id`). |
| `orders` | hasMany | `orders` | read-only | The customer's full order history. |
| `shipping-addresses` | hasMany | `customer-shipping-address` | read-only | All shipping addresses. Manage rows individually via [[api-customer-shipping-address]]. |
| `billing-addresses` | hasMany | `customer-billing-address` | read-only | All billing addresses. Manage rows individually via [[api-customer-billing-address]]. |

**Allowed include paths:** `group`, `orders`, `shipping-address`, `shipping-addresses`, `billing-address`, `billing-addresses`. Combining with dot notation for nested includes is NOT supported on this resource — only the top-level relationships above.

## Filtering & sorting

**Allowed filtering parameters**

- `filter[email]` — must be a filled, valid email. **Triggers single-record mode** (returns one customer wrapped as a single-resource response, not a list). Useful for the common "look up customer by email" integration step.
- **All resource-table columns** are auto-allowed as filters by the framework (default JSON-API v2 behaviour) — for example `filter[id]`, `filter[group_id]`, `filter[active]`, `filter[banned]`, `filter[imported]`. Equality-only — no comparison operators. Comma-separated / array-style multi-value support varies per column.

**Allowed sort parameters:** `id`, `first_name`, `last_name`, `email`, `date_added`, `updated_at`, `date_banned`. Prefix with `-` for descending (e.g. `sort=-date_added`). Multi-sort with comma: `sort=-date_added,id`. Sorting on any other column returns 422.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection (single-record mode via email)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customers?filter[email]=test@example.com"
```

(returns a single resource object — NOT a one-element array — because `filter[email]` is the single-record-mode filter.)

Regular paginated list:

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customers?page[size]=10&page[number]=1&sort=-date_added&filter[active]=yes"
```

### GET single (with all default includes)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customers/87?include=group,orders,shipping-addresses,billing-addresses"
```

### POST create (minimal required-only)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customers" \
     -d '{
       "data": {
         "type": "customers",
         "attributes": {
           "first_name": "Ivan",
           "last_name": "Petrov",
           "email": "test@example.com"
         }
       }
     }'
```

(no `group` relationship → auto-assigned to the **Default** group.)

### POST create (richer payload + group relationship)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customers" \
     -d '{
       "data": {
         "type": "customers",
         "attributes": {
           "first_name": "Ivan",
           "last_name": "Petrov",
           "email": "ivan.petrov@example.com",
           "alternative_phone": "+359 87 123 4567",
           "password": "TempPass!2026",
           "active": "yes",
           "is_activated": "yes",
           "email_confirmed": "yes",
           "marketing": "yes",
           "newsletter": "yes",
           "note": "VIP — imported from CRM batch 2026-06"
         },
         "relationships": {
           "group": { "data": { "type": "customer-groups", "id": "4" } }
         }
       }
     }'
```

### PATCH update (change phone)

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/customers/87" \
     -d '{ "data": { "type": "customers", "id": "87",
       "attributes": { "alternative_phone": "+359 88 765 4321" } } }'
```

## Example responses

### GET collection success

```json
{
  "data": [
    { "type": "customers", "id": "87",
      "attributes": {
        "first_name": "Ivan", "last_name": "Petrov", "email": "ivan.petrov@example.com",
        "active": "yes", "banned": "no", "is_activated": "yes", "email_confirmed": "yes",
        "marketing": "yes", "newsletter": "yes", "imported": "no",
        "income": 24580, "completed_orders": 3, "orders_total": 4, "orders_total_price": 31250,
        "last_order_date": "2026-05-21 14:33:02",
        "date_added": "2025-11-04 08:21:11", "updated_at": "2026-06-04 12:00:09" },
      "relationships": { "group": { "data": { "type": "customer-groups", "id": "4" } } } }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 10, "from": 1, "to": 10, "total": 412, "last-page": 42 } }
}
```

### GET single success (with includes)

```json
{
  "data": {
    "type": "customers", "id": "87",
    "attributes": {
      "first_name": "Ivan", "last_name": "Petrov", "email": "ivan.petrov@example.com",
      "default_address_id": 311, "default_billing_address_id": 188 },
    "relationships": {
      "group": { "data": { "type": "customer-groups", "id": "4" } },
      "shipping-addresses": { "data": [{ "type": "customer-shipping-address","id": "311"}] },
      "billing-addresses": { "data": [{ "type": "customer-billing-address", "id": "188"}] },
      "orders": { "data": [{ "type": "orders", "id": "9821"}] } }
  },
  "included": [
    { "type": "customer-groups", "id": "4", "attributes": { "name": "VIP" } },
    { "type": "customer-shipping-address","id": "311", "attributes": { "city_name": "Sofia", "post_code": "1000", "country_iso2": "BG" } },
    { "type": "customer-billing-address", "id": "188", "attributes": { "city_name": "Sofia", "post_code": "1000", "country_iso2": "BG", "company_name": "Acme EOOD", "company_vat": "BG123456789" } }
  ]
}
```

## Side effects

This aspect is field-shape only. Every successful POST / PATCH / DELETE runs the full business pipeline (welcome / confirmation emails, group auto-assignment, `customer.*` webhooks, KPI denormalization, delete cascade, plan-cap enforcement) — see [[api-customers-side-effects]].

## Equivalent UI

- [[customers]] — list / search / header create (the UI source of the same attributes).
- [[customers-details-overview]] — overview tab where these attributes + stats are edited.

Full UI-to-API mapping (import, export, password-set, impersonation) — see [[api-customers-testing]].

## Related

- [[api-customers]] — hub.
- [[json-api-v2]] — API hub: auth, rate limit, error envelope, pagination.
- [[customer]] — full customer attribute reference and lifecycle rules.
- [[api-customer-groups]] — group dictionary (assignable via the `group` relationship).
- [[api-customer-shipping-address]] — per-customer shipping addresses (manage `default_address_id` from here).
- [[api-customer-billing-address]] — per-customer billing addresses.
- [[api-orders]] — read-only order history (via the `orders` relationship).

## Open questions

- Whether `?include=group.customers` or other nested include paths are silently ignored or return 422 — only the top-level relationships are listed in the resource's allow-list.
- Whether the `is_activated` flag accepts the string `yes` / `no` or the integer `1` / `0` at the API layer when the field is not in the explicit cast list.
