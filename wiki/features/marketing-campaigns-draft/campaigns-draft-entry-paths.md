---
type: feature
nav_path: "Marketing → Campaigns → Draft → Entry paths and state machine"
route_name: campaigns-draft
route_path: /admin/marketing-new/campaigns/draft
aliases: ["Campaign status state machine", "Draft entry paths", "active=0 active=1 active=2", "How campaigns become Draft", "Campaign status transitions"]
tags: [marketing, campaigns, draft, state-machine]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Draft tab, Inactive tab, unsaved-changes guard, pre-flight checks, lifecycle actions).

# Campaigns — Draft entry paths and status state machine

## Purpose

Every campaign in CloudCart lives in exactly one of three states: **Draft** (`active=2`), **Active** (`active=1`), **Inactive** (`active=0`). The status drives which tab the campaign appears on, whether it is sending messages, and which row actions are available.

This page documents two things together:

1. The full list of **entry paths** — how a campaign becomes a Draft.
2. The **transition matrix** — which moves between the three states are legal, what triggers each transition, and where the Draft tab fits in the state machine.

The validators that fire during transitions are covered separately on [[campaigns-draft-preflight-checks]].

## Where to find it

The states are surfaced on the four-tab campaigns list ([[marketing-campaigns]]):

| State value | Label | Tab | Filter |
|-------------|-------|-----|--------|
| `2` | Draft | [[campaigns-draft-tab|Draft]] | `active=2 AND archived_at IS NULL` |
| `1` | Active | Active | `active=1 AND archived_at IS NULL` |
| `0` | Inactive | [[campaigns-draft-inactive-tab|Inactive]] | `active=0 AND archived_at IS NULL` |
| (any) | Archived | Archived | `archived_at IS NOT NULL` |

## What the merchant can do here

- **Create a Draft** — three entry paths (manual create, predefined clone, copy).
- **Move Draft → Active** — click **Start campaign** in [[marketing-campaigns-edit|the editor]] (subject to pre-flight checks).
- **Move Active → Inactive** — flip the Status toggle on the Active tab, OR a channel-suspension cascade flips it automatically.
- **Move Inactive → Active** — flip the Status toggle on the Inactive tab (subject to pre-flight checks).
- **Archive** — available from any non-archived tab via the row action (see [[campaigns-draft-lifecycle-actions]]).

## Settings & fields

### Draft entry paths

Every newly-created campaign starts as Draft (`active=2`), regardless of which entry path the merchant uses:

| Entry path | Source screen | Resulting state | Title behaviour |
|------------|---------------|-----------------|-----------------|
| **Manual create** | [[marketing-campaigns-create]] | `active=2` | Merchant-specified title (or empty). |
| **Predefined clone** | [[marketing-campaigns-from-predefined]] | `active=2` | Inherited from the predefined template. |
| **Copy** | [[marketing-campaigns-copy]] (row action on any tab) | `active=2` | Original title + *" - Copy"* suffix. |

The Draft tab is the merchant's "in-progress" workspace for everything created via any of these paths.

### Status transition matrix

| From → To | Trigger | Validator gate | Notes |
|-----------|---------|----------------|-------|
| (none) → `2` (Draft) | Create / Predefined clone / Copy | Schema-level only (title optional at create). | The only path INTO `active=2`. |
| `2` → `1` (Draft → Active) | **Start campaign** in the editor | Full pre-flight (see [[campaigns-draft-preflight-checks]]). | The only legal exit from Draft. |
| `2` → `0` (Draft → Inactive) | Editor save with `active=0` set manually | Schema only. | Not a normal flow; rare. |
| `1` → `0` (Active → Inactive) | Status toggle on Active tab; OR channel-suspension cascade. | Toggle: schema only. Cascade: automatic. | Common path; subscribers retained. |
| `0` → `1` (Inactive → Active) | Status toggle on Inactive tab. | Full pre-flight (see [[campaigns-draft-preflight-checks]]). | Enrolled subscribers resume mid-funnel. |
| Any → archived | Archive row action. | Only `notArchived` check — no Active-state guard. | See [[campaigns-draft-lifecycle-actions]]. |

### Key state-machine invariants

- **No direct path back to Draft.** Once a campaign has been started (entered Active or Inactive), `active` is `0` or `1` forever (until archived / deleted). A merchant who wants to "start over" must copy the campaign (yielding a fresh Draft) and delete the original.
- **`active=2` is reachable only at creation.** Drafts are born Draft; no transition lands here.
- **Direct toggle-endpoint Drafts are refused.** Hitting `campaigns.update_active` on a Draft returns *"Campaign was not started"* — Drafts must transition out via the editor's **Start campaign** flow. See [[campaigns-draft-preflight-checks]].

## Business rules

### Draft is born only at creation time

The three entry paths all set `active=2` at insert time. There is no editor action that *creates* a Draft from a non-Draft campaign — copying does it (because Copy spawns a NEW campaign), but no transition does.

### Predefined clones inherit content; status is forced to Draft

When a merchant picks a predefined template via [[marketing-campaigns-from-predefined]], the platform clones the template's actions / channels / messages but always sets the resulting campaign to `active=2`. The merchant must still click **Start campaign** to activate.

### Copy preserves the original's status, NOT the new clone's

[[marketing-campaigns-copy]] is available from rows on all three tabs (Draft / Active / Inactive). Regardless of which tab the source row was on, the resulting clone is `active=2` — Copy never produces an Active or Inactive duplicate. The title gets the *" - Copy"* suffix.

### Channel-suspension cascade scope is `active=1` only

When a channel auto-suspends (spam / bounce / open / cc_denied — see [[marketing-channels]]) or the merchant manually disables it, the cascade flips every campaign referencing that channel that is currently `active=1` to `active=0`. Drafts (`active=2`) and already-Inactive (`active=0`) campaigns are untouched. A Draft that references a suspended channel stays in Draft; the merchant hits the pre-flight failure only when they try to **Start campaign**.

### Status changes are auditable via the campaign-statistics log

Every transition that fires the activation cascade writes channel-log-name entries — used by [[marketing-campaigns-statistics]] and [[marketing-campaigns-statistics-log]] for human-readable labels. See [[campaigns-edit-launch-flow]] for the side-effect catalogue on `2→1`.

### Anti-spam policy gate applies to every transition

Like every campaign endpoint, the transition endpoints require [[marketing-campaigns-policy|anti-spam policy]] acceptance.

### Permissions

Standard campaign permission applies for every transition.

## Related

- [[marketing-campaigns-draft]] — hub.
- [[marketing-campaigns-create]] — Manual create entry path.
- [[marketing-campaigns-from-predefined]] — Predefined clone entry path.
- [[marketing-campaigns-copy]] — Copy entry path (available from all tabs).
- [[marketing-campaigns-edit]] — editor; **Start campaign** drives `2→1`.
- [[marketing-campaigns]] — parent four-tab list; tab routing is filter-based.
- [[campaigns-edit-launch-flow]] — the save → activate side-effect cascade on `2→1`.
- [[marketing-channels]] — channel-suspension cascade drives `1→0`.
- [[marketing-campaigns-policy]] — anti-spam gate.
- [[campaign]] — Campaign entity carries the `active` field.

## Open questions

No outstanding questions.
