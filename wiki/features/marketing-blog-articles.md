---
type: feature
nav_path: "Marketing → Blog → Articles"
route_name: blog-articles-list
route_path: /admin/marketing-new/blog/articles
aliases: ["Blog articles", "Posts", "Blog posts", "Articles", "Статии", "Статии на блог", "Блог", "Публикации"]
tags: [marketing, blog, content, seo, articles]
plan_gates: ["blog_articles", "blog_categories"]
created: 2026-05-21
updated: 2026-06-10
source_count: 11
---
# Blog Articles

## Purpose

The **Blog Articles** screen is where the merchant writes and publishes the long-form content that lives at `/blog/` on the storefront. Articles are the SEO + content-marketing surface of the store: write a post about *"5 ways to style our new collection"*, attach it to a blog category and tags, schedule publication, and the article appears on the storefront under `/article/<slug>` (and in the blog listing at `/blog/`).

Articles drive **organic traffic** (Google indexes the slug + content + SEO meta), **engagement** (visitors leave comments per article — see [[marketing-blog-comment]]), and **funnel conversion** (article body can link to products / categories / discount codes). They are distinct from the static *"About us / Privacy / Terms"* pages — those live elsewhere in CMS / Pages.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Articles**.

The base route is `/admin/marketing-new/blog/articles`. The header icon is the typewriter icon.

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages. Drill into the one that matches the question rather than reading every page.

- [[blog-articles-list]] — the list screen: header actions, table columns, filters, bulk publish / unpublish / delete, pending-comments banner.
- [[blog-articles-editor]] — the Add / Edit two-column form: fields, slug auto-sync, inline-image async mirroring, in-place category create, SubmitChanges footer.
- [[blog-articles-csv-import]] — the 3-step **Add via CSV** wizard (gated by the `blog_csv_import` app): upload + settings, field mapping, progress confirmation.
- [[blog-articles-rules]] — server-side validation rules (the platform code), 500-articles-per-category cap, tag caps, granular blog-permission keys, plan-feature caps, delete cascades.
- [[blog-articles-storefront-visibility]] — `active` toggle, `publish_date` scheduled-publish scope, comment routing inherited from the parent category, storefront URLs, 5-per-minute comment throttle, third-party comment-platform replacement.
- [[blog-articles-api]] — JSON-API v2 surface ([[api-posts]] / [[api-authors]]), the same side effects as the UI, the API-specific behaviours (scheduled publishing, no `active='yes'` default override).

### Sub-screens (deep links)

| Label | Route name | Route path |
|-------|------------|------------|
| List | `blog-articles-list` | `/admin/marketing-new/blog/articles` |
| Add | `blog-articles-add` | `/admin/marketing-new/blog/articles/add` |
| Edit | `blog-articles-edit` | `/admin/marketing-new/blog/articles/edit/:id` |

## What the merchant can do here

The hub catalogues the surface only. Every detail lives on the relevant sub-page.

- Browse, search, filter, bulk-edit, and inline publish-toggle articles — see [[blog-articles-list]].
- Create or edit a single article with title / rich-text body / cover image / author / category / tags / SEO meta — see [[blog-articles-editor]].
- Bulk-import articles from a CSV file — see [[blog-articles-csv-import]].
- Manage articles programmatically via [[api-posts]] — see [[blog-articles-api]].

## Settings & fields

Full field catalogue lives on the relevant sub-page. Highlights that apply cluster-wide:

- **Required fields**: `name` (3 ≤ length ≤ 191), `author_id`, `blog_id`. See [[blog-articles-rules]] for the full the platform code ruleset and verbatim error strings.
- **URL handle** is auto-derived from the title on first save then locks; renaming creates a 301 redirect from the old slug via [[marketing-seo-301-redirects]]. See [[blog-articles-editor]] + [[blog-articles-rules]].
- **Plan-feature keys**: `blog_articles` (numeric + access — article count cap; lower plans cannot access the route at all) and `blog_categories` (numeric + access — required parent). Extendable via feature pack — see [[plan-features]] + [[plan-vs-feature-pack]].
- **Permission keys** — four independent keys gate the area: `marketing.blog_articles`, `marketing.blog_categories`, `marketing.blog_comments`, `marketing.blog_tags`. See [[blog-articles-rules]] + [[settings-staff]].

