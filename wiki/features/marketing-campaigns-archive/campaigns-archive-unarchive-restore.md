---
type: feature
nav_path: "Marketing → Campaigns → Archived → Unarchive"
route_name: campaigns-archived
route_path: /admin/marketing/campaigns/archived
aliases: ["Unarchive campaign", "Unarchive restores previous status", "Restore archived campaign", "Restart completed campaign", "Clone to restart"]
tags: [marketing, campaigns, archive, unarchive, restore]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-campaigns-archive]]. See the hub for the other aspects (the tab, actions, triggers, delete cascade).

# Archived campaigns — what unarchive restores

## Purpose

Unarchiving is not a "restart" button. This page documents what state a campaign returns to when the merchant unarchives it — **the status and progress it had when archived, unchanged** — why it sends nothing more, and the caveat for Regular campaigns that auto-archived on completion: unarchiving them is only a viewing convenience.

## Where to find it

Sidebar → **Marketing** → **Campaigns** → **Archived** tab → the **Unarchive** icon on a campaign row (see [[campaigns-archive-actions]] for the icon + endpoint). After unarchiving, find the campaign on the tab its status points to — Active, Inactive (see [[marketing-campaigns-draft]]) or Draft.

## What the merchant can do here

- **Unarchive** a campaign to bring it back into the list (it lands on the tab of its unchanged status).
- Switch an unarchived **Automated** campaign on again from its Status switch, if it is off. A **Regular** campaign has no switch and cannot be re-activated from the UI.
- For an auto-completed Regular campaign, **Copy** it to send to a new audience rather than expecting unarchive to resume it (see the duplicate-send caveat on [[campaigns-copy-state-and-quota]]).

## Settings & fields

Unarchive clears `archived_at = NULL` and saves. It does **not** touch `active`, and it leaves `progress` and statistics untouched. The campaign's `active` value is preserved, so it reappears on the matching tab: `1` → Active, `0` → Inactive, `2` → Draft.

## Business rules

### Archive stops the remaining sends; unarchive does not resume them

Archiving only sets the archive date, with no status check. Every later campaign job checks that flag and drops itself, so archiving stops the remaining sends (messages already queued to the email sender still go out).

Unarchiving only clears the archive date — it changes neither `active` nor `progress`. The per-subscriber jobs dropped while archived are never re-created, so a campaign archived while executing returns to **Active, "Executing"** and sends nothing more.

### Unarchive restores `archived_at = null` but leaves `progress` and statistics untouched

When a Regular campaign completed and auto-archived (`progress = completed`, `archived_at` set), unarchiving clears `archived_at` but leaves `progress = completed` in place. A completed Regular campaign has `active = 1`, so it returns to the **Active** tab showing "Completed" — not to the Inactive tab — and nothing is re-sent. The merchant must clone the campaign (Copy) to send to a new audience. Unarchiving a completed Regular campaign is therefore only a **viewing convenience**, not a "restart" mechanism.

Automated campaigns are never marked completed. Once unarchived and on, subscribers newly entering the trigger enrol again, but steps that came due while the campaign was archived are not re-created.

### The unarchive endpoint enforces the lifecycle

Unarchive requires the campaign to be archived (`archived_at IS NOT NULL`); the endpoint 404s otherwise. See [[campaigns-archive-actions]] for the `archive/{id}/0` endpoint detail.

## Related

- [[marketing-campaigns-archive]] — hub.
- [[campaigns-archive-actions]] — the Unarchive icon + `archive/{id}/0` endpoint.
- [[campaigns-archive-triggers]] — how the campaign got archived (manual vs auto-complete).
- [[marketing-campaigns-draft]] — the Inactive / Draft tabs a campaign with that status returns to.
- [[marketing-campaigns-copy]] — Copy a completed Regular campaign to send to a new audience.
- [[marketing-campaigns]] — parent campaign list.
- [[campaign]] — Campaign entity with `archived_at`, `active`, `progress`.

## Open questions

None.
