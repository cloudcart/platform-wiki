---
type: feature
nav_path: "Settings → Staff → Edit profile"
route_name: staff.settings
route_path: /admin/settings/staff
aliases: ["Edit staff", "Edit moderator", "Edit admin", "Staff profile", "Avatar upload", "Password change"]
tags: [settings, staff, edit, profile, avatar, password]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
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
- On your own account: configure authenticator-app 2FA via a nested QR modal (see [[settings-staff-2fa]]).
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
| **Profile Summary** | Avatar uploader; shows 150×150 image. **Change password** action (PATCH `/password-update/{admin_id}`). Google account card (owner row only). |
| **Two-factor authentication** | Only on your own account. See [[settings-staff-2fa]]. |
| **Admin profile** / **Moderator profile** | Title row varies by `type`. Fields: Username (with help block *"This name is visible on your site"*), Email, First name, Last name. All required. |
| **Contacts** | Country picker, City, Street address, Postal code, Phone number. All optional, max 100 chars each. |
| **Access permissions** | Moderator rows only. The "my profile" modal from the profile menu has no such box, so a moderator cannot change their own access. See [[settings-staff-permissions-tree]]. |

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
| Display | After upload, the response returns a 150×150 thumbnail URL which immediately replaces the avatar in the open Edit modal and in the account's table row |

### Change password

Triggered from the Profile Summary slot. Endpoint: `PATCH /password-update/{admin_id}`. The endpoint enforces:

- Non-empty password.
- Non-empty `repeat_password`.
- The two values match.
- When editing yourself, the `old_password` matches your current password.


## Business rules

### The owner edits other accounts; a moderator edits their own

The owner can edit themselves and every moderator. A moderator edits their own non-permission fields. A moderator saving the owner's record gets **HTTP 422** *"You cannot change the owner"*, and the password change answers *"You cannot change the owner password"*. Saving another moderator's record is refused with *"This is a restricted area!"*.

### Validation field caps

The Form Request enforces:

- **Username** — required, must be unique across all admins on the platform. No length cap defined in this Request (relies on database column).
- **Email** — required, unique, must match RFC email format, **max 100 characters**.
- **First name** — **max 100 characters** if provided.
- **Last name** — **max 100 characters** if provided.
- **City / Street / Postal code / Phone** — **max 100 characters each** if provided.

All caps surface as inline form errors plus a toast.

### Avatar size cap is 25 KB, not 25 MB

The hard limit for a staff avatar is **25 KB**, not 25 MB. The error message *"The file size should not be more than 25kb"* is correct. A typical phone-camera headshot (often 2–4 MB) is rejected unless it is resized and compressed to 250×250 under 25 KB first.

### Password change is gated by 2FA in some cases

Whether the Edit modal requires an additional 2FA step depends on the acting user's role and an authenticator app configuration — see [[settings-staff-2fa]] for the full matrix.

### Google account card — owner row only

The owner's Edit modal shows a card for the linked Google account: its name, email and avatar with a disconnect action (confirmation *"Are you sure you want to logout?"*), or the Google sign-in button when none is linked. Connecting returns to this page through `#user-<id>`, which re-opens the account. A moderator's row does not show this card.

### Who is emailed when a profile changes

When someone saves **another person's** record and that person's email, username, first or last name changed, `admin_account_changes` goes to that person's address (the new one, if the email changed). Saving your own record sends nothing. A password set for someone else sends them `admin_account_password_change`; changing your own sends nothing. The switches on [[settings-admin-notifications]] apply.

### Changing a login email needs no code

The email here is the person's sign-in address. A change saves at once, with no confirmation code to the old or the new address. It is separate from the store email on [[settings-general]], which needs codes from both addresses, and from the account holder's email on [[merchant]]; changing one never changes the others.

### Password reset is triggered from the admin login page, not here

The `admin_account_password_reset` email is sent when an admin or moderator uses "Forgot password" on the **admin login screen**, to their own address. It carries a link to set a new password; saving the new password sends no further email.

### Password reset code valid for 60 minutes

When a staff member clicks "Forgot password" on the admin login page, the platform emails a one-time link containing a 40-character random code. The code is valid for **60 minutes** from the moment the email is sent. Each new reset request invalidates all prior pending codes for the same admin (the platform deletes existing rows before creating a new one). After 60 minutes the link is dead and the admin must request a fresh reset email.

## Related

- [[settings-staff]] — hub.
- [[settings-staff-permissions-tree]] — Access permissions section mechanics.
- [[settings-staff-2fa]] — Two-factor authentication section.
- [[settings-admin-notifications]] — `admin_account_changes`, `admin_account_password_change`, `admin_account_password_reset` notifications.
- [[settings-general]] — the store email, separate from a login email.
- [[account-cc2fa]] — generic 2FA modal mechanics that may interrupt save.

## Open questions

- Exact allowed-image MIME extensions on the avatar endpoint — listed as "configurable file extensions" in the source; the current default list should be verified against the Form Request rule.
