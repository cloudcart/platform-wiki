---
type: feature
nav_path: "Marketing → Campaigns → Draft → Draft tab"
route_name: campaigns-draft
route_path: /admin/marketing-new/campaigns/draft
aliases: ["Draft campaigns tab", "Draft list view", "Saved drafts list", "In-progress campaigns", "Чернови раздел"]
tags: [marketing, campaigns, draft, list]
plan_gates: ["abandoned_orders", "campaigns"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-campaigns-draft]]. See the hub for the other aspects (Inactive tab, entry paths, unsaved-changes guard, pre-flight checks, lifecycle actions).

# Draft campaigns — the Draft tab

## Purpose

The **Draft** tab is the merchant's "in-progress" workspace — every campaign with `active=2` AND `archived_at IS NULL` lives here. Drafts have never enrolled anyone, never sent anyone a message, and have zero statistics. The tab exists so the merchant can see at a glance *"what am I still building?"* separately from running and paused campaigns.

The Draft tab is one of four tabs on the campaigns list ([[marketing-campaigns]]); the Inactive sibling tab is covered separately on [[campaigns-draft-inactive-tab]].

## Where to find it

Sidebar → **Marketing** → **Campaigns** → click the **Draft** tab.

| Setting | Value |
|---------|-------|
| Route name | `campaigns-draft` |
| Route path | `/admin/marketing-new/campaigns/draft` |
| Filter rule | `active = 2` AND `archived_at IS NULL` |

The four campaign tabs share the same Vue list component; clicking a tab swaps the URL and re-queries the matching list endpoint.

## What the merchant can do here

- See every Draft campaign in the store in a single sortable / filterable / paginated table.
- Click a row's title to open the campaign in [[marketing-campaigns-edit|the editor]] in **editable** mode (the row click passes `query: {edit: '1'}` because `row.draft === true`).
- Copy a Draft → clones to a new Draft via [[marketing-campaigns-copy]].
- Archive a Draft → moves to [[marketing-campaigns-archive]] (no extra steps; the underlying endpoint accepts a Draft ID — see [[campaigns-draft-lifecycle-actions]]).
- Delete a Draft → soft-deletes directly (no archive-first step required — see [[campaigns-draft-lifecycle-actions]]).
- Drill into Statistics ([[marketing-campaigns-statistics]]) or Logs ([[marketing-campaigns-statistics-log]]) — both show zero data because no sends have occurred.
- Drill into Subscribers ([[marketing-campaigns-subscribers]]) — empty for Drafts.

## Settings & fields

### Columns rendered

Same columns as the Inactive tab with two structural omissions:

| Column key | Label | Behaviour on Draft tab |
|------------|-------|------------------------|
| `title` | Campaign title | Locked first column; click opens editor in editable mode. |
| `created_at` | Date added | Creation date. |
| `goal` | Goal | The campaign's `trigger_condition` / purpose. |
| `actions_count` | Steps | Number of campaign actions. |
| `reached` | Reached subscribers | **Always 0** — Drafts have never sent. |
| `orders` | Orders | **Always 0** — Drafts have no attributed orders. |
| `turnover` | Turnover | **Always 0**. |
| `subscribers_count` | Subscribers | **Always 0** — Drafts have no enrolled subscribers. |
| `statistics` | Logs | Link is rendered but logs page is empty. |
| `status` | Status | **Column omitted** — Drafts have no Active/Inactive toggle. |
| `actions` | Actions | Edit, Copy, Archive, Delete. |

### Tab-specific UI omissions

- **Status toggle column hidden.** Drafts move out of Draft only via **Start campaign** in the editor, never via a row-level toggle. The column is omitted from the column array for this tab.
- **Bulk-action bar hidden.** Only the Archived tab gets the bulk-delete bar; the Draft tab shows no bulk actions on row selection.
- **Row click opens editor in editable mode.** Because `row.draft === true`, the click passes `query: {edit: '1'}` — the merchant lands directly in the editable form (not the read-only preview).

## Business rules

### Order-statistic query is short-circuited

The Draft tab explicitly **skips** the expensive order-statistic query (which joins against the orders-meta campaign-id column on Active / Inactive tabs). The override returns an empty array for Draft, because every Draft row would always come back with 0 orders / 0 turnover anyway. The result: the Draft tab loads marginally faster on stores with many drafts.

### Draft entry is a one-way street

Every newly-created campaign starts as Draft, regardless of entry path — see [[campaigns-draft-entry-paths]] for the full list of how campaigns land here. Once a campaign has been started, there is **no path back to Draft**; it's either Active or Inactive forever (until archived / deleted).

### Status-toggle endpoint refuses Drafts

The `campaigns.update_active` toggle endpoint refuses to flip a Draft directly with the error *"Campaign was not started"*. This protects against bypass attempts — Drafts must move through the editor's **Start campaign** flow so the full pre-flight runs. See [[campaigns-draft-preflight-checks]].

### Drafts count toward the plan quota

Every Draft consumes one slot from the merchant's plan-tier campaign quota, even though it's never been started and has no enrolled subscribers. Merchants who create test drafts and never start any of them are still using their plan's campaign slots. See [[campaigns-draft-lifecycle-actions]] for the quota-recovery procedure.

### No auto-save in the editor

Every change in the Draft editor stays in the merchant's browser until they click **Save draft**. The two compensating safety nets — the `CampaignDraftGuard` modal and the browser `beforeunload` dialog — are covered on [[campaigns-draft-unsaved-changes-guard]].

### Anti-spam policy gate

Like every campaign endpoint, the Draft tab requires [[marketing-campaigns-policy|anti-spam policy]] acceptance.

### Permissions

Standard campaign permission applies.

## Related

- [[marketing-campaigns-draft]] — hub.
- [[marketing-campaigns]] — parent four-tab list; the Draft tab is one of those tabs.
- [[marketing-campaigns-edit]] — editor; row click lands here in editable mode.
- [[marketing-campaigns-create]] — create flow; every new campaign starts as Draft.
- [[marketing-campaigns-from-predefined]] — predefined clone; also starts as Draft.
- [[marketing-campaigns-copy]] — copy clone; also starts as Draft.
- [[marketing-campaigns-statistics]] — Statistics screen (empty for Drafts).
- [[marketing-campaigns-statistics-log]] — Logs screen (empty for Drafts).
- [[marketing-campaigns-subscribers]] — Subscribers screen (empty for Drafts).
- [[marketing-campaigns-policy]] — anti-spam policy required for every campaign endpoint.

## Open questions

No outstanding questions.
