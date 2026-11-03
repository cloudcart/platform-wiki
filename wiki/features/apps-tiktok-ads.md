---
type: feature
nav_path: "Apps → TikTok Ads"
route_name: apps.tiktok_ads.overview
route_path: /admin/apps/tiktok_ads
aliases: ["TikTok Ads", "TikTok Advertising", "TikTok Business", "TikTok Marketing"]
tags: [apps, social, tiktok, advertising, oauth]
plan_gates: []
created: 2026-05-22
updated: 2026-06-11
source_count: 2
---
# TikTok Ads (advertising platform integration)

## Purpose

**TikTok Ads** connects CloudCart to **TikTok for Business** (TikTok's advertising platform). It is distinct from [[apps-tiktok-shop]] (selling on TikTok) and [[apps-tiktok-pixel]] (tracking) — this app handles the ADVERTISING workflows: authorizing CloudCart with the merchant's TikTok for Business account, then managing ad accounts, campaigns, custom audiences, and performance reports from inside CloudCart.

Run all three TikTok apps together for a closed loop: [[apps-tiktok-pixel]] tracks visitors → [[apps-tiktok-shop]] promotes the catalog → this app runs ads against the pixel + catalog data, with conversions measured back via the pixel.

## Where to find it

Sidebar → Apps → install → **TikTok Ads**. See [[apps-tiktok-ads-settings]] for configuration.

## What the merchant can do here

- **Connect** CloudCart to a TikTok for Business account (OAuth consent flow).
- Select the active **ad account** (advertiser) when the account has more than one.
- **List, create, look up, and update campaigns** (rename, change budget, pause, activate) without opening TikTok Ads Manager.
- **Pull performance reports** by date range — spend, impressions, clicks, conversions, ROI.
- **Manage custom audiences** — list, create from an uploaded customer file, and build lookalike audiences for retargeting and prospecting.

### What the merchant CANNOT do here

- Use the app without a TikTok for Business account.
- Connect by credentials alone — the developer-app credentials are a prerequisite for OAuth, not a separate login path (see Business rules).
- Push the product catalog here — catalog/feed sync to TikTok lives in [[apps-tiktok-shop]]. This app handles ad accounts, campaigns, audiences, and reports only.
- Switch to a sandbox / test environment — all calls hit production (see Business rules).

## Settings & fields

App key: `tiktok_ads`.

The connection is a **two-stage flow**:

1. Paste the TikTok developer-app `app_id` and `app_secret` (issued at business-api.tiktok.com), then save.
2. Click **Connect** to run the OAuth consent flow on TikTok's user-authorization screen.

| Field | What it controls |
|---|---|
| `app_id` | TikTok developer-portal app ID. Prerequisite for the OAuth flow. |
| `app_secret` | The corresponding app secret. Prerequisite for the OAuth flow. |
| `advertiser_ids` | The full list of ad accounts the authorized user can access, fetched on connect. Stored, not edited directly. |
| `advertiser_id` | The single **active** ad account used for every request. Switchable without re-authorizing. |

After consent, TikTok redirects to the callback (route `apps.tiktok_ads.callback`), which exchanges the authorization code for an access token and fetches the merchant's full `advertiser_ids` list. **Disconnect** clears the OAuth token and `advertiser_ids` but preserves the saved `app_id` / `app_secret`.

## Business rules

### OAuth-only auth — credentials are prerequisites, not an alternative

There is no credentials-only mode. The merchant pastes `app_id` and `app_secret` first, saves, then clicks Connect to run OAuth against TikTok's user-authorization endpoint. The credentials fields exist solely to enable the OAuth flow.

### One active ad account at a time — switchable, auto-selected on connect

When the merchant authorizes, TikTok returns every ad account the user can access; CloudCart stores the full `advertiser_ids` list and uses one active `advertiser_id` per request. The **first** advertiser is selected automatically on first connect. The merchant changes the active advertiser by updating the setting — no re-authorization needed — but only one is active at any moment.

The active advertiser is **automatically injected into every API call** (query parameter on reads, body field on writes). A call cannot be sent without it; switching the active advertiser retargets every subsequent call.

### Disconnect + reconnect can change the active advertiser

Re-authorizing (e.g. after changing TikTok permissions) re-fetches and **overwrites** the stored `advertiser_ids` list. The previously-active advertiser is NOT preserved — CloudCart re-auto-selects the first advertiser in the new list. A merchant who had advertiser B active before disconnect may end up on advertiser A after re-auth.

### Campaign creation — validated fields

Creating a campaign validates:
- `campaign_name` — required, max 512 characters.
- `objective_type` — required.
- `budget` — numeric, ≥ 0.
- `budget_mode` — must be exactly `BUDGET_MODE_TOTAL`, `BUDGET_MODE_DAY`, or `BUDGET_MODE_INFINITE`; defaults to `BUDGET_MODE_DAY` if omitted. Any other value is rejected (422) before any TikTok call.

### Reporting metrics

Reports are pulled by date range at the campaign level. Default metrics: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `conversions`, `conversion_rate`, `cost_per_conversion`.

### Custom audiences

The merchant can list audiences, create one from an uploaded file (e.g. an email list, `FILE_TYPE_EMAIL`), and build a lookalike audience from any source audience.

### Long-lived access token — no refresh flow

Unlike [[apps-tiktok-shop]] (time-bound access + refresh tokens), the TikTok Business / Marketing API issues a long-lived access token. CloudCart stores only the access token (no refresh token, no expiry). It never needs refreshing — the token lives until the merchant disconnects or revokes the app in TikTok's developer portal.

### Ads OAuth differs from Shop's — different callback parameter

The TikTok Ads callback expects an `auth_code` parameter (TikTok Business API convention), not the `code` parameter used by TikTok Shop. The Ads and Shop integrations therefore cannot share callback handling.

### No sandbox / test mode

All calls hit TikTok's production advertising API; there is no UI toggle for a sandbox. Test campaigns and test data must be created in the merchant's real ad account.

### Timeouts

Campaign, audience, and report calls time out at 15 seconds; the OAuth code exchange uses a tighter 10-second timeout. A slow TikTok response surfaces in the UI as "no data".

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-tiktok-ads-settings]] — settings sub-page.
- [[apps-tiktok-pixel]] — tracking pixel sister app.
- [[apps-tiktok-shop]] — marketplace / catalog sister app.
- [[apps-google-dynamic]] — equivalent for Google Ads.
- [[apps-facebook-comments]] — Facebook equivalent ad ecosystem.

## Open questions
