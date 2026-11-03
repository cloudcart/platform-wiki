---
type: feature
nav_path: "Customers → Customer details → Change password"
route_name: (modal — no dedicated route)
route_path: /admin/customers/details/:id (modal action)
aliases: ["Change customer password", "Set customer password", "Reset password", "Промяна на парола на клиент", "Смяна на парола"]
tags: [customers, password, security, modal]
plan_gates: []
created: 2026-05-21
updated: 2026-11-03
source_count: 6
---
# Change customer password

## Purpose

The merchant's flow to **set a specific password for a customer directly** — distinct from the bulk "Change password" action on the [[customers]] list, which sends password-reset LINKS instead. This modal assigns an exact password the merchant chooses. Typical use cases:

- A customer forgot their password and the merchant sets a temporary one to walk them through login.
- B2B accounts where the merchant manages passwords for a team of buyers.
- An old customer record needs its password reset to a known value for support.

## Where to find it

From [[customers-details]] → click the **pencil icon** on the customer's identity card → dropdown shows: Edit customer / **Change password** / (when email unverified) Confirm email / Send confirmation email. Click **Change password** → a centred small modal opens.

This is NOT the bulk "Change password" on the [[customers]] list — that one emails reset links and doesn't let the merchant pick the password.

## What the merchant can do here

A small centred modal (md size, no header / no footer). ESC-close is blocked, and backdrop-close is blocked while a submit is in progress. Both fields render only while the modal is visible. Contents:

| Element | Key | Notes |
|---------|---------|-------|
| **Title** | — | *"Change password"* |
| **New password** | `password` | Masked input with eye-show toggle. Required. Two columns on lg+ viewports. |
| **Repeat password** | `repeat_password` | Masked input. Required. Must match New password. |
| **Cancel** button | — | Ghost. Closes without saving and clears both fields. Disabled during submit. |
| **Save** button | — | Primary. Disabled while either field is empty OR while submitting. Shows spinner during submit. |

On valid input the platform POSTs `{customer_id, password, repeat_password}` to the change-password endpoint. On success: toast *"Password changed successfully"* and the modal closes. The merchant must then communicate the new password to the customer through a **secure side channel** (phone, in person, secure messenger) — the customer is emailed only a change *notification*, never the new plaintext value (see Business rules).

**What the merchant CANNOT do here:**

- See the customer's existing password — passwords are stored hashed and cannot be retrieved. Set a new one only.
- Auto-email the new password to the customer in plaintext.
- Change passwords for multiple customers at once — use the [[customers]] list bulk action (reset links) for that.

## Settings & fields

| Field | Required | Validation |
|-------|----------|-----------|
| **New password** | Yes | Min 6 chars client-side; 3–20 chars enforced by backend. |
| **Repeat password** | Yes | Must match New password. |

Two client-side validators run on Save, with inline errors under the respective field. If either fails, the form does not submit:

| Validation | Error message |
|------------|---------------|
| Password length < 6 chars | *"The password must be at least 6 characters."* (translated, `{min}` substitution) |
| New password ≠ Repeat password | *"The repeat password and password must match."* |

## Business rules

### This flow vs the bulk password-reset flow

The merchant has two password-related flows, for different scenarios:

| Flow | Where | Effect |
|------|-------|--------|
| **Change password (this modal)** | Customer details → pencil dropdown | Merchant sets a SPECIFIC password directly; informs the customer via a secure side channel. |
| **Bulk Change password** | [[customers]] list → bulk action | Sends password-RESET emails; selected customers click the link and set their own new password. |

This modal is for direct intervention ("I'm setting up an account on behalf of a customer"); the bulk action is for self-service reset ("I want my customers to reset their own passwords").

### Validation is client-side; backend re-validates a stricter range

The min-6 and match checks run in the browser before the request is sent. The backend then enforces a **3–20 character** range: a 21-character password passes the modal but is rejected at the model level with `'customer.err.password_max_chars_20'`. Server errors show under the field.

### Customer gets a change notification — but not the new value

The merchant's save triggers a **"Password change"** notification email to the customer's saved address. The email tells the customer their password changed (so they can detect an unauthorized change) but does **not** contain the new plaintext password — the template's password variable receives a placeholder (literal `true` / `has_password`), not the credential. The merchant must still hand over the new password via a secure side channel.

### Next login uses the new password

The customer logs in with the new password the next time they log in.

### Password storage

Passwords are stored hashed. The merchant can only set a new password, never view the old.

### Webhook

The save fires the `customer.updated` webhook; see [[settings-hooks]].

### Permission

The endpoint is gated by the `customers` API permission, so anyone with `customers` access can use this window. See [[settings-staff]].

### Endpoint

The window submits to `POST /admin/api/core/customers/change-password` (gated `hasApiPermission:customers`; `customer_id` must exist in the store's customers, `password` min 6, `repeat_password` must match).

## Related

- [[customers-details]] — parent page; the dropdown action opens this modal.
- [[customers]] — bulk "Change password" sends reset emails (the other flow).
- [[customers-sign-in]] — sign-in-as-customer impersonation (a different security operation).
- [[settings-staff]] — permission grants for sensitive operations.
- [[settings-hooks]] — `customer.updated` webhook fires on the save.
- [[customer]] — entity page.

## Open questions

None.
