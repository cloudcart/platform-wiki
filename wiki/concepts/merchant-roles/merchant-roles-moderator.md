---
type: concept
nav_path: "Concept → Merchant roles → Moderator (delegated admin)"
aliases: ["Moderator role", "Moderator account", "Customer Service role", "Order Manager role", "Add moderator", "Edit moderator", "Plan-limit check moderators", "administrators plan feature", "Plan downgrade moderators", "2FA gate moderator edit"]
tags: [access, staff, moderator, admin, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, permissions tree, API access, force sign-out + 2FA, notifications + audit, storefront contrast).

# Merchant roles — Moderator (delegated admin)

## Definition

A **Moderator** is any **additional admin account** the Owner (or a delegating Moderator with sufficient permissions) adds via [[settings-staff]] → **Add moderator**. Moderators have **granular per-section permissions** chosen from the hierarchical permissions tree (Products, Orders, Marketing, Settings, etc. — see [[merchant-roles-permissions-tree]]). Their `type` is `moderator`. A store can have multiple Moderators, capped by the plan's `administrators` plan-feature. Moderators can be deleted, edited, password-changed, and 2FA-configured by the Owner (or by another sufficiently-permissioned Moderator).

Informal terms like "Customer Service" or "Order Manager" are just a Moderator with permissions restricted to the Orders + Customers sections. CloudCart doesn't ship named role templates.

## Scope

This page covers the 3-gate create flow, the Create / Edit modal sections, what Moderators can and cannot do, the dynamic 2FA gate on Edit, and the `administrators` plan-feature cap (including the plan-downgrade "never silently disable" rule).

Not covered here:

- The permissions tree shape, delegation rules, plan-gated row auto-hide, runtime check — see [[merchant-roles-permissions-tree]].
- 2FA channels (email vs authenticator app) + Force sign out — see [[merchant-roles-force-signout-2fa]].
- The four admin lifecycle email notifications — see [[merchant-roles-notifications-audit]].
- API Keys / PATs (separate mechanism) — see [[merchant-roles-api-access]].

## Contrasts

- **Moderator vs Owner** — Moderators have a granted permission subset; Owners have everything. Moderators can be edited / deleted / password-changed by sufficiently-permissioned others; the Owner cannot.
- **Moderator vs API Key** — Moderators are human admin accounts with username, email, login, 2FA, avatar — they appear on [[settings-staff]] and count toward the `administrators` plan-feature cap. API Keys ([[settings-api-keys]]) are programmatic credentials with their own scope model — they don't appear on Staff, don't count toward the cap, no 2FA or login.
- **Default Moderator (none) vs Owner-default (full)** — a newly created Moderator has NO permissions ticked. Until sections are ticked in the tree, they can log in but see no sidebar entries beyond their own profile.

## Where it applies

### Create flow — three sequential gates

The **Add moderator** button on [[settings-staff]] runs three sequential gates:

1. **Plan-limit check.** The store compares the plan's `administrators` feature value (allowed seats) against the current admin count. If used seats meet or exceed the allowance, the Add button opens the upgrade paywall ([[plan-gates]]) instead of proceeding.
2. **2FA challenge.** The Owner (or delegating Moderator) must complete a 2FA challenge with action `create_moderator` — via email code or authenticator app, depending on their account. On success, a one-time hash is issued.
3. **Server hash validation.** The create request verifies that hash against the `create_moderator` action; if missing, expired, or reused, it fails. Once used, the hash is consumed.

After all three gates pass, the Create modal opens with three sections:

| Section | Fields |
|---------|--------|
| **Profile** | Username, Email, First name, Last name (all required) |
| **Contacts** | Country, City, Street address, Postal code, Phone number (optional) |
| **Access permissions** | The hierarchical permissions tree — checkbox per node |

After saving, the new Moderator gets a login on the admin panel (the `/admin` URL on the same store domain) and their granted permissions, and a `new_admin_account` admin email notification fires (see [[merchant-roles-notifications-audit]]).

### What Moderators CAN and CANNOT do

