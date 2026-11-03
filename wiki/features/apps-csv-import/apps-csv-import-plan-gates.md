---
type: feature
nav_path: "Apps → CSV Import → Plan gates"
route_name: apps.csv_import.overview
route_path: /admin/apps/csv_import (plan-gating)
aliases: ["CSV Import — plan gates", "CSV Import — csv_import feature key", "CSV Import — products numeric cap", "CSV Import — plan-quota interruption"]
tags: [apps, imports, csv, plan-gated, plan-gates]
plan_gates: ["csv_import"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (wizard, task detail, row pipeline, final statuses, mapping fields, side effects).

# CSV Import — plan gates

## Purpose

CSV Import is gated through the plan-feature registry in two ways: the **install gate** (`csv_import`) controls whether the app is offered on the merchant's plan; the **products numeric cap** (inherited from the merchant's plan) interrupts the row pipeline when the running task tries to create more products than the plan allows. This page documents both gates plus the interaction with the manager-level concurrent-imports lock (which is NOT plan-driven).

## Where to find it

App Store — CSV Import card visibility depends on the `csv_import` plan-feature mapping. The numeric-cap interruption surfaces on the task-detail page's yellow message box when triggered. See [[apps-csv-import-task-detail]].

## What the merchant can do here

- **See / hide the app** based on plan — plans without `csv_import` don't surface the integration in the App Store. Upsell routes through the standard plan-features funnel.
- **Run imports up to the plan's products cap** — once the cap is hit, the running import is interrupted with a specific plan-quota message. The merchant either upgrades the plan, removes existing products to free quota, or adds a feature pack extension. See *Business rules* below.
- **Run one import at a time** — the manager-level `working` lock blocks parallel imports regardless of plan. See [[apps-csv-import-row-pipeline]].

## Settings & fields

The CSV Import app is mapped through the plan-feature registry (see [[plan-gates]], [[plan-vs-feature-pack]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `csv_import` | Plan-feature mapping (CSV Import manager) | The feature key the platform reads to surface the app + its caps in the plan-feature registry. **App availability** — plans without this key don't see the integration. |
| `products` numeric cap | Plan-feature mapping inherited from the merchant's plan | Numeric cap on total product records the store can hold. Imports that would create rows beyond the cap are **interrupted mid-flight** with a plan-quota exception. |

**Concurrent imports are serialised at the manager level (`working` lock) — INDEPENDENT of the plan.** High-tier plans do NOT get parallel imports. See [[apps-csv-import-row-pipeline]].

## Business rules

### `csv_import` install gate

The `csv_import` plan-feature is the install gate — the App Store card is offered on plans that include this key. Plans without it can't install the integration; upsell routes through [[plan-features]].

### Inherited per-plan products numeric cap

The CSV Import flow ALSO inherits the per-product create cap of the merchant's plan. Hitting the `products` numeric cap mid-import:

1. Throws a plan-quota exception upstream.
2. The manager catches the exception and calls `setWorking(false)`.
3. The `finalizeOrphanedTask` finaliser fires, marking the task `failed` with the specific message:

> *"Import was interrupted before completion (imported X of Y). Common cause: plan create-quota was reached. Check your plan limits or contact support."*

The `X of Y` numbers let the merchant see exactly how many rows landed before the cap hit. See [[apps-csv-import-final-statuses]] for the orphaned-task path and [[apps-csv-import-task-detail]] for where the message surfaces.

### `working` lock is NOT plan-tier-extended

Unlike XML Import (which has `xml_import_limit` for concurrent tasks per plan), the CSV Import integration has **no per-plan concurrent-imports setting**. The `working` lock is a hard one-import-per-store rule regardless of plan tier. The merchant must wait for an import to finish before starting another, even on the highest plan. See [[apps-csv-import-row-pipeline]].

### Feature-pack extensions apply to the products cap (not the install gate)

The `products` numeric cap CAN be extended via feature packs — see [[plan-vs-feature-pack]]. Merchants who keep hitting the cap on imports can purchase a products feature pack to lift the cap without upgrading the whole plan. The `csv_import` install gate is binary and not extended by feature packs — it's plan-included or not.

### Sibling-app gates live elsewhere

The plan-features that gate the **blog CSV import** variant live on [[apps-blog-csv-import]]; the **customer import** variant on [[customers-import]]. Each variant has its own install gate.

### Upsell routing

When the merchant hits the install gate (plan without `csv_import`) or the products numeric cap, upsell flows route through [[plan-features]]; feature packs extend numeric caps per [[plan-vs-feature-pack]].

## Related

- [[apps-csv-import]] — hub.
- [[apps-csv-import-row-pipeline]] — `working` lock + the orphaned-task path triggered when the cap hits.
- [[apps-csv-import-final-statuses]] — the orphaned-task message text.
- [[apps-csv-import-task-detail]] — where the plan-quota message surfaces to the merchant.
- [[plan-gates]] — plan-gating concept.
- [[plan-features]] — per-feature upsell surface.
- [[plan-vs-feature-pack]] — feature-pack extension semantics.
- [[apps-blog-csv-import]] — sibling app with its own gate.
- [[customers-import]] — customer-records CSV variant with its own gate.

## Open questions

_None._
