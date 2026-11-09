---
type: feature
nav_path: "Marketing → Campaigns → Draft → Lifecycle actions"
route_name: campaigns-draft
route_path: /admin/marketing/campaigns/draft
aliases: ["Campaign row actions", "Archive Draft", "Delete Draft", "Soft delete vs hard delete campaign", "Plan campaign quota", "Subscribers retained on stop", "Mid-funnel resume"]
tags: [marketing, campaigns, draft, lifecycle, archive, delete, copy]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Draft tab, Inactive tab, entry paths, unsaved-changes guard, pre-flight checks).

# Draft / Inactive campaigns — lifecycle row actions

## Purpose

The row actions on the Draft and Inactive tabs — **Edit** (row click), **Copy**, **Archive**, plus **Delete** once archived — behave subtly differently depending on which tab the row is on, the campaign's enrolment state, and whether the platform considers it a soft-delete or a permanent delete. This page catalogues:

- The per-tab availability of each action.
- The soft-delete vs hard-delete distinction.
- The plan-quota consequences of each action.
- The **subscriber-retention** rules on stop / resume (because they shape what "Inactive" actually preserves).

## Where to find it

Row actions cell on either tab:

- [[campaigns-draft-tab|Draft tab]] (`/admin/marketing/campaigns/draft`) — Edit, Copy, Archive.
- [[campaigns-draft-inactive-tab|Inactive tab]] (`/admin/marketing/campaigns/inactive`) — Edit, Copy, Archive + Status switch (Automated only).

## What the merchant can do here

- **Edit** — opens [[marketing-campaigns-edit|the editor]]. On Draft, in editable mode; on Inactive, read-only (as for any non-draft campaign).
- **Copy** — clones the campaign to a new Draft via [[marketing-campaigns-copy]] — see [[campaigns-draft-entry-paths]] for entry semantics.
- **Archive** — moves the row to [[marketing-campaigns-archive]]. Works on both tabs directly.
- **Delete** — not offered on these tabs: delete works only on an archived campaign, so archive first.

## Settings & fields

### Per-tab action availability

| Action | Draft tab | Inactive tab | Notes |
|--------|-----------|--------------|-------|
| Edit | Editable mode | Read-only | Row click passes `query: {edit: '1'}` only when `row.draft === true`. |
| Copy | Yes | Yes | Always clones to new Draft, regardless of source state — see [[campaigns-draft-entry-paths]]. |
| Archive | Yes (no extra steps) | Yes (natural archive source) | Archive endpoint only checks `notArchived` — no Active-state guard. |
| Delete | No — archive first | No — archive first | Delete works only on an archived campaign. |
| Status switch | Hidden (*"Draft"* badge) | **Automated** only — switches back on (pre-flight, see [[campaigns-draft-preflight-checks]]); **Regular** shows a read-only progress badge | Drafts cannot toggle directly — see [[campaigns-draft-tab]]. |

### Soft vs hard delete

The platform uses a **two-stage delete**:

| Stage | Trigger | Effect |
|-------|---------|--------|
| **Soft delete** | Click Delete in row actions on the Archived tab | Sets `deleted_at = now`; row stays in the DB; vanishes from the tab. |
| **Hard delete (cascade cleanup)** | Second permanent delete from Archived (`campaigns.delete` endpoint) | Removes the campaign + cascades to actions, templates, logs, and `subscriber_to_campaigns` pivot rows. |

The cascade cleanup (actions, templates, logs, subscribers) only fires on the **second** permanent delete — after `deleted_at` is already set.

### Archive endpoint laxity

The archive endpoint requires only that the campaign is `notArchived` — there is no Active-state guard. So a running Active campaign can be archived in one click without first toggling it Inactive, and a Draft can be archived directly even though it has never been started. A legacy error string *"You must stop the campaign before you can archive it"* exists in the language files but is **not currently enforced** by the controller.

## Business rules

### Drafts count toward the plan campaign quota

