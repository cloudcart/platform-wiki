---
type: concept
nav_path: "Concept → Merchant roles → Notifications + audit"
aliases: ["Admin lifecycle notifications", "new_admin_account notification", "admin_account_changes notification", "admin_account_password_change notification", "admin_account_password_reset notification", "Admin audit log", "Forgot password admin", "Password reset admin"]
tags: [access, notifications, audit, admin, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, moderator, permissions tree, API access, force sign-out + 2FA, storefront contrast).

# Merchant roles — notifications + audit

## Definition

The platform fires **four admin lifecycle email notifications** to the store email on staff create / edit / password-change / reset events, and records every admin lifecycle event in an **internal audit log** with no merchant-facing view. The merchant relies on the four emails for visibility; for richer history (who changed permission X on date Y), they contact CloudCart support.

The four notifications are governed by toggles on [[settings-admin-notifications]] and can be globally disabled or selectively suppressed:

| Notification | Fires when | Toggle on [[settings-admin-notifications]] |
|---|---|---|
| `new_admin_account` | A Moderator is created via the Create modal on [[settings-staff]]. | yes |
| `admin_account_changes` | A Moderator (or the Owner) has their profile edited (non-password fields). | yes |
| `admin_account_password_change` | A password is updated via the Edit modal's Change password action. | yes |
| `admin_account_password_reset` | A password reset is requested (initiated from the admin login page's Forgot password link). | yes |

## Scope

What this page covers:

- The four notification types, what triggers each, and where the toggles live.
- The Forgot password reset flow (initiated outside [[settings-staff]], from the admin login page).
- The internal audit log — what it captures and why there's no merchant-facing view.
- Why webhook events do NOT cover admin-account lifecycle.

Not covered here:

- The Moderator Create flow gates that fire `new_admin_account` — see [[merchant-roles-moderator]].
- The Force sign out action (Owner-only, not a notification event) — see [[merchant-roles-force-signout-2fa]].
- The general admin-notification settings UX — see [[settings-admin-notifications]].
- Webhook event names + payloads — see [[settings-hooks]].

## Contrasts

- **Email notification vs Webhook event** — admin-account events are notified by **email only**. There is NO webhook coverage for `new_admin_account`, `admin_account_changes`, etc. The webhook surface ([[settings-hooks]]) is limited to customer / order / product events. For external systems that need to react to admin changes, the merchant has no automated channel.
- **Email notification vs Audit log** — the four emails are the **only merchant-facing record** of admin lifecycle changes. The internal audit log exists but is not surfaced. Email is push (one shot at event time); the audit log is the system of record (read-only by CloudCart support).
- **Forgot password (from login page) vs Change password (from Edit modal)** — both end with a new password and fire `admin_account_password_change`. Forgot password additionally fires `admin_account_password_reset` (the "you requested" notification, separate from the "your password changed" confirmation).

## Where it applies

### The four notifications — when each fires

**`new_admin_account`** — fires the moment the Owner (or delegating Moderator) clicks Save on the Create modal in [[settings-staff]] after passing the 3-gate flow (plan-limit, 2FA challenge, server hash). Recipient: the store email. Subject and body identify the new Moderator's username and email.

**`admin_account_changes`** — fires whenever a Moderator or the Owner's profile is edited (non-password fields). Triggered by the Edit modal's Save action. Specifically covers: Profile section changes, Contacts section changes, permission grants / revokes, Avatar updates, 2FA configuration toggles.

**`admin_account_password_change`** — fires whenever a password is updated. Two trigger paths:

- The Edit modal's Change password action on [[settings-staff]].
- The completion of a Forgot password flow (after the new password is saved).

**`admin_account_password_reset`** — fires when the Forgot password flow is **initiated** from the admin login page (not from inside [[settings-staff]]). The merchant clicks Forgot password, gets a one-time code by email, enters it on a reset form, and sets a new password. The `_reset` notification fires at the **initiation** step; the `_change` notification fires at the **completion** step. Both fire separately.

### Forgot password flow — initiated from the login page

When an admin (Owner or Moderator) clicks "Forgot password" on the admin login screen:

1. They enter their email.
2. The platform emails a one-time code.
3. The admin enters the code on a reset form.
4. They set a new password.
5. Both `admin_account_password_reset` and `admin_account_password_change` notifications fire (separately).

Moderators and Owners use the **same Forgot password flow** — there's no difference in the recovery mechanism. The flow is NOT entered from [[settings-staff]]; the Staff screen's Edit modal has a separate Change password action that fires `admin_account_password_change` only.

### Notification toggles — globally or per-type

The merchant can:

- **Globally disable admin notifications** on [[settings-admin-notifications]] — none of the four fire.
- **Selectively disable specific types** — e.g., turn off `admin_account_changes` to suppress noise during a permission-tree restructure, while keeping `new_admin_account` for visibility on new accounts.

When suppressed, the notifications are dropped silently — there's no fallback channel.

### Internal audit log — exists, not surfaced

The platform records admin lifecycle events (create / edit / delete / password change / permission change) in an internal audit log. **There is no merchant-facing Audit log page in Settings to surface this** — the merchant's only direct visibility is the four email notifications.

For richer history (who changed permission X on date Y), the merchant has to contact CloudCart support, who can query the internal log on their behalf.

### Why no webhook coverage

Admin-account events do NOT fire webhook events ([[settings-hooks]] is limited to customer / order / product webhooks). Implications:

- Merchants who want to mirror admin lifecycle to an external IAM / SOC tool cannot do so via webhooks.
- The four emails are the only push channel.
- Workaround: external systems can poll the JSON-API endpoints if they need a programmatic check, but the surface is limited.

## Why this matters to the merchant

- **The four emails are the audit trail.** Without them, every admin change is invisible. Operating with admin notifications globally disabled removes the merchant's only visibility into who's changing what on the Staff screen.
- **The store email is the recipient.** If the store email is a shared inbox (e.g., `info@`), every admin reads the notifications. If it's the Owner's personal address, only they see them. Picking the right `site_email` on [[settings-general]] decides who gets visibility.
- **Password resets fire two separate emails.** That's intentional — the `_reset` notification is the "you (or someone) requested a reset" alert; the `_change` notification confirms the new password was actually set. Investigating a suspicious reset means checking for both emails.
- **No webhook coverage means external IAM tools can't auto-sync.** For merchants with compliance requirements (e.g., feeding admin lifecycle to a SOC), this is a gap — they rely on the emails (or contact support for the audit log).

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-moderator]] — Create / Edit / Delete flows that trigger the notifications.
- [[merchant-roles-owner]] — Owner profile edits trigger `admin_account_changes` too.
- [[settings-admin-notifications]] — toggles for the four admin lifecycle notifications.
- [[settings-general]] — `site_email` is the recipient.
- [[settings-staff]] — Edit modal's Change password action.
- [[settings-hooks]] — webhook events (note: admin-account events have no webhook coverage).
- [[admin-notification]] — admin-notification entity.

## Open Questions

None.
