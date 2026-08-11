---
type: feature
nav_path: "Analytics → Total Sales → Industry comparison"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Total Sales industry comparison", "Industry average badge", "main_industry benchmark", "Сравнение с бранша"]
tags: [analytics, ccanalytics, orders, total-sales]
plan_gates: ["cc_analytics.allow_industry_compare"]
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
> Part of [[analytics-total-sales]]. See the hub for the other aspects (which orders count, comparison math, Details drill-down).

# Total Sales — industry comparison

## Purpose

This page documents the **industry-compare badge** on the Total Sales box: the optional text that tells the merchant whether their revenue is above or below the average for their industry. It explains where the benchmark data comes from, why its granularity is weekly, and the important reason the badge can disagree with the headline number it sits next to.

## Where to find it

When `hasIndustryCompare: true` on the box config AND the merchant's plan grants `cc_analytics.allow_industry_compare`, the badge appears under the headline on the Total Sales card on the Analytics Dashboard. The merchant sets their industry under **Analytics Settings** (the `Site.main_industry` field).

## What the merchant can do here

- Set their store's industry in Analytics Settings so the benchmark has a peer group.
- Read the badge text, e.g. *"For period &lt;period&gt; Total Sales: &lt;value&gt; where is &lt;percent&gt; above the average for &lt;industry&gt;"*.

## Settings & fields

- **Plan gate** — the badge only renders when the plan grants `cc_analytics.allow_industry_compare`. Without it, the Total Sales box shows just the headline + chart.
- **Industry** — `Site.main_industry`, set by the merchant in Analytics Settings. Stores with no industry are silently skipped by the benchmark job and get no badge.
- **Data source** — the industry average is read from `analytics.sites_industry_statistic`, refreshed weekly by the site-industry-statistic job.

## Business rules

### Hardcoded status filter (why the badge can disagree with the headline)

The weekly site-industry pipeline (`SiteIndustryTotalSales.json`) **ignores the merchant's analytics-statuses configuration** and ALWAYS uses `status IN [paid, completed, authorized] OR (pending AND not_fulfilled) OR fulfilled`. So a merchant who added `delivered` to their analytics statuses (see [[analytics-total-sales-order-filter]]) will see the headline include `delivered` orders, while the industry-compare badge benchmarks against a count that excludes them. The two numbers are computed on different status sets by design.

### Weekly, UTC granularity

The job runs per **ISO week, starting Monday in UTC** — NOT in store timezone — and aggregates the whole week's totals. So the comparison granularity is weekly even when the merchant is viewing a single day.

### How the percentage is computed

- The job groups sites by `Site.main_industry`. The merchant's own data is split out as `self`; the baseline is `avg = sum(other) / (industry_site_count − 1)`.
- If the merchant is the only store in the industry, `avg = 0` and the badge reports `0%`.
- The percentage is `round((self / avg) * 100, 2)` with direction `above` if `self > avg`, otherwise `below`.
- When `avg = 0` and `self > 0` the badge shows `100% above`; when both are 0 it shows `0%`.
- Money values are divided by 100 inside this pipeline, so the stored snapshot is in **major** currency units — NOT the minor-units × 100 scaling used by the raw collection (see [[analytics-total-sales-order-filter]]).

## Related

- [[analytics-total-sales]] — hub.
- [[analytics-total-sales-order-filter]] — the configurable status list the headline uses, which this badge deliberately ignores.
- [[analytics-total-sales-comparison]] — the period/year deltas, a different comparison surface on the same box.
- [[plan-gates]] — `cc_analytics.allow_industry_compare`.

## Open questions

_None._
