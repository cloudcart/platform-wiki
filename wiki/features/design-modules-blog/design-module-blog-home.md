---
type: feature
nav_path: "Design → Modules → Blog → Blog - homepage"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Blog Home module", "blogHome", "blogHome module", "Recent articles home", "Latest News - Home", "Блог - начална страница", "Последни новини на индекса"]
tags: [design, modules, blog, homepage]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Blog homepage row (`blogHome`, `recentArticlesHome`)

> Part of [[design-modules-blog]]. See the category page for the other blog modules.

## Purpose

The **Blog homepage row** is a SECOND instance of an existing blog module type that themes register for the storefront's home page. Two patterns exist depending on the theme:

| Instance | Underlying type | Behaviour |
|---|---|---|
| `blogHome` | `blog.blog` | A scaled-down copy of the full blog listing, rendered as a homepage row (typically the "Latest articles" / "From the blog" block under the hero). |
| `recentArticlesHome` | `blog.recentArticles` | A homepage-scoped instance of the Latest Articles row (when the theme wants the homepage row separate from a sidebar instance). |

Both serve the same merchant intent — show a short row of recent articles on the home page — but with different underlying module types. The settings form is the form of the underlying type (see [[design-module-blog-listing]] for `blog.blog`; [[design-module-blog-recent-articles]] for `blog.recentArticles`); only the instance name and the storefront placement differ from the primary instance.

## Where to find it

Sidebar → **Design** → **Modules** → **Blogs, articles and comments** tab → click the **Blog - homepage** card (or **Latest News - Home**, depending on the active theme's display name).

If the active theme does NOT ship a `blogHome` / `recentArticlesHome` instance, this card does not appear at all — the homepage row simply doesn't exist on that theme.

## What the merchant can do here

Same actions as the underlying module type:

- For `blogHome` (using `blog.blog`) — set `per_page` (2-50). On the homepage row, this caps how many articles the row tries to render before the theme's own per-row CSS grid wraps or truncates.
- For `recentArticlesHome` (using `blog.recentArticles`) — set `count` (2-10).
- Toggle the master `enabled` switch to hide the homepage row entirely.
- Save / Reset / Cancel — identical buttons + cache invalidation pipeline as the parent type.

What the merchant CANNOT do here:

- Choose a different storefront slot — the `blogHome` / `recentArticlesHome` instance is hard-bound by the theme to the homepage's blog row slot.
- Filter by category or tag — the underlying module types don't accept those filters from the admin.
- Merge this row with the type's other instance — the two are independent (separate saved records keyed by instance name) but share the form layout and validation.

## Settings & fields

### When the instance map is `blog.blog` (typical `blogHome`)

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | on / off | `bool` | Hides the homepage row when off |
| `per_page` | int | `10` | 2-50 | `int:2,50` | How many articles the homepage row may render (theme CSS may then cap to N visible) |

### When the instance map is `blog.recentArticles` (typical `recentArticlesHome`)

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | on / off | `bool` | Hides the homepage row when off |
| `count` | int | `5` | 2-10 | `int:2,10` | Number of latest articles to fetch |

The form is identical to the primary instance's — the only difference is the instance name in the URL and where the values are stored.

## Theme dependencies

Highly theme-specific:

- **Zora-new** ships both `recentArticles` (sidebar / global) AND `recentArticlesHome` (homepage row) as separate `blog.recentArticles` instances. (verify)
- **knowledge-tmarket** ships `blogHome` as a `blog.blog` instance AND a separate `blog` instance for the landing page.
- **Many themes** ship only one instance (`recentArticles`) that the theme renders BOTH on the homepage and in sidebars.
- Themes without any homepage blog row skip the instance entirely.

The merchant should check the theme's documentation or preview the storefront to confirm where this module actually appears — the admin card title alone is the only hint.

## Business rules

### Settings are independent from the primary instance

`blogHome` and `blog` are two separate saved records. Setting `blogHome.per_page = 4` does NOT change `blog.per_page`. The same applies for `recentArticlesHome` vs `recentArticles` — each has its own saved settings.

### Switching themes can orphan the instance

If the merchant switches from a theme that ships `blogHome` to one that does not, the saved `blogHome` settings are retained but stop being editable (no card appears). Switching back re-exposes the card with the previously saved values intact.

### The article source is the SAME pool

Both instances pull from the same published-articles pool — there is no per-instance filter. To curate articles for the homepage specifically, the merchant should use the page-builder Recent Articles block on a Dynamic homepage instead (see [[design-module-blog-recent-articles]] for the page-builder variant's category filter + sort).

### Display name comes from the theme

The card label (**"Blog - homepage"** / **"Latest News - Home"** / **"Recent articles homepage"** / etc.) is set by the active theme. Different themes call the same homepage-scoped instance different things — all are the same module pattern.

### Save / Reset / Cancel

Identical to the parent module type:

| Button | Action | Confirmation | Success message |
|---|---|---|---|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes panel | None | — |

After Save or Reset the storefront cache is bumped, so the row reflects the new settings on the next storefront request.

### Why a second instance exists

The module framework keys saved settings by instance name, not by module type. By registering a second instance of the same type, the theme reserves a separate settings record the merchant can configure independently. The same pattern recurs across CloudCart modules (`homeText1` / `homeText2`, `bannersHomePage` / `bannersTextPage`, `showcaseBrands1` / `showcaseBrands2`) — `blogHome` is the blog flavour of it. At render time the only practical difference between `blogHome` and `blog` is the `per_page` / `count` value the merchant has set; the article query (newest first, published only) is otherwise identical.

## Tips for merchants

- Keep the homepage row tight — 3 to 6 articles is plenty. Long lists on the homepage hurt above-the-fold weight.
- If the homepage row and a sidebar / footer row show the same articles in the same order, it's because both instances draw from the same recency pool — there's no de-dup across instances.
- To run a "Featured" row separately from "Latest", use a Dynamic page with the page-builder Recent Articles block (with its `category_id` filter) — the only place per-category curation is exposed.

## Related

- [[design-modules-blog]] — hub.
- [[design-module-blog-listing]] — primary `blog` instance (`blog.blog`); identical form fields.
- [[design-module-blog-recent-articles]] — primary Recent Articles row (`blog.recentArticles`) + page-builder block.
- [[marketing-blog-articles]] — where articles are authored.
- [[marketing-landing-pages]] — Dynamic page builder; alternative homepage when curated per-category needed.
- [[design-themes]] — theme picker; controls whether `blogHome` / `recentArticlesHome` ships.

## Open questions

- 📡 **Which themes ship which instance.** Verify per-theme: Zora-new (recentArticlesHome), knowledge-tmarket (blogHome), and the rest of the catalogue.
- 📡 **Homepage CSS truncation.** Themes may cap the homepage row to N visible cards even when `per_page` returns more — verify per-theme the visible count vs the queried count.
