---
type: feature
nav_path: "Marketing → Blog → Articles → Business rules"
route_name: blog-articles-list
route_path: /admin/marketing-new/blog/articles
aliases: ["Article validation", "Article business rules", "Tag caps", "500-per-category cap", "Plan caps for articles", "Granular blog permissions", "Article permissions"]
tags: [marketing, blog, articles, rules, validation, plan-gates, permissions]
plan_gates: ["blog_articles", "blog_categories"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-blog-articles]]. See the hub for the other aspects (list, editor, CSV import, storefront visibility, API).

# Blog Articles — business rules

## Purpose

This aspect catalogues every server-side rule that gates create / save / delete / bulk-publish for blog articles — the verbatim validation message strings, per-category cap, tag caps, granular permission keys, and plan-feature caps. It is the canonical reference for support tickets of the form *"why won't my article save"* / *"why does it say I've reached my limit"* / *"why can't my staff user see Comments"*.

## Where to find it

These rules apply globally on every save path:

- [[blog-articles-editor]] — the manual create / edit form.
- [[blog-articles-list]] — the inline Publish toggle + bulk-update-status.
- [[blog-articles-csv-import]] — every row created by the bulk importer.
- [[blog-articles-api]] — every POST / PATCH against [[api-posts]].

## What the merchant can do here

The merchant cannot configure these rules — they are platform invariants. This page is the canonical catalogue for support agents diagnosing save failures.

## Settings & fields

There are no merchant-facing settings here — it is a rules reference. The error-message strings and setting keys below are the verbatim text the merchant sees.

### Server-side validation rules

These rules are enforced on every create + update:

| Field | Rules | Wording on failure |
|---|---|---|
| `name` | **required**, min 3 chars, max 191 chars | *"Name is required"* / *"Name is too short"* / *"Name is too long"* |
| `content` | string (no length cap; very long body text is allowed) | *"Content must be a string"* |
| `seo_title` | string, max 191 | *"SEO title is too long"* |
| `seo_description` | string, max 191 chars. The [[marketing-seo-meta]] guidance lists 320 chars as the practical limit — the stricter 191 wins on save. | *"SEO description is too long"* |
| `author_id` | **required**, integer, must be an existing admin | *"Author is required"* / *"Author does not exist"* |
| `blog_id` | **required**, integer, must be an existing blog category | *"Blog is required"* / *"Blog does not exist"* |
| `tags` | array (optional; the tags themselves are auto-created — see Tag caps below) | *"Tags must be an array"* |
| `publish_date` | optional date | *"Publish date must be a date"* |
| `active` | `yes` / `no` | *"Active must be yes or no"* |

The minimum **3-character name** blocks a 1- or 2-character title placeholder (*"On"*, *"Hi"*) — the *"Name is too short"* error shows and the modal stays open.

### Bulk-publish endpoint validation

`POST /admin/api/core/blog/articles/update-status` accepts `{ids: [], status: yes|no}`. Validated as:

- `ids` — required, array, all IDs must be existing articles.
- `status` — required, exactly `yes` or `no`.

Mass-flips `active` in one operation — no per-row side-effects fire.

## Business rules

### 500-articles-per-category cap

When the merchant creates a NEW article, the platform counts existing articles in the chosen blog category. If the count is ≥ 500, save fails with *"The blog can not have more than 500"*. There is no global cap across the store — only the per-category cap. Work around it by splitting the category (create a sister category, move overflow articles by editing each one).

### Tags: auto-create + 100-tag-per-article + 191-char-per-tag cap

- Tag names are de-duplicated case-insensitively against the store's existing tags.
- **New tags are auto-created** when typed — no need to pre-create them in [[marketing-blog-tags]].
- **Up to 100 tags per article**. Exceeding the cap throws *"Maximum 100"*.
- **Each tag name ≤ 191 chars.** Exceeding throws *"<tag-name> maximum length is 191"*.
- Tags `%` and `_` are silently filtered.
- Editing an article replaces the full tag list — there's no "add one tag" action; the article's tags are always set to whatever the merchant submits.

