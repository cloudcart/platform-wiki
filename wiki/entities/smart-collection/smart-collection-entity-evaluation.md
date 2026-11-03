---
type: entity
aliases: ["Smart Collection evaluation", "Collection membership refresh", "Selection cached product list", "Smart Collection status flag", "Pending vs Finished collection", "Преизчисляване на колекция"]
tags: [catalog, products, collections, smart-grouping, evaluation, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[smart-collection]]. See the hub for the other aspects (rule builder, storefront, discount link, vs category, management).

# Smart Collection — evaluation & caching

## Identity

**Evaluation** is the asynchronous process that turns a [[smart-collection|Smart Collection]]'s rules (see [[smart-collection-entity-rule-builder]]) into a concrete list of matching products and caches that list on the collection record. The merchant never sees rules being evaluated on a page load — the storefront reads a **cached product list**, and a background job keeps that cache current. Two record fields expose freshness to the merchant: a Status flag (`executing`) and a timestamp (`last_generated_at`).

## Aliases

- "Evaluation" / "membership refresh" / "re-generation" — the recomputation of which products match.
- "Cached product list" — the denormalised `products` field.
- "Status" / "Pending" / "Finished" — the merchant-facing surfacing of the `executing` flag.
- Bulgarian: "Преизчисляване на колекция".

## Key Attributes

### Cached product list — the storefront reads the cache, not the rules

The collection record stores the resolved product IDs in its `products` field. The storefront category-render and the landing page do **NOT** re-evaluate the rules on each request — they read the cached list. The evaluation job updates the cache, then a storefront cache flush propagates the new list to all storefront surfaces (landing page + any module showing the collection). The `products` field is denormalised precisely so page loads stay cheap.

### Status flag tells the merchant when the collection is ready

The Status column on [[products-smart-collections]] exposes the `executing` flag as a badge:

- **Pending** (`executing = true`) — membership is being re-evaluated in the background.
- **Finished** (`executing = false`) — evaluation complete; the cached list is current. `last_generated_at` updates on completion.

The merchant should not assume a freshly-edited collection is settled until the badge reads Finished — for the discount-linking caveat see [[smart-collection-entity-discount-link]].

### What triggers re-evaluation

- **Rule / metadata edit.** The merchant changes any criteria row, adds / removes a row, or edits the name / SEO / image. On save, the collection re-enters Pending until the job completes.
- **Underlying product change.** A product whose data is potentially relevant (price, category assignment, vendor, tags, properties, sale flag, etc.) is created, edited, or deleted. The platform re-evaluates affected collections automatically:
  - Adding a product whose data matches → added on the next evaluation cycle.
  - Editing a product so it stops matching → removed on the next cycle.
  - Deleting a product → removed.

### Latency at scale

The evaluation job runs on the standard background queue alongside other catalog jobs. For stores with 50,000+ products, evaluation typically completes within **1–5 minutes**; longer for very complex rule combinations. For typical catalogs it is close to real-time. There is **no queue-depth indicator** visible to the merchant — the Status badge (Pending vs Finished) is the only signal. Until the first evaluation completes after creation, the storefront serves an **empty** list.

### Debounce on rapid catalog changes

A single product change flushes only the affected collection's landing-page cache, not every collection on the site. For rapid catalog imports (bulk-updates on hundreds of products), the platform **debounces** evaluation by collection — multiple product changes within a short window collapse into a single evaluation run.

### Side effects on save / delete

A save or delete triggers:

- **Search re-index** — products in the collection get search-index updates so storefront search reflects the new grouping.
- **Storefront cache flush** — the collection landing page and any storefront module showing the collection are flushed (per-collection, not site-wide).
- **Discount re-evaluation** — if discounts are linked, they are re-evaluated against the new product set. See [[smart-collection-entity-discount-link]].

## Where it appears

- [[products-smart-collections]] — the Status column and Products count read these fields.
- [[products-products]] — editing a product can trigger affected-collection re-evaluation.
- Storefront landing page at `/selection/<url-handle>` — reads the cached `products` list. See [[smart-collection-entity-storefront]].

## Related

- [[smart-collection]] — hub.
- [[smart-collection-entity-rule-builder]] — the rules that evaluation computes.
- [[smart-collection-entity-discount-link]] — discounts re-evaluate when membership settles.
- [[product]] — product changes drive re-evaluation.
- [[products-smart-collections]] — where the Status badge surfaces.

## Open Questions

None.
