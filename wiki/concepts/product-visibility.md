---
type: concept
nav_path: "Concept → Product visibility"
aliases: ["Product visibility", "Why isn't my product showing", "Why is my product not visible", "Product not appearing on storefront", "Product hidden", "Product missing from store", "Draft vs hidden vs inactive", "active_to publish_date", "Защо продуктът ми не се показва", "Продукт не се вижда в магазина", "Скрит продукт"]
tags: [products, visibility, storefront, catalogue, stock, geo, concepts]
plan_gates: []
created: 2026-06-13
updated: 2026-06-13
source_count: 2
---

# Product visibility — why a product appears (or doesn't) on the storefront

## Definition

The set of conditions a product must satisfy to appear in storefront listings, search, and category pages — and the canonical answer to *"why isn't my product showing?"*, the most common catalogue support question. A product surfaces only when **all** of the conditions below hold; failing any one removes it, sometimes silently. The base storefront product query is `active + published` (not draft) plus the listing-level stock / geo / publishing filters.

## Scope

Covered: the catalogue flags (active, draft, hidden), the publishing window, stock gating, geo-zone, category, and the index-sync delay — as one checklist.

Not covered: search relevance / ranking ([[storefront-search-new]]); the stock model itself ([[inventory-tracking]]); the geo rules ([[geo-targeting]]); per-page rendering ([[storefront-architecture]]).

## Contrasts

- **Draft vs inactive vs hidden** — three different "not in listings" reasons: **draft** = never published (work-in-progress); **inactive** (`active = no`) = pulled from sale entirely; **hidden** (`is_hidden = yes`) = published and sellable but **link-only** — excluded from listings / search / category navigation, yet still reachable by its **direct product URL**. So "hidden" means *unlisted*, not *off*.
- **Out-of-window vs inactive** — a product before its `publish_date` or after its `active_to` is auto-hidden by schedule while the Active toggle is still ON — so it can look "off" without being inactive. Unlike *hidden*, an out-of-window product returns 404 even by direct URL (the publish window is enforced on the product-detail page too, verified).
- **Out of stock vs hidden** — an out-of-stock product disappears only when the store hides out-of-stock items AND the product isn't oversell-enabled; otherwise it stays visible (usually with an "Out of stock" label).

## Where it applies — the visibility checklist

A product appears on the storefront only when **every** condition holds:

1. **Active** — `active = yes` (the Active toggle on the [[products-products]] editor). The most common single cause of a missing product.
2. **Published, not draft** — `draft = no` (saved as Published, not Draft).
3. **Not hidden** — `is_hidden = no`. A hidden product is dropped from listings / search / category navigation but stays reachable by its direct product URL — *link-only*, not off.
4. **Inside its publishing window** — its scheduled `publish_date` has passed, and its `active_to` (if set) has **not** passed (after `active_to` the product auto-expires from the storefront).
5. **Sellable for the stock rule** — when the store hides out-of-stock products, a product / variant at 0 stock with `continue_selling = no` is dropped; with `continue_selling = yes` it stays sellable (oversell). See [[inventory-oversell]]; the customer-facing label comes from [[products-statuses]].
6. **In the customer's geo-zone** — geo-targeting can scope a product to specific zones; a shopper outside the allowed zone doesn't see it. See [[geo-targeting]].
7. **Reachable via a category** — products surface in category navigation through their (visible) categories; a product with no visible category may still be found by search but is absent from category browsing. See [[products-categories]].

**Index-sync delay (new engine):** storefront listings + search read from an index, so a just-saved change (new product, status flip, restock) may take until the next sync to appear — not always instant. See [[apps-listing-engine]] / [[storefront-search-new]].

## Where each condition is set (diagnostic)

| Not showing because… | Set / check on |
|---|---|
| Active toggle off | [[products-products]] editor |
| Saved as Draft | editor — Publish vs Save-as-draft |
| Hidden (link-only) | editor — Hidden toggle |
| Before `publish_date` / after `active_to` | editor — publishing schedule |
| Out of stock + no oversell | [[inventory-oversell]] / [[products-statuses]] |
| Outside geo-zone | [[geo-targeting]] / [[settings-geo-zones]] |
| No visible category | [[products-categories]] |
| Just edited, not yet indexed | wait for [[apps-listing-engine]] sync |

## Related

- [[products-products]] — the editor where active / draft / hidden / schedule live.
- [[products-statuses]] — stock-based status labels the customer sees.
- [[inventory-oversell]] / [[inventory-tracking]] — the stock gating.
- [[geo-targeting]] / [[settings-geo-zones]] — zone scoping.
- [[products-categories]] — category-navigation visibility.
- [[storefront-search-new]] — search-side visibility (same base filters).
- [[storefront-architecture]] — storefront rendering engines.
- [[apps-listing-engine]] — keeps the storefront index in sync (the delay).

## Open Questions

None — verified against the listing engine. The base storefront query enforces `active = yes`, `draft = no`, the `publish_date` / `active_to` window, and the geo-zone on **both** listings AND the product-detail page. Only the **hidden** flag and the **out-of-stock** rule are relaxed for direct-URL (detail-page) access. So: a **hidden** or **out-of-stock** product opens by its direct URL (but is absent from listings); a **draft**, **inactive**, or **out-of-window** product returns 404 even by direct URL.
