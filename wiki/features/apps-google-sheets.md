---
type: feature
nav_path: "Apps → Google Sheets"
route_name: apps.google_sheets.overview
route_path: /admin/apps/google_sheets
aliases: ["Google Sheets", "Sheets export", "Sheets sync", "Google Sheets integration", "no enable disable button", "app has no active toggle"]
tags: [apps, google, sheets, export, sync]
plan_gates: ["google_sheets"]
created: 2026-05-22
updated: 2026-08-06
source_count: 7
---
# Google Sheets

## Purpose

**Google Sheets** integration — **bidirectionally** syncs the merchant's **PRODUCT catalog** (not orders) with a Google Sheets spreadsheet. Used by merchants who:

- Bulk-edit product data (descriptions, prices, names, brands, tags, categories) in a spreadsheet, then push changes back into CloudCart.
- Share product data with team members who don't have CloudCart admin access (read-only Sheets shares).
- Trigger external automation via Google Apps Script / Zapier on the product data.
- Maintain a backup / second copy of the catalog.

Workflow: Upload pushes products from CloudCart to the auto-created spreadsheet; the merchant edits in Sheets; Download pulls the edits back. Each task is started manually from the Tasks tab.

This page is the **hub** for the Google Sheets cluster. The deep mechanics (sync queues, the upload push, the download import, OAuth provisioning, and the column / filter catalogue) each live on a dedicated sub-page — see [[#sub-pages-in-this-cluster|Sub-pages]] below. The two tab UIs have their own pages: [[apps-google-sheets-settings]] (config) and [[apps-google-sheets-tasks]] (job history).

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What governs whether anything happens is the **Google account connection** plus the fact that every Upload / Download is a task the merchant starts by hand from the Tasks tab, see [[apps-google-sheets-tasks]].

## Best tool for bulk product edits (vs CSV / XML import & sync)

When a merchant wants to **mass-change existing product attributes** — prices, titles, descriptions, brands, tags, categories, stock, etc. — **Google Sheets is the easiest and recommended path**, because the whole round-trip is essentially **two clicks**:

1. **Upload** — one click exports the current catalog into an auto-created Google spreadsheet. The merchant does **not** export or format anything by hand; the sheet is created and filled for them.
2. The merchant edits the values directly in the familiar spreadsheet.
3. **Download** — one click pulls the edited values back into CloudCart.

The file-based imports are built for **loading a catalog IN from an outside source**, not for editing what is already in the store. In fact **CSV Import cannot update existing products at all** — it always creates new ones, so re-importing an edited file produces **duplicates**, not updates (see [[apps-csv-import]]). Google Sheets is the tool that actually writes changes back onto the existing products.

| Tool | Get the current data out | Apply the edits | Best for |
|---|---|---|---|
| **Google Sheets** (this app) | 1 click — Upload auto-creates + fills the sheet | 1 click — Download | **editing existing products in bulk** (prices, texts, any attribute) |
| CSV Import — [[apps-csv-import]] | manual: export the catalog to a file elsewhere, convert to CSV | ❌ **cannot apply edits — a re-import creates duplicate products** | loading a catalog from a CSV file (bootstrap / migration) **only** |
| XML Import — [[apps-xml-import]] | needs an external / supplier XML feed URL | re-point + re-parse | one-time import from a supplier feed |
| XML Sync — [[apps-xml-sync]] | needs a recurring supplier XML feed | automatic on a schedule (the feed is the source of truth) | ongoing dropship / wholesale feeds |

So: **to change prices / texts / any attribute on products already in the store, use Google Sheets.** Reach for CSV / XML import only when bringing a catalog IN from an external source (new-store bootstrap, migration, supplier feed).

## Where to find it

Sidebar → Apps → install → **Google Sheets**. Route: `/admin/apps/google_sheets`. Tabs:

- **Overview** — this hub.
- **Settings** ([[apps-google-sheets-settings]]) — OAuth connect, product filter, column picker.
- **Tasks** ([[apps-google-sheets-tasks]]) — background sync job progress / history. Visible only after OAuth connect.

## Sub-pages (in this cluster)

- [[apps-google-sheets-sync-pipeline]] — the 4-step background-queue pipeline, two-phase upload, parallel download batch, live progress, one-task-at-a-time concurrency, plan / maintenance gating.
- [[apps-google-sheets-upload]] — the outbound push (CloudCart → Sheets): full-overwrite behaviour, 500-product chunked export, total-count seeding.
- [[apps-google-sheets-download]] — the inbound import (Sheets → CloudCart): Product-ID row grouping, new-product creation, category / vendor auto-creation, tag overwrite, CDN-image filtering, conflict resolution.
- [[apps-google-sheets-oauth]] — OAuth via the platform's Google connect broker, automatic spreadsheet provisioning, the signed `state` payload, disconnect / revocation behaviour, "Worksheet not found" validation.
- [[apps-google-sheets-columns-filters]] — the fixed column catalogue (+ app-conditional Units / Suppliers / Stores), the Discount column, default-checked columns, the 5 filter modes and the upload pipeline's 3-mode discrepancy.

## What the merchant can do here

### Settings
- **OAuth connect** to Google (uses [[apps-google-connect]]). The platform auto-creates a spreadsheet on first connect — see [[apps-google-sheets-oauth]].
- **Spreadsheet ID / Worksheet name** — auto-populated and READ-ONLY (the merchant cannot paste an existing spreadsheet's ID).
- **Product filter** (`filter_group` + values) — which products to include in Upload; see [[apps-google-sheets-columns-filters]].
- **Allowed columns** — which product attributes to write as columns; see [[apps-google-sheets-columns-filters]].
- Optional **Discount** — fixed-type discount campaign whose price fills the Discount column.

### Tasks
- See the history of background Upload / Download jobs (timestamp, rows processed, errors).
- Start new Upload / Download tasks (one at a time) — see [[apps-google-sheets-sync-pipeline]] for the concurrency rule.

### What the merchant CANNOT do here
- Sync orders or customers — **products only**.
- Use without OAuth + a Google account.
- Point the integration at an existing spreadsheet (the platform auto-creates one — to reuse a different sheet the merchant must disconnect and reconnect; see [[apps-google-sheets-oauth]]).

## Settings & fields

The merchant-editable settings (saved from the Settings tab) are `filter_group`, `filter_group_value`, `allowed_columns`, and an optional `discount_id`. The spreadsheet identifiers (`spreadsheet_id`, `spreadsheet_url`, `worksheet_name`) are set automatically on connect and are READ-ONLY in the UI. Full field reference is on [[apps-google-sheets-settings]]; the column / filter catalogue is on [[apps-google-sheets-columns-filters]].

### Validation

The merchant does not supply spreadsheet credentials directly — the spreadsheet is auto-created on connect. At task start time the platform calls Google's Sheets API to confirm the configured `worksheet_name` still exists in the spreadsheet (e.g., the merchant renamed the tab in Google). Mismatch → job error: *"Worksheet not found"*. See [[apps-google-sheets-oauth]] for the full validation + reconnect flow.

## Business rules

- **Bidirectional, products only.** Upload pushes the catalog out; Download pulls merchant edits back in. The integration never touches orders or customers. See [[apps-google-sheets-upload]] + [[apps-google-sheets-download]].
- **Upload replaces sheet contents (no append-only mode).** Each Upload clears the worksheet and rewrites the header + all matching products. A subsequent Download reads back whatever the merchant edited. There is no merge / append knob — see [[apps-google-sheets-upload]].
- **Download requires a prior successful upload.** A Download is only allowed once at least one Upload has completed, so the sheet has the right column structure. See [[apps-google-sheets-download]].
- **One concurrent task at a time** and **the spreadsheet wins on Download** — both detailed on [[apps-google-sheets-sync-pipeline]] and [[apps-google-sheets-download]].
- **One spreadsheet per CloudCart store.** The integration auto-creates ONE spreadsheet per store. Multi-store merchants get separate auto-created spreadsheets per site (named "CloudCart Products {site_id}").
- **Rate limits.** Google Sheets API has rate limits (60 read / 60 write requests per user per minute). High-volume stores may hit caps; the platform retries with backoff.
- **No Active/Inactive toggle.** The page's top section is read-only (`show-activate-button: false`) — the app is auto-active once Settings are saved with OAuth, unlike most apps.
- **Permission.** Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `google_sheets` | Access gate (install URL) | The install URL `/admin/apps/google_sheets/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules. Note that each sync job also re-checks plan + maintenance state at run time (it silently skips if the plan expired) — see [[apps-google-sheets-sync-pipeline]].

## Related

- [[apps]] — App Store.
- [[apps-google-sheets-settings]] — Settings tab (config UI).
- [[apps-google-sheets-tasks]] — Tasks tab (sync job history UI).
- [[apps-google-sheets-sync-pipeline]] — queue / job mechanics.
- [[apps-google-sheets-upload]] — outbound push pipeline.
- [[apps-google-sheets-download]] — inbound import pipeline.
- [[apps-google-sheets-oauth]] — OAuth + spreadsheet provisioning.
- [[apps-google-sheets-columns-filters]] — column catalogue + filter modes.
- [[apps-google-connect]] — OAuth foundation.
- [[apps-google-shopping]] — sister Google integration.
- [[products-products]] — source data (product catalog).

## Open questions

(None currently outstanding for this page.)
