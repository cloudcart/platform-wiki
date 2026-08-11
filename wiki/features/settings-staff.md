---
type: feature
nav_path: "Settings → Staff"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Staff management", "Staff", "Moderators", "Administrators", "Персонал", "Модератори", "Администратори"]
tags: [settings, staff, access, permissions]
plan_gates: ["administrators"]
created: 2026-05-21
updated: 2026-06-10
source_count: 14
---
# Staff

## Purpose

Manages the people who can log into the admin panel of the store. There is exactly one **Administrator** (the store owner — the person who created the store on CloudCart) and any number of **Moderators** (subordinate staff with limited, per-section permissions). This is where the owner adds new Moderators, edits their profile and granular permissions, removes them, configures two-factor authentication, and — owner-only — force-signs-out everyone in case of suspected credential compromise.

Creating a new Moderator is plan-gated, requires two-factor verification at the moment of creation, and emits an admin notification on success. Editing and deletion are constrained by role: a Moderator cannot edit the owner, cannot delete the owner, and cannot delete themselves.

## Where to find it

Sidebar → Settings → **Staff**.

Breadcrumb reads "Settings → Staff". URL: `/admin/settings-new/staff`.

## What the merchant can do here

- See the full list of staff (owner + all moderators) with username, email, address, phone, and last-updated timestamp.
- Sort the list by username, email, or last updated.
- Click any row to edit the person's profile (everything except deleting the owner row).
- Click **Add moderator** to create a new Moderator (opens a 2FA verification modal, then a multi-step profile form).
- Upload a profile avatar and change the password on the edit form for users they have permission to modify.
- Configure authenticator-app two-factor authentication (QR setup) for individual staff members via the Edit modal.
- Edit a Moderator's granular per-section permissions (checkbox tree).
- Delete a Moderator (with several visibility guards — see [[settings-staff-delete]]).
- (Owner only) Click **Force sign out** to invalidate every admin and moderator session in one click.
- Deep-link directly to "edit user X" via `#user-<id>` in the URL hash, or to "create new" via `#create-<hash>`.

## Settings & fields

The screen has three interactive surfaces; full mechanics live in the aspect pages.

| Surface | Where / contents | Documented in |
|---------|------------------|---------------|
| **Page header** | **Add moderator** button (visible to anyone who can open the page) and **Force sign out** button (owner only) | [[settings-staff-create-moderator]] / [[settings-staff-force-signout]] |
| **Staff list table** | Columns, sorting, per-row actions | [[settings-staff-roles-list]] |
| **Create / Edit modal** | Opens on row click or **Add moderator** — Profile, Contacts, Permissions, 2FA, Avatar | [[settings-staff-create-moderator]] (Create) / [[settings-staff-edit-profile]] (Edit) |

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question.

- [[settings-staff-roles-list]] — Administrator vs Moderator role types; the staff list table (columns, sorting, default sort); URL hash deep-linking; only two role types exist in the platform.
- [[settings-staff-create-moderator]] — Add Moderator three-step chain (2FA → Create modal → optional QR); plan-limit gating + upsell modal; one-time hash lifecycle (2 min / 60 min).
- [[settings-staff-edit-profile]] — Edit modal sections; avatar upload constraints (250×250, 25 KB); change-password rules; validation caps; field-level edit restrictions (non-owner editing owner blocked).
- [[settings-staff-permissions-tree]] — `CcCheckboxTree` permission hierarchy; delegate-only-what-you-have rule; `backups` node plan-gating; `settings.admins.create` carve-out.
- [[settings-staff-2fa]] — Email-2FA always-active vs configurable authenticator-app TOTP; QR Setup modal; the "is 2FA required for this edit?" gating helper.
- [[settings-staff-delete]] — Delete moderator inline confirm; per-row visibility rules; server-side guard against deleting the owner; no soft-delete / no audit log.
- [[settings-staff-force-signout]] — Owner-only mass logout button; invalidates every admin/moderator session; difference vs the session-key rotation on [[settings-general]].

## What the merchant CANNOT do here

- Delete the store owner (server returns 422 *"You cannot delete the owner"*).
- Change the owner's password if the current user is not the owner (server returns 422 *"You cannot change the owner password"*).
- Edit the owner's profile if the current user is not the owner.
- Promote a moderator to owner (no UI control; type is fixed at `moderator` on creation; ownership transfer requires CloudCart support).
- Grant a moderator permissions that the current acting user does not themselves possess (see [[settings-staff-permissions-tree]]).
- Skip 2FA when adding a new Moderator — gate enforced both client-side and server-side via a one-time hash.

## Business rules (cross-cutting — details in aspects)

### Owner is unique and immutable in this screen

There is exactly one `type=owner` per store — created when the store was originally registered on CloudCart. The owner row appears in the table but cannot be deleted or have its type changed here. Ownership transfer is handled outside the admin panel (via CloudCart support). See [[settings-staff-roles-list]].

### Moderator creation is gated by three sequential checks

1. **Plan limit** — current staff count vs the `administrators` quota on the plan.
2. **2FA** — the user must complete a 2FA challenge for the `create_moderator` action.
3. **One-time hash** — the create step verifies a one-time hash before saving.

Full mechanics on [[settings-staff-create-moderator]].

### Admin notifications fire on staff lifecycle events

Four admin-notification types are triggered by this screen (all gated by [[settings-admin-notifications]]):

- `new_admin_account` — moderator created.
- `admin_account_changes` — profile edited.
- `admin_account_password_change` — password updated via the Edit modal.
- `admin_account_password_reset` — password reset requested (from the admin login page, not from this screen).

If the merchant has turned off `administrator_email_notifications` OR the per-type toggle, these notifications are suppressed silently.

### Access to the screen requires a staff permission

A moderator without the `settings.admins.all` permission cannot even open or list the staff table. See [[settings-staff-permissions-tree]] for the delegation rules.

### No merchant-facing audit log

There is **no merchant-facing audit-log page** for staff actions, and the internal logging hooks are currently inactive. Lifecycle visibility is therefore limited to the four admin email notifications above. For richer accountability, merchants must contact CloudCart support.

### Cache behavior

The staff list is **not** cached — every page load re-queries the latest data, and Edit/Update actions re-fetch on success to keep the table in sync without a full reload.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `administrators` | Numeric quota | How many staff seats (owner + moderators) the merchant's plan allows. The owner counts toward the cap. Plan downgrade does NOT auto-remove existing moderators — only NEW creates are blocked. Extendable via packs ([[plan-vs-feature-pack]]). |

A second plan-conditional carve-out: the `backups` permission node is removed from the permissions tree when the merchant's plan doesn't enable `backups` — see [[settings-staff-permissions-tree]] and [[settings-backups]].

## Related

- [[settings]] — parent area hub.
- [[settings-general]] — for session-key rotation (alternative to Force sign out) and `site_email` (default notification recipient).
- [[settings-admin-notifications]] — the 4 admin notifications triggered by this screen and their delivery rules.
- [[merchant-roles]] — concept page on Administrator vs Moderator vs Customer vs Subscriber.
- [[staff-member]] — entity page for the Moderator/Administrator entity model.
- [[plan]] — the `administrators` plan feature that gates seat count.
- [[plan-gates]] — concept page on how plan limits enforce themselves across the admin panel.
- [[account-cc2fa]] — the `Cc2FaAction` modal and 2FA configuration flows referenced throughout this cluster.
- [[settings-backups]] — `backups` permission row is conditionally hidden when the feature isn't on the plan.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
