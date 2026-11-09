---
type: feature
nav_path: "Settings → Staff → Permissions tree"
route_name: staff.settings
route_path: /admin/settings/staff
aliases: ["Staff permissions", "Permissions tree", "Moderator permissions", "Access permissions", "CcCheckboxTree", "Permission hierarchy"]
tags: [settings, staff, permissions, access-control, plan-gate]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[settings-staff]]. See the hub for the other aspects (roles & list, create, edit, 2FA, delete, force sign out).

# Staff — permissions tree

## Purpose

Documents the **Access permissions** section that appears on the Create and Edit modals (moderators only — the owner doesn't get this section because the owner has everything by default). Covers the hierarchical tree shape, greyed-out nodes, the `backups` permission's plan-gating, why adding moderators stays with the owner, and the API-side permission middleware.

## Where to find it

Inside the Create or Edit modal on Settings → Staff, in the **Access permissions** section (third / fourth section depending on mode). Only visible when the row being edited has `type_code === 'moderator'`.

## What the merchant can do here

- Grant or revoke a moderator's access to specific admin-panel sections via checkboxes.
- Use parent checkboxes to grant the whole sub-tree at once (e.g., checking "Settings" grants all settings sub-pages).
- See greyed-out (disabled) permissions that the acting user themselves does not hold.

## Settings & fields

### The permission tree

The tree is a fixed list of about 96 rows built into the platform, covering every sidebar section and sub-page:

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

### The owner sets a moderator's access

The owner has the full tree fully enabled and is the one who sets a moderator's access. For anyone else who opens the tree, permissions they do not hold are visible (so the full hierarchy shows) but greyed out.

Practical implication: there is no admin-tier between owner and moderator. `settings.admins.all` opens the Staff page for a moderator; saving another moderator's record stays with the owner (*"This is a restricted area!"*).

### `backups` permission node is plan-gated for the form, not for the moderator already holding it

If a moderator was created on a plan that included Backups and that permission was granted, then the merchant downgrades to a plan without Backups, **the moderator keeps the permission row in the database**. The form simply removes the Backups node from the tree when re-editing — so the merchant cannot un-tick it through the UI (it isn't visible), and they cannot add it to a different moderator.

The dormant permission is harmless because access to the Backups feature is also independently gated by the plan check elsewhere in the platform — so the moderator effectively cannot use it even though the row exists. To clear it, the merchant must upgrade back to a plan that includes Backups, re-open the moderator, un-tick the box, then downgrade again.

### Adding moderators is the owner's

The tree has no separate "create moderator" row, and the **Add moderator** button shows to the store owner only, whatever a moderator holds on the staff section. A moderator's own access is not editable by that moderator: the "my profile" modal from the profile menu has no permissions box.

### The staff screen itself

Listing, editing and deleting staff need the **Settings** box or the **Staff** row (`settings`, `settings.admins.all`); without either the staff screen is refused. The owner holds everything.

### Ticking and unticking boxes

Ticking a box ticks every box under it, and the saved list holds that box and all of them. Unticking a box also clears the box directly above it (one level only); ticking every box under a parent ticks the parent again. So a moderator given **Orders** minus one row keeps the other Orders rows but no longer holds **Orders** itself.

### Orders → Returns and Credit notes

Under **Orders** the tree lists **Orders** (with **Orders Export**), **Abandoned**, **Invoices** (with **Invoices Download** and **Invoices Export**), **Returns**, **Credit notes** (a group holding a **Credit notes** list row and **Credit notes Download**), **Refund**, **User Files** and **Ordered Products** (with **Ordered Products Export**). These are the English names; the Bulgarian ones come from the admin's translations.

| Screen | In the menu with | The screen and its actions need |
|---|---|---|
| **Returns** (`/admin/orders/returns`) | **Orders** or **Returns** | **Orders** and **Returns** |
| **Credit notes** (`/admin/orders/credit-notes`) | invoicing switched on, plus **Orders**, the **Credit notes** group or its list row | **Orders** and the **Credit notes** list row |

Downloading credit notes in bulk is a two-factor-verified action that **Orders**, the **Credit notes** group or **Credit notes Download** each allow.

Without the needed boxes the menu item is hidden. Opening the address directly shows the admin's 403 page, *"You don't have permissions to visit this page"*, as soon as the list is refused. Because unticking any row directly under Orders clears **Orders**, such a moderator can see **Returns** in the menu and still land on the 403 page. Returns and Credit notes open only with the **Orders** box itself ticked.

### Saved as a flat list

The tree is saved as a flat list of the ticked rows. A row the platform adds later is not given to existing moderators; the owner ticks it.

## Related

- [[settings-staff]] — hub.
- [[settings-staff-create-moderator]] — where the permissions tree first appears for new moderators.
- [[settings-staff-edit-profile]] — where the permissions tree appears for existing moderators.
- [[settings-backups]] — the `backups` plan-feature that gates the `backups` permission node.
- [[plan-gates]] — concept page on how plan-features gate UI.
- [[merchant-roles]] — Administrator vs Moderator role types.

## Open questions

- Is re-enabling the commented-out `settings.admins.create` permission node on the roadmap, or is "only the owner can create moderators" an intentional product decision? (verify)
- The Bulgarian names of the rows: they come from the admin's translations, not the code.
