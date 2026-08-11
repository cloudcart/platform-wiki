---
type: feature
nav_path: "Settings → Staff → Permissions tree"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Staff permissions", "Permissions tree", "Moderator permissions", "Access permissions", "CcCheckboxTree", "Permission hierarchy"]
tags: [settings, staff, permissions, access-control, plan-gate]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, create, edit, 2FA, delete, force sign out).

# Staff — permissions tree

## Purpose

Documents the **Access permissions** section that appears on the Create and Edit modals (moderators only — the owner doesn't get this section because the owner has everything by default). Covers the hierarchical `CcCheckboxTree` shape, the **delegate-only-what-you-have** rule, the `backups` permission's plan-gating, the dormant `settings.admins.create` carve-out, and the API-side permission middleware.

## Where to find it

Inside the Create or Edit modal on Settings → Staff, in the **Access permissions** section (third / fourth section depending on mode). Only visible when the row being edited has `type_code === 'moderator'`.

## What the merchant can do here

- Grant or revoke a moderator's access to specific admin-panel sections via checkboxes.
- Use parent checkboxes to grant the whole sub-tree at once (e.g., checking "Settings" grants all settings sub-pages).
- See greyed-out (disabled) permissions that the acting user themselves does not hold — these cannot be delegated.

## Settings & fields

### The permission tree

Implementation: `CcCheckboxTree` — a recursive checkbox component. The tree shipped to the form is the platform's full admin permission hierarchy with approximately **80+ permission nodes** covering every sidebar section, every feature toggle, and every sub-page:

- **Dashboard**
- **Orders**
- **Products** (with deeper children for categories, parameters, statuses, etc.)
- **Customers**
- **Marketing**
- **Settings** (with deep sub-trees for each settings sub-page)
- **Reports**
- **Apps**
- ... and more.

Each permission node has:

- `id` — the permission section key (e.g., `settings.admins.all`, `store.admins`, `marketing.discounts`).
- `label` — human-readable label.
- `children` — nested permissions (parent grants whole sub-tree).
- `disabled` — computed flag (see below).

Permissions are sent to the create/update endpoint as a **flat array of section IDs** — the tree shape is purely UI sugar. Order does not matter.

### Three pre-render transformations

Before the tree reaches the frontend:

1. **`backups` node is removed** if the store's plan does not have the `backups` feature enabled. The merchant cannot grant access to a feature their plan doesn't include. See [[settings-backups]].
2. **`disabled` flag is computed per node:**
   - If the acting user is the owner → every node is `disabled=false` (enabled).
   - Otherwise → only nodes whose `id` appears in the acting user's own permissions are enabled; everything else is `disabled=true` (greyed out).
3. **Owner-rows never receive this section** — when editing the owner, the modal hides the Access permissions box entirely (the owner has everything by default).

## Business rules

### Delegate-only-what-you-have

**A moderator can only delegate a subset of their own permissions, never more.** The owner has the full tree fully enabled; a moderator creating or editing another moderator can only tick the boxes corresponding to permissions they themselves hold. Permissions the acting user does not have are visible in the tree (so the merchant sees the full hierarchy) but are `disabled=true` (greyed out).

Practical implication: there is no admin-tier between owner and moderator. To give a moderator the ability to manage other staff, the owner must explicitly grant `settings.admins.all` to that moderator — but even then, the moderator can only delegate the sections THEY hold to a new moderator. Permission inflation is impossible.

### `backups` permission node is plan-gated for the form, not for the moderator already holding it

If a moderator was created on a plan that included Backups and that permission was granted, then the merchant downgrades to a plan without Backups, **the moderator keeps the permission row in the database**. The form simply removes the Backups node from the tree when re-editing — so the merchant cannot un-tick it through the UI (it isn't visible), and they cannot add it to a different moderator.

The dormant permission is harmless because access to the Backups feature is also independently gated by the plan check elsewhere in the platform — so the moderator effectively cannot use it even though the row exists. To clear it, the merchant must upgrade back to a plan that includes Backups, re-open the moderator, un-tick the box, then downgrade again.

### `settings.admins.create` — defined in config but commented out

A separate `settings.admins.create` permission node is defined in the config but **commented out** — **in practice today only the owner sees the Add moderator button**, regardless of what permissions are granted to a moderator on the staff section. The `createStaffAllow` flag is computed and shipped in the table meta, but moderators effectively cannot create other moderators today. (verify — confirm whether re-enabling the config node is on the roadmap)

### Permissions middleware on the API endpoints

Every endpoint under `/admin/api/core/settings/account/admins` is wrapped in `hasApiPermission:settings,settings.admins.all,store.admins`. Translation: the acting user must have at least one of these three permission sections to make any API call against the staff API. A moderator without any of them cannot even list the staff table (the page itself renders empty / 403).

The owner has all permissions by default.

### Permissions tree is hierarchical — parent grants whole sub-tree

Checking a parent permission automatically grants the entire sub-tree underneath it. The flat-array payload sent to the server includes every child ID under a checked parent. Un-checking the parent un-checks all children.

### Permissions are flat strings server-side

Despite the UI showing a tree, the persisted permission set is a **flat array of section IDs**. The tree shape is reconstructed in the UI from the static config. So permission storage is order-independent and tree-mutation-resistant: if the platform adds a new permission node tomorrow, existing moderators do not auto-receive it (they only have the IDs explicitly granted).

## Related

- [[settings-staff]] — hub.
- [[settings-staff-create-moderator]] — where the permissions tree first appears for new moderators.
- [[settings-staff-edit-profile]] — where the permissions tree appears for existing moderators.
- [[settings-backups]] — the `backups` plan-feature that gates the `backups` permission node.
- [[plan-gates]] — concept page on how plan-features gate UI.
- [[merchant-roles]] — Administrator vs Moderator role types.

## Open questions

- Is re-enabling the commented-out `settings.admins.create` permission node on the roadmap, or is "only the owner can create moderators" an intentional product decision? (verify)
- Full list of the ~80 permission node IDs (would be useful for the support LLM to match against ticket questions like "I want to give my warehouse staff access to X").
