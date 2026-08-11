---
type: feature
nav_path: "Invoices → Download → Permissions & plan gate"
route_name: admin.core.export
route_path: /admin/api/core/export-import/download_invoices
aliases: ["Invoice download permissions", "invoices.download grant", "Invoice download plan gate", "Invoices plan feature"]
tags: [orders, invoices, download, permissions, plan-gates]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---
# Invoices bulk download — permissions & plan gate

> Part of [[orders-invoices-download]]. See the hub for related aspects (entry point, scope, sync/async, rendering).

## Purpose

Documents the two access controls on the bulk-download action: the staff-permission chain that a sub-admin needs to use it, and the `invoices` plan-feature that gates the whole invoices area.

## Where to find it

The action is reachable only from the **Download** button on [[orders-invoices]] (see [[invoices-download-entry-points]]). Staff permissions are configured on [[settings-staff]]; plan upsell is on [[plan-features]].

## What the merchant can do here

- Grant a staff member the ability to bulk-download invoices by assigning the `invoices.download` grant on [[settings-staff]].

### What the merchant CANNOT do here

- Bulk-download without the full permission chain below — a sub-admin missing any link in the chain cannot trigger the action.
- Reach the button at all on a plan that lacks the `invoices` feature — the parent list page is gated.

## Settings & fields

### Permission mapping

The download action `download_invoices` requires all three:

- `orders` permission section.
- `invoices.all` permission group.
- `invoices.download` permission grant.

Store owners (full admins) have all permissions implicitly; the chain matters for restricted staff accounts configured on [[settings-staff]]. (The sibling CSV Export action maps to `invoices.export` instead — see [[orders-invoices-export]].)

## Business rules

### Plan gate — `invoices`

This feature is gated by the `invoices` plan-feature (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `invoices` | Access gate (URL `invoices`) | The parent [[orders-invoices]] page is itself gated on `invoices` — when the plan lacks the feature the list page is inaccessible, so the **Download** button is unreachable. Reaching the download endpoint directly without first loading the list still requires the merchant's session to have passed the plan-middleware check. |

When the gate is hit, the merchant is redirected to [[plan-features]] for the per-feature upsell. `invoices` is a boolean access gate — it requires a plan that includes the feature; it does NOT extend via feature packs (see [[plan-vs-feature-pack]]).

### Two independent gates — both must pass

The plan gate and the permission chain are separate controls and a download requires **both** to be satisfied:

- The **plan gate** (`invoices`) is store-wide — it decides whether the invoices area exists for this store at all. A full admin on a plan without `invoices` still cannot reach the button.
- The **permission chain** (`orders` + `invoices.all` + `invoices.download`) is per-staff-account — it decides which staff members on an eligible plan may trigger the action. A restricted staff member on an `invoices`-enabled plan still needs the `invoices.download` grant.

For a "why can't this staff member download invoices?" support ticket, check the plan first (does the store have `invoices`?), then the staff member's `invoices.download` grant on [[settings-staff]].

## Open questions

(none.)

## Related

- [[orders-invoices-download]] — hub.
- [[settings-staff]] — `invoices.download` permission grant.
- [[orders-invoices]] — parent invoices list (gated on `invoices`).
- [[orders-invoices-export]] — sibling CSV export (maps to `invoices.export`).
- [[plan-gates]] — plan-gating mechanism.
- [[plan-vs-feature-pack]] — boolean access gate vs feature-pack extension.
- [[plan-features]] — per-feature upsell page.
