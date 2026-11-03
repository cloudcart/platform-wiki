---
type: feature
nav_path: "Analytics → Sales distribution"
route_name: analytics
route_path: /admin/analytics (box rendered on Dashboard)
aliases: ["Sales distribution", "Percentage of orders", "Order size distribution", "Order amount histogram", "Разпределение на продажбите"]
tags: [analytics, ccanalytics, orders, percentage-of-orders, distribution, histogram]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Sales distribution (Percentage of orders)

## Purpose

The **Sales distribution** box (internal key `percentage-of-orders`) answers: **"In this period, what's the spread of order sizes? Do I have a lot of small orders or a few big ones?"** It is a **bar histogram** that groups every counted order into one of ~10 amount buckets and shows the percentage of orders that fell into each bucket.

The buckets are NOT fixed — they auto-scale to the store's AOV for the selected period, so the histogram stays informative at any store scale (AOV 50 BGN → buckets *"10-20" … "Over 100"*; AOV 1,000 BGN → *"200-400" … "Over 2,000"*). It is the only `bar`-type box in the Orders category.

## Where to find it

Sidebar → **Analytics** → "Sales distribution" card on the Dashboard.

The card title reads **"Sales distribution"** (kept in English in the BG translation; tooltip and labels are localised). When the merchant zooms into a specific period, the title becomes **"Sales distribution {from} - {to}"** with the dates filled in.

## What the merchant can do here

- Read a **bar chart** with one column per amount bucket. The X-axis is the bucket label (e.g., *"50 BGN - 100 BGN"*); each bar's height is the share of orders in that bucket.
- Hover any bar for the **tooltip** with exact metrics: *"{percent} - {orders} from {count} order|{count} orders"* — e.g., *"23% - 145 from 632 orders"* (145 of 632 total orders fell in this bucket = 23%).
- Hover the box title for the **card tooltip**:
  - **EN:** *"Orders distribution aggregate in accumulated range, depend on selected order statuses in Settings."*
  - **BG:** *"Разпределение на поръчките попадащи в обхвата на тяхната акумулация. Данните се визуализират спрямо избраните статуси на поръчки в Настройки."*
- Set the Dashboard **date range** to choose which period's orders are histogrammed.
- Set the Dashboard **compare** selector (no / period / year) to overlay a second-period histogram.
- Open the Dashboard **Settings panel (cog)** to choose which order statuses count, and to reorder or hide the box.

This box does **not** have a "View details" drill-in, an industry comparison, or a per-device split — what shows on the dashboard is the full story.

## Settings & fields

### Order statuses (Dashboard Settings panel)

The **Order statuses** list directly controls which orders are histogrammed. Default counted statuses: `paid`, `completed`, `pending`, `authorized`, `fulfilled` — the same status filter as the other Orders boxes (see [[analytics-total-sales]] for the full spec, including the hidden expansion rules where `pending` counts only when `not_fulfilled` and `fulfilled` only when financial status is not one the merchant de-selected). **Industry** and **Show devices** have no effect on this box.

### One distribution per period (no time axis)

Unlike the chart-type boxes (Total Sales, Total Orders, AOV), this box does NOT chart over time — it shows ONE distribution for the WHOLE selected period. The date-range picker chooses which period's orders are included; there is no time-bucket axis (the box calls this the *accumulated range*).

### Adaptive bucket generation

Bucket boundaries are computed per request from the period's AOV:

1. Take the period's **AOV including shipping** (see the divergence note in Business rules).
2. If that AOV is **≤ 10** (major currency units), the box returns no data and renders the no-data card — a deliberate guard for tiny / brand-new stores.
3. Otherwise generate ~10 evenly-spaced closed buckets starting from 0, plus a final open-ended **"Over X"** bucket, sized so the whole histogram brackets the store's typical order.

Example: a store with AOV 1,000 BGN sees buckets 0-200, 200-400, 400-600, … 1800-2000, **Over 2000**. Labels render via the *"{min} - {max}"* template (BG: *"{min} - {max}"*) for ranged buckets and *"Over {value}"* (BG: *"Над {value}"*) for the open-ended top bucket, formatted with the store currency.

### No-data, timeout, and empty-bucket states

| State | When | What shows |
|-------|------|------------|
| **No data** | AOV ≤ 10, OR zero orders in range | "No data available for the selected range." |
| **Empty bucket** | A bucket catches no orders | Bar renders at zero height (0%). |
| **504 timeout** | Range too large to compute | "We cannot generate statistics for the selected period, please reduce it." |

## Business rules

### Bucketed amount includes shipping (divergence from Total Sales / AOV)

This is the one rule that trips merchants up. Both the bucket *sizing* and the bucket *predicates* use the **full order amount including shipping**, whereas the AOV box headline and Total Sales use the amount **without** shipping. Consequence:

- The bucket sizes are scaled to "AOV with shipping", so they will **not exactly line up** with the AOV box's headline number.
- Each order is placed by its **total size including shipping**, because Sales distribution is about *how big the order was*, not the product subtotal.

If a merchant asks why the distribution centre doesn't match the AOV headline, this divergence is the answer.

### Comparison reuses the current period's buckets

When compare is set to **period** or **year**, the bucket boundaries are computed ONCE from the **current** period's AOV and reused for the previous-period bars, so both histograms share identical X-axis labels. Trade-off: if the two periods have very different AOVs, the previous-period distribution looks skewed — orders pile into the "Over X" bucket or cluster in the lowest few. The compared range shows in the title **"Sales distribution {from} - {to}"** (`from` = lowest bucket min, `to` = highest *closed* bucket max; the "Over X" bucket is not reflected in the title range).

### Which orders count, and scope

Same counted-status filter as the other Orders boxes (default `paid` / `completed` / `pending` / `authorized` / `fulfilled`, configurable in the Dashboard Settings panel). The histogram is **not channel-filtered** — all matched orders across all channels are bucketed together. Dates are matched in UTC after store-timezone parsing. There is no industry comparison (so the hardcoded-status divergence noted on other boxes does not apply here).

### Currency scale and live data

Bucket boundaries display in the store currency. The box reads live data with no response cache, because the bucket set changes whenever AOV moves. Very-low-AOV stores can produce chunky buckets, but the AOV ≤ 10 guard catches the worst cases.

## Recommended merchant use

Open this box when:

- **Setting a free-shipping threshold** — set it just above the busiest bucket to lift order size without alienating bulk shoppers.
- **Designing bundles** — find the "thick" bucket and design bundles that target the next bucket up.
- **Diagnosing AOV moves** — if the distribution shifts only in the lowest buckets, the cause is more low-value orders, not fewer big-ticket ones.

Pair it with [[analytics-average-order-value]] (the *shape* around the mean) and [[analytics-total-orders]] (the count behind each bucket's percentage).

## Related

- [[analytics]] — parent hub.
- [[analytics-average-order-value]] — same "money on x-axis" framing, but a single mean vs. a histogram.
- [[analytics-total-orders]] — the total count being histogrammed.
- [[analytics-total-sales]] — the revenue total + full counted-status filter spec.
- [[analytics-top-order-products-by-sales]] — products driving big-bucket orders.
- [[settings-statuses]] — which statuses are counted.
- [[order]] — entity backing each bucketed order.
- [[plan-gates]] — `cc_analytics.allow_period_compare`.

## Open questions

_None._
