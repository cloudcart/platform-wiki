---
type: feature
nav_path: "Analytics → Product discounts"
route_name: analytics
route_path: /admin/analytics
aliases: ["Product discounts", "Top product discounts", "Top order product discounts", "Most used product discounts", "Отстъпки за продукт", "Отстъпки върху продукти", "Най-използвани отстъпки за продукти"]
tags: [analytics, ccanalytics, orders, discount, product, top-order-product-discounts]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 9
---
# Product discounts

## Purpose

A ranked table of the merchant's **most-used product-level discounts** — *"Which discount rules are being redeemed on individual products, and how much margin am I giving away?"* Top 5 by total amount discounted, with units affected, order count, mobile/desktop split, and a per-product drill-down.

It is the **product-level** counterpart to [[analytics-top-order-discounts]]: that box counts discounts on the **whole cart/order subtotal** (e.g. "10% off any order over €100"); this one counts discounts on **specific products within a line-item** (e.g. "Buy-one-get-one on shoes"). They use separate data sources and share the default layout, with this one as the parent.

## Where to find it

Sidebar → **Analytics** dashboard. Box title **"Product discounts"** (not translated; body is). `navigationSort: 22`. Parent of the order-level [[analytics-top-order-discounts]] box in the default layout.

From the box: click a discount name to **edit it** (`/admin/discounts/edit/:id`) — only for non-deleted, non-manual discounts; **View more →** opens the per-product trail; **See details** opens the full paginated table.

## What the merchant can do here

### Dashboard card

Top 5 ranked by total discount amount (largest first), then `sales` descending. Each row:

| Field | What it shows |
|-------|---------------|
| `name` | Discount name + code (e.g. `Spring shoes (SPRING30)`). Null → `Manual discount`. |
| `meta.row1` ("Uses {value}") | **Units affected** — line-items that got it (NOT order count). |
| `aggregate` | Total discount amount, as positive currency. |
| `device` | Mobile/desktop split of orders. |
| `viewMore` | Drill-down link — present for real discounts; absent for manual/deleted. |

### Tooltip (box-level)

*"Most frequently used discounts on products in the order. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."* (BG shows the same status set.)

### Help-link states per row

Same 3-state indicator as the sister box:

| State | EN label | BG label | When |
|-------|----------|----------|------|
| `exists` | View discount | Виж отстъпката | Active — links to `/admin/discounts/edit/:id` |
| `deleted` | Deleted discount | Изтрита отстъпка | Deleted |
| `manual` | Manually created discount | Ръчно въведена отстъпка | Entered manually during order edit |

### Details — `/admin/analytics/details/top-order-product-discounts`

Paginated 100/page, 1 000-row cap. Compare disabled. Default sort `sales` desc. Columns:

| Column key | EN label | BG label | Meaning |
|------------|----------|----------|------|
| `page_name` | Name | Заглавие | Discount name + code |
| `sales` | Orders | Поръчки | Orders that applied it |
| `uses` | Uses | Използвания | Line-items affected (distinct from order count) |
| `amount` | Discount | Отстъпка | Total discounted in period |

### View More — per-order, per-product trail — `/admin/analytics/full/top-order-product-discounts/:discount_id`

A flat table (not a chart) of every product line that applied it. Columns:

| Column key | EN label | BG label | Meaning |
|------------|----------|----------|------|
| `date` | Date | Дата | Timestamp of the order |
| `name` | Name | Заглавие | (Export-only) Discount name |
| `order` | Order | Поръчка | Order number — links to `/admin/orders/edit/:id` |
| `product_name` | Product | Продукт | Product — links to the product edit screen |
| `type` | Discount type | Тип отстъпка | `Global discount` / `Discount code` / `Free shipping` |
| `amount` | Discount | Отстъпка | Discount amount on that single line |

### Details / View More toolbar

Same **reduced toolbar** as the sister box — Compare and Group disabled. The dashboard card shows none of these.

