---
type: feature
nav_path: "Apps → Listing Engine → Embeddings"
route_name: apps.listing_engine.overview
route_path: /admin/apps/listing_engine
aliases: ["Listing Engine embeddings", "e5-small", "Embedding model", "Embedding tokens", "Vector embeddings", "AI semantic search backend", "PRODUCT_LISTING_DRIVER", "MySQL vs the search index driver"]
tags: [apps, search, infrastructure, the search index, embeddings]
plan_gates: ["advanced_search_ai_semantic_search"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-listing-engine]]. See the hub for the other aspects (statistics, re-indexing).

# Listing Engine — Embeddings & semantic search backend

## Purpose

This aspect covers the vector embedding service that powers AI Semantic Search: which embedding model is used, how token consumption is tracked, which plan feature gates access, the difference between the standard search driver and the full AI search driver, and the boundary of what the merchant can and cannot observe or control. It is the "why does semantic search work (or not)?" reference for the cluster.

## Where to find it

There is no embeddings tab in the admin — embeddings are configured at the platform level, not per merchant. The merchant interacts with this aspect indirectly: through the **AI Semantic Search** toggle on [[apps-advanced-search]] and through the embedding-token usage metric. The Listing Engine app lives at `/admin/apps/listing_engine`.

## What the merchant can do here

- **Turn AI Semantic Search on/off** — the toggle lives on [[apps-advanced-search]]; when ON, queries use the vector embeddings stored here; when OFF, queries use lexical (keyword) matching only.
- **Monitor embedding-token usage** — token consumption is tracked as an internal usage metric (`embedding.tokens`), visible as embedding-spend on the [[apps-advanced-search]] Usage tab.

### What the merchant CANNOT do here

- Pick or change the embedding model — it is a platform-operator decision per deployment.
- See the search index operator metrics (query latency p50 / p95, cache hit rate, shard health) — those are platform-operator metrics, not exposed in the merchant admin.
- Get an in-admin alert when the search index has problems — index-health alerts go to platform operators. The merchant only notices when search starts behaving differently.

## Settings & fields

### Embedding service config (platform-level)

| Setting | What it controls |
|---|---|
| `product_listing.embeddings.model` | Embedding model name (default: `e5-small`). |
| `product_listing.embeddings.host` | Self-hosted embedding service URL. |
| `product_listing.embeddings.key` | API key for the embedding service. |
| `product_listing.embeddings.openai_key` | When set, enables the OpenAI backend (`text-embedding-3-small`). |

The embedding API returns vectors for given texts; vectors are stored in the search index for semantic search.

### Driver selection

| Env key | Effect |
|---|---|
| `PRODUCT_LISTING_DRIVER` | `mysql` (default fallback) — lexical / property filtering only, no embeddings. `the search index` — full features including semantic search. |
| `EMBEDDINGS_MODEL` | `e5-small` (default, self-hosted via `EMBEDDINGS_API_HOST` + `EMBEDDINGS_API_KEY`) or `openai` (via `OPENAI_API_KEY`, `text-embedding-3-small`). |
| `EMBEDDINGS_API_ENABLED` | `false` disables embedding generation entirely; AI Semantic Search becomes non-functional even if the toggle is on. |

## Business rules

### e5-small is the active model; OpenAI is the fallback

The platform supports two embedding backends:

- **e5-small** (default) — self-hosted by CloudCart, no external API cost.
- **OpenAI** (`text-embedding-3-small`) — used when the OpenAI key is configured, as a fallback or for higher-quality vectors.

The active backend is selected at the deployment level (not per merchant). The merchant has zero control over which embedding service is used. Future support for larger e5 variants (e5-base, e5-large) is a platform decision.

### Standard search driver = filtering only (no semantic / no embeddings)

The standard search driver implements lexical / property-based filtering (keyword and attribute matching) against the regular product data. It does NOT support vector embeddings or semantic search. For AI Semantic Search to work, the deployment must run `PRODUCT_LISTING_DRIVER=the search index`. The standard driver is intended as a fallback for smaller stores without the dedicated AI search cluster. When the AI search backend has problems, the integration may silently fall back to the standard driver where configured, or surface errors in operator-side logs.

### Embedding tokens are tracked, not billed per token

Each entity's text fields (name, description) are passed through the embedding service, and token consumption is tracked centrally as an internal usage metric — NOT a per-token charge the merchant pays. Tokens consumed during re-indexing or query embedding do not translate to a separate line item; high token usage simply indicates many text changes flowing through the index.

The `advanced_search_ai_semantic_search` plan-feature **mapping exists** (it is created with the Advanced Search app), but as of this revision its **access-enforcement checks are commented out in code** — every the platform code gate is currently disabled. So AI Semantic Search is **not actually plan-gated at present**: availability is driven by the deployment driver + embeddings being enabled + the merchant's toggle (below), not the plan flag. The mapping may be re-activated later, but documenting it as a live gate would be inaccurate today. (verify whether the gate gets re-enabled in a future release.)

### Semantic search requires three things at once

For AI Semantic Search to actually return semantic results, ALL of these must hold: the deployment runs the search index driver; `EMBEDDINGS_API_ENABLED` is true; and the merchant has the AI Semantic Search toggle ON in [[apps-advanced-search]]. Missing any one falls back to lexical keyword matching. (The `advanced_search_ai_semantic_search` plan gate would normally be a fourth condition, but its enforcement is currently commented out — see above — so it does not gate access today.)

## Related

- [[apps-listing-engine]] — hub.
- [[apps-advanced-search]] — carries the AI Semantic Search toggle and the Usage tab where embedding-token spend appears.
- [[apps-cloudio-overview]] — Cloudio AI may use the same embedding infrastructure for some skills.
- [[plan]] — plan tiers gate `advanced_search_ai_semantic_search`.

## Open questions

(None currently outstanding for this page.)
