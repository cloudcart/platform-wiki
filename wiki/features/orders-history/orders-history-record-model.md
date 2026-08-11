---
type: feature
nav_path: "Orders → Order details → History → Record model"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history record model", "History row schema", "Order audit storage", "History append-only", "История — модел на записа"]
tags: [orders, history, audit, data-model, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-history]]. See the hub for the other aspects (timeline UI, action codes, synthetic entries, enrichment, acting party, API & triggers).

# Order history — the stored record model

## Purpose

How a history entry is **stored**: the fields on each row, why it is append-only, why there is no separate updated timestamp, and why entries are never pruned. This is the reference for *"is the audit log reliable / complete / permanent?"* questions.

## Where to find it

The stored rows back the History panel on [[orders-details]]; the rendered view is documented in [[orders-history-timeline-ui]]. This page covers the data layer behind that view.

## What the merchant can do here

Nothing directly — the merchant cannot read or edit raw rows. The stored model determines what the timeline can show: because the table is append-only and never pruned, the merchant can rely on the timeline being **complete** and **permanent** for the life of the order.

## Settings & fields

### Record schema (8 fields)

Each history row stores:

| Field | Purpose |
|---|---|
| `order_id` | Which order. |
| `message` | Translation key / template name (the `message_data` fills placeholders). |
| `message_data` | JSON array of placeholders for the message template. |
| `admin_id` | Which admin took the action (null = system / customer / integration). |
| `action` | Numeric action code (see [[orders-history-action-codes]]). |
| `date` | When the event happened (used as both created + updated — see below). |
| `log_id` | FK to a system log table holding the full detailed payload. |
| `namespace` | App / integration that performed the action (see [[orders-history-acting-party]]). |

## Business rules

### `date` is both created AND updated

Both the created and updated timestamp accessors point at the same single `date` column. This is unusual — normally there'd be separate `created_at` + `updated_at`. The history is **append-only by design**: no UPDATE ever happens, so the created and updated dates trivially coincide.

### Manual timestamp management

The history table does **not** use the framework's automatic timestamps. The platform manages the `date` field manually (one column serving both created + updated semantics), avoiding dual-column overhead.

### Append-only model

Platform code never updates history rows — only `id` is guarded and timestamps are set manually on create. **Corrections happen as NEW history entries** describing the correction, never as edits to existing rows. This is why the timeline in [[orders-history-timeline-ui]] is immutable from the merchant's perspective.

### `log_id` for the deep-dive payload

The `log_id` references the full action payload in a separate logs table — the source of *"what exactly changed?"*. The history row is the summary; the linked log holds the full record. Action code 27 (fulfillment add) uses `log_id` to pull in waybill details; see [[orders-history-enrichment]].

### No retention / pruning — kept forever

There is **no** built-in cron / scheduler that purges old history entries. Records remain in the history table indefinitely. The merchant should expect to see entries from years ago on long-lived orders.

### Not every shown row is a stored row

Two entries in the rendered timeline are **synthesised at view time** and are NOT in the table — see [[orders-history-synthetic-entries]]. So the stored model is the bulk of the timeline but not 100 % of it.

### Side effects

None on read. Rows are **written** as a side effect of order operations; the write triggers are catalogued in [[orders-history-api-and-triggers]].

## Related

- [[orders-history]] — hub.
- [[orders-history-timeline-ui]] — how stored rows render.
- [[orders-history-action-codes]] — the `action` code stored on each row.
- [[orders-history-synthetic-entries]] — the rows that are NOT stored.
- [[orders-history-acting-party]] — how `admin_id` / `namespace` resolve to a "Placed by" label.
- [[orders-history-enrichment]] — how `log_id` enriches action-27 rows with waybill data.

## Open questions

None.
