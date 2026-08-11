---
type: api-resource
resource_path: /api/v2/product-options
http_methods: [GET]
related_entity: product-option
related_features: [apps-product-options-settings-new, products-options-overview]
aliases: ["Product Options API", "JSON-API v2 product-options", "API опции на продукт", "/product-options"]
tags: [api, json-api-v2, products]
plan_gates: [product-options-app]
created: 2026-05-26
updated: 2026-06-05
source_count: 3
---
# Product Options (JSON-API v2)

## Purpose

A `product-options` resource is one entry from the [[apps-product-options-settings-new|Product Options]] app's catalog — a merchant-defined add-on selector that a product can offer at checkout beyond its variant grid: engraving text, gift wrapping, extended warranty, custom configuration choices. Each option's price modifier flows into the cart line at checkout.

This resource is **read-only on JSON-API v2** — the option catalog is mirrored from the app's internal `form_fields` table (with the `ProductOptions` global scope applied) and is mutated only through the admin app at [[apps-product-options-settings-new]]. The API is for **enumeration only**: integrations list the configured options to reference them when reading per-line option selections on orders or to render an integration-side picker that mirrors the catalog.

## Endpoint

- **URL base:** `<store-host>/api/v2/product-options/`
- **GET collection** — `GET /api/v2/product-options`.
- **GET single** — `GET /api/v2/product-options/{id}`.
- **POST / PATCH / DELETE — NOT supported.** The route is registered `readOnly` — those verbs return **405 Method Not Allowed**.
- No relationship endpoints.
- No custom action routes.
- **App-install requirement:** the route is wrapped in `api_apps_installed:product-options` middleware. Without the Product Options app installed, every request returns **HTTP 404** with the message `"product-options app not installed"` (occasionally wrapped as 422 in the body — see [[json-api-v2]] framework quirks).

Auth, headers, rate limits: [[json-api-v2]].

## Attributes

The schema declares no `appends` and no `relationships`; the only hidden field is `type`. All other columns on the underlying `form_fields` table (scoped to `form = 'product_options'`) are serialised. Common fields include:

| Attribute | Type | Notes |
|---|---|---|
| `id` | integer | Stable option identifier. |
| `name` | string | Internal name. |
| `storefront_name` | string | Customer-facing label. |
| `mapping` | string | Per-option mapping key. |
| `active` | tinyint | Whether the option is enabled. |
| `sort_order` | integer | Display order in the option list on the product page. |
| `amount` | integer | Price modifier in minor units. |
| `required` | tinyint | Whether the customer must pick a value at checkout. |
| `product_symbol` | string | Symbol shown next to the per-product control. |
| `value_symbol` | string | Symbol shown next to the value. |
| `allow_negative` | tinyint | Whether negative amount inputs are accepted. |
| `min_square` | integer | Lower bound for square-type options. |
| `system` | tinyint | System-managed flag. |
| `customer_modify` | tinyint | Whether the customer can modify the value post-checkout. |
| `key` | string | Key used to identify the option in cart-line payloads. |
| `apply_over_price_type` | string | Whether the modifier applies over the discounted or undiscounted price. |
| `amount_type` | string | `fixed` or `percent`. |
| `per_item` | tinyint | Whether the modifier applies per unit or per line. |
| `type` | — | **Hidden** in serialised output. |

The Schema also exposes the appended accessors defined on the parent `FormFields` model (`type_text`, `required_text`, `amount_formatted`, etc.) when included.

Read-only: every attribute, since the resource is read-only.

## Relationships

None declared in the schema. Per-product option bindings are managed by the admin app, not exposed through this resource. To read which options a specific order line used, inspect the [[api-order-products-options]] resource.

## Filtering & sorting

**Allowed filtering parameters** — no named filters declared. All raw columns on `form_fields` are auto-allowed, but with the global `ProductOptions` scope applied (so `form = 'product_options'` is implicit and cannot be overridden).

