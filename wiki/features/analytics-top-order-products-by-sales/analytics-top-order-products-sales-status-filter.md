---
type: feature
nav_path: "Analytics → Products by sales → Status filter"
route_name: analytics
route_path: /admin/analytics
aliases: ["Products by sales status filter", "Products by sales hardcoded statuses", "Products by sales order statuses", "Продукти по продажби — статуси на поръчки"]
tags: [analytics, ccanalytics, orders, products, top-order-products-by-sales, order-statuses]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---
> Part of [[analytics-top-order-products-by-sales]]. See the hub for the other aspects (UI surface, data source, export).

# Products by sales — status filter

## Purpose

Explains **which order statuses count** toward the "Products by sales" ranking, why that set is **fixed** (Paid, Completed, Pending, Authorized payment, Fulfilled), and why — unlike most analytics boxes — the merchant cannot change it from Settings → Analytics → Order statuses. This is the single most common point of confusion for this report, so it has its own page.

## Where to find it

The constraint surfaces in two places on the Analytics dashboard: the box **tooltip** (hover the "Products by sales" title) and a permanent **yellow alert banner** above the Details table.

## What the merchant can do here

Nothing configurable — this aspect is read-only behaviour. The merchant can only **read** the status set (from the tooltip / banner) to understand why a revenue figure here differs from a figure on a box that honours the configurable status set. To change which statuses count for OTHER analytics boxes, see [[analytics]] (Settings → Analytics → Order statuses), but note it has no effect here.

## What the merchant sees

### Tooltip

*"Best-selling products by their total value from all orders. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."* / *"...спрямо следните статуси на поръчки - Платена, Изпълнена, Изчакваща, Оторизирано плащане, Изпратена."*

### Status-filter alert banner (Details only)

A permanent yellow alert (set by the box's `formatters.alerts.details`):

> *"Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled"* / *"Данните се визуализират спрямо стандартните статуси в Настройки и не могат да бъдат променяни → Платена, Изпълнена, Изчакваща, Оторизирано плащане, Изпратена"*

The alert is shown via the `the platform code(false, "top-order-products-by-sales.alerts.details")` hook.

## Settings & fields

There is no Settings field for this box's status set. For contrast, the relevant keys elsewhere are:

| Key | Where | Effect on THIS box |
|-----|-------|--------------------|
| `cc_analytics.statuses` | Settings → Analytics → Order statuses | **None.** Used by other boxes (e.g. [[analytics-top-order-discounts]]) at query time, ignored here. |
| (ingestion `$match`) | Platform pipeline | The fixed status `$or` below; not exposed in any merchant Setting. |

## Business rules

### The set is enforced at ingestion, not at query time

The by-sales pipeline uses the **base** match filter (date + site_id only — no per-status condition). The status set is applied **when the daily aggregation job writes the collection**, not when the box reads it. So changing Settings → Analytics → Order statuses does NOT alter what enters the data — it's a platform-fixed list for these "top products" boxes.

### Exact list (verified against backend)

The `topOrderProductsPerDay` aggregation `$match` uses this fixed status `$or`:

- `status in [paid, completed, authorized]`
- OR (`status = pending` AND `status_fulfillment = not_fulfilled`)
- OR (`status_fulfillment = fulfilled`)

This is hardcoded in the pipeline JSON and cannot be overridden per merchant — confirming what the tooltip and banner say.

### Why this is documented behaviour, not a bug

The tooltip names the statuses explicitly, so the constraint is disclosed in the UI. The fixed set is intentional: the per-day collection is a pre-aggregated cache (see [[analytics-top-order-products-sales-data-source]]) that depends on a stable status definition for cache coherence. The same set applies to **every** store — there is no per-store override.

### Contrast with configurable boxes

This differs from boxes like [[analytics-top-order-discounts]], which apply the merchant-configurable `cc_analytics.statuses` Setting at query time. If a merchant compares revenue between "Products by sales" and a configurable box and the totals differ, the status set is the usual reason.

## Related

- [[analytics-top-order-products-by-sales]] — hub.
- [[analytics-top-order-products-sales-data-source]] — the pre-aggregated collection the status set is baked into.
- [[analytics]] — Settings → Analytics → Order statuses (controls other boxes, not this one).
- [[analytics-top-order-discounts]] — contrasting box that honours the configurable status set.
- [[order]] — order entity; status / status_fulfillment fields.

## Open questions

_None._
