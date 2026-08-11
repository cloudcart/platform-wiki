---
type: feature
nav_path: "Apps → Advanced Search"
route_name: apps.advanced_search.overview
route_path: /admin/apps/advanced_search
aliases: ["Advanced Search", "Search engine", "AI Semantic Search", "Storefront search", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, others, search, ai, analytics]
plan_gates: ["advanced_search"]
created: 2026-05-22
updated: 2026-08-06
source_count: 6
---
# Advanced Search

## Purpose

**Advanced Search** replaces CloudCart's default storefront search with a more powerful search engine. It is the largest "Others" app — plan-gated under the `advanced_search` feature — and brings:

- **Better matching** — typo tolerance, configurable per-field weights, per-language stemming.
- **AI Semantic Search** — an opt-in toggle for vector / meaning-based search (a search for "running shoes" can find "athletic sneakers").
- **Multi-source results** — products + categories + vendors + properties + brand-model + tags in one result panel.
- **Search analytics** — popular queries and, critically, queries that returned ZERO results (product / SEO gaps).
- **Usage statistics** — storefront vs backend search counts over time, plus aggregated charts.
- **Search-driven orders** — orders that originated from a search query, for conversion insight.

This page is the **hub** for the Advanced Search cluster. It has grown past one concept, so the detail lives in the aspect pages below — drill into the one that matches the question rather than reading them all.

> **On/off control appears only when the store has an active plan (tier) for the app.** Without a tier the app screen shows no **Enable / Disable** button and no enabled / disabled indicator — a missing button is not a fault, the storefront simply keeps using basic search. Buy a tier from the plan panel on the **Settings** tab (**Activate — choose a plan**); the button appears as soon as the tier is active.

## Where to find it

Sidebar → Apps → install → **Advanced Search**. The app exposes ten admin sub-routes:

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.advanced_search.overview` |
| Settings | `apps.advanced_search.settings` |
| Analytics | `apps.advanced_search.analytics` |
| Analytics → No-hits | `apps.advanced_search.analytics.nohits` |
| Usage | `apps.advanced_search.usage` |
| Usage → Bot | `apps.advanced_search.usage.bot` |
| Usage → Backend | `apps.advanced_search.usage.backend` |
| Statistics | `apps.advanced_search.statistic` |
| Stopwords | `apps.advanced_search.stopwords` |
| Orders | `apps.advanced_search.orders` |

## What the merchant can do here

- **Configure the engine and result fields** — pick the backend, toggle AI Semantic Search, choose which fields are searched, set per-field weights, set per-type result limits, manage stopwords. See [[apps-advanced-search-settings]].
- **Read search demand** — popular queries and no-hits (zero-result searches). See [[apps-advanced-search-analytics]].
- **Monitor search volume** — storefront vs backend/patches usage over a date range, plus aggregated charts. See [[apps-advanced-search-usage]].
- **See which searches convert** — orders attributed to a search query. See [[apps-advanced-search-orders]].
- **Trigger a full re-index** — rebuild the index (puts the storefront into maintenance mode while it runs). See [[apps-advanced-search-indexing]].

### What the merchant CANNOT do here

- Use it without the paid plan feature (plan-gated under `advanced_search`).
- Pin a specific product to the top of a specific query's results — no manual ranking override (see [[apps-advanced-search-indexing]]).
- Define synonyms — no synonyms editor; matching relies on per-language stemming + AI vectors (see [[apps-advanced-search-settings]]).
- Run a built-in A/B test of semantic vs lexical search — there is one global toggle only (see [[apps-advanced-search-settings]]).

## Settings & fields

The full field catalogue (engine, AI toggle, filters, weights, limits, stopwords, install defaults, and save-time validation ranges) lives on [[apps-advanced-search-settings]]. The Usage date range is capped at 3 months back (see [[apps-advanced-search-usage]]); analytics limits run 10–500 (see [[apps-advanced-search-analytics]]).

## Business rules

- **Plan-gated.** The app sits behind the `advanced_search` plan feature; AI Semantic Search additionally requires the `advanced_search_ai_semantic_search` feature — it is enable-per-plan, NOT per-query metered. See [[apps-advanced-search-settings]].
- **Engine selection.** The `searchBarEngine` setting toggles between the built-in [[apps-listing-engine]] and [[apps-algolia]]; without Algolia installed, built-in is forced. Install order matters. See [[apps-advanced-search-indexing]].
- **Re-index = maintenance mode.** A full re-index puts the storefront into maintenance until the batch completes. One batch runs at a time. See [[apps-advanced-search-indexing]].
- **Result freshness.** Product / category / vendor changes re-index reactively via a background queue (typically seconds); there is no nightly-only batch. See [[apps-advanced-search-indexing]].
- **Analytics retention = 90 days.** Aggregations only consider the last 90 days; the Usage tab additionally caps the visible range at 3 months. See [[apps-advanced-search-analytics]].
- **Order attribution is session-based.** The search term is stored in the customer session and persisted as order meta at checkout. See [[apps-advanced-search-orders]].

## Sub-pages (in this cluster)

- [[apps-advanced-search-settings]] — engine choice, AI Semantic Search toggle, per-field filters + weights, result limits, stopwords; install defaults and save-time validation ranges.
- [[apps-advanced-search-analytics]] — popular queries + no-hits (zero-result) insight; analytics limits (10–500) and the 90-day retention window.
- [[apps-advanced-search-usage]] — Usage tab (Storefront vs Patches/Backend), Grand Total, 3-month date cap, and the Statistics charts.
- [[apps-advanced-search-orders]] — search-driven Orders tab and the session-based search-to-order attribution mechanism.
- [[apps-advanced-search-indexing]] — engine selection (built-in vs Algolia), re-index + maintenance mode, one-batch-at-a-time, freshness, and multi-language indexes.

## Related

- [[apps]] — App Store.
- [[apps-listing-engine]] — the underlying index + embedding service that powers built-in search.
- [[apps-algolia]] — alternative search backend selectable via `searchBarEngine`.
- [[apps-cloudio-overview]] — CloudCart's AI brand; semantic search may use Cloudio's models.
- [[products-products]] — products searched.
- [[products-categories]] — searchable category names.
- [[products-vendors]] — searchable vendor names.
- [[products-property]] — searchable properties.
- [[products-variants-options]] — searchable variants.
- [[orders]] — search-driven orders linked here.
- [[plan-gates]] — concept page.

## Open questions

(None currently outstanding for this page.)
