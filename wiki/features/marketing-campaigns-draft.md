---
type: feature
nav_path: "Marketing → Campaigns → Draft"
route_name: campaigns-draft
route_path: /admin/marketing-new/campaigns/draft
aliases: ["Draft campaigns", "Saved drafts", "Inactive campaigns", "Stopped campaigns", "Чернови", "Спрени кампании", "Неактивни кампании"]
tags: [marketing, campaigns, draft, inactive]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-05-23
updated: 2026-06-10
source_count: 2
---

# Draft and Inactive campaigns

## Purpose

The **Draft** and **Inactive** tabs are the merchant's two "not running" states for a campaign — together they cover every campaign that isn't currently sending messages and isn't archived. The distinction matters:

- **Draft** (`active=2`) — a campaign that has been created but never started. It might be half-built (no segment yet, no message templates, no title) or fully configured but waiting for **Start campaign**. Drafts have never enrolled anyone; never sent anyone a message; have zero statistics.
- **Inactive** (`active=0`) — a campaign that WAS started and has now been stopped. The merchant flipped the Status toggle, or a channel-suspension cascade auto-stopped it, or a regular campaign explicitly inactivated itself. Inactive campaigns retain their full history, enrolled subscribers, and statistics — they just aren't sending right now.

The two tabs are listed separately so the merchant can quickly see "what am I still building?" (Draft) vs "what's paused that I should resume?" (Inactive). Both are still in the active rotation, just paused — distinct from [[marketing-campaigns-archive|Archived]].

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click **Draft** or **Inactive** tab.

The two tabs are separate routes with separate controllers but identical table shape:

| Tab | Route name | Route path | Filter rule |
|-----|------------|------------|-------------|
| **Draft** | `campaigns-draft` | `/admin/marketing-new/campaigns/draft` | `active = 2` AND `archived_at IS NULL` |
| **Inactive** | `campaigns-inactive` | `/admin/marketing-new/campaigns/inactive` | `active = 0` AND `archived_at IS NULL` |

The campaign list's tab control (Active / Inactive / Archived / Draft) drives these routes — all four tabs render the same list component; clicking a tab swaps the URL and re-queries the matching list endpoint.

## What the merchant can do here

- **Draft tab** — browse all in-progress campaigns; open a row to continue setup in [[marketing-campaigns-edit|the editor]]; copy / archive / delete from row actions. Statistics columns are zero. See [[campaigns-draft-tab]].
- **Inactive tab** — browse all paused-but-not-archived campaigns; flip the Status toggle to re-activate; view full historical stats; see banned-reason badges from channel-suspension cascade. See [[campaigns-draft-inactive-tab]].
- **Continue an unsaved draft** — the editor surfaces a *"Leave draft campaign?"* modal + browser `beforeunload` warning when the merchant navigates away with unsaved changes. See [[campaigns-draft-unsaved-changes-guard]].
- **Re-activate** — flipping Inactive→Active or starting a Draft re-runs the activation pre-flight checks (channel configured + active + credits + messages set + segment filtered). See [[campaigns-draft-preflight-checks]].
- **Manage the row** — archive, copy, delete behaviour differs slightly between Draft and Inactive rows. See [[campaigns-draft-lifecycle-actions]].

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[campaigns-draft-tab]] — the Draft tab itself: filter, route, columns, no-status-toggle, statistics-skip optimisation, row click opens editor in editable mode.
- [[campaigns-draft-inactive-tab]] — the Inactive tab: filter, route, Status toggle column, ongoing statistics aggregation, channel-suspension banned-reason badge.
- [[campaigns-draft-entry-paths]] — how campaigns become Draft (create / predefined / copy), the 0/1/2 status state machine, valid transitions.
- [[campaigns-draft-unsaved-changes-guard]] — `CampaignDraftGuard` modal, browser `beforeunload`, **Save draft** button + toast behaviour, snapshot diff detection.
- [[campaigns-draft-preflight-checks]] — Draft→Active + Inactive→Active activation pre-flight checks; the toggle-endpoint trust gap; channel-suspension cascade.
- [[campaigns-draft-lifecycle-actions]] — archive / delete / copy behaviour across Draft and Inactive rows; plan-quota impact; subscriber retention semantics.

## Settings & fields

### Common columns (both tabs)

| Column key | Label | Notes |
|------------|-------|-------|
| `title` | Campaign title | Locked first column; click to open editor. |
| `created_at` | Date added | Creation date. |
| `goal` | Goal | The campaign's `trigger_condition` / purpose. |
| `actions_count` | Steps | Number of campaign actions. |
| `reached` | Reached subscribers | Successfully-sent uniques (always 0 on Draft). |
| `orders` | Orders | Attributed orders (always 0 on Draft). |
| `turnover` | Turnover | Revenue from attributed orders (always 0 on Draft). |
| `subscribers_count` | Subscribers | Enrolled count (0 on Draft). |
| `statistics` | Logs | Link to per-action logs. |
| `status` | Status | Active/Inactive toggle — **shown on Inactive tab, hidden on Draft tab**. |
| `actions` | Actions | Edit, Copy, Archive, Delete. |

### Status values

| Status | Value | Tab |
|--------|-------|-----|
| Inactive | 0 | Inactive |
| Active | 1 | Active |
| Draft | 2 | Draft |

A campaign is in exactly one of these states at any time. Full transition matrix on [[campaigns-draft-entry-paths]].

## Business rules

- **Drafts count toward the plan campaign quota** — see [[campaigns-draft-lifecycle-actions]].
- **Save draft skips most pre-flight validation** — only basic schema checks run; full pre-flight defers to **Start campaign**. See [[campaigns-draft-preflight-checks]].
- **Channel-suspension cascade flips Active campaigns to Inactive** — Drafts are untouched; the merchant hits the pre-flight failure only on Start. See [[campaigns-draft-preflight-checks]].
- **Inactive campaigns retain enrolled subscribers** — flipping back to Active resumes mid-funnel subscribers from where they left off. See [[campaigns-draft-lifecycle-actions]].
- **Inactive tab statistics keep updating hourly** — attributed orders from previously-sent subscribers continue to roll in. See [[campaigns-draft-inactive-tab]].
- **No auto-save** — the editor relies on `CampaignDraftGuard` + `beforeunload` instead. See [[campaigns-draft-unsaved-changes-guard]].
- **Anti-spam policy gate** — both tabs require [[marketing-campaigns-policy|anti-spam policy]] acceptance like every campaign endpoint.

## Related

- [[marketing-campaigns]] — parent hub; the Draft and Inactive tabs are part of the four-tab list.
- [[marketing-campaigns-edit]] — editor; Drafts are edited here; **Start campaign** moves Draft to Active.
- [[marketing-campaigns-create]] — create flow; every campaign starts as Draft.
- [[marketing-campaigns-from-predefined]] — predefined clones; also start as Draft.
- [[marketing-campaigns-copy]] — copy clone; also starts as Draft.
- [[marketing-campaigns-archive]] — Archived tab; Inactive campaigns can move there.
- [[marketing-campaigns-banned-info]] — banned-reason explainer; Inactive campaigns with channel issues link here.
- [[marketing-channels]] — channel setup; channel suspension auto-moves campaigns to Inactive.
- [[marketing-campaigns-policy]] — anti-spam policy required for every campaign endpoint.
- [[campaign]] — Campaign entity.

## Open questions

No outstanding questions.
