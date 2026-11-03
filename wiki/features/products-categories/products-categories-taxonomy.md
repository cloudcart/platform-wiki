---
type: feature
nav_path: "Products → Categories → Taxonomy (Google Shopping)"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Category taxonomy", "Google Shopping taxonomy", "Google Product Taxonomy", "Define taxonomy modal", "taxonomy_id", "g:google_product_category", "Категория — таксономия", "Google Shopping категория"]
tags: [products, categories, taxonomy, google-shopping, feeds]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, edit modal, hierarchy rules, cart restrictions, deletion rules, JSON-API/validation). SEO title / description / URL handle is on [[products-categories-seo]].

# Categories — Taxonomy (Google Shopping mapping)

## Purpose

The **external taxonomy mapping** the merchant assigns per category: the Google Product Taxonomy `taxonomy_id` read by every feed-generating app (Google Shopping, Meta / Facebook Catalog, Criteo) and the storefront search index — plus the **standalone Define-taxonomy modal** for quick row-by-row assignment from the List tab. (SEO title / description / URL handle is on [[products-categories-seo]].)

## What "category taxonomy" actually IS

CloudCart bundles **Google's official Product Taxonomy** — the canonical ~5,500-node list Google maintains for Google Shopping (e.g. *"Apparel & Accessories > Clothing > Dresses"*). It is the de-facto standard the feed exporters use: **Google Shopping** (required `g:google_product_category` for paid listings), **Meta / Facebook Catalog**, **Criteo**, and other comparison engines (Skroutz, Glami, Compari, …) — see [[apps]] for the full XML-feed catalogue. The list is refreshed from Google's official EN + DE source by a bundled update task.

### The product-inherits-from-category model

**A Product has NO `taxonomy_id` field of its own** — it is defined ONLY on the [[category|Category]] entity, and every feed exporter reads it through the product's category. This is the **key merchant benefit**: assign the taxonomy ONCE on the parent category and every product inside inherits it in every feed — the merchant never taxonomizes products individually. The [[products-products|product editor]] therefore has NO Google taxonomy field; asked *"where do I set the Google taxonomy on this product"* — the answer is *"you don't; set it on the category."*

### Search-index ancestor walk

For the storefront search / filter (powered by [[apps-listing-engine|the listing engine]] — see [[storefront-arch-search-read-side]]), each Variant is indexed with the direct category's `taxonomy_id` **and every ancestor category's** `taxonomy_id`. So a product in *"Smartphones"* is also indexed under *"Phones"* and *"Electronics"* (when those parents carry their own taxonomy), making upward-scoped search ("all electronics") work.

## Where to find it

- **Full Add / Edit modal** — Sidebar → Products → **Categories** → +Add category (or Edit) → the **Taxonomy** card.
- **Standalone Define-taxonomy modal** — Sidebar → Products → **Categories** → List tab → click the **Taxonomy** cell on any row.

## What the merchant can do here

- Assign a **Google Shopping taxonomy** node from a tree-search modal (used by the feed apps + search index).
- Use the **Define taxonomy** standalone modal (from the List tab) to set the taxonomy on one row without opening the full edit modal.

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Google Product Taxonomy** (`taxonomy_id`) | Reference to a node in the taxonomy lookup. Picker is a tree-search modal over ~5,500 nodes. Optional. Read by every feed exporter (Google Shopping, Meta / Facebook Catalog, Criteo) plus the storefront search index; every product in the category inherits it automatically. |

### The standalone Define-taxonomy modal

The List table's **Taxonomy** column lets the merchant set / change the taxonomy WITHOUT opening the full edit modal. Clicking the cell opens a focused **Define taxonomy** modal (`xl`-sized) with only the taxonomy picker. Saving updates the row immediately via the categories API — no full-modal round-trip. This is the merchant's quick path for row-by-row taxonomy assignment.

## Business rules

### Taxonomy assignment is informational, not enforced
Assigning a taxonomy does NOT restrict which products can go into the category — it is metadata read by feed apps and the search index, not a validation gate.

### Taxonomy must exist in the lookup
On save, the server validates that `taxonomy_id` **must exist in the taxonomy lookup**; a deleted / unknown node fails validation. See [[products-categories-api-validation]].

### Feed exporters skip the element gracefully when no taxonomy is set
If a category has no `taxonomy_id`, the Google / Facebook / Criteo XML feed templates **omit the `g:google_product_category` element** for its products. The feed still validates and products still export — they just lack the standard-taxonomy hint. For **paid** Google Shopping, listings without it may be auto-classified or rejected for ad-eligibility on some categories, so merchants running paid Shopping ads should taxonomize every category they sell from; organic Shopping works without it.

### Taxonomy is store-wide, not per-language
The `taxonomy_id` is a single store-wide value — it is NOT translated per storefront language (unlike the category name / SEO fields). See [[multi-language]].

### Permission
Editing the taxonomy requires the products / categories permission; the standalone Define-taxonomy modal has the same requirement as the full edit modal.

## Related

- [[products-categories]] — hub.
- [[products-categories-seo]] — SEO title / description / URL handle (the sibling concern).
- [[products-categories-edit-modal]] — the Taxonomy card lives in the full modal.
- [[products-categories-list-organize]] — the List tab's Taxonomy column opens the standalone modal.
- [[products-categories-api-validation]] — taxonomy validation + JSON-API behaviour.
- [[apps-google-shopping]] — Google Shopping formatter; reads `taxonomy_id`.
- [[apps]] — XML feed exporters (Google, Meta, Criteo, Skroutz, Compari, Glami, …).
- [[category]] — entity page; `taxonomy_id` is a per-category attribute.

## Open questions

- (none)