## Business rules

The full catalogue lives on the sub-pages. Highlights that apply cluster-wide:

- **500 articles per blog category.** Save fails with *"The blog can not have more than 500"* once the cap is hit; the merchant must split the category. See [[blog-articles-rules]].
- **Plan-feature cap fires before the per-category cap.** Hitting the `blog_articles` numeric cap throws the platform's standard plan-limit error before the 500-cap check.
- **Tag caps.** Up to 100 tags per article, each ≤ 191 chars (*"Maximum 100"* / *"<tag-name> maximum length is 191"*). `%` and `_` are silently filtered. Editing an article replaces the full tag list. See [[blog-articles-rules]].
- **Title-driven slug locks after first save.** Manually editing the slug later auto-creates a 301 redirect via [[marketing-seo-301-redirects]].
- **`active='yes'` from the editor; `publish_date` from the API.** The modern [[blog-articles-editor]] always submits `active='yes'` on Save and does NOT expose `publish_date`. Scheduled publishing is enforced by a passive SQL scope that hides articles until `publish_date <= now` — set only via [[blog-articles-api]] or the legacy editor. See [[blog-articles-storefront-visibility]].
- **Comment behaviour is inherited from the parent category** (not configurable per-article). To change comment behaviour for one article, the merchant moves it to a differently-configured [[marketing-blog-category]].
- **Storefront comment throttle**: 5 submissions per 1 minute per IP via a submission throttle on `/blog/article/create-comment/{article_id}`. Exceeding returns HTTP 429 + *"Too many requests"*. See [[blog-articles-storefront-visibility]].
- **Delete cascades wipe comments**; deleting the parent category orphans the article (FK is `ON DELETE SET NULL`). See [[blog-articles-rules]].
- **Third-party comment apps replace the native thread.** When [[apps-disqus-comments]] or [[apps-facebook-comments]] is installed, the storefront swaps the native form + thread for the third-party module; CloudCart's native comments remain in the DB.
- **Inline images in editor content are mirrored asynchronously** via the `text_image_from_url` queue task; the featured cover image (`image` field) is uploaded synchronously. See [[blog-articles-editor]] + [[background-queue-inventory]].

## Related

- [[marketing-blog-category]] — required parent; `blog_id` is a required FK.
- [[marketing-blog-tags]] — multi-select; tags auto-create on assignment.
- [[marketing-blog-comment]] — comment thread per article; moderation governed by the parent category.
- [[marketing]] — parent hub.
- [[marketing-seo-meta]] — per-article SEO title + description.
- [[marketing-seo-301-redirects]] — auto-created when the URL handle changes.
- [[apps-blog-csv-import]] — bulk-import articles from a CSV.
- [[apps-blog-csv-import-progress]] — progress-tracking screen for an in-flight import.
- [[apps-disqus-comments]] — third-party commenting replacement.
- [[apps-facebook-comments]] — Facebook Comments Plugin alternative.
- [[apps-seo-spinner]] — auto-generate SEO meta for articles.
- [[settings-staff]] — list of admins eligible to be article authors; permission matrix.
- [[blog-article]] — entity page.
- [[blog-category]] — entity page.
- [[blog-tag]] — entity page.
- [[api-posts]] — JSON-API v2 resource for articles.
- [[api-authors]] — read-only author lookup.
- [[json-api-v2]] — auth, rate limits, side-effects principle.
- [[plan-features]] — per-tier counts for `blog_articles` and `blog_categories`.
- [[plan-vs-feature-pack]] — feature-pack extension model.
- [[plan-gates]] — overall plan-gate catalogue.
- [[background-queue-inventory]] — catalogue of all background processes; covers the async inline-image mirroring + blog-CSV import job.

## Open questions

No outstanding questions for the hub. Aspect-specific open questions live on [[blog-articles-csv-import]] (importer field enum) + [[blog-articles-storefront-visibility]] (Cloudflare cache flush) + [[blog-articles-api]] (bulk update-status endpoint).
