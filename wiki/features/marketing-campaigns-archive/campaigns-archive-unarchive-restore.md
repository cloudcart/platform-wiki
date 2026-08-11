---
type: feature
nav_path: "Marketing → Campaigns → Archived → Unarchive"
route_name: campaigns-archived
route_path: /admin/marketing-new/campaigns/archived
aliases: ["Unarchive campaign", "Unarchive resurrects to inactive", "Restore archived campaign", "Restart completed campaign", "Clone to restart"]
tags: [marketing, campaigns, archive, unarchive, restore]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-archive]]. See the hub for the other aspects (the tab, actions, triggers, delete cascade).

# Archived campaigns — what unarchive restores

## Purpose

Unarchiving is not a "restart" button. This page documents what state a campaign returns to when the merchant unarchives it — **Inactive, never Active** — why that's intentional, and the important caveat for Regular campaigns that auto-archived on completion: unarchiving them is mostly a viewing convenience, because the executor still treats them as completed.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **Archived** tab → the **Unarchive** icon on a campaign row (see [[campaigns-archive-actions]] for the icon + endpoint). After unarchiving, find the campaign on the **Inactive** tab (see [[marketing-campaigns-draft]]).

## What the merchant can do here

- **Unarchive** a campaign to bring it back into the rotation (it lands on the Inactive tab).
- **Manually re-Activate** the unarchived campaign via the Status toggle on the Inactive tab to start sending again.
- For an auto-completed Regular campaign, **Copy** it to send to a new audience rather than expecting unarchive to resume it.

## Settings & fields

Unarchive clears `archived_at = NULL` and saves. It deliberately does **not** touch `active`, and it leaves `progress` and statistics untouched. The campaign's `active` value (0) is preserved, so it reappears on the Inactive tab.

## Business rules

### Unarchive resurrects to INACTIVE — not active

Unarchiving clears `archived_at` but does NOT flip `active` back to 1. The campaign re-appears on the Inactive tab. The merchant must manually toggle it Active (via the Status switch on the Inactive tab) to start sending again.

This is intentional — auto-resuming a campaign whose trigger segment may have changed or whose channels may have been suspended could send stale messages to the wrong audience. The Inactive-then-manual-Active path forces a deliberate restart.

### Unarchive restores `archived_at = null` but leaves `progress` and statistics untouched

When a Regular campaign completed and auto-archived (`progress = completed`, `archived_at` set), unarchiving clears `archived_at` but leaves `progress = completed` in place. The campaign appears on the Inactive tab — but the executor knows it's already completed and will refuse to re-enrol anyone. The merchant must clone the campaign (Copy) to send to a new audience. Unarchiving a completed Regular campaign is therefore mostly a **viewing convenience** rather than a "restart" mechanism.

Automated campaigns, by contrast, were never marked completed, so unarchiving + re-Activating them resumes normal trigger enrolment.

### The unarchive endpoint enforces the lifecycle

Unarchive requires the campaign to be archived (`archived_at IS NOT NULL`); the endpoint 404s otherwise. See [[campaigns-archive-actions]] for the `archive/{id}/0` endpoint detail.

## Related

- [[marketing-campaigns-archive]] — hub.
- [[campaigns-archive-actions]] — the Unarchive icon + `archive/{id}/0` endpoint.
- [[campaigns-archive-triggers]] — how the campaign got archived (manual vs auto-complete).
- [[marketing-campaigns-draft]] — the Inactive tab the campaign returns to; re-Activate from there.
- [[marketing-campaigns-copy]] — Copy a completed Regular campaign to send to a new audience.
- [[marketing-campaigns]] — parent campaign list.
- [[campaign]] — Campaign entity with `archived_at`, `active`, `progress`.

## Open questions

None.