| Control | What it does | Gate |
|---------|--------------|------|
| **Date range picker** | Re-fetches. | Capped by `cc_analytics.compare_range` (default 12 months). |
| **Compare select** | **HIDDEN** on Details and View More. | — |
| **Group select** | **HIDDEN** on Details and View More. | — |
| **Export link** | Goes **directly to the 2FA modal** (no Export modal). | Hidden without `reports.reports_export`. |
| **Status-filter alert** | Yellow alert: *"Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled"*. Literally true here (see Business rules). | — |
| **Force-limit banner** | *"This report shows up to {total} results. To see all results, you can [Export]"* | Fires at the 1000-row cap. |

### Export flow (2FA / queue, no compare modal)

Export **bypasses the Export modal** and goes straight to the **2FA modal** ([[account-cc2fa]]) — 6-digit code, auto-submits `cc` if 2FA is off. It POSTs to `/admin/api/import-export/export_analytics`, queues, and toasts *"The export is being processed. You will receive an email with the download link."* A CSV is generated asynchronously, emailed, and listed in [[settings-import-history]]. Queue limit **150 000 rows**. The dashboard box caches its result per date-range for 60 seconds.

## Settings & fields

No box-specific settings. Date range filters all views; Compare and Group are locked off.

## Business rules

### Two distinct metrics: `sales` vs `uses`

This box reports **two** metrics (the sister box has one): `sales` = **orders** that applied the discount, `uses` = **product line-items** affected. One order with three discounted shirts is `sales=1, uses=3`. `uses` is **inferred** — total amount divided by per-unit discount, not the literal line quantity, so rounding can make the two differ.

### Status filter is FIXED at ingest — Settings do NOT affect this box

The key asymmetry versus the sister [[analytics-top-order-discounts]] box: data is pre-filtered when written, against a **hardcoded** status set — `paid OR completed OR authorized OR (pending AND not_fulfilled) OR fulfilled` — with no per-merchant filter at query time. So **changing Settings → Analytics → Order statuses does NOT affect Product discounts** (it applies to the order-level box only); the yellow status-filter alert is literally true here.

### Discount name resolution

No name → `Manual discount` / `Ръчна отстъпка`; name + code → `"{name} ({code})"`; otherwise the name. Renamed discounts show their **most recent** name.

### Only existing discounts are ingested; no double-count

Rows are written only for discounts that still exist at ingest; one deleted before a new order is captured is not ingested for that order, while older orders that already applied it are preserved (shown as **deleted**). This box has its own product-level data source, so a product carrying both an order-level and a product-level discount appears in **different boxes** — never double-counted.

### Product info only in View More; empty state

The affected product name and link are recorded per line but aggregated away on the Dashboard and Details — only View More shows them. Stores with no product-line discounts (or that use only cart-level discounts) see a blank card.

## How it works (verified against backend)

- **Three views** — Dashboard card, Details, View More — all from the same pre-aggregated product-discounts data, as a `table`-type box (not a chart). Endpoints under `/admin/api/analytics/.../top-order-product-discounts`; permission `reports` / `reports.analytics` + `reports` / `reports.reports`.
- **Ranking** — by total amount discounted (descending), then `sales`. Top 5 on the dashboard; Details capped at 1 000 discounts; export cap 150 000 rows.
- **View More name fallback** — for a renamed discount, the title resolves the current discount name directly.

## Related

- [[analytics]] — parent hub.
- [[analytics-top-order-discounts]] — sister box for **order-level** discounts (whole-cart) — same UI shape, different data source.
- [[analytics-details]] — generic Details sub-screen.
- [[analytics-full]] — generic View More sub-screen.
- [[discount]] — entity.
- [[discount-code]] — entity.
- [[marketing-discounts]] — admin screen for creating/editing discounts.
- [[discount-stacking]] — concept on multi-discount interaction.
- [[settings-statuses]] — used-statuses filter source.


## Open questions

_None._
