---
type: feature
nav_path: "Apps → Aura Search"
route_name: apps.advanced_search.dashboard
route_path: /admin/apps/advanced_search/dashboard
aliases: ["Aura Search", "Advanced Search", "AI search", "AI Semantic Search", "Storefront search app", "Search engine app", "search autocomplete", "enable disable button", "app active toggle", "missing enable button", "Аура търсене", "Разширено търсене", "Търсачка на магазина", "AI търсене"]
tags: [apps, others, search, ai, analytics, merchandising]
plan_gates: ["advanced_search", "advanced_search_packs"]
created: 2026-05-22
updated: 2026-09-23
source_count: 14
---

# Aura Search

> **The on/off control appears only once a search plan is active.** Installing and opening the app are free, and so is looking around its screens. **Enabling** it requires a paid monthly plan (Starter, Growth or Pro). Without one the screen shows no Enable / Disable control and the storefront keeps the basic store search. The plan is bought from **Settings → Plan & usage → Activate — choose a plan**, and the control appears as soon as it is active. See [[apps-advanced-search-plans]].

## Purpose

**Aura Search** replaces the store's basic search with CloudCart's own search engine, and adds the tools to see and steer what it does:

- **An instant results dropdown** under the search box — products, categories and vendors as the shopper types.
- **Matching by meaning** (AI semantic search) on top of matching by words, plus typo tolerance and per-language word handling.
- **Merchandising** — pin chosen products to the top of a search, a category or a vendor page; teach the engine synonyms.
- **Ranking signals** — lift best-sellers, in-stock, discounted or featured products in the results.
- **Search analytics** — what shoppers type, what finds nothing, what gets clicked, and which searches end in an order.

**Aura Search** is the app's commercial name; **Advanced Search** is its internal working name. The working name shows through in the admin address (`/admin/apps/advanced_search`), the setting keys, the over-quota alert and the plan panel, so a merchant may meet either. Both mean this app. Towards merchants it is Aura Search.

## Where to find it

Sidebar → **Apps → Aura Search** (`/admin/apps/advanced_search`). The screen has five tabs, in the order a merchant works through them:

| Tab | What it answers | Aspect |
|---|---|---|
| **Overview** | How is search doing, and what is worth fixing? | [[apps-advanced-search-overview]] |
| **Searches** | What did shoppers type, and how did each term perform? | [[apps-advanced-search-analytics]] |
| **Optimization** | Pinned products, stopwords, synonyms, index status | [[apps-advanced-search-pinned]], [[apps-advanced-search-vocabulary]], [[apps-advanced-search-indexing]] |
| **AI & relevance** | How the engine reads a query, and what pushes a product up | [[apps-advanced-search-ai]] |
| **Settings** | The engine, matching, the dropdown, sorting, the plan | [[apps-advanced-search-settings]] |

The header carries a date range (up to 3 months back), a **Compare with** selector, a **New optimization** button (opens Optimization) and a **View the search** link to the live storefront `/search` page.

## Sub-pages (in this cluster)

- [[apps-advanced-search-plans]] — the paid plans, the monthly search quota, what counts as one search, and what happens when it runs out.
- [[apps-advanced-search-overview]] — the Overview tab: the four headline figures, impact on sales, the quality score and the opportunity cards.
- [[apps-advanced-search-analytics]] — the Searches tab: turning analytics on, the term table and its four views, verdict badges, the drill-down and the export.
- [[apps-advanced-search-orders]] — how an order is credited to a search, and the list of those orders.
- [[apps-advanced-search-usage]] — why the app shows three different counts of "searches", and the older usage pages.
- [[apps-advanced-search-pinned]] — pinning products to a search term, a category or a vendor.
- [[apps-advanced-search-vocabulary]] — synonyms, stopwords and typo tolerance: how the words of a query are read.
- [[apps-advanced-search-ai]] — the AI & relevance tab: semantic search, the signal sliders, the engine's counters and the test search.
- [[apps-advanced-search-settings]] — the Settings tab, pane by pane, with defaults and save limits.
- [[apps-advanced-search-indexing]] — the engine choice, the search index, rebuilding it, and how fast changes appear.

## What the merchant can do here

- **Buy and change the search plan**, and add extra searches ([[apps-advanced-search-plans]]).
- **Read how search performs** and act on the suggested fixes ([[apps-advanced-search-overview]], [[apps-advanced-search-analytics]]).
- **Put chosen products first** for a search term, a category or a vendor ([[apps-advanced-search-pinned]]).
- **Add synonyms** so a shopper's word reaches the catalogue's word ([[apps-advanced-search-vocabulary]]).
- **Tune matching and ranking** — searched fields, their weights, business signals, "all words must match" ([[apps-advanced-search-ai]], [[apps-advanced-search-settings]]).
- **Shape the dropdown** — how many products, categories and vendors, prices, highlighting ([[apps-advanced-search-settings]]).
- **Rebuild the search index** ([[apps-advanced-search-indexing]]).

### What the merchant CANNOT do here

- **Use it on the storefront without a paid plan** — see the note at the top.
- **Buy unlimited searches** — every plan is a monthly number; extra packs add to it ([[apps-advanced-search-plans]]).
- **Grade search results by hand** — relevance is judged from where shoppers click ([[apps-advanced-search-overview]]).
- **Let the engine tune itself** — the **Automatic** working mode is shown but marked *not available yet* ([[apps-advanced-search-ai]]).

## Settings & fields

The settings are spread over the tabs, each with its own aspect: engine, matching and the dropdown on [[apps-advanced-search-settings]]; ranking sliders on [[apps-advanced-search-ai]]; synonyms and stopwords on [[apps-advanced-search-vocabulary]]; pin lists on [[apps-advanced-search-pinned]]; the plan on [[apps-advanced-search-plans]].

## Business rules

### The storefront search box is what the plan pays for

The monthly quota is spent by the **instant results dropdown** under the search box, not by the full results page. When the quota runs out, the dropdown drops to basic keyword search and the app stays enabled. Pinned products, synonyms and the full `/search` page keep working. The rules for what counts, and what changes over quota, are on [[apps-advanced-search-plans]].

### Most figures need analytics switched on

**Search analytics is off on a new install.** Until it is turned on (**Searches** tab → **Turn on**), the term table, the no-results rate, the category breakdown and most opportunity cards stay empty. The headline search count and the orders after a search are recorded regardless. See [[apps-advanced-search-analytics]].

### Changes to synonyms and pins apply on the next search

Synonyms, pinned products, weights and signals are applied when each search runs. None of them needs the index rebuilt. The index only has to be rebuilt when the catalogue in it is incomplete ([[apps-advanced-search-indexing]]).

### Algolia is an alternative engine, not an add-on

With [[apps-algolia]] installed and active, **Settings → Search engine** can hand the search box to Algolia. Aura Search's own dropdown settings then stop applying ([[apps-advanced-search-indexing]]).

## Related

- [[apps]] — the App Store.
- [[apps-listing-engine]] — the index the engine searches.
- [[apps-algolia]] — the alternative search engine.
- [[search]] — the storefront `/search` results page.
- [[products-categories]], [[products-vendors]] — the listings pins can be attached to.
- [[orders]] — where orders after a search land.
- [[plan-gates]] — how paid plan features work.

## Open questions

- Whether themes built on the new storefront engine use the Aura Search dropdown, or their own predictive search — which would not spend the quota and would not credit orders to a search.
