---
type: feature
nav_path: "Settings → Statuses"
route_name: statuses
route_path: /admin/settings/statuses
aliases: ["Statuses", "Order statuses", "Shipping statuses", "Payment statuses", "Статуси", "Статуси на поръчки", "Статуси на доставки", "Статуси на плащания"]
tags: [settings, statuses, orders, payments, shipping]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Statuses

## Purpose

The screen where the merchant manages three independent status taxonomies that drive how every order, shipment, and payment in the store is labelled and routed:

- **Order statuses** — the high-level workflow state of an order (`pending`, `paid`, `completed`, `refunded`, etc.). The merchant can rename built-ins, add custom ones, and delete custom ones (with protection against deleting in-use statuses). See [[settings-statuses-orders-tab]].
- **Shipping (fulfillment) statuses** — the warehouse-state of an order (`not_fulfilled`, `fulfilled`). Rename only — the taxonomy is platform-defined and cannot be extended. See [[settings-statuses-shipping-tab]].
- **Payment statuses** — the low-level state of payment processing (`authorized`, `completed`, `failed`, `refunded`, etc.). Rename only. See [[settings-statuses-payment-tab]].

Status renames are **translation overrides**: the original built-in status code stays the same (e.g., `pending`) but the merchant-facing label can be customised per store (e.g., "Awaiting confirmation"). See [[settings-statuses-rename-mechanic]] for the precedence rules vs [[settings-translations]].

## Where to find it

Sidebar → Settings → **Statuses**.

The page's breadcrumb reads "Settings → Statuses → `<active tab>`". The route is `/admin/settings/statuses` (root); the page is a tabbed wrapper whose Orders tab (`/admin/settings/statuses/order`) is the default/first tab. (The root path has no explicit router-level redirect — there is no `index` child on the `statuses` route — so the active tab is driven by the tabbed wrapper's tab navigation, with Orders listed first.) The header icon is the stream icon.

### Sub-screens

Distinct routes within this feature.

| Label | Route name | Route path |
|-------|------------|------------|
| Statuses (root) | `statuses` | `/admin/settings/statuses` |
| Orders | `order-statuses` | `/admin/settings/statuses/order` |
| Shipping | `shipping-statuses` | `/admin/settings/statuses/shipping` |
| Payment | `payment-statuses` | `/admin/settings/statuses/payment` |

## Sub-pages (in this cluster)

This page is split into seven aspect pages. The Assistant should drill into the aspect that matches the merchant's question, not read every page.

- [[settings-statuses-orders-tab]] — the Orders tab: 11 built-in order statuses, add-custom modal, inline rename, delete-custom action.
- [[settings-statuses-shipping-tab]] — the Shipping tab: 2 built-in fulfillment statuses, rename only, no add / delete.
- [[settings-statuses-payment-tab]] — the Payment tab: 13 built-in payment statuses set by gateway callbacks, rename only.
- [[settings-statuses-rename-mechanic]] — how rename works as a translation override; precedence vs [[settings-translations]]; clearing deletes the override row.
- [[settings-statuses-custom-codes]] — how a custom status NAME maps to an internal CODE (slugify + numeric suffix on collision); integration consequences of renaming vs deleting + re-creating.
- [[settings-statuses-delete-protection]] — the attached-orders count gate; archived-order rule; carrier-locked shipping statuses; error wording.
- [[settings-statuses-permissions-validation]] — `settings.statuses` permission grant for moderators; server-side Form Request validation rules; route-level `type` constraints.

## What the merchant can do here

In summary: rename any built-in status across the three taxonomies (inline edit + per-row Save button — no auto-save on blur or Enter), add a new custom order status, and delete a custom order status (only if no orders are attached). Each aspect page above documents one slice of the surface. The merchant CANNOT delete built-in statuses, change the underlying status CODE, set per-language labels here (use [[settings-translations]] for that), or reorder the table — see [[settings-statuses-rename-mechanic]] and [[settings-statuses-orders-tab]] for the full list of restrictions.

## Settings & fields

The page's own fields are documented per tab:

- [[settings-statuses-orders-tab]] — Orders table columns (Current name / New name / Actions) + Add-status modal + Delete confirmation popover.
- [[settings-statuses-shipping-tab]] — Shipping table columns (rename-only).
- [[settings-statuses-payment-tab]] — Payment table columns (rename-only).

Saves are immediate per row — there is no page-level draft / Save All button. The page consumes settings owned elsewhere:

- [[settings-cart]] — `order_status_for_quantity_decrease` (picks `paid` vs `pending` for when stock decrements — see [[inventory-decrement-timing]]).
- [[settings-translations]] — per-language overrides of platform translation keys for status labels (see [[settings-statuses-rename-mechanic]] for precedence).
- [[settings-admin-notifications]] — `order_status_change` and `order_payment_status_change` notification toggles.

## Business rules

The three taxonomies have different write capabilities, summarised in one table — full mechanics on each aspect page:

| Taxonomy | Built-in count | Can add? | Can rename? | Can delete? |
|----------|----------------|----------|-------------|-------------|
| **Order** | 11 | Yes (custom statuses) | Yes | Yes (only custom, only if no orders attached) |
| **Shipping** (fulfillment) | 2 | No | Yes | No |
| **Payment** | 13 | No | Yes | No |

The Add and Delete UI affordances are gated by both client (tab-driven Vue checks) and server (route-level `->where('type', 'order')` constraint). Status renames and adds do NOT fire queued jobs, admin notifications, or webhooks from this page — the status taxonomy is purely platform-internal metadata. Operations that subscribe to "order status changed" fire from the order itself, not from this management page.

No explicit plan gate on this page — the three taxonomies are core platform functionality.

## Related

- [[settings]] — parent hub.
- [[settings-cart]] — `order_status_for_quantity_decrease` setting picks `paid` vs `pending` for when stock decrements.
- [[settings-translations]] — per-language overrides; interacts with renames per [[settings-statuses-rename-mechanic]].
- [[settings-admin-notifications]] — `order_status_change` and `order_payment_status_change` notifications fire when these statuses change.
- [[settings-hooks]] — merchants can subscribe webhooks to order status change events; the status CODE (not the renamed label) is sent in webhook payloads.
- [[settings-invoicing]] — `credit_payment` rule on the credit-note tab references payment statuses.
- [[settings-staff]] — moderator grants; the `settings.statuses` permission is required for this page.
- [[order]] — entity page; uses these statuses on every record.
- [[order-status]], [[shipping-status]], [[payment-status]] — entity pages.
- [[customer]] — customer detail page shows orders grouped/filtered by status using these labels.
- [[order-status-workflow]] — concept page on how statuses transition.
- [[orders-status-change]] — the order-side flow for changing a status (consumes this taxonomy).
- [[checkout-flow]] — checkout creates the order in a starting status.
- [[order-processing-pipeline]] — custom statuses don't write a history row through this pipeline — they use a separate path.

## Open questions

_None._
