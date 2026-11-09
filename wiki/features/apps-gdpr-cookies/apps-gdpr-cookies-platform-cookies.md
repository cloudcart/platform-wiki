---
type: feature
nav_path: "Apps → GDPR → Cookies → The platform's own cookies"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["Storefront cookie inventory", "CloudCart cookies list", "Cookie policy cookies", "_ccs", "_ccases", "uuid cookie", "XSRF-TOKEN", "ccchc", "cc-history", "cc cookie", "store_location cookie", "remember me cookie", "Бисквитки на платформата", "Списък с бисквитки за политика"]
tags: [apps, gdpr, cookies, consent, storefront, privacy]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---
# GDPR — Cookies: the platform's own cookies

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (bar & wall, groups, definitions, consent state).

## Purpose

The cookies a CloudCart storefront sets by itself, before any app or tracking code: what each is for, when it is set, how long it lives, and whether the visitor's cookie choice affects it. A merchant writing a cookie policy needs this list; the third-party cookies of tracking apps are on the merchant's own cookie definitions ([[apps-gdpr-cookies-definitions]]).

## Where to find it

There is no admin screen for these cookies. When the GDPR app is installed, its seed lists them under the **Strictly necessary** group (`system`), as two cookie entries: **CloudCart Platform** (`_ccs`, `cc`, `cc-cookie-consent`, `cc-history`, `ccchc`, `XSRF-TOKEN`) and **CloudCart Analytics** (`_ccases`, `uuid`). The merchant sees and can edit those entries in **Apps → GDPR → Cookies**.

## What the merchant can do here

- Copy the facts below into the store's cookie policy, or rely on the `{cookies_table}` placeholder, which prints the GDPR app's cookie entries on a page ([[apps-gdpr-cookies-definitions]]).
- Nothing else: none of these cookies can be switched off or renamed from the admin.

## Settings & fields

### Cookies every storefront sets

| Cookie | Set when | Lifetime | Purpose |
|---|---|---|---|
| `_ccs` | Every page | 7 days, renewed on each request | The store session: it ties the visitor to their cart and sign-in and keeps the visit's traffic source until an order. HttpOnly, Secure. |
| `XSRF-TOKEN` | Every page | 7 days, renewed on each request | Protects forms and requests against cross-site request forgery. |
| `uuid` | First page view of a visitor without one (not for crawlers) | 10 years | The visitor's ID for CloudCart Analytics, also used to connect forms, push subscriptions and orders to the same visitor. Secure, readable by scripts. |
| `_ccases` | With `uuid` | 10 years | The CloudCart Analytics session token issued with `uuid`. |
| `ccchc` | When the cart changes (add, remove, update) | 60 days | A fingerprint of the cart's contents. The checkout page compares it to notice that the cart changed in another tab. It does **not** identify the cart. |
| `cc`, `cc-history` | By the storefront script | Session (until the browser closes) | Created empty (`{}`) by the storefront's storage helper; the data itself (the pages visited in this tab, for the back navigation of side panels) is kept in the browser's local storage, not in the cookie. (verify) |
| `cc-cookie-consent` | When the visitor answers the cookie prompt (GDPR app only) | 180 days | The visitor's choice per cookie group. See [[apps-gdpr-cookies-consent-state]]. |

### Cookies set only in some cases

| Cookie | Set when | Lifetime |
|---|---|---|
| `remember_customer_…` (name ends in a hash) | A customer signs in with "remember me" | 400 days |
| `store_location` | A visitor picks a location in [[apps-store-locations]] | The app's cookie lifetime, 7 days by default; 1 day when set at checkout |
| `policies_popup` | A signed-in customer must re-accept the store's policies (GDPR app) | Until the popup is answered |

## Business rules

### None of these waits for the cookie prompt

All of them are set before, and regardless of, the visitor's answer. `uuid` and `_ccases` arrive with the first page, before any choice. Refusing every optional group deletes none of them: the GDPR app's cleanup only removes cookies listed under a declined group, and these are listed under **Strictly necessary**, which cannot be declined ([[apps-gdpr-cookies-groups]]).

### The guest cart is found through the session

A guest's cart is tied to the `_ccs` session, not to a cart cookie. There is no `_cart_key` cookie, and `ccchc` is only a content fingerprint. A guest who comes back after 7 days without a visit gets a new session and an empty cart; a signed-in customer gets the cart of the account ([[cart-entity-lifecycle]]).

### The classification is the seed's, the policy is the merchant's

The seed files these cookies as strictly necessary and describes CloudCart Analytics as anonymous visit statistics. Whether that classification suits the store's own cookie policy is for the merchant (and their lawyer) to decide; the entries can be edited or moved to another group in **Apps → GDPR → Cookies**, but moving them changes only the text shown to visitors, not when the cookies are set.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-consent-state]] — the consent cookie in detail.
- [[apps-gdpr-cookies-definitions]] — the cookie entries and the `{cookies_table}` placeholder.
- [[analytics-event-capture]] — what CloudCart Analytics records with `uuid`.
- [[cart-entity-lifecycle]] — cart lifetime and cleanup.

## Open questions

- That `cc` and `cc-history` are created by the storage helper's cookie fallback is read from the storefront script, not observed (verify).