### Plan-tier gating for article + category COUNT

Article and category creation are mapped to plan-feature limits in the platform's plan configuration:

| Plan-feature key | Shape | What it controls |
|---|---|---|
| `blog_articles` | Numeric + Access | Per-plan article count cap (counted against the Article model). Lower plans cannot access the `blog/article` route at all. Hitting the cap throws the platform's standard plan-limit error on save BEFORE the per-category 500-cap check. Extendable via feature pack. |
| `blog_categories` | Numeric + Access | Required parent — articles need an existing blog category, and category creation is also plan-capped. See [[marketing-blog-category]]. |

When over the article cap or below the access tier, the merchant is redirected to the per-feature upsell at [[plan-features]]. Numeric gates extend via packs (see [[plan-vs-feature-pack]]); boolean / access gates require a plan upgrade.

### Granular permission gating (4 independent keys)

The Marketing → Blog area splits into four independent permission keys checked per controller endpoint:

| Permission key | Gates |
|----------------|-------|
| `marketing.blog_categories` | All `/admin/api/core/blog/categories/*` endpoints. |
| `marketing.blog_articles` | All `/admin/api/core/blog/articles/*` endpoints (including bulk publish/unpublish). |
| `marketing.blog_comments` | All `/admin/api/core/blog/comments/*` endpoints (status change + delete). |
| `marketing.blog_tags` | All `/admin/api/core/blog/tags/*` endpoints. |

A role can have access to comments but NOT categories, for example — so a "moderator" admin role can be configured to only see the comment queue.

Standard admin roles include all four keys; restricted roles (cashier, fulfilment-only) typically do not. See [[settings-staff]] for the permission matrix.

### Delete cascades wipe comments, orphan on category deletion

- **Article delete**: Hard delete (no soft-delete, no recovery). The article and all of its comments are removed together in the same operation.
- **Parent blog-category delete**: Does NOT delete the article. The article survives orphaned — visible in the [[blog-articles-list]] with no category chip. The merchant must re-assign it. See [[marketing-blog-category]].

### Title-driven slug locks after first save

Once an article has been saved at least once, the URL handle field stops auto-syncing from the title. Manually editing the slug afterwards creates a 301 redirect from the OLD slug to the new slug (via [[marketing-seo-301-redirects]]). The lock applies regardless of whether the merchant saved through the editor, the API, or the CSV import.

### Slug uniqueness per store

The `url_handle` must be unique per store. A collision on save throws the standard uniqueness error and the merchant is asked to edit the slug.

## Related

- [[marketing-blog-articles]] — hub.
- [[blog-articles-list]] — the list page where bulk-status updates respect these rules.
- [[blog-articles-editor]] — the editor whose Save runs this validation.
- [[blog-articles-csv-import]] — bulk import where the 500-cap + plan caps + tag caps still apply.
- [[blog-articles-api]] — JSON-API v2 path that runs the same validation.
- [[blog-articles-storefront-visibility]] — how `active` and `publish_date` are interpreted on the storefront once the validation passes.
- [[marketing-blog-category]] — parent category; orphan-on-delete behaviour.
- [[marketing-blog-tags]] — auto-create target for tag chips.
- [[marketing-seo-meta]] — SEO field semantics; the 191 char cap on `seo_description` is stricter than the 320 char SEO guidance.
- [[marketing-seo-301-redirects]] — auto-created when `url_handle` changes.
- [[settings-staff]] — list of admins eligible to be authors + permission matrix for the four blog keys.
- [[plan-features]] — per-tier counts for `blog_articles` and `blog_categories`.
- [[plan-vs-feature-pack]] — how numeric caps extend via packs.
- [[plan-gates]] — overall plan-gate catalogue.
- [[plan]] — plan tiers.

## Open questions

No outstanding questions.
