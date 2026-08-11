---
type: feature
nav_path: "Marketing → Blog → Tags → Storefront & SEO"
route_name: blog-tags
route_path: /admin/marketing-new/blog/tags
aliases: ["Blog tag storefront URL", "Blog tag page", "/blog/tag/<slug>", "Blog tag SEO", "Blog tag sitemap", "Blog tag no redirect", "URL на таг на блог", "SEO на блог тагове"]
tags: [marketing, blog, tags, taxonomy, content, seo]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---

> Part of [[marketing-blog-tags]]. See the hub for the other aspects (list & modal, lifecycle & sanitization, API/plan/permissions).

# Blog Tags — Storefront & SEO

## Purpose

This aspect covers what a blog tag does on the customer-facing storefront and the SEO consequences of the tag system. Every tag becomes its own indexable page at `/blog/tag/<slug>` listing every active article carrying it, regardless of category. The key warnings here are about **silent SEO breakage**: tags produce no 301 redirects on rename/delete, are excluded from the sitemap, and fire no webhooks — so integrations and inbound links can break without any signal.

## Where to find it

The admin-side tag management is at Sidebar → **Marketing** → **Blog** → **Tags** (`/admin/marketing-new/blog/tags`). The storefront output appears at the public URL `/blog/tag/<slug>` (rendered by the storefront blog templates — see [[blog-filter]]) and inside the "More articles tagged …" related-content modules on article pages.

## What the merchant can do here

- Drive **storefront discovery** — every tag has its own URL at `/blog/tag/<slug>` showing every article carrying it, regardless of category.
- Enable **cross-category browsing** — visitors clicking "summer-2026" see articles from multiple categories in one place.
- Target **SEO long-tail keywords** — each tag page is its own indexable page with the tag's slug as the URL.
- Surface **related-content recommendations** on individual article pages (storefront "More articles tagged …" module).

## Settings & fields

There are no merchant-editable storefront/SEO settings on a blog tag. The only field that affects the storefront URL is the auto-derived `url_handle`:

| Field | Behaviour |
|-------|-----------|
| **URL handle** (`url_handle`) | Auto-derived from the tag name; produces `/blog/tag/<url_handle>`. Not editable in the modal. |
| Per-tag SEO title / description / image | **None** — unlike [[marketing-blog-category]], tags carry no SEO metadata fields. |

## Business rules

### Storefront URL: `/blog/tag/<slug>`

The frontend route `blog.view` matches `/blog/{filter}/{slug}` where `filter=tag`. The storefront renders all articles where `active='yes'` AND the tag is attached. The page is its own indexable URL — Google can rank it for the tag name as a keyword.

### NO 301 redirect on rename or delete

Unlike articles / categories (which auto-write 301s via the `UrlHandle` trait's history mechanism), blog tags do **NOT** register redirect history. Inbound links to `/blog/tag/<old-slug>` break silently after a rename, and the tag page returns 404 (or redirects to `/blog/`) after a delete. To preserve SEO continuity, the merchant has to add a manual redirect via [[marketing-seo-301-redirects]].

### NOT included in the auto-generated sitemap

Blog tags are NOT part of CloudCart's sitemap — the `blog_tags` entry is present in the sitemap config but commented out. Consequences:

- Google does NOT discover `/blog/tag/<slug>` URLs via the sitemap.
- They are only discoverable via internal links from articles + the "related articles" modules on storefront article pages.

This is intentional — tag pages can multiply quickly and produce thin SEO content (sometimes just one article per tag). The merchant who wants SEO-rich tag pages must build inbound links manually.

### Tag taxonomy NOT in webhooks

Unlike [[product]] or [[category]], the blog tag does NOT fire `tag.created` / `tag.updated` / `tag.deleted` webhooks (the [[settings-hooks]] event list has no entry for blog tags). Subscribers cannot listen for blog-tag CRUD — integrations must poll (see [[blog-tags-api-permissions]]).

## Related

- [[marketing-blog-tags]] — hub.
- [[blog-filter]] — storefront blog filter / tag page rendering.
- [[marketing-blog-category]] — has full SEO metadata fields (contrast: tags have none).
- [[marketing-seo-301-redirects]] — add a manual redirect to cover renamed / deleted tag URLs.
- [[settings-hooks]] — webhook event list (no blog-tag events).

## Open questions

No outstanding questions.
