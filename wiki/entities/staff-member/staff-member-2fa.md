---
type: entity
aliases: ["Staff member 2FA", "Two-factor authentication", "Authenticator app", "cc2fa_secret", "Email two factor", "2FA gating", "Двуфакторна автентикация на персонал"]
tags: [settings, access, staff, permissions, admin, 2fa, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Staff Member — Two-Factor Authentication

## Identity

Every [[staff-member|Staff Member]] has two-factor protection on sensitive actions. There are two channels:

- **Email channel** — always on for every staff member, cannot be turned off. CloudCart sends `two_factor_action` codes to the staff member's email whenever a sensitive action requires verification.
- **Authenticator-app channel** (`cc2fa_secret`) — opt-in per account. Once a TOTP secret is configured, future 2FA gates prefer the authenticator code over the email code.

> Part of [[staff-member]]. See the hub for the other aspects (roles & types, permissions, lifecycle, sessions & notifications, profile fields).

## Aliases

- "Email two factor authentication" — the always-on email-code channel; the Edit modal shows the permanent indicator *"Email two factor authentication is active"*.
- "Authenticator app" / `cc2fa_secret` — the opt-in TOTP channel.
- "`two_factor_action`" — the notification key for the emailed verification code.
- "`create_moderator`" — the 2FA action name for the Add-moderator gate.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **2FA email channel** | Always on; cannot be disabled | Fires `two_factor_action` emails per [[settings-admin-notifications]] when sensitive actions require verification. |
| **2FA authenticator secret** (`cc2fa_secret`) | Opt-in per account via the Edit modal's "Use authenticator app for faster login" | Optional. Scan the QR with Google Authenticator / Authy / 1Password / etc. to enable TOTP. |

## Where it appears

- [[settings-staff]] — the Edit modal shows the email-2FA indicator and the authenticator-app **Configure** option.
- [[account-cc2fa]] — the per-account TOTP secret setup screen.
- [[account-cc2fa-email]] — email-channel 2FA settings.
- [[account-cc2fa-codes]] — recovery codes for 2FA fallback.

## Business rules

### Email is always on, authenticator app is opt-in per account

Every Staff Member implicitly has the email-based 2FA channel enabled. The authenticator-app TOTP channel is opt-in per account: the staff member opens their own Edit modal, clicks **Configure** under "Use authenticator app for faster login," and scans the QR with their authenticator app. Once the secret is saved, future 2FA gates prefer the authenticator code over the email code. Recovery codes for the TOTP secret are managed on [[account-cc2fa-codes]].

### Two-factor gating on edit varies by actor and target

The platform's "is 2FA required?" helper decides whether an extra 2FA step is required when editing a given staff record:

| Actor vs target | 2FA required? |
|-----------------|---------------|
| Fresh `cc2fa_verify` session flag present | No (the step is consumed and skipped) |
| Editing yourself | Only if you have an authenticator-app secret (`cc2fa_secret`) configured |
| Owner editing someone else | No |
| Non-Owner editing someone else | Yes — IF they personally have a `cc2fa_secret` configured |

This pattern keeps the Owner unblocked for routine maintenance while forcing extra verification for Moderators acting on each other.

### Adding a Moderator passes a `create_moderator` 2FA challenge

The **+ Add moderator** flow opens a 2FA action modal with action `create_moderator`; the actor completes it (email code or authenticator code) before a one-time hash is issued and validated server-side. See [[staff-member-lifecycle]] for the full three-check sequence.

### Authenticator-app reset path

When a staff member loses their authenticator device:

1. Sign in with backup codes from [[account-cc2fa-codes]].
2. Revisit [[account-cc2fa]] to remove the current secret.
3. Reconfigure with the new device.

If the staff member has lost **both** the device AND the backup codes, the only path is to contact CloudCart support for a manual reset.

## Related

- [[staff-member]] — hub.
- [[account-cc2fa]] — per-account TOTP secret setup.
- [[account-cc2fa-email]] — email-channel 2FA settings.
- [[account-cc2fa-codes]] — recovery codes for fallback.
- [[settings-staff]] — the Edit modal exposing both channels.
- [[settings-admin-notifications]] — `two_factor_action` email gating.

## Open Questions

None.
