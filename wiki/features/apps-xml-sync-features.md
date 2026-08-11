---
type: feature
nav_path: "Apps → XML Sync → Features"
route_name: apps.xml_sync.features
route_path: /admin/apps/xml_sync/features
aliases: ["XML Sync Features", "Xml Sync features", "Xml Sync capabilities"]
tags: [apps, imports, xml, sync, features, capabilities]
plan_gates: ["xml_sync_limit"]
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# XML Sync → Features

## Purpose

The **Features** page is the **capabilities + plan-features documentation view** for XML Sync. Shows what the app can do + which capabilities are gated by the merchant's plan. Same architectural pattern as [[apps-xml-import-features]] — the route reuses the `Status` component with features-focused data.

Used by merchants evaluating whether to install OR considering an upgrade.

For the full feature set, see [[apps-xml-sync]].

## Where to find it

Sidebar → Apps → XML Sync → **Features tab**. Route: `/admin/apps/xml_sync/features`.

## What the merchant can do here

### Read app capabilities

Features displayed (per [[apps-xml-sync]]):
- **Recurring sync** (vs one-time [[apps-xml-import]]).
- **Per-field update policy** — always-update / threshold / never per field.
- **Discontinued-product handling** — Deactivate / Delete / Keep (the on_missing option in [[apps-xml-sync-step3]]).
- **3 queue mappings** for the parse/parse-single/insert pipeline.
- **Plan-gated** — three buyable feature packs (product limit, processing priority, processing frequency) plus a `xml_sync_limit` active-task cap (see *Plan-feature meters* below).
- **maxTasks** cap based on plan.
- **Background processing** — long syncs run async.
- **Cancellation mid-flight**.

### Plan-feature usage

Same plan-feature display as [[apps-xml-sync-status]]:
- Total products across all sync tasks vs limit.
- Upgrade CTA when approaching cap.

### Upgrade flow

`PlanFeature` modal opens via upgrade CTA → payment flow → limits refresh.

### What the merchant CANNOT do here
- Configure tasks (use [[apps-xml-sync-step2]] / [[apps-xml-sync-step3]]).
- Run tasks (use [[apps-xml-sync-status]]).
- Edit capabilities (platform-defined).

## Settings & fields

Read-only / informational view. No persistent settings here.

## Business rules

### Reused component

Same `Status` component as [[apps-xml-sync-status]]. Route distinguishes intent — Features focuses on capabilities + plan, Status focuses on per-task progress.

### Plan-feature visibility

When the merchant is on a tier with restricted XML Sync features (limited tasks, longer intervals), the Features page surfaces these limits + upgrade CTAs.

### Permission
Standard apps permission scope.

## Related

- [[apps-xml-sync]] — XML Sync hub.
- [[apps-xml-sync-overview]] — Overview tab.
- [[apps-xml-sync-settings]] — task list.
- [[apps-xml-sync-status]] — per-task status (shares Vue).
- [[apps-xml-sync-step2]] / [[apps-xml-sync-step3]] — wizard.
- [[plan]] — plan definitions.
- [[apps-xml-import-features]] — parallel page in XML Import.

## How it works (verified against backend)

### Plan-feature meters: the three feature packs + the task cap

The merchant can buy **three feature packs** for XML Sync — **product limit, processing priority, and processing frequency** — and the plan separately caps the number of active tasks. The page surfaces these per-plan meters (when the corresponding plan feature is active in the platform registry):
- **product limit** — grouped under "products". Caps how many products are processed across all sync tasks. When a run exceeds it, the over-limit products are **not processed** and the merchant gets an in-app notification + email — see [[apps-xml-sync-status]]. (Feature pack.)
- **`xml_sync-priority`** — grouped under "priority", suffix `percent`. Higher plans get higher queue priority. (Feature pack.)
- **`xml_sync-interval`** — grouped under "interval", suffix `hours`. Lower interval = faster cadence; default falls back to 12h. (Feature pack.)
- **`xml_sync_limit`** — grouped under "tasks". The per-plan cap on concurrent active sync tasks — not one of the three packs.

Each meter shows the plan ceiling and current consumption — when the `used` count approaches `current`, the UI surfaces an upgrade prompt.

### No side-by-side plan tier comparison table

The page returns the merchant's CURRENT plan's ceilings only. The upgrade CTA opens a plan-feature upgrade modal for the specific feature hit, not a full plan-tier matrix.

### Same `Status` Vue component as the Status tab

There is no dedicated Features route in the XML Sync module. The Features tab hits the status endpoint with no task ID. The Vue layer renders the Features panel from that response — plan-feature meters + general install state — and omits the per-task progress block.

### Plan-feature payload structure

The plan-feature objects returned to the Vue have the shape:
- `group` — meter-group label (typically `tasks` for limits, `priority` for queue priority, `interval` for cadence).
- `id` / `mapping` — platform plan-feature row reference.
- `name` — translated feature name shown to the merchant.
- `current` — the merchant's plan-set ceiling.
- `used` — current consumption (e.g., active task count for `xml_sync_limit`).
- `suffix` — UI hint (`count`, `hours`, `percent`).
- `type` — flag set including `export`.
- `cast: int` — floor-to-integer on display.

Plan features whose registry row is `active = false` are silently omitted from the response.

## Open questions

_None._
