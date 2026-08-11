---
type: feature
nav_path: "Orders → Ordered Products → Export → Permissions & plan"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders_products
aliases: ["Ordered Products export permission", "Products by orders export plan gate", "Aggregated product export access", "products_by_orders.export grant", "Order products export legacy job"]
tags: [orders, products, export, permissions, plan-gates, staff]
plan_gates: ["export_orders"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-ordered-products-export]]. See the hub for related aspects (trigger / 2FA, CSV schema, sync vs async, filter scope, delivery).

# Ordered Products export — permissions & plan

## Purpose

Documents **who can use the export and on which plans** — the staff-permission grants that gate the action regardless of plan, the `export_orders` plan-feature mapping that shows / hides the button, and the legacy job alias that keeps older queued exports completing. This is the access-control layer behind the Export button.

## Where to find it

- Staff permission grants are configured on [[settings-staff]] (per-role / per-staff).
- The plan-feature gate is part of the platform's plan framework — when the merchant lacks the plan feature, the Export button is hidden on [[orders-ordered-products]] and a gate redirect leads to [[plan-features]].

## What the merchant can do here

- Grant or revoke the `products_by_orders.export` permission to staff via [[settings-staff]].
- Upgrade the plan to gain `export_orders` (which unlocks BOTH this export and [[orders-export]]).

The merchant CANNOT enable this export without the `export_orders` plan feature, and a staff member CANNOT trigger it without the `products_by_orders.export` grant even on a qualifying plan.

## Settings & fields

### Staff permission mapping

The export action `export_orders_products` requires all three grants:

| Grant | Level |
|-------|-------|
| `orders` | permission section |
| `products_by_orders.all` | permission group |
| `products_by_orders.export` | permission grant |

### Plan-feature mapping

| Mapping | Shape | What it controls |
|---|---|---|
| `export_orders` | Boolean access gate (shared URL family `orders/export/%`) | The platform registers `orders/export/orders` for `export_orders`. The Ordered-Products export action `export_orders_products` is delivered through the same `/admin/api/core/export-import/...` endpoint family, so it inherits the same gate. A verbatim `export_orders_products` entry is NOT in the plan config — only `export_orders` is. |

## Business rules

### One plan gate controls both exports

Because no separate `export_orders_products` mapping exists, a merchant who has `export_orders` in their plan can use BOTH the orders export and the ordered-products export; a merchant without it has neither button. The button visibility is driven from the same permission check as [[orders-export]].

### `export_orders` is a boolean access gate — no feature-pack extension

`export_orders` requires a plan that includes the feature; it does NOT extend via feature packs (contrast [[plan-vs-feature-pack]]). The "this export tier" boolean controls both exports together. When the gate is hit, the merchant is redirected to [[plan-features]] for the per-feature upsell ([[plan-gates]]).

### Staff permission gates the action regardless of plan

Even on a qualifying plan, the action checks `products_by_orders.export` first. A staff member without that grant cannot trigger the export. This is the same staff-permission model as the orders export — see [[orders-export-permissions-plan]].

### Legacy method alias retained — `OrderProductsNewExport`

The queue dispatcher recognises both `OrderProductsExport` and `OrderProductsNewExport` as job types; the latter aliases to the former. This is a one-line bridge so older queued jobs from before the renaming continue to complete successfully. Merchants never see this distinction.

## Related

- [[orders-ordered-products-export]] — hub.
- [[orders-ordered-products]] — the page where the gated Export button appears.
- [[orders-export-permissions-plan]] — the orders export's permission / plan layer (shares the `export_orders` gate).
- [[settings-staff]] — `products_by_orders.export` permission grant.
- [[plan-features]] — per-feature upsell when the gate is hit.
- [[plan-gates]] / [[plan-vs-feature-pack]] — plan-feature framework.

## Open questions

None.
