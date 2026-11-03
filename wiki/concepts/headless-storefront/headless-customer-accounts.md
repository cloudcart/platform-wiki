---
type: concept
nav_path: "Concept → Headless storefronts → Customer Account API"
aliases: ["Customer Account API", "Headless login", "Email-code login", "Passwordless headless login", "customerLoginCodeSend", "customerLoginCodeVerify", "customerCreate", "TOKEN_INVALID", "CUSTOMER_DISABLED", "PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID", "Customer JWT", "Вход с код", "Регистрация през API"]
tags: [nitrogen, headless, customer, authentication, oauth, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Nova platform, Storefront API, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — Customer Account API

## Definition

The **Customer Account API** is the customer sign-in part of the [[headless-storefront-api]] that Nitrogen storefronts use to log customers in; it is not a separate endpoint. The auth flow is **passwordless 6-digit email code** — the customer enters their email, receives a code, exchanges it for a customer access token (a JWT), then sends that token with later calls to the Storefront API.

The customer's underlying account, addresses, orders, and saved data are the **same as on the legacy CloudCart storefront**. The Customer Account API is just the headless-app-facing entry point for that data; the records themselves live in the unified [[customer]] table.

## Scope

Covered:

- The 6-digit-email-code login flow, its limits and refusals.
- The `customerLoginCodeSend` and `customerLoginCodeVerify` mutations against `/api/sf`.
- Registration through `customerCreate`.
- How customer auth interacts with the Storefront API.

Not covered:

- The legacy storefront's customer login — that's the theme's path; see [[checkout-step-customer]] for its code.
- The `customer` entity's data model — see [[customer]].
- A guest who types a registered e-mail at the cart — see [[headless-cart-rules]].

## Contrasts

- **Customer JWT vs Storefront API token** — the storefront token (`X-Storefront-Access-Token`, or the private token in `X-Storefront-Private-Token`) names the store; the customer access token identifies the CUSTOMER. Operations on customer data take it as their `customerAccessToken` argument; sent as `Authorization: Bearer <token>` (or in the operation's `@inContext(buyer:)`), it runs the whole request as that customer. See [[headless-storefront-api]].
- **Same data backs every storefront** — a customer who has an account on the legacy CloudCart storefront sees the same orders / addresses / wishlist on a Nitrogen storefront that points at the same CloudCart backend (with the customer's access token).

## Where it applies

### Customer Accounts set-up (no longer needed)

Sign-in by email code needs nothing set up in the admin. The admin no longer has a Customer Account API tab on [[nitrogen-storefront-overview]]; its old address opens the storefront's General settings. A storefront set up before that tab was removed still has two read-only variables, `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID` and `PUBLIC_CUSTOMER_ACCOUNT_API_URL` (see [[headless-environment-variables]]), which sign-in does not read.

### The 6-digit email code flow

The active login flow is passwordless:

1. Customer enters their email on the merchant's Nitrogen storefront.
2. Storefront calls `customerLoginCodeSend` with the email. The call always succeeds, so it does not reveal who has an account. A code is mailed only to an active, non-guest customer.
3. Customer enters the code from the e-mail.
4. Storefront calls `customerLoginCodeVerify` with `email + code`; CloudCart returns a **customer access token** (a JWT) and its expiry. The token's lifetime is the same for every storefront.
5. Storefront stores the token (typically in an HttpOnly cookie) and sends it with later calls — as the `customerAccessToken` argument of the customer operations, or as `Authorization: Bearer <token>`.

This is the **only** customer sign-in flow of the Storefront API, by design: it has no password sign-in and no password reset (the classic storefront keeps both).

### Limits and refusals

- A code lives 60 minutes and takes 5 tries, right or wrong, and then stops working: ask for a new one.
- A pending code is mailed again at most once a minute per address.
- A visitor may ask for a code 10 times a minute, and try one 10 times a minute. Past that the answer is `THROTTLED`, for any address (see [[headless-storefront-limits]]).

`customerLoginCodeVerify` refuses in the store's language:

| Code | When | Message (en / bg) |
|---|---|---|
| `TOKEN_INVALID` | A wrong or used code | "Code is invalid" / "Кодът е невалиден" |
| `TOKEN_INVALID` | An expired code, or the right code past its tries | "Code is expired" / "Кодът е изтекъл" |
| `CUSTOMER_DISABLED` | A disabled or banned account | "Your user account is not active" / "Вашият потребителски профил не е активен" |

### Registration

`customerCreate` runs the store's own registration, without a password: the default customer group, the welcome e-mail with no password in it, account confirmation as the store's settings say, the merchant's notice and the `customer.created` webhook. A login code is mailed after creation.

- A registered customer's e-mail is `TAKEN`.
- An e-mail left by a guest's order becomes the account, keeping the guest's orders and addresses and the details the input leaves out. `customer` is then null: read it after signing in with the code.
- A refusal of the platform's validation is a user error on `input.email`.
- A visitor may register 10 times a minute.

See [[customer-register]] for the classic storefront's form.

### Customer JWT carried alongside the storefront token

Once the customer has a token, the operations on their own data (orders, profile, wishlist, addresses) take it as their `customerAccessToken` argument, while the storefront names the store as usual:

- `X-Storefront-Access-Token: <public-storefront-token>` (or the private token in `X-Storefront-Private-Token`, from the storefront's server) — identifies the storefront.
- `Authorization: Bearer <customer-token>` — optional; runs the whole request as that customer (their prices, discounts and checkout hand-off).

Without a valid token, `customer` answers null and the customer mutations answer `TOKEN_INVALID`.

### Customer account credentials are per-storefront

Each Nitrogen storefront has its own signing key for customer tokens, made when the storefront is created. A customer logging in on Storefront A gets a token signed with A's key — that token does NOT authenticate calls made with Storefront B's storefront token, even though both storefronts read from the same CloudCart backend. A token from another store is refused too.

### Same `customer` entity underneath

Despite per-storefront token isolation, the underlying [[customer]] record is the same. So:

- A customer who registers on Storefront A and places an order sees that order on the legacy storefront too (if they log in via the legacy email/password flow).
- The merchant sees ONE customer in [[customers]] regardless of which storefront the customer used.

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-api]] — `/api/sf` GraphQL endpoint where customer-bound queries are made.
- [[headless-environment-variables]] — the two older read-only variables.
- [[headless-storefront-limits]] — the per-visitor limits.
- [[headless-cart-rules]] — who the buyer of a cart is.
- [[headless-checkout-submit]] — signing in through the web checkout hand-off.
- [[customer]] — the unified customer record backing every storefront.
- [[customers]] — admin view of customers across legacy + Nitrogen storefronts.
- [[nitrogen-storefront-overview]] — storefront settings (the Customer Account API tab was removed).

## Open Questions

_None._
