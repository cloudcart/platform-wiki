---
type: feature
nav_path: "Apps → OLX → Connection model"
route_name: apps.olx.settings
route_path: /admin/apps/olx/settings
aliases: ["OLX connection", "OLX OAuth", "OLX multi-country", "OLX endpoints", "OLX token lifetime", "OLX re-authorize"]
tags: [apps, olx, marketplace, oauth, connection, multi-country]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX — connection & authorization model

> Part of [[apps-olx]]. See the hub for the other aspects (sync, advert format, publishing).

## Purpose

How CloudCart connects to OLX: which markets are reachable, how credentials are scoped per country, the two-token OAuth model behind the **Connect** button, and how token expiry silently gates every OLX operation. This is the aspect to read for "why can't I connect my country?", "why did my adverts stop publishing?", and "do I have to re-authorize?".

## Where to find it

Sidebar → Apps → OLX → **Settings tab**. Route: `/admin/apps/olx/settings`. The connection lives on [[apps-olx-settings]]; this page explains the verified mechanics behind that screen.

## What the merchant can do here

- Pick **which country's OLX** to connect (the `endpoint_id` / Country field).
- Authorize CloudCart against the merchant's OLX account via the **Connect** button (OAuth handshake).
- Configure **multiple OLX accounts** in the same integration — one per OLX country — because credentials are per-endpoint.
- Re-authorize when the token has expired.

## Settings & fields

### Multi-country / per-endpoint credential model

Credentials are **per-endpoint** (per OLX country). OLX runs a separate API per country (e.g. `olx.bg`, `olx.ro`, `olx.pl`, `olx.ua`), and the merchant configures credentials per endpoint. This means the **same CloudCart store can publish to OLX BG and OLX RO simultaneously** — multi-country OLX is supported.

**Currently only Bulgaria (`OLX_BG`) and Romania (`OLX_RO`) are active in production.** Other countries (Poland, Ukraine, Portugal, Kazakhstan, Belarus, Angola, Mozambique) are present in the codebase and appear in the country dropdown via language files, but their API credentials are commented out in config — they cannot be connected today.

### Two-token auth model — partner credentials AND merchant user OAuth

OLX needs **both** of two separate, separately-stored tokens:

1. **Partner credentials** — CloudCart's shared `client_id` + `client_secret` per country, used for `client_credentials` flows that fetch OLX-side public data (categories, regions, cities).
2. **Per-merchant OAuth user token** — obtained via the `authorization_code` flow, used to advertise on the merchant's own OLX account. The merchant's user token carries read + write + v2 scope.

### CloudCart Socialite handles the OAuth redirect (external service)

The merchant's OAuth flow does **not** redirect directly to OLX — it routes through `config('url.domains.cc_socialite') . '/redirect/{site_id}/olx/{endpoint_id}'`, a CloudCart-hosted intermediary. The practical effect: CloudCart registers a single OLX developer application centrally, and the redirect URL is identical for all stores. **Merchants do not need to register their own OLX developer app** (verify whether the intermediary domain is configurable per environment).

## Business rules

### Refresh token lasts 1 month from issuance

When an access token expires, CloudCart uses the refresh token to obtain a new one. The **refresh token itself is valid for 1 month** (`+1 month`). Each successful access-token refresh extends the refresh-token validity another month. **If the merchant makes no OLX-related action for over a month, the refresh token expires and the merchant must re-authorize.** This is the most common cause of an integration that "worked and then quietly stopped".

### Token check is silent on a missing or expired token

The internal token validity check returns false when the refresh token is missing, the validate-token is missing, or the validate-token has expired. The integration uses this check to gate **all** OLX-side operations — and in many code paths it **silently returns without surfacing a "please reconnect" message**. The merchant has to notice that adverts simply aren't publishing. When a merchant reports "nothing is syncing", re-authorizing on [[apps-olx-settings]] is the first thing to try.

## Related

- [[apps-olx]] — hub.
- [[apps-olx-settings]] — the Settings tab where the merchant connects + re-authorizes.
- [[apps-olx-history]] — operation log; surfaces auth-related rejection responses.
- [[apps]] — App Store.

## Open questions

- Whether the Socialite intermediary domain (`cc_socialite`) is environment-specific or fixed (verify).
