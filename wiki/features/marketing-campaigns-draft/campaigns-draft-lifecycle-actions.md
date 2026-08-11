---
type: feature
nav_path: "Marketing → Campaigns → Draft → Lifecycle actions"
route_name: campaigns-draft
route_path: /admin/marketing-new/campaigns/draft
aliases: ["Campaign row actions", "Archive Draft", "Delete Draft", "Soft delete vs hard delete campaign", "Plan campaign quota", "Subscribers retained on stop", "Mid-funnel resume"]
tags: [marketing, campaigns, draft, lifecycle, archive, delete, copy]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Draft tab, Inactive tab, entry paths, unsaved-changes guard, pre-flight checks).

# Draft / Inactive campaigns — lifecycle row actions

## Purpose

The row actions on the Draft and Inactive tabs — **Edit**, **Copy**, **Archive**, **Delete** — behave subtly differently depending on which tab the row is on, the campaign's enrolment state, and whether the platform considers it a soft-delete or a permanent delete. This page catalogues:

- The per-tab availability of each action.
- The soft-delete vs hard-delete distinction.
- The plan-quota consequences of each action.
- The **subscriber-retention** rules on stop / resume (because they shape what "Inactive" actually preserves).

## Where to find it

Row actions cell on either tab:

- [[campaigns-draft-tab|Draft tab]] (`/admin/marketing-new/campaigns/draft`) — Edit, Copy, Archive, Delete.
- [[campaigns-draft-inactive-tab|Inactive tab]] (`/admin/marketing-new/campaigns/inactive`) — Edit, Copy, Archive, Delete + Status toggle.

## What the merchant can do here

- **Edit** — opens [[marketing-campaigns-edit|the editor]]. On Draft, in editable mode; on Inactive, read-only unless the merchant re-activates first.
- **Copy** — clones the campaign to a new Draft via [[marketing-campaigns-copy]] — see [[campaigns-draft-entry-paths]] for entry semantics.
- **Archive** — moves the row to [[marketing-campaigns-archive]]. Works on both tabs directly.
- **Delete** — soft-deletes from this tab; second delete from Archived hard-deletes.

## Settings & fields

### Per-tab action availability

| Action | Draft tab | Inactive tab | Notes |
|--------|-----------|--------------|-------|
| Edit | Editable mode | Read-only unless re-activated | Row click passes `query: {edit: '1'}` only when `row.draft === true`. |
| Copy | Yes | Yes | Always clones to new Draft, regardless of source state — see [[campaigns-draft-entry-paths]]. |
| Archive | Yes (no extra steps) | Yes (natural archive source) | Archive endpoint only checks `notArchived` — no Active-state guard. |
| Delete (soft) | Yes — cascades immediately on Draft | Yes — soft-delete with pivot intact | See *Soft vs hard delete* below. |
| Status toggle | Hidden | Visible — flips to Active (subject to pre-flight, see [[campaigns-draft-preflight-checks]]) | Drafts cannot toggle directly — see [[campaigns-draft-tab]]. |

### Soft vs hard delete

The platform uses a **two-stage delete**:

| Stage | Trigger | Effect |
|-------|---------|--------|
| **Soft delete** | Click Delete in row actions on Draft / Inactive / Archived | Sets `deleted_at = now`; row stays in the DB; vanishes from the tab. |
| **Hard delete (cascade cleanup)** | Second permanent delete from Archived (`campaigns.delete` endpoint) | Removes the campaign + cascades to actions, templates, logs, and `subscriber_to_campaigns` pivot rows. |

The cascade cleanup (actions, templates, logs, subscribers) only fires on the **second** permanent delete — after `deleted_at` is already set. From the merchant's POV, single-click Delete is the soft-delete; Archived → Delete is the hard-delete.

