---
type: feature
nav_path: "Apps → Google Sheets → OAuth & spreadsheet"
route_name: apps.google_sheets.settings
route_path: /admin/apps/google_sheets/settings
aliases: ["Google Sheets OAuth", "Sheets connect", "Sheets spreadsheet provisioning", "Sheets reconnect", "Worksheet not found"]
tags: [apps, google, sheets, oauth, connect, spreadsheet]
plan_gates: ["google_sheets"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Google Sheets → OAuth & spreadsheet provisioning

> Part of [[apps-google-sheets]]. See the hub for related aspects (upload, download, sync pipeline, columns & filters).

## Purpose

Explains how the merchant **connects Google**, how CloudCart **auto-creates the spreadsheet** (the merchant never pastes a URL), and how disconnect / revocation / "Worksheet not found" errors behave. This is the foundation every sync depends on — no OAuth, no spreadsheet, no Upload or Download.

## Where to find it

Sidebar → Apps → Google Sheets → **Settings tab** (`/admin/apps/google_sheets/settings`). The OAuth box sits at the top of Settings; the field-level UI is on [[apps-google-sheets-settings]]. OAuth itself uses the shared [[apps-google-connect]] foundation.

## What the merchant can do here

- **Sign in with Google** — connect a Google account via OAuth.
- See the connected account (avatar / name / email) once linked.
- **Open the spreadsheet** — a button links straight to the auto-created Google Sheet.
- **Disconnect** — revoke the link (which also wipes job history; below).

### What the merchant CANNOT do here

- Paste or choose an existing spreadsheet — the platform auto-creates one. To use a different sheet the merchant must disconnect and reconnect (which creates a fresh one).
- Edit the Spreadsheet ID or Worksheet name — both are READ-ONLY, auto-populated on connect.
- Pick a different worksheet tab from the same spreadsheet — sync always uses the configured `worksheet_name`.

## Settings & fields

| Field | Notes |
|---|---|
| `oauth` | OAuth tokens (stored on connect; auto-refreshed; wiped on disconnect / revocation). |
| `spreadsheet_id` | Auto-populated on first connect — READ-ONLY. |
| `spreadsheet_url` | Auto-populated — backs the "Open the spreadsheet" button — READ-ONLY. |
| `worksheet_name` | Auto-populated to the auto-created spreadsheet's first tab — READ-ONLY. |

### Validation: "Worksheet not found"

Before starting any sync task, the platform calls Google's API to confirm the configured `worksheet_name` still exists in the spreadsheet (lists the sheets). If the merchant renamed or deleted the tab in Google, the task is never created and the error is *"Worksheet not found"*. The fix is to rename the tab back, or disconnect + reconnect to provision a fresh spreadsheet.

## Business rules

### Auto-creates a fresh spreadsheet on connect

On first connect, when no `spreadsheet_url` is yet stored, the platform automatically creates a new spreadsheet named **"CloudCart Products {site_id}"** via the Sheets API and stores its ID, URL, and first worksheet name on the app. Connecting is enough — the merchant doesn't create or paste anything. If spreadsheet creation FAILS (e.g. an API error), the platform resets the connection so the merchant starts from a clean Connect state. Multi-store merchants get one spreadsheet per site.

### OAuth flows through the centralised `cc_socialite` broker

The "Sign in with Google" button does NOT redirect straight to Google. The connect endpoint builds a URL of the form `{cc_socialite_domain}/redirect/{site_id}/google_sheets?state={signed JSON}`. The broker holds the OAuth client_id + client_secret, forwards the merchant to Google's consent screen, stores the returned tokens back on the store, and redirects to `/admin/apps/google_sheets/settings`.

Practical consequences:

- The consent screen the merchant sees lists "CloudCart Sheets" (or similar), not their own brand.
- Revoking access at google.com/security removes the connection for ALL merchant stores using the same OAuth client identity.
- Access tokens auto-refresh via the Google client's token-refresh callback — the merchant rarely needs to reconnect unless they explicitly disconnect or revoke.

### The signed `state` payload returns the merchant to the right page

The `state` parameter is a urlencoded JSON carrying `referer`, `site_id`, `type` (`google_sheets`), `type_id` (admin user ID), and `next` (the post-OAuth return URL). The broker uses `next` to bounce the merchant back to `/admin/apps/google_sheets/settings`, so the round-trip is deterministic — the same merchant returns to the same admin page.

### Disconnect (or re-provision) wipes ALL sync jobs

Disconnecting Google deletes ALL historical sync jobs from the database — the Tasks tab is empty after reconnect. The same wipe happens when a fresh spreadsheet is re-created. So job history does not survive a disconnect / reconnect cycle.

### Revocation is detected reactively

CloudCart detects a revoked / invalid token reactively on the next API call. The merchant sees *"Please, reconnect your google account."* (or *"Invalid Credentials. Please, reconnect your google account."*); the platform clears the `oauth` setting so the Connect button reappears, and flashes the error. The merchant must re-Connect to resume syncing.

## Related

- [[apps-google-sheets]] — hub.
- [[apps-google-connect]] — the shared OAuth foundation.
- [[apps-google-sheets-settings]] — the Settings tab UI where the OAuth box lives.
- [[apps-google-sheets-sync-pipeline]] — where auth failures surface as job errors.

## Open questions

(None currently outstanding for this page.)