Every Draft campaign in the store consumes one slot from the merchant's plan-tier campaign limit, even though it's never been started and has no enrolled subscribers. A merchant who creates 5 drafts to test ideas, then never starts any of them, is still using 5 of their plan's campaign slots.

**To free quota**, the merchant must **permanently delete** the drafts (not just archive). Delete is not offered on the Draft tab, so a draft is archived first and deleted from the Archived tab. Archived drafts that haven't been hard-deleted still occupy a quota slot.

### Inactive campaigns retain enrolled subscribers — dropped steps are not resumed

When a previously-Active campaign is flipped to Inactive (by its Status switch, or by a manual channel switch-off — see [[marketing-channels-cross-lifecycle]]), the `subscriber_to_campaigns` pivot rows stay intact. Only **Automated** campaigns can be switched back on, one by one; **Regular** campaigns cannot be re-activated from the UI. When an Automated campaign is re-activated:

- **Steps that came due while it was stopped** (or while its channel was off) were dropped and are **not** re-created; the campaign stays *"Executing"*.
- **Subscribers who already completed a step** are never re-sent it.
- **New subscribers** entering the trigger segment after re-activation join the campaign at step 1 normally.

### Inactive campaign statistics keep accruing

Even though the campaign isn't sending, the hourly campaign-statistics aggregation continues to update `reached` / `orders` / `turnover` if new attribution activity arrives (e.g., a customer who got the campaign last week places an order today). See [[campaigns-draft-inactive-tab]].

### Inactive→Archive doesn't lose history

Archiving an Inactive campaign moves it to [[marketing-campaigns-archive]] but the soft-delete state is separate from the archive state — the row is still recoverable until the hard-delete from Archived. Statistics / logs / enrolled subscribers remain readable in the Archived view.

### Deletion order matters for quota recovery

The quota is recovered only at hard-delete (cascade cleanup). The typical merchant flow for quota recovery is:

1. Archive the campaign (Delete is not offered on the Draft / Inactive tabs).
2. Delete it from the Archived tab; the slot is freed once the cascade cleanup runs.

### Copy always clones to Draft

Copy is available on every tab, Archived included. Regardless of source state, the clone is `active=2` (Draft) with the original title + *" - Copy"* suffix. See [[campaigns-draft-entry-paths]].

### Inactive campaigns are read-only in the editor

The editor is read-only for any non-draft campaign, and re-activating does not change that. The Draft-tab row click passes `query: {edit: '1'}` (because `row.draft === true`); the Inactive-tab click does not. To change an Inactive campaign, copy it to a new Draft — see the duplicate-send caveat on [[campaigns-copy-state-and-quota]].

### Anti-spam policy gate

Required for every campaign endpoint — see [[marketing-campaigns-policy]].

### Permissions

Standard campaign permission applies for all row actions.

## Related

- [[marketing-campaigns-draft]] — hub.
- [[campaigns-draft-tab]] — Draft tab where these actions surface.
- [[campaigns-draft-inactive-tab]] — Inactive tab; same actions + Status switch (Automated only).
- [[campaigns-draft-entry-paths]] — how Copy / Create / Predefined all yield a Draft.
- [[campaigns-draft-preflight-checks]] — Status toggle on Inactive runs the activation pre-flight.
- [[marketing-campaigns-archive]] — Archived tab; the natural archive target.
- [[marketing-campaigns-copy]] — Copy clone flow.
- [[marketing-campaigns-edit]] — editor; Edit row action opens it.
- [[marketing-campaigns-statistics]] — Statistics screen (still updates for Inactive).
- [[marketing-campaigns-statistics-log]] — Logs screen.
- [[marketing-channels]] — a manual channel switch-off drives some Inactive landings.
- [[marketing-campaigns-policy]] — anti-spam gate.
- [[campaign]] — Campaign entity.
- [[plan-gates]] — campaign quota plan-tier feature.

## Open questions

No outstanding questions.
