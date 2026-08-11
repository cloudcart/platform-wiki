---
type: feature
nav_path: "Design → Modules → Blog"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Blog modules", "Blog module", "Recent articles module", "Recent comments module", "Article module", "Blog list module", "Blog panel", "Blog modules side panel", "Модули - Блог", "Последни статии", "Последни коментари"]
tags: [design, modules, blog, content]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# Storefront Modules — Blog

## Purpose

The **Blog modules** drive every blog-related storefront surface — the blog landing page, individual article pages, the "Latest articles" row on the homepage, the "Recent comments" sidebar block, and the internal admin side panel that lets other admin surfaces open the blog-module picker. They pull content from the blog admin ([[marketing-blog-articles]], [[marketing-blog-category]], [[marketing-blog-comment]]) and render it in slots the active theme has placed for them.

Three of these modules are **editable** on the Modules screen (Blog, Latest articles, Last comments). One is a **system module** that has no merchant settings (the per-article page). Two are **specialised instances / panels** that piggy-back on the same module types. This page is the navigation pivot for the cluster — drill into the aspect that matches the question.

## Sub-pages (in this cluster)

- [[design-module-blog-listing]] — the `blog` instance (`blog.blog`) that drives `/blog`, `/blog/category/{slug}`, `/blog/tag/{slug}` — per-page count + enable / disable.
- [[design-module-blog-home]] — the `blogHome` / `recentArticlesHome` secondary instances for the homepage "Featured / Latest articles" row.
- [[design-module-blog-recent-articles]] — the `recentArticles` row PLUS the page-builder Recent Articles block (the only place where per-category curation + sort are exposed).
- [[design-module-blog-recent-comments]] — the `recentComments` sidebar block; surfaces approved comments across all articles.
- [[design-module-blog-article]] — the `article` SYSTEM module that renders one article on `/article/{slug}` and hosts the comment form + thread.
- [[design-module-blog-panel]] — the blog-modules side panel (`/admin/storefront/widgets/blog/panel`) used by the page builder to open the blog-module picker without leaving context.

## Where to find it

Sidebar → **Design** → **Modules** → **Blogs, articles and comments** tab.

Three cards always appear (when the active theme ships them):

| Card | Module type | Sub-page |
|---|---|---|
| **Blog** | `blog.blog` | [[design-module-blog-listing]] |
| **Latest articles** | `blog.recentArticles` | [[design-module-blog-recent-articles]] |
| **Last comments** | `blog.recentComments` | [[design-module-blog-recent-comments]] |

The remaining blog modules do NOT have a card here:

| Module | Why no card |
|---|---|
| `article` (`blog.article`) | System module — auto-renders on `/article/{slug}`; no merchant fields. See [[design-module-blog-article]]. |
| Page-builder Recent Articles block | Exposed inside the Dynamic page builder ([[marketing-landing-pages]]). See [[design-module-blog-recent-articles]] for the page-builder fields. |
| Blog modules side panel | Internal helper panel — opens the blog-tab list from other admin surfaces. See [[design-module-blog-panel]]. |

## What the merchant can do here

Common actions for the three editable cards (exact messages in the Save / Reset / Cancel table under Business rules):

- **Save module** — persists settings; storefront cache regenerates and new settings are live on the next page load.
- **Reset module** — wipes the merchant's saved settings and reverts to theme-shipped defaults.
- **Cancel** — closes the panel without saving.
- **Enable / disable** — every form has a master toggle. When OFF, the module is hidden on the storefront.

What the merchant CANNOT do:

- Add new blog-module instances — the catalogue is theme-fixed (see [[design-themes]]).
- Rename or move module instances.
- Edit the underlying blog posts here — that's [[marketing-blog-articles]] / [[marketing-blog-category]] / [[marketing-blog-comment]].
- Configure the article-page layout — controlled by the active theme; the article-view module has no settings form.

## Settings & fields

Per-module settings live on each sub-page (link tables follow the same schema — key / type / default / allowed / validation / notes). Quick map:

