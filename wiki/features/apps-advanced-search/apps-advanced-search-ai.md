---
type: feature
nav_path: "Apps → Aura Search → AI & relevance"
route_name: apps.advanced_search.ai
route_path: /admin/apps/advanced_search/ai
aliases: ["AI & relevance", "AI semantic search", "semantic search", "search by meaning", "relevance signals", "ranking signals", "boost in stock products", "search ranking", "test a search", "Match the intent", "working mode", "Typos corrected", "Empty results rescued", "семантично търсене", "търсене по смисъл", "подредба на резултатите", "тествай търсене"]
tags: [apps, search, ai, semantic, ranking, relevance]
plan_gates: ["advanced_search"]
created: 2026-09-23
updated: 2026-09-23
source_count: 6
---

# Aura Search — AI & relevance

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, searches, pins, vocabulary, settings, indexing).

## Purpose

The AI & relevance tab is where the merchant controls **how a search is understood** (by words, by meaning, or both) and **which products are ranked first** among those it finds. It also shows what the engine did beyond plain word matching, and lets the merchant run a test search.

## Where to find it

**Apps → Aura Search → AI & relevance** (`/admin/apps/advanced_search/ai`). Changes are saved with the bar at the top of the page, like the Settings tab.

## What the merchant can do here

- Switch **AI semantic search** on or off.
- Choose a **Working mode**.
- Move the sliders under **Where the words are matched** and **What pushes a product up**.
- **Try it** — type a query and see how the engine reads it and what it returns.
- Read the engine's counters and the **What the AI did** list for the period.

## Settings & fields

### Where the words are matched

| Slider | Setting | Range, default |
|---|---|---|
| **Match the intent** | `sort.weight.intent_match` | 0–100, **100** — how much meaning counts against wording |
| **Product title** | `weight.name` | 1–100, 10 |
| **Category** | `weight.category_name` | 1–100, 5 |
| **Brand** | `weight.vendor_name` | 1–100, 5 |
| **Product features** | `weight.properties` | 1–100, 5 |
| **Description** | `weight.description` | 1–100, 2 — long text matches easily, so a high weight buries exact title matches |

These weights only count for fields that are switched on as searchable ([[apps-advanced-search-settings]]).

### What pushes a product up

| Slider | Setting | Lifts |
|---|---|---|
| **Sales** | `sort.weight.bestselling` | products with more orders |
| **Popularity** | `sort.weight.views` | products with more views |
| **In stock** | `sort.weight.availability` | products that can be bought now |
| **New products** | `sort.weight.new` | products marked as new |
| **Recently added** | `sort.weight.recency` | products created lately |
| **Discount** | `sort.weight.save_percent` | a bigger percentage off |
| **Price** | `sort.weight.price` | more expensive products |
| **Promoted** | `sort.weight.manual` | products marked as featured |
| **Category relevance** | `sort.weight.category` | products whose category matches the search |

All run **0–100** and start at **0**. With every one at 0 the results stay in pure relevance order. *"Weights compete with each other — raising one lowers the rest in practice."* The Settings tab's **Sorting** pane holds the same kind of weights plus two more (**In-stock quantity**, **Discount amount**).

## Business rules

### 🔴 Three sliders and the working mode are not kept when saved

**Match the intent**, **In stock** and **Recently added** can be moved and the save bar accepts the change, but **the save does not keep them**. After saving or reloading they are back at their defaults (100, 0 and 0), and search uses those defaults. The same applies to the **Working mode** choice.

The other sliders on this tab are kept. To lift products that can actually be bought, **Settings → Sorting → In-stock quantity weight** is saved and ranks better-stocked products higher ([[apps-advanced-search-settings]]). The *Out-of-stock products rank first* card's **Adjust the signal** button leads to this tab ([[apps-advanced-search-overview]]).

### Working mode

Three options: **Automatic** (*Aura tunes the weights on its own. Not available yet.* — cannot be selected), **With recommendations** (*Aura suggests, you approve*) and **Manual** (*Full manual control*). Nothing changes weights on its own in any mode; the suggestions a merchant acts on are the Overview's opportunity cards.

### How AI semantic search works alongside words

With **AI semantic search** on, a search is matched two ways at once — by its **words** (with the field weights above) and by its **meaning**. The results are combined, so *running shoes* can also bring back *athletic sneakers*. Switched off, only the words are matched.

Meaning-based matching is **not used**:

- once the shopper narrows the `/search` page with **filters** (category, vendor, price, property…) — by-meaning matching would return the whole filtered set;
- for searches that look like a **code** — SKUs, barcodes, model numbers — which are matched against codes only;
- in the **dropdown after the monthly quota is used up** ([[apps-advanced-search-plans]]). The `/search` page keeps it.

It needs no separate purchase: any active plan includes it.

### How the ranking sliders apply

They reorder results on **search** only, in the dropdown and on the `/search` page — not on category or vendor pages. They are skipped:

- when a **pin list** fires for the search — pins lead, and the rest stay in plain relevance order ([[apps-advanced-search-pinned]]);
- when the shopper picks a sort order themselves (the optional sort dropdown, [[apps-advanced-search-settings]]).

### The engine's counters

| Counter | Counts |
|---|---|
| **AI semantic searches** | Dropdown searches that ran the meaning-based path, and their share of all searches. |
| **Queries mapped to a category** | Share of searches whose words name one of the store's categories. |
| **Typos corrected** | Searches whose words matched nothing as typed but found products thanks to typo tolerance ([[apps-advanced-search-vocabulary]]). |
| **Empty results rescued** | Searches that would have found nothing under **Require all search words to match** and were broadened instead. Only possible with that setting and its fallback on. |

A counter the platform has never recorded for the store shows a dash, not a zero. **What the AI did** lists only the kinds that actually happened in the period. The rail's **Last update** always reads *Not run yet*: the index does not report when it was last written to.

### The test search (Try it)

Type a query, for example *quiet air conditioner for a 20 m² room under 1500*, and the panel shows: a one-line reading of the result (how many products match, how many can be bought now), **Matching** (*Meaning and wording* or *Wording only*), **Fields searched**, a **Category** if the words name one, the word-matching mode, and up to six products with an *In stock* / *Out of stock* dot and a match percentage relative to the best result.

Two limits apply. The test shows results **without pinned products**, and its **Also searched** and **Corrected from** lines are never filled, even though synonyms do shape the results it lists. A test search is not billed and is not recorded as a shopper's search.

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-settings]] — searchable fields, "all words", the Sorting pane.
- [[apps-advanced-search-vocabulary]] — synonyms, stopwords, typo tolerance.
- [[apps-advanced-search-pinned]] — pins, which override the ranking sliders.
- [[apps-advanced-search-overview]] — the opportunity cards that send merchants here.
- [[apps-listing-engine-embeddings]] — the embedding service behind matching by meaning.

## Open questions

(None currently outstanding for this page.)
