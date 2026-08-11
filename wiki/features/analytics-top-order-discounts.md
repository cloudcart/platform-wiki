---
type: feature
nav_path: "Analytics → Order discounts"
route_name: analytics
route_path: /admin/analytics
aliases: ["Order discounts", "Top order discounts", "Most used order discounts", "Отстъпки за поръчка", "Най-използвани отстъпки за поръчка"]
tags: [analytics, ccanalytics, orders, discount, top-order-discounts]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 9
---
# Order discounts

## Purpose

A ranked table of the merchant's **most-used cart/order-level discounts** for the selected time range. Answers: *"Which of my discount rules — coupon codes, global cart promotions, free-shipping rules — are actually being redeemed, and how much money are they costing me?"* Shows the top 5 by total discount amount given out, with usage count, mobile/desktop split, and drill-down to per-order history.

It is paired with [[analytics-top-order-product-discounts]] — that sister box covers **product-level** discounts (per line-item), while this one covers **order-level** discounts (applied to the whole cart). Both appear together in the default layout.

## Where to find it

Sidebar → **Analytics** dashboard. The box title is **"Order discounts"** (the BG localisation in `bg.json` is left as the English string). In the default sort (`navigationSort: 23`) it appears nested under the **Product discounts** parent; the merchant can flip the order via Settings → Analytics → Dashboard layout.

From the box, the merchant can click a discount name to **edit the discount** (`/admin/discounts/edit/:id`, only for non-deleted, non-manual discounts), **View more →** for per-order usage history, or **See details** for the full paginated table.

## What the merchant can do here

### Dashboard card

Top 5 discounts ranked by **largest discount given out first**, then usage count descending. Each row shows the discount **Name** (code in parens when attached, e.g. `Summer sale (SUMMER20)`; nameless ones show `Manual discount`), a **"Uses {value}"** usage count, the total **Amount** as positive money, the **mobile/desktop split**, and a **drill-down** link — present only when the discount has a real id (hidden for manual / deleted).

### Tooltip (box-level)

**EN**: *"Most frequently used discounts to the total value of the order. The data is visualized according to the following statuses of orders - Paid, Completed, Pending, Authorized payment, Fulfilled."* (BG: *"Най-често използвани отстъпки към общата стойност на поръчката…"* with the same status list.)

### Help-link states per row (`PageHelp` icon)

- `exists` — **View discount** / **Виж отстъпката** — discount still active; click opens its edit screen at `/admin/discounts/edit/:id`.
- `deleted` — **Deleted discount** / **Изтрита отстъпка** — discount has been deleted; link disabled.
- `manual` — **Manually created discount** / **Ръчно въведена отстъпка** — a manual discount entered at order-edit time (not from a rule).

### Details — `/admin/analytics/details/top-order-discounts`

Paginated 100/page, 1 000-row hard cap, comparison disabled, default sort usage count desc. Columns: **Name** (Заглавие — discount + code), **Sales** (Поръчки — usage count), **Discount** (Отстъпка — total amount), plus the three-state help icon above.

### View More — per-order usage trail — `/admin/analytics/full/top-order-discounts/:discount_id`

Flat table (no time-bucketing, no comparison) listing every order that applied this discount. Columns: **Date** (Дата), **Order** (Поръчка — links to `/admin/orders/edit/:id`), **Discount type** (Тип отстъпка — `Global discount` / `Discount code` / `Free shipping`), and **Discount** (Отстъпка). Export adds a Name (Заглавие) column.

### Details / ViewMore toolbar

This box has the **most reduced toolbar** of any top-N box. The dashboard box itself shows none of these controls — they are page-wide on Details / ViewMore:

