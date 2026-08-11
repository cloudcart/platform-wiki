---
type: feature
nav_path: "Marketing → Campaigns → Row actions"
route_name: campaigns-archived
route_path: /admin/marketing-new/campaigns/archived
aliases: ["Campaign row actions", "Archive campaign action", "Copy campaign action", "Delete campaign action", "Bulk delete campaigns"]
tags: [marketing, campaigns, list, actions, bulk]
plan_gates: ["campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-campaigns]]. See the hub for the other aspects (tabs & filters, create modal, AI assistant, types & actions, rules, execution internals).

# Campaigns — row actions and bulk delete

## Purpose

This aspect catalogues every action exposed in the row-actions column of the [[marketing-campaigns]] list (archive / unarchive, copy, delete) and the **bulk delete** bar that shows only on the Archived tab. Each affordance has a specific confirmation pattern and toast vocabulary.

## Where to find it

The actions column is the right-most column of the campaigns table on any of the four status-tab routes (`campaigns-active`, `campaigns-inactive`, `campaigns-archived`, `campaigns-draft`). The bulk-delete bar appears at the bottom of the table on `campaigns-archived` only.

## What the merchant can do here

### Status toggle (inline)

- Toggle a campaign's status inline via the Active/Inactive switch in the Status column.
- The toggle is **hidden on the Archived tab**.

### Archive / Unarchive

- Available on every non-archived row (Active / Inactive / Draft tabs).
- Fires directly when clicked — **no confirm modal**.
- Success toasts: *"Archived successfully"* / *"Unarchived successfully"*.
- The optimistic UI removes the row from the current tab and refetches.
- See [[marketing-campaigns-archive]] for the underlying endpoint behaviour.

### Copy

- Available on every row.
- **No confirm** — clicking immediately calls `GET /admin/api/core/marketing/campaigns/copy/{id}`.
- On success: toasts *"Campaign copied successfully."* and navigates to `campaigns-edit/{type}/{newId}?edit=1`.
- See [[marketing-campaigns-copy]] for full details on what is/isn't preserved (steps, message templates, segment binding, statistics).

### Delete (Archived tab only)

- The Delete icon appears **only on the Archived tab**.
- Opens an inline *"Remove campaign?"* confirm.
- On confirm, calls `DELETE /admin/api/core/marketing/campaigns/{id}`, toasts *"Campaign deleted successfully."*, removes the row from the table. On error, toast surfaces the error message.
- Soft-delete + cascade — see Business rules below.

### Bulk delete (Archived tab only)

- The CcTable wrapper auto-renders a bulk-delete action when `ignore-default-bulk-action = false`, which is true ONLY when `routeName === 'campaigns-archived'`.
- Selecting multiple rows on the Archived tab shows the bulk action bar at the bottom.
- Clicking Delete calls `POST /admin/api/core/marketing/campaigns/delete` with the selected IDs.
- Other tabs hide bulk actions entirely.

## Settings & fields

The row-action affordances are wired to fixed endpoints — no merchant-configurable settings.

| Affordance | Endpoint | Confirm? | Tab visibility |
|------------|----------|----------|----------------|
| Status toggle | (inline `active` field PATCH) | No | All except Archived |
| Archive | (single archive endpoint) | No | Non-archived tabs |
| Unarchive | (single unarchive endpoint) | No | Archived tab |
| Copy | `GET /admin/api/core/marketing/campaigns/copy/{id}` | No | All tabs |
| Delete | `DELETE /admin/api/core/marketing/campaigns/{id}` | Yes (inline) | Archived only |
| Bulk delete | `POST /admin/api/core/marketing/campaigns/delete` | (selection-level) | Archived only |

## Business rules

### Archive available on every non-archived row — no Active-state guard

The archive action is exposed in the row action column on every non-archived tab (Active / Inactive / Draft). The archive endpoint requires only that the campaign is `notArchived` — there is **no Active-state guard**, so a running Active campaign can be archived in one click. (A legacy error string *"You must stop the campaign before you can archive it"* exists in the language files but is not currently enforced by any controller.)

### Soft-delete + cascade

Deleting a campaign is a **soft-delete**. Permanent deletion cascades to actions, action templates, action logs, and detaches all subscribers. The bulk-delete endpoint goes the soft route.

### Plan-quota frees only on permanent delete

Permanent-deleting an Archived campaign frees a slot against the plan-tier quota. Archiving or Inactivating does **NOT** free a slot — the quota counts every non-deleted campaign including Drafts, Inactive, and Archived. See [[campaigns-list-rules]].

### Soft-deleted titles become re-usable

The `unique:campaigns,title` validator excludes soft-deleted rows. So if a merchant deletes a campaign, the title is free to reuse on the next create. See [[campaigns-list-rules]] for the title-uniqueness scope.

### Status toggle visibility

The Active/Inactive switch in the Status column is **hidden on the Archived tab** because an archived campaign cannot be toggled — it must be unarchived first.

## Related

- [[marketing-campaigns]] — hub.
- [[marketing-campaigns-archive]] — archive / unarchive endpoint details.
- [[marketing-campaigns-copy]] — copy-flow details (what's preserved).
- [[campaigns-list-tabs-and-filters]] — why bulk delete shows only on Archived (`routeName` check).
- [[campaigns-list-rules]] — quota frees only on permanent delete; title-uniqueness scope.

## Open questions

None.
