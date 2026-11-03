---
type: feature
nav_path: "Invoices → Download → Entry point & 2FA"
route_name: admin.core.export
route_path: /admin/api/core/export-import/download_invoices
aliases: ["Invoice download button", "Download invoices button", "Invoice download 2FA", "Download invoices verification", "Изтегли фактури"]
tags: [orders, invoices, download, 2fa, ui]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---
# Invoices bulk download — entry point & 2FA

> Part of [[orders-invoices-download]]. See the hub for related aspects (scope, sync/async, rendering, permissions/plan).

## Purpose

Documents the **single Download button** that triggers a bulk invoice download, the **two-factor verification** step that gates it, and the response types the frontend reacts to after verification. This is the entry point for the `download_invoices` action; note that the download currently covers **all** invoiced orders regardless of the applied filter (see [[invoices-download-scope]]).

## Where to find it

From [[orders-invoices]]:

- **Download** — the top-right header button (ghost style, with a file-arrow-down icon), next to **Export**. There is no per-row selection, no "Download all (X)" counter, and no date-range picker beside it.

Clicking **Download** opens the platform's shared 2FA verification step before the download runs (when 2FA is active on the admin).

## What the merchant can do here

1. Optionally narrow the list first via the [[orders-invoices-list-filters|filter panel]] (an unfiltered list downloads everything — see [[invoices-download-scope]]).
2. Click **Download**.
3. Verify with a one-time code (when 2FA is active).
4. Receive the PDF bundle in the browser, or (for large sets) an email link.

### Two-factor verification (shared step)

When 2FA is active for the admin, clicking **Download** opens the platform's shared two-factor verification dialog — the same one used by [[orders-export]] and documented as the list-level guard in [[orders-invoices-list-verification]]. The dialog shows:

- The admin avatar + a *"Signed in as"* line.
- A one-time **Authentication code** input.
- A short instruction (email 2FA: *"Enter the code sent to your email…"*; TOTP: *"Open your two-factor authenticator (TOTP) app…"*) plus an expiry notice.
- **Verify** (submit the code + run the action) and **Cancel** (abort).

Which kind of code applies depends on the admin's setup: an **email** one-time code (sent to the admin's email) when only email 2FA is active, or a **TOTP** code from an authenticator app when the admin has an authenticator secret set.

When 2FA is NOT active for the admin, the verification step is skipped and the action fires immediately.

Cancelling (closing the dialog) aborts the verification — nothing is downloaded or queued. The merchant can re-trigger **Download** at any time.

### Response-type handling (what happens after Verify)

The action's JSON response tells the frontend what to do next:

- **`type = zip`** (set at or below the sync threshold) — the browser decodes the bundle and triggers a Save File dialog. See [[invoices-download-sync-async]] for the synchronous path.
- **`type = queue`** (over the threshold) — a toast appears: *"The export is being processed. You will receive an email with the download link."* The bundle is built in the background and delivered by email (see [[invoices-download-sync-async]]).
- **`status = error`** with `no_targeted_orders_nor_all` — an empty scope; the merchant is told there is nothing to download (see [[invoices-download-scope]]).

## Settings & fields

### 2FA code expiry windows

| 2FA type | Code expires after |
|----------|--------------------|
| Email one-time code (default) | 60 minutes |
| Authenticator app (TOTP) | 2 minutes |

## Business rules

- **One entry point, one action** — the header **Download** button is the only way in; it calls the `download_invoices` action. There is no second (row-selection / "Download all") entry point in the current UI.
- **2FA cannot be skipped when active** — every bulk download goes through verification whenever 2FA is active for the admin. When 2FA is not active, the step is skipped automatically.
- **Verification creates only a temporary auth task** — passing the code creates a short-lived verification record (see the expiry windows above); no permanent state is created by verifying.

## Open questions

(none.)

## Related

- [[orders-invoices-download]] — hub.
- [[orders-invoices]] — parent invoices list (the button lives here).
- [[orders-invoices-list-verification]] — the same 2FA step, documented as the list-level guard shared with Export.
- [[orders-export]] — shares the platform's 2FA verification dialog.
- [[settings-staff]] — `invoices.download` permission grant.