**Allowed sort parameters** — none declared. Natural ordering applies.

**Allowed include paths** — none declared.

## Side effects on write

None — read-only endpoint. POST / PATCH / DELETE return 405. The catalog is mutated only through the admin app.

## Plan-feature gating

The endpoint requires the Product Options app to be installed on the store's plan. Without the app, every request returns 404. See [[apps-product-options-settings-new]] for install + activation.

## Error examples

- App not installed:
  ```
  HTTP 404 Not Found
  {"errors":[{"status":"404","title":"Not Found","detail":"product-options app not installed"}]}
  ```
- POST / PATCH / DELETE attempted:
  ```
  HTTP 405 Method Not Allowed
  ```

## Example requests

Read-only — only GET is supported. All examples use `<store-host>` and `<YOUR_API_KEY>`.

### GET collection (filter by active, sort)

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/product-options?page[size]=50&filter[active]=1"
```

### GET single

```bash
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/product-options/7"
```

### Confirm app-install gate (without the Product Options app)

```bash
# When the Product Options app is NOT installed, every request returns 404.
curl -s -o - -w "\nHTTP %{http_code}\n" \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/product-options"
```

### Blocked verbs (always return 405)

```bash
curl -s -X POST -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     "https://<store-host>/api/v2/product-options" \
     -d '{"data":{"type":"product-options","attributes":{"name":"Engraving"}}}'
# HTTP 405 Method Not Allowed
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "product-options",
      "id": "7",
      "attributes": {
        "name": "Engraving",
        "storefront_name": "Add engraving",
        "mapping": "engraving",
        "active": 1,
        "sort_order": 0,
        "amount": 500,
        "amount_type": "fixed",
        "apply_over_price_type": "discounted",
        "per_item": 1,
        "required": 0,
        "product_symbol": null,
        "value_symbol": null,
        "allow_negative": 0,
        "min_square": 0,
        "system": 0,
        "customer_modify": 0,
        "key": "engraving"
      }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 1, "total": 1, "last-page": 1 } }
}
```

### App not installed

```
HTTP 404 Not Found
{"errors":[{"status":"404","title":"Not Found","detail":"product-options app not installed"}]}
```

### Blocked verb

```
HTTP 405 Method Not Allowed
```

## Testing checklist

1. `GET /product-options` — confirm 200 when the [[apps-product-options-settings-new|Product Options]] app is installed; otherwise expect 404 `product-options app not installed`.
2. `GET /product-options?filter[active]=1` — verify only active options come back.
3. `GET /product-options/{id}` — verify single-resource lookup works for an id from step 1.
4. `POST /product-options` with any payload — verify **405 Method Not Allowed**.
5. `PATCH /product-options/{id}` — verify **405**.
6. `DELETE /product-options/{id}` — verify **405**.

## Equivalent UI

- [[apps-product-options-settings-new]] — Product Options app's settings screen (CRUD on options happens here).
- [[products-options-overview]] — overview of Product Options on individual products.
- [[product-option]] — entity reference for the Product Option attribute model.

## Related

- [[json-api-v2]] — protocol contract.
- [[apps-product-options-settings-new]] — admin app where the option catalog is managed.
- [[products-options-overview]] — overview of Product Options on individual products.
- [[product-option]] — entity reference for the Product Option attribute model.
- [[api-products]] — products that may reference product options.
- [[api-order-products-options]] — per-order-line option selections (the read surface integrations use after a checkout completes).
- [[settings-api-keys]] — authentication setup.

## Open questions

- Document the exact list of attributes returned by GET — the Schema appends no fields, declares no relationships, and only hides `type`. The underlying `form_fields`-with-`ProductOptions`-scope model is the source of truth; a sample API response would let integrators wire to the real envelope.
- Verify whether the merchant can configure per-plan limits on the number of product options (the app is plan-gated; per-app limits may not exist).
- Confirm whether `?include=` is silently ignored or returns 422 given the Schema has no relationships.
