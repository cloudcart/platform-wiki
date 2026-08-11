---
type: concept
nav_path: "Concept → Headless storefronts → Customer Account API"
aliases: ["Customer Account API", "Headless login", "Email-code login", "Passwordless headless login", "customerAccessTokenCreate", "nitro_customer_accounts", "PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID", "Customer JWT"]
tags: [nitrogen, headless, customer, authentication, oauth, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Nova platform, Storefront API, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Customer Account API

## Definition

The **Customer Account API** is the per-storefront authentication endpoint Nitrogen storefronts use to log customers in. Currently the auth flow is **passwordless 6-digit email code** — the customer enters their email, receives a code, exchanges it for a JWT, then includes that JWT in subsequent calls to the Storefront API.

The customer's underlying account, addresses, orders, and saved data are the **same as on the legacy CloudCart storefront**. The Customer Account API is just the headless-app-facing entry point for that data; the records themselves live in the unified [[customer]] table.

## Scope

Covered:

- The 6-digit-email-code login flow.
- The `customerAccessTokenCreate` mutation against `/api/sf`.
- The `nitro_customer_accounts` record + the OAuth fields it stores (currently unused).
- Default scopes at creation.
- System env vars exposed when customer accounts are enabled.
- How customer auth interacts with the Storefront API.

Not covered:

- The legacy storefront's customer login (cookie-based session) — that's the legacy theme path; Nitrogen doesn't use it.
- The `customer` entity's data model — see [[customer]].
- OAuth 2.0 PKCE flow (scopes, callback URIs, JS origins, logout URI) — fields stored but NOT enforced yet (verify).

## Contrasts

- **Email-code login (active) vs OAuth 2.0 PKCE (stored-not-enforced)** — the OAuth-shaped fields (`client_id`, `client_secret_hash`, `client_secret_prefix`, `scopes`, `callback_uris`, `js_origins`, `logout_uri`) all exist on the `nitro_customer_accounts` record. The auth middleware currently ignores them — the only flow exposed by the admin UI is the 6-digit email code.
- **Customer JWT vs Storefront API token** — the storefront token (`X-Storefront-Access-Token`) authenticates the APP; the customer JWT (`Authorization: Bearer <jwt>`) authenticates the CUSTOMER. Calls touching customer data need BOTH headers. See [[headless-storefront-api]].
- **Same data backs every storefront** — a customer who has an account on the legacy CloudCart storefront sees the same orders / addresses / wishlist on a Nitrogen storefront that points at the same CloudCart backend (with `read_customers` + the customer JWT).

## Where it applies

### When the merchant enables Customer Accounts

When the merchant enables Customer Accounts on a Nitrogen storefront, the platform:

1. Creates a `nitro_customer_accounts` record with default scopes and a generated `client_id` + `client_secret`.
2. Exposes two system env vars (see [[headless-environment-variables]]):
   - `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID`
   - `PUBLIC_CUSTOMER_ACCOUNT_API_URL`

The admin UI surface is the **Customer Account API tab** on [[nitrogen-storefront-overview]].

### The 6-digit email code flow

The active login flow is passwordless:

1. Customer enters their email on the merchant's Nitrogen storefront.
2. Storefront calls a `customerAccessTokenCreate` (or similar) mutation against `/api/sf` requesting a code.
3. CloudCart emails a 6-digit code to the customer's address.
4. Customer enters the code in the storefront app.
5. Storefront calls the mutation again with `email + code`; CloudCart returns a **customer JWT**.
6. Storefront stores the JWT (typically in an HttpOnly cookie) and includes it as `Authorization: Bearer <jwt>` on subsequent calls.

This is the **only** customer-auth flow exposed via the Customer Account API right now. There is no username/password flow yet (verify).

### Customer JWT carried alongside the storefront token

Once the customer has a JWT, calls to `/api/sf` that need a logged-in customer (orders, profile, wishlist, addresses) include BOTH headers:

- `X-Storefront-Access-Token: <public-or-private-storefront-token>` — identifies the storefront.
- `Authorization: Bearer <customer-jwt>` — identifies the customer.

Without the JWT, customer-bound queries return permission-denied even if the storefront has `read_customers` scope.

### `nitro_customer_accounts` record fields

The record stores OAuth-style fields (verify exact column names):

- `client_id` — UUID, public.
- `client_secret_hash` — SHA-256 of a raw secret prefixed `cc_cas_`.
- `client_secret_prefix` — 15 chars, for masked display.
- `scopes` — array; defaults below.
- `callback_uris` — array of allowed OAuth redirect URIs (not enforced yet).
- `js_origins` — array of allowed JS origins (not enforced yet).
- `logout_uri` — single URI (not enforced yet).

A comment in the env service notes that OAuth scope/URI enforcement and private-token enforcement are both still TODO (verify).

### Default scopes at creation

When customer accounts are enabled, defaults are:

- `customer_read_customers`
- `customer_write_customers`
- `customer_read_orders`

These are **customer-side** scopes — they govern what the logged-in customer can read/write about themselves on their own account. Distinct from the **storefront-side** scopes (`read_customers`, `read_orders`, etc.) documented in [[headless-storefront-api]].

### Future: OAuth 2.0 PKCE — fields stored, middleware not yet enforcing

The presence of `client_id`, `client_secret_hash`, `scopes`, `callback_uris`, `js_origins`, and `logout_uri` is a forward-compatible scaffold. Once the storefront auth middleware shifts from email-code-only to full OAuth 2.0 PKCE, the existing records will carry the right shape. **Today** none of these OAuth-specific fields gate the auth flow (verify against current code).

### Customer account credentials are per-storefront

Each Nitrogen storefront has its own `nitro_customer_accounts` record. A customer logging in on Storefront A gets a JWT scoped to A's `client_id` — that JWT does NOT authenticate calls to Storefront B's `/api/sf` even if both storefronts read from the same CloudCart backend.

### Same `customer` entity underneath

Despite per-storefront `client_id` isolation, the underlying [[customer]] record is the same. So:

- A customer who registers on Storefront A and places an order sees that order on the legacy storefront too (if they log in via the legacy email/password flow).
- The merchant sees ONE customer in [[customers]] regardless of which storefront the customer used.

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-api]] — `/api/sf` GraphQL endpoint where customer-bound queries are made.
- [[headless-environment-variables]] — `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID` + `PUBLIC_CUSTOMER_ACCOUNT_API_URL` system vars.
- [[customer]] — the unified customer record backing every storefront.
- [[customers]] — admin view of customers across legacy + Nitrogen storefronts.
- [[nitrogen-storefront-overview]] — Customer Account API tab.

## Open Questions

- Exact mutation name + argument shape for the email-code flow (`customerAccessTokenCreate` is the assumed Shopify-shaped name — verify).
- Whether the JWT TTL is configurable per storefront or a global default.
- Timeline / status of full OAuth 2.0 PKCE enforcement (env-service comment says TODO).
- Whether username/password fallback will be added or remain email-code-only.
