---
type: feature
nav_path: "Apps → TikTok Ads → Settings"
route_name: apps.tiktok_ads.settings
route_path: /admin/apps/tiktok_ads/settings
aliases: ["TikTok Ads Settings", "TikTok Business config"]
tags: [apps, social, tiktok, ads, advertising, settings, oauth]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 2
---
# TikTok Ads → Settings

## Purpose

The **Settings** tab is where the merchant connects CloudCart to **TikTok for Business** — picks auth method (credentials OR OAuth), selects ad account, configures API access. See [[apps-tiktok-ads]] for the full feature set.

## Where to find it

Sidebar → Apps → TikTok Ads → **Settings tab**. Route: `/admin/apps/tiktok_ads/settings`.

## What the merchant can do here

### Two-stage workflow: paste developer-app credentials → save → Connect → OAuth

There is no "credentials path vs OAuth path" alternative — the saved fields are the **prerequisites** for the OAuth flow, not an alternative. The flow is:

**Stage 1 — TikTok Ads API Credentials box (always visible):**
- **App ID** (`app_id`) — required (min 3 chars), from business-api.tiktok.com.
- **App Secret** (`app_secret`) — required (min 3 chars).
- Save with the Submit Changes bar.

Until both are saved, the bottom card reads: *"Enter your App ID and App Secret above and save settings to enable the Connect button."*

**Stage 2 — Connect card (appears after credentials saved):**
- **Connect TikTok Ads** button — calls `/admin/api/tiktok_ads/connect`, redirects to TikTok's OAuth consent screen, returns via `apps.tiktok_ads.callback`. The callback exchanges `auth_code` for an access token and fetches the merchant's `advertiser_ids` list.
- If already connected: shows *"TikTok Ads account connected"* + the active `advertiser_id` + an outline-danger **Disconnect** button.

### Ad account selection

After OAuth, TikTok returns every `advertiser_id` the merchant has access to. The platform stores the full list in `advertiser_ids` and auto-selects the first as the active one. The merchant can change which advertiser is active by updating the `advertiser_id` setting (no re-OAuth needed).

### Disconnect

Clears OAuth access token + `advertiser_ids` list. **Preserves** `app_id` + `app_secret` (developer-portal credentials), so reconnect only requires re-running OAuth.

### What the merchant CANNOT do here
- Use without a TikTok for Business account + ad-account access.
- Manage individual campaigns from here (Campaign mgmt is in TikTok's Ads Manager UI).

## Settings & fields

Per [[apps-tiktok-ads]] — credentials-based auth is supported alongside OAuth, and the integration defines its own credential schema.

## Business rules

### OAuth is the only auth path (credentials are prerequisites)

There is no separate "credentials-only" mode. `app_id` + `app_secret` come from the merchant's TikTok developer app registration and are required BEFORE OAuth can run. The OAuth flow then authorizes the merchant's user against that app.

### Triple-app TikTok stack

Pairs with [[apps-tiktok-pixel]] (tracking) + [[apps-tiktok-shop]] (selling) for the full TikTok ecosystem.

### Permission
Standard apps permission scope.

## Related

- [[apps-tiktok-ads]] — hub.
- [[apps-tiktok-pixel]] — tracking sister app.
- [[apps-tiktok-shop]] — marketplace sister app.
- [[apps-google-dynamic]] — sister Google Ads platform.

## How it works (verified against backend)

### OAuth is the primary path — credentials are scaffolding

The **Connect** button always redirects to TikTok's OAuth, which requires the `app_id` to be filled in first. After the merchant authorizes on TikTok's side, TikTok redirects back with an `auth_code` that the platform swaps for a long-lived access token. The credentials fields (`advertiser_id`, `app_id`, `app_secret`) describe the **app registration credentials** the merchant gets from TikTok's developer portal — they are not an alternative to OAuth, they are the prerequisites for it. So in practice: paste `app_id` / `app_secret` from the TikTok developer portal first, then click Connect to run OAuth.

### Multi-ad-account — stored full list, one active at a time

On first authorization TikTok returns every `advertiser_id` the user has access to. CloudCart stores the full list in `advertiser_ids` and auto-selects the first one as the active `advertiser_id`. The merchant can change which advertiser is active by updating the setting (without re-doing OAuth). Each API call uses only the one currently-active advertiser — so the merchant cannot have two ad accounts active in parallel; switching mid-session means changing the active advertiser setting.

### Custom audiences push — supported via the Ads app

The merchant can build TikTok custom audiences by uploading a customer email list (or similar file types) and pushing it to TikTok for retargeting. The platform can also build lookalike audiences off a source audience for prospecting. This is wired through the Ads integration, not Pixel or Shop.

### No sandbox toggle — production API only

The API base URL is hardcoded to `https://business-api.tiktok.com/open_api/v1.3/` — there is no Settings option to switch to TikTok's sandbox. All ad-account, campaign, audience and report calls hit production. Merchants who want to test should use a real (low-budget / paused) ad account.

### Disconnect clears OAuth and advertiser list

Disconnecting removes both the OAuth access token and the `advertiser_ids` from settings. The `app_id` and `app_secret` (developer-portal credentials) stay, so reconnecting only requires re-running OAuth, not re-pasting the app keys.

### Form save whitelist — only these three credential fields persist

The save controller writes exactly `advertiser_id`, `app_id`, `app_secret` from the form. Any other field in the submission (e.g. tokens, advertiser_ids array) is discarded — those are managed via the OAuth callback and disconnect, not the settings form. The save also requires `app_id` and `app_secret` to be at least 3 characters or rejects with "App ID is required" / "App Secret is required" 422 errors.

### Connect button requires app_id to be saved first

The Connect endpoint (`apps.tiktok_ads.connect`) refuses to redirect if the merchant has not yet saved an `app_id` — it returns a 422 with "Missing app_id. Please configure TikTok Ads settings first." So the workflow is: paste app_id + app_secret, save the form, THEN click Connect to start OAuth. The button itself doesn't validate the app_id upfront in the UI — the redirect fails server-side if it's missing.

### State and rid params on the OAuth URL — CSRF protection

The OAuth authorize URL CloudCart builds includes `state` (CSRF token) and a unique `rid` (request ID via `uniqid`). TikTok returns `state` on callback for validation. The `rid` is just for TikTok's request tracking. The merchant doesn't configure these — they are generated per-redirect.

## Open questions
