---
type: feature
nav_path: "Apps → XML Import → Overview"
route_name: apps.xml_import.overview
route_path: /admin/apps/xml_import
aliases: ["XML Import Overview", "Xml Import overview"]
tags: [apps, imports, xml, overview, plan-gated]
plan_gates: ["xml_import", "xml_import_limit", "xml_import_total_products"]
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# XML Import → Overview

## Purpose

The **Overview** tab is the landing card for the XML Import app — shows install state, brief description, capabilities, and quick-jumps to the next merchant action. Reused component (`ErpOverview`) is shared across all imports/exports / ERP apps for consistent presentation.

For the full feature set, see [[apps-xml-import]].

## Where to find it

Sidebar → Apps → XML Import → **Overview tab** (the default landing when entering the app). Route: `/admin/apps/xml_import`.

## What the merchant can do here

- See the app's metadata: name, icon, description, install state.
- View install help / capabilities ("With this app you can import XML feeds from suppliers, ...").
- Trigger Install (if not installed) or Uninstall.
- Jump to the actual import management view ([[apps-xml-import-settings]]).
- See plan-feature usage chip (if plan-gated — XML Import has `supportPlanPriority` + `supportPlanInterval` + `maxTasks` per [[apps-xml-import]]).

### What the merchant CANNOT do here
- Create import tasks directly — that's the Settings / List tab.
- See per-task progress — that's [[apps-xml-import-status]].

## Settings & fields

This view is a near-static metadata + install-action page. No editable fields beyond the install / uninstall trigger.

## Business rules

### Shared with ERP overview pattern

The component `Erp/Core/components/Tabs/ErpOverview` is reused across many apps (XML Import, XML Sync, ERP integrations, etc.) — ensures consistent install / metadata UX.

### Plan feature surfaced

When the merchant's current plan caps `maxTasks` or has restricted intervals, that constraint is shown on the Overview (typically a small "X of Y tasks used" or "Daily sync allowed" chip).

### Permission
Standard apps permission scope.

## Plan gates

The Overview surfaces all three plan-features the app is gated by (see [[plan-gates]], [[plan-vs-feature-pack]]):

| Mapping | Shape | What it controls on this screen |
|---|---|---|
| `xml_import` | App-install access gate (`apps/xml_import/install`) | Whether the Install CTA actually installs vs. redirects to the per-feature paywall. |
| `xml_import_limit` | Numeric (max concurrent active tasks) | Surfaced as the "X of Y tasks used" chip (grouped under `tasks`). Clicking *Create new task* when at the cap returns HTTP 402 → `PlanFeature` modal. |
| `xml_import_total_products` | Numeric (cumulative product cap) | Surfaced as the "X of Y products" chip (grouped under `products`). Caps the total products across every XML Import task on the store. |

Both numeric chips read the plan's ceiling AND the current consumption; chips for plan-features that are inactive in the registry are silently hidden. Beyond these two chips, the app also exposes a **processing-priority** (`xml_import-priority`) and a **processing-frequency / interval** (`xml_import-interval`) feature, surfaced on [[apps-xml-import-features]]. So in total the merchant can buy **three feature packs — product limit, priority, and frequency** — while `xml_import_limit` (active-task count) is the per-plan cap. Feature packs extend the numeric caps per [[plan-vs-feature-pack]]; the install gate requires a plan upgrade. Upsell flows route through [[plan-features]].

## Related

- [[apps-xml-import]] — XML Import hub with all sub-pages + feature set.
- [[apps-xml-import-settings]] — task management.
- [[apps-xml-import-status]] — per-task status.
- [[apps-xml-import-features]] — capabilities documentation.
- [[apps-xml-sync]] — sister recurring sync.
- [[apps-csv-import]] — alternative CSV-based import.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.

## How it works (verified against backend)

### Install help text (English)

The install help text in English reads: **"You can import product to your store from this application by using XML feed."** This is the description the Overview surfaces along with the install CTA. The Bulgarian translation follows the same wording.

### Plan-feature chips: two values surfaced

When the app is installed, the Overview pulls TWO plan-feature values from the active subscription:
- **`xml_import_limit`** — grouped under `tasks`. The "X of Y tasks used" chip — shows how many active tasks the merchant has out of their plan's max.
- **`xml_import_total_products`** — grouped under `products`. Caps the cumulative product count across all tasks (not per-task).

Both chips show the plan ceiling and current consumption. When a plan-feature is inactive or absent, that chip is hidden. (The Overview shows only these two count chips; the **priority** and **interval** feature packs are surfaced on [[apps-xml-import-features]].)

### Upgrade CTA on cap

When the merchant clicks "Create new task" while at the plan's `xml_import_limit`, the API returns **HTTP 402** with `feature: xml_import_limit`, `message: "You can have maximum {max} active tasks"`, and `info: {max, total}`. The frontend surfaces this as a plan-feature upgrade modal — the standard in-app payment flow used across plan-gated apps.

### App uninstall is automatic when no active tasks remain

The app self-uninstalls (drops all 3 queue mappings) when the last active task is removed or all tasks are deactivated. Saving a new task or activating one re-installs the parser queue mapping immediately. The merchant doesn't have to click "Uninstall" to free the queue resources — deactivating the last task does it.

### English / Bulgarian install help diverge on emphasis

English install help reads "You can import product to your store from this application by using XML feed." The Bulgarian translation mirrors it. **No "see other plans" or pricing copy** lives on Overview — the upgrade CTA opens the standard plan-feature modal flow.

## Open questions

_None._
