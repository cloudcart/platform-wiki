---
type: feature
nav_path: "Reports → Customers"
route_name: admin.reports.customers
route_path: /admin/reports/customers
aliases: ["Customers report", "Customer analytics", "Customer registrations report", "Анализ на клиенти", "Отчет клиенти"]
tags: [reports, customers, analytics, chart, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-05-21
source_count: 0
---
# Customers report

## Purpose

The **customer analytics page** under Reports — visualises new customer registrations and customer-driven revenue over a selectable date range, grouped by 9 dimensions (day / week / month / year / hourOfDay / dayOfWeek / dayOfMonth / customerGroup / country) and filtered by tag, group, banned status, marketing consent, country, and region. The merchant tracks acquisition trends, spots peak registration days / hours for campaign timing, segments growth by country / group, and sees per-customer revenue (top spenders).

This sits in the **Reports** section (sibling to Sales / Products / Payments reports), NOT under Customers directly. It overlaps the [[customers]] list (which also shows per-customer revenue) but adds chart visualisation + groupable date dimensions.

## Where to find it

Sidebar → Reports → **Customers** (route `/admin/reports/customers`, route name `admin.reports.customers`).

The page is server-rendered (Reports is not yet migrated to Vue).

## What the merchant can do here

### Chart area

A configurable chart of new customer registrations over time:

- **Sales-by selector** — the 9 grouping dimensions (see Settings & fields).
- **Chart type buttons** — Area (default, active), Line, Column (bar).
- **Date range picker** — sets the range for both chart and table.
- **View in table** — opens a modal table version of the chart data.

### Filters (6)

| Filter | Notes |
|--------|-------|
| **Customer tagged with** | Autocomplete from defined customer tags. |
| **Customer group** | Autocomplete from defined [[customers-custom-groups]]. |
| **Banned** | Yes / No. |
| **Marketing** (accepts) | Yes / No. |
| **Country** | Country picker with flag. |
| **Region** | Autocomplete from city names. |

Filters apply to both the chart and the data table.

### Data table

Below the chart, a paginated table of customers matching the filters:

| Column | Notes |
|--------|-------|
| **Group** (`group_formatted`) | Customer's group badge. |
| **Name** | Full name. Clickable — opens the customer detail page in a new tab. Not sortable. |
| **Email** | Sortable. |
| **Orders total** (`orders_total`) | The customer's **lifetime completed-orders count** (a running aggregate on the customer record). Clickable — opens the customer's orders tab in a new tab. Not sortable. |
| **Date added** | When the customer registered. Sortable. |
| **Income** | The customer's **lifetime completed-orders income** (running aggregate on the customer record) — NOT scoped to the date range (see Business rules). |

### Totals block (`#report_totals`)

A summary block beneath the chart, scoped to the selected date range AND to `status = 'completed'` orders only:

- **Customer count** — registrations in the range (the chart total).
- **Order count** — completed orders placed in the range by those customers.
- **Order total** — sum of completed-order totals in the range.
- **Order average** — average completed-order total in the range.

### What the merchant CANNOT do here
- Bulk-edit customers from the table — read-only analytics; edit on [[customers-details]].
- Export the chart / table — no export button here; use the export on the [[customers]] list.
- Compare two date ranges side-by-side — single-range only.
- Save / bookmark a custom filter preset.

## Settings & fields

### Chart group options (9 dimensions)

| Group | Use case |
|-------|----------|
| **day** / **week** / **month** / **year** | Time-series trend at the chosen granularity. |
| **hourOfDay** | Peak registration hours. |
| **dayOfWeek** | Peak registration days (Monday vs Sunday). |
| **dayOfMonth** | End-of-month vs start-of-month patterns. |
| **customerGroup** | Bar per customer group (Regular / VIP / Wholesale). |
| **country** | Bar per country (Bulgaria / Romania / Germany / etc.). |

The first available group (`day`) is selected by default.

### Date range filter

A date-range picker controls the range (today / yesterday / last 7d / last 30d / this month / last month / custom).

## Business rules

### Read-only analytics view

This page does NOT modify customer data — it's purely a visualisation layer over the customers + orders data. To take action (edit, ban, change group, marketing), click through to [[customers-details]] or use [[customers]].

### Chart and table share one filter

The chart and table share the same filter conditions and date range — changing any filter updates both. The chart shows the time-bucketed count; the table shows the underlying records. The merchant can drill into a country / group / tag and see both together.

### Income is lifetime, not date-range

The table's **Income** column is the customer's **lifetime completed-orders income** (a running aggregate on the customer record) — it does NOT scope by the date range. The same figure appears on the [[customers]] list's Revenue column. Only the chart, the totals block, and which customers appear in the table (those registered in the range) are date-range-scoped.

The totals block (Order count / Order total / Order average), in contrast, IS date-ranged AND scoped to `status = 'completed'` orders only — Cancelled, Pending, etc. excluded.

### Group-dimension semantics

Time-based groups (day / week / month / year) plot a time-series; pattern groups (hourOfDay / dayOfWeek / dayOfMonth) plot recurring patterns for peak windows; `customerGroup` and `country` each plot a bar per group / country (mix analysis).

### Legacy reports area — live data, no cache, not CcAnalytics

`/admin/reports/customers` is the **legacy reports area** (not yet migrated to Vue), separate from the Vue-based Analytics Dashboard at `/admin/analytics`. Practical consequences:

- **Data source** — reads the live customers + orders data directly, so a new order reflects **instantly**. The Analytics Dashboard reads a pre-aggregated analytics store and lags ~1-2 min for new orders / up to 1 hour for visitor data (see [[analytics-pipeline]]).
- **No query cache** — every chart load and filter change runs a fresh aggregation query, so on stores with millions of orders rendering can take seconds (instant on small stores). The Vue dashboard is faster at scale.
- **Two-system gap** — a merchant showing 50 registrations here but 48 on the Analytics Dashboard's Total Customers box sees the gap: the dashboard count is filtered through the platform's "analytics statuses" setting (a customer with no orders or only Cancelled orders may not appear), while this page counts every registration regardless of order status. The two systems are independent and can differ slightly.
- **Rendering** — server-rendered legacy page with client-side filters, date pickers, and an AJAX-loaded table feeding the front-end chart library. No Vue components.

### Permission

Requires the reports permission section. Moderators without it cannot access Reports.

### Side effects

- **None** — pure read.

## Related

- [[customers]] — customer list with lifetime revenue (different scope from this report's date-range income).
- [[customers-custom-groups]] — group dimension for the chart.
- [[customers-details]] — drill-in target (name → detail page; orders count → orders tab).
- [[settings-cart]] — order-status-driven revenue attribution.
- [[customer]] — entity page.
- [[analytics-pipeline]] — concept page on the CcAnalytics pipeline. This Reports → Customers page does NOT use CcAnalytics; it queries the live database directly, so the two systems can show slightly different numbers.
- [[analytics]] — Vue-based Analytics Dashboard with the CcAnalytics-backed boxes.
- (Sibling reports: Sales, Products, Payments — same Reports section, different metrics.)

## Open questions

(none)
