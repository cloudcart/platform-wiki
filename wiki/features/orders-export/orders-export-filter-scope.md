---
type: feature
nav_path: "Orders → Export → Filter scope"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders
aliases: ["Orders export filter", "Orders export scope", "Export current filter", "Export selected orders", "Export archived orders", "Export SQL snapshot"]
tags: [orders, export, filters, scope]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-export]]. See the hub for related aspects (trigger / 2FA, sync vs async, CSV schema, delivery, permissions / plan).

# Orders export — filter scope

## Purpose

Documents **which rows the export includes** — the filter pipeline that mirrors the orders list, the absence of a selection-based bulk export, the archived-orders rule, and the SQL-snapshot semantics for async exports (chunks read against the click-time slice, not the current state).

## Where to find it

The merchant configures scope from [[orders]] — the standard filter row (status, date range, customer, payment provider, etc.) and the Archived toggle. **There is no scope UI in the Export modal itself** — the filter is whatever's currently applied to the list.

## What the merchant can do here

- Narrow the orders list by any filter the list supports (status, date range, customer, payment, courier, currency, etc.).
- Toggle Archived to include / exclude archived orders.
- Use a search query in the list — the export pipeline reads the same filter as the list, so search terms apply.

The merchant CANNOT:

- Select specific orders by checkbox and export only those — there is no "Export selected" bulk action on this list (unlike [[orders-invoices]] which DOES support per-selection bulk download / export).
- Change filters after the modal opens and have them apply — the filter is **captured at click time** (see below).
- Specify a filter from the URL that the orders list doesn't already support — the modal's `extra` payload is sanitised to only `ids` + `dates`.

## Settings & fields

### Sanitised `extra` payload

The modal's form action URL passes `extra` (a sanitised array with only `ids` and `dates` keys) so the merchant's filter scope survives the modal round-trip. The platform validates `extra` via the export validation step — values outside `{ids, dates}` are **stripped**, preventing arbitrary query tampering through the modal layer.

The full list-filter context (status, customer, payment provider, etc.) is captured separately as part of the export request — the `extra` channel is the supplementary scope passed through the 2FA round-trip.

## Business rules

### Filter captured at click time

The export reads from the same filter pipeline as the orders list. Whatever filters / search the merchant has applied via the orders list URL are also applied to the export query. So:

- "Status = Paid + Date = This month" → exports only paid orders from this month.
- No filter → exports the full order history.

The merchant should set the filter **BEFORE** clicking Export. Changing the URL filter after the modal opens has no effect — the filter is captured at export-trigger time.

### Async path — SQL snapshot consistency

The async path passes a serialised SQL snapshot of the filter query to the queue worker. The worker reuses that same SQL slice for each chunk. This means: **if the merchant adds / changes / deletes orders between clicking Export and the queue running, the export reflects the SQL snapshot from the click time, not the current state.** For audit / accounting use this is the desirable behaviour — every chunk sees a consistent slice.

### No selection-based export

The orders list has no "Export selected" bulk action. For orders, the merchant ALWAYS narrows by filter, never by row checkbox, before exporting. Contrast with [[orders-invoices]], which supports per-selection bulk PDF download.

### Archived orders follow the current filter

The export pipeline shares the orders list's filter for the `archived` parameter:

| Archived filter state | Export includes |
|---|---|
| Unset (default) | Both active and archived orders. |
| `yes` | Only archived orders. |
| `no` | Only active (non-archived) orders. |

To exclude archived orders, the merchant applies **Archived = no** in the orders list before clicking Export.

### Multi-currency caveat

The price columns use each order's currency individually — see [[orders-export-csv-schema]]. For multi-currency stores, the merchant should filter by currency in the orders list first to get a clean single-currency export, otherwise the resulting CSV contains rows in mixed currencies.

### Narrowing forces sync mode

A filter that returns ≤ 50 rows routes through the synchronous path documented in [[orders-export-sync-vs-async]] — instant browser download, no queue. The merchant who needs an instant CSV (and no email round-trip) can use the filter as a deliberate lever: narrow to ≤ 50, click Export.

## Related

- [[orders-export]] — hub.
- [[orders]] — the list whose filter is mirrored by the export.
- [[orders-export-trigger-2fa]] — the modal that preserves the filter via the `extra` payload.
- [[orders-export-sync-vs-async]] — the SQL snapshot is what each async chunk reads against.
- [[orders-export-csv-schema]] — the currency / row-layout caveat that interacts with filter choices.
- [[orders-invoices]] — contrast: selection-based bulk export IS supported there.

## Open questions

None.
