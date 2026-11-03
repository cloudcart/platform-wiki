---
type: feature
nav_path: "Design → Modules → Blog → Blog"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Blog module", "Blog listing module", "blog.blog", "Storefront blog module", "Модул Блог", "Блог модул"]
tags: [design, modules, blog, content, listing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Blog listing (`blog`)

> Part of [[design-modules-blog]]. See the category page for the other blog modules.

## Purpose

The **Blog** module (`blog.blog`, instance name `blog`) drives the storefront's main blog index — the page customers see at `/blog`, plus the per-category and per-tag filtered variants `/blog/category/{slug}` and `/blog/tag/{slug}`. It controls **how many articles per page** the listing paginates by and decides what category-filter UI surrounds the article list. The article CONTENT itself (titles, bodies, hero images, tags, status) is edited in [[marketing-blog-articles]] — this module only configures the LISTING.

Most themes also re-use the same module type for a homepage "Featured articles" row by registering a second instance named `blogHome` — that homepage variant is documented in [[design-module-blog-home]].

## Where to find it

Sidebar → **Design** → **Modules** → **Blogs, articles and comments** tab → click the **Blog** card.

The form opens in a side panel with two fields: enable / disable + per-page count.

## What the merchant can do here

- **Set how many articles per page** the storefront blog listing paginates by.
- **Disable** the module — when off, the blog landing page renders an empty listing (the surrounding header / footer still appear; only the article list is suppressed).
- **Save** to persist; storefront cache regenerates and the new setting is live on the next request.
- **Reset** to revert to the theme's shipped default (10 per page).
- **Cancel** to close without saving.

What the merchant CANNOT do here:

- Filter the listing to a specific blog category — the listing always shows EVERY published article. Per-category navigation is configured per-link in [[design-navigation]].
- Pick a sort order — articles are always sorted by ID descending (newest first). For a sorted / curated row, use the page-builder Recent Articles block — see [[design-module-blog-recent-articles]].
- Change the image size, the read-more link wording, the snippet length, or the layout — those are theme-controlled.

## Settings & fields

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | on / off | `bool` (coerced via `isset` on save) | Master on/off; when off the blog landing page returns an empty list |
| `per_page` | int | `10` | 2-50 | `int:2,50` | Articles per page on `/blog` and the filtered variants |

That is the entire merchant-facing form for this module — there are no theme / layout / image-size controls.

### Validation behaviour

- `per_page` below 2 or above 50 triggers a field-level validation error.
- A non-integer value (e.g., empty string, decimal) is rejected by the `int:` rule.
- Unknown fields submitted with the form are silently dropped (only `enabled` and `per_page` are stored).

## Theme dependencies

Every theme that ships a blog feature also ships a `blog` module instance pointed at the storefront blog landing page. Themes WITHOUT blog support (rare) skip the instance entirely and the `/blog` route is unreachable.

The display name shown on the card (**"Blog"**) comes from the active theme's `theme.json` `name` block, with translations per locale (e.g., `bg` = "Блог", `en` = "Blog").

## Business rules

### `per_page` is the only dial that affects the listing

Article ordering (always newest first by ID), the category-sidebar layout, image sizes, the article-card markup — all theme-controlled. The merchant can ONLY change pagination size from here.

### Filtered URLs share the same module instance

The same `blog` instance powers:
- `/blog` — every published article, newest first.
- `/blog/category/{slug}` — articles in one blog category (resolved from [[marketing-blog-category]]).
- `/blog/tag/{slug}` — articles tagged with one tag (resolved from [[marketing-blog-tags]]).

The module reads the active filter from the URL and narrows the listing automatically; `per_page` applies the same way on every variant.

### Pagination is automatic

When the article count exceeds `per_page`, pagination links render at the bottom of the listing — no merchant configuration required.

### Disabling the module leaves an empty page

The route still resolves but renders a notification — the theme typically shows *"sf.module.blog.err.blog_is_disabled"* ("Blog is disabled") in place of the article list. Headers and footers still render. To fully hide the blog from the storefront, the merchant should also remove the Blog link from [[design-navigation]].

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|---|---|---|---|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes panel | None | — |

### Cache invalidation

Save and Reset both bump the per-site modules cache key. The storefront picks up the new `per_page` on the next request — no manual cache-clear required. Adding or publishing an article in [[marketing-blog-articles]] surfaces in the listing immediately on the next storefront load (the article list is read live, not cached).

### Settings precedence

A saved value always wins over the theme's shipped default. Reset discards the saved value and falls back to the default (10 per page).

### Renamed categories / tags redirect automatically

If the merchant renames a blog category or tag, the storefront auto-redirects the old `/blog/category/{slug}` or `/blog/tag/{slug}` URL to the new one. An unknown slug returns a 404. Each listing card also shows that article's comment count.

### SEO on filtered listings

When a category filter is active, the listing uses the SEO title / description set on that blog category in [[marketing-blog-category]]; otherwise it falls back to the global blog SEO strings.

### Plan gating

None — the Blog module is available on every plan that has blog enabled. If a merchant sees no Blog tab at all, the cause is the plan or the active theme not shipping blog templates, not this module.

## Tips for merchants

- Keep `per_page` between 6 and 20 for a good balance between page weight and pagination clicks.
- For per-category curation on the homepage, use the page-builder Recent Articles block ([[design-module-blog-recent-articles]]) — this module itself does NOT accept a category filter from the admin.
- If the merchant wants the blog hidden, disabling the module is faster than unpublishing every article — but remember to ALSO remove the Blog link from the navigation menu.
- Article ordering is fixed (newest first). If the merchant needs a "Featured" or "Editor's pick" article at the top, the simplest workaround is to bump that article's `created_at` or use the page-builder block on a dedicated landing page.

## Related

- [[design-modules-blog]] — hub.
- [[design-module-blog-home]] — sibling `blogHome` instance for the homepage row.
- [[design-module-blog-recent-articles]] — sibling "Latest articles" row.
- [[marketing-blog-articles]] — where the articles themselves are edited.
- [[marketing-blog-category]] — blog categories surfaced as `/blog/category/{slug}`.
- [[marketing-blog-tags]] — blog tags surfaced as `/blog/tag/{slug}`.
- [[design-navigation]] — where the Blog menu link is added / removed.
- [[design-themes]] — theme picker; determines whether the `blog` instance ships.

## Open questions

- 📡 **Per-language `per_page`.** With the `multylang` app, the module reads the merchant's locale setting on save — verify whether `per_page` is single-value or stored per-language (verify).
