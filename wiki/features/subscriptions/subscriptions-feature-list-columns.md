---
type: feature
nav_path: "Profile → My subscriptions → List columns"
route_name: subscriptions-list
route_path: /admin/details/subscriptions
aliases: ["Subscriptions list columns", "Subscriptions list grid", "My subscriptions columns", "Subscriptions row expand", "Subscriptions filters", "Колони на абонаментите"]
tags: [subscriptions, list, billing, account, columns, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions]]. See the hub for the other aspects (actions, status state machine, renewal retry, types, notifications & pricing).

# Subscriptions — list columns, expand row, filters

## Purpose

This aspect documents the **list grid itself** on [[subscriptions]] — the 9 columns the merchant sees, the per-row expand toggle that previews recent transactions inline, the 2 filters (Status, Type), the default sort order, and the source endpoint backing the page. It is the answer to merchant questions in the form *"what do those columns mean?"* and *"why are these rows in this order?"*.

## Where to find it

Top-right **profile avatar** dropdown → **My subscriptions**. The grid renders at `/admin/details/subscriptions`. See the hub [[subscriptions]] for the broader navigation context.

## What the merchant can do here

- Scan the 9 informational columns to see what each subscription costs, when it next renews, what its current status is, and how many failed renewal attempts have accumulated.
- Click the **expand toggle** on the **Name** column to drop the row open and preview recent transactions inline (without leaving the page).
- Filter the list by **Status** and / or **Type** (multi-select) — see the Filters table below.
- Sort by Status (the only sortable column). Default sort is Status descending so Active rows surface above Canceled rows.

## Settings & fields

### List columns (9)

| Column | Sortable | Notes |
|--------|----------|-------|
| **Name** | No | The subscription's description: e.g., *Plan: Business — Year*, *Application: Algolia*, *Feature: 1000 extra products*. Has an **expand toggle** that drops the row open to show this subscription's recent transactions inline (see "Expandable row" below). |
| **ID / Date** | No | The subscription's `unique_id` + the `updated_at` date. The ID is also a clickable link into [[subscriptions-detail]]. |
| **Price** | No | The subscription's current per-cycle price, formatted in the subscription's currency. |
| **Billing period** | No | `One time` / `Monthly` / `Year` / `2 years` — translated from the underlying `billing_period` value. One-time subscriptions render with no recurring fields. |
| **Next billing date** | No | When the next renewal will be attempted. Empty for one-time subscriptions and for permanently terminated subscriptions. |
| **Next billing amount** | No | The amount that will be charged at the next renewal (may differ from `Price` for promo / first-cycle pricing — see [[subscriptions-feature-notifications-pricing]]). |
| **Status** | **Yes** (default sort) | Badge — `Active` / `Canceled` / `Past due` / `Expired`. See [[subscriptions-feature-status-state-machine]] for what each badge means. |
| **Failed attempts** | No | Count of consecutive failed renewal charges (0 when healthy). After 5 the auto-retry loop stops; see [[subscriptions-feature-renewal-retry]]. |
| **Actions** | No | State-conditional buttons: **Cancel** (Active), **Renew** (Canceled / Expired), or **Renew + Cancel** (Past due). See [[subscriptions-feature-actions]] for the full button matrix. |

Default sort: **Status descending** (so Active rows surface first). Default page size: 25.

### Source endpoint

The list reads from `/admin/api/core/subscriptions` (paginated, with `status` and `type` filters applied via query string). Fields displayed are aggregates of the underlying subscription record:

| Field | Source | Notes |
|-------|--------|-------|
| `unique_id` | subscription ID | A short opaque token (e.g., `66b3fa1...`). Same value powers the URL `/admin/details/subscriptions/<unique_id>`. |
| `name` | Derived from the linked model (Plan / App / Feature pack / Service / Theme) | E.g., *Plan: Business — 12 months*. See [[subscriptions-feature-types]] for the mapping. |
| `price` / `price_formatted` | Per-cycle price | Stored in cents; formatted with the subscription's currency. |
| `billing_period` | Derived from `billing_cycle` (months) | `once` → null, `month` → 1, `year` → 12, `2years` → 24, else literal months. |
| `next_billing_date` | When the platform will attempt the next charge | Null for one-time / fully cancelled. |
| `next_billing_amount` / `next_billing_amount_formatted` | Amount of the next charge | May be a promo price for the first cycle, then the regular price thereafter — see [[subscriptions-feature-notifications-pricing]]. |
| `status` | One of `1` (Active), `0` (Canceled), `2` (Past due), `3` (Expired) | See [[subscriptions-feature-status-state-machine]]. |
| `failed_attempts` | Consecutive failed renewal charges | Resets to 0 on a successful charge. |
| `model_type` | `plan_details` / `cloudcart_app` / `cloudcart_feature` / `cloudcart_service` / `theme` | Maps to the **Type** column. |
| `lta_contract_id` | Set when this subscription belongs to a contract | When set, the Action column is empty. |

### Expandable row (inline transaction preview)

Clicking the expand toggle on the **Name** column drops the row open to a panel listing this subscription's recent transactions (date, description, amount, approved / declined badge, response message for declined, and a **Download** invoice button for approved). The expandable row uses the same Billing API as the dedicated transactions list — it's a quick-look without leaving the page. For the full transaction history see [[subscriptions-transactions]].

### Filters (2)

| Filter | Options |
|--------|---------|
| **Status** | `Active` / `Canceled` / `Past due` / `Expired`. |
| **Type** | Multi-select — `Feature` (feature packs), `Application` (paid apps), `Service` (Expert Services), `Plan` (the store's main plan subscription). |

(There's no filter for "Theme" subscriptions even though the platform stores them; they're surfaced only on the row's Type column.)

The Status filter values map: Active=1, Canceled=0, Past due=2, Expired=3 (matches the platform constants). Type filter uses string keys: `cloudcart_feature`, `cloudcart_app`, `cloudcart_service`, `plan_details`.

## Business rules

- **Default sort differs between UIs.** The modern Vue list orders by `status DESC` so Active surfaces first. The legacy Smarty list ordered by `updated_at DESC` — a different default per UI generation. Both pages back the same data; only the ordering changes.
- **No CSV / Excel export** exists on this screen. The list is browse-only.
- **No bulk actions.** Every row is one-at-a-time — see [[subscriptions-feature-actions]] for action semantics.
- **Soft-cancelled rows remain visible.** Cancel never deletes a subscription row — past cancelled subscriptions stay in the list (filterable by Status = Canceled) and their transaction history / invoices remain downloadable. See [[subscriptions-feature-status-state-machine]] for the soft-delete behaviour.
- **One-time subscriptions appear without recurring fields.** When `billing_cycle` is null, the row renders with `Billing period = One time`, no `Next billing date`, no `Next billing amount` — and no Action buttons. The merchant can still download the invoice. See [[subscriptions-feature-types]] for one-time semantics.

## Related

- [[subscriptions]] — hub.
- [[subscriptions-detail]] — per-subscription view (drilled into via the ID link).
- [[subscriptions-transactions]] — full transaction history (the expandable row is a preview).

## Open questions

(None.)
