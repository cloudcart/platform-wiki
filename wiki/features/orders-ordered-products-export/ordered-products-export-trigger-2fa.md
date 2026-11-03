---
type: feature
nav_path: "Orders → Ordered Products → Export → Trigger / 2FA"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders_products
aliases: ["Ordered Products export button", "Ordered Products export 2FA", "Products by orders export trigger", "Aggregated product export verification"]
tags: [orders, products, export, 2fa, csv]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-ordered-products-export]]. See the hub for related aspects (CSV schema, sync vs async, filter scope, delivery, permissions / plan).

# Ordered Products export — trigger & 2FA

## Purpose

Documents the **Export button** on the [[orders-ordered-products]] page, where it lives, and the **two-factor authentication confirmation** the merchant passes through before the aggregated product CSV is produced. The 2FA step is shared with every other CSV export on the platform — this page covers the parts specific to the Ordered Products export plus the conditions under which the modal appears at all.

## Where to find it

From [[orders-ordered-products]] → top-right header → **Export** button (primary blue). It sits in the same header as the page filters, so the merchant sets filters first, then clicks Export.

When the platform 2FA email functionality is active (or the admin has a TOTP secret), the button opens the shared verification modal before the export runs. When 2FA is not in play, the export fires immediately with no modal.

## What the merchant can do here

1. Apply filters on the [[orders-ordered-products]] page to narrow the pivot.
2. Click **Export**.
3. Verify via 2FA code (when 2FA is active on the admin — same modal as [[orders-export-trigger-2fa]]).
4. Receive the CSV — see [[ordered-products-export-delivery]].

The merchant CANNOT skip 2FA when the 2FA email functionality is active, and cannot choose the output format from this modal (CSV only).

## Settings & fields

### Two-factor authentication confirmation (shared modal)

This export uses the **same shared 2FA verification modal** as every other CSV export action. See [[orders-export-trigger-2fa]] for the full field list (avatar, signed-in-as line, OTP code input with text-security disc masking, expiry notice, helper text). The modal's form posts directly to this export's route — on success the frontend's `cc.ajax.success` handler routes the response by `type`:

- `csv` → CSVHandler download (synchronous result).
- `zip` → ZipHandler download.
- `queue` → toast confirming the async export was enqueued.

### 2FA expiry windows

| 2FA type | Expires after |
|----------|---------------|
| 2FA email (default) | 60 minutes |
| 2FA app (TOTP) | 2 minutes |

## Business rules

### 2FA gating is conditional on a platform flag — NOT always on

The 2FA email modal only appears when the platform-wide `2fa_email` functionality flag is enabled (it defaults OFF). When OFF and the admin has no TOTP-app secret configured, the Export button fires immediately without a verification modal. The 2FA email is NOT a hard requirement on every store. This matches the orders export — see [[orders-export-trigger-2fa]].

### 2FA is per-admin

Whether the modal appears depends on the **admin's** configured 2FA, not a store-level setting alone. Two staff members on the same store can have different experiences.

### Verification creates a temporary auth task

A successful 2FA verification creates a temporary auth task record that authorises the export request. The merchant never sees this; it is the mechanism that lets the export route trust the click.

## Related

- [[orders-ordered-products-export]] — hub.
- [[orders-ordered-products]] — parent pivot page (the Export button lives here).
- [[orders-export-trigger-2fa]] — the shared 2FA modal, documented in full for the orders export.
- [[ordered-products-export-delivery]] — what happens after verification (sync download vs async email).
- [[settings-staff]] — per-admin 2FA configuration.

## Open questions

None.
