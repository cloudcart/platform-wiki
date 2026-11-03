---
type: feature
nav_path: "Apps → Algolia → Credentials"
route_name: apps.algolia.overview
route_path: /admin/apps/algolia
aliases: ["Algolia credentials", "Algolia API keys", "Application ID", "Admin API Key", "Search API Key", "Algolia validation"]
tags: [apps, algolia, search, credentials, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-algolia]]. See the hub for the other aspects (indexing, dashboard-side configuration, settings tab).

# Algolia — Credentials & validation

## Purpose

Covers how the merchant authenticates CloudCart to their Algolia account: which keys are required, how they are validated live as the merchant types, when a missing key silently disables sync, and why the merchant must save credentials before they can trigger an upload. Authentication is **credentials-based (API key + application ID), not OAuth** — there is no redirect roundtrip; the merchant copies keys out of Algolia's own dashboard and pastes them here.

## Where to find it

Sidebar → Apps → Algolia → **Settings tab**. Route: `/admin/apps/algolia`. The credential fields sit at the top of the settings form (the broader settings tab is documented on [[apps-algolia-settings]]).

## What the merchant can do here

- Paste the **Application ID** (`appId`) from the Algolia dashboard.
- Paste the **Admin API Key** (`apiKey`) — the write-capable key used for indexing uploads.
- Paste the **Search API Key** (`searchApiKey`) — the read-only key used by the storefront autocomplete client.
- See **live inline validation** of the credentials as they type (no save needed to learn the keys are bad).

### What the merchant CANNOT do here

- Trigger **Upload data to Algolia** before saving credentials — the button is gated (see Business rules).
- Use OAuth / "Connect with Algolia" — there is no OAuth flow; only manual key entry.
- Activate Algolia with only the Admin key — the Search API Key is enforced server-side too.

## Settings & fields

| Field (lang key) | Required | Notes |
|---|---|---|
| `appId` | yes (on activate) | Algolia Application ID from the Algolia dashboard. |
| `apiKey` | yes (on activate) | Admin API Key — write permission, used for indexing uploads. |
| `searchApiKey` | yes (on activate) | Search API Key — read-only, used by the storefront's autocomplete client. Enforced via `'required_if:active,1'`. |

The Vue settings page uses **live-watching** of `connect.appId` + `connect.apiKey` (`live-watch="['connect.appId', 'connect.apiKey']"`), re-validating on the fly. Pasting invalid credentials surfaces an error immediately rather than at save time.

Validation error strings:

- **Missing settings** (`error.missing_settings`): *"You have not saved your Application ID и Admin API Key"*.

## Business rules

### THREE credentials required when activating Algolia — not two

The Settings save validates THREE fields when the app is being activated:

- **Application ID** (`appId`) — required.
- **Admin API Key** (`apiKey`) — required (write-capable, used for indexing uploads).
- **Search API Key** (`searchApiKey`) — required (read-only key used by the storefront's autocomplete client).

The merchant must paste BOTH keys from Algolia's dashboard, not just one. The UI may emphasise the Admin API Key, but the Search API Key is enforced server-side via `'required_if:active,1'` and the activation will fail without it. (Some legacy flows squash `searchApiKey` into `apiKey` on save.)

### Sync gating — both credentials must be present

The integration only attempts to sync when:

1. App is installed.
2. `appId` setting is present.
3. `apiKey` setting is present.

So missing either credential → no sync attempted (silent). The merchant must complete both fields. This gating is what [[apps-algolia-indexing]] checks before any auto-sync or repeatable run pushes data.

### "Start indexing" button is gated by `isConfigured`

If the merchant clicks **Upload data to Algolia** without saving both `appId` + `apiKey` first, the endpoint returns HTTP 400 with the message *"You have not saved your Application ID и Admin API Key"*. So **the merchant has to save credentials BEFORE starting indexing** — there is no "save and index" combo action.

### "Application ID и Admin API Key" — Bulgarian conjunction in EN string

The EN translation of `algolia.error.missing_settings` keeps the Bulgarian word "и" (meaning "and") as a typo in the English message: *"You have not saved your Application ID и Admin API Key"*. The intended English text is *"…Application ID and Admin API Key"*. This is a translation bug surfacing in the English UI, not a feature.

### Permission

Standard apps permission scope.

## Related

- [[apps-algolia]] — hub.
- [[apps-algolia-settings]] — the Settings tab where these fields live.
- [[apps-algolia-indexing]] — what the validated credentials unlock (uploads + auto-sync).

## Open questions

(None currently outstanding for this page.)
