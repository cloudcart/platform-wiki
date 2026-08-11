---
type: concept
nav_path: "Concept → Merchant roles → Permissions tree"
aliases: ["Permissions tree", "Permission inheritance", "Delegation downward only", "Plan-gated permission auto-hide", "Permission node disabled", "Granted section IDs", "Runtime permission check", "settings.admins.all"]
tags: [access, permissions, admin, plan-gates, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[merchant-roles]]. See the hub for the other aspects (owner, moderator, API access, force sign-out + 2FA, notifications + audit, storefront contrast).

# Merchant roles — permissions tree

## Definition

The **permissions tree** is the static hierarchical structure of admin-panel sections (Products, Orders, Marketing, Settings, Apps, …) that the merchant ticks on a Moderator's Create / Edit modal to grant access. Each node is a section with deeper children for granular actions (e.g., `Settings → Staff → settings.admins.all`). The tree is what every Moderator's access is built from; the Owner short-circuits the check.

Three transformations apply before the tree reaches the Create / Edit modal:

1. **Plan-gated rows are removed.** Permission nodes for features the store's plan doesn't include are stripped from the tree entirely.
2. **Each node's `disabled` flag is computed** from the acting user's own permissions. Owners see everything enabled; Moderators see only their own granted nodes enabled.
3. **Permissions submit as a flat array of section IDs.** The tree shape is UI sugar; storage is flat.

## Scope

What this page covers:

- The shape of the permissions tree (sample sections).
- The three transformations between catalog and rendered checkbox tree.
- The delegation-downward-only rule (acting user can only grant their own subset).
- Flat storage of granted section IDs and how runtime checks work.
- The "parent grants subtree" inheritance convention and what unticking a child means.
- The plan-gated permission-row auto-hide.

Not covered here:

- The Moderator Create flow itself — see [[merchant-roles-moderator]].
- The Owner short-circuit — see [[merchant-roles-owner]].
- The full list of permission section IDs (the tree is dynamic and changes as new features ship; documented per-feature on each feature page).
- API-Key / PAT scopes (a separate model) — see [[merchant-roles-api-access]].

## Contrasts

- **Permission grant vs Plan gate** — a permission grant restricts what a specific Moderator can do (Moderator-level). A plan gate ([[plan-gates]]) restricts what the entire store can do based on what was paid for. **Both gates must pass** — even a Moderator with full permissions can't access a feature the store's plan doesn't include.
- **Plan-gated permission auto-hide vs runtime permission check** — when the store's plan doesn't include a feature, the corresponding permission node is removed from the **delegation tree** entirely (auto-hide). Separately, the **runtime check** verifies the acting user's granted set when they hit an endpoint. Auto-hide is "you cannot grant"; runtime is "you cannot exercise."
- **Tree shape (UI sugar) vs flat storage (granted section IDs)** — the checkbox tree displays hierarchy; the DB stores a flat list. Ticking a parent writes all its children's IDs separately. Inheritance is a UX convention, not a runtime rule.

## Where it applies

### The tree shape — sample sections

The platform ships a static permission hierarchy that mirrors the admin-panel sidebar: **Products** (with leaves like Products → Products / Variants / Properties / Vendors), **Orders** (Orders / Abandoned carts / Refunds), **Settings** (General / Staff with `settings.admins.all` and `settings.admins.create` / Domains / Backups — plan-gated, auto-hidden if plan doesn't include `backups`), **Marketing** (Discounts / Campaigns / Segments / Subscribers), **Apps** (per-app permission nodes), etc.

The tree's exact membership changes as new features ship. The Create / Edit modal renders the current snapshot. See the per-feature pages (e.g., [[settings-staff]], [[settings-backups]]) for the section IDs they declare.

### Three transformations before rendering

**1. Plan-gated rows are removed.** If the store's plan doesn't include a feature (e.g., `backups`), the corresponding permission node is stripped from the tree — Moderators can't be granted access to a feature the store hasn't paid for. [[settings-backups]] is the canonical example.

**2. Each node's `disabled` flag is computed based on the acting user's own permissions.** If the acting user is the Owner, every node is enabled (the Owner short-circuit — see [[merchant-roles-owner]]). Otherwise, only nodes whose ID appears in the acting user's own permissions are enabled — greyed-out otherwise. **A Moderator can only delegate a subset of their own permissions, never more.**

**3. Permissions submit as a flat array of section IDs.** The tree shape is purely UI sugar. Under the hood the permission grant is a flat list. So checking a parent + a leaf both produce row entries; the merchant doesn't need to understand the parent-child storage.

### Delegation downward-only — privilege escalation prevented at two layers

When a Moderator creates another Moderator, the permissions tree is filtered to only the nodes the acting Moderator personally holds. Greyed-out nodes are non-grantable, so delegation flows downward — a junior Moderator cannot promote a peer above themselves. Even if they bypass the UI and craft a PATCH request directly to the API, server-side validation rejects it: **a non-Owner cannot grant permissions outside their own granted set**. UI greys out the option AND the server rejects the API call.

Example: Moderator C holds `Products + Orders`. On their own Edit modal, ticking `Settings → General` is **disabled** (greyed out) because they don't hold that permission to delegate; a direct PATCH is likewise rejected server-side.

### Permission inheritance — parent grants subtree (UX convention)

The checkbox tree's "tick parent ticks all children" behaviour is a UX convention layered on flat storage. In practice:

- **Checking a parent** translates to writing all its children's IDs to the granted-permissions list.
- **Unchecking one child of a parent** that was checked means that child's ID is NOT written — the rest of the children are kept.
- **The runtime check intersects the user's granted IDs with the endpoint's required IDs.** "Inheritance" is not enforced at runtime; it's just what the form does on save.

This means a Moderator can have `Products → Products` (the leaf) without holding the parent `Products` if the merchant unticks the parent but leaves the child — and the runtime check still works on the leaf ID.

### Runtime check — every page load + every API endpoint

The permission check runs on every admin-panel page load and on every API endpoint:

- The endpoint declares which permission sections grant access (often a small list like `settings,settings.admins.all,store.admins`).
- The acting user's permissions are loaded once at the start of the request.
- If the user is the Owner OR any declared section intersects with the user's granted set, access is allowed; otherwise, access is denied (the sidebar entry is hidden, the API returns 403).

### Plan-gated permission auto-hide — `backups` as the canonical example

If the store's plan doesn't include the `backups` feature, the `Settings → Backups` node is removed from the tree entirely and no Moderator can be granted Backups access. If the merchant later upgrades to a plan that includes `backups`, the node reappears on the next Edit modal open and the Owner can then tick it. This works for any plan-gated feature — see [[plan-gates]] for the broader mechanism.

## Related

- [[merchant-roles]] — hub.
- [[merchant-roles-moderator]] — the Create / Edit flow that renders this tree.
- [[merchant-roles-owner]] — the Owner short-circuit that bypasses the check.
- [[settings-staff]] — Staff screen where the tree is rendered.
- [[plan-gates]] — the broader plan-feature paywall + auto-hide mechanism.
- [[settings-backups]] — canonical plan-gated permission row.

## Open Questions

None.
