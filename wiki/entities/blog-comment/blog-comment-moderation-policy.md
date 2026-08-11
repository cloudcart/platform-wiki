---
type: entity
nav_path: "Entity → Blog Comment → Moderation policy"
aliases: ["Blog Comment moderation policy", "Blog Comment category comments setting", "automatic moderator no comments policy", "Pending approval badge", "Comment policy per category"]
tags: [entity, blog, comments, moderation, policy]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[blog-comment]]. See the hub for the other aspects (data model, lifecycle, validation, threading & visibility, spam protection).

# Blog Comment — Moderation policy

## Identity

The moderation policy for Blog Comments is **per-[[blog-category|Blog Category]], not per-article and not per-comment**. Each Blog Category carries a `comments` setting with three values — `automatic`, `moderator`, or `no` — and that setting drives what happens when a visitor submits a comment on any article inside the category. The submission-time lookup reads the parent article's category and applies the policy. There is no per-article override and no admin-side affordance to change a single comment's "should this have been auto-approved" status retroactively (beyond the standard transitions on [[blog-comment-lifecycle]]).

The policy also feeds the **"Pending approval" badge** — the only nudge the merchant ever sees about new comments. There is no email notification, no toast, no admin push — the merchant must either visit [[marketing-blog-comment]] or notice the badge.

## Aliases

- **`comments` setting** / **Comment policy** / **Category comment mode** — the field on [[blog-category]] that takes the three values.
- **Automatic mode** / **Moderator mode** / **Disabled mode** — informal phrasing for the three values.
- **Pending approval badge** — the queue-count pill that surfaces backlog from `moderator` mode.

## Key Attributes

### The three category `comments` settings

| Setting | Initial comment status | Storefront behaviour | Queue behaviour |
|---------|------------------------|----------------------|-----------------|
| `automatic` | `approved` | Submitted comment appears immediately. | Queue is a clean-up surface for spam that slipped through. |
| `moderator` | `pending` | Submitted comment is invisible to other visitors (the author still sees their own — see [[blog-comment-threading-visibility]]). | Comment lands in the "Pending" filter; the "Pending approval" badge increments. |
| `no` | (no row created) | Storefront refuses the submission with *"The comments for this post are disabled"*. | Nothing arrives. |

The setting is read at **submission time** — changing the category later does NOT retroactively change the status of existing comments. Switching a category from `automatic` to `moderator` does not move historic comments from `approved` to `pending`.

### Initial status is decided per-article-category, not per-comment

The platform reads the parent [[blog-category|Blog Category]]'s `comments` setting at submission time to decide whether the new comment lands as `approved` (under `automatic`), `pending` (under `moderator`), or is rejected entirely (under `no`). To change the policy for an article, the merchant changes the parent category's `comments` setting in [[marketing-blog-category]] — there is no per-article comment-policy override and no per-comment policy override.

For mixed-content blogs (e.g. an "Editorial" category and a "Community discussion" category), the merchant should split high-traffic content into a `moderator`-mode category and low-traffic content into `automatic`-mode if they want different defaults.

### Storefront success messaging

The submission endpoint returns two distinct success messages based on the parent category's `comments` setting:

- `automatic` → *"Comment posted"*.
- `moderator` → *"Comment posted (pending moderation)"*.

The endpoint also fires the `cc.blog.article.comment.posted` event so storefront templates can hook UI updates (e.g. success toast, refresh the comment list). The `no` mode never reaches success — the submission errors out with *"The comments for this post are disabled"*.

### The "Pending approval" badge

When at least one comment has `status='pending'`, a badge appears on:

- The admin sidebar (next to the Blog navigation entry).
- The dashboard.
- The [[marketing-blog-articles]] header.

Badge label: *"%n comments pending for approval"*. This is the merchant's daily nudge to visit [[marketing-blog-comment]] and clear the queue. The badge clicking navigates to the queue's Pending filter.

The badge count feeds from a meta field on the article-list response — the admin list response includes `meta.pending_comments` computed via a single COUNT query on rows where `status='pending'`. The sidebar/dashboard pill reads from this meta on every article-list fetch; there is no separate "count" endpoint.

### No admin notification on new comment

There is NO admin notification when a new Blog Comment is posted (unlike new orders or new customer registrations). The merchant must visit [[marketing-blog-comment]] periodically — the "Pending approval" badge is the only nudge.

The list of events that DO trigger admin notifications lives on [[settings-admin-notifications]]; comments are intentionally not on that list. Merchants who want a notification on each pending comment have to wire one up via [[settings-hooks|webhooks]] (no native blog-comment webhook exists either — see [[blog-comment-spam-protection]] for what is and isn't on the platform).

### No customer notification on status change

There is NO customer notification when a comment is approved, marked spam, or replied to. The storefront's article page is the only place comment activity is visible. A logged-in author who comes back to the article will see their pending comment surface as approved once the merchant clears it — but they get no push, no email, no toast.

### Permission gating

Comment moderation requires the granular **`marketing.blog_comments`** permission on the admin's [[merchant-roles|role]] — independent from `marketing.blog_articles`, `marketing.blog_categories`, and `marketing.blog_tags`. A role can be configured as a comment-moderator-only admin without giving them write access to articles or categories. Bulk actions check the same permission. The `admin_id` column on each comment records which staff member performed the last status change — see [[blog-comment-data-model]].

## Where it appears

- [[marketing-blog-category]] — the `comments` setting field is edited here (per-category dropdown with `automatic` / `moderator` / `no`).
- [[marketing-blog-comment]] — the moderation queue + status filters that the policy feeds into.
- [[marketing-blog-articles]] — surfaces the per-article "Comments (N)" link and the "Pending approval" header badge.
- The storefront `/blog/<slug>` article page — applies the policy at submission time and returns the policy-specific success message.
- Admin sidebar / dashboard — "Pending approval" badge linking to the queue.

## Related

- [[blog-comment]] — hub.
- [[blog-comment-lifecycle]] — the seven phases the policy starts the comment in.
- [[blog-comment-data-model]] — the `status` field that the policy assigns at submit time.
- [[blog-comment-validation]] — what gates the submission BEFORE the policy is applied.
- [[blog-category]] — entity carrying the `comments` setting.
- [[marketing-blog-category]] — feature page for editing the setting.
- [[marketing-blog-comment]] — moderation queue.
- [[merchant-roles]] — `marketing.blog_comments` permission.
- [[settings-admin-notifications]] — list of events that DO notify; comments are NOT on it.

## Open Questions

None.
