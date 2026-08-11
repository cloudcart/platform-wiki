---
type: concept
nav_path: "Concept → Merchant roles (hub)"
route_name: (none)
route_path: (none)
aliases: ["Merchant roles", "Owner vs Moderator", "Administrator vs Moderator", "Staff roles", "Admin accounts", "Permissions model", "Store owner", "Moderator", "Admin role", "Staff permissions", "Permission inheritance", "Собственик и модератори", "Администратор и модератор", "Роли на персонала", "Права на достъп"]
tags: [access, staff, permissions, admin, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Merchant roles (hub)

## Definition

The CloudCart admin panel is accessed by a small number of **admin accounts** that the store has provisioned — distinct from the unlimited [[customer|Customers]] and [[subscriber|Subscribers]] who interact with the storefront. Admin accounts come in two built-in role types, plus a separate access mechanism for programmatic clients:

1. **Owner** — the **single account** that created the store on CloudCart. Root admin: full access, cannot be deleted, demoted, or transferred without CloudCart support. `type = owner`. See [[merchant-roles-owner]].
2. **Moderator** — any additional admin account the Owner (or a delegating Moderator) adds via [[settings-staff]]. Granular per-section permissions, capped by the plan's `administrators` plan-feature. `type = moderator`. See [[merchant-roles-moderator]].
3. **API access** — entirely separate from staff accounts. [[settings-api-keys|API Keys]] (long-lived OAuth-style credentials) and [[settings-pat-tokens|Personal Access Tokens]] (PATs) authenticate machine clients. NOT staff accounts; do NOT appear on [[settings-staff]]; do NOT count toward the `administrators` cap. See [[merchant-roles-api-access]].

A common informal term — "Customer Service" or "Order Manager" — is just a Moderator with permissions restricted to the Orders + Customers sections. CloudCart doesn't ship named role templates (no "Marketing role", no "Warehouse role"); the merchant builds each Moderator's permission set from scratch via the permissions checkbox tree. See [[merchant-roles-permissions-tree]].

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages. Drill into the aspect that matches the question, not every page.

- [[merchant-roles-owner]] — the unique root account; the three server-side guards against edit / delete / password-change; Owner-only Profile dropdown items (Plan, Billing, Invoices, My subscriptions); Connected social accounts.
- [[merchant-roles-moderator]] — Moderator creation flow (3 gates: plan-limit, 2FA, server hash), Edit modal sections, dynamic 2FA gate on edit (self / Owner-on-other / Moderator-on-Moderator), what Moderators can and cannot do.
- [[merchant-roles-permissions-tree]] — the hierarchical permission tree (Products / Orders / Marketing / Settings / Apps), plan-gated row auto-hide, delegation-downward-only rule, flat storage of granted section IDs, runtime permission check on every page load + API endpoint.
- [[merchant-roles-api-access]] — API Keys (long-lived, integrations) vs PAT Tokens (short-to-mid-lived, development); scopes are NOT Moderator permissions; do NOT count toward the `administrators` cap; revocation is per-credential.
- [[merchant-roles-force-signout-2fa]] — Owner-only Force sign out vs `sessionKeyGuard` rotation; email two-factor (always-on after first login) vs authenticator-app TOTP (`cc2fa_secret`); which sensitive actions trigger a 2FA challenge.
- [[merchant-roles-notifications-audit]] — the four admin lifecycle email notifications (`new_admin_account`, `admin_account_changes`, `admin_account_password_change`, `admin_account_password_reset`); internal audit log with no merchant-facing view; Forgot-password reset flow.
- [[merchant-roles-storefront-contrast]] — Customers and Subscribers are storefront users, NOT admin accounts; a Moderator who also buys from the store has a separate Customer record; cross-reference to [[subscriber-vs-customer]].

## Scope

What this concept covers (across the 7 sub-pages):

- The two admin role types — **Owner** (unique, root) and **Moderator** (multiple, per-section permissions).
- The **granular permissions tree** with delegation-downward-only and plan-gated auto-hide.
- The **plan-gated `administrators` cap** on Moderator count + the plan-downgrade rule that never silently disables Moderators.
- The **2FA gates** on Moderator create / edit and per-user authenticator-app option.
- **Owner-only Profile dropdown** items and **Force sign out** mass logout.
- The **four admin lifecycle email notifications**.
- **API access** as a parallel, separate mechanism — [[settings-api-keys]] and [[settings-pat-tokens]].

What it does NOT cover:

- Storefront-side users — see [[customer]], [[subscriber]], [[subscriber-vs-customer]].
- The detailed UX of the [[settings-staff]] screen (table columns, modal layouts) — that lives on the feature page.
- The exact list of permission section IDs — the tree is dynamic; documented per-feature.
- API-Key / PAT scope catalogs — see [[settings-api-keys]] and [[settings-pat-tokens]].
- 2FA setup mechanics (QR code, email code, recovery codes) — see [[account-cc2fa]], [[account-cc2fa-email]], [[account-cc2fa-codes]].

## Contrasts

- **Owner vs Moderator** — one Owner per store, with full unconditional access; multiple Moderators, each with granular per-section permissions. The Owner cannot be deleted, edited, or password-changed by others. See [[merchant-roles-owner]] + [[merchant-roles-moderator]].
- **Moderator vs API Key vs PAT Token** — Moderators are human admin accounts with username, email, login, 2FA, avatar — they appear on [[settings-staff]] and count toward the `administrators` cap. API Keys and PATs are programmatic credentials, on separate screens, with their own scope model, not subject to the cap. See [[merchant-roles-api-access]].
- **Permission grant vs Plan gate** — a permission grant restricts what a specific Moderator can do (Moderator-level). A plan gate restricts what the entire store can do based on what was paid for. Both gates must pass. See [[merchant-roles-permissions-tree]] + [[plan-gates]].
- **Owner-only Profile dropdown vs Moderator-visible sidebar** — Plan, Billing, Invoices, My subscriptions are role-gated to Owner only (no permission can grant them). Sidebar entries (Products, Orders, Marketing, Settings, etc.) are permission-gated.
- **Force sign out vs Session key rotation** — both invalidate admin sessions. Force sign out is Owner-only on [[settings-staff]], immediate; `sessionKeyGuard` rotation in [[settings-general]] rotates the cookie name pattern. **Force sign out does NOT revoke API Keys or PAT Tokens** — those have their own revocation surfaces. See [[merchant-roles-force-signout-2fa]].
- **Customer vs Subscriber vs Moderator vs Owner** — all four interact with CloudCart but live in different parts of the model. None overlap as records. See [[merchant-roles-storefront-contrast]].

## Where it applies

The role / permission model touches the whole admin panel; primary surfaces:

- **Admin account management** — [[settings-staff]], [[staff-member]], [[account]], [[account-cc2fa]] / [[account-cc2fa-email]] / [[account-cc2fa-codes]].
- **Owner-only Profile dropdown** — [[plans]], [[plans-purchase]], [[plan-features]].
- **API access** — [[settings-api-keys]], [[settings-pat-tokens]], [[api-key]], [[pat-token]].
- **Plan-gating + permission-tree dependencies** — [[plan-gates]], [[settings-backups]] (example of an auto-hidden permission row).
- **Notifications + audit** — [[settings-admin-notifications]], [[settings-general]] (`sessionKeyGuard`).
- **Storefront-user contrast** — [[customer]], [[subscriber]], [[subscriber-vs-customer]].

## Why it matters to the merchant

This concept governs **who can do what** inside the admin panel. Getting it wrong creates two opposite problems:

- **Too permissive**: a Moderator with the full tree can change the store's plan, billing email, or domain, or keep access to financial records after leaving.
- **Too restrictive**: Moderators can't do their daily work, constantly need the Owner to unblock them, and resort to shared logins (which defeats the audit trail).

The model is intentionally simple — two role types, with fully-customisable permissions on the Moderator side. There are no "role templates" or "permission groups"; every Moderator is built from a fresh checkbox tree. See [[merchant-roles-permissions-tree]] for delegation rules.

## Related

- [[settings-staff]] — the Staff management screen.
- [[staff-member]] — Staff-Member entity (Owner / Moderator).
- [[account]] / [[account-cc2fa]] — per-admin account profile + 2FA setup.
- [[settings-api-keys]] / [[settings-pat-tokens]] — separate-access-mechanism screens.
- [[api-key]] / [[pat-token]] — programmatic-credential entities.
- [[plans]] / [[plans-purchase]] / [[plan-features]] — Owner-only plan / billing flows.
- [[plan]] — Plan entity; carries `administrators` feature cap.
- [[plan-gates]] — `administrators` cap enforcement; plan-gated permission rows.
- [[settings-admin-notifications]] — admin lifecycle email notifications.
- [[settings-backups]] — plan-gated permission auto-hide example.
- [[settings-general]] — `sessionKeyGuard` rotation as an alternative to Force sign out.
- [[customer]] / [[subscriber]] / [[subscriber-vs-customer]] — storefront users (NOT admin accounts).

## Open Questions

- ⏸️ Ownership transfer between accounts is NOT a self-service action — the merchant cannot demote / re-assign the Owner row from the admin UI. To transfer a store to a different account, the merchant opens a support ticket with CloudCart; support handles the account swap manually. Downtime during the transfer depends on the support team's process.

All other previously-flagged questions resolved. See sub-pages for details.
