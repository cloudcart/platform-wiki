---
type: feature
nav_path: "Marketing → Campaigns → Archived → Actions"
route_name: campaigns-archived
route_path: /admin/marketing-new/campaigns/archived
aliases: ["Archive icon", "Unarchive icon", "Delete campaign icon", "Bulk delete campaigns", "Campaign archive endpoint", "archive/{id}/{action}"]
tags: [marketing, campaigns, archive, actions, bulk-delete]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-archive]]. See the hub for the other aspects (the tab, triggers, unarchive/restore, delete cascade).

# Archived campaigns — actions and endpoints

## Purpose

This page documents the actions-column affordances on the campaign list as they relate to archiving: the **Archive** and **Unarchive** icons (which fire with no confirmation against a single endpoint), the **Delete** inline-confirm panel, and the **bulk-delete** bar that only appears on the Archived tab. It also gives the exact endpoints behind each action.

## Where to find it

The actions cell at the right of each campaign row, on the relevant tab:

- **Archive** icon — on the Active / Inactive / Draft tabs.
- **Unarchive** + **Delete** icons — on the Archived tab (`/admin/marketing-new/campaigns/archived`).
- **Bulk-delete** bar — at the bottom of the page, Archived tab only.

## What the merchant can do here

- **Archive** an Active / Inactive / Draft campaign (one click, no confirm) — moves it to the Archived tab.
- **Unarchive** an archived campaign (one click, no confirm) — moves it back to the Inactive tab. See [[campaigns-archive-unarchive-restore]].
- **Delete** an archived campaign via an inline confirm panel — permanently removes it. See [[campaigns-archive-delete-cascade]].
- **Bulk-delete** multiple selected archived campaigns at once.

## Settings & fields

### The archive / unarchive / delete endpoints

| Endpoint | Method | Route path | What it does |
|----------|--------|------------|--------------|
| `admin.api.campaigns.archive` | GET | `/admin/api/core/marketing/campaigns/archive/{id}/{action}` | `action=1` archives, `action=0` unarchives — a **single** endpoint, not two separate routes. |
| `admin.api.campaigns.destroy` | DELETE | `/admin/api/core/marketing/campaigns/{id}` | Soft-delete a single archived campaign. |
| (bulk delete) | POST | `/admin/api/core/marketing/campaigns/delete` | Bulk soft-delete the selected archived campaigns. |

### Actions column on the archived tab

The Archived tab's actions column has three icons (instead of the Active tab's two), each rendered with a hover tooltip via `CcTooltip`:

| Icon | Tooltip | Action |
|------|---------|--------|
| `fa-light fa-copy` | *"Copy campaign"* | One-click copy — generally not surfaced for archived rows; the merchant should unarchive first if they want to duplicate. |
| `fa-light fa-inbox-out` | *"Unarchive campaign"* | One-click unarchive |
| `fa-light fa-trash-alt` (inside `CcDeleteComponent`) | *"Remove campaign"* | Inline confirm *"Remove campaign?"* with two-step **Cancel** / **Delete** picker |

On non-archived tabs (Active / Inactive / Draft), the actions column shows the Copy icon plus `fa-light fa-inbox-in` (*"Archive campaign"*, one-click archive, no confirmation).

## Business rules

### Archive — no confirm modal

Clicking the **Archive** icon fires directly with no confirmation:

1. The icon's loading state activates (`opacity-60 pointer-events-none`).
2. `GET /admin/api/core/marketing/campaigns/archive/{id}/1` is called (the trailing `1` is the action: 1 = archive, 0 = unarchive).
3. **On success:** toast *"Archived successfully"*, the row is optimistically removed from the current tab, the tab refetches.
4. **On error:** the icon's loading state clears; the error toast surfaces.

### Unarchive — no confirm modal

Same pattern as Archive, but with action code `0`:

1. `GET /admin/api/core/marketing/campaigns/archive/{id}/0`
2. On success: toast *"Unarchived successfully"*, row removed from the Archived tab.

The unarchived campaign reappears on the **Inactive** tab (because `active=0` is preserved) — see [[campaigns-archive-unarchive-restore]] for why it doesn't return Active.

### Delete — `CcDeleteComponent` inline confirm

Only available on the Archived tab. The delete affordance uses `CcDeleteComponent`, which expands the trash icon into an inline two-button confirm panel:

- Label: *"Remove campaign?"*
- Buttons: Cancel + Delete.
- On Cancel: collapses back to the trash icon.
- On Delete: calls `DELETE /admin/api/core/marketing/campaigns/{id}` → on success toasts *"Campaign deleted successfully."*, removes the row, refetches. On error: surfaces the error toast.

The cascade behaviour behind delete is on [[campaigns-archive-delete-cascade]].

### Bulk delete — Archived tab only

The campaigns list page sets `ignore-default-bulk-action: !isArchivedTab` — meaning the `CcTable`'s default bulk-action bar is enabled only on the Archived tab. Selecting multiple rows shows the bulk-delete bar at the bottom of the page. Clicking the bulk delete button calls `POST /admin/api/core/marketing/campaigns/delete` (the `delete-default-bulk-action-url` prop) with the array of selected IDs. On success, the `onSuccessBulkDelete` callback refetches the current tab. The Active / Inactive / Draft tabs do not expose this bar — the merchant must archive first to bulk-delete.

## Related

- [[marketing-campaigns-archive]] — hub.
- [[campaigns-archive-unarchive-restore]] — what unarchive restores the campaign to.
- [[campaigns-archive-delete-cascade]] — what delete / bulk-delete cascade-removes.
- [[campaigns-archive-triggers]] — manual archive vs auto-archive on completion.
- [[marketing-campaigns]] — parent campaign list.
- [[campaign]] — Campaign entity with `archived_at` / `deleted_at`.

## Open questions

None.
