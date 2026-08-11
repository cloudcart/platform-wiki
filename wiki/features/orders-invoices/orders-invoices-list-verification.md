---
type: feature
nav_path: "Invoices → 2FA verification"
route_name: admin.invoices.list
route_path: /admin/invoices
aliases: ["Invoice 2FA modal", "Invoice download verification", "Bulk invoice OTP", "2FA преди изтегляне на фактури"]
tags: [orders, invoices, list, 2fa, security]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices]]. See the hub for the other aspects (list table, filters, bulk download / export).

# Invoices — 2FA verification modal

## Purpose

Both header actions on [[orders-invoices]] — **Download** (PDF bundle) and **Export** (CSV) — open a shared two-factor verification step BEFORE the action runs, when 2FA is active on the admin. The step protects bulk extraction of invoice data (customer names, totals, invoice numbers) behind a one-time code. This page documents when the modal appears, what it asks for, and the three possible outcomes after the merchant submits.

## Where to find it

Sidebar → **Invoices**. The modal opens on click of **Download** or **Export** — it is not a standalone screen.

## What the merchant can do here

- **Enter the one-time code** to authorise the bulk action.
- **Cancel** — closing the modal aborts the action; nothing is downloaded or queued.
- **Skip the step entirely** — when 2FA is not active on the admin, the action fires directly without this dialog.

## Settings & fields

The modal is the platform's shared verification dialog — the same one documented for [[orders-export]]. It shows:

- The admin avatar + a "signed-in-as" line.
- An OTP code input, masked with `text-security` disc characters.
- An expiry notice and helper text.
- **Submit** (verify + run the action) and **Cancel** (abort).

## Business rules

### Modal gating — only when 2FA is active

The modal step appears only when 2FA is active on the admin: either the platform-wide `2fa_email` flag is enabled OR the admin has a `cc2fa_secret` set. When NEITHER is true, the modal is skipped and the action fires immediately. So whether a merchant sees the OTP prompt depends on their store's 2FA configuration, not on the action.

### Captured at open — the request payload is fixed when the modal opens

The action's request payload (the list's current filter query, forwarded by the button) is captured when the modal opens, so changing the filter while it is open does not change the request. There is no row selection to capture. (Note: the download / export currently cover **all** invoiced orders regardless of that filter — see [[orders-invoices-list-bulk]].)

### Three outcomes after successful submission

After the merchant submits a valid code, the modal closes and one of three outcomes happens based on the JSON response `type`:

| Response `type` | Outcome |
|-----------------|---------|
| `csv` | Frontend CSVHandler triggers an immediate browser download. |
| `zip` | Frontend ZipHandler triggers an immediate browser download (PDF bundle). |
| `queue` / fallback | Toast: *"The export is being processed. You will receive an email with the download link."* |

The `queue` outcome is what happens for large jobs that exceed synchronous limits — the work moves to the background queue (see [[settings-queue-view]]) and the merchant receives the file by email.

### Cancel aborts cleanly

Closing the modal = action aborted. No partial download, no queued job. The merchant can re-trigger the action at any time.

## Related

- [[orders-invoices]] — hub.
- [[orders-invoices-list-bulk]] — the two actions (Download / Export) this modal guards + the scope behaviour.
- [[orders-export]] — the shared verification modal's full field list.
- [[settings-queue-view]] — where the `queue`-outcome job's status appears.

## Open questions

None.
