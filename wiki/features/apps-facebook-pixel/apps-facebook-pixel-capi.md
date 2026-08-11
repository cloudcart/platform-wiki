---
type: feature
nav_path: "Apps → XML Feed → Facebook → CAPI server-side"
route_name: apps.facebook.overview
route_path: /admin/apps/xml_feed/facebook
aliases: ["Facebook CAPI", "Meta Conversions API", "Facebook CAPI gating", "Facebook CAPI PII matching", "Facebook user_data", "Facebook server-side events"]
tags: [apps, facebook, meta, capi, conversions-api, tracking, gdpr, pii]
plan_gates: ["facebook.capi"]
created: 2026-06-10
updated: 2026-06-24
source_count: 4
---

> Part of [[apps-facebook-pixel]]. See the hub for the other aspects (event vocabulary, `event_source_url` known bug) and the settings tab.

# Facebook Pixel — server-side CAPI

## Purpose

This aspect documents the **server-side Conversions API leg**: when it fires (the gating conditions), how it matches the visitor to a Meta profile (the PII `user_data` fallback chain), and how failures are handled. CAPI is a server-side POST from CloudCart to Meta's API, complementing the browser pixel so conversions still reach Meta when the browser pixel is blocked (ad-blockers, iOS 14+ attribution loss).

## Where to find it

CAPI is enabled via the **Enable CAPI** toggle + **Access Token** on [[apps-facebook-pixel-settings]] (Sidebar → Apps → XML Feed → Facebook → Settings). There is no separate CAPI screen — it runs server-side once configured.

## What the merchant can do here

- Enable / disable the server-side CAPI leg (the **Enable CAPI** toggle, stored as `capi_status`).
- Supply the **Access Token** that authorises the server-side POST to Meta.
- Confirm server events arrive via Meta Events Manager → server events (not inside CloudCart).

### What the merchant CANNOT do here

- See CAPI errors in the admin — failures are logged silently server-side (see "Errors are logged silently" below); the only signal is Meta Events Manager → Diagnostics.
- Override the PII hashing or the `user_data` fallback order.
- Run CAPI from anything other than a same-origin storefront session (CSRF + admin exclusion below).
- Use more than one Pixel ID per store install.

## Settings & fields

See [[apps-facebook-pixel-settings]] — only `pixel`, `token`, `test_event_code`, `capi_status` are read by the CAPI controller.

## Business rules

### CAPI is gated by three conditions

Server-side CAPI fires only when ALL of these are true:

1. The merchant's plan includes the `facebook.capi` feature (see [[plan-features]]).
2. The merchant has filled **Access Token** AND switched the **Enable CAPI** toggle on in [[apps-facebook-pixel-settings]] (`capi_status = 1`).
3. The visitor has accepted the **Targeting** cookie group (per [[apps-gdpr-cookies]]).

If any gate fails, only the browser pixel fires (and the browser pixel itself is also gated by Targeting consent).

### Targeting cookie group gates BOTH legs

Both the browser pixel AND the server-side CAPI path check the `targeting` GDPR cookie group. If the visitor rejects the Targeting cookie category in the GDPR banner, neither path sends any data to Meta. See [[apps-gdpr-cookies]] for the cookie-group model.

### PII matching parameters

For each event, the server-side CAPI payload assembles **`user_data`** from the most-authoritative available source, in this fallback chain:

1. Logged-in customer — `email`, `phone`, first/last name, shipping or billing address (city, state, country ISO2, post code).
2. Cart's attached customer (when no auth but cart has a customer).
3. Authenticated subscriber from [[marketing-subscribers]] (`single_channel` — verified email / phone, country).
4. Browser-supplied fields from the AJAX request body (`customer_email`, `customer_phone`, `customer_first_name`, `customer_last_name`, `customer_city`, `customer_state`, `customer_country`, `customer_zip`).
5. GeoIP-derived `countryCode` (via [[platform-rate-limits]] MaxMind helper, ISO2 lowercased).

Each step only fills fields still empty — earlier sources take precedence. Meta's PHP SDK hashes these PII fields (SHA-256) before they leave the server.

Always included regardless of customer state:

