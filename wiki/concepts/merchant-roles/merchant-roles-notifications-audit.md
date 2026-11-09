---
type: concept
nav_path: "Concept → Merchant roles → Notifications + audit"
aliases: ["Admin lifecycle notifications", "new_admin_account notification", "admin_account_changes notification", "admin_account_password_change notification", "admin_account_password_reset notification", "Admin audit log", "Forgot password admin", "Password reset admin"]
tags: [access, notifications, audit, admin, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, moderator, permissions tree, API access, force sign-out + 2FA, storefront contrast).

# Merchant roles — notifications + audit

## Definition

The platform sends **four admin lifecycle emails** on staff create / edit / password-change / reset events, each to **the staff member's own address**, not the store email. It keeps **no log of staff changes**: creating, editing, re-permissioning or deleting an account is recorded nowhere the merchant or support can read; the store's event log holds staff sign-ins only.

The four notifications are governed by toggles on [[settings-admin-notifications]] and can be globally disabled or selectively suppressed:

| Notification | Fires when | Toggle on [[settings-admin-notifications]] |
|---|---|---|
| `new_admin_account` | A Moderator is created via the Create modal on [[settings-staff]]. | yes |
| `admin_account_changes` | Someone else changed this person's email, username, first or last name. | yes |
| `admin_account_password_change` | Someone else set this person's password on the Edit modal. | yes |
| `admin_account_password_reset` | A password reset is requested (initiated from the admin login page's Forgot password link). | yes |

## Scope

What this page covers:

- The four notification types, what triggers each, and where the toggles live.
- The Forgot password reset flow (initiated outside [[settings-staff]], from the admin login page).
- That no log of staff changes exists.
- Why webhook events do NOT cover admin-account lifecycle.

Not covered here:

- The Moderator Create flow gates that fire `new_admin_account` — see [[merchant-roles-moderator]].
- The Force sign out action (Owner-only, not a notification event) — see [[merchant-roles-force-signout-2fa]].
- The general admin-notification settings UX — see [[settings-admin-notifications]].
- Webhook event names + payloads — see [[settings-hooks]].

## Contrasts

- **Email notification vs Webhook event** — admin-account events are notified by **email only**. There is NO webhook coverage for `new_admin_account`, `admin_account_changes`, etc. The webhook surface ([[settings-hooks]]) is limited to customer / order / product events. For external systems that need to react to admin changes, the merchant has no automated channel.
- **Email notification vs log** — the four emails are the **only record** of staff changes, and they go to the person changed, not the owner. No staff-change log stands behind them.
- **Forgot password (from login page) vs Change password (from Edit modal)** — Forgot password sends `admin_account_password_reset` with a link and nothing once the new password is saved; Change password sends `admin_account_password_change` only when someone else's password is set.

## Where it applies

### The four notifications — when each fires

**`new_admin_account`** — fires the moment the Owner clicks Save on the Create modal in [[settings-staff]] after passing the 3-gate flow (plan-limit, 2FA challenge, server hash). Recipient: the new Moderator's own address. Subject and body identify their username and email.

**`admin_account_changes`** — sent when someone saves another person's record and that person's email, username, first or last name changed, to that person's (new) address. Contacts, permissions, avatar and 2FA changes, and edits to your own record, send nothing.

**`admin_account_password_change`** — sent when someone sets another person's password with Change password on [[settings-staff]]. Changing your own password, or finishing Forgot password, sends nothing.

**`admin_account_password_reset`** — sent when Forgot password is used on the admin login page. It carries a link to set a new password, valid 60 minutes.

### Forgot password flow — initiated from the login page

When an admin (Owner or Moderator) clicks "Forgot password" on the admin login screen:

1. They enter their email.
2. The platform emails a link (the `admin_account_password_reset` email), valid 60 minutes.
3. The link opens a form to set a new password.
4. Saving it signs them in; no further email is sent.

Moderators and Owners use the **same Forgot password flow** — there's no difference in the recovery mechanism. The flow is NOT entered from [[settings-staff]]; the Staff screen's Edit modal has a separate Change password action that fires `admin_account_password_change` only.

### Notification toggles — globally or per-type

The merchant can:

- **Globally disable admin notifications** on [[settings-admin-notifications]] — none of the four fire.
- **Selectively disable specific types** — e.g., turn off `admin_account_changes` to suppress noise during a permission-tree restructure, while keeping `new_admin_account` for visibility on new accounts.

When suppressed, the notifications are dropped silently — there's no fallback channel.

### No log of staff changes

Nothing records who created, edited, re-permissioned or deleted a staff account: there is no log page, and the store's event log holds staff sign-ins only. The four emails above are the only trace, and only for the changes they cover.

### Why no webhook coverage

Admin-account events do NOT fire webhook events ([[settings-hooks]] is limited to customer / order / product webhooks). Implications:

- Merchants who want to mirror admin lifecycle to an external IAM / SOC tool cannot do so via webhooks.
- The four emails are the only push channel.
- Workaround: external systems can poll the JSON-API endpoints if they need a programmatic check, but the surface is limited.

## Why this matters to the merchant

- **The four emails are the audit trail.** Without them, every admin change is invisible. Operating with admin notifications globally disabled removes the merchant's only visibility into who's changing what on the Staff screen.
- **The person changed is the recipient.** The owner is not copied, so an owner learns of a change only when it was made to their own account.
- **A password reset sends one email**, the link, to the person's own inbox.
- **No webhook coverage means external IAM tools can't auto-sync.** For merchants with compliance requirements (e.g., feeding admin lifecycle to a SOC), this is a gap — they rely on the emails.

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-moderator]] — Create / Edit / Delete flows that trigger the notifications.
- [[merchant-roles-owner]] — Owner profile edits trigger `admin_account_changes` too.
- [[settings-admin-notifications]] — toggles for the four admin lifecycle notifications.
- [[settings-general]] — the store email, which these emails do not use.
- [[settings-staff]] — Edit modal's Change password action.
- [[settings-hooks]] — webhook events (note: admin-account events have no webhook coverage).
- [[admin-notification]] — admin-notification entity.

## Open Questions

None.
