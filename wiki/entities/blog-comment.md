---
type: entity
nav_path: "Entity → Blog Comment"
aliases: ["Blog Comment", "Comment", "Article comment", "Blog post comment", "Visitor comment", "Reader comment", "Коментар", "Коментар на статия", "Коментар в блога"]
tags: [entity, blog, marketing, content, comments, moderation]
created: 2026-05-24
updated: 2026-06-10
source_count: 5
---

# Blog Comment

## Identity

A **Blog Comment** is a piece of visitor-submitted feedback attached to a single [[blog-article|Blog Article]] on the store's blog. It carries the commenter's name, email, comment text, and (optionally) a parent comment reference for threaded replies — plus a moderation `status` (`pending` / `approved` / `spam`) and timestamps. Comments can be left by anonymous guests (who type their name + email into the storefront form) OR by logged-in customers (whose name and email are pulled from their [[customer|Customer]] record). The merchant moderates them on [[marketing-blog-comment]] (Sidebar → Marketing → Blog → Comment), where the queue surface lets them approve, mark as spam, or delete each comment.

A Blog Comment's behaviour at submission time is decided by the **parent [[blog-category|Blog Category]]'s `comments` setting** (`automatic` / `moderator` / `no`) — see [[blog-comment-moderation-policy]] for the full per-category gating model. A Blog Comment is distinct from a **product review** (which lives on a Product, not a Blog Article, and uses separate moderation) and from comments managed by third-party modules like [[apps-disqus-comments|Disqus]] or [[apps-facebook-comments|Facebook Comments]] — when those apps are active on the storefront, visitor comments go to the third-party platform's database and admin tools, NOT to CloudCart's native queue. See [[blog-comment-spam-protection]] for how the third-party replacements interact with the native queue.

## Aliases

- **Blog Comment** / **Article comment** / **Blog post comment** — canonical merchant-facing terms.
- **Comment** — short form used throughout the [[marketing-blog-comment]] queue.
- **Visitor comment** / **Reader comment** — informal phrasing.
- **Коментар** / **Коментар на статия** / **Коментар в блога** — Bulgarian labels used interchangeably in the BG admin.

## Key Attributes

The Blog Comment record is small — 10 merchant-visible fields covering content, authorship, moderation state, and audit. The full attribute table + cascade-delete rules + the email-not-verified rule live on [[blog-comment-data-model]].

Headline points:

- **One comment belongs to one [[blog-article|Blog Article]]** via `item_id` and (optionally) to one parent comment via `parent_id` (replies — see [[blog-comment-threading-visibility]]).
- **Author identity is locked at submission time** — `author_id` is the [[customer|Customer]] record when the commenter is logged in, NULL for guests. There is no admin-side affordance to relink a guest comment to a Customer after the fact.
- **`status` is one of three values** — `approved` / `pending` / `spam` — plus the implicit "deleted" terminal state. See [[blog-comment-lifecycle]] for the full transition matrix.
- **`comment` text is plain text, max 1,000 characters** — no rich text, no HTML, rendered as escaped HTML on the storefront. See [[blog-comment-validation]] for the full validation rules.
- **`admin_id`** records which staff member last changed the status; survives admin churn (`ON DELETE SET NULL`).

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[blog-comment-data-model]] — the field-by-field attribute table; cascade-delete rules on `item_id` / `parent_id` / `author_id`; `admin_id` set-null behaviour; email-not-verified rule; guest-stays-guest rule.
- [[blog-comment-lifecycle]] — submission flow; the seven phases (submitted → initial status → in queue → approved / pending / spam / deleted); the manual status-transition matrix; delete vs spam semantics.
- [[blog-comment-moderation-policy]] — per-[[blog-category|Blog Category]] `comments` setting (`automatic` / `moderator` / `no`); how it decides initial status at submit time; the "Pending approval" badge that nudges the merchant.
- [[blog-comment-validation]] — the five storefront validation checks and their error messages; the deterministic check order; format-only email validation; the `5 submissions / 1 minute / IP` rate-limit; success messaging by category mode.
- [[blog-comment-threading-visibility]] — `parent_id` replies model; flat admin queue (no threaded UI); storefront visibility rule; the author-sees-own-pending exception; no admin-side reply / edit.
- [[blog-comment-spam-protection]] — what the platform does NOT provide (CAPTCHA, Akismet, MX lookup, per-IP block-list, banned-word filter, IP exposure in queue); the three practical mitigations (moderator mode, [[apps-disqus-comments|Disqus]], [[apps-facebook-comments|Facebook Comments]]); third-party replacement behaviour.

## Where it appears

- [[marketing-blog-comment]] — the master moderation queue. Filters, search, bulk actions, Manage modal, per-row delete. Primary admin surface for everything in this cluster.
- [[marketing-blog-articles]] — inline "Comments (N)" link on each article row navigates to the comment queue pre-filtered by that article.
- [[marketing-blog-category]] — the category's `comments` setting decides the initial status of comments on articles in this category — see [[blog-comment-moderation-policy]].
- The storefront `/blog/<slug>` article page — comment module renders approved comments and (for logged-in authors) their own pending comments. The submission form posts to `POST /blog/article/create-comment/{article_id}`.
- Admin sidebar / dashboard — "%n comments pending for approval" badge linking to the queue.

## Related

### Related entities

- [[blog-article]] — the article the comment is attached to via `item_id`.
- [[blog-category]] — sets the `comments` policy (`automatic` / `moderator` / `no`) that decides initial comment status.
- [[customer]] — logged-in commenters reference their customer record via `author_id`.
- [[staff-member]] — the moderator who last changed status (`admin_id`).
- [[blog-tag]] — tag relationship is on articles, not on comments.

### Cross-cutting concepts

- [[notification-delivery]] — comments do NOT participate in the notification pipeline; the merchant must check the queue manually.
- [[merchant-roles]] — the granular `marketing.blog_comments` permission gates the moderation queue independently of articles / categories / tags.

### Settings & feature pages

- [[marketing-blog-comment]] — primary admin moderation screen.
- [[marketing-blog-articles]] — articles list with inline comments link.
- [[marketing-blog-category]] — comment policy per category.
- [[apps-disqus-comments]] — third-party replacement for the native module.
- [[apps-facebook-comments]] — Facebook plugin alternative.
- [[apps-gdpr-requests]] — customer deletion cascades to comments.
- [[settings-banned-ip]] — to ban a spam commenter's IP, the merchant must do it here manually (no banning shortcut from the queue).
- [[settings-admin-notifications]] — comments are NOT on the list of events that send admin notifications.

## Open Questions

None — all open items distributed to sub-pages or resolved.
