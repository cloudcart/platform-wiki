---
type: feature
nav_path: "Settings → Staff → Delete moderator"
route_name: staff.settings
route_path: /admin/settings/staff
aliases: ["Delete moderator", "Remove staff", "Staff delete", "CcDeleteComponent"]
tags: [settings, staff, delete, security]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-11-03
source_count: 2
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, create, edit, permissions, 2FA, force sign out).

# Staff — delete moderator

## Purpose

Documents the per-row delete affordance on the staff list table: the inline confirm popover, who sees the button (the owner, on moderator rows), the server-side guard, and the absence of soft-delete / audit-log persistence.

## Where to find it

Sidebar → Settings → **Staff** → table row → trash icon in the **Actions** column. The icon is **hidden** for rows the acting user cannot delete (see Who sees the button).

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

### Who sees the button

The trash icon shows to the **store owner**, on every moderator's row. The owner's own row never has one, and a moderator sees none on any row.

After a successful delete the toast reads *"Deleted successfully"* and the row leaves the table without a reload.

## Business rules

### Server-side guard against deleting the owner

The DELETE endpoint blocks any row with `type='owner'` and returns **HTTP 422** *"You cannot delete the owner."* The owner row cannot be deleted.

### Hard delete

Deleting a moderator is a **hard delete**: the account and its permissions are removed and it cannot be restored. What stays is the admin-notification emails sent during the account's lifecycle (`new_admin_account`, `admin_account_changes`, `admin_account_password_change`).

### No admin notification fires on delete

Unlike create / edit / password-change events, **deleting a moderator does NOT fire an admin notification** — there is no `admin_account_deleted` notification type in [[settings-admin-notifications]]. The four lifecycle notifications cover create / edit / password-change / password-reset; delete is silent. (verify)

### Plan-seat count decreases on delete

After a successful delete, the current `administrators` plan-feature usage count drops by 1. If the merchant was over-quota (e.g., after a plan downgrade), deleting enough moderators to fall back under the cap lets **Add moderator** start the create flow again. See [[settings-staff-create-moderator]] for the plan-gating logic.

### Signing a moderator out first

To end a moderator's sign-in right away, use **Force sign out** ([[settings-staff-force-signout]]) before deleting the account. It ends all admin sessions, not just theirs.

## Related

- [[settings-staff]] — hub.
- [[settings-staff-roles-list]] — the table where the delete button appears.
- [[settings-staff-permissions-tree]] — the staff section of the permissions tree.
- [[settings-staff-force-signout]] — owner-only mass-logout for ensuring a deleted moderator's session is also wiped.
- [[settings-admin-notifications]] — the 4 staff notifications (none fires on delete).
- [[mobile-admin-app-account-deletion]] — a Moderator CAN delete their own account, but only from the CloudCart Admin mobile app.

## Open questions

- Does deleting a moderator wipe their stored login sessions automatically, or does the session persist until natural expiry? (verify)
- Is there any `admin_account_deleted` notification in flight, or is delete intentionally silent? (verify)
