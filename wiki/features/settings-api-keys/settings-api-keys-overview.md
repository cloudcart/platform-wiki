---
type: feature
nav_path: "Settings → Api keys → Overview"
route_name: api_keys.settings
route_path: /admin/settings/api_keys
aliases: ["API keys overview", "API keys table", "Преглед на API ключове"]
tags: [settings, api-keys, developer, integration]
plan_gates: ["api_requests"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Api keys — Overview

> Part of [[settings-api-keys]]. See the hub for related aspects (modal, rate limits, feature packs, delete protection, security).

## Purpose

The list view of the API-keys screen — page header (Site ID badge, Add button), the rate-limit info banner, the keys table itself, and the inline row controls (copy-to-clipboard, Active toggle). This page covers what the merchant SEES on `/admin/settings/api_keys` and the synchronous CRUD wiring that backs each row. Create / Edit dialogs are documented in [[settings-api-keys-create-edit-modal]].

## Where to find it

Sidebar → Settings → **Api keys**.

The page's breadcrumb reads "Settings → Api keys". The route is `/admin/settings/api_keys`. The header icon is a key.

## What the merchant can do here

- See the store's **Site ID** displayed in the page header as a chip — the store identifier integrations send alongside the API key.
- See the **API Base URL** — `<store-host>/api/v2` — and the plan's current API requests-per-minute cap. See [[settings-api-keys-rate-limits]].
- Click **Upgrade** (when shown) to buy extra `api_requests` capacity. See [[settings-api-keys-feature-packs]].
- Click **+ Add Api key** to open the create modal — see [[settings-api-keys-create-edit-modal]].
- Click any row's **Name** to open the edit modal.
- Click the API key value in the table — only the first 30 characters are shown followed by `...` and a clipboard icon. Clicking copies the full key with a toast confirmation.
- Toggle a key's **Active** switch to disable / enable without deleting. Inactive keys cannot authenticate.
- Click the row's **Remove** button to delete a single key — see [[settings-api-keys-delete-protection]].
- Bulk-delete: select multiple rows, then trigger the standard table bulk-delete action which POSTs to `/admin/api/core/settings/api-keys/delete`.
- Sort, filter, and paginate through the keys table (default sort: by ID descending — newest first).

## Settings & fields

### Page header

| Element | What it shows | Notes |
|---------|---------------|-------|
| **Site ID badge** | `Site ID: <numeric id>` chip in the top-right action area. | From `serverSettings('site.id')` (verify). The value the integration must send alongside the API key. |
| **+ Add Api key** | Primary button. | Opens the create modal. Always visible. |

### API rate-limit info banner

Shown above the table when `api_requests_limit` is present in the page meta (i.e., the plan exposes an API rate limit at all). Banner content:

| Element | What it shows |
|---------|---------------|
| **Plan + limit line** | *"Your current `<plan-name>` plan allows `<N>` API requests per minute."* |
| **API Base URL line** | *"API Base URL: `<host>/api/v2`"* (clickable, opens in new tab). |
| **Upgrade button** | Visible only when `meta.api_requests_feature_exists` is true. Branches by `meta.api_requests_has_packs`. See [[settings-api-keys-feature-packs]]. |

The full cap rules + edge enforcement are documented in [[settings-api-keys-rate-limits]].

### Keys table

| Column | What it shows | Sortable | Notes |
|--------|---------------|----------|-------|
| **Name** | Free-text label the merchant chose. | No | Click opens the Edit modal. |
| **Api key** | First 30 chars of the full key + `...` and a copy icon. | No | Click copies the full value to clipboard. |
| **Created** | Date of creation. | No | |
| **Last updated** | Date of last edit (or activity toggle). | No | |
| **Active** | Toggle switch. | No | Flipping calls `GET /admin/api/core/settings/api-keys/status/{id}/{0\|1}`; success toast + local row mutation. |
| **(actions)** | Per-row Remove button. | No | See [[settings-api-keys-delete-protection]]. |

Default sort: `id` descending — most recently created at the top.

### Copy-to-clipboard cell

In the Api key column, the displayed value is the first 30 characters of the full key + `...` followed by a clone icon. Clicking the entire cell reads the FULL key value from the row's `data.key` (not from the truncated display), calls `navigator.clipboard.writeText`, and shows toast *"Copied to clipboard"*. The truncation is **cosmetic only** — see [[settings-api-keys-security]] for the visibility implications.

### Active toggle (inline row)

Standard `CcTable` toggle column. Calls `getStatus.useMutation` which hits `GET /admin/api/core/settings/api-keys/status/{id}/{0|1}`. On success → toast *"Status changed successfully"*; the local row is mutated in-place. No confirmation modal — toggling is one-click. Operational semantics (when the toggle actually starts blocking requests, in-flight behaviour) are documented in [[settings-api-keys-security]].

## Business rules

### CRUD is synchronous — no queue / async / notifications

This screen's CRUD actions are synchronous. No background jobs are dispatched on create / edit / delete / status-toggle. No admin notifications are fired. No webhooks are triggered. The merchant's clicks land in the database immediately.

### What the merchant CANNOT do here

- Manually choose the key value (server-generated, immutable — see [[settings-api-keys-create-edit-modal]] + [[settings-api-keys-security]]).
- See the rate limit per-key (the cap is store-wide — see [[settings-api-keys-rate-limits]]).
- Restrict a key to specific endpoints or scopes (no per-key permission model — see [[settings-api-keys-security]]).
- Delete a key in use by a webhook (see [[settings-api-keys-delete-protection]]).

## Related

- [[settings-api-keys]] — hub.
- [[settings-api-keys-create-edit-modal]] — Add / Edit modal fields + validation.
- [[settings-api-keys-rate-limits]] — per-plan rate limit + edge enforcement.
- [[settings-api-keys-feature-packs]] — Upgrade flow for buying extra capacity.
- [[settings-api-keys-delete-protection]] — FK protection + bulk delete caveats.
- [[settings-api-keys-security]] — plaintext storage, immutability, truncation, permissions.
- [[settings-hooks]] — Webhooks use API keys for authentication.

## Open questions

None.
