---
type: feature
nav_path: "Orders → Export → Delivery"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders
aliases: ["Orders export delivery", "Orders export email link", "Orders export ZIP download", "Export file ready notification", "Export archive folder", "Export file retention"]
tags: [orders, export, email, notification, files, s3]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-export]]. See the hub for related aspects (trigger / 2FA, sync vs async, CSV schema, filter scope, permissions / plan).

# Orders export — delivery (sync vs async paths)

## Purpose

Documents **how the exported file reaches the merchant** — browser download for sync (≤ 50 orders), email link + in-app alert + Files page entry for async (>50 orders). Also covers the silent-failure case when the merchant has disabled notification emails, file retention rules (indefinite, no auto-purge), and the storage layout on Hetzner Object Storage.

## Where to find it

- **Sync** — the browser downloads the CSV immediately after the [[orders-export-trigger-2fa]] modal verifies.
- **Async** — three surfaces:
  - The merchant's admin email inbox (when notifications are enabled).
  - The in-app notification bell at the top of the admin (always fires).
  - [[settings-files]] → **Archive** folder (the canonical persistent location).

## What the merchant can do here

- Click the download link in the email — the link does NOT expire (see retention rule below).
- Click the in-app alert — same direct download link + a deep-link to the Filemanager entry.
- Browse to [[settings-files]] → Archive to retrieve a previously generated export.
- Manually delete a previously generated export from [[settings-files]] (storage cleanup is merchant-driven).

## Settings & fields

### Per-merchant notification gating

The "your file is ready" email goes through the platform's admin-notification pipeline, which checks **two** settings before sending:

| Setting key | Required value | What it controls |
|---|---|---|
| `administrator_email_notifications` | `yes` | Global "send me emails" toggle for the merchant. |
| `mail_file_download` | `yes` | Per-event toggle for export-ready / file-download notifications. |

If either setting is OFF, the file is generated and uploaded but **no email goes out** — the merchant must check the [[settings-files]] page to find the ZIP. This is the silent-failure case for merchants who disable notification noise but still expect the email.

### In-app alert — always fires

In addition to the email, the platform creates an in-app success alert (the notification bell at the top of the admin) when the export ZIP is ready. This alert contains both a direct download link and a link to the file in the Files page. **The alert is independent of the email** — even if the email is suppressed or never arrives, the alert appears in the notification bell.

### Storage layout

| Surface | Where the file lives |
|---|---|
| Sync CSV (≤ 50 orders) | Built in-memory on the server, streamed to the browser as a download. **Not persisted.** |
| Async ZIP (>50 orders) | Filemanager record with `dir=archive`, `mime=application/zip`, `storage_backend=s3` — physical file at `/{site_id}/files/archive/` on Hetzner Object Storage. From the merchant's perspective: [[settings-files]] → Archive folder. |

### File retention

The generated ZIP (and the URL in the email) does **NOT expire** — it works as long as the file exists. There is **no scheduled cleanup job** that auto-purges old export files; they persist until manually deleted (e.g., by the merchant from [[settings-files]], or by CloudCart support during storage cleanup).

## Business rules

### Sync delivery — no persistent record

For small exports (≤ 50 orders), the CSV is built in-memory on the server, returned to the browser, and never stored. If the merchant closes the browser before the download completes, they must re-run the export.

### Async ZIP assembly — streamed multi-part upload

For large exports, each chunk CSV is uploaded as a Filemanager file first, then a `finally` step streams all the Filemanager files into a single ZIP at a server-side temp location, then uploads the assembled ZIP to S3-compatible storage (Hetzner Object Storage) via multipart upload (5 MB parts, retryable). Once the ZIP is on S3 and the Filemanager row is saved, the individual chunk CSV files are deleted to clean up. If the ZIP-row save fails, the platform deletes the orphaned S3 object inline so storage doesn't leak.

### Partial completion not delivered

If the async export's `finally` step never runs (because a chunk job exhausted retries — see [[orders-export-sync-vs-async]]), the merchant receives **no email, no in-app alert, and no Archive entry**. The merchant must re-run the export. Partial chunk CSV files are not exposed.

### Email + in-app alert are not redundant

The email is conditional on `administrator_email_notifications=yes` + `mail_file_download=yes`. The in-app alert is unconditional. For a merchant who has both notifications off and a busy notification bell, the file may sit unclaimed in [[settings-files]] → Archive — diagnostic clue when a ticket says "my export never arrived."

### Single email per export

One email per completed batch. The rapid-click no-dedup behaviour documented in [[orders-export-sync-vs-async]] means multiple clicks produce multiple emails — each with its own download link to a separately generated ZIP.

## Related

- [[orders-export]] — hub.
- [[orders-export-sync-vs-async]] — the threshold and queue mechanics that decide which delivery path runs.
- [[orders-export-trigger-2fa]] — where the merchant initiates the export.
- [[orders-export-csv-schema]] — what's inside the file the merchant receives.
- [[settings-files]] → Archive folder — canonical persistent location.
- [[settings-admin-notifications]] — `administrator_email_notifications` + `mail_file_download` toggles.
- [[settings-general]] — `site_email` as default notification recipient.

## Open questions

None.
