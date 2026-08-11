---
type: feature
nav_path: "Apps → Microinvest → Sync debug (internal)"
route_name: apps.microinvest.tasks
route_path: /admin/apps/microinvest/tasks
aliases: ["Microinvest sync debug", "erpTasks", "erpTaskXml", "what Microinvest sent", "ERP task XML", "Microinvest Tasks tab", "ERP task payload"]
tags: [apps, erp, microinvest, debug, graphql, internal]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 2
---

> Part of [[apps-microinvest]]. See the hub for the other aspects (settings, sync model, product matching, reset import).

# Microinvest — sync debug (inspect what Microinvest sent)

> **INTERNAL USE ONLY.** The GraphQL queries below are a CloudCart-staff debugging facility — not part of the merchant-facing API, and not to be handed to merchants. Use them for internal sync investigations; surface only the *conclusion* (what was wrong, what to fix) to the merchant.

## Purpose

When a sync looks wrong (a product didn't update, a price / stock is off, an order didn't post), the load-bearing question is *"what did Microinvest actually send?"* — this aspect covers how staff read the raw received payload.

## Where to find it

The **Tasks tab** ([[apps-microinvest-settings]]) is the UI: each task's detail panel shows its XML. The **same data is on the admin GraphQL API** (`POST /graphql`, authenticated admin session) via two queries — the faster path when investigating.

## What the merchant can do here

Nothing — this is a staff-only investigation path. The merchant only sees the Tasks tab; the queries are not exposed to them.

## Settings & fields

No settings — two read-only GraphQL queries.

## Business rules

### `erpTasks` — list the ERP background tasks

Paginated; returns a JSON list of id / status / type / timestamps. The Tasks tab is a **parent → children tree**: omit `parentId` for the top-level tasks, then pass a task's id as `parentId` to list its children.

```graphql
query {
  erpTasks(key: "microinvest", first: 15, page: 1) # top-level tasks
}
query {
  erpTasks(key: "microinvest", parentId: "<PARENT_TASK_ID>") # that task's children
}
```

### `erpTaskXml` — the raw XML the ERP sent for one task

Take the failing task's id from `erpTasks` and read exactly what arrived (the same payload the task detail view shows):

```graphql
query {
  erpTaskXml(key: "microinvest", id: "<TASK_ID>")
}
```

Returns the XML as a string, or `null` if that ERP exposes no task-detail view.

### Both queries are ERP-generic

The same pair works for any ERP integration by swapping `key` (e.g. `"gensoft"`, `"selmatic"`); `"microinvest"` is just this app's key. The standard diagnosis for a Microinvest sync ticket is: `erpTasks` → find the suspect task → `erpTaskXml` → compare the received XML (its `BarCode1` / `BarCode2` / `Code`) against what was expected, alongside the matching check on [[apps-microinvest-product-matching]].

## Related

- [[apps-microinvest]] — hub.
- [[apps-microinvest-settings]] — the Tasks tab UI these queries sit behind.
- [[apps-microinvest-product-matching]] — pair the payload with the two-layer match check.
- [[external-record-mapping]] — the `externalMetaData` / `externalMetaIntegrations` queries for reading the mapping rows.

## Open questions

(none)
