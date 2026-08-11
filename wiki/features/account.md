---
type: feature
nav_path: "Admin profile"
route_name: account
route_path: /admin/account
aliases: ["Admin profile", "Account", "Профил на администратора", "Профил"]
tags: [account, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 6
---
# Admin profile

## Purpose

Hub for everything tied to **the currently signed-in admin's personal account**. From here the merchant can:

- Edit their **profile** (name, email, avatar, address, phone).
- **Change their password** (modal accessed via the profile screen).
- Enable / configure **two-factor authentication** (TOTP via [[account-cc2fa]]) and its **backup codes** ([[account-cc2fa-codes]]) and the **email-2FA fallback** ([[account-cc2fa-email]]).
- **Connect / disconnect social accounts** (Google, Facebook).
- See the store's **disk-storage usage** progress bar (shared with [[settings-files]]).
- For the **store owner** editing another admin: assign the moderator's `type` (predefined role) and tweak per-area `permissions[]` checkboxes — this is where staff RBAC is wired.

It is the entry point the profile dropdown lands on (top-right user menu) and the `Admin profile` sidebar group.

## Where to find it

- **Top-right user menu (profile dropdown) → Admin profile** OR sidebar `sidebar.account` group.
- The own-profile page lives at `/admin/account/profile` (route `admin.account.profile`).
- The store owner editing another staff member opens `/admin/account/profile/{admin_id}` from the [[settings-staff]] list.

Breadcrumb on the profile page reads `Admin profile → Profile`. From the *Profile* page the merchant clicks **Change your password** (top-right) to open the password modal, or **Two-factor authentication → Configure** to land on [[account-cc2fa]].

## What the merchant can do here

### Edit own profile (self)

The own-account `/admin/account/profile` page is built from the Smarty template `protected/templates/sitecp/account/profile.tpl`. Visible sections, in order:

#### Header strip

- **Avatar circle** (150×150) — clicking opens the OS file picker; uploads to `POST /admin/account/profile/change-avatar/{admin_id}` (route `admin.account.change-avatar`). On success the topbar avatar refreshes too.
- **Display name** — concatenated `first_name` + `last_name` if either is set; falls back to `username` then `email`.
- **Change your password** button → opens the password-change modal (see below).
- **Save** button → submits the profile form with a confirmation dialog (*"Are you sure you want to save changes?"*).
- **Storage progress bar** — green bar at the top showing `used / total` from the store's disk quota; matches the indicator on [[settings-files]].
- **Hire an expert** (owner-only) — direct link to [[services]] for purchasing CloudCart professional services.

#### Connect social accounts

Two cards: **Google** and **Facebook**. Each one shows:

- If NOT connected: a `Connect with Google` / `Connect with Facebook` button → GET `/admin/account/profile/connect/{provider}` (route `admin.account.connect`).
- If connected: shows the linked account's avatar + name + email; clicking the card disconnects via GET `/admin/account/profile/disconnect/{provider}` (route `admin.account.disconnect`).

#### Two-factor authentication block

Status indicators inline on the profile:

- **Email 2FA** row — visible only when platform-level `2fa_email` functionality is ON AND the admin has NOT set up authenticator 2FA. Shows a green checkmark when active.
- **Authenticator-app 2FA** row — always visible. Shows a green checkmark if `cc2fa_secret` is set; provides a **Configure** button → [[account-cc2fa]].

#### Name section

| Field | Input | Validation |
|---|---|---|
| Username | text, required, autofocus | required |
| Email | email, required | required, valid email format, unique across admins |
| First name | text | (not required) |
| Last name | text | (not required) |

#### Address section

| Field | Input | Notes |
|---|---|---|
| Country | select2 dropdown of all countries (localized name shown in parens) | defaults to store's `setting('country')` if blank |
| City | text | defaults to `setting('site_city')` if blank |
| Street | text | optional |
| Postal code | text | optional |
| Phone | tel with intl-tel-input (auto-detects ISO2 from country) | optional; validated by `js-phone-intl` format |

#### Settings & Permissions (owner editing OTHER admin only)

These two sections render only when `self.type == 'owner' AND admin_id != site_owner.id`:

- **Moderator type** — select dropdown of the predefined admin types (excluding `owner`). Help text from `account.help.moderator_type`.
- **Permissions checkboxes** — a nested checkbox tree of every permission section (from `App\Helper\SiteCp\Settings\Config::$sections`). Each parent has children grouped under it; toggling a parent affects children via `class="parent-{id}"`.

### Change password (modal)

Triggered by the **Change your password** button. Loads `protected/templates/sitecp/account/change_password.tpl` via `GET /admin/account/profile/change-pass/{admin_id}` (route `admin.account.change-pass`).

If the platform requires 2FA (`isRequiredCC2FA($admin) == true`), the modal first asks for a 2FA OTP code before showing the password form — uses the platform code view.

Fields in the password modal (when not blocked by 2FA):

| Field | Visible when | Validation |
|---|---|---|
| New password | always | required |
| Old password | editing OWN account AND existing password is NOT empty | required |
| Repeat new password | always | must match `password` |

On submit → `POST /admin/account/profile/change-pass/{admin_id}` → toast `account.succ.password_changed`.

### Upload / change avatar

`POST /admin/account/profile/change-avatar/{admin_id}` (multipart). On success, the topbar avatar refreshes via FileReader + dataURL injection (no page reload). The same file can't be uploaded twice in a row — the form caches the input value and toasts *"Same file chosen"* if the merchant retries.

### Disconnect social account

Click the connected Google/Facebook card → opens `/admin/account/profile/disconnect/{provider}` which removes the `SocialAccount` row and redirects back to `/admin/account/profile`.

## Settings & fields

See per-section table above. All fields submit together via `POST /admin/account/profile/{admin_id}` (handled by the request handler).

## Business rules

### `@deprecated` controller, still in production

The PHP class the platform code carries an `@deprecated` annotation but it is **the live controller** — no replacement has been wired. The Smarty template is still rendered for all profile edits. Treat the page as actively supported.

### Owner can edit any admin; staff can edit only themselves

The page resolves `admin_id` to the platform code if missing — so non-owner staff always edit their own row. Owners pass an `{admin_id}` URL segment to edit a different staff member; the route's `{admin_id?}` is optional.

### Permissions tree is the same one used in Settings → Staff

The permissions checkbox tree is rendered from `App\Helper\SiteCp\Settings\Config::$sections` — exactly the source [[settings-staff]] uses. Both screens write to the `admins.permissions` JSON column.

### Storage progress bar reflects S3 bucket usage

The `storage` data variable is populated by the platform code — the same call that drives the [[settings-files]] quota gauge. When this profile is opened, the bar shows current bucket usage in real time.

### 2FA-required-for-password-change is platform-level

When the platform-level `2fa_email` is ON OR the admin already has `cc2fa_secret`, the change-password modal first prompts for the OTP. This is enforced via `isRequiredCC2FA` in the platform code.

### Address fields are stored separately

The address fields (country, city, street, postal_code, phone, first_name, last_name) live on `admin_infos` (one-to-one to `admins`), NOT on the admin row itself. The `addressInfo` is upserted on save.

## Related

- [[account-cc2fa]] — TOTP authenticator setup.
- [[account-cc2fa-codes]] — backup codes.
- [[account-cc2fa-email]] — email-2FA fallback.
- [[settings-staff]] — staff list (owner adds / removes admins).
- [[settings-files]] — storage usage breakdown.
- [[services]] — Hire an expert link.
- [[merchant]] — platform-level account-holder / billing identity that owns the store(s).

## Open questions

(none — verified against controllers + Smarty templates.)
