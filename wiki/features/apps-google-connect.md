---
type: feature
nav_path: "Apps → Google Connect"
route_name: apps.google_connect.settings
route_path: /admin/apps/google_connect
aliases: ["Google Connect", "Google OAuth", "Sign in with Google", "Google authentication"]
tags: [apps, google, oauth, authentication]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 4
---
# Google Connect (OAuth)

## Purpose

**Google Connect** integration — the **shared OAuth foundation** for ALL other Google apps. Provides:

- OAuth 2.0 connect flow with the merchant's Google account.
- Token storage + refresh management.
- Scope-based permissions (each downstream Google app requests specific scopes).
- "Sign in with Google" button rendering in app settings.

When the merchant clicks "Sign in with Google" in [[apps-google-shopping]], [[apps-google-sheets]], or other Google integrations, they're going through Connect's plumbing. Connect itself doesn't do anything user-facing — it's the prerequisite infrastructure.

## Where to find it

Sidebar → Apps → install → **Google Connect**. Typically auto-installed as a dependency when any Google integration is enabled.

## What the merchant can do here

The Connect page itself is **install-only** — it has no settings form, no OAuth UI, no avatar/email display, and no Disconnect button. The actual Connect / Disconnect UI lives in each downstream Google app's Settings page ([[apps-google-sheets-settings]], [[apps-google-shopping-settings]], etc.) — Connect just exists as a catalog entry that documents the OAuth concept.

### What the merchant CANNOT do here
- Connect or disconnect anything from this page — go to the relevant Google app's Settings tab instead.
- Use Connect alone — it does nothing visible to the customer without a downstream Google integration.

## Settings & fields

The integration is a thin facade around Google's OAuth 2.0 flow. The Connect class extends the abstract app manager and exposes:
- `appInfo` — app metadata for the App Store catalog.

Other Google apps inherit OAuth handling from this base — they don't duplicate the OAuth dance.

## Business rules

### Single Google account per store

The OAuth tokens are stored at the STORE level (not per-admin). Once any admin connects, the integration works for all admins. To switch to a different Google account, the merchant disconnects + reconnects.

### Token refresh

Google's access tokens are short-lived (~1 hour). Connect handles automatic refresh using the refresh token (long-lived). If the refresh token is revoked (e.g., admin removed CloudCart from their Google account permissions), all downstream Google apps fail until reconnected.

### Scope-based authorization

Each downstream Google app requests specific OAuth scopes:
- [[apps-google-shopping]] → Merchant Center scopes.
- [[apps-google-sheets]] → Sheets read/write scopes.
- [[apps-google-analytics]] → Analytics read scope.
- [[apps-google-search-console]] → Search Console verify scope.

The Connect flow presents the merchant with Google's consent screen listing ALL requested scopes. The merchant must approve.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-google-shopping]] — uses Connect for OAuth.
- [[apps-google-sheets]] — uses Connect.
- [[apps-google-analytics]] — uses Connect.
- [[apps-google-search-console]] — uses Connect.
- [[apps-google-workspace]] — uses Connect.
- [[apps-google-dynamic]] / [[apps-google-tags]] — measurement apps that don't directly use OAuth.

## How it works (verified against backend)

### Per-app OAuth tokens — Connect is a directory entry, not a token store

Each Google app stores its OWN OAuth tokens at its own settings level (the `oauth` setting on the app), separately from this Connect app. [[apps-google-shopping]] holds its own tokens; [[apps-google-sheets]] holds its own tokens; the same applies to [[apps-google-search-console]] (which actually only stores a meta tag, not OAuth) and [[apps-google-workspace]] (which is a stub with no settings). The Connect entry primarily exists so the merchant can see Google authentication as a concept inside the App Store catalog. Disconnecting one downstream app does NOT affect the others — each manages its own connection lifecycle.

### Disconnect impact: app-specific, not global

When the merchant clicks Disconnect inside a specific Google app (e.g., Google Shopping), the platform calls `disconnectGoogleAccount` on THAT app's Manager — revoking just that app's stored token via Google's `revokeToken` (best-effort, exceptions swallowed) and deleting the app's settings. Other Google apps continue working with their own stored credentials. There is no global "disconnect all Google apps" action from this Connect page.

### Multi-account is naturally supported because each app stores its own token

Since each Google app holds its own OAuth credentials, the merchant CAN technically connect different Google accounts for different apps — e.g., a separate Google account for Sheets and for Merchant Center. The OAuth flow each app launches presents its own consent screen; the connected user is captured in each app's `oauth_user` setting independently. The UX nudge is to use ONE account (because each app shows its own Connect button), but the underlying storage doesn't enforce a single-account constraint at the store level.

### Token revocation detection happens at call time

There is no background poller checking whether Google has revoked any token. The platform detects revocation reactively: the next time a downstream app makes an API call, Google returns an `invalid_grant` / `401` error; the app's `getAuthErrorMessage($e)` translates it to a merchant-facing message (e.g., "Please, reconnect your google account."), removes the `oauth` setting so the app's UI shows the Connect button again, and surfaces the message to the merchant. There is no admin email alert.

### Per-admin OAuth is NOT the model — tokens are store-wide

OAuth tokens are saved at the store/site level on each app's settings, not per logged-in admin. Once any admin connects Google for, say, Google Shopping, ALL admins of that store use the same connection. There is no UI where each admin connects their own Google account; switching the connected account requires the current connection to be disconnected first.

### OAuth callback goes through CloudCart's "cc_socialite" service — not directly to the merchant store

The OAuth redirect for each Google app is built as: `{cc_socialite domain}/redirect/{site_id}/{app_key}?state={signed json}`. The merchant's browser bounces from the CloudCart admin → `cc_socialite` service → Google's consent screen → back through `cc_socialite` → the merchant's admin URL (where the state's `next` URL points, e.g., `/admin/apps/google_sheets/settings`).

`cc_socialite` is CloudCart's centralised OAuth broker that holds the client_id + client_secret per Google app type (Sheets / Shopping). The merchant store does NOT hold OAuth client credentials; CloudCart centralises them. This means:
- The "Google permissions screen" the merchant sees lists CloudCart's app name (e.g., "CloudCart Sheets"), not their own brand.
- Revoking access in google.com/security removes ALL CloudCart-Sheets connections for that Google account across all stores using the same OAuth client. (Revocation is observed reactively on the next API call.)

### Token auto-refresh via Google Client's token callback

Once connected, the access token (short-lived, ~1h) auto-refreshes on every API call using the long-lived refresh token. The Google PHP client updates the stored `oauth.token.access_token` + `oauth.token.created` timestamp transparently. The merchant never has to "reconnect" unless the refresh token itself is revoked (admin removed CloudCart's permission in their Google account settings, or the user explicitly hit "Disconnect" in CloudCart).

### Connect app has NO settings page — install only

The Vue Connect index uses `:install-only="true"` and `:support-config="false"` — the app is a catalog listing in the App Store with no settings tab and no configuration. Useful purely as a landing point that describes Google authentication. Real OAuth UI sits on each downstream app (Sheets, Shopping).

### Single route, no children

The Vue router exposes ONE route for this app: `apps.google_connect.settings` at `/admin/apps/google_connect`. No `overview`, no `settings` child — the whole page IS just the install screen with app metadata. The `Application` wrapper uses `app-name="app.name || 'Google Connect'"` so the catalog entry's name takes precedence over the fallback.

## Open questions

(None currently outstanding for this page.)
