---
type: feature
nav_path: "Apps → XML Sync → Overview"
route_name: apps.xml_sync.overview
route_path: /admin/apps/xml_sync
aliases: ["XML Sync Overview", "Xml Sync overview"]
tags: [apps, imports, xml, sync, recurring, overview]
plan_gates: ["xml_sync_limit"]
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# XML Sync → Overview

## Purpose

The **Overview** tab is the landing card for the XML Sync app — shows install state, brief description, capabilities, and quick-jumps. Reuses the shared `ErpOverview` Vue component (same pattern as [[apps-xml-import-overview]]).

Distinct from XML Import in one key way: XML Sync runs **recurring** (per the configured interval) — not just one-time. The Overview surfaces this scheduled-sync nature + the merchant's plan-gated cap (`xml_sync_limit`).

For the full feature set, see [[apps-xml-sync]].

## Where to find it

Sidebar → Apps → XML Sync → **Overview tab** (default landing). Route: `/admin/apps/xml_sync`.

## What the merchant can do here

- See the app's metadata: name, icon, description, install state.
- View install help text emphasizing recurring sync vs one-time import.
- Trigger Install (if not installed) / Uninstall.
- Jump to [[apps-xml-sync-settings]] for task management.
- See plan-feature usage chip showing `xml_sync_limit` against current sync-task count.

### What the merchant CANNOT do here
- Create / configure sync tasks directly — that's the Settings / List view.
- See per-task progress — that's [[apps-xml-sync-status]].

## Settings & fields

Near-static metadata + install-action page. No editable fields beyond install / uninstall.

## Business rules

### Same shared overview pattern as XML Import

The component `ErpOverview` is reused across all imports/exports/ERP apps for consistent install + metadata UX.

### Plan-feature gating

Per [[apps-xml-sync]]: max sync tasks comes from the `xml_sync_limit` plan feature, and the Overview surfaces this chip — when the merchant is on a plan that doesn't allow XML Sync tasks (or has run out), the upgrade CTA appears. Beyond the task cap, XML Sync has **three buyable feature packs — product limit, processing priority, and processing frequency (interval)** — detailed on [[apps-xml-sync-features]]; the product-limit behaviour (over-limit products not processed + in-app notification + email) is documented on [[apps-xml-sync-status]].

### Permission
Standard apps permission scope.

## Related

- [[apps-xml-sync]] — XML Sync hub with feature set + 3 queue mappings.
- [[apps-xml-sync-settings]] — sync task management.
- [[apps-xml-sync-status]] — per-task status.
- [[apps-xml-sync-features]] — capabilities documentation.
- [[apps-xml-import]] — sister ONE-TIME import (different cadence model).
- [[apps-xml-import-overview]] — parallel overview page.
- [[apps-csv-import]] — alternative CSV-based import.

## How it works (verified against backend)

### Install copy emphasises recurring nature

The English install copy reads:
- **Title** (`info.title`): "XML products synchronization"
- **Header** (`header.install`): "XML Product Synchronization Tool"
- **Install help** (`help.install`): "With this application you can syncronize your products and their variations from your Inventory management system. To make the syncronization you will need XML file from your inventory software."
- **Info line** (`info.install`): "You can automatically sync the quantity, prices and product status of your products"

The word "synchronize" + "automatically sync" appears in both header and body — distinguishing it from one-shot [[apps-xml-import]] in the merchant's mental model.

### Upgrade-to-unlock: HTTP 402 + in-app `PlanFeature` modal

When the merchant tries to create or re-activate a sync task while at `xml_sync_limit`, the API returns **HTTP 402** with `feature: xml_sync_limit`, `message: "You can have maximum {max} active tasks"`, and `info: {max, total}`. The frontend opens the standard plan-feature upgrade modal in-app — same flow as XML Import's `xml_import_limit` cap (no redirect to a billing page).

### Auto-uninstall when no active tasks remain

When the last sync task is deactivated or deleted, the platform automatically uninstalls all three `xml_sync_*` queue mappings — no more scheduled tick. The merchant doesn't have to formally uninstall the app to free the queue resources; deactivating all tasks does it. Creating or activating a task re-installs them transparently.

## Open questions

_None._
