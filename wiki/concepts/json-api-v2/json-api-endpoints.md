---
type: concept
nav_path: "Concept → JSON-API v2 → Endpoint inventory"
aliases: ["JSON-API v2 endpoints", "JSON-API v2 resources", "API endpoint inventory", "Read-only resources", "47 resources", "/api/v2 endpoint list", "Custom routes", "order-status helper", "linked-products endpoint"]
tags: [api, json-api, endpoints, resources, integration, concepts]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[json-api-v2]]. See the hub for the other aspects (auth, headers/envelope, pagination, filtering & sorting, status codes, webhooks, audit log, CORS & soft-delete, atomic operations).

# JSON-API v2 — Endpoint inventory

## Definition

JSON-API v2 exposes **47 JSON:API resources + 1 non-JSON:API helper endpoint**. Each resource has a base URL `<store-host>/api/v2/<resource>`, a method matrix across the five standard verbs (`GET`/`POST` on the collection, `GET`/`PATCH`/`DELETE` on a single record), an optional **read-only** flag (16 of the 47 are read-only), optional **custom routes** (e.g. `POST /generate`, `PATCH /{id}/fulfill`), and registered **relationships**.

*"Full"* means all five verbs are supported. **POST and DELETE are blocked on `orders`**; **PATCH is blocked on `images`**. A blocked verb returns **405 Method Not Allowed** at the routing layer.

## Scope

- The full 47-resource inventory by domain, plus the 16-read-only summary, custom routes, the `order-status` helper, the `linked-products` not-callable resource, and app-gated resources.
- Not covered: per-resource attribute / validation / relationship detail (the `api-<name>` pages); auth ([[json-api-auth]]); status codes ([[json-api-status-codes]]); webhook side-effects of PATCH writes ([[json-api-webhooks-integration]]).

## Contrasts

- **Full vs read-only** — 31 writable, 16 read-only. Writes on read-only resources return 405.
- **JSON:API resource vs non-JSON:API helper** — the 47 resources return the typed envelope; the `order-status` helper returns flat `{data: [...]}` without it.
- **Registered + routed vs registered + commented-out routes** — `linked-products` is in the resource map but its routes are commented out; reachable only as a `hasMany` on `products`.

## Endpoint inventory

Every resource's base URL is `/api/v2/<resource>` (the Resource column). Custom routes exist only on `discount-codes`, `discount-codes-pro`, and `orders`, noted in prose under their tables.

### Catalog & products

| Resource | Methods | Relationships |
|---|---|---|
| `products` | full | `hasOne`: `variant`, `image`, `category`, `parameter1`, `parameter2`, `parameter3`. `hasMany`: `variants`, `images`, `categories`, `property-options`, `linked-products` |
| `variants` | full | `hasOne`: `product`, `option1`, `option2`, `option3`. `hasMany`: `images` |
| `variant-parameters` | full | `hasMany`: `variant-options` |
| `variant-options` | full | `hasOne`: `variant-parameters` |
| `properties` | full | `hasMany`: `property-options` |
| `property-options` | full | `hasOne`: `properties` |
| `images` | GET / POST / DELETE — **PATCH blocked** (rows can be added or removed, not edited) | `hasOne`: `product` |
| `categories` | full | `hasOne`: `parent`. `hasMany`: `properties` |
| `vendors` | full | — |
| `product-options` | **GET only** (read-only) | — |

**Note on `product-options`:** gated by the Product Options app install. When not installed, the API returns 404 (wrapped as 422 in the body — see [[json-api-status-codes]]).

### Marketing — discounts, codes, segments

| Resource | Methods | Relationships |
|---|---|---|
| `discounts` | full | — |
| `discount-codes` | full | — |
| `discount-codes-pro` | full | `hasOne`: `discount` |
| `product-to-discount` | full | — |
| `segments` | **GET only** (read-only) | `hasMany`: `subscribers` |

**Custom routes:** `POST /api/v2/discount-codes/generate` bulk-generates Container codes (accepts `application/json`, relaxing `application/vnd.api+json`). `POST /api/v2/discount-codes-pro/generate` is the random / range generator (hard-capped at 5,000 codes per request, any plan).

**Note on `segments`:** registered in routes only (not the main resource map). Read-only — segments cannot be created or modified via the API.

### Subscribers (marketing channels)

| Resource | Methods | Relationships |
|---|---|---|
| `subscribers` | full | `hasMany`: `channels`, `tags` |
| `subscribers-channels` | full | `hasMany`: `subscriber` |
| `subscribers-tags` | full | `hasMany`: `subscriber`, `customer-tags` |

**Note on `subscribers`:** when created via API, `subscribed_from` is force-set to `"API"` — letting a downstream segment / report distinguish API-originated subscribers from form / import sources.

### Orders

| Resource | Methods | Relationships |
|---|---|---|
| `orders` | GET / PATCH — **POST blocked, DELETE blocked** | `hasOne`: `payment`, `shipping`, `shipping-address`, `billing-address`. `hasMany`: `products`, `discounts`, `modifications`, `totals`, `taxes` |
| `order-fulfillment` | full | `hasOne`: `order` |

