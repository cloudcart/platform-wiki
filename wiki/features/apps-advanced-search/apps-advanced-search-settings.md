---
type: feature
nav_path: "Apps → Aura Search → Settings"
route_name: apps.advanced_search.settings
route_path: /admin/apps/advanced_search/settings
aliases: ["Aura Search settings", "Advanced Search settings", "search engine settings", "searchable fields", "search description", "require all search words to match", "instant search results settings", "autocomplete settings", "highlight matched terms", "search result sorting", "sort dropdown on search page", "property filters on all listings", "recommended settings", "настройки на търсачката", "търсене в описанието", "всички думи да съвпадат"]
tags: [apps, search, settings, autocomplete, ranking]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-09-23
source_count: 5
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, searches, pins, vocabulary, AI, indexing).

# Aura Search — the Settings tab

## Purpose

The Settings tab configures how search behaves, what it returns, and how products are shown in the dropdown. It is split into panes chosen from a sub-menu on the left, with a status rail on the right.

## Where to find it

**Apps → Aura Search → Settings** (`/admin/apps/advanced_search/settings`). Each pane has its own address (`?section=matching`, `results`, `autocomplete`, `sorting`, `plan`), so a link can point at one pane.

## What the merchant can do here

Change any field below and save with the bar at the top of the page. The panes are **Basic**, **Matching & AI**, **Results & filters**, **Autocomplete**, **Sorting** and **Plan & usage**.

## Settings & fields

### Basic

A short summary of the most-used controls, plus a live **Preview**:

- **Search engine** (`searchBarEngine`) — **CloudCart**, or Algolia when that app is installed and active; with a *Connected* / *Not active* badge.
- **Word matching** — the two "all words" switches below.
- **AI semantic search** (`aiSemanticSearch`).
- **Product features** — the property-filters switch below.
- **Search results** — a read-only summary with **Edit**, which opens Results & filters.
- **Preview** — type a query to see what shoppers get, using the **saved** settings. Unsaved changes show once saved.

### Matching & AI

| Field | Default | Notes |
|---|---|---|
| **Require all search words to match** (`search.match_all_words`) | off | Only products containing **every** word of a multi-word search. *"red office chair"* then stops returning red things and chairs in general. Codes, SKUs and barcodes are unaffected. |
| **Fall back to broad search when nothing matches all words** (`search.match_all_words_fallback`) | off | Shown only when the above is on. If no product has every word, the search broadens to any word instead of showing nothing. |
| **AI Semantic Search** (`aiSemanticSearch`) | off | Matching by meaning as well as words ([[apps-advanced-search-ai]]). |
| **Search Relevance & Weights** — a switch per field (`filter.*`) and a weight (`weight.*`) | only **name** on | Fields: product name (always on), description, category name, vendor name, variants, properties, tags, and brand & model when [[brand-model]] is installed. |

**Weights are saved in the range 1–100** (defaults: name 10, description 2, the rest 5), although the pane's help text describes them as 0 to 10. With AI semantic search on, the field switches still govern the word-matching part. Matching by meaning looks at the product as a whole and cannot be limited to fields.

### Results & filters

| Field | Default | Limit |
|---|---|---|
| **Show products prices** (`showPrice`) | on | |
| **Show strikethrough (old) price** (`showOldPrice`) | on | shown when prices are on |
| **The number of the products to be displayed** (`limit.products`) | 9 | 0–20 |
| **… categories …** (`limit.categories`) | 5 | 0–20 |
| **… vendors …** (`limit.vendors`) | 5 | 0–20 |
| **Show categories from product results** (`search.categories_from_products`) | off | categories of the matched products, instead of a separate category search |
| **Show vendors from product results** (`search.vendors_from_products`) | off | the same for vendors |
| **Show property filters on all listing pages** (`showPropertiesOnAllListings`) | off | property filters on search, vendor, tag and collection pages, not only on categories |

A limit of **0** hides that block from the dropdown. The instant-results settings apply only while **CloudCart** is the search engine.

### Autocomplete

- **Highlight matched terms in suggestions** (`search.highlight`, on) — marks the typed words in each suggestion.
- **Show product … in suggestions** (`search.display.*`, all on) — description, category, vendor, variants, properties, brand & model. A switch appears only for a field that is searched, or for every field when AI semantic search is on. These control **display only**; matching is set under Matching & AI. Name and image are always shown; price follows **Show products prices**.

### Sorting

- **Show sort dropdown on the search results page** (`search.sort_ui.enabled`, off) — lets shoppers re-order `/search` themselves. A shopper's choice replaces the weights below for that page.
- Weights **0–100**, all **0** by default: **Best-selling**, **Most-viewed**, **In-stock quantity**, **Discount amount**, **Discount %**, **Sale price** (more expensive first), **Featured**, **New products**, **Category relevance**. All at 0 = pure relevance order. How they apply, and when they are skipped, is on [[apps-advanced-search-ai]].

### Plan & usage

The plan, packs and monthly count — see [[apps-advanced-search-plans]].

## Business rules

### A new install searches the product name only

Out of the box only `filter.name` is on. Description, category, vendor, variants, properties and tags are **not searched** until switched on. That is the usual answer to *"a word from my product description finds nothing"*.

### The rail: System status, Recommended settings, Plan & usage

- **System status** — *Products in the index*, *Categories*, *Vendors*, refreshed every 30 seconds, and the rebuild button ([[apps-advanced-search-indexing]]). The headline reads *The app is turned off* when it is off, *The index is empty* when nothing is indexed, and otherwise *Everything is running normally*.
- **Recommended settings** — a gauge of how many of seven recommended switches are on: AI semantic search, searching categories, features and variants, highlighting, prices in suggestions, and feature filters on all pages. **Review** opens the pane of the first one that is off. Nothing is enforced.
- **Plan & usage** — plan name, searches per month, Used, Left, and a bar.

### Settings not on this tab

Typo tolerance is automatic and not adjustable ([[apps-advanced-search-vocabulary]]). Click tracking is on whenever analytics is on ([[apps-advanced-search-analytics]]).

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-ai]] — semantic search and the ranking sliders in detail.
- [[apps-advanced-search-vocabulary]] — synonyms, stopwords, typo tolerance.
- [[apps-advanced-search-indexing]] — the engine choice and the rebuild button.
- [[apps-advanced-search-plans]] — the Plan & usage pane.
- [[apps-algolia]] — the alternative engine.
- [[brand-model]] — the brand & model field.

## Open questions

(None currently outstanding for this page.)
