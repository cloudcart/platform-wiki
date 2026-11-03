---
type: api-resource
resource_path: /api/v2/shipping-providers
http_methods: [GET]
related_entity: shipping-provider
related_features: [settings-shipping, apps-econt, apps-speedy, apps-boxnow, apps-dpdbulgaria]
aliases: ["Shipping providers API", "Couriers API", "Carriers API", "JSON-API v2 shipping-providers", "API доставчици", "/shipping-providers"]
tags: [api, json-api-v2, infra, shipping]
plan_gates: []
created: 2026-05-26
updated: 2026-06-05
source_count: 4
---
# Shipping providers (JSON-API v2)

## Purpose

**Read-only** access to the **list of shipping-provider configurations on the merchant's store** — one resource row per courier integration the merchant has installed and (optionally) activated. Useful for integrators who need to **enumerate which couriers are wired up on a store**, **read the storefront-facing labels and provider type codes** (e.g., `econt`, `speedy`, `boxnow`, `dpd-bulgaria`), and **filter behaviour by which carriers are active**.

CloudCart does not expose courier credential / sender-address / channel-toggle CRUD via JSON-API v2 — those are admin-panel-only (each courier has a dedicated settings page). To activate, configure or remove a provider, see [[settings-shipping]] or the per-courier feature pages ([[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-dpdbulgaria-speedy]], etc.).

This API does NOT generate shipping quotes — for quote calculation, integrators call the storefront checkout API or replicate the carrier's own quote endpoint client-side.

## Endpoint

- **URL base:** `<store-host>/api/v2/shipping-providers`
- **HTTP methods:** GET only (collection + single). **Read-only** — POST / PATCH / DELETE return **405 Method Not Allowed** at the routing layer.
- **Custom routes:** none.
- **App requirements:** none — every store has at least the default offline / custom shipping methods. The endpoint returns whatever rows exist for the store.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v2/shipping-providers` | List all installed shipping providers on the merchant's store. |
| GET | `/api/v2/shipping-providers/{id}` | Fetch one provider by ID. |
| ❌ POST | `/api/v2/shipping-providers` | **405 Method Not Allowed.** Install / activate / configure couriers via [[settings-shipping]]. |
| ❌ PATCH | `/api/v2/shipping-providers/{id}` | **405 Method Not Allowed.** |
| ❌ DELETE | `/api/v2/shipping-providers/{id}` | **405 Method Not Allowed.** |

Authentication, host resolution, common headers, status codes, and rate limits: see [[json-api-v2]].

## Attributes

All attributes are read-only — no write shape to validate. The serialiser exposes a curated subset of the [[shipping-provider|Shipping Provider]] entity:

All read-only (no POST / PATCH write shape; nothing required).

| Attribute | Type | Notes |
|---|---|---|
| `id` | integer | Stable per-store provider identifier (distinct from the internal type code). |
| `name` | string | Customer-facing storefront label (merchant may rename `econt` to "Express delivery"). |
| `description` | string | Explainer text shown on the checkout shipping picker. |
| `active` | enum `yes` / `no` | Master on/off toggle. `yes` = visible at checkout (subject to scoping); `no` = hidden. Set from [[settings-shipping]]. |
| `provider_type` | string | Internal type code (e.g., `econt`, `speedy`, `boxnow`, `dpd-bulgaria`, `dpd-romania`, `cargus`, `gls`, `dhlexpress`, `sameday`, `bgpost`, `acscourier`, `tcscourier`, `albanian-courier`, `cod`, `custom`, ...). Accessor alias for the hidden `type` column (see `type` row). |
| `geo_zone_id` | integer / null | Geo zone scope. NULL = global. See [[settings-geo-zones]]. |
| `insurance` | integer | Insurance flag — quote includes insurance up to the cart subtotal. Carrier-specific. |
| `external_id` | integer | Carrier-side ID for the per-courier integration handshake. |
| `postal_money` | integer | COD-enabled flag (carriers offering Cash-on-Delivery). |
| `created_at` / `updated_at` / `date_modified` | datetime | Standard timestamps. |
| `image` / `max_thumb_size` / `background` / `width` / `height` | image metadata | Provider logo + background image references. |
| `type` | string | **Hidden** — exposed via the aliased `provider_type` accessor instead. |

**NOT exposed via this API** (admin-panel-only, never serialised): API credentials (username / password / client ID / secret / API key); per-provider sender address book; COD agreement number / pallet rules / additional-services config; pricing tables (per-zone / per-weight / per-cart-value rate rows). There is no programmatic configuration surface in JSON-API v2 — use the admin panel.

## Relationships

The schema declares **no static relationships** (`$relationships = []`). The underlying entity has `geo_zone`, `addresses`, `rates`, `orders_shipping`, `payments`, but none are exposed in v2.

To read "which courier did this order use", integrations follow the order-side companion [[api-order-shipping]] (read-only per-order snapshot, exposes a `shipping.provider` relationship) rather than walking from this provider list.

## Filtering & sorting

- **Filtering:** none declared explicitly (`$allowedFilteringParameters = []`), but the framework auto-merges every column into the allowed-filters list. Practical examples: `filter[active]`, `filter[type]` (the internal column name for `provider_type`), `filter[geo_zone_id]`. Value-equality only.
- **Sorting:** none declared (`$allowedSortParameters = []`). Rows return in DB-default order (typically `id` ASC); `?sort=name` returns 422.
- **Include paths:** none (`$allowedIncludePaths = []` and `$relationships = []`).

## Side effects on write

GET-only. **No writes triggered by this endpoint.**

## Plan-feature gating

- **No app-installed middleware on this route** — every store can reach this endpoint regardless of which couriers are installed.
- **Deprecated providers may still appear** — some integrations are deprecated at the **business level** (no longer recommended for new merchants) but their **code remains active** for existing merchants. E.g., Speedy and Rapido are deprecated (→ DPD BG) but still returned if rows exist. See [[apps-deprecated]].

## Error examples (common cases)

| Condition | Status | Notes |
|---|---|---|
| POST / PATCH / DELETE on this resource | **405 Method Not Allowed** | Blocked at the routing layer — the route is `readOnly`. |
| `?sort=name` (sort key not in allow-list) | **422 Unprocessable Entity** | `$allowedSortParameters` is empty. |
| `GET /api/v2/shipping-providers/{id}` with non-existent ID | **404 Not Found** | Standard JSON:API behaviour. |
| Plan-expired | **402 Payment Required** | Standard api2-layer plan check (see [[json-api-v2]]). |

## Example requests

Read-only resource — only GET is supported. Examples use `<store-host>` and `<YOUR_API_KEY>`.

```bash
# GET collection
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/shipping-providers?page[size]=50"

