---
type: storefront-page
route_name: blog.list
route_path: /blog
themes_using: [all]
tags: [storefront, blog, listing]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Blog list (storefront)

## Purpose

Public landing page for the merchant's blog — a paginated list of every published article across every blog. Customers reach it from the main menu link "Blog" (added by most themes), from a blog module on the homepage, or directly via `/blog`.

## URL & route

- **Route name:** `blog.list`
- **Path:** `/blog`
- **Middleware:** `uuid_generate`, `subscriber_uuid` (anonymous-visitor tracking).
- **Method:** `GET`.

## How it loads

1. The route resolves to the request handler (verify).
2. The blog module (the platform code) is initialised with `handle(segment(2))` — empty on `/blog`, so it lists every active article from every blog.
3. The template guards on the platform code. If the **Blog** app is disabled in the merchant's store, the page renders the error notification `sf.module.blog.err.blog_is_disabled` instead.
4. SEO metadata comes from `$module->setSeo('blog')` and the global metatag template at the theme templates.

## What the customer sees

- Breadcrumb: **Home › Blog**.
- Section title from the platform code.
- Main column: a list/grid of article cards rendered by the theme templates. Each card includes:
  - Cover image (thumb size `600x600`, lazy-loaded with `lazyload-image`).
  - Article title (links to `/article/{slug}`).
  - Short excerpt and publish date (`siteDateTime($article->created_at)`).
  - Author name and tags (if assigned).
- Pagination bar from the theme templates.
- Right-hand sidebar from the theme templates containing: list of blogs, recent articles, recent comments, and tag cloud.
- Sidebar collapses to a slide-in panel on mobile, toggled by `.js-sidebar-toggler`.

## Storefront behaviour

- Pagination is page-based; `page=N` query parameter is appended to `/blog?page=2`.
- Article listing respects the per-blog "active" flag — disabled blogs/articles are excluded server-side.
- Microdata for the blog as a whole is emitted via the theme templates; per-article schema is emitted inside the theme templates.

## JavaScript behaviour

- `.js-sidebar-toggler` — opens/closes the filter sidebar on small screens.
- `.js-loader-articles` — loader placeholder shown while AJAX pagination/filter requests are in-flight (when the theme switches to AJAX paging).
- Cards rely on the global `lazyload-image` class for lazy image loading.

## Customisations available to the merchant

- **Blog app on/off** — disabling it hides the entire page (renders the disabled notification).
- **Articles, categories, tags** — managed under [[marketing-blog-articles]], [[marketing-blog-category]], [[marketing-blog-tags]].
- **Per-article publish state** — only `active = yes` articles appear.
- **Sidebar content** — driven by the active theme's sidebar template; recent-comments box only appears when the relevant module has data.
- **Comments globally** — toggled per-article and per-blog (see [[marketing-blog-comment]]).
- **Theme editor** — listing columns/grid density depend on the active theme; some themes ship a [[design-modules-blog]] block that mirrors the same articles on the homepage.

## Theme variations

- All Smarty themes use `templates/blog/blog.tpl` with the same module call. Layout differences (grid vs list, image ratio, sidebar position) are CSS-only.
- Themes without a blog sidebar (e.g., some minimal themes — verify) omit the right column.
- Liquid-engine themes (Headless / Storefront API) bypass this controller — see [[storefront-architecture]].

## Known issues / by-design vs bug

- Disabling the Blog app does NOT 404 the URL; it renders a disabled-blog notice inside the normal layout (by design — keeps direct links from breaking).
- The route is registered even for sites that never publish a blog; SEO-wise this can produce a thin page. Recommend the merchant link to it from menus only when articles exist.

## Related

- [[blog-filter]]
- [[storefront-blog-article]]
- [[marketing-blog-articles]]
- [[marketing-blog-category]]
- [[marketing-blog-tags]]
- [[marketing-blog-comment]]
- [[design-modules-blog]]
- [[storefront-architecture]]
- [[storefront-known-issues]]

## Open questions

- Confirm controller class path (the request handler) on latest builds.
- Confirm whether any production theme renders this page with infinite-scroll instead of numbered pagination.
- Confirm exact thumb sizes per theme (Flair uses `600x600`).
