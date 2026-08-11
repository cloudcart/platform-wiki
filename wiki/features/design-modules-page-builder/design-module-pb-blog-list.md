---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Blog list"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Blog list module", "Blog listing block", "Blog feed block", "Модул блог листинг"]
tags: [design, modules, page-builder, blog, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Blog list block (`blog-list`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Blog list** block renders a paginated list of the store's blog articles inside a Dynamic page. The merchant uses it to surface a blog feed on a non-blog page (e.g., a "News" landing page, a marketing campaign page that mixes content blocks with the latest articles, or a custom homepage that ends with the blog roll).

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Blog list** from the block picker.

> **Status note.** The module class (the platform code) and the settings template (`blog-list.tpl`) are both implemented in the codebase, but the entry in the page-builder module registry is currently **commented out** (annotated `//@todo 50-60% ready`). At the time of writing the block does NOT appear in the picker — track this against the current production state. (verify)

## What the merchant can do here

- Pick how many articles per page (2-50; default 10).
- Toggle the master enable switch.

(Additional fields — category filter, sort order, per-row count — may be added when the module ships; verify against the final shipped form.)

## What the merchant cannot do here

- The merchant cannot configure article excerpt length, image size, or layout from this block — those are theme defaults.
- The merchant cannot filter by tag or author from this block (verify — the recent-articles block has those controls; the listing block may not yet).
- The merchant cannot embed an individual article — use the standard blog detail page instead.

## Settings & fields

| Field | Type | Validation | Default | Notes |
|-------|------|------------|---------|-------|
| `enabled` | toggle | `bool` | `true` | Master on/off. Hidden when the module class returns `canDisable == false`. |
| `per_page` | number | `int:2,50` | 10 | Articles per page in the listing. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]] for the builder's save flow.

## Business rules

### Pagination is built-in

The block renders pagination links (next / previous) based on the total article count and the `per_page` setting. The merchant doesn't need to configure pagination separately.

### Article source is the storefront blog

Articles surface via the same listing query as the storefront's `/blog` page — published, non-draft articles, sorted by published date descending. The module doesn't expose a filter to scope by category yet.

### Theme-controlled article card rendering

Each article in the list uses the theme's article-card partial. To customise the look (image size, excerpt length, badge), the merchant would have to switch themes or use [[design-custom-assets]] CSS.

### Currently disabled in the registry

The module map in the platform code has the `blog-list` entry commented out — meaning the block does not appear in the picker even though the underlying class is shipped. This is a known TODO; the module is ~50-60% complete. When enabled, the block will appear in the picker without app-gating.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-modules-blog]] — theme-wide blog modules (different surface — recent articles, recent comments).
- [[marketing-blog-articles]] — the article catalogue this block lists.
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.
- [[marketing-blog-category]] — blog categories (potential future filter).

## Open questions

- 📡 **Final field set.** Once the module ships, confirm whether category / tag filtering, sort order, and per-row count are added. (verify)
- ⏸️ **Shipping date.** The module is annotated `//@todo 50-60% ready` in the registry — track when it's enabled.