| Tab | Delete pathway | What it removes |
|-----|----------------|-----------------|
| Draft | Soft-delete (instant cascade because there's nothing to preserve). | Row vanishes; quota recovers on hard-delete. |
| Inactive | Soft-delete; pivot rows + logs preserved for potential support-recovery. | Row vanishes from Inactive. |
| Archived | Hard-delete via `campaigns.delete`; cascade runs. | Quota slot freed; logs / pivot gone. |

### Archive endpoint laxity

The archive endpoint requires only that the campaign is `notArchived` — there is no Active-state guard. So a running Active campaign can be archived in one click without first toggling it Inactive, and a Draft can be archived directly even though it has never been started. A legacy error string *"You must stop the campaign before you can archive it"* exists in the language files but is **not currently enforced** by the controller.

## Business rules

### Drafts count toward the plan campaign quota

Every Draft campaign in the store consumes one slot from the merchant's plan-tier campaign limit, even though it's never been started and has no enrolled subscribers. A merchant who creates 5 drafts to test ideas, then never starts any of them, is still using 5 of their plan's campaign slots.

**To free quota**, the merchant must **permanently delete** the drafts (not just archive). Drafts can be soft-deleted directly from the Draft tab — that clears the slot once the cascade hard-delete runs via the model's deletion path. Archived drafts that haven't been hard-deleted still occupy a quota slot.

### Inactive campaigns retain enrolled subscribers — mid-funnel resume

When a previously-Active campaign is flipped to Inactive (manually or via the channel-suspension cascade — see [[campaigns-draft-preflight-checks]]), the `subscriber_to_campaigns` pivot rows stay intact. Subscribers mid-funnel keep their `progress` value.

When the merchant re-activates:

- **Already-enrolled subscribers** do NOT auto-restart from step 1 — they pick up where they were when the campaign stopped.
- **Timing may shift** — the worker re-evaluates next-step delays from the moment of resume, not from the original schedule.
- **New subscribers** entering the trigger segment after re-activation join the campaign at step 1 normally.

### Inactive campaign statistics keep accruing

Even though the campaign isn't sending, the hourly campaign-statistics aggregation continues to update `reached` / `orders` / `turnover` if new attribution activity arrives (e.g., a customer who got the campaign last week places an order today). See [[campaigns-draft-inactive-tab]].

### Inactive→Archive doesn't lose history

Archiving an Inactive campaign moves it to [[marketing-campaigns-archive]] but the soft-delete state is separate from the archive state — the row is still recoverable until the hard-delete from Archived. Statistics / logs / enrolled subscribers remain readable in the Archived view.

### Deletion order matters for quota recovery

The quota is recovered only at hard-delete (cascade cleanup). The typical merchant flow for quota recovery is:

1. Soft-delete from Draft / Inactive (row vanishes from that tab but the campaign still counts).
2. (Implicit) The row moves into the "soft-deleted" state — visible only in Archived if archived first, else gone from view.
3. Hard-delete from Archived → cascade fires → quota slot freed.

### Copy always clones to Draft

Copy is available on rows in all three tabs (Draft / Active / Inactive). Regardless of source state, the clone is `active=2` (Draft) with the original title + *" - Copy"* suffix. See [[campaigns-draft-entry-paths]].

### Editing Inactive requires re-activation OR a different flow

Clicking a row on the Inactive tab opens the editor in read-only mode by default — the merchant must either flip the Status toggle first (running the pre-flight — see [[campaigns-draft-preflight-checks]]) or trigger a save through a different flow. The Draft-tab row click passes `query: {edit: '1'}` (because `row.draft === true`); the Inactive-tab click does not.

### Anti-spam policy gate

Required for every campaign endpoint — see [[marketing-campaigns-policy]].

### Permissions

Standard campaign permission applies for all row actions.

## Related

- [[marketing-campaigns-draft]] — hub.
- [[campaigns-draft-tab]] — Draft tab where these actions surface.
- [[campaigns-draft-inactive-tab]] — Inactive tab; same actions + Status toggle.
- [[campaigns-draft-entry-paths]] — how Copy / Create / Predefined all yield a Draft.
- [[campaigns-draft-preflight-checks]] — Status toggle on Inactive runs the activation pre-flight.
- [[marketing-campaigns-archive]] — Archived tab; the natural archive target.
- [[marketing-campaigns-copy]] — Copy clone flow.
- [[marketing-campaigns-edit]] — editor; Edit row action opens it.
- [[marketing-campaigns-statistics]] — Statistics screen (still updates for Inactive).
- [[marketing-campaigns-statistics-log]] — Logs screen.
- [[marketing-channels]] — channel suspension cascade drives some Inactive landings.
- [[marketing-campaigns-policy]] — anti-spam gate.
- [[campaign]] — Campaign entity.
- [[plan-gates]] — campaign quota plan-tier feature.

## Open questions

No outstanding questions.
