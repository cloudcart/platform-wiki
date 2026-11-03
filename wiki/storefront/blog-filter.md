---
type: storefront-page
route_name: blog.view
route_path: /blog/{filter}/{slug}
themes_using: [all]
tags: [storefront, blog, listing, filter]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Blog filtered listing (storefront)

## Purpose

Paginated article list scoped to a single blog category or tag. Same visual layout as [[blog-list]] but pre-filtered. Reached from the blog sidebar (categories list, tag cloud), from breadcrumbs on the article page, or from internal links inside article bodies.

## URL & route

- **Route name:** `blog.view`
- **Path:** `/blog/{filter}/{slug}` where `{filter}` is constrained by `where('filter', '(category|tag)')`.
  - Examples: `/blog/category/news`, `/blog/tag/promotions`.
- **Middleware:** `uuid_generate`, `subscriber_uuid`.
- **Method:** `GET`.

## How it loads

1. Route resolves to the request handler (verify).
2. the platform code here receives the `{filter}` segment; internally the controller scopes the article query by category or tag depending on the segment, using `{slug}` to identify the term.
3. Template is shared with the unfiltered listing (`templates/blog/blog.tpl`) — the platform code block, sidebar include, and microdata stay identical.
4. SEO meta: `$module->setSeo('blog')` plus the theme templates.

## What the customer sees

- Breadcrumb: **Home › Blog › <Category or Tag name>** — the active label is the platform code which returns the category/tag label.
- `<h1>` matches the breadcrumb tail.
- Article cards, pagination, sidebar all rendered exactly as on [[blog-list]].
- If the slug does not match any category/tag, the listing comes back empty (no 404 by default — verify).

## Storefront behaviour

- Pagination preserves the filter: `/blog/category/news?page=2`.
- Sidebar entries highlight the currently active category/tag (CSS class set by the module — verify exact class).
- Article query is filtered server-side; URL is canonical and indexable.

## JavaScript behaviour

- Same as [[blog-list]]: `.js-sidebar-toggler`, `.js-loader-articles`, lazyload.
- No client-side filter switching by default — changing category/tag is a normal link click.

## Customisations available to the merchant

- Categories live under [[marketing-blog-category]]; their slug determines the URL segment.
- Tags live under [[marketing-blog-tags]].
- A category/tag with zero active articles still renders — its slug is reachable as long as the term exists.
- To hide a category from the public sidebar without deleting it, the merchant typically disables every article inside it.

## Theme variations

- Identical to [[blog-list]] — no theme ships a different filter UI.
- Some themes (verify) expand the sidebar's active category branch automatically.

## Known issues / by-design vs bug

- Empty filter pages still return `200` (by design — keeps SEO-discovered URLs alive).
- Misspelled `{filter}` segment (anything not `category` or `tag`) returns `404` from the application framework's route constraint, not from the controller.

## Related

- [[blog-list]]
- [[storefront-blog-article]]
- [[marketing-blog-category]]
- [[marketing-blog-tags]]
- [[storefront-architecture]]
- [[storefront-known-issues]]

## Open questions

- Confirm whether an unknown `{slug}` 404s or just renders empty.
- Confirm the active-state CSS class for the current category/tag in the sidebar.
- Confirm controller method (the request handler) on latest builds.
