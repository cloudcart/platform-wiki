---
type: feature
nav_path: "Apps → TikTok Shop → Connection (OAuth / shop cipher)"
route_name: apps.tiktok_shop.callback
route_path: /admin/apps/tiktok_shop/callback
aliases: ["TikTok Shop OAuth", "TikTok Shop connection", "TikTok shop cipher", "TikTok Shop token refresh", "TikTok Shop disconnect"]
tags: [apps, social, tiktok, oauth, marketplace, plan-gated]
plan_gates: ["tiktok_shop_export"]
created: 2026-06-10
updated: 2026-06-18
source_count: 3
---

> Part of [[apps-tiktok-shop]]. See the hub for the other aspects (product mapping, export & sync).

# TikTok Shop — connection (OAuth, shop cipher, token refresh)

## Purpose

This aspect covers **how CloudCart authenticates to the merchant's TikTok Shop seller account** and keeps that connection alive. Every product push depends on a valid OAuth session — without one, every export silently succeeds with empty results. This page explains the connect flow, the per-shop identifier (`shop_cipher`), automatic token refresh, the region implication, and disconnect.

The merchant performs the connect action on the [[apps-tiktok-shop-settings]] tab; this page documents what happens behind that button.

## Where to find it

Sidebar → Apps → install → **TikTok Shop** → **Settings** tab → **Sign in with TikTok**. The OAuth round-trip returns to the `apps.tiktok_shop.callback` route, after which the merchant is back on the Settings tab with the connection shown as active.

## What the merchant can do here

- **OAuth Connect** — *Sign in with TikTok* button authorizes CloudCart to push products to the merchant's TikTok Shop.
- **See connected shop** — after connect, the Settings tab shows the resolved shop name.
- **Disconnect** — clears stored tokens and the `shop_cipher` setting; product pushes stop working until the merchant reconnects.

What the merchant CANNOT do here:

- **Pick which shop** to publish to when one TikTok login owns several shops — there is no shop-picker (see Business rules).
- **Pick a region** — region is inherited from the seller account, not chosen in CloudCart.
- Connect without a TikTok Shop merchant account or without the `tiktok_shop_export` plan feature.

## Settings & fields

App key: `tiktok_shop`. Plan-feature key: `tiktok_shop_export`.

Connection-related stored settings:

- `app_key` / `app_secret` — **platform-level** TikTok app credentials, held in CloudCart config (`TIKTOK_SHOP_APP_KEY` / `TIKTOK_SHOP_APP_SECRET` / `TIKTOK_SHOP_AUTH_HOST`), the single app CloudCart registered with TikTok. These are **NOT** per-merchant settings — the merchant never enters them; the same secret also validates inbound webhooks.
- `shop_cipher` — TikTok's internal identifier for the specific shop CloudCart pushes to. Stored after OAuth; cleared on disconnect.
- `shop_name` — display name of the connected shop, saved alongside the cipher.
- Stored access token + refresh token — managed automatically; not merchant-editable in normal use.

## Business rules

### Single platform OAuth app — merchants supply no credentials

CloudCart authenticates through **one platform-wide TikTok Shop app** that CloudCart registered with TikTok (credentials in `TIKTOK_SHOP_APP_KEY` / `TIKTOK_SHOP_APP_SECRET` / `TIKTOK_SHOP_AUTH_HOST` config). The merchant never pastes an App Key / App Secret — they only click *Sign in with TikTok*, and the OAuth round-trip is brokered through CloudCart's `cc-socialite` service. If the platform credentials are not configured, the connect URL is `null` and the *Sign in with TikTok* button is hidden rather than producing a broken redirect.

### OAuth-protected operations

All TikTok API calls require an active OAuth session. TikTok tokens have a limited lifetime; refresh is handled automatically when the integration loads its client (see token auto-refresh below).

### Shop cipher per shop

A single TikTok seller account can own multiple shops. The `shop_cipher` identifies which specific shop CloudCart publishes to. It is stored on app activation/connect and cleared on disconnect.

### After OAuth callback, CloudCart auto-fetches the authorized shops and stores the FIRST cipher

The callback handler fetches the authorized shops after the token exchange. The **first** shop in the returned list is automatically saved as `shop_cipher`, and its name as `shop_name`. Merchants with multiple TikTok Shop accounts under one TikTok login get whichever shop TikTok returns first — **there is no UI shop-picker**. To use a different shop, the merchant has to disconnect, re-authorize, and hope TikTok returns the desired shop first (or manually edit the `shop_cipher` setting).

### Token auto-refresh, refreshed 1 hour before expiry

When the stored access token is within 1 hour of expiring, the integration auto-calls the refresh endpoint using the stored refresh token. If the refresh fails, the client is null and operations silently skip — nothing is pushed and no error surfaces in the UI.

### TikTok API client init returns null on missing credentials — no exception

A central client factory returns the configured TikTok client with the current OAuth token, but returns `null` if the platform TikTok app credentials are not configured, if no access token is stored, or if the token refresh fails. All subsequent operations check for null and skip silently — no exception is thrown. So an expired token causes uploads to "succeed with empty results" rather than fail loudly; the merchant has to check the status endpoint or the system logs to learn what happened. Every TikTok API call routes through this factory.

### Region is inherited from the TikTok Shop seller account

CloudCart has no region picker (US / UK / SEA / Bulgaria / etc.). The region is whatever the merchant's TikTok Shop seller account is registered in — when the merchant connects via OAuth, TikTok returns the `shop_cipher` for that specific shop and CloudCart pushes products there. Merchants who operate in multiple regions need separate TikTok seller accounts and would reconnect to switch.

### Disconnect

Disconnect clears the stored tokens and the `shop_cipher` setting. Existing TikTok-side listings are not removed by disconnect; CloudCart simply stops being able to push updates until the merchant reconnects.

### Permission

Standard apps permission scope.

## Related

- [[apps-tiktok-shop]] — hub.
- [[apps-tiktok-shop-settings]] — the Settings tab where the merchant clicks Connect / Disconnect.
- [[apps-google-shopping]] — architecturally similar OAuth + Merchant Center model.
- [[plan-gates]] — `tiktok_shop_export` plan-gating.

## Open questions

None.
