---
type: feature
nav_path: "Apps → Algolia"
route_name: apps.algolia.overview
route_path: /admin/apps/algolia
aliases: ["Algolia", "Algolia search", "Algolia integration"]
tags: [apps, search, algolia, external-search, alternative]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 7
---
# Algolia

## Purpose

**Algolia** integration — replaces CloudCart's built-in storefront search with **Algolia's hosted search service**. Algolia is a leading external search provider with sub-50ms global response times, instant search, typo tolerance, ranking customisation, and personalization features.

Used by merchants who:
- Want a faster, more polished search experience than the default.
- Have large catalogs (100k+ products) where built-in search struggles.
- Want Algolia-specific features like personalization, A/B testing, dynamic re-ranking.
- Already use Algolia on other sites and want consistency.

Alternative to [[apps-listing-engine]] + [[apps-advanced-search]] (the built-in stack). When Algolia is enabled, search queries route to Algolia's API instead. This page is the **hub** for the Algolia cluster; deep mechanics live on the aspect pages below.

## Where to find it

Sidebar → Apps → install → **Algolia**. The route is `/admin/apps/algolia`.

## What the merchant can do here

- **Enter credentials** — Application ID + Admin API Key + Search API Key (see [[apps-algolia-credentials]]).
- **Configure result-display limits** — products / categories / vendors counts + show-price toggle (the day-to-day settings tab is documented on [[apps-algolia-settings]]).
- **Upload data to Algolia** — the `btn.start_indexing` button enqueues a queue-backed batch upload of products + categories + vendors (see [[apps-algolia-indexing]]).
- **Read the install help text** — Header (`header.install`): *"Algolia"*; Help (`help.install`): *"With this app you will improve, optimize and personalize the search results into your CloudCart store. If you want to give an unique way to instantly visualize search results and grant your users a discovery experiences than this application is just for you."*

### What the merchant CANNOT do here

- Use Algolia AND the built-in [[apps-listing-engine]] simultaneously — Algolia replaces the default search (the merchant picks one stack).
- Index more data than the Algolia plan allows — Algolia's operation quota limits apply (see [[apps-algolia-dashboard]]).
- Configure Algolia ranking rules / synonyms / facets / personalization from the CloudCart UI — those live in Algolia's dashboard (see [[apps-algolia-dashboard]]).

## Settings & fields

| Field (lang key) | Notes |
|---|---|
| `appId` | Algolia Application ID (from Algolia dashboard). |
| `apiKey` | Algolia Admin API Key (write-capable). |
| `searchApiKey` | Algolia Search API Key (read-only; used by storefront autocomplete). See [[apps-algolia-credentials]]. |
| `count.products` | Result-count for products in storefront search. |
| `count.categories` | Result-count for categories. |
| `count.vendors` | Result-count for vendors. |
| `show_price` | Whether to display product price in result cards. |

Validation error strings (full handling on [[apps-algolia-credentials]]):

- **Missing settings** (`error.missing_settings`): *"You have not saved your Application ID и Admin API Key"* (the Bulgarian "и" in the EN string is a translation bug).
- **Quota exceeded** (`error.quota_exceeded`): *"Operations quota exceeded in Algolia, change plan to get more operations."*

## Business rules

### Replaces default search

When Algolia is active and credentials are validated, storefront search routes to Algolia instead of [[apps-listing-engine]] + [[apps-advanced-search]]. The internal index becomes inactive.

### Credentials-based auth, not OAuth

Pure API key/ID auth — no OAuth roundtrip. The three keys are pasted from Algolia's dashboard. See [[apps-algolia-credentials]].

### Queue-backed, plan-capped indexing

The "Upload data to Algolia" button enqueues a batch job (chunks of 300 products) rather than running synchronously, and a plan-feature cap limits how many products may be indexed. Full mechanics on [[apps-algolia-indexing]].

### Dashboard-side configuration

Facets, ranking rules, synonyms, personalization, A/B testing, and analytics all live in Algolia's own dashboard — CloudCart surfaces none of them. See [[apps-algolia-dashboard]].

## Sub-pages (in this cluster)

- [[apps-algolia-credentials]] — the three required credentials (`appId` + admin `apiKey` + `searchApiKey`); live-watch validation; sync gating; the `isConfigured` gate on Start indexing; the "и" translation bug.
- [[apps-algolia-indexing]] — queue-backed upload, 300-product chunks, the `algolia` plan cap, the auto-sync listener (active + visible + non-draft gating), the nightly 00:10 UTC repeatable full sync, and why only products / categories / vendors sync.
- [[apps-algolia-dashboard]] — what stays in Algolia's dashboard (facets, ranking, synonyms, personalization, A/B, analytics); multi-language indexes; plan-cost not estimated; quota-exceeded handling; error-log filtering; no-fallback behaviour when Algolia is down.

(The day-to-day Settings tab also has its own page, [[apps-algolia-settings]].)

## Related

- [[apps]] — App Store hub.
- [[apps-algolia-settings]] — the Settings tab where credentials + display limits are entered.
- [[apps-listing-engine]] — built-in search infrastructure (alternative).
- [[apps-advanced-search]] — built-in search UI (alternative — uses Listing Engine).
- [[products-products]] / [[products-categories]] / [[products-vendors]] — indexed entities.

## Open questions

(None currently outstanding for this page.)
