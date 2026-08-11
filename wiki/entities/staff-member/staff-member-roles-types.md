---
type: entity
aliases: ["Staff member roles", "Owner vs Moderator", "Staff member type", "Owner type", "Moderator type", "Ownership transfer", "Собственик срещу Модератор"]
tags: [settings, access, staff, permissions, admin, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
# Staff Member — Roles & Types

## Identity

Every [[staff-member|Staff Member]] is one of exactly two types, fixed at creation:

- **Owner** (`type = owner`) — the single root account per store, created automatically when the store is registered. The Owner has every permission unconditionally and bypasses the permission tree entirely.
- **Moderator** (`type = moderator`) — every other admin account. A Moderator only reaches the screens, sidebar entries, and API endpoints granted by its [[staff-member-permissions|permission set]].

The type is **immutable through the admin panel** — there is no UI control to promote a Moderator to Owner or to demote the Owner. The only path to change ownership is a CloudCart support-led process (see below).

> Part of [[staff-member]]. See the hub for the other aspects (permissions, lifecycle, 2FA, sessions & notifications, profile fields).

## Aliases

- "Owner" / "Собственик" — the single `type = owner` root account.
- "Moderator" / "Модератор" — any `type = moderator` account.
- "Administrator" / "Admin" / "Администратор" — informal umbrella for either type; also the wording on the `administrators` plan-feature cap.

## Key Attributes

| Attribute | Owner | Moderator |
|-----------|-------|-----------|
| **`type`** | `owner` (exactly one per store) | `moderator` (any number) |
| **Created** | Automatically at store registration | Added on [[settings-staff]] via **+ Add moderator** |
| **Permissions** | All, unconditionally (bypasses the tree) | Hand-picked subset — see [[staff-member-permissions]] |
| **Deletable** | No — never shows a delete button; server blocks with HTTP 422 | Yes — per-row Delete (cannot delete self) |
| **Counts toward the `administrators` cap?** | Yes | Yes |
| **Sees Owner-only Profile items?** | Yes (Plan, Billing, Invoices, My subscriptions) | No — not unlockable by any permission |

## Where it appears

- [[settings-staff]] — the Owner row is shown distinctly (no delete button); Moderators are added / edited / deleted here.
- [[merchant-roles]] — the concept page mapping Owner vs Moderator vs API Keys vs PATs.
- [[plan-features]] / [[plans]] — the Owner-only Profile dropdown items and the `administrators` cap.

## Business rules

### Owner is unique, immutable, and CloudCart-controlled

There is exactly one `type = owner` per store. The Owner row appears in the Staff list but never shows a delete button; the server enforces this with HTTP 422 *"You cannot delete the owner."* The Owner's type cannot be changed in the UI, and the Owner holds every permission unconditionally — the [[staff-member-permissions|permission tree]] is bypassed entirely for the Owner.

### Owner-only Profile dropdown items

The Profile dropdown items **Plan**, **Billing**, **Invoices**, and **My subscriptions** are role-gated to the Owner only — no Moderator permission can unlock them. The same surfaces are unreachable for Moderators even with the broadest permission set. See [[merchant-roles]].

### Ownership transfer is support-led

Ownership transfer is **not exposed in the admin panel** — it is a CloudCart support-led process initiated by emailing support. The support team verifies the requester's identity (typically requires both the outgoing and incoming Owner's email confirmation), then flips the `type = owner` flag and links the new Owner's account record. Turnaround time is typically same-day to 1 business day for verified requests. This usually happens when a business is sold or the founding admin leaves.

### Owner vs Moderator in the 2FA edit rules

The actor's type changes how 2FA gates behave when editing staff records — the Owner stays unblocked for routine maintenance, while non-Owners face extra verification when acting on others. See [[staff-member-2fa]] for the full actor-vs-target matrix.

### The Owner also appears as a Customer if they place a test order

Placing a storefront test order creates a separate [[customer|Customer]] record with the Owner's name and email — it is NOT linked to the Staff-Member record. The Owner is then visible both as a Staff Member and as a Customer. See [[merchant-roles-storefront-contrast]].

## Related

- [[staff-member]] — hub.
- [[merchant-roles]] — Owner vs Moderator vs API Keys vs PATs.
- [[merchant-roles-owner]] — concept-side detail on the Owner role.
- [[merchant-roles-moderator]] — concept-side detail on the Moderator role.
- [[settings-staff]] — the management screen where the type distinction surfaces.
- [[plan]] — the `administrators` cap counts both Owner and Moderators.

## Open Questions

None.
