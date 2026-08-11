---
type: feature
nav_path: "Settings → Staff → Force sign out"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Force sign out", "Mass logout", "Sign out everyone", "logoutAll", "Admin session wipe"]
tags: [settings, staff, security, sessions, owner-only]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, create, edit, permissions, 2FA, delete).

# Staff — force sign out

## Purpose

Documents the owner-only **Force sign out** button on the page header: a single-click mass logout that invalidates every admin and moderator session record in the store. Useful after a suspected credential compromise, a moderator leaving the company, or routine security rotation. Also documents how this differs from the `sessionKeyGuard` rotation on [[settings-general]].

## Where to find it

Sidebar → Settings → **Staff** → page header → red **Force sign out** button (next to **Add moderator**).

**Visibility:** The button only appears when `user.is_owner === true`. Moderators do not see it.

## What the merchant can do here

- (Owner only) Click **Force sign out** to open the confirm modal.
- Confirm to invalidate every admin/moderator session record in the store.
- Cancel to dismiss without action.

## Settings & fields

### Force sign out button (page header)

| Control | Visible to | What it does |
|---------|------------|--------------|
| **Force sign out** (red Danger button) | Only when `user.is_owner` is true | Opens a confirm dialog. On confirm, deletes every admin session record from the store's session store, logs out the CC2FA session, and force-reloads the page — which signs the owner out too. |

### Confirm modal

This is the platform's standard confirm dialog.

| Element | Content |
|---------|---------|
| **Title** | *"Are you sure?"* |
| **Message** | *"This action will sign out every moderator and/or administrator who is currently logged in."* |
| **Confirm button** | *"Yes, I am sure"* (danger). |
| **Cancel button** | *"Cancel"*. |
| **Loader** | Spinner while the sign-out-everyone request runs. |

### Endpoint

`GET /admin/api/core/settings/account/admins/logout-all` (note: GET, not POST — verify).

## Business rules

### On confirm — exact sequence

1. Triggers the sign-out-everyone action — deletes all admin session records from the store's session store (every record tied to a staff account).
2. Logs the CC2FA session out.
3. Shows toast: *"All moderators have been signed out"*.
4. After **500ms** delay, force-reloads the page — the owner lands on the login screen (along with everyone else).

The 500ms delay exists to give the toast notification time to render before the page reloads.

### The acting owner is signed out too

There is no "stay signed in as owner" option. The wipe deletes every admin session — including the owner's. The reload ensures the owner lands on the login screen along with everyone else and must sign in fresh (re-establishing 2FA if applicable).

### Customer sessions are untouched

The wipe targets only session records tied to a staff account. Customer sessions (storefront shoppers, which aren't linked to any staff account) are not touched. The storefront continues to operate normally for customers during and after the wipe.

### Owner-only — both client and server

The button only renders when `user.is_owner === true`. The endpoint at `/admin/api/core/settings/account/admins/logout-all` is gated by the same staff-management permission (`settings`, `settings.admins.all`, or `store.admins`) as the rest of the staff API; in practice, only the owner has the right combination of permissions to reach it. (verify — whether the endpoint additionally enforces `is_owner` server-side or relies on the standard permission gate)

### When to use this vs `sessionKeyGuard` rotation

This is a **separate mechanism** from the `sessionKeyGuard` rotation in [[settings-general]] (Security box). Both achieve the same end-result for admin sessions, but they differ in mechanics:

| Mechanism | What it does | Tradeoff |
|---|---|---|
| **Force sign out** (this button) | Actively **deletes** the admin session records server-side. Sessions are immediately invalidated; next request returns 401. | Audit-friendly (session records are gone), one-click, owner only. |
| **`sessionKeyGuard` rotation** ([[settings-general]]) | Changes the cookie name pattern. Cookies stay valid until they expire on the client; the server simply stops recognising them. | Less aggressive — sessions don't survive a refresh, but the stored session records remain until natural expiry. |

For an **immediate, audit-friendly mass logout**, Force sign out is the right tool. For a quieter rotation (e.g., as part of a scheduled security rotation routine that doesn't need to bounce live users at the exact moment), `sessionKeyGuard` rotation is the alternative.

### No admin notification fires on force sign out

Unlike create / edit / password-change events, **Force sign out does NOT fire an admin notification** — there is no `force_signout` or `mass_logout` notification type in [[settings-admin-notifications]]. The merchant must coordinate with their team out-of-band that a mass logout is about to happen. (verify)

### Force sign out does not delete or modify staff records

The wipe targets session records only. No staff accounts are modified — every staff member's account, permissions, profile, and authenticator-app two-factor secret remain intact. After the wipe, the same staff members can log back in with the same credentials. To remove a moderator's access permanently, use [[settings-staff-delete]] in addition to (or instead of) Force sign out.

### Loader interaction

While the sign-out-everyone request is running, the confirm modal shows a spinner. The merchant cannot dismiss the modal during this window. On error, the modal stays open and surfaces the error message; on success, the toast renders and the 500ms reload timer starts.

## Related

- [[settings-staff]] — hub.
- [[settings-general]] — the `sessionKeyGuard` rotation alternative in the Security box.
- [[settings-staff-delete]] — for removing a specific moderator's account (not just their session).
- [[settings-admin-notifications]] — staff-lifecycle notifications (Force sign out is silent).
- [[account-cc2fa]] — the CC2FA session that is also logged out as part of the sweep.

## Open questions

- Does the `/logout-all` endpoint enforce `is_owner` server-side, or rely purely on the standard staff-management permission gate? (verify)
- Is the endpoint's HTTP verb GET or POST? (verify — the source notes GET, but mutating actions usually go through POST/DELETE)
- Is there any audit trail recorded for a Force sign out event (e.g., a log entry visible to CloudCart support staff), or is the action fully silent post-execution? (verify)
