---
type: feature
nav_path: "Apps → Algolia → Settings"
route_name: apps.algolia.settings
route_path: /admin/apps/algolia/settings
aliases: ["Algolia Settings", "Algolia config"]
tags: [apps, algolia, search, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# Algolia → Settings

## Purpose

The **Settings** tab is where the merchant configures their Algolia search integration — enters credentials, picks result-display limits, toggles price display. See [[apps-algolia]] for the full feature set.

## Where to find it

Sidebar → Apps → Algolia → **Settings tab**. Route: `/admin/apps/algolia/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **Application ID** (`appId`) | Algolia app identifier from the merchant's Algolia dashboard. |
| **Admin API Key** (`apiKey`) | Algolia admin key with write permissions. |

Live-watch validates the credentials as the merchant types (per [[apps-algolia]] `live-watch="['connect.appId', 'connect.apiKey']"`).

### Display options

| Field | Notes |
|---|---|
| **Products result count** (`count.products`) | Max products in search results. |
| **Categories result count** (`count.categories`) | Max categories. |
| **Vendors result count** (`count.vendors`) | Max vendors. |
| **Show products price** (`show_price`) | Toggle price display in search-result cards. |

### Upload trigger

The **Upload data to Algolia** button (`btn.start_indexing` per [[apps-algolia]]) starts a queue-backed batch upload. On success: *"Sending data to Algolia was added to the queue."*

### What the merchant CANNOT do here
- Use Algolia AND the built-in search ([[apps-listing-engine]] + [[apps-advanced-search]]) simultaneously.
- Configure Algolia ranking / synonyms / facets from CloudCart (only in Algolia's dashboard).
- Exceed Algolia's plan operations quota.

## Settings & fields

See [[apps-algolia]] for the full settings schema + validation errors.

## Business rules

### Quota awareness

The settings page surfaces `error.quota_exceeded`: *"Operations quota exceeded in Algolia, change plan to get more operations."* when the merchant exceeds Algolia's plan limits.

### Permission
Standard apps permission scope.

## Related

- [[apps-algolia]] — Algolia hub.
- [[apps-listing-engine]] / [[apps-advanced-search]] — alternative built-in search stack.

## How it works (verified against backend)

### Single Algolia application per CloudCart store

The settings allow one `appId` + one `apiKey`. When [[apps-multilang]] is active, the integration pushes localized text to Algolia's default index per the storefront's primary language — there is no UI here to split indexes per language. Merchants needing per-language indexes typically configure replicas / additional indexes inside Algolia's own dashboard.

### Custom ranking / synonyms / facets stay in Algolia's dashboard

The CloudCart Settings page only exposes credentials, result counts per entity type, and the show-price toggle. Ranking customisation (custom rank order, business rules, boosting), synonyms (per-language synonym lists), and facets (filterable attributes shown in storefront search) are all configured inside Algolia's own dashboard (algolia.com). There is no CloudCart UI mirroring those options.

### No proactive quota warning — only post-error notification

The only quota signal CloudCart surfaces is the `error.quota_exceeded` toast once Algolia's API actually returns "quota exceeded" on a sync. There is no usage-percentage gauge, no "you're at 80% of your plan" warning, and no admin email when usage trends upward. Merchants monitor plan usage from Algolia's dashboard.

### Settings save requires THREE keys (not two) when activating

When the merchant activates Algolia, the platform's save endpoint enforces `appId` + `apiKey` (admin) + `searchApiKey` (read-only) all required. **The merchant must enter the Search API Key in addition to the Admin API Key** — both are pasted from Algolia's dashboard. Without `searchApiKey`, the save fails with *"Search API Key is required"*.

### Live credential validation calls Algolia's `listApiKeys` endpoint

As the merchant types/pastes `appId` + `apiKey` (live-watched), the platform fires `POST /api/algolia/validate` which initialises an Algolia client and calls `listApiKeys`. If Algolia returns an error (bad credentials, blocked application), the message is shown inline next to the credentials field. So the merchant gets near-instant feedback that their pasted keys are valid before they save.

### Defaults shown for result counts when nothing is set

When the merchant hasn't yet customised result counts, the defaults are:
- `shownProductsCount = 9`.
- `shownCategoriesCount = 5`.
- `shownVendorsCount = 5`.

(Same defaults as built-in [[apps-listing-engine]].) The merchant can adjust each independently; there is no joint cap on total result count across the three.

## Open questions

(None currently outstanding for this page.)
