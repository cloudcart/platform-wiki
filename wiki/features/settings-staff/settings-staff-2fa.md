---
type: feature
nav_path: "Settings → Staff → Two-factor authentication"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Staff 2FA", "Two-factor authentication", "Authenticator app", "QR setup", "TOTP", "Email 2FA", "cc2fa_secret"]
tags: [settings, staff, 2fa, security, authenticator]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, create, edit, permissions, delete, force sign out).

# Staff — two-factor authentication

## Purpose

Documents the **Two-factor authentication** section on the Edit modal: the always-on email channel (status indicator, not a toggle), the configurable authenticator-app channel (TOTP via QR code), the nested QR Setup modal, and the "is 2FA required for this edit?" gating helper that decides whether saving a staff change pops a verification challenge.

## Where to find it

Sidebar → Settings → **Staff** → click any row → **Two-factor authentication** section on the Edit modal (second section, below Profile Summary).

This section is **Edit-only** — it does not appear in the Create modal.

## What the merchant can do here

- See whether email-based 2FA is active for this staff member (it always is — permanent indicator).
- Open the QR Setup modal via **Configure** to enable authenticator-app TOTP for this staff member.
- Scan the QR with Google Authenticator / Authy / 1Password / etc., enter the 6-digit confirmation code, and persist `cc2fa_secret`.

## Settings & fields

### Two-factor authentication section (Edit modal)

| Row | Content | Type |
|-----|---------|------|
| **Email two factor authentication is active** | Permanent indicator with a green check badge | Status indicator (not a toggle) |
| **Use authenticator app for faster login** | Laptop-mobile icon + **Configure** button | Action — opens nested QR Setup modal |

### QR Setup nested modal

Opened by the **Configure** button. Implementation: a `b-modal` nested inside the Edit modal, size `xl`, no footer.

| Element | Content |
|---------|---------|
| **Title** | *"Two-factor authentication"* |
| **Body** | A `QrSetup` component (shared) — displays a QR code generated server-side; the merchant scans it with Google Authenticator / Authy / 1Password / etc. and enters the 6-digit confirmation code. On verify, the secret is persisted as `cc2fa_secret` and the merchant gets a success toast: *"Two-factor authentication setup completed"*. |
| **Close** | Standard X / Cancel — discards if not yet verified. |

This modal is OPENED from within the Edit modal. When open, the parent Edit modal's backdrop is locked (`no-close-on-backdrop`).

## Business rules

### Email channel is always active for every staff member

Every staff member receives a `two_factor_action` email automatically when a 2FA-protected action requires verification. This email channel is **permanent** — the "Email two factor authentication is active" row on the Edit modal is a **status indicator, not a toggle**. There is no per-row UI to disable email 2FA.

**But it stops being used once the authenticator app is configured.** The platform only generates and sends an email code for a staff member who has **no** authenticator secret; with one configured, no email is produced at all and the app's code is what satisfies the challenge. The two channels do not run side by side — see [[account-cc2fa-email]].

### Authenticator-app 2FA is configurable per row

The configurable bit is the **authenticator-app 2FA** (`cc2fa_secret`):

1. The staff member opens the Edit modal for their own row.
2. Clicks **Configure** on the "Use authenticator app for faster login" row.
3. Scans the QR in their authenticator app.
4. Enters the 6-digit confirmation code.
5. The secret is persisted as `cc2fa_secret` on the staff record.

From then on, the user can use the app for faster 2FA (no email round-trip).

### "Is 2FA required for this edit?" gating helper

The platform's "is 2FA required?" helper decides whether an extra 2FA step is required when editing a given staff record. The matrix:

| Acting user | Editing | Has fresh `cc2fa_verify` flag | Has `cc2fa_secret` configured | 2FA required? |
|---|---|---|---|---|
| Anyone | Anyone | Yes | — | No (flag consumed) |
| User X | User X (themselves) | No | Yes | **Yes** |
| User X | User X (themselves) | No | No | No |
| Owner | Someone else | No | — | No |
| Non-owner | Someone else | No | Yes | **Yes** |
| Non-owner | Someone else | No | No | No |

In plain language:

- **Fresh 2FA flag in session** → skip this time (the flag is consumed).
- **Editing yourself** → 2FA only if you personally have an authenticator-app secret configured (the app-based 2FA is the trigger for self-edit gating).
- **Owner editing someone else** → no 2FA (owner is trusted for routine maintenance).
- **Non-owner editing someone else** → 2FA required if that non-owner has an authenticator-app secret configured (forces extra verification for moderators acting on each other).

This pattern keeps the owner unblocked for routine maintenance while forcing extra verification for moderators acting on other staff.

### Create flow always requires 2FA — separate gate

Note that creating a new moderator is **always** 2FA-gated regardless of the above matrix — the gate is `create_moderator` 2FA action on the [[settings-staff-create-moderator]] Add button, not the edit-gating helper. The gate is enforced both client-side (the Add button opens the 2FA modal) and server-side (the create endpoint requires a valid one-time hash).

### Force sign out is owner-only and uses a different mechanism

The **Force sign out** button on the page header is owner-only and wipes admin sessions server-side — it is NOT 2FA-gated by this helper, but does require owner privileges. See [[settings-staff-force-signout]].

### `cc2fa_secret` is per-staff, not per-store

Each staff member configures their own authenticator-app secret independently. A moderator with `cc2fa_secret` configured will be prompted for the 6-digit code; one without it will get the email channel instead. Disabling/removing `cc2fa_secret` reverts the staff member to the email channel only.

### Verification code character lengths

| Channel | Code length |
|---|---|
| Authenticator app (TOTP) | 6 digits |
| Email channel | 6 digits |

## Related

- [[settings-staff]] — hub.
- [[settings-staff-create-moderator]] — the `create_moderator` 2FA gate at moderator creation.
- [[settings-staff-edit-profile]] — where the 2FA section appears.
- [[account-cc2fa]] — generic Cc2FaAction modal mechanics and the `cc2fa_verify` session flag.
- [[settings-admin-notifications]] — `two_factor_action` email is emitted by the admin-notification system when email-channel verification is required.

## Open questions

None.
