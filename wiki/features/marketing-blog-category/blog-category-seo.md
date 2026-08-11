---
type: feature
nav_path: "Marketing → Blog → Category → SEO, URL handle & sitemap"
route_name: blog-categories
route_path: /admin/marketing-new/blog/category
aliases: ["Blog category SEO", "Blog category URL handle", "Blog category slug", "Blog category cover image", "Blog category sitemap", "Blog category 301 redirect", "SEO на блог категория"]
tags: [marketing, blog, content, categories, seo]
plan_gates: ["blog_categories"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-category]]. See the hub for the other aspects (list & modal, comment policy, lifecycle, API/plan/permissions).

# Blog Categories — SEO, URL handle & sitemap

## Purpose

This aspect covers everything that controls how a blog category appears to search engines and how its storefront URL is built: the **SEO title / description** fields and their save-time fallback, the **URL handle** (auto-slug on create, locked on edit, 301 redirect on rename), the **cover image** rendering, and **sitemap inclusion** (only categories with at least one active article). These are the rules behind "why does my blog category title show the category name instead of blank" and "will Google find this category".

## Where to find it

Sidebar → **Marketing** → **Blog** → **Category** → open a category's modal → **Advanced settings** card (default-expanded). The modal mechanics are on [[blog-category-list]].

## What the merchant can do here

- Set a custom **SEO title** and **SEO description** for the category page.
- Override the **URL handle** (on create; locked after the category exists).
- Upload / remove the **cover image** used as the category hero + list thumbnail + social OG image.

## Settings & fields

### SEO + URL fields

| Field | Validation | Notes |
|-------|------------|-------|
| **URL handle** (`url_handle`) | Auto-derived from title; overrideable on first create. Locked on edit. | Storefront URL: `/blog/category/<url_handle>`. Shown with a `/category/` prefix preview in the modal. |
| **SEO title** (`seo_title`) | String, max 191. | Maps to the page title on `/blog/category/<slug>`. If empty, falls back to the category name (at save time — see below). |
| **SEO description** (`seo_description`) | String, max 191. | Maps to the meta description. Defaults to the category name if empty (at save time). |
| **Cover image** (`image`) | Optional file upload. | Thumbnail shown at `150x150` in the list. Removable via a separate action. |

## Business rules

### SEO fallback applied at SAVE time (not just render time)

The merchant can leave **SEO title** and **SEO description** empty in the modal. When the modal submits, the front-end **auto-fills** both fields with the category name (`name || ''`) BEFORE posting to the API. So an "empty" SEO field is stored as the category name, not as NULL. This protects category pages from rendering a blank `<title>` / `<meta description>`, but means the merchant can't truly "leave SEO empty" — they get a name-based default whether they want it or not. To override, they have to type a different SEO value. (This is also why the Zod `seo_title` / `seo_description` "required" checks effectively never fire — see [[blog-category-list]].)

### URL handle: auto-slug on create, locked on edit

When the merchant types the title in a NEW category modal, the URL handle is auto-derived from the title. Once the category exists (the edit modal), the merchant must edit the URL handle field manually to change it. This protects pre-existing slugs from accidental rename.

Renaming the URL handle on an existing category creates a **301 redirect** from the old `/blog/category/<old-slug>` to the new one, preserving inbound links and Google's index. See [[marketing-seo-301-redirects]].

### Cover image rendering

The category's cover image is used as:

- The hero banner on `/blog/category/<slug>` storefront page.
- The thumbnail next to the category title in the admin list (`150x150`).
- Optionally the OG image for the category page's social share preview.

The image has a dedicated delete endpoint (`/admin/api/core/blog/categories/{id}/delete-image`, only on existing categories); removing it inside the modal clears the list-row thumbnail live — see [[blog-category-list]].

### Sitemap inclusion: only categories with active articles

The store's auto-generated sitemap (see [[marketing-seo-meta]]) includes the category page `/blog/category/<slug>` ONLY when the category has at least one article where `active='yes'` (the `activeItems` relation is non-empty). Empty categories — including newly-created ones with no articles yet — are NOT submitted to search engines via the sitemap. The category page itself still renders on the storefront with "no articles yet", but Google won't discover it via sitemap until the first article is published. So the merchant should publish at least one article shortly after creating a category, or the SEO presence will lag. Verified in the platform code (the `'has' => ['activeItems']` constraint).

## Related

- [[marketing-blog-category]] — hub.
- [[blog-category-list]] — the Advanced settings card hosting these fields + the image card.
- [[marketing-seo-meta]] — per-category SEO title + description, and the sitemap generator.
- [[marketing-seo-301-redirects]] — auto-created when the URL handle changes.
- [[blog-category-lifecycle]] — storefront URL + visibility (category has no active flag).

## Open questions

No outstanding questions.
