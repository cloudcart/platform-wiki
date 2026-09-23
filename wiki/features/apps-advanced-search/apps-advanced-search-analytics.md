---
type: feature
nav_path: "Apps → Aura Search → Searches"
route_name: apps.advanced_search.analysis
route_path: /admin/apps/advanced_search/analysis
aliases: ["Aura Search searches", "search analysis", "search analytics", "search terms report", "popular searches", "no results searches", "zero results", "no clicks", "low conversion searches", "export search terms", "turn on search analytics", "анализ на търсенията", "търсения без резултат", "популярни търсения", "какво търсят клиентите"]
tags: [apps, search, analytics, reports]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-09-23
source_count: 5
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, pins, vocabulary, AI, settings, indexing).

# Aura Search — the Searches tab (search analytics)

## Purpose

The Searches tab lists **what shoppers typed** and how each term performed: how often it was searched, whether it found anything, whether anyone clicked, and whether it led to an order. It is where a merchant finds the terms worth fixing — the ones that find nothing, the ones nobody clicks, the ones that never sell.

## Where to find it

**Apps → Aura Search → Searches** (`/admin/apps/advanced_search/analysis`). Its views have their own addresses: `/analysis/nohits`, `/analysis/noclick`, `/analysis/lowconversion`. The table follows the header's date range.

## What the merchant can do here

- **Turn on** search analytics, if it is off.
- Switch between four views: **Popular**, **No results**, **No clicks**, **Low conversion**.
- Filter the table: **Search a query**, **All results / With results / Without results**, **All devices / Desktop / Mobile / Tablet**.
- Open a term to see its figures, the products it returns today, and what to do about it.
- **Export** the table as a CSV file.
- **Copy link to this view** — the filters live in the address, so the link reopens the same view.

## Settings & fields

### Table columns

| Column | Meaning |
|---|---|
| **Query** | The term, lower-cased, cut to 10 words / 100 characters. |
| **Searches** | How many times it was searched in the period. |
| **CTR** | Share of those searches where a result was clicked. |
| **Orders** / **Revenue** | Orders credited to this exact term ([[apps-advanced-search-orders]]). |
| **Conversion** | Orders ÷ searches for this term. |
| **Trend** | Searches per day across the period. |
| **Opportunity** | A verdict badge — see below. |

### The four views

| View | Terms listed |
|---|---|
| **Popular** | All terms, most-searched first. |
| **No results** | Terms that found nothing. |
| **No clicks** | Terms searched **10+ times** that found products but got **no click**. Empty until clicks are reported. |
| **Low conversion** | Terms searched **10+ times** that found products and converted **below 0.5 %**. |

### Verdict badges

| Badge | When |
|---|---|
| **Improve results** | The term found nothing. |
| **Performing well** | It has orders and converts at **2 % or more**. |
| **Optimize** | Searched 10+ times, found products, **no order**. |
| **Review** | Searched 10+ times with orders, converting under 2 %. |
| **Out of stock** | Its first results are mostly unbuyable. |
| **Add a synonym** | It finds nothing, but a product name contains its words. |

A term searched fewer than 10 times gets no badge. **Out of stock** and **Add a synonym** come from the same check that builds the Overview's opportunity cards ([[apps-advanced-search-overview]]). Only the most-searched terms get that check, so a quieter term keeps its count-based badge.

## Business rules

### 🔴 Analytics is off until switched on — and switching it off deletes the history

On a new install search analytics is **off**, and this tab shows only a **Turn on** card. Until it is on, no terms are recorded. The **Searches** figure on the Overview and the orders after a search are recorded either way.

Turning it on also starts **click tracking**: the storefront reports each result opened, which is what fills CTR, **No clicks** and the click-based parts of the quality score.

The switch to turn analytics **off** is on the older Analytics page (`/admin/apps/advanced_search/analytics`), which is still reachable by its address. **Switching it off there deletes every term recorded for the store**, not only future ones. Turning it back on starts again from empty.

### What is recorded, and why partial words appear

Terms are recorded from **both** the dropdown under the search box and the full `/search` results page. The dropdown searches at every pause in typing, so a shopper typing *маратонки* slowly can leave *мар* and *марато* in the table next to the full word. That is the record of what was sent, not a fault.

A term counts as **finding something** on a day if any of its searches that day returned products.

### Clicks come from the storefront, and only for real results

A click is recorded when a shopper opens a product from the dropdown or from the product list of the `/search` page. Clicks elsewhere on that page, such as a *recently viewed* strip, are not counted. Bots' clicks are stored but left out of every figure. A click more than **10 minutes** after its search still counts as a click, but is left out of the time-to-product average.

### The table covers the 5 000 most-searched terms

On a store with a very large vocabulary only the **5 000 most-searched** terms of the period are analysed, and the tab says so: *Only the 5000 most-searched queries are analysed for this period.* What is dropped is the single-search tail.

The **Export** follows the same filters, writes up to **5 000 rows**, and adds a closing line when rows or terms were left out. The file is UTF-8 with the marker Excel needs to show Cyrillic correctly. Columns: *Query, Searches, CTR %, Orders, Conversion %, Revenue, Opportunity*.

### The drill-down runs the search live

Opening a term shows its **Searches**, **CTR**, **Orders**, **Revenue** and **Conversion**, then **Top results**: the products the search returns **right now**, each with an *In stock* / *Out of stock* dot and a match percentage relative to the best result. Its recommendations are *Add a synonym* (no results), *Order available first* (out-of-stock results), *Pin a product* (searched often, never ordered) and *Review results* (low conversion). **See the orders behind this term** opens the orders list filtered to it.

Because the results are live, they may differ from what shoppers saw earlier in the period.

### Data is kept for 90 days

Recorded terms, clicks and the engine's counters are kept for **90 days**, and the date range goes back 3 months at most.

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-overview]] — the summary built from the same data.
- [[apps-advanced-search-orders]] — how orders are credited to a term.
- [[apps-advanced-search-vocabulary]] — synonyms, the usual fix for **No results**.
- [[apps-advanced-search-pinned]] — pins, the usual fix for **Optimize**.
- [[apps-advanced-search-usage]] — why the counts here differ from the billed count.
- [[products-missing-product]] — a separate signal of demand for products not in stock.

## Open questions

(None currently outstanding for this page.)