**CAN**: log in with email + password; configure 2FA on themselves (email is always-on after first login; authenticator-app TOTP is opt-in); see only the sidebar entries their permissions allow; edit their own non-permission fields (name, avatar, password — gated by their own 2FA if configured); create / edit / delete OTHER Moderators IF they hold the Settings → Staff permissions (delegation downward-only — see [[merchant-roles-permissions-tree]]).

**CANNOT**: see Owner-only Profile dropdown items (Plan, Billing, Invoices, My subscriptions); see the Force sign out button; edit or delete the Owner (three server-side guards reject this — see [[merchant-roles-owner]]); delete themselves through the UI; grant another Moderator permissions they don't themselves have; change a different Moderator's `type` to `owner` (no UI control; PATCH endpoint rejects it).

### Edit modal — 2FA gate decided dynamically

The Edit modal on [[settings-staff]] opens the same Profile + Contacts + Permissions sections as Create, plus Avatar, Password change, and 2FA configuration. The 2FA gate on Edit is decided dynamically:

- **Fresh `cc2fa_verify` session flag** (just passed a challenge) → step consumed and skipped.
- **Acting user editing themselves** → 2FA required only if they have an authenticator-app secret (`cc2fa_secret`) configured.
- **Owner editing someone else** → 2FA NOT required (the Owner is trusted for routine staff management).
- **Non-Owner Moderator editing another Moderator** → 2FA IS required if the acting Moderator has a `cc2fa_secret` configured.

This keeps the Owner unblocked for routine staff management while forcing extra verification when Moderators act on each other.

## `administrators` plan-feature cap

The `administrators` plan-feature caps Moderator count per store, varying by plan:

- Starter typically allows ~2 Moderators (verify).
- Pro typically allows 5–10 Moderators (verify).
- Enterprise typically removes the cap (verify).

When the cap is hit, the Add moderator button opens the paywall modal (the standard plan-gates flow — see [[plan-gates]]). The merchant has three paths:

1. Delete excess Moderators (lower used count below the cap).
2. Buy a Moderator-seat feature-pack (raise the cap by N seats).
3. Upgrade the plan (jump to a tier with more seats baked in).

### Plan downgrade does NOT auto-remove Moderators

If the merchant downgrades to a plan with fewer seats than they have Moderators, **all existing Moderators continue to log in normally** — the platform never silently disables accounts. Only the Add moderator button is locked, until the merchant prunes the list below the new cap or buys more seats. The paywall string is *"You have reached the maximum number of administrators allowed, you need to purchase more to continue."*

## Worked example — a Moderator quits

1. Owner opens [[settings-staff]], clicks Moderator A's row → Delete. The delete is allowed because the target is not the Owner, the acting user is the Owner, and they are not deleting themselves; the record, its permissions, and audit linkages are removed.
2. If Moderator A is logged in elsewhere, their session continues until expiry. The Owner can force immediate termination with Force sign out, which invalidates ALL admin sessions including the Owner's own — see [[merchant-roles-force-signout-2fa]].
3. The `admin_account_changes` notification fires.

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-owner]] — the role that can always edit / delete Moderators.
- [[merchant-roles-permissions-tree]] — the tree the Create / Edit modal renders.
- [[merchant-roles-force-signout-2fa]] — 2FA channels + Force sign out (Owner-only).
- [[merchant-roles-notifications-audit]] — admin lifecycle emails fired on Moderator create / edit / delete.
- [[settings-staff]] — the Staff management screen (Add / Edit / Delete UI).
- [[staff-member]] — Staff-Member entity (`type = moderator`).
- [[account]] / [[account-cc2fa]] — Moderator manages their own profile + 2FA here.
- [[plan-gates]] — `administrators` cap enforcement + paywall flow.
- [[plan]] — Plan entity; carries the `administrators` feature value.

## Open Questions

- ⏸️ Exact seat counts per plan tier (Starter / Pro / Business / Enterprise) — varies over time and by region; verify against [[plans]] catalogue at query time.
