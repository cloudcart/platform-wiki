---
type: feature
nav_path: "Products → Tags"
route_name: products.tags
route_path: /admin/products/products/edit/:id (Tags section)
aliases: ["Product Tags", "Tags", "Тагове", "Етикети", "Продуктови тагове"]
tags: [products, tags, classification, taxonomy]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---

# Product Tags

## Purpose

**Tags** are free-form labels the merchant attaches to products as a **lightweight cross-cutting classification mechanism**. Different from [[products-categories]] (hierarchical), [[products-vendors]] (1:1 manufacturer), or [[brand-model]] (compatibility) — tags are flat, many-to-many, and the merchant freely defines what each tag means.

Common use cases:
- **Seasonal markers**: "summer-2026", "back-to-school", "holiday-gifts".
- **Promotional flags**: "bestseller", "new-arrival", "clearance".
- **Material / style tags**: "cotton", "minimalist", "vintage".
- **Audience tags**: "gift-for-mom", "kids-safe", "professional-grade".
- **Internal operational tags**: "fragile-packaging", "hand-pick", "long-lead-time".

Tags drive storefront browse filters, [[products-smart-collections]] auto-population, [[apps-cart-rules]] condition matching, size-chart and Google-Shopping mapping, and search relevance — the full consumer list is on [[products-tags-consumers-api]]. This topic is split into focused aspect pages; this hub gives the overview and points to them.

## Sub-pages (in this cluster)

- [[products-tags-assignment]] — the inline tag picker on the product editor (type-to-add, auto-suggest, create-on-Enter, remove), bulk tagging via the list page, and what the merchant can / cannot do.
- [[products-tags-data-model]] — the flat tag record, the dormant SEO / image columns (no admin UI), the automatic storefront filter, and the `/tags/<url-handle>` landing page.
- [[products-tags-lifecycle]] — auto-create on save (`firstOrCreate`), lowercase storage, wildcard (`%` / `_`) stripping, the 100-tags / 191-chars caps, deadlock recovery during imports, and the no-auto-prune rule.
- [[products-tags-consumers-api]] — who consumes tags (Cart Rules, Smart Collections, Google Shopping, size charts, OLX), the JSON-API v2 surface, the `products.tags` permission, and plan gates.

## Where to find it

Per-product tags are managed from the **product edit page**: [[products-products]] → click product → **Tags** section in the right sidebar (Aside).

There is **no standalone "Tags list" page** in the admin — tags are managed per-product, and the platform auto-aggregates the global tag set from per-product assignments. (Contrast with [[marketing-blog-tags]], which DOES have a central admin list.) Full picker behaviour is on [[products-tags-assignment]].

## What the merchant can do here

- Assign / remove tags per product from the editor's Tags aside, and bulk-tag from the list — see [[products-tags-assignment]].
- Let new tags auto-create on save (no "create tag first" step) — see [[products-tags-lifecycle]].
- Rely on the automatic storefront tag filter + `/tags/<url-handle>` landing page — see [[products-tags-data-model]].
- Use tags as conditions in downstream features and set them via JSON-API v2 — see [[products-tags-consumers-api]].

What the merchant **cannot** do: see a global Tags-management page, build tag hierarchies, set tag-level metadata (description / SEO / image), or bulk-rename a tag without a workaround. Details on [[products-tags-assignment]] + [[products-tags-data-model]].

## Settings & fields

A product tag carries effectively one field the merchant sees — the **name** — plus a derived **count**. The full record (including dormant `url_handle` / SEO / image columns) and the storefront filter are documented on [[products-tags-data-model]]. The server-side validation caps (100 tags/product, 191 chars/tag) are on [[products-tags-lifecycle]].

## Business rules

Each rule is documented in full on its aspect page:

- **Auto-create + lowercase + wildcard stripping + caps + no-auto-prune + re-index behaviour** — see [[products-tags-lifecycle]].
- **Dormant SEO / image columns, storefront filter, `/tags/<url-handle>` landing page, no central management page** — see [[products-tags-data-model]].
- **Consumers (Cart Rules, Smart Collections, Google Shopping, size charts, OLX), JSON-API v2 surface, `products.tags` permission, plan-neutral feature with gated consumers** — see [[products-tags-consumers-api]].
- **Distinct from blog tags** — [[marketing-blog-tags]] is a separate system (different table, different filter UI). A `summer` product tag is unrelated to a `summer` blog tag.

## Related

- [[products-products]] — products that get tagged.
- [[products-categories]] — different concept (hierarchical structure, full SEO).
- [[products-vendors]] — different concept (1:1 manufacturer).
- [[products-smart-collections]] — auto-population by tag.
- [[marketing-blog-tags]] — separate tag system for blog articles.
- [[apps-cart-rules]] — uses tags in rule conditions.
- [[apps-size-chart-conditions]] — maps charts via tags.
- [[apps-google-shopping-attributes]] — maps tags to Google attributes.
- [[apps-olx-configuration]] — maps tags to OLX categories.

## Open questions

No outstanding questions at the hub level; aspect-specific verifies are tracked on each sub-page.
