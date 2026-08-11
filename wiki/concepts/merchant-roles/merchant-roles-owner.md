---
type: concept
nav_path: "Concept → Merchant roles → Owner (root account)"
aliases: ["Owner role", "Store owner", "Root admin account", "Owner unique", "Owner immutable", "Owner cannot be deleted", "Transfer ownership", "Connected social accounts owner"]
tags: [access, staff, owner, admin, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[merchant-roles]]. See the hub for the other aspects (moderator, permissions tree, API access, force sign-out + 2FA, notifications + audit, storefront contrast).

# Merchant roles — Owner (root account)

## Definition

The **Owner** is the account that **registered the store on CloudCart**. The `type` field on the admin record is set to `owner` at registration and never changes. There is exactly **one Owner per store**. The Owner is the store's root admin — they can do everything, see everything, change billing, switch plans, manage staff, and force-sign-out everyone. The Owner cannot be deleted, cannot be demoted, and cannot be transferred to a different account without CloudCart support intervention.

## Scope

What this page covers:

- The unique `type = owner` record and how it is set at registration.
- The full Profile dropdown (Plan, Billing, Invoices, My subscriptions) visible only to the Owner.
- The three server-side guards that block edit / delete / password-change of the Owner by anyone else.
- The Owner-only Connected social accounts section.
- The ownership-transfer path (support ticket only).

Not covered here:

- The Moderator creation flow and Edit modal — see [[merchant-roles-moderator]].
- The Force sign out button itself — see [[merchant-roles-force-signout-2fa]].
- API-Key / PAT access (separate mechanism, not the Owner) — see [[merchant-roles-api-access]].

## Contrasts

- **Owner `type = owner` vs Moderator `type = moderator`** — the `type` field on the admin record is set at registration and is not editable through the admin UI. The PATCH endpoint rejects type changes.
- **Owner has every permission vs Moderator has granted subset** — the permission check for `type = owner` short-circuits the gate and returns full access without a lookup. Moderators go through the normal intersection check. See [[merchant-roles-permissions-tree]].
- **Owner-only Profile dropdown vs Moderator-visible sidebar** — Plan / Billing / Invoices / My subscriptions are role-gated to Owner only and not exposed through any permission. No combination of Moderator permissions reveals them.

## Where it applies

The Owner role surfaces across:

### Full Profile dropdown (Owner only)

In the admin top-right Profile dropdown, the Owner sees:

- **Plan** — current plan + upgrade flow ([[plans]]).
- **Billing** — invoices, payment methods.
- **Invoices** — downloadable PDFs.
- **My subscriptions** — the merchant's CloudCart service subscriptions (SMS packs, Cloudio AI, etc.).
- **Plan features** — feature-pack upsell screen ([[plan-features]]).

Moderators do NOT see these items, regardless of any permission they hold.

### Permission short-circuit

The permission check verifies the user's granted set when they try to access an endpoint. For `type = owner`, the platform reads `isOwner` and short-circuits the gate — every endpoint passes, every sidebar entry is visible, every permission node is enabled.

### Force sign out — Owner-only

The **Force sign out** button on [[settings-staff]] header is visible only to the Owner. The action deletes every admin session, invalidates the 2FA session layer, and signs the Owner out as a side effect. See [[merchant-roles-force-signout-2fa]] for the contrast with `sessionKeyGuard` rotation.

### Connected social accounts (Owner only)

The Owner's Edit modal on [[settings-staff]] shows a **Connected social accounts** section listing OAuth identities (Google, Facebook, etc.) the Owner has linked. The connect / disconnect actions are NOT on the Staff screen — they're on the public login page's "Sign in with Google" / "Sign in with Facebook" flow. The Edit modal shows them as read-only. Moderators don't have this section.

## Server-side guards — three rejections

Three guards protect the Owner record from non-Owner modification:

| Action attempted on Owner by non-Owner | HTTP response | Message |
|---|---|---|
| PATCH `/admin/staff/<owner-id>` | 422 | *"You cannot change the owner"* |
| Password-change on Owner | 422 | *"You cannot change the owner password"* |
| DELETE `/admin/staff/<owner-id>` | 422 | *"You cannot delete the owner."* |

No combination of Moderator permissions overrides these. The guards run after the permission check, so even a Moderator with `settings.admins.all` is rejected.

## Ownership transfer — not self-service

There is no UI control to flip the `type` field from `moderator` to `owner` on a different account. The PATCH endpoint rejects type changes. The only transfer path is via **CloudCart support** — used when:

- A business is sold to a new operator.
- The original Owner leaves the company and the account email is no longer accessible.
- The Owner account is compromised and needs to be replaced.

Support handles the swap manually. Downtime during the transfer depends on the support team's process. See the Open Questions on [[merchant-roles]] for the (verify) note.

## What the Owner typically does first

The Owner's first task on a new store is typically to:

1. Configure their own 2FA on [[account-cc2fa]] (authenticator app preferred over email-only).
2. Set the store's billing email + invoice details.
3. Provision a few Moderators via [[settings-staff]] for day-to-day work (see [[merchant-roles-moderator]]).

This sequence minimises the time the store has only one credential pathway.

## Related

- [[merchant-roles]] — hub.
- [[settings-staff]] — where the Owner row appears (top of list, no delete / no edit by non-Owner).
- [[staff-member]] — Staff-Member entity (carries `type = owner`).
- [[account]] / [[account-cc2fa]] — Owner manages their own profile + 2FA here.
- [[plans]] / [[plans-purchase]] / [[plan-features]] — Owner-only screens via the Profile dropdown.
- [[settings-admin-notifications]] — admin lifecycle notifications cover Owner profile edits too.

## Open Questions

None.
