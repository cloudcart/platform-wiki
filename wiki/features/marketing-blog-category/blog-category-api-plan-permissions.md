---
type: feature
nav_path: "Marketing → Blog → Category → API, plan & permissions"
route_name: blog-categories
route_path: /admin/marketing-new/blog/category
aliases: ["Blog category API", "Blog category plan gate", "Blog category permission", "marketing.blog_categories", "blog_categories plan feature", "Blog category webhook", "API за блог категории"]
tags: [marketing, blog, content, categories, api, plan-gates, permissions]
plan_gates: ["blog_categories"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-category]]. See the hub for the other aspects (list & modal, comment policy, lifecycle, SEO).

# Blog Categories — API, plan gating & permissions

## Purpose

This aspect covers the programmatic and access-control surface of blog categories: managing them via **JSON-API v2**, the **`blog_categories` plan-feature** cap, the granular **`marketing.blog_categories`** staff permission, and the cache / webhook side effects. These are the rules a developer integrating an external CMS, or an admin configuring staff roles, needs.

## Where to find it

Admin UI: Sidebar → **Marketing** → **Blog** → **Category**. Programmatic: JSON-API v2 at [[api-blogs]]. Permissions: [[settings-staff]]. Plan limits: the per-feature upsell at [[plan-features]].

## What the merchant can do here

- Manage categories programmatically (create / read / update / delete) via [[api-blogs]].
- Grant or withhold blog-category management per staff role via `marketing.blog_categories`.
- Extend the per-plan category cap via a feature pack ([[plan-vs-feature-pack]]).

## Settings & fields

There are no UI fields specific to this aspect. The relevant configuration lives in:

- The **plan-feature** `blog_categories` (Numeric + Access) — defined in the platform code.
- The **staff permission** `marketing.blog_categories` — assigned per role on [[settings-staff]].
- The **JSON-API v2 payload** for the `blogs` resource — see [[api-blogs]] for the full field shape; it mirrors the modal fields (`name`, `comments`, `url_handle`, `seo_title`, `seo_description`, `image`).

## Business rules

### Programmatic access (JSON-API v2)

Blog Categories can be managed via **JSON-API v2** at [[api-blogs]] (resource named `blogs`; the underlying entity is the Blog Category). Use this resource to mirror a content taxonomy from an external CMS, pre-create categories before bulk-importing articles via [[api-posts]], or maintain SEO metadata.

**Same side effects apply.** A POST / PATCH runs the same pipeline as the admin modal: auto-slug + uniqueness, **301-redirect auto-creation** on `url_handle` rename (via [[marketing-seo-301-redirects]]), SEO fallback at save time (blank `seo_title` / `seo_description` populated with the category name BEFORE persisting — see [[blog-category-seo]]), the `blog_categories` plan-feature cap, and the storefront blog-list cache flush.

**API-specific behaviours worth knowing:**

- **Delete is NOT blocked** by attached Articles — the FK uses `ON DELETE SET NULL`. Articles survive orphaned (`blog_id = NULL`) and fail the "Blog is required" validation on next save. Re-assign before deleting — see [[blog-category-lifecycle]].
- **No webhook event** for Blog Category CRUD — integrations must poll.
- **Comment policy** (`comments` = `no` / `moderator` / `automatic`) is part of the API payload and drives every Article inside this Category at submission time — see [[blog-category-comment-policy]].
- **Per-area permission** — gated by `marketing.blog_categories`, separate from articles / tags / comments.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

### Permission

Category management requires the granular **`marketing.blog_categories`** permission on the admin's role — independent from `marketing.blog_articles`, `marketing.blog_comments`, and `marketing.blog_tags`. A role can be allowed to manage articles + comments while still being blocked from creating / deleting categories. See [[settings-staff]].

### Cache + webhooks

Editing a category flushes the storefront's blog-list cache. Unlike product categories, blog categories do **NOT** fire webhook events on changes — they don't appear in the [[settings-hooks]] event list, so integrations must poll via [[api-blogs]].

### Plan-tier limit on category count

Category creation is mapped to the `blog_categories` plan-feature limit. On lower-tier plans, the merchant hits the plan cap before any business-logic cap. Save fails with the platform's standard plan-limit error. (The separate per-category 500-article cap is on [[blog-category-lifecycle]].)

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `blog_categories` | Numeric + Access | Per-plan blog-category count cap (counted against the Blog entity). Lower plans cannot access the `blog/category` route at all. Hitting the cap throws the standard plan-limit error on the create modal. Extendable via feature pack. |

When over the category cap or below the access tier, the merchant is redirected to the per-feature upsell at [[plan-features]]. Numeric gates extend via packs ([[plan-vs-feature-pack]]); boolean / access gates require a plan upgrade.

## Related

- [[marketing-blog-category]] — hub.
- [[api-blogs]] — JSON-API v2 resource for blog categories.
- [[api-posts]] — JSON-API v2 resource for articles (pre-create categories before bulk-import).
- [[json-api-v2]] — auth, rate limits, side-effects principle.
- [[settings-staff]] — the `marketing.blog_categories` staff permission.
- [[settings-hooks]] — confirms blog categories fire no webhook events.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-feature gating model.
- [[blog-category-lifecycle]] — the per-category 500-article cap + delete/orphan behaviour.

## Open questions

No outstanding questions.
