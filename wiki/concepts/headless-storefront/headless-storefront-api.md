---
type: concept
nav_path: "Concept → Headless storefronts → Storefront API + tokens"
aliases: ["Storefront API", "/api/sf", "Storefront GraphQL", "Public storefront token", "Private storefront token", "X-Storefront-Access-Token", "Storefront API scopes", "Storefront scope set", "cc_nit_ token"]
tags: [nitrogen, headless, graphql, api, tokens, scopes, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Nova platform, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Storefront API + tokens

## Definition

The **Storefront API** is the single GraphQL endpoint Nitrogen storefronts (and any other custom headless app) use to talk to CloudCart at runtime: read products, list collections, mutate cart, fetch customer profile, etc. It is **distinct from** the admin GraphQL schema at `/api/gql` (see [[json-api-v2]] for the cross-API map) — the storefront schema is curated for customer-facing surfaces.

Every Nitrogen storefront has its own **public + private access tokens** that authenticate calls to the Storefront API and carry a per-storefront **scope set** controlling which CloudCart data the headless app can read or write.

## Scope

Covered:

- The four `/api/sf` route variants (POST, GET, downloads, playground).
- Required + optional HTTP headers.
- Public vs private token semantics (where each lives, rotation rules, masked-display rules).
- The default scope set + the full catalogue of scopes the merchant can enable.
- Permission-denied behaviour when an app calls outside its scope.

Not covered:

- Customer-account login (`customerAccessTokenCreate` mutation + email-code flow) — see [[headless-customer-accounts]].
- Nova deploy tokens (a different token surface) — see [[headless-deployment-methods]].
- The endpoint at the cross-API level (admin vs storefront vs JSON-API v2) — see [[json-api-v2]].

## Contrasts

- **Public access token vs private access token** — public is client-side-safe (embedded in browser code, always visible in admin). Private is server-side only, shown ONCE on rotation with a *"Copy now — you won't see it again"* warning, stored as SHA-256 hash + 15-char prefix.
- **Storefront API tokens vs Nova deploy tokens** — Storefront tokens authenticate the deployed app's calls TO CloudCart. Nova deploy tokens authenticate the deploy command's calls to Nova itself. Different tabs, different rotation rules. See [[headless-deployment-methods]].
- **Storefront GraphQL vs admin GraphQL** — `/api/sf` exposes customer-facing types (cart-lines, checkout-redirect URL, public product fields). `/api/gql` (admin) exposes back-office operations (`productsBulkCreate`, analytics reports, settings mutations). Different schemas, different middleware, different tokens.

## Where it applies

### The four `/api/sf` route variants

- **`POST <store-host>/api/sf`** — main GraphQL endpoint for queries and mutations. Shopify-Storefront-API-shaped: products, collections, cart create/lines-add/lines-update/lines-remove, customer access tokens, customer profile/addresses/orders/wishlist, shop info, search, content/menus/pages/blogs.
- **`GET <store-host>/api/sf`** — same endpoint, exposed for introspection clients (GraphiQL, Apollo Studio, codegen tools).
- **`GET <store-host>/api/sf/downloads/{id}?site_id=...&signature=...`** — signed-URL streaming endpoint for digital files attached to customer orders. HMAC-verified; bypasses the storefront-token middleware because the signature itself is the proof of auth.
- **`GET <store-host>/api/sf/playground`** — built-in GraphQL playground UI for developers. **Debug-only — auto-disabled in production.** Accepts the storefront's public/private token in the `X-Storefront-Access-Token` field plus an optional customer bearer token.

The endpoint is served by the platform's `sf` (storefront) Lighthouse instance (verify framework).

### Authentication headers

- **`X-Storefront-Access-Token: <public-or-private-token>`** — REQUIRED. Identifies the storefront and carries its scope set.
- **`Authorization: Bearer <customer-jwt>`** — OPTIONAL. Only for queries / mutations that require a logged-in customer (orders, profile, wishlist, addresses). The JWT is issued by `customerAccessTokenCreate` against the Customer Account API — see [[headless-customer-accounts]].
- **`Content-Type: application/json`**.

A call with an invalid or missing `X-Storefront-Access-Token` gets a 401. A call with a valid token but an operation outside the storefront's scope set gets a permission-denied error in the GraphQL response (not a 4xx).

### Public access token — client-side, always visible

The public access token is provisioned via the platform's existing `StorefrontAccessTokenService` (verify) and stored as a normal token (NOT hashed). The merchant sees the full token on every page render of the Storefront API tab and on rotation. It's safe to ship in client code by design — its scope is the same scope set the storefront has on its profile.

Rotation replaces the old token with the new and is visible on the same screen — no one-time-reveal.

### Private access token — server-side, shown ONCE on rotation

The private access token is generated with the fixed prefix **`cc_nit_`** followed by `bin2hex(random_bytes(32))` for the entropy (verify exact constant). The platform stores ONLY a **SHA-256 hash** of the raw token plus a **15-character prefix** for the masked display (e.g., `cc_nit_xxxx****`).

On rotation, the merchant sees the new raw token ONCE with the warning *"Private token rotated. Copy it now — you won't see it again."* If the merchant loses the raw value, the only recovery is to rotate again. The platform CANNOT recover the original.

A comment in the env-var service notes that **private-token enforcement at the middleware level is still TODO** (verify) — currently both public and private tokens authenticate the same calls, with private intended as a stricter-scope variant.

### Default scope set at creation

Defaults at storefront creation:

- `read_products`
- `read_product_inventory`
- `read_product_tags`
- `read_customers`
- `read_content`
- `read_checkouts`
- `write_checkouts`

### Full scope catalogue

Additional scopes the merchant can enable from the Storefront API tab on [[nitrogen-storefront-overview]]:

- **Products** — `read_products`, `read_product_inventory`, `read_product_tags`.
- **Customers** — `read_customers`, `write_customers`, `read_customer_tags`.
- **Content** — `read_content` (articles, blogs, pages).
- **Checkout** — `read_checkouts`, `write_checkouts`.
- **Orders** — `read_orders`.
- **Bulk Operations** — `read_bulk_operations` (and related write scopes — verify exact key list).

Scope changes **save immediately**. A storefront app calling an API endpoint outside its scope set gets a permission-denied error.

### Both tokens carry the SAME scope set

Public and private tokens both inherit the storefront's scope set. The distinction is exposure surface (client-side vs server-side), not scope. If the scope set includes `write_customers`, BOTH tokens can call `customerUpdate` — which is why the merchant should leave write scopes off if their app doesn't truly need them.

### Plan gating on scopes

Some scopes (`write_customers`, `read_orders`, `read_bulk_operations`) may be implicitly gated by the merchant's plan capabilities (verify). The Nitrogen feature itself does NOT have a published `plan_gate` key, but plan tier still constrains what the storefront app can do. See [[plan-gates]] and [[headless-nitrogen-overview]].

## Related

- [[headless-storefront]] — hub.
- [[headless-customer-accounts]] — `customerAccessTokenCreate` mutation + customer JWT.
- [[headless-deployment-methods]] — Nova deploy tokens (different surface).
- [[headless-nitrogen-overview]] — per-site limits + plan-gate context.
- [[headless-environment-variables]] — `PUBLIC_STOREFRONT_API_TOKEN` is auto-injected as a system variable.
- [[nitrogen-storefront-overview]] — Storefront API tab (tokens + scope picker).
- [[json-api-v2]] — the OTHER GraphQL endpoint (`/api/gql`) and how it differs.
- [[plan-gates]] — how plan tier affects scope availability.

## Open Questions

- Whether private-token middleware enforcement (separating private-only operations from public) has shipped — the env-service comment said TODO.
- Exact list of write scopes under "Bulk Operations" (`write_bulk_operations`? something else?).
- Whether `read_orders` is plan-gated or always available when Nitrogen is.
