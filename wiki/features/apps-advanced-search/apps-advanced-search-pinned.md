---
type: feature
nav_path: "Apps → Aura Search → Optimization → Pinned products"
route_name: apps.advanced_search.optimization
route_path: /admin/apps/advanced_search/optimization
aliases: ["pinned products", "pin a product", "pin product to top", "product at the top of search", "merchandising", "boost product for a search term", "pin products in category", "force product first", "закачени продукти", "закачи продукт", "продукт най-отгоре в търсенето", "продукт първи в категория"]
tags: [apps, search, merchandising, categories, vendors]
plan_gates: ["advanced_search"]
created: 2026-09-23
updated: 2026-09-23
source_count: 5
---

# Aura Search — pinned products

> Part of [[apps-advanced-search]]. See the hub for the other aspects (plans, overview, searches, vocabulary, AI, settings, indexing).

## Purpose

A **pin list** forces chosen products to the top of a listing, in the merchant's order. It is the direct answer to *"when a customer searches X, I want product Y first"*, and it works for a category page and a vendor page too.

## Where to find it

**Apps → Aura Search → Optimization → Pinned products** (`/admin/apps/advanced_search/optimization`). A pin list can also be started from an opportunity card or a term's drill-down (**Pin a product**), with the term filled in.

## What the merchant can do here

- **Add** a pin list for a **search term**, a **category** or a **vendor**.
- Pick up to **10 products**, **drag to reorder** them, **remove** any.
- **Edit** a list's products later, or **delete** the list.
- Filter the table by **Type** and by whether a list **Has products**.

## Settings & fields

| Field | Applies to | Notes |
|---|---|---|
| **Listing type** | all | **Search term**, **Category** or **Vendor**. Fixed once saved. |
| **Search term** | search term | Up to 191 characters, e.g. *cooker*. |
| **Match** | search term | **Exact query** or **Contains the term** — see below. |
| **Listing** | category / vendor | The category (shown with its full path) or the vendor. |
| **Pinned products** | all | Up to 10, in the order shown. *You can pin up to 10 products.* |

A list's owner cannot be changed on edit; a different term or category means a new list.

## Business rules

### One list per category, per vendor, per term-and-match

A category or vendor holds **one** pin list; adding a second is refused with *This listing already has a pin list*. For search terms, one list per term **and** match type: *A pin for this search term already exists*. The same word can have one **Exact** and one **Contains** list.

### Exact versus Contains

| Match | Fires when |
|---|---|
| **Exact query** | The shopper's whole search is the term. *cooker* fires on *cooker* only. |
| **Contains the term** | Every word of the term appears in the search, in any grammatical form. *cooker* fires on *gas cooker* and *cookers*. |

When several lists fit one search, **one** wins: an **Exact** list beats any Contains list, and among Contains lists the one with the **most words** wins. Pins from different lists are never mixed.

### 🔴 Pinned products appear even when they do not match the words

A product pinned to a term is **put into the results** for that term whether or not its name contains the words. That is the point of it: the merchant decides. It must still be **visible and orderable** on the storefront. Hidden, inactive or draft products are not shown by being pinned ([[product-visibility]]), and a filter the shopper applied still narrows the list.

### Where pinned products go

- **Search** — to the top of the results, in the pinned order, in both the dropdown and the full `/search` page.
- **Category / vendor page** — to the top of **page one**.
- If the store pushes out-of-stock products to the end of listings (`order_latest_out_of_stock`, [[design-module-product-filters]]), a pinned product still respects that: a pinned in-stock product tops the sellable ones, and a pinned out-of-stock product tops only the out-of-stock ones.

### 🔴 A pin switches off the ranking signals for that search

On a search where a pin list fires, the pinned products lead and **the rest of the results stay in plain relevance order**. The ranking signals set on the AI & relevance tab — best-selling, discount, featured and the others — are **not applied** to that search ([[apps-advanced-search-ai]]). Searches with no pin keep them.

### Pins work while the app is on — over quota too

Pins are read when the app is installed **and enabled**. They keep working after the month's search quota is used up ([[apps-advanced-search-plans]]). A disabled app shows no pins anywhere: the pin lists are kept, not deleted, and apply again once it is re-enabled.

### Changes need no reindex; deletions clean up after themselves

A category or vendor list applies from the next page load. A search-term list is handed to the search engine in the background and applies within moments. Neither needs the index rebuilt.

Deleting a product removes it from every pin list, and a list it leaves empty is removed. Deleting a category or vendor removes its list. Deleting a list removes only the list, not the products.

A pin has no dates: it applies until it is edited or deleted.

## Related

- [[apps-advanced-search]] — hub.
- [[apps-advanced-search-analytics]] — the **Optimize** and **Low conversion** terms that usually call for a pin.
- [[apps-advanced-search-overview]] — the *searched often and never ordered* card that opens this form.
- [[apps-advanced-search-ai]] — the ranking signals a pin overrides.
- [[apps-advanced-search-vocabulary]] — synonyms, for when the right product exists but is not found.
- [[products-categories]], [[products-vendors]] — the listings a pin list can belong to.
- [[product-visibility]] — why a pinned product may still not show.

## Open questions

(None currently outstanding for this page.)
