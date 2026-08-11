---
type: feature
nav_path: "Invoices → Export → Trigger & delivery"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_invoices
aliases: ["Invoices export trigger", "Launch invoice export", "Invoice export 2FA modal", "Invoice export scope", "Стартиране на експорт на фактури"]
tags: [orders, invoices, export, csv, 2fa, async]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices-export]]. See the hub for the other aspects (column schema, credit-note rows, async processing).

# Invoices export — trigger & delivery

## Purpose

Covers **how the merchant launches the invoice CSV export** and how the result comes back: the top-right **Export** header button, the shared two-factor verification modal, how the export scope is captured from the applied filter chips (not selected rows), the 10-invoice synchronous-vs-asynchronous threshold, and the resulting filenames.

## Where to find it

Sidebar → **Invoices** → **Export** — the top-right header button, next to **Download**.

The Export action is the header button; there is **no** per-row bulk menu, **no** row checkboxes, and **no** date-range picker. Like other 2FA-protected actions, clicking Export opens a verification modal before producing the file (when 2FA is active on the admin).

## What the merchant can do here

### Export the filtered list

1. Optionally narrow the list via the [[orders-invoices-list-filters|filter panel]] (date / credit-note / customer / search box).
2. Click **Export** (top-right header).
3. Verify via 2FA code (when 2FA is active).
4. Receive the CSV directly (small set) or an email link (large set).

The Export button forwards the **list's current filter query** to the export action, but the action reads only the legacy `extra.ids` parameter — which the current UI no longer sends — so the export currently covers **every invoiced order regardless of the applied filter** (the filter narrows only the on-screen list). It does **not** depend on selecting rows — the list has no row selection.

### Receive the result

| Volume | Delivery |
|--------|----------|
| Up to **10 invoices** | Synchronous — CSV downloads directly in the browser. |
| Over **10 invoices** | Asynchronous — chunked at 500 per background job; emailed when complete. Toast: *"The export is being processed. You will receive an email with the download link."* See [[invoices-export-async-processing]]. |

### What the merchant CANNOT do here

- Skip 2FA when 2FA email is enabled.
- Resume / cancel a running async job.
- Export invoices for orders that don't have an invoice number — the list itself only shows invoiced orders.

## Settings & fields

### Two-factor authentication confirmation (shared modal)

When 2FA is active for the admin (`2fa_email` platform flag enabled OR `cc2fa_secret` configured on the admin), the Export button opens the platform's shared 2FA verification modal. See [[orders-export]] *"Two-factor authentication confirmation"* for the full field list. Submit posts the OTP code to the `export_invoices` action — the response `type` tells the frontend handler what to do next:

- `type=csv` (≤ threshold) → the frontend CSV handler converts the returned rows to a CSV file and triggers a browser download.
- `type=queue` (over threshold) → toast *"The export is being processed. You will receive an email with the download link."*

When 2FA is not active, the verification step is skipped — the action fires the export immediately.

### 2FA expiry windows

| 2FA type | Expires after |
|----------|---------------|
| 2FA email (default) | 60 minutes |
| 2FA app (TOTP) | 2 minutes |

### Sync / async threshold

| Parameter | Value | What it controls |
|-----------|-------|------------------|
| **limit** | 10 | Threshold at/below which the export runs synchronously. At or below 10 invoices, the CSV is returned directly. |
| **chunk** | 500 | Async chunk size — when going async, each background job processes 500 invoices. |

### Scope — currently all invoiced orders (the filter is not applied)

The Export button forwards the list's filter query (the same chips shown on screen: **Date** / **Credit note** / **Customer**, plus the search box), but the `export_invoices` action reads only the legacy `extra.ids` parameter, which the current UI no longer sends. So the filter is **not** applied to the export: it currently covers **every invoiced order** regardless of the on-screen filter (the same is true of the **Download** button). It does **not** collect ticked rows — the list has no row selection — and there is no separate date-range picker.

### Filename pattern

- Synchronous: `invoices-YYYY-MM-DD-HH-MM-SS.csv` (single file).
- Asynchronous: split into parts — `invoices-export-YYYY-MM-DD-HH-MM-part_1.csv`, `part_2.csv`, etc., bundled into a single ZIP archive named `invoices-YYYY-MM-DD-HH-MM-SS.zip` (see [[invoices-export-async-processing]]).

## Business rules

### Scope — no row selection, no header picker, filter not applied

Unlike the earlier list UI (which had per-row checkboxes and a bulk dropdown), the current Invoices list has **no row selection**. The Export button forwards the applied filter query, but the action does not consume it — so **there is currently no way to export only a slice**: every run covers **all** invoiced orders. Filtering the list first changes what the merchant sees, not what the file contains.

### Async threshold — 10 invoices

The synchronous threshold (10) is lower than the orders-export threshold (50). This reflects that invoice-export queries are more expensive (they join orders + customers + addresses + invoice fields). When the scope is more than 10 invoices, the platform queues the work automatically and delivers by email.

### Two header actions: Export (CSV) vs Download (PDF)

The Export button (CSV register) sits next to the **Download** button (PDF bundle — see [[orders-invoices-list-bulk]] / [[orders-invoices-download]]). The merchant chooses based on downstream need — CSV for spreadsheet / ERP, PDF for archive / printing. Neither currently applies the list filter to the file — both cover all invoiced orders.

### Side effects

- 2FA verification creates a temporary auth task record.
- **Synchronous (≤10 invoices)**: builds the CSV in memory, returns the rows to the browser, and the frontend's CSV handler triggers the download — no server-side persistence.
- **Asynchronous (>10 invoices)**: queues background jobs that produce CSV parts and a final ZIP, delivered by email — see [[invoices-export-async-processing]].

## Related

- [[orders-invoices-export]] — hub.
- [[orders-invoices]] — parent invoices list (Export is a header button).
- [[orders-invoices-list-filters]] — the filters the Export button consumes (and where to set the period).
- [[orders-invoices-list-bulk]] — the Download + Export header actions overview.
- [[orders-invoices-download]] — sibling PDF bundle Download.
- [[orders-export]] — orders export; the shared 2FA modal field list lives there.
- [[settings-staff]] — the invoices permission grant.
- [[settings-queue-view]] — async job status for large exports.

## Open questions

(none.)
