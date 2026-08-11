---
type: feature
nav_path: "Apps → TikTok Shop → Settings"
route_name: apps.tiktok_shop.settings
route_path: /admin/apps/tiktok_shop/settings
aliases: ["TikTok Shop Settings", "TTS settings", "TikTok Shop config"]
tags: [apps, social, tiktok, settings, oauth, marketplace]
plan_gates: ["tiktok_shop_export"]
created: 2026-05-21
updated: 2026-06-18
source_count: 3
---
# TikTok Shop → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to their TikTok Shop account via OAuth and turns on automatic product sync. After valid configuration, the merchant can push products via [[apps-tiktok-shop-products]]. For the full TikTok Shop feature set, see [[apps-tiktok-shop]].

## Where to find it

Sidebar → Apps → TikTok Shop → **Settings tab**. Route: `/admin/apps/tiktok_shop/settings`.

## What the merchant can do here

Connecting is a **single step** — the merchant just clicks Connect and authorises via TikTok. CloudCart now uses a **single platform-wide TikTok Shop app** (registered by CloudCart with TikTok; credentials held in platform configuration), so **the merchant no longer enters any App Key / App Secret**.

**Connect card:**
- If not yet authorized: a dark **Connect TikTok Shop** button. Clicking it redirects the browser to TikTok's OAuth consent page (through CloudCart's `cc-socialite` OAuth broker). After approval, TikTok redirects back; CloudCart exchanges the code for an access + refresh token and auto-resolves the authorised shop (storing its `shop_cipher` and `shop_name`).
- If TikTok Shop OAuth is not configured at the platform level yet, the Connect button is unavailable (the integration shows a "not available" state instead of a broken redirect).
- If already connected: shows the TikTok icon + shop name (e.g. *"My Shop BG"*) + an outline-danger **Disconnect** button.

**Product Sync Settings box (only visible after OAuth):**
- **Auto-sync product updates** (`update_products`) — see Settings & fields below.

**Disconnect** — clears the OAuth tokens, `shop_cipher`, and `shop_name`. It **preserves** `update_products`, `filter_group`, and `filter_group_value`, so reconnecting only requires re-running OAuth.

### What the merchant CANNOT do here
- Use TikTok Shop without an active TikTok Business + TikTok Shop seller account.
- Connect multiple TikTok accounts simultaneously — one account per CloudCart store.
- Pick a shop, region, currency, language, or category mapping. There is no shop-cipher selector, no region picker, and no category/currency/language picker — TikTok Shop is product-export-only and inherits all of these from the connected TikTok shop's own settings. The `shop_cipher` is auto-set from the first shop TikTok returns at OAuth; to use a different shop the merchant must Disconnect and re-authorize.
- Push products from this page — that's [[apps-tiktok-shop-products]].

## Settings & fields

| Field | Type | Notes |
|---|---|---|
| **Auto-sync product updates** (`update_products`) | Switch (1/0) | When ON, any product create / update or variant change triggers an immediate TikTok push. When OFF, the merchant must push manually from the Products tab. |
| `update_columns` | Array (internal) | Which product column changes are treated as a change that triggers auto-sync. Set together with the auto-sync switch. |
| `filter_group` / `filter_group_value` | Stored config | Intended to restrict which products are eligible for export. See Business rules — currently not enforced. |

The Save action persists only these fields (`update_products`, `update_columns`, `filter_group`, `filter_group_value`); any other submitted field is discarded.

**The TikTok app credentials (`app_key` / `app_secret`) are NOT merchant settings** — they live in CloudCart's platform configuration (`TIKTOK_SHOP_APP_KEY` / `TIKTOK_SHOP_APP_SECRET` / `TIKTOK_SHOP_AUTH_HOST` env), the single TikTok Shop app CloudCart registered with TikTok. Merchants never see or enter them; the same platform secret is what verifies the HMAC-SHA-256 signature on incoming TikTok webhooks.

**OAuth state** — once connected, the tab stores the access token, refresh token, and the shop's `shop_cipher` and `shop_name`. The `shop_cipher` scopes every API call to that one shop. Tokens are stored encrypted.

**Plan-gating** — plan feature key `tiktok_shop_export`. Merchants without this feature can install the app but cannot push products.

## Business rules

### Single shop per store
The `shop_cipher` is a single value — one CloudCart store maps to one TikTok shop. Multi-shop or multi-region merchants need separate CloudCart stores. There is no in-UI shop switcher; the only way to change the active shop is to Disconnect and re-authorize.

### Switching shops does not migrate already-synced products
The local record of what was pushed keeps the product IDs from the OLD shop. After connecting a different shop, those mappings still exist locally but no longer correspond to anything in the new shop. CloudCart does not auto-republish — the merchant must push products again from the [[apps-tiktok-shop-products]] tab.

### Token auto-refresh — refreshes 1 hour before expiry
When the stored token is within 1 hour of expiring and a refresh token exists, CloudCart refreshes automatically and saves the new tokens and expiry. If the refresh fails (e.g. the merchant revoked CloudCart in TikTok Seller Center), operations skip silently and the merchant must Reconnect.

### Auto-sync switch gates updates, but not deletes
With `update_products` OFF, no automatic re-sync runs when products or variants are edited — the merchant must push manually. With it ON, any product create / update or variant change fires an immediate push. **Deletes always propagate to TikTok regardless of this setting** — deleting the CloudCart product auto-removes the TikTok listing.

### Product filter is configurable but not yet enforced
`filter_group` / `filter_group_value` are saved from this tab, but the export query does not currently apply them. Today **all active products are eligible for export** regardless of the filter values. (verify — track whether this becomes enforced.)

### Order webhooks are received but orders are not imported
TikTok sends webhook events for order status changes (type 1), product status changes (type 2), and return status changes (type 3). CloudCart verifies each event's HMAC-SHA-256 signature against the **platform** TikTok app secret (config, not a merchant-entered value), then logs it. **Orders placed on TikTok Shop are not imported into the CloudCart [[orders]] list** — the integration is product-export-only on the order side.

### Side effects on Connect
Tokens are persisted, the shop is fetched and stored, and the other TikTok Shop tabs unlock.

## Related

- [[apps-tiktok-shop]] — TikTok Shop hub.
- [[apps-tiktok-shop-products]] — products + push.
- [[apps-tiktok-ads]] — sister TikTok app (advertising).
- [[apps-tiktok-pixel]] — sister TikTok app (tracking).

## Open questions

- Will `filter_group` / `filter_group_value` eventually restrict the export query, or be removed from the UI?
