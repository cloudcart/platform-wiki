---
type: feature
nav_path: "Marketing → Blog → Tags → API, plan & permissions"
route_name: blog-tags
route_path: /admin/marketing-new/blog/tags
aliases: ["Blog tag API", "Blog tag endpoints", "marketing.blog_tags", "Blog tag permission", "Blog tag plan gate", "Blog tag PATCH", "API за блог тагове", "Права за блог тагове"]
tags: [marketing, blog, tags, taxonomy, content, api, plan-gates, permissions]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---

> Part of [[marketing-blog-tags]]. See the hub for the other aspects (list & modal, lifecycle & sanitization, storefront & SEO).

# Blog Tags — API, plan & permissions

## Purpose

This aspect covers the non-UI access controls around blog tags: programmatic management via JSON-API v2, the full HTTP endpoint surface, the granular staff permission that gates tag CRUD, and the (absent) plan gating. Useful when an integration needs to pre-build a tag vocabulary before bulk-importing articles, or when a support ticket asks "why can't this staff member create tags".

## Where to find it

- **Admin**: Sidebar → **Marketing** → **Blog** → **Tags** (`/admin/marketing-new/blog/tags`).
- **Permissions**: the granular `marketing.blog_tags` toggle on the admin's role — see [[settings-staff]].
- **API**: JSON-API v2 tag resource — see [[api-tags]].

## What the merchant can do here

- Manage tags programmatically via **JSON-API v2** ([[api-tags]]) — pre-create a vocabulary before bulk-importing articles via [[api-posts]], rename a tag centrally, or delete obsolete tags.
- Restrict tag CRUD to specific staff roles via the `marketing.blog_tags` permission (independent from articles / categories / comments).

## Settings & fields

### Tag CRUD endpoint surface

| Action | Method + path |
|--------|---------------|
| List | `GET /admin/api/core/blog/tags` |
| Show | `GET /admin/api/core/blog/tags/{id}` |
| Create | `POST /admin/api/core/blog/tags` |
| Update | `PATCH /admin/api/core/blog/tags/{id}` (PATCH, not POST) |
| Delete | `DELETE /admin/api/core/blog/tags/{id}` |
| Bulk-delete | `DELETE /admin/api/core/blog/tags` (body: `{ids:[]}`) |

Bulk delete validates: `ids` required, array, each ID an integer, all IDs must exist. The error messages are *"The ids field is required"* / *"The ids field must be an array"* / *"The ids field must contain valid ids"* / *"The ids field must contain only integers"*.

### Permission

Tag CRUD requires the granular **`marketing.blog_tags`** permission on the admin's role — independent from `marketing.blog_articles`, `marketing.blog_categories`, and `marketing.blog_comments`. A role can be configured to write articles + manage categories but be blocked from creating / deleting tags (useful when the merchant wants a curated tag vocabulary). See [[settings-staff]].

## Business rules

### Same side effects as the admin modal

A POST / PATCH via [[api-tags]] runs the same pipeline as the admin modal: 2-191 char validation, uniqueness check, **lowercase normalisation** (`Summer-2026` → `summer-2026`), silent wildcard stripping (`%` and `_` removed), and auto-derived `url_handle`. The full normalisation rules are on [[blog-tags-lifecycle]].

### API-specific behaviours worth knowing

- **No webhook event** for tag CRUD — integrations must poll. See [[blog-tags-storefront-seo]].
- **No 301 redirect on rename** — external bookmarks to `/blog/tag/<old-slug>` break silently. Add a manual redirect via [[api-redirects]] if SEO continuity matters.
- **Tag pages are not in the auto-generated sitemap** — Google discovers them only via internal links.
- **Bulk-delete is atomic** — partial deletes rejected.
- **Update uses PATCH** (not POST — tags are the exception versus articles, which use POST).
- **Per-area permission** — gated by `marketing.blog_tags`, separate from articles / categories / comments.
- **Per-Article cap (100 tags) is NOT enforced here** — it's enforced Article-side via [[api-posts]], not on tag-record creation.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

### Plan gates

This feature is **NOT plan-gated** (verified against the platform code). Tags have no entry in the `mapping`, `restrict.creating`, or `restrict.access` arrays — every plan tier with access to [[marketing-blog-articles]] can also create, edit, and delete unlimited tags. The only access barrier is the `marketing.blog_tags` staff permission ([[settings-staff]]), not a plan-feature gate.

If tag management ever needs gating in future, the natural mappings would follow [[marketing-blog-articles]] / [[marketing-blog-category]] precedent and use either an access entry (`blog_tags` → `blog/tags`) or a numeric mapping; today neither is wired. See [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]] for the gate framework.

## Related

- [[marketing-blog-tags]] — hub.
- [[api-tags]] — JSON-API v2 tag resource.
- [[api-posts]] — JSON-API v2 article resource (where the 100-tag cap is enforced).
- [[api-redirects]] — manual 301 redirects for renamed / deleted tag URLs.
- [[json-api-v2]] — API authentication, rate limits, side-effects principle.
- [[settings-staff]] — `marketing.blog_tags` permission.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-gate framework (tags are not gated).

## Open questions

No outstanding questions.
