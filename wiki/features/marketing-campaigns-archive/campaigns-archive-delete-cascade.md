---
type: feature
nav_path: "Marketing → Campaigns → Archived → Delete cascade"
route_name: campaigns-archived
route_path: /admin/marketing-new/campaigns/archived
aliases: ["Delete archived campaign", "Soft delete campaign", "Permanent delete campaign", "Campaign delete cascade", "Plan quota campaign delete", "Statistics survive campaign delete"]
tags: [marketing, campaigns, archive, delete, cascade, plan-quota]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-archive]]. See the hub for the other aspects (the tab, actions, triggers, unarchive/restore).

# Archived campaigns — delete cascade and what survives

## Purpose

Deleting a campaign is the only way to permanently remove it, and it's only callable on the Archived tab. This page documents the two-phase soft-delete → permanent-delete pattern, exactly what the cascade removes from the campaign's main records, what survives in the separate statistics/log store (and why), and the one business consequence merchants most need to know: only a permanent delete frees a plan-tier campaign slot.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **Archived** tab → the **Delete** inline-confirm panel, or the **bulk-delete** bar after multi-selecting rows. See [[campaigns-archive-actions]] for the affordances and endpoints.

## What the merchant can do here

- **Delete** a single archived campaign (inline confirm) — permanently removes it and cascades cleanup.
- **Bulk-delete** multiple archived campaigns at once.
- **Free a plan-tier campaign slot** — permanent delete is the only action that does this.

## Settings & fields

### Archive vs Delete: what's preserved

| Action | Campaign record | Actions | Action templates | Action logs | Subscriber links | Statistics |
|--------|--------------|---------|------------------|-------------|------------------|------------|
| **Archive** | Stays (with `archived_at`) | Kept | Kept | Kept | Kept | Kept |
| **Unarchive** | Stays (`archived_at=NULL`) | Kept | Kept | Kept | Kept | Kept |
| **Delete** (from archived tab) | Soft-deleted (`deleted_at` set) | Deleted on permanent delete | Deleted on permanent delete | Deleted on permanent delete | Detached on permanent delete | Statistics live in a separate store (not auto-cleaned) |

(Archive / unarchive behaviour is detailed on [[campaigns-archive-triggers]] and [[campaigns-archive-unarchive-restore]].)

## Business rules

### Delete is only callable on archived campaigns

The delete endpoint finds the campaign filtered to `archived_at IS NOT NULL`. A non-archived campaign returns 404 when the merchant hits the delete endpoint. So the only way to permanently delete a campaign is: **Stop → Archive → Delete.**

### Soft-delete then permanent delete (two phases)

Campaign deletion has two phases:

1. The first delete sets `deleted_at` to the current time (soft-delete). The campaign disappears from the normal lists but its records still exist — the campaign itself, its actions, its action templates, its action logs, and its subscriber links.
2. The cleanup cascade fires ONLY when `deleted_at` is already set — i.e., on the **second** delete (the permanent one), which removes the actions, action templates, and action logs, and detaches subscribers.

In practice the cascade runs as soon as the merchant clicks Delete on an archived row, because the soft-delete and the cascade-triggering second pass happen in the same action. For the merchant the experience is single-click "Delete" → vanish → cascade. The two-phase pattern protects against accidental permanent removal from unintended paths.

### Bulk delete

The merchant can multi-select archived campaigns and delete them en masse via `POST /admin/api/core/marketing/campaigns/delete` with an array of IDs. The action soft-deletes each campaign together (all-or-nothing); the cascade detaches subscribers and removes campaign actions / action templates / action logs. Bulk delete is available only on the Archived tab — Active / Inactive / Draft tabs don't expose it (archive first to bulk-delete).

### Statistics and send-log history are NOT auto-cleaned

The statistics store is NOT auto-cleaned on campaign delete — it retains the campaign ID reference. Even after a permanent delete, the per-(subscriber, campaign) send history survives in the send log, and the per-channel logs retain the campaign ID, for forensic / audit purposes. This is intentional.

### Per-channel log names persist in the audit trail

When a campaign is permanently deleted, the cascade also leaves the `channel_log_names` registry (which maps campaign titles + segments + channels to human-readable labels for the [[marketing-campaigns-statistics-log|logs]] screen) intact. So historical log entries from the deleted campaign still resolve to readable names rather than IDs in the per-channel logs viewer.

### Plan-tier quota only drops on permanent delete

The plan-tier campaign count includes Archived campaigns — they still have a row, so archiving does **not** free a slot. Permanent delete is what drops the count. A merchant who's at their plan ceiling and wants to create a new campaign MUST: Stop → Archive → Delete an old one. Inactivating a campaign and leaving it on the Inactive tab does not free a slot either.

### Anti-spam policy gate and permission

Delete and bulk-delete, like all campaign endpoints, are behind the campaign anti-spam policy gate ([[marketing-campaigns-policy]]). Standard campaign permission applies.

## Related

- [[marketing-campaigns-archive]] — hub.
- [[campaigns-archive-actions]] — the Delete inline-confirm + bulk-delete affordances and endpoints.
- [[campaigns-archive-triggers]] — Stop → Archive precedes Delete.
- [[marketing-campaigns-statistics-log]] — the logs screen that the surviving `channel_log_names` registry serves.
- [[marketing-campaigns-subscribers]] — subscriber links detached on permanent delete.
- [[marketing-campaigns]] — parent campaign list.
- [[campaign]] — Campaign entity with `archived_at` and `deleted_at` fields.

## Open questions

None.
