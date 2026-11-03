---
type: feature
nav_path: "Settings → Staff → Roles & staff list"
route_name: staff.settings
route_path: /admin/settings/staff
aliases: ["Staff list", "Roles", "Administrator vs Moderator", "Staff table"]
tags: [settings, staff, roles, list]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[settings-staff]]. See the hub for the other aspects (create, edit, permissions, 2FA, delete, force sign out).

# Staff — roles & staff list

## Purpose

Documents the two role types that exist in the platform (`owner` and `moderator`), the columns and sort behaviour of the staff list table on Settings → Staff, and the URL-hash deep link that opens one account's Edit modal.

## Where to find it

Sidebar → Settings → **Staff**. The table occupies the whole page; everything else (Add, Force sign out, Edit) opens on top of it.

## What the merchant can do here

- See every staff member (owner + all moderators) in one list.
- Sort by username, email, or last-updated.
- Click any row to open the Edit modal (see [[settings-staff-edit-profile]]).
- Bookmark a filtered / sorted view (filters and sort live in the URL query string).
- Arrive on the page via `#user-<id>` to auto-open Edit (see Deep-linking below).

## Settings & fields

### Staff list table

| Column | Notes |
|--------|-------|
| **Username** | Custom-rendered (`SettingsStaffUsername` component — shows username with the avatar). Sortable. *"This name is visible on your site"* — the username appears in places where the staff member is visible to customers (e.g., blog post author). |
| **Email** | Sortable. |
| **Address** | Computed server-side as `<country>, <city>, <street>, <postal_code>`. Empty values are skipped. Not sortable. |
| **Phone Number** | Comes from `info.phone`. Not sortable. |
| **Last updated** | Date rendered. Sortable. **Default sort: `id` descending** (newest first). |
| **Actions** | Per-row delete button. See [[settings-staff-delete]] for visibility rules. |

The table supports filters, search, page size, and sorting — all driven by URL query string, so a merchant can bookmark a filtered view.

## Business rules

### Only two staff role types exist — owner and moderator

There are exactly **two role types** in the platform: `owner` and `moderator`. No custom roles, no "admin" tier between owner and moderator, no role templates. The owner is a singleton per store; everyone else is a moderator. Permission granularity is achieved via the per-section checkbox tree (see [[settings-staff-permissions-tree]]) — not via named roles. So a "viewer" or "warehouse staff" or "support agent" persona is created by giving a moderator a curated subset of permissions, not by selecting a role.

### Owner row identification and immutability

- `type_code === 'owner'` identifies the owner row (used by the UI to hide the delete button and to flip the modal title from "Edit moderator" to "Edit admin").
- The owner is set at store registration on CloudCart; there is **no UI control to transfer ownership** in the admin panel. Practical implication: business sales / staff transitions that require ownership transfer require CloudCart support to intervene.
- The owner row appears in the table like any other staff member but has reduced affordances: no delete button, restricted edit (non-owner users cannot edit it), and the modal adds the owner's Google account card (see [[settings-staff-edit-profile]]).

### URL hash deep-linking on mount

`#user-<numeric_id>` in the address opens that account's Edit modal once the list has loaded. The admin returns this way after connecting a Google account.

### Plan limit and the header buttons

**Add moderator** and **Force sign out** show to the store owner only. The list brings the plan's `administrators` limit with it, and adding or deleting a moderator keeps the used count current without a reload. When the used count has reached the limit, **Add moderator** opens the [[plan-features]] upgrade modal instead of starting the 2FA flow. The owner counts toward the cap. See [[settings-staff-create-moderator]] for the upsell modal.

## Related

- [[settings-staff]] — hub.
- [[merchant-roles]] — concept page on Administrator vs Moderator vs Customer vs Subscriber.
- [[staff-member]] — entity page for the Moderator/Administrator entity model.
- [[plan-features]] — the upgrade modal triggered when the seat cap is hit.

## Open questions

None.
