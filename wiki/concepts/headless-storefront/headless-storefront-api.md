---
type: concept
nav_path: "Concept → Headless storefronts → Storefront API + tokens"
aliases: ["Storefront API", "/api/sf", "Storefront GraphQL", "Public storefront token", "Private storefront token", "X-Storefront-Access-Token", "Storefront API scopes", "Storefront scope set", "cc_nit_ token"]
tags: [nitrogen, headless, graphql, api, tokens, scopes, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-10-21
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
- The default scope set + the platform's catalogue of scopes (stored, not shown in the admin, not checked by the Storefront API).

Not covered:

- Customer-account login (the `customerLoginCodeSend` / `customerLoginCodeVerify` email-code flow) — see [[headless-customer-accounts]].
- Nova deploy tokens (a different token surface) — see [[headless-deployment-methods]].
- The endpoint at the cross-API level (admin vs storefront vs JSON-API v2) — see [[json-api-v2]].

## Contrasts

- **Public access token vs private access token** — public is client-side-safe (embedded in browser code, always visible in admin). Private is server-side only (its own header, `X-Storefront-Private-Token`) and shown ONCE in the admin when generated, with a *"Copy this value now. You won't be able to see it again."* warning; the platform keeps it encrypted, and the Admin GraphQL API can return it (see below).
- **Storefront API tokens vs Nova deploy tokens** — Storefront tokens authenticate the deployed app's calls TO CloudCart. Nova deploy tokens authenticate the deploy command's calls to Nova itself. Different tabs, different rotation rules. See [[headless-deployment-methods]].
- **Storefront GraphQL vs admin GraphQL** — `/api/sf` exposes customer-facing types (cart-lines, checkout-redirect URL, public product fields). `/api/gql` (admin) exposes back-office operations (`productsBulkCreate`, analytics reports, settings mutations). Different schemas, different middleware, different tokens.

## Where it applies

### The four `/api/sf` route variants

- **`POST <store-host>/api/sf`** — main GraphQL endpoint for queries and mutations. Shopify-Storefront-API-shaped: products, collections, cart create/lines-add/lines-update/lines-remove, customer access tokens, customer profile/addresses/orders/wishlist, shop info, search, content/menus/pages/blogs.
- **`GET <store-host>/api/sf`** — same endpoint, exposed for introspection clients (GraphiQL, Apollo Studio, codegen tools).
- **`GET <store-host>/api/sf/downloads/{id}?site_id=...&signature=...`** — signed-URL streaming endpoint for digital files attached to customer orders. HMAC-verified; bypasses the storefront-token middleware because the signature itself is the proof of auth.
- **`GET <store-host>/api/sf/playground`** — built-in GraphQL playground UI for developers. **Debug-only — auto-disabled in production.** Accepts the storefront's public token in the `X-Storefront-Access-Token` field plus an optional customer bearer token; it has no field for the private token.

The endpoint is served by the platform's `sf` (storefront) Lighthouse instance (verify framework).

### Authentication headers

- **`X-Storefront-Access-Token: <public-token>`** — names the store. Optional on one of the store's own domains: without it, the store is found from the address the request came to.
- **`X-Storefront-Private-Token: <private-token>`** — OPTIONAL, from the storefront's server only. With it, the server may also send **`X-Storefront-Buyer-IP: <shopper's IP>`**, which then counts as the request's address (for orders, policy consents and the form rate limits); without the private token that header is ignored. A public token sent alongside must belong to the same storefront.
- **`Authorization: Bearer <customer-access-token>`** — OPTIONAL. Runs the whole request as that signed-in customer (their prices, discounts and checkout hand-off), as does naming the token in the operation's `@inContext(buyer:)`; an invalid token is ignored and the request runs as a guest. The operations on the customer's own data (profile, orders, wishlist, addresses) take the token as their `customerAccessToken` argument instead. The token comes from `customerLoginCodeVerify`, after `customerLoginCodeSend` — see [[headless-customer-accounts]].
- **`Content-Type: application/json`**.

A token that is sent but does not verify (an unknown or revoked public token, or a wrong private token) gets a 403 (`ACCESS_DENIED`); the API never falls back to the domain. So does a request without a token on an address that serves no store. The storefront's scope set is not checked: no operation is refused for being outside it.

### Public access token — client-side, always visible

The public access token is created with the storefront and stored as a normal token (NOT hashed). The merchant sees the full token, with a Copy button, every time the Storefront API tab opens; it is also the storefront's `PUBLIC_STOREFRONT_API_TOKEN` variable. It's safe to ship in client code by design: it only names the store, and a customer's own data also needs that customer's access token.

The admin has no button to replace the public token: replacing it would stop every deployed copy of the storefront at once, until each is deployed again.

### Private access token — server-side, shown ONCE on rotation

The private access token is generated with the fixed prefix **`cc_nit_`** followed by 64 random hexadecimal characters. The storefront's record holds a **SHA-256 hash** of it, which the Storefront API checks, plus its first **15 characters** for the masked display (e.g., `cc_nit_xxxxxxxx********************`). The raw token is also kept, encrypted, as the storefront's `PRIVATE_STOREFRONT_API_TOKEN` variable, so the next deploy binds it.

The Storefront API tab shows only the masked token. **Generate new token** first asks for confirmation (the new token replaces the current one at once, and a storefront deployed with the old one is refused until it is deployed again), then shows the new raw token ONCE with the warning *"Copy this value now. You won't be able to see it again."* The variables page masks it too. The admin screens never show it again, but it can be recovered: through the Admin GraphQL API (its tokens are made in [[settings-pat-tokens]]), `nitrogenStorefrontPrivateToken` returns it to an admin with the Nitrogen permission (with a personal access token, one that has the "full-access" or "settings" scope), and each disclosure is logged; `cloudcart nitrogen env pull` gets it this way. Only for a storefront created before the platform kept the token does it return nothing; there the only recovery is a new token (**Generate new token**, or that API's `nitrogenStorefrontPrivateTokenRotate`).

Both tokens authenticate the same operations. The private token is sent in its own header, `X-Storefront-Private-Token`, and only from the storefront's server; a wrong one is refused. What it adds is that the server may state the shopper's IP address (`X-Storefront-Buyer-IP`).

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

The platform's catalogue of storefront scopes. The Storefront API tab on [[nitrogen-storefront-overview]] does not show them, and the Storefront API does not check them:

- **Products** — `read_products`, `read_product_inventory`, `read_product_tags`.
- **Customers** — `read_customers`, `write_customers`, `read_customer_tags`.
- **Content** — `read_content` (articles, blogs, pages).
- **Checkout** — `read_checkouts`, `write_checkouts`.
- **Orders** — `read_orders`.
- **Bulk Operations** — `read_bulk_operations` (and related write scopes — verify exact key list).

No operation is refused for being outside the scope set.

### Both tokens carry the SAME scope set

Public and private tokens reach the same operations; the distinction is exposure surface (client-side vs server-side), not scope. Operations on a customer's own data, such as `customerUpdate`, also need that customer's access token, whatever the scope set says.

### Plan gating on scopes

Some scopes (`write_customers`, `read_orders`, `read_bulk_operations`) may be implicitly gated by the merchant's plan capabilities (verify). The Nitrogen feature itself does NOT have a published `plan_gate` key, but plan tier still constrains what the storefront app can do. See [[plan-gates]] and [[headless-nitrogen-overview]].

## Related

- [[headless-storefront]] — hub.
- [[headless-customer-accounts]] — `customerLoginCodeSend` / `customerLoginCodeVerify` + customer access token.
- [[headless-deployment-methods]] — Nova deploy tokens (different surface).
- [[headless-nitrogen-overview]] — per-site limits + plan-gate context.
- [[headless-environment-variables]] — `PUBLIC_STOREFRONT_API_TOKEN` is auto-injected as a system variable.
- [[nitrogen-storefront-overview]] — Storefront API tab (tokens + scope picker).
- [[json-api-v2]] — the OTHER GraphQL endpoint (`/api/gql`) and how it differs.
- [[metafields-nitrogen]] — the metafield and metaobject queries.
- [[plan-gates]] — how plan tier affects scope availability.

## Open Questions

- Exact list of write scopes under "Bulk Operations" (`write_bulk_operations`? something else?).
- Whether `read_orders` is plan-gated or always available when Nitrogen is.
