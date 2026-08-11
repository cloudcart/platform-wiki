---
type: api-resource
resource_path: /api/v2/order-shipping-address
http_methods: [GET]
related_entity: order
related_features: [orders-details, orders-address-edit]
aliases: ["Order shipping address API", "Recipient address API", "JSON-API v2 order-shipping-address", "/order-shipping-address"]
tags: [api, json-api-v2, orders, addresses]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Order Shipping Address (JSON-API v2)

## Purpose

The `order-shipping-address` resource is the **read-only view of the shipping (recipient) address on every order** — the customer's name, phone, postal address, country, city, state, optional latitude / longitude, and OmniShip integration metadata. External integrations use it to populate fulfillment systems, courier waybill generators, and CRM dashboards with the recipient details.

The shipping address is captured at storefront checkout and can be edited via the admin-panel [[orders-address-edit]] flow. It is not modifiable through this API endpoint.

## Endpoint

| Method | Path | Status |
|---|---|---|
| `GET` | `/api/v2/order-shipping-address` | List every order shipping address. |
| `GET` | `/api/v2/order-shipping-address/{id}` | Fetch a single shipping address. |
| `POST` / `PATCH` / `DELETE` | `/api/v2/order-shipping-address[/{id}]` | **GET only — returns 405 Method Not Allowed.** To edit an order's shipping address, the merchant uses [[orders-address-edit]] in the admin panel. |

No app install or plan feature gates this resource. To scope the response to a single order, filter by `order_id` (auto-merged from the column list) or fetch via the parent with `?include=shipping-address` on [[api-orders]].

## Attributes

All attributes are returned by GET only.

| Attribute | Type | Notes |
|---|---|---|
| `order_id` | integer | Parent order. |
| `first_name`, `last_name` | string | Recipient name. |
| `phone` | string | Recipient phone. |
| `company_name` | string | Recipient company (when applicable). |
| `company_vat` | string | Recipient company VAT number. |
| `companyYesNo` (`company`) | enum `yes` / `no` | Whether the recipient is a company. |
| `country_iso2` (`country`) | string | ISO 3166-1 alpha-2 country code. |
| `country_name` | string | Localised country name snapshot. |
| `city_name` (`city`) | string | City name. |
| `state_name`, `state_iso2` | string | State / region (when applicable). |
| `street_name` + `street_number` (`street`) | string | Street address fields. |
| `post_code` (`postal_code`) | string | Postal code. |
| `latitude` (`lng`) / `longitude` (`lat`) | float | Map coordinates (when the integration supplies them — Econt office, BoxNow locker, gmap auto-fill). |
| `address1` (`note_customer`) | string | Free-text address note from the customer. |
| `text` (`gmap_address`) | string | Google Maps-formatted address string. |
| `formatted` (appended) | string | Pre-rendered "first_name last_name, street, city, postal_code, country" string. |
| `integration` | string | OmniShip integration that produced this address (default `internal`; courier-supplied addresses note their courier). |

**Hidden by default** (these store JSON payloads of the original mapping data; surfaced through the typed accessors above instead): `address`, `country`, `city`, `state`, `street`.

**Sparse-field append values:** none configured — `formatted` is appended by default.

## Relationships

| Name | Cardinality | Type | Notes |
|---|---|---|---|
| `order` | belongsTo | order | Parent order. |

**Allowed include paths:** `order`.

## Filtering & sorting

**Allowed filtering parameters:** none specific to the resource — only the framework's auto-merged column filters (exact-equality on any column, e.g., `filter[order_id]=123`, `filter[integration]=econt`). No comparison operators.

**Allowed sort parameters:** none declared — natural insertion order applies.

**Pagination:** standard JSON:API `page[number]` / `page[size]` (1–100, default 20).

## Side effects

None. **`order-shipping-address` is read-only — POST / PATCH / DELETE return 405 Method Not Allowed.** Address capture happens at checkout (storefront) or via the admin-panel [[orders-add]] flow; address edits happen via [[orders-address-edit]]. Saving an address through the merchant flow may sync to the chosen courier (the `integration` field, OmniShip mapping); this endpoint does not trigger any of those side effects — it exposes the saved address only.

## Example requests

All examples use `<store-host>` (e.g., `mystore.cloudcart.net`) and `<YOUR_API_KEY>` (64-char uppercase).

### GET collection

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping-address?page[size]=20"
```

### GET collection scoped to one order

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping-address?filter[order_id]=1042"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping-address/1042?include=order"
```

### POST / PATCH / DELETE blocked (405)

```bash
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping-address" \
     -d '{"data":{"type":"order-shipping-address","attributes":{"first_name":"Ivan","last_name":"Petrov"}}}'
```

```bash
curl -s -X PATCH \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping-address/1042" \
     -d '{"data":{"type":"order-shipping-address","id":"1042","attributes":{"phone":"+359888123456"}}}'
```

```bash
curl -s -X DELETE \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/order-shipping-address/1042"
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "order-shipping-address",
      "id": "1042",
      "attributes": {
        "order_id": 1042,
        "first_name": "Ivan",
        "last_name": "Petrov",
        "phone": "+359888123456",
        "company_name": "",
        "company_vat": "",
        "companyYesNo": "no",
        "country_iso2": "BG",
        "country_name": "Bulgaria",
        "city_name": "Sofia",
        "state_name": "Sofia-grad",
        "state_iso2": "BG-22",
        "street_name": "Vitosha Blvd",
        "street_number": "12",
        "post_code": "1000",
        "latitude": 42.6977,
        "longitude": 23.3219,
        "address1": "Ring the bell twice",
        "text": "12 Vitosha Blvd, Sofia 1000, Bulgaria",
        "formatted": "Ivan Petrov, 12 Vitosha Blvd, Sofia, 1000, Bulgaria",
        "integration": "econt"
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

1. `GET /order-shipping-address?page[size]=5` — confirm read.
2. `GET /order-shipping-address/{id}?include=order` — verify shape (`formatted` appended by default).
3. `GET /order-shipping-address?filter[country_iso2]=BG` — verify column filter.
4. `POST /order-shipping-address` — verify 405.
5. `PATCH /order-shipping-address/{id}` — verify 405.
6. `DELETE /order-shipping-address/{id}` — verify 405.
7. Confirm the resource cannot be modified directly — address capture happens at checkout, and edits go through the admin-panel [[orders-address-edit]] flow.

## Equivalent UI

- [[orders-details]] — single-order detail view showing the shipping address inline.
- [[orders-address-edit]] — admin-panel address edit on a placed order.
- [[orders-add]] — admin-panel manual order creation captures the initial address.

## Related

- [[json-api-v2]] — API hub.
- [[api-orders]] — parent order resource (`?include=shipping-address`).
- [[api-order-billing-address]] — billing address counterpart.
- [[api-customer-shipping-address]] — customer-level saved shipping addresses (the source for repeat-customer pre-fills).
- [[order]] — full order envelope including addresses.

## Open questions

- Document the exact behaviour when the order's chosen courier requires a specific address format (e.g., Econt office ID vs free-text address) — the `integration` field signals which transformation was applied at order time.
- Confirm whether `companyYesNo` is returned consistently as `yes` / `no` strings or as boolean (per OmniShip mapping rules).
