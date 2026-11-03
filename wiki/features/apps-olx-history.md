---
type: feature
nav_path: "Apps → OLX → History"
route_name: apps.olx.history
route_path: /admin/apps/olx/history
aliases: ["OLX History", "OLX operation log", "OLX activity log", "OLX audit"]
tags: [apps, olx, marketplace, history, audit, log]
plan_gates: []
created: 2026-05-21
updated: 2026-10-21
source_count: 2
---
# OLX → History

## Purpose

The **History** tab is the **error log** of OLX product publishing and syncing — each failed publish or sync, and each advert OLX accepted but is not showing. Each row records the product, the message and the time.

Used by the merchant + support for **troubleshooting**:
- "Why did this product fail to publish?" — find the row + read the error.
- "When did this advert get rejected?" — find the product's row and read its date.

For the OLX feature set, see [[apps-olx]].

## Where to find it

Sidebar → Apps → OLX → **History tab**. Route: `/admin/apps/olx/history`.

## What the merchant can do here

### View operation history

| Column | Notes |
|---|---|
| **Product** | The product's image and name, linking to its edit page. |
| **Message** | A **View** link that opens a pop-up with the error text. |
| **Created** | When the entry was written. |
| (delete) | Deletes this entry. |

A **Clear all events** button above the table empties the whole history.

### No filters

The list has no filters or search; it is paged.

### View the message

**View** in the **Message** column opens a pop-up with the error text. The request sent to OLX and OLX's full response are not shown.

### What the merchant CANNOT do here
- Edit log entries (they can only be deleted, one by one or all at once).
- Re-run an operation directly from this view (must navigate to the relevant entity — [[apps-olx-products]] for re-publish, etc.).

## Settings & fields

### Per-log-entry fields

| Field | Notes |
|---|---|
| **Product** | The product the publish or sync was for. |
| **Error message** | OLX's validation errors (one line per field), OLX's error text, or the platform's own message. |
| **Created** | When the entry was written. |

### Common messages

- One line per field OLX rejected — the field name, a dash, and OLX's reason (e.g. **title** - too short).
- "OLX accepted the advert but is not showing it (status). Update it in your OLX account to make the changes visible."
- "An unexpected error occurred, please try again later or contact support." — followed by the error code (403, 404, 406, 429 or 500) when OLX returned one.
- "You are not logged in to your account" — when OLX refused the connection.

## Business rules

### Retention

Entries are kept until the merchant deletes them or disconnects OLX (see *How it works* below). Critical for compliance is the [[apps-gdpr-acceptance]] log (separate), not this operation log.

### Per-product correlation

Each row links to its product's edit page. There is no per-product filter; the merchant scans the list for the product.

### Side effects of viewing
- No API calls to OLX (read from local DB).
- Read-only — no state changes.

### Permission
Standard apps permission scope.

## Related

- [[apps-olx]] — OLX hub.
- [[apps-olx-products]] — products + publishing.
- [[apps-olx-adverts]] — live OLX adverts.
- [[apps-olx-configuration]] — category mapping (not recorded here).
- [[apps-olx-parameters]] / [[apps-olx-parameters-values]] — parameter mapping (not recorded here).
- [[apps-olx-settings]] — disconnecting there empties this history.

## How it works (verified against backend)

### History records publish failures only

The history stores failures tied to a product. Entries are created when a publish or sync to OLX fails, or when OLX accepts an advert but does not show it — recording the product and the message. The UI lists each entry with the product name, image, link to edit the product, the parsed OLX error message, and a timestamp.

### Full error detail surfaces — including OLX field-level validation

When OLX returns a 400 error with per-field validation, each `field` and `title` is concatenated and saved. The merchant sees e.g. "title - too short" + "category_id - required" in the same row. Higher-level HTTP errors (403 forbidden, 404 not found, 406 not acceptable, 429 rate limit, 500 server error) are appended as "An unexpected error occurred, please try again later or contact support. - {code}"; a 401 appends "You are not logged in to your account".

### Per-row delete and bulk clear

The merchant can delete a single entry from its row, or click **Clear all events** to empty the entire history. So the log is NOT append-only from the merchant's perspective — manual clearing is supported.

### Linked product required

The listing only includes entries whose linked product still exists in CloudCart — entries whose product was deleted are filtered OUT. The merchant only sees errors for products that still exist.

### No automatic log retention

There is no cron / scheduled job that prunes OLX history. Entries persist indefinitely until the merchant manually deletes them (per-row delete or **Clear all events**). The merchant is responsible for housekeeping if the log grows large.

### No export of the history log

There is no Export / Download endpoint for the history. To take the log off-platform for analysis or to share with support, the merchant has to copy rows out of the UI manually (screenshot, copy/paste).

### Two log types — History (publish failures) and Exceptions (lower-level)

History entries are the merchant-facing failure log. Separately, the integration writes deeper exceptions to the platform's `Exceptions` table (via the platform code) for support / engineering — those include the OLX response body for diagnosing rare cases. The merchant only sees the History tab; the Exceptions table is internal.

### History only records publish (type 0) failures with product_id

The current History model has `type = 0` (publish failure) records. Other operation types (refresh, category mapping save, parameter mapping save, advert delete) are NOT written to this table — they go straight to platform-wide system logs. So the merchant can only audit publish/sync attempts here, not the full breadth of OLX operations.

### Truncated when the merchant disconnects

Disconnecting OLX (via [[apps-olx-settings]]) truncates the History table along with adverts and mappings. The merchant cannot recover historical errors after disconnect — they have to keep notes or screenshots before disconnecting.

## Open questions
