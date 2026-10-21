---
type: concept
nav_path: "Concept → Headless storefronts → Customer Account API"
aliases: ["Customer Account API", "Headless login", "Email-code login", "Passwordless headless login", "customerLoginCodeSend", "customerLoginCodeVerify", "nitro_customer_accounts", "PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID", "Customer JWT"]
tags: [nitrogen, headless, customer, authentication, oauth, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-10-21
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Nova platform, Storefront API, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Customer Account API

## Definition

The **Customer Account API** is the customer sign-in part of the [[headless-storefront-api]] that Nitrogen storefronts use to log customers in; it is not a separate endpoint. The auth flow is **passwordless 6-digit email code** — the customer enters their email, receives a code, exchanges it for a customer access token (a JWT), then sends that token with later calls to the Storefront API.

The customer's underlying account, addresses, orders, and saved data are the **same as on the legacy CloudCart storefront**. The Customer Account API is just the headless-app-facing entry point for that data; the records themselves live in the unified [[customer]] table.

## Scope

Covered:

- The 6-digit-email-code login flow.
- The `customerLoginCodeSend` and `customerLoginCodeVerify` mutations against `/api/sf`.
- The `nitro_customer_accounts` record + the OAuth fields it stores (currently unused).
- Default scopes at creation.
- System env vars exposed when customer accounts are enabled.
- How customer auth interacts with the Storefront API.

Not covered:

- The legacy storefront's customer login (cookie-based session) — that's the legacy theme path; Nitrogen doesn't use it.
- The `customer` entity's data model — see [[customer]].
- OAuth 2.0 PKCE flow (scopes, callback URIs, JS origins, logout URI) — fields stored but not read by sign-in.

## Contrasts

- **Email-code login (active) vs OAuth 2.0 PKCE (stored-not-enforced)** — the OAuth-shaped fields (`client_id`, `client_secret_hash`, `client_secret_prefix`, `scopes`, `callback_uris`, `js_origins`, `logout_uri`) all exist on the `nitro_customer_accounts` record. Sign-in does not read them, and the admin no longer has a screen for them: sign-in by email code needs nothing set up.
- **Customer JWT vs Storefront API token** — the storefront token (`X-Storefront-Access-Token`, or the private token in `X-Storefront-Private-Token`) names the store; the customer access token identifies the CUSTOMER. Operations on customer data take it as their `customerAccessToken` argument; sent as `Authorization: Bearer <token>` (or in the operation's `@inContext(buyer:)`), it runs the whole request as that customer. See [[headless-storefront-api]].
- **Same data backs every storefront** — a customer who has an account on the legacy CloudCart storefront sees the same orders / addresses / wishlist on a Nitrogen storefront that points at the same CloudCart backend (with the customer's access token; the storefront's scopes are not checked).

## Where it applies

### Customer Accounts set-up (no longer needed)

Sign-in by email code needs nothing set up in the admin. The admin no longer has a Customer Account API tab on [[nitrogen-storefront-overview]]; its old address opens the storefront's General settings.

A storefront whose customer account was set up before that tab was removed still has a `nitro_customer_accounts` record (default scopes and a generated `client_id` + `client_secret`). For it, the platform still writes two system env vars (see [[headless-environment-variables]]), which sign-in does not read:
   - `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID`
   - `PUBLIC_CUSTOMER_ACCOUNT_API_URL`

### The 6-digit email code flow

The active login flow is passwordless:

1. Customer enters their email on the merchant's Nitrogen storefront.
2. Storefront calls `customerLoginCodeSend` with the email against `/api/sf`.
3. CloudCart emails a 6-digit code to the customer's address — only when the email belongs to an active customer with an account. The answer is the same either way, so it does not reveal who has an account. A pending code is mailed again at most once a minute.
4. Customer enters the code in the storefront app.
5. Storefront calls `customerLoginCodeVerify` with `email + code`; CloudCart returns a **customer access token** (a JWT) and its expiry. A code allows 5 tries. The token's lifetime is the same for every storefront.
6. Storefront stores the token (typically in an HttpOnly cookie) and sends it with later calls — as the `customerAccessToken` argument of the customer operations, or as `Authorization: Bearer <token>`.

This is the **only** customer sign-in flow of the Storefront API, by design: it has no password sign-in and no password reset (the classic storefront keeps both).

### Customer JWT carried alongside the storefront token

Once the customer has a token, the operations on their own data (orders, profile, wishlist, addresses) take it as their `customerAccessToken` argument, while the storefront names the store as usual:

- `X-Storefront-Access-Token: <public-storefront-token>` (or the private token in `X-Storefront-Private-Token`, from the storefront's server) — identifies the storefront.
- `Authorization: Bearer <customer-token>` — optional; runs the whole request as that customer (their prices, discounts and checkout hand-off).

Without a valid token, `customer` answers null and the customer mutations answer `TOKEN_INVALID`; the storefront's scopes play no part.

### `nitro_customer_accounts` record fields

The record stores OAuth-style fields (verify exact column names):

- `client_id` — UUID, public.
- `client_secret_hash` — SHA-256 of a raw secret prefixed `cc_cas_`.
- `client_secret_prefix` — 15 chars, for masked display.
- `scopes` — array; defaults below.
- `callback_uris` — array of allowed OAuth redirect URIs (not enforced yet).
- `js_origins` — array of allowed JS origins (not enforced yet).
- `logout_uri` — single URI (not enforced yet).

Sign-in reads none of these fields. (The private storefront token, by contrast, is enforced — see [[headless-storefront-api]].)

### Default scopes at creation

When customer accounts are enabled, defaults are:

- `customer_read_customers`
- `customer_write_customers`
- `customer_read_orders`

These are **customer-side** scopes, stored on the record; nothing reads them, so they do not limit what a signed-in customer can read or change on their own account. Distinct from the **storefront-side** scopes (`read_customers`, `read_orders`, etc.) documented in [[headless-storefront-api]].

### Future: OAuth 2.0 PKCE — fields stored, middleware not yet enforcing

The presence of `client_id`, `client_secret_hash`, `scopes`, `callback_uris`, `js_origins`, and `logout_uri` is a forward-compatible scaffold. Once the storefront auth middleware shifts from email-code-only to full OAuth 2.0 PKCE, the existing records will carry the right shape. **Today** none of these OAuth-specific fields gate the auth flow.

### Customer account credentials are per-storefront

Each Nitrogen storefront has its own signing key for customer tokens, made when the storefront is created. A customer logging in on Storefront A gets a token signed with A's key — that token does NOT authenticate calls made with Storefront B's storefront token, even though both storefronts read from the same CloudCart backend. A token from another store is refused too.

### Same `customer` entity underneath

Despite per-storefront token isolation, the underlying [[customer]] record is the same. So:

- A customer who registers on Storefront A and places an order sees that order on the legacy storefront too (if they log in via the legacy email/password flow).
- The merchant sees ONE customer in [[customers]] regardless of which storefront the customer used.

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-api]] — `/api/sf` GraphQL endpoint where customer-bound queries are made.
- [[headless-environment-variables]] — `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID` + `PUBLIC_CUSTOMER_ACCOUNT_API_URL` system vars.
- [[customer]] — the unified customer record backing every storefront.
- [[customers]] — admin view of customers across legacy + Nitrogen storefronts.
- [[nitrogen-storefront-overview]] — storefront settings (the Customer Account API tab was removed).

## Open Questions

- Timeline / status of full OAuth 2.0 PKCE enforcement (no such work is visible in the code).

