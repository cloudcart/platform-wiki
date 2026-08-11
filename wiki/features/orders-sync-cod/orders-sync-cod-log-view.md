---
type: feature
nav_path: "Orders → COD sync → Log view"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync log", "COD sync grid", "COD sync table", "COD sync usage banner", "COD sync empty state"]
tags: [orders, cod, sync, smarty, ui]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# COD sync — log view

> Part of [[orders-sync-cod]]. See the hub for related aspects (eligibility, polling job, status flip, errors, quota, manual alternatives).

## Purpose

The visible UI of the COD sync page: the usage banner at the top, the read-only sync-event grid below it, the Provider filter, and the empty state. This is the surface the merchant actually looks at to confirm "did the courier report my COD orders as paid this month?".

## Where to find it

Sidebar → Orders → **COD sync** (or directly via `/admin/orders/sync/cod`).

## What the merchant can do here

- Read the log of COD sync events for the current calendar month.
- Filter the grid by courier provider.
- Click an Order ID to preview the order in a side panel.
- See remaining COD-sync capacity in the usage banner (full quota mechanics on [[orders-sync-cod-quota]]).

## Settings & fields

### Usage banner (top)

A two-column info banner:

**Left column** — usage stats:
- **Period** — the current calendar-month range as `d.m.Y - d.m.Y` (e.g., `01.05.2026 - 31.05.2026`).
- **Used** — how many sync events have been consumed this period.
- **Remaining** — capacity left for this period.
- When **Remaining = 0**: a red *"Add more COD"* link appears (see [[orders-sync-cod-quota]]).

**Right column** — generic explanatory info text (`order.info.text` translation key).

### List table (when records exist)

When the merchant has at least one synced COD order in the current month:

| Column | Notes |
|--------|-------|
| **Datetime** | When this sync event happened (`d.m.Y H:i` format). |
| **Order ID** | The order's ID. Clickable — opens the order in a side-panel preview (uses `data-ajax-panel`). |
| **Action** | What the sync detected — see the vocabulary below. |
| **Courier** | The courier provider that returned the status. |

### Action column vocabulary (verified)

Each row's Action column shows one of three values:
1. **Default sync label** — *"Sync"* — the sync ran but didn't detect a status change.
2. **Success with amount** — e.g., *"Paid: 45.00 BGN"* — the courier reported a successful COD collection with the received sum.
3. **Error string** — the platform stores the courier's error message in the `sync_payment_error` meta field and shows it verbatim. The full error categorisation is on [[orders-sync-cod-errors]].

There is no separate "Refused" / "Unchanged" enum — those fall under the default Sync label unless the courier returns a specific error.

### Filter

| Filter | Operator codes | Notes |
|--------|----------------|-------|
| **Provider** (`codprovider`) | 1=Is, 2=Is not | Pick from configured shipping providers that have sync enabled. |

The Provider filter is populated from the OmniShip layer's list of currently-enabled COD-sync providers (couriers installed in [[apps]] / [[shipping]], with COD-sync explicitly enabled and valid credentials). Removing a courier from active providers also removes it from this filter.

### Empty state

When no records exist for the current month:
- *"No COD sync records yet"* (`order.notify.no_records_yet`).
- A help paragraph using a COD-specific translation (`order.notify.no_records_help_cod`). The platform's stock translation reads *"You have no synchronized orders to check the payments imposed"* — wording carried over from the original implementation; the merchant might find it less clear than expected. The actual remediation is to ensure (1) a courier with COD-sync is installed, (2) it has valid credentials, and (3) the merchant has paid COD orders in their pipeline.

## Business rules

### Current-month scope — hard-coded

The list filters to orders placed within the current calendar month (start-of-month to end-of-month, on the order's `date_added` field). The filter is on the order's `date_added`, **NOT** the sync event's date — so even sync events that happened today may be excluded if the underlying order was placed last month. For historical access the merchant uses each order's individual history page ([[orders-history]]).

### One row per order — latest sync only

The grid queries the orders table directly (not a separate sync-log table), grouping by `order_id`. If an order was synced multiple times this month (e.g., first sync detected nothing, second detected the payment), the grid shows **one row per order with the latest sync's metadata**. Earlier sync events on the same order are not visible here — the merchant looks at the order's own history ([[orders-history]]) for the full timeline.

### Side-panel preview for orders

Clicking an Order ID opens the order in a side-panel preview (the platform's slide-from-right panel) rather than navigating away, so the merchant can inspect the order without losing the log context.

### Read-only audit view

No bulk actions and no per-row edit/delete. The grid wrapper loads its rows over AJAX (`data-url` pointing at the COD-sync route); the Provider filter uses Select2. Side effects on this page: **none** — syncs are triggered by the background-job system, not by this page. See [[orders-sync-cod-polling-job]].

## Related

- [[orders-sync-cod]] — hub.
- [[orders-details]] — the side-panel preview opens this.
- [[orders-history]] — full per-order sync timeline (older than current month, or multiple syncs on one order).
- [[shipping]] — courier integrations that populate the Provider filter.
- [[apps]] — courier apps that implement COD sync.

## Open questions

None.
