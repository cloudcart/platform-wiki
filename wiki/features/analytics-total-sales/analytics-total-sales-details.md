---
type: feature
nav_path: "Analytics → Total Sales → Details drill-down"
route_name: analytics
route_path: /admin/analytics (Details view of the Total Sales box)
aliases: ["Total Sales details", "Total Sales drill-down", "Total Sales line items", "Total Sales export", "Детайли за Общи продажби"]
tags: [analytics, ccanalytics, orders, total-sales]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
> Part of [[analytics-total-sales]]. See the hub for the other aspects (which orders count, comparison math, industry-compare badge).

# Total Sales — Details drill-down

## Purpose

This page documents the **Details drill-down** of the Total Sales box: the per-line table that shows every product, shipping, fee, VAT, and discount line that contributed to the period's headline total. This is where a merchant goes from "I made X" to "here is exactly which lines made up X", and where the 1,000-row cap and the Export fallback live.

## Where to find it

On the Total Sales card, the **Details** action (`hasDetails: true`) opens the per-order breakdown. This pivots into the deep-dive views under [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]]. (The card's separate **"View more"** link does NOT come here — it goes to [[analytics-top-order-products-by-units-sold]].)

## What the merchant can do here

- Read the full per-line breakdown of the period: one row per product / shipping / fee / VAT / discount line.
- Page through results (100 rows per page).
- **Export** the full unpaginated collection when the period exceeds the on-screen cap.
- Unlike the Dashboard chart, the Details view supports an explicit `group=daily/weekly/monthly/...` parameter rather than the automatic grouping (see [[analytics-total-sales-comparison]]).

## Settings & fields

### Details table columns

The rows come from the per-line `analytics.orders_detailed` collection:

| Column | EN label | BG label | Notes |
|--------|----------|----------|-------|
| `date` | Date | Дата | Order date, formatted to store timezone |
| `product_name` | Name | Заглавие | Linked to the product page |
| `product_type` | Type | Тип | One of `product`, `shipping`, `fee`, `discount`, `vat` (translated) |
| `order` | Order | Поръчка | Linked to `/admin/orders/details/<id>?preview=1` |
| `price` | Price | Цена | Per-line price, money-formatted |
| `discount` | Discounts | Отстъпки | Line discount amount, money-formatted |
| `quantity` | Quantity | Количество | Number-formatted |
| `total_sale` | Total sale | Крайна цена | Line subtotal × qty, money-formatted |

Because the table breaks the order into typed lines, it is where the **shipping and tax components excluded from the headline** become visible — the headline sums `amount_without_shipping`, but Details separately surfaces `shipping_amount`, `shipping_discount_amount`, `tax_amount`, `vat_amount`, and the discount fields (see [[analytics-total-sales-order-filter]] for the headline field).

### Money units

All money columns are stored as minor-units × 100 and rendered via `moneyFormat`, identical to the headline scaling.

## Business rules

### Pagination cap & Export

Details lists are paginated at **100 rows per page** (`DETAILS_PAGINATION_LIMIT`) AND **hard-capped at 1,000 rows total** (`DETAILS_FORCE_LIMIT`). If a period would produce more than 1,000 line items, the table shows the first 1,000 and the merchant sees the platform-wide alert *"This report shows up to {total} results. To see all results, you can &lt;Export&gt;"*. The Export endpoint returns the full unpaginated collection.

### Query source

The Details and Details-export queries read the per-line documents from `analytics.orders_detailed` (connection `the analytics store-analytics`) using index `idx_list`, sorted by `order_id` then `index`. This is a different collection and index from the headline chart, which reads the pre-rolled `analytics.total_orders` — see [[analytics-total-sales-order-filter]] for the storage layout.

## Related

- [[analytics-total-sales]] — hub.
- [[analytics-total-sales-order-filter]] — which orders feed these lines, and the headline money field vs the per-line fields shown here.
- [[analytics-total-sales-comparison]] — the auto grouping the Dashboard uses; Details allows explicit grouping.
- [[analytics-details]] / [[analytics-more-details]] / [[analytics-full]] — the generic drill-down pages this opens into.
- [[order]] — entity backing every row; each row links to its order.

## Open questions

_None._
