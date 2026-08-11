---
type: feature
nav_path: "Marketing → Blog → Articles → Storefront visibility"
route_name: blog-articles-list
route_path: /admin/marketing-new/blog/articles
aliases: ["Article visibility", "Article publishing", "Publish toggle", "Publish date", "Scheduled publishing", "Comment routing", "Comment throttle", "Storefront blog URLs", "Видимост на статия", "Публикуване на статия"]
tags: [marketing, blog, articles, storefront, publishing, comments]
plan_gates: ["blog_articles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-blog-articles]]. See the hub for the other aspects (list, editor, CSV import, rules, API).

# Blog Articles — storefront visibility & publishing

## Purpose

This aspect documents what happens **once an article is saved** — whether it appears on the storefront, on which URLs, with which comment behaviour, and how the platform throttles abusive comment posts. It is the canonical reference for tickets of the form *"my article saved but doesn't show on the site"* / *"how do I schedule a post"* / *"why does my article have comments off"*.

## Where to find it

These rules are not directly configurable on a dedicated screen — they are governed by:

- The **Published** toggle on the [[blog-articles-list]].
- The `publish_date` field, exposed only by [[blog-articles-api]] and the legacy editor (NOT by [[blog-articles-editor]]).
- The parent category's `comments` setting on [[marketing-blog-category]].
- Third-party apps that replace the native comment thread — see [[apps-disqus-comments]] / [[apps-facebook-comments]].

## What the merchant can do here

- Flip an article between live and hidden via the inline **Published** toggle on the [[blog-articles-list]] (no editor open required).
- Schedule a future publish time — but only via [[blog-articles-api]] or the legacy editor; the modern [[blog-articles-editor]] does NOT expose `publish_date`.
- Change comment behaviour for an article — but only by **moving the article to a differently-configured [[marketing-blog-category]]**. Comments are inherited from the parent category, not configured per-article.
- Replace the native comment thread with Disqus or Facebook Comments by installing the corresponding app — see [[apps-disqus-comments]] / [[apps-facebook-comments]].

## Settings & fields

### Visibility flags

| Flag | Where set | Effect on storefront |
|------|-----------|----------------------|
| `active` (`yes` / `no`) | [[blog-articles-list]] Published toggle, [[blog-articles-editor]] Save (always `yes`), [[blog-articles-api]] | When `no`, the article is excluded from `/blog/` listings + `/article/<slug>` (404 on the detail page). |
| `publish_date` | [[blog-articles-api]] + legacy editor only | When set in the future, the storefront's "Published" scope hides the article until `publish_date <= now` (store timezone, end-of-minute). |

### Storefront URLs

- Single article: `/article/<url_handle>` (route `blog.article.view`).
- Articles by category: `/blog/category/<category_url_handle>` (route `blog.view` with `filter=category`).
- Articles by tag: `/blog/tag/<tag_url_handle>` (route `blog.view` with `filter=tag`).
- Blog index (all categories): `/blog/` (route `blog.list`).
- Submit a comment (POST): `/blog/article/create-comment/{article_id}`.

The storefront pages render only articles where `active='yes'` AND `publish_date` either NULL or `<= now` in the store timezone.

## Business rules

### Status: publish toggle, not workflow

There is no draft / review / scheduled workflow in the modern editor — `active` is a simple yes / no flag. The article is either live on the storefront or hidden. Toggling it OFF immediately removes the article from `/blog/` listings + the `/article/<slug>` detail page on the next page load (no cache delay beyond Cloudflare's edge TTL).

### Scheduled publishing is available, but only via legacy paths

A `publish_date` field exists in the data model and **DOES still gate storefront visibility when populated** — the storefront applies a global "Published" scope that hides articles whose `publish_date > now` (timezone-aware, evaluated to end-of-minute in the store's timezone). The modern editor does not expose this field, so a typical merchant flow uses `active` only.

To use scheduled publishing today, the merchant has to either:

1. Set `publish_date` via the legacy editor in Sitecp; or
2. Set it via the public API — see [[blog-articles-api]].

There is no admin notification at the moment a scheduled article goes live — the transition is passive (the SQL scope check finally passes; no cron / queue job fires).

### Comment routing: per article, controlled by the parent category

Whether comments are accepted on a given article — and whether they are auto-approved or moderated — is decided at the **blog category** level, not per-article. See [[marketing-blog-category]] for the three `comments` settings (`no`, `moderator`, `automatic`). To change comment behaviour for a single article, the merchant has to move it to a differently-configured category.

When a visitor submits a comment, the platform reads the parent blog category's comment policy and stamps the new comment with the right status (`pending` for moderator, `approved` for automatic, rejected outright for `no`). See [[marketing-blog-comment]] for the moderation queue.

### Comment submission rate-limit (storefront)

The storefront `POST /blog/article/create-comment/{article_id}` is throttled at **5 submissions per 1 minute per IP** (via the a submission throttle middleware on the `/blog` route group). Exceeding the cap returns *"Too many requests"* / HTTP 429 — the `guessField` maps that error to the `comment` field, so the storefront highlights the comment textarea. This is the platform's only built-in rate limit on comment submission — there is no IP block-list, no CAPTCHA, no Akismet.

### Third-party comment-platform replaces native

When [[apps-disqus-comments]] or [[apps-facebook-comments]] is installed, the storefront's article page replaces the native comment form + thread with the third-party module. CloudCart's native comment records remain in the DB (visible in [[marketing-blog-comment]]) but aren't rendered on the storefront. This means the merchant can switch platforms back and forth without losing historical native comments.

### Cover image surfaces in three places

The **featured cover image** (`image` field) is displayed:

- In the [[blog-articles-list]] view as a `150x150` thumbnail next to the article title.
- On the storefront article page (header banner) and blog listing card.
- In any RSS / sitemap export of the blog.

## Related

- [[marketing-blog-articles]] — hub.
- [[blog-articles-list]] — Published toggle + pending-comments banner.
- [[blog-articles-editor]] — the editor does NOT expose `publish_date`; first save defaults `active='yes'`.
- [[blog-articles-rules]] — `active` and `publish_date` validation.
- [[blog-articles-api]] — the way to set `publish_date` programmatically.
- [[marketing-blog-category]] — parent category drives comment routing.
- [[marketing-blog-comment]] — moderation queue; pending comments banner lands here.
- [[apps-disqus-comments]] — third-party commenting replacement.
- [[apps-facebook-comments]] — Facebook Comments Plugin alternative.

## Open questions

- Whether changing `active` from `yes` → `no` purges Cloudflare's edge cache automatically or relies on the natural TTL is `(verify)`.