Custom route on `orders`: `PATCH /api/v2/orders/{id}/fulfill` marks the order fulfilled (with side-effects). The 10 read-only `order-*` sub-resources (all **GET only**) are listed in the read-only summary below.

**Critical orders constraints:** Orders cannot be created (POST blocked) or deleted (DELETE blocked) via API — place via storefront checkout or the manual-order flow (see [[orders-add]]); cancel via a status change on PATCH. All `order-*` sub-resources except `order-fulfillment` are read-only; to modify line items, payments, discounts, taxes, or addresses, PATCH the parent `orders` resource or use the admin panel.

### Order status helper

| Endpoint | URL | Method | Notes |
|---|---|---|---|
| `order-status` (helper) | `/api/v2/order-status` | **GET only** | NON-JSON:API — flat `{data: [{id, name, slug, status_type}, ...]}` of all configured order statuses (built-ins + custom). Supports `?filter=<query-string>` to search by name. Use before PATCHing an order's status to confirm valid status IDs. |

### Customers

| Resource | Methods | Relationships |
|---|---|---|
| `customers` | full | `hasOne`: `group`, `shipping-address`, `billing-address`. `hasMany`: `orders`, `shipping-addresses`, `billing-addresses` |
| `customer-groups` | full | `hasMany`: `customers` |
| `customer-shipping-address` | full | `hasOne`: `customer` |
| `customer-billing-address` | full | `hasOne`: `customer` |
| `customer-tags` | full | `hasMany`: `customer` |

### Multi-store (app-gated)

| Resource | Methods | App requirement |
|---|---|---|
| `stores` | **GET only** (read-only) | Stores / multi-store app |
| `store-quantity` | full | Stores / multi-store app |
| `units` | **GET only** (read-only) | Grocery Store app |

When the corresponding app is not installed, the API returns 404 (wrapped as 422 in the body).

### Blog

| Resource | Methods | Relationships |
|---|---|---|
| `blogs` | full | — |
| `posts` | full | `hasOne`: `blog`, `author`. `hasMany`: `tags` |
| `authors` | **GET only** (read-only) | — |
| `tags` | full | — |

### SEO / redirects

| Resource | Methods | Relationships |
|---|---|---|
| `redirects` | full | `hasOne`: `item` |

### Shipping & payment

`shipping-providers` and `payment-providers` are both **GET only** (read-only). They enumerate the merchant's configured providers — useful before building a checkout flow that needs to know which payment / shipping methods are active.

### Webhooks

`webhooks` — **full** methods — manage the merchant's webhook subscriptions (admin UI: [[settings-hooks]]; delivery: [[notification-delivery]]).

### Registered but not callable

- **`linked-products`** — registered in the resource map, but its routes are **commented out** — NO direct HTTP endpoints. Reachable only as a **`hasMany` on `products`**: fetch via `GET /api/v2/products/{id}/linked-products` or `?include=linked-products` on `products` requests.

## Read-only resource summary (16 endpoints)

GET-only resources (mutations happen via the admin UI, app installs, or the parent `orders` resource): `product-options`, `segments`, `shipping-providers`, `payment-providers`, `authors`, `stores`, `units`, plus the 10 `order-*` sub-resources (`order-products`, `order-products-options`, `order-discount`, `order-modification`, `order-payment`, `order-tax`, `order-total`, `order-shipping`, `order-shipping-address`, `order-billing-address`).

POST / PATCH / DELETE on a read-only resource returns **405 Method Not Allowed** at the routing layer.

## Where it applies

- Integrator capability planning — which resources accept writes determines whether blocked operations need storefront-side or admin-side help (order creation goes through checkout or [[orders-add]]).
- Catalog migration — product import is one-at-a-time; for true bulk use admin GraphQL `productsBulkCreate` (see [[json-api-atomic-operations]]).
- Audit-trail integrations — the read-only `order-*` sub-resources are the cleanest way to export an order snapshot.

## Related

- [[json-api-v2]] — hub.
- [[json-api-status-codes]] — 405 on read-only verbs; 404 wrapped as 422 on app-gated resources.
- [[orders-add]] — admin manual-order flow (orders cannot be created via API).
- [[settings-hooks]] — admin UI for the `webhooks` resource.
- [[notification-delivery]] — outbound delivery semantics for webhook subscriptions.
- The per-resource `api-<name>` pages — full attribute / validator / relationship detail for each endpoint above.

## Open Questions

- **`linked-products` direct route** — registered but routes commented out. Likely a deliberate hold-back; clarifying when (if ever) it will be exposed would help integrators planning catalog-relationship work.
- **App-gated 404 wrapped in 422** — the framework quirk that wraps "app not installed" as 422-with-404-inside obscures which app is missing. Cleaner detection would help integrator error handling `(verify)`.
