---
type: feature
nav_path: "Orders → Order details → History"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history", "Order audit log", "Order timeline", "Order activity", "История на поръчката", "Активност на поръчката"]
tags: [orders, history, audit, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 8
---
# Order history (audit log)

## Purpose

The **per-order audit log** — a chronological collapsible timeline of every change that has happened to one order: who did what and when. Merchants use it to investigate disputes (*"when exactly did this order's status change?"*), reconstruct the customer's journey, audit moderator activity, or debug an unexpected state.

Entries are **grouped by day**. Each entry shows an action icon, a short description, the acting party (admin / system / external integration), and the time. Entries that carry an `action_string` are **expandable** (accordion-style) — clicking the row reveals an extended detail panel. The log is **append-only** and **immutable** — corrections appear as new entries, never edits.

This page is the **hub** for the order-history cluster. The detail lives in the seven aspect pages below.

## Where to find it

From [[orders-details]] → embedded section / lazy-loaded panel (the parent page uses `data-box-ajax` to load this view inline). The merchant rarely visits the route directly.

Route: `/admin/orders/action/history/{order_id}`. The route returns a Smarty-rendered response that's swapped into the order details page. The whole timeline is **hidden when the order is still in DRAFT state** (`is_draft = 1`) — see [[orders-history-timeline-ui]].

## Sub-pages (in this cluster)

This page is split into seven aspect pages. The Assistant should drill into the aspect that matches the merchant's question, not read every page.

- [[orders-history-timeline-ui]] — the on-screen timeline: day-grouping, per-entry layout slots, expand/collapse chevron, draft-order hiding, abandoned-cart recovery banner, and what the merchant can / cannot do (no edit, no delete, no filter, no export).
- [[orders-history-action-codes]] — the **62 numbered action codes** (running to 63, including the returns block 58–63) + the 30 expandable sub-templates; what is deliberately NOT logged; the corrected code 21/22 = payment partial-refund / void (NOT product add/remove, which are 24/25).
- [[orders-history-record-model]] — the 8-field stored record schema; `date` doubles as created + updated; append-only by design; no retention / pruning (kept forever); `log_id` deep-dive link.
- [[orders-history-synthetic-entries]] — the two entries derived **at view time** and NOT stored: the synthetic `order_add` creation row and the `order_receipt_sent` row from the active invoicing app.
- [[orders-history-enrichment]] — view-time enrichment: translation-key locale rendering, custom-status (code 53) live name lookup, action 27 (fulfillment) waybill join, country-code → country-name resolution, app friendly-name lookup.
- [[orders-history-acting-party]] — the 3-step actor identification chain (admin → namespace → *"No such admin"*); why only the `api2` namespace shows a friendly **"API"** label; the role-type badge.
- [[orders-history-api-and-triggers]] — what mutations write a history row (admin panel AND JSON-API v2); the `api2` namespace on API writes; why the log is NOT itself a JSON-API v2 resource.

## What the merchant can do here

- **Read** the chronological per-day log of every order change. See [[orders-history-timeline-ui]].
- **Expand** entries that carry an `action_string` to see the per-action detail panel. See [[orders-history-action-codes]].
- **Identify** who made each change — admin username + role, an integration namespace, or *"No such admin"*. See [[orders-history-acting-party]].
- The merchant **cannot** edit, delete, filter, or export the log — it is a read-only immutable audit trail. See [[orders-history-timeline-ui]].

## Settings & fields

The history has **no merchant-editable settings** — it is a pure read surface populated as a side effect of order operations. The displayed time uses the merchant's configured `time_format` (the store-wide date/time format). For the stored record fields, see [[orders-history-record-model]]; for the displayed entry slots, see [[orders-history-timeline-ui]].

## Business rules

- **Hidden for draft orders** (`is_draft = 1`) — see [[orders-history-timeline-ui]].
- **Append-only, immutable, never pruned** — see [[orders-history-record-model]].
- **Two synthetic entries are derived at view time**, not stored — see [[orders-history-synthetic-entries]].
- **Several rows are enriched at view time** (locale, custom-status name, waybill, country names, app names) — see [[orders-history-enrichment]].
- **Only the `api2` namespace shows a friendly label** — every other integration shows *"No such admin"* — see [[orders-history-acting-party]].
- **JSON-API v2 mutations write to the same log** with namespace `api2` — see [[orders-history-api-and-triggers]].
- **Side effects:** none — the page is a pure read.

## Related

- [[orders-details]] — parent page that lazy-loads this view.
- [[orders]] — parent list.
- [[order]] — entity page.
- [[order-processing-pipeline]] — every history row maps to a pipeline event.
- [[settings-staff]] — admin identity shown on each entry comes from the staff list.
- [[settings-hooks]] — `order.created` / `order.updated` webhooks are independent of this in-app audit log.
- [[marketing-campaigns]] — abandoned-cart recovery campaigns drive the recovery banner.
- [[apps]] — pick_and_pack / ERP / shipping apps inject their own action types.
- [[api-orders]] — JSON-API v2 endpoint; mutations through it emit `api2` history rows.
- [[json-api-v2]] — API overview + side-effects principle.

## Open questions

None.
