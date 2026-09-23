---
type: feature
nav_path: "Apps → Aura Search → Settings → System status / Optimization → Index status"
route_name: apps.advanced_search.optimization.index
route_path: /admin/apps/advanced_search/optimization/index
aliases: ["Aura Search index", "search index", "reindex", "re-index", "Update CloudCart search engine index", "rebuild search index", "product not found in search", "new product not in search", "search engine Algolia or CloudCart", "index status", "индекс на търсачката", "преиндексиране", "продуктът не излиза в търсенето"]
tags: [apps, search, indexing, engine]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-09-23
source_count: 5
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, searches, pins, vocabulary, AI, settings).

# Aura Search — the search index and the engine

## Purpose

Aura Search does not search the product tables directly. It searches an **index**: a copy of the catalogue kept in the search engine. This aspect covers which engine answers the search box, how the index stays current, how to rebuild it, and how to tell whether it holds the whole catalogue.

## Where to find it

- **Settings → System status** (right-hand rail) — products, categories and vendors in the index, and the **Update CloudCart search engine index** button.
- **Optimization → Index status** (`/admin/apps/advanced_search/optimization/index`) — per-type counts of the index against the store (*Variants*, *Categories*, *Vendors*), and a summary of orders after a search by status.
- **Overview** — an *index is missing products* card appears when the index falls well behind ([[apps-advanced-search-overview]]).

## What the merchant can do here

- **Rebuild the index** with **Update CloudCart search engine index**. The button is greyed out while the app is off.
- Compare what is indexed with what the store holds.
- Choose the **Search engine** — CloudCart or Algolia ([[apps-advanced-search-settings]]).

## Settings & fields

| Field | Values | Notes |
|---|---|---|
| **Search engine** (`searchBarEngine`) | `cloudcart`, `algolia` | Algolia is offered only while [[apps-algolia]] is installed and active. |

## Business rules

### Which engine answers the search box

- **Algolia not installed, or not active:** the CloudCart engine answers, whatever the setting says. A saved `algolia` choice falls back to `cloudcart` on its own once Algolia is switched off.
- **Algolia active:** the **Search engine** setting decides. With `algolia`, the search box is Algolia's, and Aura Search's dropdown settings (limits, prices, highlighting, all-words matching) no longer apply to it.
- **Installing Aura Search while Algolia is already active** sets the engine to `algolia` from the start. Installed the other way round, it stays `cloudcart` until changed.

### Changes reach the index by themselves, within seconds

Adding, editing or deleting a product, variant, category or vendor — and changes to price, stock, images, visibility, discounts, tags, brand/model and the like — are sent to the index automatically as they happen. The background queue normally applies them within seconds. A large import can make it lag for a while as the queue works through. A nightly pass also applies prices and discounts scheduled for the next day.

A rebuild is therefore **not** part of normal work. It is the fix for an index that has fallen behind — a missing product type, counts that do not match — not a step after every edit.

### 🔴 Rebuilding does not take the store offline

**Update CloudCart search engine index** queues a full rebuild in the background (*Sending data to index was added to the queue.*). **The storefront stays open and search keeps answering** while it runs: every product is re-sent to the index, and entries for things no longer in the store are removed. When it finishes, an admin notification says *Content indexing has been completed successfully.*

Starting a rebuild while one is still running **cancels the first**. Two never run side by side.

(Earlier versions of the platform put the store into maintenance mode for the length of a rebuild. That is no longer the case.)

### Telling whether the index is complete

- **System status** reads *The index is empty* when the app is on but nothing is indexed, and *Everything is running normally* otherwise.
- **Index status** puts each type's indexed count beside the store's own.
- The Overview raises *Your catalogue is not in the search index* or *The search index is missing about N products* when fewer than **70 %** of the store's product variants are indexed, and lists it before every other card: until it is fixed, the other figures describe only what is indexed.

Some difference between the counts is normal. Hidden, inactive and draft products, and products outside the store's zones, are not all indexed. The 70 % threshold is deliberately generous for that reason.

### One index per store, per language

Each store's data is kept apart from every other store's. Each language is analysed with its own rules for word endings and common words, so a multilingual store is matched correctly in each language. Changing the store's main language starts a rebuild automatically ([[settings-general-language]]).

## Related

- [[apps-advanced-search]] — hub.
- [[apps-listing-engine]] — the index itself, and its statistics page.
- [[apps-listing-engine-reindex]] — the same rebuild, seen from the index's side.
- [[apps-algolia]] — the alternative engine.
- [[apps-advanced-search-overview]] — the index-coverage card.

## Open questions

- When the index will report the time of its last update, so that System status can show its reserved *Last synchronised* line.
