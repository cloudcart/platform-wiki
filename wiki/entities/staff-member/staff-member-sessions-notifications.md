---
type: entity
aliases: ["Staff member sessions", "Force sign out", "Session key rotation", "Staff lifecycle notifications", "Admin account notifications", "No audit log", "Изход на персонал"]
tags: [settings, access, staff, sessions, notifications, admin, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Staff Member — Sessions & Notifications

## Identity

This page covers the two server-side levers that end a [[staff-member|Staff Member]]'s active sessions (Force sign out + session-key rotation), the four lifecycle email notifications that fire as staff records change, and the fact that CloudCart has **no merchant-facing audit-log screen** for staff events.

> Part of [[staff-member]]. See the hub for the other aspects (roles & types, permissions, lifecycle, 2FA, profile fields).

## Aliases

- "Force sign out" — the Owner-only button in the [[settings-staff]] list header.
- "`sessionKeyGuard`" — the session-key rotation control on [[settings-general]].
- "Admin account notifications" — the four staff-lifecycle email types.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Active session** | Ended via Force sign out (Owner) or session-key rotation | A staff member can be forced out of the admin panel; customer sessions are untouched. |
| **Lifecycle notifications** | Toggled on [[settings-admin-notifications]] | Four event types, each suppressible. |

## Where it appears

- [[settings-staff]] — the Owner-only **Force sign out** button in the list header.
- [[settings-general]] — `sessionKeyGuard` rotation + the `site_email` that receives admin-creation notifications.
- [[settings-admin-notifications]] — the master toggle + per-type toggles for the four notifications.
- [[admin-notification]] — the entity behind the queued lifecycle emails.

## Business rules

### Force sign-out is Owner-only and wipes admin sessions only

The **Force sign out** button in the Staff list header is visible only when `user.is_owner = true`. On confirm, the server deletes every admin session record (every row where `admin_id` is not null) from the store's session table, logs out the CC2FA layer, and the front-end reloads after 500 ms — so the Owner lands on the login screen too. Customer sessions (no `admin_id`) are NOT touched.

This is a separate mechanism from the `sessionKeyGuard` rotation in [[settings-general]]: **rotation invalidates sessions passively** (cookies stop being recognized); **Force sign out actively wipes records**. Either path logs every admin out; only Force sign out is exposed as a one-click button and only to the Owner.

### Lifecycle email notifications

Each lifecycle event queues an admin notification on the `admin_notify` queue (delivery depends on the master toggle + per-type toggle in [[settings-admin-notifications]]):

| Event | Notification key |
|-------|------------------|
| Moderator created via Add modal | `new_admin_account` |
| Moderator / Owner profile edited | `admin_account_changes` |
| Password updated via Edit modal | `admin_account_password_change` |
| Password reset requested (from the admin login page's "Forgot password") | `admin_account_password_reset` |

If `administrator_email_notifications` (the master toggle) is off OR the specific per-type toggle is off, the notification is suppressed silently. The intended readers are the staff members, but the actual recipient is the store's single `site_email` from [[settings-general]] — see [[admin-notification]].

### No merchant-facing audit log for staff lifecycle

The platform records staff lifecycle events internally but **does not expose a merchant-facing audit-log screen**. Visibility of staff lifecycle events relies on the four email notifications above. For richer audit history, the merchant must rely on inbox records or contact CloudCart support.

## Related

- [[staff-member]] — hub.
- [[settings-staff]] — the Force sign out button.
- [[settings-general]] — `sessionKeyGuard` rotation + `site_email`.
- [[settings-admin-notifications]] — the four notification types + toggles.
- [[admin-notification]] — the notification entity.

## Open Questions

None.
