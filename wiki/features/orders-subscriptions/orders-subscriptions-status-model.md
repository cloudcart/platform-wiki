---
type: feature
nav_path: "Orders → Subscriptions → Status & expiry model"
route_name: apps.membership.overview
route_path: /admin/orders/subscriptions
aliases: ["Subscription status model", "Computed subscription status", "Unlimited subscription", "expired = NULL", "No expiry cron", "Status filter gap", "Membership record fields"]
tags: [administration, membership, orders, subscriptions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Subscriptions — status, expiry & the minimal record

## Purpose

A customer membership record carries almost no fields: there is **no stored status**, no plan tier, no pricing snapshot — just the customer, product, page, and a single `expired` date. Everything the merchant sees as "status" is computed from that one date at read time. This page explains the derived states, what *Unlimited* means, why there is no expiry job, and the filter gap that hides unlimited rows.

> Part of [[orders-subscriptions]]. See the hub for the other aspects (overview list, auto-lifecycle, manual admin, integration).

## Where to find it

The status badge and *Active to* date render in the overview data-table ([[orders-subscriptions-overview]]); the storefront content-gate reads the same `expired` value to decide whether to unlock a page.

## What the merchant can do here

- Read a subscription's state from the badge and the *Active to* column.
- Filter by Active / Disabled (with the gap noted below).
- Disable a subscription by **deleting** it — there is no soft-disable / pause flag.

## Settings & fields

Membership records carry only: `customer_id`, `product_id`, `page_id`, `expired` (date). No status column, no tier, no price.

| Stored value | Derived status | Displayed |
|--------------|----------------|-----------|
| `expired = NULL` | Active / Unlimited | *"Unlimited"* in the date column; **Active** badge (the formatter returns `is_active = true` when `expired` is NULL). |
| `expired >= today` | Active | future date + green **Active** badge. |
| `expired < today` | Inactive (expired) | past date + grey **Inactive** badge (rendered *Disabled* in the status filter dropdown). |

## Business rules

### Status is COMPUTED — there is no "paused" state

The status shown in the list is derived from `expired`; there is no stored status field and therefore no soft-disable or "paused" subscription. To disable a subscription the merchant deletes it (see [[orders-subscriptions-overview]] for the Delete action).

### The status filter excludes Unlimited rows

The status filter applies a WHERE clause on `expired`:

- Active (1) → `expired >= today`.
- Disabled (0) → `expired < today`.

Rows with `expired = NULL` (the "Unlimited" subscriptions) match NEITHER side — they are EXCLUDED from both the Active and Disabled buckets. To view unlimited subscriptions the merchant must clear the status filter entirely. This is the single most common "where did my lifetime members go?" support question.

### List filter scope

Filters: customer (`customer_id IN list`), product (`product_id IN list`), pages (`page_id IN list`), date (`expired` date comparison), status (1 = active = `expired >= today`, 0 = disabled = `expired < today`). The search query field matches: `id`, customer email / first / last name, product name. (Full filter UI on [[orders-subscriptions-overview]].)

### NO cron / daily expiry job

There is NO daily cron that expires memberships. The `expired` date is just a stored timestamp — the list's "active" filter and the storefront's content-gate logic compare it to `now` at query time. A membership expires implicitly when its date passes; no automatic notification or status change happens at expiry. (The renewal-communication path is segment-driven — see [[orders-subscriptions-integration]].)

### Unlimited is reached three ways

`expired = NULL` (Unlimited) results from: a product-page link with `days = 0` on auto-create ([[orders-subscriptions-auto-lifecycle]]), a manual Create with `days = 0`, or an Add Extra Days call with `extra_days = 0` ([[orders-subscriptions-manual-admin]]).

## Related

- [[orders-subscriptions]] — hub.
- [[orders-subscriptions-overview]] — where the status badge / date / filters render.
- [[orders-subscriptions-auto-lifecycle]] — how the `expired` date is set / cleared on order events.
- [[orders-subscriptions-manual-admin]] — admin paths that set `expired = NULL`.
- [[orders-subscriptions-settings]] — the status taxonomy as documented on the Settings screen.

## Open questions

(none.)
