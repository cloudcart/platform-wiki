---
type: feature
nav_path: "Settings → Staff → Edit profile"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Edit staff", "Edit moderator", "Edit admin", "Staff profile", "Avatar upload", "Password change"]
tags: [settings, staff, edit, profile, avatar, password]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, create, permissions, 2FA, delete, force sign out).

# Staff — edit profile

## Purpose

Documents the Edit modal that opens when the merchant clicks a non-owner row (or the owner row, if they ARE the owner). Covers the four sections in the modal (Profile Summary, Two-factor authentication, Profile, Contacts, Permissions), the avatar upload constraints, the password-change rules, and the field validation caps.

## Where to find it

Sidebar → Settings → **Staff** → click any row in the table. Or deep-link via `#user-<id>` (see [[settings-staff-roles-list]]).

## What the merchant can do here

- Edit the profile (username, email, names) of a moderator or themselves.
- Upload / replace the profile avatar (250×250 max dimensions, 25 KB max file size).
- Change the password via the **Change password** action (with role-based restrictions).
- Configure authenticator-app 2FA via a nested QR modal (see [[settings-staff-2fa]]).
- Edit Contacts (country, city, street, postal code, phone).
- Edit Access permissions (moderators only — see [[settings-staff-permissions-tree]]).
- Save and trigger the `admin_account_changes` admin notification.

## Settings & fields

### Edit modal layout

Implementation: `CcModal` (size `xl`, becomes `xll` when the nested 2FA modal is active). Title depends on row:

- Edit mode (owner row): *"Edit admin"*.
- Edit mode (moderator row): *"Edit moderator"*.

**Backdrop** — non-closable while the nested 2FA modal is open or while saving (`no-close-on-backdrop`).

The form is rendered via `CcSettingsBox` with the following sections, top to bottom:

| Section | Notes |
|---------|-------|
| **Profile Summary** | Avatar uploader (`CcProfileSummary` slot); shows 150×150 image. **Change password** action (PATCH `/password-update/{admin_id}`). Connected social accounts (read-only, owner-row only). |
| **Two-factor authentication** | See [[settings-staff-2fa]]. |
| **Admin profile** / **Moderator profile** | Title row varies by `type`. Fields: Username (with help block *"This name is visible on your site"*), Email, First name, Last name. All required. |
| **Contacts** | Country picker, City, Street address, Postal code, Phone number. All optional, max 100 chars each. |
| **Access permissions** | Moderators only (no Permissions section on owner rows). See [[settings-staff-permissions-tree]]. |

**Footer buttons:**
- **Cancel** (closes — discards changes).
- **Save** (primary) — submits to `PATCH /admin/api/core/settings/account/admins/{id}`.

### Avatar upload

| Constraint | Value |
|---|---|
| Dimensions | 250×250 max (wider/taller rejected with *"Maximum width cannot exceed 250px."*) |
| File size | 25 KB max (see Business rules — this is **kilobytes**, not megabytes) |
| Endpoint | `POST /avatar/{admin_id}` |
| Allowed MIME types | platform's standard allowed image MIME types (`jpeg`, `png`, `gif`, `webp` — verify exact list) |
| Display | After upload, the response returns a 150×150 thumbnail URL which immediately replaces the avatar in the open Edit modal |

### Change password

Triggered from the Profile Summary slot. Endpoint: `PATCH /password-update/{admin_id}`. The endpoint enforces:

- Non-empty password.
- Non-empty `repeat_password`.
- The two values match.
- When editing yourself, the `old_password` matches your current password.

**There is no minimum length, no uppercase/digit/symbol rule, no banned-password list** enforced server-side at this endpoint. The commented-out validation in the Form Request hints at a planned 6-character minimum, but it isn't active.

## Business rules

### A non-owner cannot edit the owner

Server-side, the update endpoint rejects with **HTTP 422** *"You cannot change the owner"* if any non-owner user tries to PATCH the owner's record. Same applies to password update — returns *"You cannot change the owner password"*. The owner can edit themselves; a moderator can edit themselves (their own non-permission fields); a moderator cannot edit the owner.

### Validation field caps

The Form Request enforces:

- **Username** — required, must be unique across all admins on the platform. No length cap defined in this Request (relies on database column).
- **Email** — required, unique, must match RFC email format, **max 100 characters**.
- **First name** — **max 100 characters** if provided.
- **Last name** — **max 100 characters** if provided.
- **City / Street / Postal code / Phone** — **max 100 characters each** if provided.

All caps surface as inline form errors plus a toast.

### Avatar size cap is 25 KB, not 25 MB

The avatar upload form-request enforces `max:25` on the uploaded file — the application framework's `max` rule on file uploads is measured in **kilobytes**, not megabytes. So the practical hard limit for a staff avatar is **25 KB**, not 25 MB. The error message *"The file size should not be more than 25kb"* is correct. A merchant uploading a typical phone-camera headshot (often 2–4 MB) will be rejected unless they pre-resize and compress it down to 250×250 at a quality level that stays under 25 KB.

### Password change is gated by 2FA in some cases

Whether the Edit modal requires an additional 2FA step depends on the acting user's role and `cc2fa_secret` configuration — see [[settings-staff-2fa]] for the full matrix.

### Connected social accounts — read-only, owner-only

The owner's "Connected social accounts" section on the Edit modal is a **read-only** list of OAuth identities (Google, Facebook, etc.) that the owner previously linked to their CloudCart account. Connect/disconnect actions are not on this page — they live in the owner's personal account area (the same flow used to "Sign in with Google / Facebook" on the public login page). A moderator's row does not show this section.

### `admin_account_changes` admin notification fires on save

When the merchant saves any profile change on this modal, the `admin_account_changes` admin notification is queued via [[settings-admin-notifications]]. Delivery is asynchronous on the `admin_notify` queue task and depends on the master toggle + per-type toggle. Recipient: `site_email`.

A password update fires a **separate** `admin_account_password_change` admin notification.

### Password reset is triggered from the admin login page, not here

The `admin_account_password_reset` notification fires when an admin/moderator clicks "Forgot password" on the **admin login screen** (not from inside this Settings page). The reset flow emails a one-time code to the admin's recorded email; the admin enters it on a reset form, then sets a new password. Once the new password is saved, the `admin_account_password_change` notification ALSO fires (separately).

### Password reset code valid for 60 minutes

When a staff member clicks "Forgot password" on the admin login page, the platform emails a one-time link containing a 40-character random code. The code is valid for **60 minutes** from the moment the email is sent. Each new reset request invalidates all prior pending codes for the same admin (the platform deletes existing rows before creating a new one). After 60 minutes the link is dead and the admin must request a fresh reset email.

## Related

- [[settings-staff]] — hub.
- [[settings-staff-permissions-tree]] — Access permissions section mechanics.
- [[settings-staff-2fa]] — Two-factor authentication section.
- [[settings-admin-notifications]] — `admin_account_changes`, `admin_account_password_change`, `admin_account_password_reset` notifications.
- [[settings-general]] — `site_email` recipient for the change notifications.
- [[account-cc2fa]] — generic 2FA modal mechanics that may interrupt save.

## Open questions

- Exact allowed-image MIME extensions on the avatar endpoint — listed as "configurable file extensions" in the source; the current default list should be verified against the Form Request rule.
