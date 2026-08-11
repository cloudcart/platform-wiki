---
type: entity
aliases: ["Staff member permissions", "Moderator permissions", "Permission tree", "Permission section IDs", "Permission delegation", "Subset delegation", "Права на модератор"]
tags: [settings, access, staff, permissions, admin, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Staff Member — Permissions

## Identity

A Moderator's access to the admin panel is defined by a **flat array of permission section IDs** stored on the [[staff-member|Staff-Member]] record. Each ID maps to an admin-panel area or action — e.g. `settings`, `settings.admins.all`, `settings.admins.create`, `store.admins`, `backups`, `orders`, `products`, `marketing.discounts`. The checkbox tree shown in the Add / Edit modal is **UI sugar**; the saved payload is a flat list. The Owner is not stored with permissions at all — it holds every permission implicitly and bypasses this whole model.

> Part of [[staff-member]]. See the hub for the other aspects (roles & types, lifecycle, 2FA, sessions & notifications, profile fields).

## Aliases

- "Permission section IDs" — the flat string keys saved on the record (`settings`, `orders`, `backups`, …).
- "Permission tree" — the hierarchical checkbox UI rendered in the Add / Edit modal.
- "Subset delegation" — the rule that a Moderator can only grant a subset of its own grants.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Permission set** (Moderators only) | Edited via the checkbox tree in the Edit modal | Stored as a flat array of section IDs; the tree shape is purely UI sugar. |
| **`createStaffAllow` flag** | n/a (derived) | Computed server-side and shipped in the table meta; controls whether this staff member sees the "Add moderator" button. Requires `settings.admins.create` (or being the Owner). |
| **Node `disabled` state** | n/a (computed per actor) | Each tree node is enabled only if the actor already holds it (Owner: all enabled). |

## Where it appears

- [[settings-staff]] — the Add / Edit modal renders the permission tree and saves the flat array.
- [[settings-staff-roles-list]] — the staff list reads `createStaffAllow` to decide whether to show "Add moderator".
- [[merchant-roles]] — the concept page describing the permission model.

## Business rules

### Permissions are hierarchical in the UI but capped by the actor's own grants

Three transformations happen before the permission tree reaches the frontend:

1. **Plan-gated permission nodes auto-hide.** If the store's plan does not include a feature (e.g. `backups`), that permission node is removed entirely from the delegation tree — the merchant cannot grant access to a feature they haven't paid for. See [[plan-gates]].
2. **Each node's `disabled` flag is computed.** If the actor is the Owner, every node is enabled. Otherwise, only nodes whose ID appears in the actor's own permissions are enabled. **A Moderator can only delegate a subset of their own permissions, never more.**
3. **Payload is flat.** Permissions are sent to the server as a flat array of section IDs; the tree shape is purely UI sugar.

### Permission middleware gates the staff API itself

Every endpoint under `/admin/api/core/settings/account/admins` is wrapped in `hasApiPermission:settings,settings.admins.all,store.admins`. A Moderator without at least one of those three permissions cannot even list the Staff table. The Owner holds all permissions implicitly. The `createStaffAllow` flag additionally requires `settings.admins.create` for non-Owners — without it, the "Add moderator" button is hidden.

### The permission section catalog is dynamic — no exportable manifest

The full permission tree is built dynamically at request time from registered admin-panel navigation items and the active plan's plan-features. There is **no exportable manifest** — the tree is only knowable from the Add modal as rendered for the current store + current plan. New feature releases extend the tree automatically when new sidebar items / API endpoints register their permission IDs.

### Owner bypasses the permission model entirely

The Owner is not stored with a permission array. Every permission check short-circuits to "allowed" for the Owner, and every tree node renders enabled. See [[staff-member-roles-types]].

## Related

- [[staff-member]] — hub.
- [[merchant-roles]] — the permission model in concept form.
- [[settings-staff]] — where permissions are edited.
- [[settings-staff-roles-list]] — the staff list + `createStaffAllow`.
- [[plan-gates]] — how plan-gated permission nodes auto-hide.

## Open Questions

None.
