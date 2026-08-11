---
type: api-resource
resource_path: /api/v2/payment-providers
http_methods: [GET]
related_entity: payment-provider
related_features: [settings-payment-providers, payment-providers, payment-providers-stripe, payment-providers-icard, payment-providers-borica-way4]
aliases: ["Payment providers API", "Gateways API", "JSON-API v2 payment-providers", "API платежни доставчици", "/payment-providers"]
tags: [api, json-api-v2, infra, payments]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 4
---
# Payment providers (JSON-API v2)

## Purpose

**Read-only** access to the **list of payment-provider configurations on the merchant's store** — one resource row per installed gateway. Integrators use it to **discover which gateways are wired up** before rendering payment-method pickers, read the storefront label + active state, filter behaviour by active gateways, and resolve the provider's logo URL for checkout flows.

The endpoint is **strictly read-only**: CloudCart does not expose gateway credential / mode / activation / amount-range CRUD via JSON-API v2. To install, activate, configure or remove a gateway, use the admin panel — [[settings-payment-providers]] or the [[payment-providers|payment-providers hub]], plus per-gateway pages such as [[payment-providers-stripe]], [[payment-providers-icard]], [[payment-providers-borica-way4]], [[payment-providers-cloudcart-pay]], [[payment-providers-cod]].

This API does **not** process payments — transaction creation, capture, refund, and webhook callbacks run through each gateway's own integration layer. This endpoint is purely a configuration / discovery surface.

## Endpoint

- **URL base:** `<store-host>/api/v2/payment-providers`
- **HTTP methods:** GET only (collection + single). The route is read-only; **POST / PATCH / DELETE return 405 Method Not Allowed** at the routing layer.
- **App requirements:** none — every store has at least Cash-on-Delivery and bank-transfer available.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/payment-providers` | List all installed payment providers (auto site-scoped). |
| GET | `/api/v2/payment-providers/{provider-code}` | Fetch one provider by **gateway code** (e.g., `stripe`, `icard`, `borica_way4`, `cod`). |
| ❌ POST | `/api/v2/payment-providers` | **405.** Configure gateways via [[settings-payment-providers]]. |
| ❌ PATCH | `/api/v2/payment-providers/{provider-code}` | **405.** |
| ❌ DELETE | `/api/v2/payment-providers/{provider-code}` | **405.** |

**Primary key:** the resource ID is `provider` (the gateway code string), **not** the integer table `id`. `GET /api/v2/payment-providers/stripe` resolves the Stripe config; `/api/v2/payment-providers/1` returns 404. Integrations must address rows by gateway code.

**Site-scoping:** every query is automatically filtered to the API key's site. Cross-site reads are not possible — one API key authenticates one site and returns only that site's providers.

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

All attributes are **read-only** — there is no write shape to validate.

| Attribute | Type | Notes |
|---|---|---|
| `provider` | string | The gateway code (`stripe`, `icard`, `borica_way4`, `cod`, `paypal`, `mokka`, ...). Also the JSON:API resource `id`. |
| `title` | string | Merchant-set storefront title (e.g., "Pay with card", "Cash on Delivery"). Falls back to translation `sf.payment_provider.name_<provider>` when empty. |
| `active` | enum `yes` / `no` | Master on/off. When `no`, the gateway is hidden at checkout; when `yes`, it appears (subject to amount-range, country, and per-product allow-list scoping). |
| `width` / `height` | integer | Provider logo dimensions. |
| `image_url` | string | **Appended accessor** — resolved logo URL: the per-store uploaded logo when set, otherwise the platform-default media path. Use for logo placement at checkout. |
| `created_at` / `updated_at` | datetime | Standard timestamps. |

**Hidden (never on the wire):**

- `id` (integer table PK — gateway code is the wire identifier) and `site_id` (redundant given the site filter).
- `image` / `max_thumb_size` — the resolved URL is exposed via `image_url` instead.
- `configuration` — **deliberately hidden.** This AES-encrypted blob holds gateway credentials (API keys, merchant IDs, terminal IDs, private keys, certificates), `amount_from` / `amount_to`, `discount_amount` / `discount_type`, mode (live / test), 3DS / save-card flags, surcharge rules, and per-country / per-product allow-lists. It **must never leave the platform**. Integrations needing amount-range / discount-fee logic must replicate the rules on their side or read them per-gateway in the admin panel.

A `storefront_name` accessor exists on the model (resolves to `title`, else the `sf.payment_provider.name_<provider>` translation) but is **currently commented out** in the schema's appended attributes. Rely on `title` with the same fallback client-side, or read the [[payment-provider|payment provider]] catalog `name` for the default label.

## Relationships

The schema declares **no relationships** and no includable paths. The underlying row belongs to the master [[payment-provider|payment provider]] catalog entry, but that link is not exposed in v2.

To read "which gateway processed this order", use the companion resource [[api-order-payment]] — it exposes the per-order payment snapshot (resolved provider type + name) read-only, rather than walking from this provider list.

## Filtering & sorting

**Filtering:**

- **`filter[active]`** — accepts `yes` / `no`. The primary filter for enumerating gateways visible at checkout.
- Plus value-equality on any column, e.g. `filter[provider]`, `filter[title]`.

**Sorting:** none declared. Rows return in DB-default order (by `id` ASC). `?sort=title` returns 422.

**Includes:** none — there are no relationships to include.

## Side effects on write

GET-only. **No writes triggered by this endpoint.**

## Plan-feature gating

- **No app-installed middleware on this route** — every CloudCart store can reach this endpoint regardless of which gateways are installed.
- **Site-scoped automatically** — multi-store merchants get only the current site's providers; cross-site discovery requires separate API keys per site.

## Error examples (common cases)

| Condition | Status | Notes |
|---|---|---|
| POST / PATCH / DELETE on this resource | **405 Method Not Allowed** | Blocked at the routing layer — the route is `readOnly`. |
| `?sort=title` (sort key not in allow-list) | **422 Unprocessable Entity** | `$allowedSortParameters` is empty. |
| `GET /api/v2/payment-providers/1` (integer ID instead of gateway code) | **404 Not Found** | The primary key is `provider`, not `id`. Use the gateway code. |
| `GET /api/v2/payment-providers/{code}` with an unknown gateway code | **404 Not Found** | Standard JSON:API behaviour. |
| Plan-expired | **402 Payment Required** | Standard api2-layer plan check (see [[json-api-v2]]). |

## Example requests

All examples use `<store-host>` and `<YOUR_API_KEY>`, header `X-CloudCart-ApiKey: <YOUR_API_KEY>` and `Accept: application/vnd.api+json`. Only GET is supported; the resource id is the gateway code, not the integer PK.

```bash
# Collection
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/payment-providers?page[size]=50"

