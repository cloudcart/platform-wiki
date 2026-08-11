---
type: feature
nav_path: "Customers → Export customers → Trigger & 2FA"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_customers
aliases: ["Export customers button", "Customer export 2FA", "Export 2FA modal", "Two-factor export gate", "Експорт на клиенти — 2FA"]
tags: [customers, export, 2fa, trigger]
plan_gates: ["customer_export"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-export]]. See the hub for the other aspects (filter scope, sync vs async, CSV schema, plan & permissions).

# Export customers — trigger & 2FA

## Purpose

This aspect covers **how the merchant launches a customer export and the two-factor authentication gate that guards every export**. The Export customers action is not a sidebar page — it is a header button on the Customers list, and clicking it always opens a 2FA modal before any data leaves the store.

## Where to find it

Sidebar → **Customers** → **Export customers** button in the page header (top-right, next to **Import** and **+ Add customer**).

The button is rendered by the Customers list header. The working flow is the **legacy** header (`CustomersIndex`); in the modern variant (`CustomersMainPage`) the handler is currently a stub, so the legacy header is what actually launches the export.

## What the merchant can do here

### Trigger an export

- Click the **Export customers** button in the Customers list header.
- A **Two-factor authentication** modal opens before the export runs (required for every export — even repeated exports inside the same admin session).
- Enter the 6-digit code from the authenticator app (TOTP, 2-minute expiry) OR the 6-digit code sent to the admin's email when the admin has Email-2FA enabled (60-minute expiry — see [[account-cc2fa]], [[account-cc2fa-email]]).
- On a valid code, the export runs against the current filter state (see [[customers-export-filter-scope]]) and either downloads directly or is queued (see [[customers-export-sync-vs-async]]).

### What the merchant CANNOT do here

- Skip the 2FA modal — there is no "remember this device" or "skip for 5 minutes" option.
- Reuse a previous code — each export creates a new authentication task.
- Run the export without any 2FA configured — there is no bypass.

## Settings & fields

### 2FA gate

| Field | Value |
|-------|-------|
| **Authentication code** | 6-digit numeric code, required |
| **Authentication type** | `cc2fa` (authenticator app) OR `cc2fa_email` (email fallback) |
| **TOTP code expiry** | 2 minutes |
| **Email code expiry** | 60 minutes |
| **Modal title** | *"Two-factor authentication"* |

The modal shows the signed-in admin's avatar and email plus the help text *"Open your two-factor authenticator (TOTP) app or browser extension to view your authentication code."* (or the email equivalent when on email-2FA).

## Business rules

### Every export needs a fresh 2FA code

Each click on **Export customers** opens the 2FA modal — there is no "remember this device" or "skip 2FA for 5 minutes" option. The platform creates a new authentication task each time, valid for 2 minutes (authenticator) or 60 minutes (email). After the code is verified and the export starts, the task is marked verified and cannot be reused.

### No 2FA configured means no export

If the admin doesn't have an authenticator app set up AND doesn't have Email-2FA enabled, the export cannot run — there is no bypass. The merchant must first configure 2FA from [[account-cc2fa]] / [[account-cc2fa-email]].

### Authentication task lifecycle

A `CC2FaTasks` log row is created with `action = export_customers` and `status = pending`, then promoted to `verified` after the code is validated. The export itself modifies no customer record and fires no webhook — see [[customers-export-plan-permissions]] for the full side-effect list.

## Related

- [[customers-export]] — hub.
- [[customers]] — the parent list page that hosts the **Export customers** button.
- [[account-cc2fa]] — authenticator-app 2FA setup; required to authorise exports.
- [[account-cc2fa-email]] — email fallback for 2FA; required if the merchant has no authenticator app.
- [[settings-staff]] — moderator permission grants (the button is hidden without the export grant).

## Open questions

(All resolved.)
