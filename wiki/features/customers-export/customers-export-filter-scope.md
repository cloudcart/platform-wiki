---
type: feature
nav_path: "Customers → Export customers → Filter scope"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_customers
aliases: ["Customer export filter scope", "Export filter state", "Filtered customer export", "Vue to legacy filter remapping", "Експорт по филтър"]
tags: [customers, export, filters, scope]
plan_gates: ["customer_export"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-export]]. See the hub for the other aspects (trigger & 2FA, sync vs async, CSV schema, plan & permissions).

# Export customers — filter scope

## Purpose

This aspect explains **which customers end up in the exported file**. The export inherits the filter state of the Customers list at the moment the button is clicked, so the merchant controls the scope by filtering the list first. It also documents the filter-key remapping between the Vue list and the export back-end, and why pagination / sort settings are ignored.

## Where to find it

The filters live on the Customers list ([[customers]]) — there is no separate filter UI on the export action itself. Apply filters, confirm the filtered subset in the list, then click **Export customers** (see [[customers-export-trigger-2fa]]).

## What the merchant can do here

### Respect filter state

The export uses whatever filters are applied on the Customers list at the moment the button is clicked. So the merchant can:

- Filter Customers by **active** / **banned** / **accept marketing** / **customer tag** / **customer group** / **country** / **state** ([[customers]] filters table).
- See the filtered subset in the list.
- Click **Export customers** → the CSV contains only that filtered subset.

If no filters are applied, the entire customer base is exported (subject to the synchronous-vs-queued threshold — see [[customers-export-sync-vs-async]]).

### What the merchant CANNOT do here

- Select individual customers by checkbox — the export always uses the FILTER scope, never a row selection.
- Export historical / deleted (soft-deleted) customers — only the live customer table is exported.
- Carry pagination or sort order into the file — those parameters are stripped (see below).

## Settings & fields

### Filter mapping (Vue → legacy export)

The Customers list (Vue) and the export back-end use slightly different filter key names. The platform automatically remaps them at export time:

| Vue list key | Export back-end key |
|--------------|---------------------|
| `accept_marketing` | `marketing` |
| `tag` | `customerTaggedWith` |
| `state` | `region` |

### Stripped parameters

Pagination / sort / per-page parameters from the list (`page`, `perpage`, `sort`, `order`, `direction`) are stripped — the export ignores them and always returns the full filtered set (subject to the row-limit threshold on [[customers-export-sync-vs-async]]).

## Business rules

### Filter captured at click time

The exporter applies the same `Filter` class the Customers list uses, so any filter combination supported in the list works on the export. The scope is the filtered set as it stands when the button is clicked; changing filters after the file is generated has no effect on the already-produced file.

### Pagination and sort never affect the export

Because pagination + sort parameters are stripped before the filter set is built, an export of page 2 of the list is identical to an export of page 1 — the file always contains the entire filtered set, not the visible page.

### No selection-based export

There is no checkbox-selection export from this surface. To narrow the export, the merchant narrows the list filters. This mirrors the behaviour of the orders export ([[orders-export-filter-scope]]).

## Related

- [[customers-export]] — hub.
- [[customers]] — the parent list page whose filters define the export scope.
- [[customers-custom-groups]] — customer groups usable as a filter (and a CSV column).
- [[orders-export-filter-scope]] — the equivalent filter-scope behaviour for orders export.

## Open questions

(All resolved.)
