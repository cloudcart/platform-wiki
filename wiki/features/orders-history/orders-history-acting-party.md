---
type: feature
nav_path: "Orders → Order details → History → Acting party"
route_name: admin.orders.history
route_path: /admin/orders/action/history/:order_id
aliases: ["Order history acting party", "History placed-by", "Who made the change", "History No such admin", "История — извършител"]
tags: [orders, history, audit, gdpr, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-history]]. See the hub for the other aspects (timeline UI, action codes, record model, synthetic entries, enrichment, API & triggers).

# Order history — acting-party identification

## Purpose

How the timeline answers *"who did this?"* for each entry — the "Placed by" slot. This is the section a merchant relies on for audit / GDPR work (*"which staff member changed this order?"*) and for distinguishing manual admin work from automated integrations.

## Where to find it

The "Placed by" slot is the third column of each entry in the History panel on [[orders-details]] — see [[orders-history-timeline-ui]] for the full row layout.

## What the merchant can do here

The merchant **reads** who performed each action. They cannot change attribution — it is recorded when the row is written. The displayed actor is one of: an admin (username + role badge), an integration namespace, or the *"No such admin"* fallback.

## Settings & fields

No editable settings. The "Placed by" value resolves from the row's `admin_id` and `namespace` fields (see [[orders-history-record-model]]) through a fixed 3-step chain:

| Step | Condition | Displayed |
|---|---|---|
| 1. Admin | The action was done by a logged-in admin | Username (mailto link) + role badge |
| 2. Namespace | No admin; an integration triggered it | The namespace string — **only** if it equals `api2` (renders as **"API"**) |
| 3. Fallback | Neither resolves | *"No such admin"* (`admin.err.no_such_admin`) |

## Business rules

### 3-step fallback chain

The platform identifies the actor in this order:

1. **Admin** — when a logged-in admin performed the action, shows their username as a mailto link plus a role badge.
2. **Namespace** — when an external integration (ERP, courier, payment provider) triggered the action, the row carries a `namespace` string identifying the integration.
3. **No such admin** — the fallback when the original actor is unknown or deleted.

### Only `api2` shows a friendly label — every other namespace falls through

This is the key correction to the simple "namespace identifies the integration" story. Namespaces **are** stored on the row, but the **only** namespace value that the UI renders as a friendly label is `api2` → shown as **"API"** (actions triggered through JSON-API v2 — see [[orders-history-api-and-triggers]]). Every other namespace value — including **all** module / app / integration namespaces — resolves to `null` in the display logic, which causes the template to fall through to *"No such admin"*.

So a merchant auditing JSON-API v2 operations sees **"API"** next to those rows, but actions performed by apps / ERP / courier integrations appear as *"No such admin"* — even though a namespace is stored. The stored `namespace` is therefore richer than what the merchant sees.

### Role badge is the admin TYPE, not specific permissions

The *"(owner)"* / *"(moderator)"* badge next to the actor's username is the admin's `type` (owner / moderator) — NOT their specific permission set. A moderator with broad permissions is shown identically to a moderator with narrow permissions. Staff identities come from [[settings-staff]].

### Side effects

None — pure read.

## Related

- [[orders-history]] — hub.
- [[orders-history-timeline-ui]] — the row layout where this slot appears.
- [[orders-history-record-model]] — the `admin_id` / `namespace` fields resolved here.
- [[orders-history-api-and-triggers]] — why `api2` is the one namespace shown as "API".
- [[settings-staff]] — admin identities + types behind the username + role badge.

## Open questions

None.
