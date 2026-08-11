---
type: feature
nav_path: "Settings → Staff → Delete moderator"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Delete moderator", "Remove staff", "Staff delete", "CcDeleteComponent"]
tags: [settings, staff, delete, security]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, create, edit, permissions, 2FA, force sign out).

# Staff — delete moderator

## Purpose

Documents the per-row delete affordance on the staff list table: the inline confirm popover, the per-row visibility rules (the owner row never shows the button; users cannot delete themselves), the server-side guard, and the absence of soft-delete / audit-log persistence.

## Where to find it

Sidebar → Settings → **Staff** → table row → trash icon in the **Actions** column. The icon is **hidden** for rows that the acting user is not allowed to delete (see Visibility rules).

## What the merchant can do here

- Click the trash icon on a moderator's row to open the inline confirm popover.
- Confirm to hard-delete the moderator.
- Cancel to dismiss without action.

## Settings & fields

### Delete confirm — inline popover

Triggered by the trash icon on a moderator's row in the table. It uses the platform's shared delete-confirm popover.

| Element | Content |
|---------|---------|
| **Label** | *"Delete moderator?"* (default delete-component label). |
| **Confirm** | *"Delete"* (danger). |
| **Cancel** | Closes — no action. |

On confirm, the row is submitted to `DELETE /admin/api/core/settings/account/admins/{id}`.

### Per-row visibility rules — button is HIDDEN when any of these are true

- Row's `type_code === 'owner'` (the owner row never shows a delete button).
- The acting user is **not** the owner **AND** row id is the acting user's own id (users cannot delete themselves through this UI — regardless of role).

The button is **shown** only when: row is not the owner AND (acting user is the owner OR row id !== acting user id). The visibility check is more permissive than "owner-only" might suggest: a moderator CAN see the delete button on another moderator's row, but the server-side permissions check will reject the actual DELETE call unless the moderator holds `settings.admins.all` or equivalent (see [[settings-staff-permissions-tree]]).

## Business rules

### Server-side guard against deleting the owner

The DELETE endpoint blocks any row with `type='owner'` and returns **HTTP 422** *"You cannot delete the owner."* This is independent of the UI visibility rule — even a forged request bypassing the UI cannot delete the owner row.

### Users cannot delete themselves

The UI hides the delete button on the acting user's own row. The server does not appear to have a symmetric self-delete guard documented, but the UI affordance is absent, so this is enforced at the client layer for current flows. (verify — server-side self-delete behaviour)

### Permissions middleware applies

Even if the trash icon is visible (because the acting user is the owner OR the row is not the acting user's own), the DELETE call is gated by the staff-management permission (`settings`, `settings.admins.all`, or `store.admins`). A moderator without those permissions cannot DELETE another moderator's row regardless of UI affordance.

### Hard delete — no soft delete, no audit row

Deleting a moderator is a **hard delete** — the moderator's permissions and any audit-log connections drop with them. The platform has an internal admin-activity logging store, but the logging mechanism currently **never starts** — its initialisation exits before any change-tracking is wired up. So **no audit rows are written** at present. (verify — the admin-logging initialisation still exits early)

Practical implication: once a moderator is deleted, the merchant has no in-platform record that they ever existed beyond the admin-notification emails that fired during their lifecycle (`new_admin_account`, `admin_account_changes`, `admin_account_password_change`).

### No admin notification fires on delete

Unlike create / edit / password-change events, **deleting a moderator does NOT fire an admin notification** — there is no `admin_account_deleted` notification type in [[settings-admin-notifications]]. The four lifecycle notifications cover create / edit / password-change / password-reset; delete is silent. (verify)

### Plan-seat count decreases on delete

After a successful delete, the current `administrators` plan-feature usage count drops by 1. If the merchant was over-quota (e.g., after a plan downgrade), deleting enough moderators to fall back under the cap re-enables the **Add moderator** button. See [[settings-staff-create-moderator]] for the plan-gating logic.

### Sessions belonging to the deleted moderator

Deleting a moderator does **not** appear to automatically wipe their active admin sessions — the moderator's account is hard-deleted, but their stored login sessions remain until they expire naturally. For an immediate forced sign-out of a specific moderator about to be deleted, the owner should use **Force sign out** [[settings-staff-force-signout]] first (which wipes ALL admin sessions, not just the target's) or wait for the session to expire. (verify — whether per-row delete cascades to session cleanup)

## Related

- [[settings-staff]] — hub.
- [[settings-staff-roles-list]] — the table where the delete button appears.
- [[settings-staff-permissions-tree]] — `settings.admins.all` permission gates the DELETE endpoint.
- [[settings-staff-force-signout]] — owner-only mass-logout for ensuring a deleted moderator's session is also wiped.
- [[settings-admin-notifications]] — the 4 staff notifications (none fires on delete).

## Open questions

- Does the server enforce the self-delete rule (i.e., reject if `acting_user_id == row_id`), or is it purely UI? (verify)
- Does deleting a moderator wipe their stored login sessions automatically, or does the session persist until natural expiry? (verify)
- Is there any `admin_account_deleted` notification in flight, or is delete intentionally silent? (verify)