# GET single
curl -s -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Accept: application/vnd.api+json" \
     "https://<store-host>/api/v2/shipping-providers/3"

# POST / PATCH / DELETE → 405 Method Not Allowed (blocked at the routing layer)
curl -s -X POST \
     -H "X-CloudCart-ApiKey: <YOUR_API_KEY>" \
     -H "Content-Type: application/vnd.api+json" \
     "https://<store-host>/api/v2/shipping-providers" \
     -d '{"data":{"type":"shipping-providers","attributes":{"name":"Test"}}}'
# → HTTP 405 {"errors":[{"status":"405","title":"Method Not Allowed"}]}
```

## Example responses

### GET collection success

```json
{
  "data": [
    {
      "type": "shipping-providers",
      "id": "3",
      "attributes": {
        "name": "Econt Express",
        "description": "Доставка с Еконт",
        "active": "yes",
        "provider_type": "econt",
        "geo_zone_id": 1,
        "insurance": 0,
        "postal_money": 1,
        "external_id": 0,
        "created_at": "2025-01-15T10:00:00+00:00",
        "updated_at": "2026-05-30T11:02:14+00:00"
      }
    },
    {
      "type": "shipping-providers",
      "id": "5",
      "attributes": {
        "name": "DPD Bulgaria",
        "active": "yes",
        "provider_type": "dpd-bulgaria",
        "geo_zone_id": 1
      }
    }
  ],
  "meta": {
    "page": { "current-page": 1, "per-page": 50, "from": 1, "to": 2, "total": 2, "last-page": 1 }
  }
}
```

Note: `provider_type` is the accessor alias for the underlying `type` column — the schema hides raw `type` to avoid clashing with the JSON:API top-level `type` member that designates the resource collection (`shipping-providers`).

### GET single success

```json
{
  "data": {
    "type": "shipping-providers",
    "id": "3",
    "attributes": {
      "name": "Econt Express",
      "active": "yes",
      "provider_type": "econt"
    }
  }
}
```

## Equivalent UI

- [[settings-shipping]] — admin-panel list of all installed shipping providers with the master Active toggle per row.
- Per-courier configuration pages — credentials, sender addresses, allowed channels, COD agreement number, pricing tables. Each courier has its own page (e.g. [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] / [[apps-dpdbulgaria-speedy]] / [[apps-dpdromania]] / [[apps-dhlexpress]] / [[apps-gls]] / [[apps-cargus]] / [[apps-sameday]] / [[apps-fancourier]] / [[apps-acscourier]] / [[apps-tcscourier]] / [[apps-albanian-courier]] / [[apps-eushipment]] / [[apps-sendcloud]] / [[apps-rapido]] / ...).
- [[apps-deprecated]] — couriers still present in code but deprecated at the business level.

## Related

- [[json-api-v2]] — API hub.
- [[shipping-provider]] — full entity reference (carrier credentials, sender address book, channel toggles, pricing models).
- [[shipping-provider-mechanism]] — concept page on how all couriers share a common lifecycle.
- [[api-order-shipping]] — per-order shipping snapshot (read-only, exposes `shipping.provider` relationship including resolved courier type + name).
- [[api-orders]] — orders resource; the typical entry-point for "which courier did this order use".
- [[settings-shipping]] — admin-panel hub for installed couriers.
- [[geo-zone]] — geo-zone scoping for providers.

## Open questions

- Confirm exact set of fields exposed in the response (the schema hides `type` and exposes `provider_type` via the appended accessor; other entity fields like `target`, `marketplaces`, `integration` aren't documented as hidden — verify by issuing a real GET against a test store and listing returned keys).
- Document whether deprecated providers (per business-state — see [[apps-deprecated]]) should be filtered out client-side or whether the API will eventually expose a deprecation flag.
- Verify whether the API returns providers from disabled couriers (`active = no`) or filters them out by default — the schema does not document an implicit scope.
