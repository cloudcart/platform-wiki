---
type: entity
aliases: ["Staff member lifecycle", "Add moderator", "Edit staff member", "Delete moderator", "Add moderator checks", "Plan cap downgrade", "Жизнен цикъл на персонал"]
tags: [settings, access, staff, permissions, admin, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Staff Member — Lifecycle

## Identity

This page covers how a [[staff-member|Staff Member]] record comes into being, gets edited, and is removed — plus the gates that control adding and deleting Moderators. The Owner is created once at store registration and never deleted; everything below applies to the Moderator population the merchant actively manages on [[settings-staff]].

> Part of [[staff-member]]. See the hub for the other aspects (roles & types, permissions, 2FA, sessions & notifications, profile fields).

## Aliases

- "Add moderator" — the **+ Add moderator** button + modal on [[settings-staff]].
- "Plan-downgrade carry-over" — the rule that existing Moderators survive a plan downgrade.

## Key Attributes

| Lifecycle state | Trigger | Notes |
|-----------------|---------|-------|
| **Owner created** | Store registration | Automatic; no UI to repeat or revoke. |
| **Moderator added** | **+ Add moderator** on [[settings-staff]] | Gated by three sequential checks (below). |
| **Edited** | Edit modal | Profile, contacts, password, avatar, 2FA config, permissions (Moderators). |
| **Force-signed-out** | Owner-only button | See [[staff-member-sessions-notifications]]. |
| **Deleted** (Moderators only) | Per-row Delete | Hard delete; cannot delete the Owner or yourself. |

## Where it appears

- [[settings-staff]] — every lifecycle action (Add / Edit / Delete) happens here.
- [[plan-features]] — the `administrators` cap is read at Add time.
- [[settings-admin-notifications]] — each lifecycle event queues a notification (see [[staff-member-sessions-notifications]]).

## Business rules

### The full lifecycle

1. **Owner created at store registration.** When the store is registered, the registering account becomes the Owner (`type = owner`). No 2FA gate at this point — credentials were set during store creation. There is no UI to repeat or revoke this step.
2. **Moderator added** via **+ Add moderator** (three checks below), then the Profile + Contacts + Permissions sections are filled.
3. **Edited.** Username, email, contact details, password, avatar, 2FA configuration, and (for Moderators) permission set are editable from the Edit modal. A non-Owner cannot edit the Owner or change the Owner's password (server returns HTTP 422 in both cases). 2FA may be required on the edit depending on actor / target rules — see [[staff-member-2fa]].
4. **Force-signed-out.** The Owner can wipe all admin sessions — see [[staff-member-sessions-notifications]].
5. **Deleted (Moderators only).** A Moderator's row is removed via the per-row Delete button (visibility rules below). Delete is a **hard delete** — the Moderator's permissions and audit-log connections drop with them.

### Adding a Moderator is gated by three sequential checks

1. **Plan limit.** [[settings-staff]] reads the store's `administrators` plan-feature (allowed) and counts existing admins (used). If used ≥ allowed, the Add button opens the [[plan-features]] upgrade modal instead of proceeding. The Owner counts toward the cap too.
2. **2FA verification.** The Add button opens a 2FA action modal with action `create_moderator`. The actor must complete the challenge — email code if no authenticator-app secret is configured, otherwise the authenticator code. On success, a one-time hash is issued. See [[staff-member-2fa]].
3. **Server hash validation.** The create endpoint (`POST /admin/api/core/settings/account/admins/create/{hash}`) verifies the hash against the `create_moderator` 2FA action. Expired, missing, or wrong-action hashes are rejected. On success, the hash is marked used so it cannot be replayed, the Moderator row is created, the `new_admin_account` notification is queued, and the staff list re-fetches.

### Deleting a Staff Member follows visibility rules plus a server guard

The per-row Delete button is shown only when ALL of these are true:

- The row's `type_code` is NOT `owner`.
- Either the actor is the Owner, OR the actor is NOT the row being deleted (a user cannot delete themselves through this UI).

Server-side, the delete endpoint blocks deletion of any row with `type = owner` and returns HTTP 422 *"You cannot delete the owner."*

### Plan-feature cap on Moderator count and the downgrade carry-over

The `administrators` plan-feature value caps how many Staff Members the store can have (Owner counted). When the cap is reached, **Add moderator** redirects to the plan-upgrade flow with the message *"You have reached the maximum number of administrators allowed, you need to purchase more to continue."* On a paid upgrade, the cap increases and Add proceeds normally. **A plan downgrade does NOT auto-remove existing Moderators** — they continue to log in. The cap is enforced only at creation time, so a downgraded store can be over-quota until the merchant actively prunes Moderators or pays for more seats.

## Related

- [[staff-member]] — hub.
- [[settings-staff]] — the screen where the lifecycle plays out.
- [[plan-features]] — the `administrators` cap read at Add time.
- [[plan-gates]] — how the cap enforces itself.
- [[merchant-roles]] — Owner vs Moderator role model.

## Open Questions

None.