- **Date range picker** — re-fetches; capped by `cc_analytics.compare_range` (default 12 months).
- **Compare select** and **Group select** — both **HIDDEN** on this box. Even when the dashboard compare selector is set to "previous period", Details / ViewMore ignore it; and ViewMore is a flat per-order trail, not a time-bucketed chart.
- **Export link** — goes **directly to 2FA modal** (no ExportModal — there's no compare option to ask about); hidden without `reports.reports_export`.
- **Status-filter alert** — permanent yellow alert: *"Data is visualized according to the default statuses in Settings and cannot be changed → Paid, Completed, Pending, Authorized payment, Fulfilled"*. **Misleading on THIS box** — changing Settings → Analytics → Order statuses DOES affect it. See Business rules.
- **Force-limit banner** — *"This report shows up to {total} results…"*; fires when Details is capped at 1000 rows.

### Export flow (no compare modal)

Export **bypasses the ExportModal** (compare is hard-locked to `no`) and goes straight to the **2FA modal** ([[account-cc2fa]]) — 6-digit email/TOTP code, auto-submitted if 2FA is off. A single CSV is then generated asynchronously, the merchant emailed a download link, and the file appears in [[settings-import-history]]. Export row limit: **150 000**.

### Client-side 60-second cache

The dashboard box caches its result (keyed by route + box + date range + compare) for 60 seconds.

## Settings & fields

The box has no settings of its own. Its only inputs are the page-wide **date range**, **Compare** (locked to `no` on Details / View More), and **Group** (not applicable). The one external setting that affects it is the order-status list under Settings → Analytics — see Business rules.

## Business rules

### Status filter IS merchant-configurable for this box

Unlike the by-sales product/category/brand boxes (and its own sister [[analytics-top-order-product-discounts]], which use a hardcoded ingest-time status filter), this box honours the merchant's **Settings → Analytics → Order statuses** choice. The default fallback (when the choice is empty/invalid) is **Paid, Completed, Pending+not_fulfilled, Authorized payment, Fulfilled**. So changing that setting DOES affect this box — the permanent yellow alert claiming statuses "cannot be changed" is incorrect here. This is a meaningful asymmetry: changing the setting affects Order discounts but not Product discounts.

### Discount name resolution

The display name is built conditionally: a discount with no name shows `Manual discount` (`order.Manual_discount`); with a code it shows `"{name} ({code})"` (e.g. "Summer sale (SUMMER20)"); without a code just `"{name}"` (global discounts). A renamed discount shows its **most recent** name even for older orders.

### Compare-disabled for Details and View More

Period-over-period comparison is explicitly disabled here, unlike most other table boxes. Reason inferred: discount usage reflects rules in place at the time, so prior-period comparison is ambiguous (the rule may not have existed earlier).

### Manual discounts bucket; Free shipping label; positive amounts

Manually-entered discounts (no rule attached) all aggregate under one "Manual discount" row with no drill-down. In View More, a free-shipping discount is labelled "Free shipping" (using the **last** recorded free-shipping state in the period); otherwise the discount type is shown directly. Because a discount reduces the order total, the underlying amount is negative; the box flips the sign so merchants always see positive money values.

### Deleted discounts persist in old periods only

Discounts deleted at the system level **are not captured** for orders placed after the deletion, but orders captured BEFORE it retain their rows (with the last-known name) and can still appear in older period queries — flagged with the PageHelp `deleted` state.

### "Sales" = order count

One row exists per `(order, discount)` pair (no per-line splits), so "Sales" is the number of **orders** that applied the discount; mobile/desktop are direct counts of those orders.

### Empty state, Top-N, and caps

Stores with no discount usage show a "No data" placeholder (new merchants without discount rules see it permanently empty unless hidden). The dashboard shows the **top 5**; Details shows 100/page capped at **1 000** distinct discounts, above which the banner directs the merchant to Export.

## Related

- [[analytics]] — parent hub.
- [[analytics-top-order-product-discounts]] — sister box for **product-level** discounts (similar structure).
- [[analytics-details]] / [[analytics-full]] — generic Details / View More sub-screens.
- [[discount]] / [[discount-code]] — entities.
- [[marketing-discounts]] — admin screen where these discounts are created/edited.
- [[discount-stacking]] — how multiple discount rules interact on a single order.
- [[settings-statuses]] — defines the order statuses included.

## Open questions

_None._
