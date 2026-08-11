---
type: entity
aliases: ["Blog Tag", "Blog tag", "Article tag", "Tag", "Blog label", "Таг", "Етикет на статия", "Блог етикет", "Тагове на блог"]
tags: [blog, marketing, content, taxonomy, entity]
created: 2026-05-21
updated: 2026-05-26
source_count: 3
---
# Blog Tag

## Identity

A **Blog Tag** is a free-form, flat label that the merchant attaches to a [[blog-article|Blog Article]] for **cross-categorisation, discovery, and filtering**. Where every Article must belong to **exactly one** [[blog-category|Blog Category]] (the required hierarchical parent — "News", "How-to guides"), Tags cut sideways across that hierarchy: an Article in the *How-to* category might simultaneously carry `summer-2026`, `outdoor`, `beginner`, and `under-100`. Tags drive (a) **storefront discovery** via per-tag URLs at `/blog/tag/<slug>` that list every Article carrying that tag regardless of Category; (b) **cross-Category browsing**; (c) **SEO long-tail keywords** — each tag page is its own indexable URL; and (d) **related-content modules** on Article pages ("More articles tagged …"). Tags are managed centrally from [[marketing-blog-tags]] (Sidebar → Marketing → Blog → Tags).

A Blog Tag is intentionally **distinct from a [[blog-category|Blog Category]]**: one Article has many Tags but exactly one Category. Categories form the navigation hierarchy and carry their own settings (comment policy, cover image, SEO meta); Tags are a flat, lightweight discovery layer with only a `name` + auto-derived `url_handle`. A Blog Tag is also **distinct from a Product Tag** — different storefront namespace (`/blog/tag/<slug>` vs the product-tag filter on category pages) and different cap rules. A tag named `summer` on a Blog Article is unrelated to a tag named `summer` on a product.

## Aliases

- **Blog Tag** / **Blog tag** — canonical merchant-facing term in the sidebar ("Marketing → Blog → Tags") and on [[marketing-blog-tags]].
- **Article tag** — admin breadcrumb form, emphasising the M2M attachment to Articles.
- **Tag** — short form in the Article editor's Tags multi-select. **Blog label** — informal phrasing.
- **Таг** / **Етикет на статия** / **Блог етикет** / **Тагове на блог** — Bulgarian terms used across Marketing → Blog.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (`tag`) | Required free text, 2 ≤ length ≤ 191 chars, **unique** across the store's blog tags | The displayed and customer-readable label. Validation errors: *"Tag name is required"* / *"Tag name is too long"* / *"Tag name is too short"* / *"Tag name already exists"*. **Stored lowercase** — `Summer-2026`, `summer-2026`, and `SUMMER-2026` all resolve to one tag stored as `summer-2026`. |
| **URL handle** (`url_handle`) | n/a — auto-derived from the tag name | Not exposed in the create / edit modal; computed automatically via the `UrlHandle` trait. Drives the storefront URL `/blog/tag/<url_handle>`. |
| **Articles count** | n/a — derived | Cached count of Articles attached to this tag, shown as a clickable "Articles (N)" button in the list. Clicking jumps to [[marketing-blog-articles]] pre-filtered by this tag (`filters[tags]=<id>`). The button is disabled when N = 0. |
| **Created at** / **Updated at** | n/a — auto | Standard timestamps. Available in the list view via column sorting. |
| **Per-language naming** | Optional translations on multilang stores | Tag names + auto-derived slugs can be translated per-locale so customers browsing in BG see Bulgarian tag names, customers browsing in EN see English. See [[multi-language]]. |
| **M2M attachment to Articles** | Editable on the [[marketing-blog-articles]] Article editor | Tags are NOT attached on this management screen — the merchant attaches tags to Articles inside the Article editor's Tags multi-select, where new tags are also auto-created on first use. |

A Blog Tag deliberately has **no parent_id, no description, no SEO meta, no per-tag image, no `active` flag, and no sort_order** — far lighter than [[blog-category|Blog Categories]] (which carry SEO + cover image + comment policy). The storefront tag page is always visible; an empty tag (all Articles untagged or deleted) returns 404 or redirects to `/blog/`.

