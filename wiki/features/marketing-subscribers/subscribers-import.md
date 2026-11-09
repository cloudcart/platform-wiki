---
type: feature
nav_path: "Marketing → Subscribers → Import"
route_name: subscribers.import
route_path: /admin/marketing/subscribers/import
aliases: ["Subscribers import", "CSV import subscribers", "Import wizard", "Bulk subscriber import", "accepts_marketing column", "Marketing consent column", "Импорт на абонати"]
tags: [marketing, subscribers, import, csv, bulk]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (list view, bulk actions, detail modal, channels, settings, lifecycle).

# Subscribers — CSV import wizard

## Purpose

The CSV import brings an external contact list into the audience pool. The wizard validates the file, maps CSV columns to subscriber fields, and dispatches a queued background import; the platform handles dedup, phone normalisation, tag stacking, and plan-cap truncation.

## Where to find it

Click the **Import subscribers** button on the [[subscribers-list-view]] page header. The button is icon `fa-file-arrow-up` (light).

## What the merchant can do here

- After a 2FA check, upload a CSV (up to 10 MB), set the header row, common tags, consent override and verification method, map 8 fields to columns, and queue the import.

## Settings & fields

### Two gates before the wizard opens

1. **2FA challenge** — the merchant must satisfy the platform's 2FA verification for bulk-export-import actions (action key `EXPORT_IMPORT_ACTION_IMPORT_SUBSCRIBERS`).
2. The modal opens; while submitting, only its X closes it.

### The 4-screen wizard

| # | Step label | What the merchant does |
|---|---|---|
| **1** | **Upload CSV** | Drag-and-drop or click to select the CSV file. Hard upload cap **10 MB**. The screen accepts `.csv` files only (the server would also take `.txt`). No sample file is offered: column names are free, since each is mapped in step 3. The Next button stays disabled until a file is picked. |
| **2** | **Settings** | Configure the import-wide options: <br>• **"My file has a header row with column names"** toggle (when ON, row 1 is treated as column names + skipped from import) <br>• **Tags** picker — comma-separated tag list applied to EVERY imported row (combined with per-row tags from step 3 — see "Tag handling" below) <br>• **"Mark imported subscribers as accepting marketing"** toggle (forces `marketing = 1` regardless of per-row value) <br>• **Verification method** dropdown — either *"Mark all as verified"* (skip email verification) OR *"Send email with link to verify"* (send each row a verification email after import) |
| **3** | **Mapping** | For each of the 8 mappable subscriber fields (table below), pick which CSV column it corresponds to (or leave unmapped). The button on this step is labelled **"Import"** instead of **"Next"** — clicking it dispatches the background import. |
| **4** | **Success** | Terminal screen with the import-queued confirmation. Step navigation collapses; the merchant returns to the Subscribers list. |

A **Back** button appears on steps 2 and 3 (not step 1); a step-indicator strip at the top highlights the active step. Refreshing the browser mid-wizard resets to step 1.

### Mappable CSV columns (per-row, configured in step 3)

The 8 fields the merchant can map to CSV columns:

| Column | Required | Notes |
|---|---|---|
| **Email** | one of email/phone required | Must be a valid email; row dropped when invalid AND no valid phone is present. |
| **Phone** | one of email/phone required | Normalised to E.164 against the row's `Country` (if provided) — invalid numbers are silently dropped. |
| **First name** | optional | |
| **Last name** | optional | |
| **Marketing** (consent) | optional | Any column name (e.g. `accepts_marketing`) mapped to this field. Any non-zero whole number (`1`, `2`, …) = consent **on**; `0` = **off**; text such as `yes` / `true` / `no` counts as `0` = **off**. Empty cell, or the field left unmapped = **on**. Applies to every channel of the row (email and phone). |
| **User agent** | optional | Stored on the subscriber for analytics provenance. |
| **Country** | optional | 2-letter ISO code (uppercased); validated against the platform's known-country list. Drives phone-number parsing fallback. |
| **Tags** | optional | **Comma-separated tag names** to attach to that specific subscriber row (e.g., `vip,early-adopter,sofia`). See "Tag handling" below. |

## Business rules

### Tag handling — two sources, merged + de-duplicated

Tags can be set on imported subscribers via **two independent channels**:

1. **Per-row CSV column** — when the CSV file has a `Tags` column mapped to `subscriber.tags`, the comma-separated values become tags on that specific row (e.g., row A gets `vip,sofia`; row B gets `wholesale,partner`).
2. **Import-wide common tags** — a single comma-separated string set once at import-wizard time; applies to **every** imported row in the batch (e.g., `newsletter,jan-2026-campaign`).

The platform merges the two sources — so a subscriber whose CSV row has `vip,sofia` and import-wide common tags `newsletter,jan-2026-campaign` ends up with all four tags: `vip, sofia, newsletter, jan-2026-campaign`. Duplicate names (case-sensitive) are de-duplicated.

If neither source provides a tag, the imported subscriber lands without tags — no automatic default tag is applied.

### Job dispatch + source attribution

Imported subscribers land with `subscribed_from = 'import'` (visible under the "Import" bucket in the "Subscribed from" filter on [[subscribers-list-view]]).

### Plan-cap truncation

The plan's subscriber-count limit is enforced during the import — if the import would exceed the cap, the import truncates and the merchant sees:

> *"You have:has subscribers. Your limit is:limit"*

The truncation drops the trailing rows (rows are processed in order). Rows that fit may stay above the active cap threshold for ~10 minutes until the background recompute — see [[subscribers-lifecycle]].

### Identity resolution applies — imports merge into existing subscribers

The wizard does NOT create one new subscriber per CSV row blindly. Each row goes through the identity-resolution cascade ([[subscribers-channels]]): if the row's email already exists as an Email channel on another subscriber, the import UPDATES that row instead of creating a duplicate. Re-importing a CSV with overlapping contacts won't double the audience size, but it **overwrites** marketing consent on the matched channels with the file's value, and consent **on** also re-subscribes a channel that had unsubscribed.

### Phone normalisation + verification

- **Phone** values are parsed against the row's `Country` (if mapped) and normalised to E.164. Invalid numbers are silently dropped from the Phone channel; the row still lands if Email is valid.
- **"Send email with link to verify"** queues a verification email per imported Email channel — campaigns won't send until clicked (see [[subscribers-channels]]).
- **"Mark all as verified"** sets `verified = 1` immediately. The merchant accepts the deliverability risk — bouncing addresses still flip `bounced = 1` on the first failed send.

### Webhooks fire per row

Each imported subscriber fires `subscriber.created`, so receivers get a burst; there is no separate import webhook.

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-list-view]] — header button that opens this wizard.
- [[subscribers-channels]] — channel-identifier validation + verification mechanics.
- [[subscribers-lifecycle]] — plan-cap rule that drives truncation; source taxonomy (`subscribed_from`).
- [[subscribers-settings]] — plan-cap limits + "Upgrade" CTAs.
- [[background-queue-inventory]] — the queued background import task + its queue.
- [[settings-hooks]] — per-row `subscriber.created` webhook fires.

## Open questions

- The exact 2FA challenge flow (TOTP vs email link vs both) is not documented per merchant; `(verify)` against the 2FA settings in [[account-cc2fa]].
