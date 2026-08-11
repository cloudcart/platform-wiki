---
type: api-resource
resource_path: /api/v2/order-billing-address
http_methods: [GET]
related_entity: order
related_features: [orders-details, orders-address-edit, orders-invoice]
aliases: ["Order billing address API", "Invoice address API", "JSON-API v2 order-billing-address", "/order-billing-address"]
tags: [api, json-api-v2, orders, addresses]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Order Billing Address (JSON-API v2)

## Purpose

The `order-billing-address` resource is the **read-only view of the billing (invoice) address on every order** — the customer's name, optional company details (name, VAT, registration number, responsible person), postal address, and country. External integrations use it to populate accounting / invoicing systems with the correct invoice recipient, validate VAT numbers against tax-zone rules, and surface billing context in ERP dashboards.

The billing address is captured at storefront checkout (separately from the shipping address when the customer ticks "Bill to different address") and can be edited via the admin-panel [[orders-address-edit]] flow. It is not modifiable through this API endpoint.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-billing-address` | List every order billing address. |
| `GET` | `/api/v2/order-billing-address/{id}` | Fetch a single billing address. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-billing-address[/{id}]` | **GET only — returns 405 Method Not Allowed.** To edit an order's billing address, the merchant uses [[orders-address-edit]] in the admin panel. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=billing-address` on [[api-orders]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `first_name`, `last_name` | string | Invoice recipient name. |
| `phone` | string | Contact phone. |
| `company_name` | string | Company name (when invoicing a business). |
| `company_vat` | string | Company VAT number (used for VAT-exempt cross-border B2B sales — see [[tax-computation]]). |
| `company_person` (appended) | string | Responsible person on the invoice. |
| `company_registration_number` (appended) | string | Company registration number (Bulgarian EIK, etc.). |
| `country_iso2` / `country_name` | string | ISO 3166-1 alpha-2 + localised name snapshot. |
| `city_name` | string | City. |
| `state_name`, `state_iso2` | string | State / region (when applicable). |
| `street_name` + `street_number` | string | Street address fields. |
| `post_code` | string | Postal code. |
| `formatted` (appended) | string | Pre-rendered display string. |

**Hidden by default** (these store JSON payloads of the original mapping data; surfaced through the typed accessors above instead): `address`, `country`, `city`, `state`, `street`.

**Sparse-field append values:** none configured — `company_person`, `company_registration_number`, `formatted` are appended by default.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |

**Allowed include paths:** `order`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column, e.g., `filter[order_id]=123`, `filter[country_iso2]=BG`). No comparison operators.

**Allowed sort parameters:** none declared — natural insertion order applies.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-billing-address` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Address capture happens at checkout (storefront) or via the admin-panel [[orders-add]] flow; address edits happen via [[orders-address-edit]]. Saving an address through the merchant flow may trigger VAT-zone re-evaluation on the parent order (per [[tax-computation]]); this endpoint does not trigger any of those side effects — it exposes the saved address only.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-billing-address?page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-billing-address?filter[order_id]=1042"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-billing-address/1042?include=order"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-billing-address" \
     -d '{"data":{"type":"order-billing-address","attributes":{"first_name":"Ivan","last_name":"Petrov"}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-billing-address/1042" \
     -d '{"data":{"type":"order-billing-address","id":"1042","attributes":{"company_vat":"BG123456789"}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-billing-address/1042"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-billing-address",
      "id": "1042",
      "attributes": {
        "order_id": 1042,
        "first_name": "Ivan",
        "last_name": "Petrov",
        "phone": "+359888123456",
        "company_name": "ACME EOOD",
        "company_vat": "BG123456789",
        "company_person": "Ivan Petrov",
        "company_registration_number": "203456789",
        "country_iso2": "BG",
        "country_name": "Bulgaria",
        "city_name": "Sofia",
        "state_name": "Sofia-grad",
        "state_iso2": "BG-22",
        "street_name": "Vitosha Blvd",
        "street_number": "12",
        "post_code": "1000",
        "formatted": "ACME EOOD (BG123456789), 12 Vitosha Blvd, Sofia, 1000, Bulgaria"
      },
      "relationships": {
        "order": { "data": { "type": "orders", "id": "1042" } }
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 20, "from": 1, "to": 1, "total": 1, "last-page": 1 }
  }
}
```

### Failure mode

```
HTTP 405 Method Not Allowed
{"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

## Testing checklist

1. `GET /order-billing-address?page[size]=5` — confirm read.
2. `GET /order-billing-address/{id}?include=order` — verify shape (`formatted`, `company_person`, `company_registration_number` appended by default).
3. `GET /order-billing-address?filter[country_iso2]=BG` — verify column filter.
4. `POST /order-billing-address` — verify 405.
5. `PATCH /order-billing-address/{id}` — verify 405.
6. `DELETE /order-billing-address/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — address capture happens at checkout, and edits go through the admin-panel [[orders-address-edit]] flow (which may also trigger VAT-zone re-evaluation per [[tax-computation]]).

## Equivalent UI

- [[orders-details]] — single-order detail view showing the billing address inline.
- [[orders-address-edit]] — admin-panel address edit on a placed order.
- [[orders-invoice]] — invoice generation reads from this address for the "Bill to" section.
- [[orders-add]] — admin-panel manual order creation captures the initial address.

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=billing-address`).
- [[api-order-shipping-address]] — shipping address counterpart.
- [[api-customer-billing-address]] — customer-level saved billing addresses.
- [[tax-computation]] — VAT-zone rules that depend on billing country / VAT number.
- [[order]] — full order envelope including addresses.

## Open questions

- Confirm exact VAT-zone re-evaluation behaviour when the billing address changes country (whether order totals recompute automatically or require manual action via [[orders-products]]).
- Document the relationship between this snapshot address and the customer-level billing-address store ([[api-customer-billing-address]]) — whether updating the customer record propagates to past orders (it should NOT, per [[order]] snapshot rules).