**Renames do NOT auto-create 301 redirects.** Unlike [[blog-article|Articles]] and [[blog-category|Categories]] (which auto-redirect on slug change), renaming a Tag changes the storefront URL with no fallback — bookmarks to the old `/blog/tag/<old-slug>` break. Add a manual redirect via [[marketing-seo-301-redirects]] if SEO continuity matters.

**Caps** — a per-Article cap of **100 tags** and a **191-char-per-tag** length cap are enforced on every save path (UI, auto-create-on-save, programmatic). Failure messages: *"Maximum %1$s"* and *"%1$s — max length %2$s"*.

**Wildcard hygiene:** `%` and `_` are silently stripped from names with no warning — a pasted `[tag1, %, tag2]` saves `tag1` and `tag2` only.

**No webhook event** — there is no `tag.created` / `tag.updated` / `tag.deleted` event; subscribers cannot listen for blog-tag changes.

**Not in the sitemap.** The sitemap config explicitly omits blog tag URLs (the `blog_tags` entry is commented out), so `/blog/tag/<slug>` is reachable only via internal links from articles and storefront modules. A merchant who wants tag pages to rank must build inbound links manually.

**Granular permission gating** — tag CRUD is gated by `marketing.blog_tags`, independent from `marketing.blog_articles`, `marketing.blog_categories`, and `marketing.blog_comments`. A role can write articles yet be blocked from creating tags (enforces a curated vocabulary).

**Bulk-delete** — `DELETE /admin/api/core/blog/tags` accepts `{ids: []}` and fails atomically if any ID is unknown (no partial deletes). **Update uses PATCH** — `PATCH /admin/api/core/blog/tags/{id}` with body `{tag: <new-name>}` (most other blog endpoints use POST for update; Tag is the exception).

## Where it appears

- [[marketing-blog-tags]] — the master management screen (Sidebar → Marketing → Blog → Tags): "+ Add tag" to create, click the Name to edit, per-row + bulk delete, search by name.
- [[marketing-blog-articles]] — the Article editor's Tags multi-select; **the most common place tags are created** (auto-create on first use when the merchant types a new name and saves).
- [[marketing-blog-comment]] — sibling moderation surface; comments live on Articles, NOT on tags.
- [[apps-blog-csv-import]] — the CSV importer does **NOT** map tags; merchants must tag Articles manually after import.
- The storefront tag page at `/blog/tag/<url_handle>` — lists all active Articles carrying the tag (paginated). Its own indexable URL — Google can rank it for the tag's slug.
- Storefront "More articles tagged …" modules on Article pages — surface other Articles sharing tags.

## Programmatic access

Blog Tags can be managed via **JSON-API v2** at [[api-tags]] — pre-create a vocabulary before bulk-importing Articles via [[api-posts]], rename centrally, or delete obsolete tags. A POST / PATCH runs the **same pipeline as the admin modal** (validation, uniqueness, lowercase normalisation, wildcard stripping, auto-derived `url_handle`), and the same **Key Attributes** caveats all apply — no webhook event, no 301 redirect on rename (add one via [[api-redirects]]), absent from the sitemap, atomic bulk-delete, PATCH-for-update, separate `marketing.blog_tags` permission. See [[json-api-v2]] for auth and the side-effects principle.

## Related

### Related entities

- [[blog-article]] — Articles are tagged via M2M; tags are stored lowercase and deduplicated case-insensitively at save time.
- [[blog-category]] — orthogonal hierarchy; one required Category per Article + many flat Tags.
- [[blog-comment]] — comments are on Articles, not tags.
- [[seo-redirect]] — unlike Article / Category URL changes, renaming or deleting a Blog Tag does **NOT** create a 301 redirect; inbound links to `/blog/tag/<old-slug>` silently break.
- [[seo-meta]] — Tags carry no per-tag SEO meta (no `meta_title`, no `meta_description`); the tag page uses generic defaults.

### Cross-cutting concepts

- [[seo-handling]] — URL handles + redirects; Tags follow a slimmer pattern than Articles / Categories (no auto-redirect on rename).
- [[multi-language]] — per-locale translation of tag names + slugs on multilang stores.

### Settings & feature pages

- [[marketing-blog-tags]] — primary admin screen.
- [[marketing-blog-category]] — sibling Category management screen.

## Open Questions

No outstanding questions — all items resolved or removed.
