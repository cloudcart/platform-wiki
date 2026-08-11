---
type: feature
nav_path: "Settings → Staff → Roles & staff list"
route_name: staff.settings.new
route_path: /admin/settings-new/staff
aliases: ["Staff list", "Roles", "Administrator vs Moderator", "Staff table"]
tags: [settings, staff, roles, list]
plan_gates: ["administrators"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-staff]]. See the hub for the other aspects (create, edit, permissions, 2FA, delete, force sign out).

# Staff — roles & staff list

## Purpose

Documents the two role types that exist in the platform (`owner` and `moderator`), the columns and sort behaviour of the staff list table on Settings → Staff, and the URL-hash deep-linking that lets the merchant arrive directly on Edit / Create modals.

## Where to find it

Sidebar → Settings → **Staff**. The table occupies the whole page; everything else (Add, Force sign out, Edit) opens on top of it.

## What the merchant can do here

- See every staff member (owner + all moderators) in one list.
- Sort by username, email, or last-updated.
- Click any row to open the Edit modal (see [[settings-staff-edit-profile]]).
- Bookmark a filtered / sorted view (filters and sort live in the URL query string).
- Arrive on the page via `#user-<id>` to auto-open Edit, or `#create-<hash>` to auto-open Create (see Deep-linking below).

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
- The owner is set at store registration on CloudCart; there is **no UI control to transfer ownership** in the admin panel. The API rejects any PATCH that tries to change another admin's `type` to `owner`. Practical implication: business sales / staff transitions that require ownership transfer require CloudCart support to intervene.
- The owner row appears in the table like any other staff member but has reduced affordances: no delete button, restricted edit (non-owner users cannot edit it), and the modal shows extra read-only sections (Connected social accounts).

### URL hash deep-linking on mount

When the page mounts, it inspects `window.location.hash`:

- `#user-<numeric_id>` — finds that user in the loaded table and opens the Edit modal directly with their record. The hash is stored in `hash.value` (used by some 2FA flows).
- `#create-<some_hash>` — opens the Create modal directly with that hash. **This bypasses the 2FA modal UI on the client side** — but the server still validates the hash against the `create_moderator` 2FA action, so a forged or expired hash will fail at submit. The mechanism exists to support email links like *"finish creating moderator X"* sent during multi-step onboarding flows. See [[settings-staff-create-moderator]] for the hash lifecycle.

When the Edit/Create modal is closed, the hash is cleared so a later refresh doesn't re-open it.

### Plan-limit indicator on the page header

The page header surfaces the current `administrators` plan-feature usage (used vs allowed). When `used >= allowed`, the **Add moderator** button opens the [[plan-features]] upgrade modal instead of starting the 2FA flow. The owner counts toward the cap. See [[settings-staff-create-moderator]] for the upsell modal.

## Related

- [[settings-staff]] — hub.
- [[merchant-roles]] — concept page on Administrator vs Moderator vs Customer vs Subscriber.
- [[staff-member]] — entity page for the Moderator/Administrator entity model.
- [[plan-features]] — the upgrade modal triggered when the seat cap is hit.

## Open questions

None.
