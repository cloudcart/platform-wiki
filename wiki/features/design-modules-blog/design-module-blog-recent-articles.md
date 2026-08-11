---
type: feature
nav_path: "Design → Modules → Blog → Latest articles"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Recent articles module", "Latest articles module", "recentArticles", "blog.recentArticles", "Latest News", "Recent Articles", "Последни статии", "recent-articles"]
tags: [design, modules, blog, homepage, recent]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Storefront Modules — Recent articles (`recentArticles` + page-builder block)

> Part of [[design-modules-blog]]. See the category page for the other blog modules.

## Purpose

The **Recent articles** module renders a short row of the most recently published blog articles. It exists in TWO distinct forms (the platform did NOT merge them), each with its own surface:

| Form | Surface | Settings |
|---|---|---|
| Legacy storefront module (`blog.recentArticles`) | Modules screen → **Blogs, articles and comments** tab → **Latest articles** card | enabled + count |
| Page-builder Recent Articles block (`recent-articles`) | Inside a Dynamic page in [[marketing-landing-pages]] | enabled + count + per_row + title + category_id + order_by + order_direction |

Both render the same storefront article row, but only the page-builder block exposes per-category filtering and sort options. The legacy variant drives global "Latest articles" rows the theme has slotted into header / sidebar / homepage; the page-builder variant drives ad-hoc landing-page rows.

## Where to find it

- **Legacy variant:** Sidebar → **Design** → **Modules** → **Blogs, articles and comments** tab → click the **Latest articles** card. The form opens in a side panel.
- **Page-builder variant:** Sidebar → **Marketing** → **Pages** → open a Dynamic page → drag the **Recent Articles** block from the palette. See [[marketing-landing-pages]].

## What the merchant can do here

### Legacy storefront variant (`recentArticles` / `recentArticlesHome`)

- **Set the count** of articles to show (2-10).
- **Disable** the row entirely with the master switch.
- Save / Reset / Cancel — standard pipeline.

Cannot: filter by blog category, pick a sort order (always newest-first), set a custom title, or change the per-row count (theme-controlled).

### Page-builder Recent Articles block

- **Set the count** (2-10) and **per-row** count (1-5) for desktop.
- **Set a title** shown above the row (0-100 chars).
- **Filter by blog category** via the picker (or "all" for every category).
- **Pick a sort field** (`created_at`, `name`, or `rand`) and **direction** (`asc` / `desc`, hidden when sort is `rand`).
- Drag the block to any position on the Dynamic page canvas.

## Settings & fields

### Legacy storefront module (`blog.recentArticles`)

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | on / off | `bool` | Hides the row when off |
| `count` | int | `5` | 2-10 | `int:2,10` | Number of articles in the row |

### Page-builder Recent Articles block

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `enabled` | bool | `true` | on / off | `bool` | Hides the block when off |
| `per_row` | int | `3` | 1-5 | `int:1,5` | Cards per row on desktop |
| `count` | int | `5` | 2-10 | `int:2,10` | Total articles to fetch |
| `title` | string | `null` | free text | `char:0,100` | Section heading shown above the row |
| `category_id` | int / null | `null` | blog category ID or null | optional; resolved against the blog-categories catalogue | When null, shows every category |
| `order_by` | enum | `created_at` | `created_at` / `name` / `rand` | `in:created_at,name,rand` | `rand` triggers a random order on each render |
| `order_direction` | enum | `desc` | `asc` / `desc` | `in:asc,desc` | Ignored when `order_by = rand` |

### Validation behaviour (both forms)

- Unknown fields are dropped on save; the legacy variant silently ignores any field other than `enabled` and `count`.
- In the page-builder block, an empty `category_id` becomes null, and an invalid `order_by` / `order_direction` falls back to its default.

## Theme dependencies

Most themes ship the legacy `recentArticles` instance as the canonical "Latest articles" homepage row, and often a second instance (`recentArticlesHome`) so a homepage row can be configured separately from a sidebar row — see [[design-module-blog-home]]. The page-builder block is theme-independent. Both variants use the active theme's article-row template (its override if present, otherwise the platform default).

## Business rules

### The legacy variant ALWAYS sorts newest first

There is no merchant control — it always returns the most recent N articles, newest first (by article ID, descending). For sorted / curated rows, use the page-builder block.

### The page-builder variant is the ONLY place category filtering exists

The legacy `blog.recentArticles` module always pulls from the global recent pool — it cannot be filtered by category. Per-category curation on a landing page requires the page-builder block with `category_id` set.

### `rand` sort randomises on every page load

Setting `order_by = rand` makes the row pick N random articles per request, shuffling each visit — useful for surfacing evergreen back-catalogue content.

### Both variants pull from the SAME published pool

Both show only published articles that belong to a blog category. Drafts, archived articles, and articles without a category are excluded — neither form can override this. If the result is empty (empty blog, or a `category_id` filter matching no published articles), the row renders nothing — no empty-state message.

### Hero image fallback

The thumbnail comes from each article's hero image set in [[marketing-blog-articles]]. If an article has no image, the theme falls back to a placeholder (theme-controlled); the module itself does NOT supply a generic asset.

### Save / Reset / Cancel — legacy variant only

The legacy variant uses the standard Modules screen buttons:

| Button | Action | Confirmation | Success message |
|---|---|---|---|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes panel | None | — |

The page-builder block has no per-block save button — it is saved by saving the Dynamic page itself.

### Where settings live + cache

The legacy variant keeps per-instance settings keyed by the instance name (e.g. `recentArticles`); the page-builder block stores its config on the Dynamic page, so different pages carry independent configs. Saving the legacy variant refreshes the storefront modules cache; saving the Dynamic page refreshes the page cache. Newly published articles surface immediately in either variant — the article list is fetched live, not cached.

## Tips for merchants

- Use the legacy variant for an always-newest homepage row; use the page-builder block with `category_id` for per-category landing pages.
- The hard maximum is 10 articles in either variant. For longer lists, link to the full blog landing page (`/blog`) — see [[design-module-blog-listing]].
- The page-builder block inherits the theme's button + card styling, so the row matches the storefront without touching CSS.

## Related

- [[design-modules-blog]] — hub.
- [[design-module-blog-listing]] — primary `blog` module; the full listing the row links into.
- [[design-module-blog-home]] — `recentArticlesHome` homepage-scoped instance pattern.
- [[design-module-blog-recent-comments]] — sibling Latest comments row.
- [[marketing-blog-articles]] — articles displayed by the row.
- [[marketing-blog-category]] — categories used by the page-builder filter.
- [[marketing-landing-pages]] — Dynamic page builder; hosts the page-builder variant.

## Open questions

- 📡 **Page-builder plan gating.** The Dynamic page builder is gated by the `storefront_builder` plan feature — without it, the page-builder Recent Articles block is unreachable. GraphQL-resolvable: query the merchant's plan + feature stacks.
- 📡 **Per-language `title`.** The page-builder block's `title` is stored as a single string by default; per-language storage is enabled by the `multylang` app (verify).
