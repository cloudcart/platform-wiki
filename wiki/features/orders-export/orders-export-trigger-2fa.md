---
type: feature
nav_path: "Orders → Export → Trigger + 2FA"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders
aliases: ["Export 2FA modal", "Orders export 2FA", "Export OTP", "Export authentication code"]
tags: [orders, export, 2fa, otp, modal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-export]]. See the hub for related aspects (sync vs async, CSV schema, delivery, filter scope, permissions / plan).

# Orders export — trigger + 2FA

## Purpose

Documents the **Export** button click + the two-factor authentication modal that gates the export. Two variants exist: an **email-2FA** modal (default for most merchants) and an **authenticator-app TOTP** modal (when the admin has `cc2fa_secret` configured). The modal can also be entirely skipped on stores where the platform `2fa_email` flag is OFF and the admin has no TOTP credential.

## Where to find it

[[orders]] → top-right header → **Export** button → modal opens (size `small`). The modal's form action submits POST directly to `admin.core.export` — there is no separate verify endpoint.

## What the merchant can do here

- Read the signed-in admin email + avatar (50 × 40 px circle, sourced from 150 × 150 profile image).
- Enter the OTP code (masked with `text-security: disc` dots, autocomplete disabled).
- Submit — the form's `cc.ajax.success` handler inspects the JSON response and routes to the right delivery path (see [[orders-export-delivery]]).

The form embeds CSRF + the merchant's filter scope payload (`extra` query param) so the filter survives the modal round-trip — see [[orders-export-filter-scope]].

## Settings & fields

### Modal fields

| Field / element | Type | Description |
|---|---|---|
| Avatar | image (50 × 40 px) | Signed-in admin profile image. |
| *"Signed in as"* line | static | Email of the signed-in admin, bolded. |
| OTP code label | label | *"Authentication code"* (the platform code). |
| OTP code input | text input | Free text, autocomplete disabled, masked with dots. Placeholder *"Enter code"* (the platform code). |
| Expiry notice | static text | *"This code expires at <formatted-date> <timezone>"* (the platform code). Only the email-2FA modal renders this line. |
| OTP info helper | static text | *"Enter the code from your email"* (the platform code). |
| Setup helper | static text | *"To configure 2FA setup..."* (the platform code). |

### 2FA expiry windows

| 2FA type | Expires after | When used |
|----------|---------------|-----------|
| 2FA email (default) | **60 minutes** | Admin has email-based two-factor active and the store has the `2fa_email` flag ON. |
| 2FA app (TOTP) | **2 minutes** | Admin has `cc2fa_secret` set — authenticator app code. |

### Conditional `2fa_email` platform flag

The 2FA email modal only appears when the platform `2fa_email` functionality flag is enabled for the store. The flag defaults to **OFF** platform-wide. When OFF, clicking Export skips the modal entirely (no verification code) and the export fires immediately — provided the merchant has the staff permission grant (see [[orders-export-permissions-plan]]). When ON (or when the admin has TOTP via `cc2fa_secret`), the modal appears.

### CC2FaTasks task lifecycle

When the merchant clicks Export, the platform first hits `GET /admin/api/core/export-import/export_orders?engine=sm` which:

1. Identifies the admin and their 2FA type (TOTP if `cc2fa_secret` is set, else `2fa_email`).
2. Creates (or reuses an active one) a task record with the action `export_orders`, the chunk / limit values, and the console-login auth_id.
3. Renders the appropriate Smarty modal (the platform code for TOTP, the platform code for email-2FA) with the task's expiry time.

The form inside the modal submits POST to the same route with the OTP code. The middleware validates the code against the stored task and only then runs the underlying export — see [[orders-export-sync-vs-async]] for what runs next. After successful execution, the task is marked verified and **cannot be reused** — a second click re-creates a fresh task.

## Business rules

- **2FA is per-admin, not per-store.** Modal appearance depends on the signed-in admin's 2FA configuration, not the store's. If the admin has neither email-2FA nor TOTP active (and the store flag is OFF), the export runs without a verification step.
- **Verification gates access, not the file.** The 2FA step gates access to the export endpoint. Once verified, the actual CSV data is NOT encrypted in transit beyond standard HTTPS. The 2FA protects against unauthorised exports (e.g., a compromised admin session); it does not encrypt the resulting file.
- **One task, one export.** A verified task is marked `STATUS_VERIFIED` and cannot fire a second export — the merchant must re-click to spawn a new task.
- **Expired code blocks the export.** If the merchant doesn't submit within 60 minutes (email) / 2 minutes (TOTP), the task expires and the OTP no longer validates — the merchant must close and re-open the modal.

## Related

- [[orders-export]] — hub.
- [[orders-export-sync-vs-async]] — what runs after verification (sync browser CSV vs queued async).
- [[orders-export-delivery]] — how the result reaches the merchant.
- [[orders-export-filter-scope]] — the `extra` query payload that preserves the filter through the modal.
- [[orders-export-permissions-plan]] — staff permission required to see the Export button at all.
- [[settings-staff]] — admin 2FA configuration surface.

## Open questions

None.
