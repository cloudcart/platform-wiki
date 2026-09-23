---
type: feature
nav_path: "Apps → Aura Search → Overview"
route_name: apps.advanced_search.dashboard
route_path: /admin/apps/advanced_search/dashboard
aliases: ["Aura Search overview", "Aura Search dashboard", "search quality score", "impact on sales", "higher conversion after a search", "opportunities for more sales", "revenue after a search", "customers who searched", "AI contribution", "what customers search for", "качество на търсенето", "влияние върху продажбите", "възможности за повече продажби"]
tags: [apps, search, analytics, dashboard, kpi]
plan_gates: ["advanced_search"]
created: 2026-09-23
updated: 2026-09-23
source_count: 5
---

# Aura Search — the Overview tab

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, searches, pins, vocabulary, AI, settings, indexing).

## Purpose

The Overview is the one-screen answer to *"is my search working, and what should I fix first?"*. It puts four headline figures, a sales comparison, a single quality score and a short list of suggested fixes over the period chosen in the header.

## Where to find it

**Apps → Aura Search → Overview** (`/admin/apps/advanced_search/dashboard`). Every block follows the header's date range (up to 3 months back) and its **Compare with** choice — the previous period of the same length, the same period last year, or no comparison.

## What the merchant can do here

- Read the four headline figures and how they moved against the comparison period.
- Read **Impact on sales** and the **Search quality** score.
- Act on an **opportunity card** — its button opens the synonym form, the pin form, the index rebuild or the tab that owns the fix.
- Jump through **Quick actions** — test a search, add a synonym, and the other shortcuts listed there.

## Settings & fields

### The four headline cards

| Card | What it counts |
|---|---|
| **Searches** | Dropdown searches by people in the period — the billed count **with bots taken out** ([[apps-advanced-search-usage]]). |
| **Customers who searched** | Despite the label, the number of **searches that led to at least one click** on a result. A shopper opening three results from one search counts once. |
| **Orders after a search** | Orders credited to a search ([[apps-advanced-search-orders]]). |
| **Revenue after a search** | The total value of those orders, in the store currency. |

Each card shows a small daily chart and the change against the comparison period. The change is left blank when the earlier period had nothing to grow from (*No previous period to compare with*). Cancelled, refunded and other negative-status orders, and archived orders, are left out of the order and revenue figures.

The click card shows a dash and *Click tracking is not collecting data yet* when no clicks were reported in the period. That is "not measured", not "nobody clicked". Clicks are only recorded while search analytics is on ([[apps-advanced-search-analytics]]).

### Impact on sales

A multiplier — *"3.1× higher conversion after a search"* — and four lines under it:

| Line | Calculation |
|---|---|
| **Conversion with search** | Orders after a search ÷ searches. |
| **Without search** | All other orders ÷ the store's other visits (sessions minus searches). |
| **Average order** | Revenue after a search ÷ orders after a search. |
| **Revenue per search** | Revenue after a search ÷ searches. |

Each figure is a dash until its side has **at least 30** searches (or visits). A multiplier computed from a handful is not shown.

The "with search" side divides by **searches, not shoppers**, so a shopper who searched three times counts three times. That makes the multiplier a **minimum**: the real difference is at least this large.

### Search quality (0–100)

One score built from four measured parts:

| Part | Weight | Read as |
|---|---|---|
| **Relevant results** | 35 | Share of clicks that landed on one of the **top three** results. |
| **Searches with no results** | 25 | 100 minus the no-results rate. |
| **Searches with a click** | 25 | Share of searches with a click. |
| **Average time to product** | 15 | Full marks under 5 s, zero at 60 s or more, straight line between. |

Verdict: **Excellent** from 90, **Good** from 75, **Fair** from 60, **Needs work** below. A part that cannot be measured — no clicks reported, analytics off — is **left out and the rest re-weighted**, so the score is built from what is known rather than dragged down by a gap. With nothing measurable the dial reads *Not enough searches in this period to score*.

## Business rules

### Opportunity cards — what triggers each

Recalculated for the period, at most every **15 minutes**. Only terms searched **at least 10 times** qualify, and only the most-searched eight of each kind are examined closely.

| Card | Shown when | Button |
|---|---|---|
| *Your catalogue is not in the search index* / *The search index is missing about N products* | The index holds under **70 %** of the store's products. Always listed **first**. | **Update the index** |
| *"{term}" finds nothing, but you sell it* | A term with no results whose words appear in a product name. | **Add a synonym** |
| *"{term}" finds nothing at all* | A term with no results and no product named with its words. | **See all of them** (the No results view) |
| *Out-of-stock products rank first for "{term}"* | Half or more of a popular term's first three results cannot be bought. | **Adjust the signal** (AI & relevance) |
| *"{term}" is searched often and never ordered* | A term with results and no order after it. One such card at most. | **Pin a product** |

The name match behind the two no-results cards is literal. A term in another alphabet from the catalogue (*айфон* against *iPhone*) cannot be matched, so it lands on *finds nothing at all* even when the product exists. The card's text leaves that open: a synonym is also the fix there ([[apps-advanced-search-vocabulary]]).

### AI contribution this period

Three bars: **Searches understood by meaning**, **Searches saved from an empty page** and **Spelling mistakes corrected**. On this tab the spelling line always shows a dash; the counted figure is on the AI & relevance tab ([[apps-advanced-search-ai]]).

### What customers search for

The top categories by share of searches. A term is credited to a category when the shopper typed the category's name or something the name contains. It is a **name match, labelled as a guess**, not a record of what shoppers opened.

### The status line reports the switch, not the index

The rail's *"The search is running and your catalog is synchronized"* is shown whenever the app is **on**. It does not check the index. Whether the index actually holds the catalogue is on **Settings → System status** ([[apps-advanced-search-indexing]]).

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-analytics]] — the per-term detail behind these figures.
- [[apps-advanced-search-orders]] — how orders are credited to a search.
- [[apps-advanced-search-usage]] — why "Searches" here is smaller than the billed figure.
- [[apps-advanced-search-pinned]] — what the **Pin a product** button creates.
- [[apps-advanced-search-vocabulary]] — what the **Add a synonym** button creates.

## Open questions

(None currently outstanding for this page.)
