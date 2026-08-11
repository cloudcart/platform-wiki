---
type: feature
nav_path: "Apps → Google Sheets → Settings"
route_name: apps.google_sheets.settings
route_path: /admin/apps/google_sheets/settings
aliases: ["Google Sheets Settings", "Sheets config", "Sheets credentials"]
tags: [apps, google, sheets, settings, oauth, integration]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---
# Google Sheets → Settings

## Purpose

The **Settings** tab is the one configuration screen for the Google Sheets integration. It hosts three things the merchant interacts with: the **OAuth connect box** (sign in with Google), the **read-only spreadsheet identifiers** (auto-provisioned, not editable), and the **product filter + column picker** that decide what the sync moves.

This page documents the **tab UI itself** — how the boxes render and behave on screen. The deep mechanics behind those controls live on dedicated aspect pages:

- Connect / disconnect / spreadsheet auto-creation / `cc_socialite` broker / revocation / "Worksheet not found" → [[apps-google-sheets-oauth]].
- The column catalogue, the 5 filter modes, the Discount-column rule, and save-time validation → [[apps-google-sheets-columns-filters]].

For the full Google Sheets feature set, see the hub [[apps-google-sheets]].

## Where to find it

Sidebar → Apps → Google Sheets → **Settings tab**. Route: `/admin/apps/google_sheets/settings`.

## What the merchant can do here

- **Connect / disconnect Google** via the OAuth box at the top (shared infrastructure: [[apps-google-connect]]). The connect mechanics, auto-created spreadsheet, and disconnect side-effects are on [[apps-google-sheets-oauth]].
- **Pick the product filter** (`filter_group` + `filter_group_value`) — which products to sync.
- **Pick the allowed columns** (`allowed_columns`) — which product attributes become spreadsheet columns.
- Optionally add a **Discount** column sourced from a fixed-type discount campaign.
- **Open the spreadsheet** in Google Sheets via the inline button at the bottom.

The catalogue of columns and filter modes is on [[apps-google-sheets-columns-filters]].

### What the merchant CANNOT do here

- Save without a connected Google account, or without picking at least one column.
- Paste a spreadsheet URL or rename the worksheet — both fields are READ-ONLY (see Settings & fields).
- Sync orders or customers — the integration is **products only**.

## Settings & fields

This tab saves exactly **four** merchant-editable keys; everything else (OAuth tokens, spreadsheet identifiers) is set automatically elsewhere and is NOT touched by the Settings save.

| Field | Editable? | Notes |
|---|---|---|
| `filter_group` | yes | `all` / `category` / `vendor` / `product` / `tag` / `selection` — which products to sync. See [[apps-google-sheets-columns-filters]]. |
| `filter_group_value` | yes | The IDs picked for the chosen filter (category IDs, vendor IDs, etc.). |
| `allowed_columns` | yes | Which product attributes to include as columns. **Required** — cannot save empty. |
| `discount_id` | yes | Optional; required only if the Discount column is selected. |
| `spreadsheet_id` | READ-ONLY | Auto-populated on first connect. |
| `spreadsheet_url` | READ-ONLY | Auto-populated; backs the "Open the spreadsheet" button. |
| `worksheet_name` | READ-ONLY | Auto-populated to the auto-created spreadsheet's first tab. |
| `oauth` (state) | — | Connected-user profile (avatar / name / email); set on connect, wiped on disconnect. |

### Validation

The save endpoint validates only two things:

1. `allowed_columns` — required (cannot save empty). Error: *"You have not selected any columns to export"*.
2. `discount_id` — required only when the Discount column is in `allowed_columns`. Error: *"You have not selected a discount"*.

See [[apps-google-sheets-columns-filters]] for the Discount-column rule (only `fixed`-type discounts are selectable) and the full column / filter catalogue.

## Business rules

- **OAuth gating.** Every operation requires valid OAuth tokens; if Google permission expires or is revoked, sync silently fails until reconnected. Full revocation / reconnect behaviour: [[apps-google-sheets-oauth]].
- **No "sync mode" knob.** Sync is task-driven from [[apps-google-sheets-tasks]]; Upload overwrites the sheet and Download reads edits back. There is no append-vs-overwrite toggle on this tab — see [[apps-google-sheets-upload]] / [[apps-google-sheets-download]].
- **Save persists 4 keys only.** Re-saving Settings stores `filter_group`, `filter_group_value`, `allowed_columns`, `discount_id` — and nothing else. Spreadsheet identifiers and tokens are managed by the connect / auto-provision flow on [[apps-google-sheets-oauth]].
- **Permission.** Standard apps permission scope.

## Related

- [[apps-google-sheets]] — Google Sheets hub.
- [[apps-google-sheets-oauth]] — connect / disconnect / spreadsheet provisioning mechanics.
- [[apps-google-sheets-columns-filters]] — column catalogue + filter modes + Discount rule.
- [[apps-google-sheets-tasks]] — sync task history (where Upload / Download run).
- [[apps-google-connect]] — OAuth foundation.
- [[apps-google-shopping-settings]] — sister Google integration with the same OAuth pattern.

## How it works (verified against backend)

This section covers only the **on-screen rendering** of the Settings tab. The functional mechanics (OAuth broker, spreadsheet auto-creation, disconnect side-effects, column / filter semantics, validation strings) are not repeated here — they live on [[apps-google-sheets-oauth]] and [[apps-google-sheets-columns-filters]].

### OAuth box — three visible UI states

The OAuth box at the top of Settings renders one of three states:

1. **Loading** — `redirectLoader` is true; a small `b-spinner` shows while a Connect / Disconnect request is in flight.
2. **Not connected** — a large **Sign in with Google** button (CSS class `btn-google-signin`, Google's branded button image). Clicking calls `/admin/api/google_sheets/connect`, which returns a `redirect` URL the browser navigates to (the broker — see [[apps-google-sheets-oauth]]).
3. **Connected** — a "logged-as" card with the circular Google avatar, name, email, and a **Logout** button. Logout uses the shared `DeleteComponent` confirm modal (*"Are you sure you want to logout?"* / confirm label *"Logout"*); on confirm it calls `/admin/api/google_sheets/disconnect`, then re-fetches settings to flip auth back to false.

### Read-only spreadsheet fields + inline "Open the spreadsheet" button

The **Spreadsheet ID** and **Worksheet Name** fields render with `readonly: true` — the merchant cannot type into them. Below the columns / filters block, the tab renders an **Open the spreadsheet in Google Sheets** button (green Sheets icon) that opens the stored `spreadsheet_url` in a new tab — the merchant's launch point into the spreadsheet.

### Settings boxes are slide-over panels, not modals

The settings render via the shared `SettingsBox` component with `editMethod: 'panel'` — clicking Edit opens a right-side drawer with the fields inline (a slide-over panel, not a modal dialog). The bottom of the page has a `SubmitChanges` save bar.

### Filter dropdowns use conditional visibility

The `filter_group_value` field is rendered once per filter type, each instance guarded by `dependField: "filter_group"` + `dependValue` so only the dropdown matching the chosen `filter_group` is visible. The category / vendor / product dropdowns are server-side autocompletes (`/admin/api/core/product-categories/search`, `/vendors/search`, `/products/search`, all `searchable: true` + `requestOnSearch: true`). On load, the tab resolves the saved `filter_group_value` IDs to human-readable chip labels (Category / Vendor / Product / Tag / Selection names) so the merchant sees names, not IDs.

## Open questions

(None currently outstanding for this page.)
