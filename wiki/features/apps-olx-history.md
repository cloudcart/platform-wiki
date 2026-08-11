---
type: feature
nav_path: "Apps → OLX → History"
route_name: apps.olx.history
route_path: /admin/apps/olx/history
aliases: ["OLX History", "OLX operation log", "OLX activity log", "OLX audit"]
tags: [apps, olx, marketplace, history, audit, log]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# OLX → History

## Purpose

The **History** tab is the **operation log** of every OLX API call CloudCart made — every publish attempt, every refresh, every parameter mapping save, every delete. Each row records the operation type, the affected entity (product / category / parameter), the OLX API response (success / error), the timestamp.

Used by the merchant + support for **troubleshooting**:
- "Why did this product fail to publish?" — find the row + read the error.
- "When did this advert get rejected?" — filter by date + status.
- "How many adverts succeeded yesterday?" — filter by status + date.
- "Did this category mapping change recently?" — filter by entity type + date.

For the OLX feature set, see [[apps-olx]].

## Where to find it

Sidebar → Apps → OLX → **History tab**. Route: `/admin/apps/olx/history`.

The data table component uses:
- `TableHistoryName` — operation name / entity column.
- `TableHistoryMessage` — error / success message column.

## What the merchant can do here

### View operation history

Standard data table:

| Column | Notes |
|---|---|
| **Operation name** (`TableHistoryName`) | Type of operation — Publish advert / Update advert / Delete advert / Map category / Map parameter / Refresh adverts list / etc. |
| **Entity** | Which CloudCart record was involved (product name + ID, category name, etc.). |
| **OLX response message** (`TableHistoryMessage`) | The API response — success confirmation OR error reason. |
| **Status** | Success / Error / Pending. |
| **Timestamp** | When the operation ran. |
| **OLX API endpoint** | (Verify) Which OLX URL was called. |

### Filter by operation type / status / date

Standard filter UI lets the merchant scope to:
- Specific operation types (e.g., "show only Publish failures").
- Specific entities (e.g., "show everything related to product X").
- Date range.
- Success / error toggles.

### Drill-down

Clicking a row may open a detail view (verify) with:
- Full API request payload sent to OLX.
- Full API response from OLX.
- Stack trace if applicable.

### What the merchant CANNOT do here
- Edit or delete log entries (append-only).
- Re-run an operation directly from this view (must navigate to the relevant entity — [[apps-olx-products]] for re-publish, etc.).

## Settings & fields

### Per-log-entry fields

| Field | Notes |
|---|---|
| **Operation type** | One of: publish_advert / update_advert / delete_advert / map_category / map_parameter / map_value / refresh_adverts / etc. |
| **Entity type + ID** | The affected CloudCart record. |
| **OLX endpoint** | URL hit (e.g., `POST /partner/adverts`). |
| **Request payload** | What was sent. |
| **Response payload** | What OLX returned. |
| **Status code** | HTTP status. |
| **Status label** | Success / Error / Pending. |
| **Error message** | Parsed user-friendly error from OLX response. |
| **Timestamp** | When the operation ran. |

### Common error messages (from OLX API)

Examples surfaced here (per [[apps-olx]] lang):
- "Please, synchronize your product parameters with those in Etsy" (`err.params_not_mapped`).
- "One Etsy parameter is associated with more than one from store" (`err.same_params_mapping`).
- "This product can not be synced into Etsy..." (`err.missing_product_id`).
- "You must configure all your settings first" (`err.settings_not_saved`).

(Note: some error strings reference "Etsy" — likely shared error wording across marketplace integrations. The OLX-specific variants follow similar pattern.)

## Business rules

### Append-only log

Operation log entries are immutable. The merchant can't delete entries to "clean up" the log — useful for audit.

### Retention

Older log entries are typically pruned after N months (verify retention policy). Critical for compliance is the [[apps-gdpr-acceptance]] log (separate), not this operation log.

### Per-product correlation

Each row's Entity field correlates back to the source CloudCart product. The merchant can filter "show all operations for product X" to trace the full publish lifecycle.

### Side effects of viewing
- No API calls to OLX (read from local DB).
- Read-only — no state changes.

### Permission
Standard apps permission scope.

## Related

- [[apps-olx]] — OLX hub.
- [[apps-olx-products]] — products + publishing.
- [[apps-olx-adverts]] — live OLX adverts.
- [[apps-olx-configuration]] — category mapping operations recorded here.
- [[apps-olx-parameters]] / [[apps-olx-parameters-values]] — parameter mapping operations recorded here.
- [[apps-olx-settings]] — Connect / Disconnect operations recorded here.

## How it works (verified against backend)

### History records publish failures only

The history table stores failures (and other operations) tied to a `product_id`. Entries are created when a publish/sync to OLX fails — recording `type=0`, the product ID, and the error message. The UI lists each entry with the product name, image, link to edit the product, the parsed OLX error message, and a timestamp.

### Full error detail surfaces — including OLX field-level validation

When OLX returns a 400 error with per-field validation, each `field` and `title` is concatenated and saved. The merchant sees e.g. "title - too short" + "category_id - required" in the same row. Higher-level HTTP errors (401 not logged in, 403 forbidden, 404 not found, 406 not acceptable, 429 rate limit, 500 server error) are appended as `error_other - {code}`.

### Per-row delete and bulk clear

The merchant can delete a single entry by ID, or click "Clear" to truncate the entire history table. So the log is NOT append-only from the merchant's perspective — manual clearing is supported.

### Linked product required

The listing only includes entries whose linked product still exists in CloudCart — entries whose product was deleted are filtered OUT. The merchant only sees errors for products that still exist.

### No automatic log retention

There is no cron / scheduled job that prunes OLX history. Entries persist indefinitely until the merchant manually deletes them (per-row delete or the **Clear** bulk action). The merchant is responsible for housekeeping if the log grows large.

### No export of the history log

There is no Export / Download endpoint for the history. To take the log off-platform for analysis or to share with support, the merchant has to copy rows out of the UI manually (screenshot, copy/paste).

### Two log types — History (publish failures) and Exceptions (lower-level)

History entries are the merchant-facing failure log. Separately, the integration writes deeper exceptions to the platform's `Exceptions` table (via the platform code) for support / engineering — those include the OLX response body for diagnosing rare cases. The merchant only sees the History tab; the Exceptions table is internal.

### History only records publish (type 0) failures with product_id

The current History model has `type = 0` (publish failure) records. Other operation types (refresh, category mapping save, parameter mapping save, advert delete) are NOT written to this table — they go straight to platform-wide system logs. So the merchant can only audit publish/sync attempts here, not the full breadth of OLX operations.

### Truncated when the merchant disconnects

Disconnecting OLX (via [[apps-olx-settings]]) truncates the History table along with adverts and mappings. The merchant cannot recover historical errors after disconnect — they have to keep notes or screenshots before disconnecting.

## Open questions
