---
type: feature
nav_path: "Analytics → Returns boxes (Returns over time, Net revenue, Return rate)"
route_name: analytics
route_path: /admin/analytics
aliases: ["Returns over time", "Returns Over Time", "Net revenue", "Return rate", "returns analytics", "return statistics", "returns report inflated", "too many returns in analytics", "cancelled orders counted as returns", "връщания в анализите", "справка връщания", "нетни приходи", "процент връщания"]
tags: [analytics, dashboard, returns, reporting, din-7016]
plan_gates: []
created: 2026-08-08
updated: 2026-08-08
source_count: 4
---

> Part of [[analytics]]. See the hub for the other aspects (dashboard shell, date & compare, settings panel, box catalog, data freshness).

# Analytics — the three returns boxes

## Purpose

Three dashboard boxes report on returns, and **all three read the same underlying figure**. Understanding what that figure counts — and, just as importantly, what it deliberately does **not** count — explains most merchant questions about return statistics.

## Where to find it

On the [[analytics]] dashboard. All three ship **visible by default** and can be hidden or reordered like any other box ([[analytics-overview-box-catalog]]).

| Box | Type | What it plots |
|---|---|---|
| **Returns over time** | chart | The returned **value** (money out) per period, with the return **count** alongside. |
| **Net revenue** | chart | **Sales minus returns** per period. |
| **Return rate** | chart | **Returns value ÷ sales value**, as a percentage per period (2 decimals). |

Because they share one source figure, a question about any one of them is really a question about the rule below.

## What the merchant can do here

Read the three boxes, change the date range, compare periods, and hide or reorder them. There is no per-box configuration of what counts as a return — the counting rule is platform-wide.

## Settings & fields

None of their own. The **sales** side of Net revenue and Return rate follows the merchant's status filter in the Settings panel ([[analytics-overview-settings]]); the returns side does not have an equivalent filter.

## Business rules

### 🔴 Only PARTIAL returns are counted

Return reporting counts **partial returns only** — the case where the order stays active and just part of it comes back.

**Full returns and cancelled orders are not counted as returns.** A reversal of the whole order is already visible through the order's own status (*Отказана* / *Възстановена*) and through the order leaving the sales figures, so counting it a second time on the returns side would report the same reversal twice.

That double-count is exactly what used to happen: cancelling an already-confirmed (invoiced or paid) order records a system return ([[orders-returns-lifecycle]]), and while those were counted, the returns figure was inflated — even though no credit note was issued and no goods physically came back. The counting was corrected so that only genuine partial returns register.

**The return record still exists.** The correction changed what the **reports count**, not what the platform stores. Cancelling a committed order still writes a system return (no credit note, created by the platform rather than by a person), and it is still listed under the order's returns. It simply no longer appears in these three boxes.

### Past periods keep their old figures

Values already accumulated for **past periods are not recalculated**. Historical buckets keep whatever was recorded at the time, so a merchant looking at a long range can see a **step change**: earlier periods still carry the inflated numbers, later ones do not.

This is expected, and it is the single most likely explanation when a merchant says *"my returns dropped off a cliff"* or *"last year's return rate doesn't match this year's"* across the changeover. It is a change in counting, not lost data and not a collapse in returns.

### Only a received return counts, and it lands on the date it was received

A return registers in analytics **only once it reaches `returned`** — i.e. the goods were received ([[orders-returns-lifecycle]]). A return still `pending` does not appear; one that is later cancelled is **removed** from analytics again.

The period it lands in is the date it was **received**, not the date it was raised. A return opened in one month and received in the next belongs to the **next** month — so a merchant reconciling returns against the date the customer contacted them will see a shift.

### Offset exchanges count in the number, but contribute nothing to the value

An **exchange settled as an offset** — where the returned value is discounted on the replacement order instead of being refunded — is not money out. Its value contributes **zero** to Returns over time, Net revenue and Return rate, while the return still counts as **one return** in the count series.

A merchant can therefore see the return **count** rise with the returned **value** flat. That is correct: nothing was refunded. See [[orders-returns-refunds]] for the refund methods.

### Returns are not filtered by the merchant's status selection

The status filter in the Settings panel shapes the **sales** side ([[analytics-overview-settings]]). The returns side has no equivalent control — which is why the sales and returns halves of Net revenue and Return rate are not governed by the same setting.

## Related

- [[analytics]] — hub.
- [[analytics-overview-box-catalog]] — the full box catalogue and how boxes are shown, hidden and reordered.
- [[analytics-overview-settings]] — the status filter that shapes the sales side.
- [[analytics-overview-data-freshness]] — the hourly aggregation cycle; a return received in the last hour may not show yet.
- [[orders-returns-lifecycle]] — return types, statuses, and the system return created when a committed order is cancelled.
- [[orders-returns-refunds]] — refund methods, including the offset exchange.
- [[order-status-negative-semantics]] — why an order in a negative status leaves the sales figures.

## Open questions

None.