| Module | Settings | Sub-page |
|---|---|---|
| `blog` (`blog.blog`) | `enabled`, `per_page` (2-50) | [[design-module-blog-listing]] |
| `blogHome` / `recentArticlesHome` | inherits from `blog.blog` or `blog.recentArticles` | [[design-module-blog-home]] |
| `recentArticles` (`blog.recentArticles`) | `enabled`, `count` (2-10) | [[design-module-blog-recent-articles]] |
| Page-builder Recent Articles block | `enabled`, `count`, `per_row`, `title`, `category_id`, `order_by`, `order_direction` | [[design-module-blog-recent-articles]] |
| `recentComments` (`blog.recentComments`) | `enabled`, `count` (2-10) | [[design-module-blog-recent-comments]] |
| `article` (`blog.article`) | none — system module | [[design-module-blog-article]] |

## Business rules

### The blog module catalogue is theme-driven

Which of the three editable cards appear on the Modules screen depends on the active theme. A theme that doesn't ship a `recentArticles` instance will not show the "Latest articles" card. Switching themes via [[design-themes]] can change the catalogue — settings for instances that disappear are KEPT in the database but become non-editable until the merchant switches back.

### Save / Reset / Cancel — standard for all editable blog modules

| Button | Action | Confirmation | Success message |
|---|---|---|---|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes panel | None | — |

### Cache invalidation on save

Save and Reset both regenerate the storefront cache — new settings appear on the next request, no manual cache-clear needed. New articles published in [[marketing-blog-articles]] surface immediately without any module save.

### Plan gating

None of the blog modules are plan-gated — they are available on every plan that has blog enabled. The page-builder Recent Articles block IS gated by the `storefront_builder` feature (the whole Dynamic page builder is) — see [[marketing-landing-pages]].

### Settings are stored per instance

Settings are saved per instance name (`blog`, `blogHome`, `recentArticles`, `recentArticlesHome`, `recentComments`). Two themes that use the same module TYPE (e.g. `blog.blog`) under different INSTANCE names keep their settings INDEPENDENT.

### Third-party comment apps override the native comment surface

When the merchant installs Disqus ([[apps-disqus-comments]]) or Facebook Comments ([[apps-facebook-comments]]), the article-page comment slot switches to the third-party block at the THEME level. The native Recent Comments module still queries the native pool — but new approved comments stop arriving because the form is replaced. See [[design-module-blog-article]] and [[design-module-blog-recent-comments]] for per-module impact.

### No page-builder "Blog list" block

The Dynamic page builder has no working "Blog list" block. The active page-builder block for blog content is the **Recent Articles** block — see [[design-module-blog-recent-articles]]. If a merchant looks for a page-builder "Blog list" block, point them at Recent Articles instead.

### Non-editable modules show no card

A module whose theme declares it non-editable shows no card and its settings form returns a 404.

## Related

- [[design-modules]] — parent module catalogue (overview + tab structure).
- [[design]] — pillar hub for Design.
- [[design-themes]] — theme picker; theme decides which blog modules appear.
- [[design-modules-navigation]] — sibling module category (header / footer / search / logo).
- [[design-modules-products]] — sibling module category (product modules).
- [[design-modules-utility]] — sibling module category (vendors, providers, filters, social, etc.).
- [[marketing-blog-articles]] — source of articles displayed by the blog modules.
- [[marketing-blog-category]] — blog categories (used as the filter in the page-builder Recent Articles block).
- [[marketing-blog-tags]] — blog tags (used in tag-filter routes).
- [[marketing-blog-comment]] — comment moderation (gates what Recent Comments shows).
- [[marketing-landing-pages]] — Dynamic pages use the page-builder, which exposes the Recent Articles block.
- [[apps-disqus-comments]] — third-party Disqus integration (alternative to native comments).
- [[apps-facebook-comments]] — third-party Facebook comments integration.

## Open questions

- 📡 **Page-builder "Blog list" revival.** A blog-list page-builder block is implemented but disabled. Verify whether it will be enabled in an upcoming release or replaced entirely by the Recent Articles block.
- 📡 **Per-language module content.** With multi-language enabled, module text fields (titles, captions) accept per-language entries via the language switcher.