- `client_ip_address` — the request's IP.
- `client_user_agent` — the `User-Agent` header (with an iOS 14+ string downgrade to "iPhone OS 13_2" to work around Meta's known iOS 14 attribution issues).
- `fbp` — the visitor's **`_fbp`** (Meta Browser ID), resolved in order from the **browser-forwarded value** in the request body (`data.fbp`) → the `_fbp` cookie → the session, with the format validated at each step. Only when no valid `_fbp` is found is one freshly minted (`fb.1.<ms>.<10-digits>`); whichever value wins is stored back into the cookie + session so subsequent events stay stable. Preferring the browser-forwarded value keeps the server event's `fbp` aligned with the browser pixel (better dedup / match quality) instead of fabricating a throwaway id.
- `fbc` (when available) — read from request body → `_fbc` cookie → session, validated against regex `/^fb\.1\.\d{13}\..+$/`. Invalid `_fbc` values are dropped, not sent.
- `external_id` — anonymous browser UUID from the storefront (matches the same `external_id` the browser pixel sends, so dedup works — see [[apps-facebook-pixel-events]]).

### Single Pixel ID per store

One Pixel ID per store install. Merchants advertising from multiple ad accounts that need separate pixels have to use [[apps-google-tags]] (GTM) and disable CAPI here.

### Pixel only fires on the storefront, not in admin

The pixel + CAPI relay runs only from the storefront — the admin panel is excluded, so admin previews never fire conversion events. The CAPI controller additionally rejects requests from authenticated admins (an authenticated admin ID short-circuits the response).

### CSRF token required on every CAPI call

The storefront-to-CloudCart leg (`POST /pixel/v2/{event}`) requires a valid `_token` (CSRF) in the request body. Anonymous requests without a token receive an empty JSON response. So the CAPI relay can only fire from same-origin storefront sessions; embedded iframes or external sites cannot trigger it.

### Errors are logged silently, never block the user

If the CAPI call to Meta fails (timeout, 5xx, invalid token), the exception is captured into the router logs entity ([[settings-hooks]] uses the same Logs model) with context `'Facebook CAPI error'` — the storefront page renders normally and the user sees no error. So a misconfigured Access Token degrades attribution but never breaks the checkout.

The CAPI POST is also **hard-bounded so a slow or unreachable Meta can never stall a storefront worker**: each server-side call uses **short timeouts (2 s connect / 3 s total)** — well under the worker's own request timeout — plus a **per-pixel circuit breaker**. After **3 consecutive failures** the breaker opens and further CAPI calls for that pixel are **skipped entirely (≈0 ms)** for a **60-second cooldown** before it retries. So a Meta outage costs at most a couple of slow requests, not a stalled checkout, and the browser pixel keeps firing throughout.

### Permission

Standard apps permission scope (any admin with Apps access can edit). CAPI access requires plan feature `facebook.capi`.

## Related

- [[apps-facebook-pixel]] — hub.
- [[apps-facebook-pixel-events]] — the event vocabulary + `event_id` dedup that CAPI sends.
- [[apps-facebook-pixel-event-source-url]] — the `event_source_url` known bug affecting some CAPI events.
- [[apps-facebook-pixel-settings]] — Enable CAPI toggle + Access Token.
- [[apps-gdpr-cookies]] / [[apps-gdpr-overview]] — Targeting cookie consent gating.
- [[plan-features]] — `facebook.capi` plan feature gate.
- [[marketing-subscribers]] — subscriber PII fallback (channel-verified email/phone).
- [[platform-rate-limits]] — GeoIP fallback for `countryCode` (MaxMind).
- [[settings-hooks]] — shares the router Logs model where `Facebook CAPI error` is recorded.
- [[apps-google-tags]] — GTM alternative for multi-pixel routing.

## Open questions

- **(verify)** The Meta Graph API version used by the bundled FB SDK — older SDK versions hit deprecated `v<X>` endpoints. Confirm which version is in the active composer-locked `facebook/php-business-sdk`.
- **(verify)** The CAPI controller hard-codes the `website` action source — but the same integration may fire from in-app browsers (Facebook IAB, Instagram IAB). Should some events use `chat` or `email` action source instead? Currently always `website`.
- **(verify)** Are CAPI errors surfaced anywhere in the admin? The merchant's only signal today is Meta Events Manager → Diagnostics — no in-admin alert.
