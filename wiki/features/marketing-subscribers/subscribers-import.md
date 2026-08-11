---
type: feature
nav_path: "Marketing → Subscribers → Import"
route_name: subscribers.import
route_path: /admin/marketing-new/subscribers/import
aliases: ["Subscribers import", "CSV import subscribers", "Import wizard", "Bulk subscriber import"]
tags: [marketing, subscribers, import, csv, bulk]
plan_gates: ["subscribers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers]]. See the hub for related aspects (list view, bulk actions, detail modal, channels, settings, lifecycle).

# Subscribers — CSV import wizard

## Purpose

The CSV import is how a merchant brings an external contact list into the audience pool — newsletter migrations, lead-magnet exports, post-event signups, ERP customer dumps. The wizard validates the file, maps CSV columns to subscriber fields, and dispatches a queued background import; the platform handles dedup, phone normalisation, tag stacking, and plan-cap truncation.

## Where to find it

Click the **Import subscribers** button on the [[subscribers-list-view]] page header. The button is icon `fa-file-arrow-up` (light).

## What the merchant can do here

- Satisfy a 2FA challenge before any data is uploaded.
- Upload a CSV up to 10 MB.
- Toggle whether the first row is a header.
- Set common (import-wide) tags applied to every imported row.
- Mark every imported row as accepting marketing regardless of per-row value.
- Choose between "mark all as verified" or "send each row a verification email".
- Map each of 8 subscriber fields to a CSV column (or leave unmapped).
- Dispatch the import as a queued background task.

## Settings & fields

### Two gates before the wizard opens

1. **2FA challenge** — the merchant must satisfy the platform's 2FA verification for bulk-export-import actions (action key `EXPORT_IMPORT_ACTION_IMPORT_SUBSCRIBERS`).
2. The modal opens — backdrop-close and ESC are disabled while submitting; it can only be closed mid-step via the X in the title bar.

### The 4-screen wizard

| # | Step label | What the merchant does |
|---|---|---|
| **1** | **Upload CSV** | Drag-and-drop or click to select the CSV file. Hard upload cap **10 MB**. Accepted MIME types: `.csv`, `text/csv` only. The Next button stays disabled until a file is picked. |
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
| **Marketing consent** | optional (default 1) | `1` / `0`; empty string → defaults to `1`. |
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

Imported subscribers land with `subscriber_from = 'import'` (visible under the "Import" bucket in the "Subscribed by" filter on [[subscribers-list-view]]).

### Plan-cap truncation

The plan's subscriber-count limit is enforced during the import — if the import would exceed the cap, the import truncates and the merchant sees:

> *"You have:has subscribers. Your limit is:limit"*

The truncation drops the trailing rows (the import is processed in row order). The chronological-max-id rule means newly-imported subscribers that DO fit under the cap may still fall above the active `subscribers.max_id` threshold for ~10 minutes until the background recompute runs — see [[subscribers-lifecycle]] for the cap mechanics.

### Identity resolution applies — imports merge into existing subscribers

The wizard does NOT create one new subscriber per CSV row blindly. Each row goes through the identity-resolution cascade ([[subscribers-channels]]): if the row's email already exists as an Email channel on another subscriber, the import UPDATES that row instead of creating a duplicate. Re-importing a CSV with overlapping contacts won't double the audience size.

### Phone normalisation + verification

- **Phone** values are parsed against the row's `Country` (if mapped) and normalised to E.164. Invalid numbers are silently dropped from the Phone channel; the row still lands if Email is valid.
- **"Send email with link to verify"** queues a verification email per imported Email channel — campaigns won't send until clicked (see [[subscribers-channels]]).
- **"Mark all as verified"** sets `verified = 1` immediately. The merchant accepts the deliverability risk — bouncing addresses still flip `bounced = 1` on the first failed send.

### Webhooks fire per row

Bulk-imported subscribers DO fire `subscriber.created` webhooks per row as the import processes them — receivers should be prepared for a burst. No special "import" webhook exists.

## Related

- [[marketing-subscribers]] — hub.
- [[subscribers-list-view]] — header button that opens this wizard.
- [[subscribers-channels]] — channel-identifier validation + verification mechanics.
- [[subscribers-lifecycle]] — plan-cap rule that drives truncation; source taxonomy (`subscriber_from`).
- [[subscribers-settings]] — plan-cap limits + "Upgrade" CTAs.
- [[background-queue-inventory]] — the queued background import task + its queue.
- [[settings-hooks]] — per-row `subscriber.created` webhook fires.

## Open questions

- The exact 2FA challenge flow (TOTP vs email link vs both) is not documented per merchant; `(verify)` against the 2FA settings in [[account-cc2fa]].
