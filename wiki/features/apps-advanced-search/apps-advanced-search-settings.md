---
type: feature
nav_path: "Apps → Advanced Search → Settings"
route_name: apps.advanced_search.settings
route_path: /admin/apps/advanced_search/settings
aliases: ["Advanced Search Settings", "Search engine settings", "AI Semantic Search toggle", "Search field weights", "Stopwords"]
tags: [apps, others, search, ai, settings]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (analytics, usage, orders, indexing, support).

# Advanced Search — Settings

## Purpose

The **Settings** tab is where the merchant configures how the storefront search behaves: which engine runs it, whether AI Semantic Search is on, which catalogue fields are searched, how heavily each field counts toward ranking, how many results of each type appear in the autocomplete dropdown, and which words the engine ignores (stopwords).

## Where to find it

Sidebar → Apps → **Advanced Search** → **Settings** tab (`apps.advanced_search.settings`). The Stopwords editor is a sibling tab (`apps.advanced_search.stopwords`).

## What the merchant can do here

- **Search bar engine** — pick the underlying search backend (`searchBarEngine`). See [[apps-advanced-search-indexing]] for how built-in vs [[apps-algolia]] is resolved.
- **AI Semantic Search** toggle — enable semantic / vector search.
- **Show properties on all listings** — toggle.
- **Show price** — display price in search results.
- **Limits per result type** — max products / categories / vendors shown in the result panel.
- **Filter (per field)** — name / description / category_name / vendor_name / variants / properties / brand_model / tags — which fields are searched.
- **Weight (per field)** — numeric relevance weight per field; higher weight ranks that field's matches higher.
- **Stopwords** — multi-tag input of common words to ignore; add via Enter / comma / space. Help text: *"Stopwords are common words (e.g. 'the', 'and', 'of') that are excluded from search queries to improve relevance and performance."*

### What the merchant CANNOT do here

- Define **synonyms** — there is no synonyms editor in [[apps-advanced-search]] or [[apps-listing-engine]]. Merchants cannot declare equivalences like "tshirt = t-shirt = tee"; matching relies on per-language stemming (the search index built-in stemmers for 30+ languages, plus a `latin_text` analyzer that transliterates Cyrillic to Latin for cross-script matching) and on the AI semantic vectors. Custom stopwords are stored in site settings (`search_stopwords`) and applied across the site's indexes.
- Run an **A/B test** of semantic vs lexical — there is one global `aiSemanticSearch` on/off toggle, no built-in split test. To compare, the merchant flips the toggle and observes metrics over time, or uses external A/B infrastructure.
- Customise the **search UI styling** — the autocomplete UI follows the storefront theme; visual changes go through Theme settings / custom CSS, not this app.

## Settings & fields

### Configuration shape (per Settings interface)

| Field | Notes |
|-------|-------|
| `searchBarEngine` | Underlying engine choice (`cloudcart` / `algolia`). See [[apps-advanced-search-indexing]]. |
| `aiSemanticSearch` | Boolean — toggle semantic search. |
| `showPropertiesOnAllListings` | Boolean. |
| `showPrice` | Boolean. |
| `limit.products` / `limit.categories` / `limit.vendors` | Result counts per type. |
| `filter.<field>` | Boolean per searchable field. |
| `weight.<field>` | Numeric weight per searchable field. |

### Default settings on install

- `showPrice = 1` (show price in results).
- `searchBarEngine = 'cloudcart'` (built-in [[apps-listing-engine]], NOT Algolia) — but if Algolia is already active at install time the value auto-flips to `algolia` (see [[apps-advanced-search-indexing]]).
- `aiSemanticSearch = 0` (off by default — paid plan feature).
- `showPropertiesOnAllListings = 0`.
- `limit.products = 9` (default 9 products in the autocomplete dropdown).
- `limit.categories = 5`, `limit.vendors = 5`.
- **Field filters: ONLY `name` is searched by default** (`filter.name = 1`). Description, category_name, vendor_name, variants, properties, brand_model, and tags are all OFF until the merchant ticks them on. This gives a tighter relevance baseline on install but means many merchants don't realise their description text isn't searched until they enable it.

Fields the merchant hasn't set fall back to these defaults.

### Save-time validation ranges

When the merchant saves Settings, the platform enforces:

- `limit.products`, `limit.categories`, `limit.vendors` — integers **0–20** (max 20 results per type in autocomplete).
- `weight.*` (name / description / category_name / vendor_name / variants / properties / brand_model) — integers **1–100**.

Values outside these ranges are rejected at save time.

## Business rules

### Plan-gated

The app is gated under the `advanced_search` plan feature. AI Semantic Search additionally requires the `advanced_search_ai_semantic_search` plan feature — it is enable-per-plan, NOT per-query metered. (Plan tier gating answers the "AI Semantic Search cost" question.)

### Semantic vs lexical

The AI Semantic Search toggle changes the matching algorithm:

- **OFF**: lexical (keyword-based) search with weights + stopwords + typo tolerance.
- **ON**: vector-based semantic search — finds conceptually similar results even when wording differs.

Semantic search has higher inference cost; access is plan-tier gated rather than per-query billed. Embedding tokens are logged under `embedding.tokens` for platform operators but the merchant is not charged per token. Re-indexing is the main token cost; on-storefront search only embeds the query string.

### No manual ranking override

There is no rule that forces product Y to the top when the customer searches X. Ranking is driven by per-field weights, category boosts, and (when on) the semantic similarity score. See [[apps-advanced-search-indexing]].

## Related

- [[apps-advanced-search]] — hub.
- [[apps-listing-engine]] — built-in engine the weights / filters drive.
- [[apps-algolia]] — alternative engine selectable via `searchBarEngine`.
- [[apps-cloudio-overview]] — AI brand behind semantic search.
- [[plan-gates]] — `advanced_search` / `advanced_search_ai_semantic_search` features.

## Open questions

(None currently outstanding for this page.)
