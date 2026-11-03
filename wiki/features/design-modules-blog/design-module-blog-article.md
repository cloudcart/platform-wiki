---
type: feature
nav_path: "Storefront → Article page (system module)"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Article module", "Single article module", "blog.article", "Article page module", "Comment form module", "Article comments module", "Модул статия"]
tags: [design, modules, blog, article, comments, system]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Article page (`article`)

> Part of [[design-modules-blog]]. See the category page for the other blog modules.

## Purpose

The **Article** module (`blog.article`) is the SYSTEM module that renders a single blog article on its own storefront page (`/article/{slug}`). It pulls the article body, hero image, author, publish date, tags, breadcrumbs, and the related comments — including the customer-facing comment FORM. This is the module the customer experiences when they click a blog headline anywhere on the storefront.

It is a **system module** — there is no card on the Modules screen, no settings form, no enable / disable toggle. The module renders automatically when the route resolves. Everything about how an article looks is controlled by the article record itself (edited in [[marketing-blog-articles]]) and the active theme's article template.

## Where to find it

This module has **no admin surface**. It is invoked automatically by the storefront's article route:

| Surface | Route | Notes |
|---|---|---|
| `/article/{slug}` | `article.view` | The customer-facing article page |
| Article create-comment | `article.create.comment` | POST endpoint hit by the comment form |

To configure what the customer sees, the merchant edits the underlying article in [[marketing-blog-articles]] (title, body, image, tags, blog category, SEO metadata, comment-allowed flag).

## What the merchant can do here

This module has NO admin form — there's nothing the merchant can do FROM this module directly. Even so, the merchant DOES control article-page behaviour via other admin screens:

- **Whether comments are allowed on the article's blog category** — toggled per blog in [[marketing-blog-category]]. The module reads `blog.comments` and shows the comment form only when it's not `no`.
- **Whether a customer comment is visible** — moderated per-comment in [[marketing-blog-comment]]. Pending comments show with an *"sf.module.blog.article.nfy.comment_not_approved"* label to the customer who posted it (so they know it's been received), and stay invisible to other customers until approved.
- **The article content itself** — title, body, hero image, author, tags, publish date, status, SEO. Edited in [[marketing-blog-articles]].
- **The active theme** — controls the layout (image-on-top, image-beside-text, full-width), the typography, and which sidebar modules render next to the article. See [[design-themes]].
- **Whether a third-party comment provider takes over** — installing Disqus ([[apps-disqus-comments]]) or Facebook Comments ([[apps-facebook-comments]]) replaces the native comment form at the theme level.

The module has no enable / disable toggle, the comment-form fields are fixed (name, email, comment), and the avatar source is hard-coded to Gravatar.

## Settings & fields

**None** — this system module has no settings form. The rendered data comes from elsewhere:

| Field source | Editing surface |
|---|---|
| Title, body, hero image, content | [[marketing-blog-articles]] |
| SEO title / description | [[marketing-blog-articles]] → SEO panel |
| Tags | [[marketing-blog-tags]] + per-article tag picker |
| Blog category | [[marketing-blog-category]] |
| Author | Per-article author select in [[marketing-blog-articles]] |
| Comment-allowed flag | Per-blog setting in [[marketing-blog-category]] (`comments` enum: `no` / `all` / `customers-only` — verify) |
| Per-comment moderation status | [[marketing-blog-comment]] |

## Theme dependencies

Universal — every theme that has blog enabled ships an `article` module instance + an `article.tpl` template. Themes WITHOUT blog support don't expose the `/article/{slug}` route at all and the module never instantiates. Layout decisions (image-on-top vs image-beside-text, comment-thread placement, whether the form requires login) are 100 % theme-controlled.

## Business rules

### Article must be published to be reachable

Loading `/article/{slug}` resolves the article by URL handle. Drafts, archived articles, and articles without a blog category are excluded — hitting an unpublished article raises HTTP 404 with the translation key *"sf.module.blog.article.err.article_no_longer_active"*. URL handle changes auto-redirect (URL history tracked at the article level).

### Comment form visibility is controlled by the blog category

The comment form renders only when the parent blog category has comments enabled (`comments` != `no`). Disabling comments at the category level silently hides the form on every article in that category — there is no per-article override.

### Anonymous vs logged-in comment form

When the customer is logged in, the comment form HIDES the name + email fields (the module uses the authenticated customer's profile data). When the customer is not logged in, both fields appear and are required.

### Pending comments visible only to the author

After submitting a comment, the customer who posted it sees their own comment in the thread with an *"sf.module.blog.article.nfy.comment_not_approved"* badge — so they know it's received. Other customers do NOT see pending comments. Once moderated (approved), the badge disappears and every customer sees it.

### Form post fires a JS custom event

After a successful POST, the storefront fires `cc.blog.article.comment.posted` and the form resets. Third-party scripts (analytics, anti-spam tools) and merchant custom theme code can listen to it.

### Empty-state and author fallback

When the article has no comments yet AND commenting is allowed, an empty-state notice appears under the comment form; when commenting is disabled, no message appears. An article with no author still renders normally (the author slot is simply blank).

### Third-party comment apps replace the form, not the module

Installing Disqus or Facebook Comments replaces the COMMENT FORM + THREAD section of the article-page template at the theme level. The Article module itself still loads — the article body, hero image, breadcrumbs and metadata still render — only the comment slot is swapped out.

## Tips for merchants

- Tickets like "how do I change the article-page layout" route to the THEME ([[design-themes]]) or the ARTICLE record ([[marketing-blog-articles]]), never to this module.
- After installing a third-party comment app, old third-party comments stay with the third-party provider — uninstalling returns the slot to the native module but the existing third-party comments are not migrated.
- The `cc.blog.article.comment.posted` JS event is the right hook for analytics / spam-tool integrations.

## Related

- [[design-modules-blog]] — hub.
- [[design-module-blog-listing]] — sibling; the listing the customer arrives from.
- [[design-module-blog-recent-comments]] — sibling; reads the same comment pool.
- [[marketing-blog-articles]] — article authoring; source of every field the module renders.
- [[marketing-blog-category]] — gates whether the comment form renders.
- [[marketing-blog-comment]] — comment moderation; gates which comments render publicly.
- [[marketing-blog-tags]] — tag links rendered alongside the article.
- [[apps-disqus-comments]] — third-party Disqus integration; replaces the comment slot.
- [[apps-facebook-comments]] — third-party Facebook Comments; replaces the comment slot.
- [[design-themes]] — theme picker; controls article-page layout.

## Open questions

- 📡 **`comments` enum on the blog category.** Confirm the exact allowed values (`no`, `all`, `customers-only` — verify) and whether the customers-only state hides the form from anonymous visitors. Current behaviour reads as two-state (comments on / off), but the underlying field may include more values (verify).
- 📡 **Comment form JS.** Confirm the inline comment-form script still runs (it does — the `cc.blog.article.comment.posted` event is observable today).