# Only active gateways
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/payment-providers?filter[active]=yes"

# Single — by gateway code (substitute icard, borica_way4, cod, paypal, mokka, epay, ...)
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/payment-providers/stripe"
```

A POST / PATCH / DELETE to this resource returns `HTTP 405 Method Not Allowed`; GET by integer ID returns `HTTP 404 Not Found`. Configure gateways via [[settings-payment-providers]] instead.

## Example responses

A collection GET returns one object per installed provider; a single GET returns the same shape for one provider:

```json
{
  "data": [
    {
      "type": "payment-providers",
      "id": "stripe",
      "attributes": {
        "provider": "stripe",
        "title": "Pay with card",
        "active": "yes",
        "image_url": "https://<store-host>/media/payment-providers/stripe.png",
        "width": 120,
        "height": 40,
        "created_at": "2025-02-10T14:00:00+00:00",
        "updated_at": "2026-05-30T11:02:14+00:00"
      }
    },
    {
      "type": "payment-providers",
      "id": "cod",
      "attributes": { "provider": "cod", "title": "Cash on Delivery", "active": "yes",
        "image_url": "https://<store-host>/media/payment-providers/cod.png" }
    }
  ],
  "meta": { "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 2, "total": 2, "last-page": 1 } }
}
```

Error bodies follow standard JSON:API: `{"errors":[{"status":"404","title":"Not Found"}]}` for a wrong identifier, `{"errors":[{"status":"405","title":"Method Not Allowed"}]}` for a write attempt.

## Equivalent UI

- [[settings-payment-providers]] — admin-panel list of all installed gateways with the master Active toggle, amount-range edits, discount / surcharge configuration.
- [[payment-providers]] — payment-provider feature hub; jumps to every per-gateway settings page (credentials, live / test mode, amount range, country scoping, surcharge / fee, save-card flag). The full gateway catalogue lives there — e.g. [[payment-providers-stripe]], [[payment-providers-paypal]], [[payment-providers-icard]], [[payment-providers-borica-way4]], [[payment-providers-cloudcart-pay]], [[payment-providers-cod]].

## Related

- [[json-api-v2]] — API hub.
- [[payment-provider]] — full entity reference (credentials shape, mode toggle, save-card behaviour, authorize-then-capture, 3DS handling, surcharge / discount).
- [[payment-provider-mechanism]] — concept page on the shared payment-provider lifecycle.
- [[api-order-payment]] — per-order payment snapshot (read-only, exposes resolved provider + status). The recommended path for "which gateway processed this order".
- [[api-orders]] — orders resource.
- [[settings-payment-providers]] — admin-panel hub for installed gateways.
- [[payment-providers]] — payment-provider feature hub.

## Open questions

- Confirm whether the `provider` primary-key convention (using gateway code instead of integer ID) is documented for integrators externally, or whether integrators routinely trip over GETing by integer ID and getting 404s.
- The `storefront_name` accessor is commented out in the schema's `$appends`. Verify whether it should be uncommented (to give integrators a stable customer-facing label) or whether `title` + client-side fallback is the contract.
- Document whether the `image_url` exposed via this endpoint is the full absolute URL or a relative media-path that the integrator must resolve against the storefront host.
