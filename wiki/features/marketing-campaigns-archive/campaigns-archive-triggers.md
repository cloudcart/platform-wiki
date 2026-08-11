---
type: feature
nav_path: "Marketing → Campaigns → Archived → Triggers"
route_name: campaigns-archived
route_path: /admin/marketing-new/campaigns/archived
aliases: ["How a campaign gets archived", "Auto-archive on completion", "Manual archive", "Regular campaign auto-archive", "Stop before archive error"]
tags: [marketing, campaigns, archive, lifecycle, auto-archive]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-archive]]. See the hub for the other aspects (the tab, actions, unarchive/restore, delete cascade).

# Archived campaigns — how a campaign gets here

## Purpose

A campaign lands on the Archived tab in exactly two ways: the merchant archives it manually, or a Regular campaign auto-archives itself when it finishes. This page documents both paths, the (lack of) status checks around manual archive, and why Automated campaigns never auto-archive.

## Where to find it

The archive trigger originates either from the **Archive** action in the row actions menu on any non-archived tab (see [[campaigns-archive-actions]]) or from the campaign-execution job that completes a Regular campaign. The result lands on Sidebar → **Marketing** → **Campaigns** → **Archived**.

## What the merchant can do here

- **Manually archive** any non-archived campaign (Active / Inactive / Draft) from its row actions — one click, no confirmation.
- **Rely on auto-archive** for Regular campaigns — once they finish their single send, they move to the Archived tab on their own, with no merchant action needed.
- Recognise that **Automated campaigns will never appear here on their own** — they must be manually archived.

## Settings & fields

A campaign appears on this tab when its `archived_at` is non-null. This is set in two ways:

1. **Manual archive** — merchant clicks the Archive action on a non-archived campaign → archive flips `archived_at = now`.
2. **Auto-archive on completion** — Regular campaigns that finish their single send (no more enrolments, all subscribers processed) auto-complete, which atomically sets `progress = completed` AND `archived_at = now` in the same step.

## Business rules

### Archive is available on every non-archived tab

The Archive action is exposed in the row action column on every non-archived tab (Active / Inactive / Draft). The archive endpoint requires only that the campaign is `notArchived` — there is **no status check** preventing an Active campaign from being archived directly.

A legacy error string *"You must stop the campaign before you can archive it"* exists in the platform's language files but is **not currently enforced** by any controller — it is dead text. So a merchant can archive a running campaign in one click without stopping it first.

### Auto-archive on Regular-campaign completion

The campaign-execution job auto-completes a Regular campaign when no more subscribers remain to process and the campaign has fully drained (every enrolled customer has either completed or exited). This:

1. Sets `progress = completed`.
2. Sets `archived_at = now`.

So a Regular campaign that finishes vanishes from the Active tab and shows up on the Archived tab automatically — the merchant doesn't need to do anything.

### Auto-archive on Regular completion is silent

There is **no "completed" notification, email, or system message** — the merchant only discovers the auto-archive on the next visit to the campaigns list. The move from the Active tab to the Archived tab happens in the same hour the queue drains.

### Automated campaigns never auto-archive

Automated campaigns can run indefinitely, enrolling new subscribers as triggers fire, until the merchant manually Inactivates and Archives them. They never trigger the auto-archive path. The only way an Automated campaign reaches the Archived tab is manual archive.

### Anti-spam policy gate and permission

The archive action, like all campaign endpoints, is behind the campaign anti-spam policy gate ([[marketing-campaigns-policy]]). Standard campaign permission applies.

## Related

- [[marketing-campaigns-archive]] — hub.
- [[campaigns-archive-actions]] — the Archive icon and endpoint that fires manual archive.
- [[campaigns-archive-unarchive-restore]] — what happens when an auto-archived completed campaign is unarchived.
- [[marketing-campaigns-draft]] — the Inactive / Draft tabs a campaign leaves when archived.
- [[marketing-campaigns]] — parent campaign list.
- [[marketing-campaigns-policy]] — anti-spam policy gate.
- [[campaign]] — Campaign entity with `archived_at` and `progress`.

## Open questions

None.
