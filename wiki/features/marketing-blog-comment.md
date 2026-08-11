---
type: feature
nav_path: "Marketing → Blog → Comment"
route_name: blog-comments
route_path: /admin/marketing-new/blog/comment
aliases: ["Blog comments", "Comments", "Comment moderation", "Comment queue", "Коментари", "Коментари на блог", "Модерация на коментари"]
tags: [marketing, blog, comments, moderation, content]
plan_gates: ["blog_comments"]
created: 2026-05-21
updated: 2026-06-10
source_count: 9
---
# Blog Comments

## Purpose

The **Blog Comments** screen is the **comment moderation queue** for the store's blog. Every visitor-submitted comment lands here — whether posted by an anonymous guest with name+email or by a logged-in customer — where the merchant approves it for public display, marks it as spam, deletes it, or (for stores set to automatic) quickly audits comments that have already gone live.

The screen exists because public comment threads attract spam ("nice post, buy [product]…"), off-topic abuse, and well-meaning but irrelevant content. A merchant running a content blog needs a place to triage all of this before (or after) it appears on the storefront's article pages.

What arrives here depends on the **comment policy** of the parent blog category ([[marketing-blog-category]]): `moderator` → new comments arrive `pending` (invisible until approved); `automatic` → new comments arrive `approved` (this page becomes a clean-up surface); `no` → submissions are rejected outright. See [[marketing-blog-comment-status-model]] for the full status lifecycle.

This hub is slim by design — it catalogues the cluster. Drill into the aspect that matches the question rather than reading every page.

## Sub-pages (in this cluster)

- [[marketing-blog-comment-list]] — the moderation list screen: columns, filters (Article / Blog / Status), search, bulk actions (Approve / Mark spam / Mark pending / Delete), and what the merchant cannot do here.
- [[marketing-blog-comment-manage-modal]] — the status-aware **Manage comment** modal: conditional button set, dynamic opposite-status transition, variant colours, submit-loader.
- [[marketing-blog-comment-status-model]] — comment fields, the `approved` / `pending` / `spam` enum, manual-only transitions, delete-vs-spam, cascade-delete behaviour.
- [[marketing-blog-comment-submission]] — the storefront submission flow: validation order, 5-per-minute rate-limit, distinct success copy, the `cc.blog.article.comment.posted` event, and storefront visibility rules.
- [[marketing-blog-comment-anti-spam]] — native has no built-in spam filter; the two practical answers (moderator policy or third-party [[apps-disqus-comments]] / [[apps-facebook-comments]] replacement).
- [[marketing-blog-comment-permissions-plan]] — the `blog_comments` plan gate, the granular `marketing.blog_comments` staff permission, and cache / side-effect notes.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Comment**.

Route name `blog-comments`; path `/admin/marketing-new/blog/comment`. Header icon is the comments icon. The breadcrumb reads "Marketing → Blog comments".

There is also an **inline link** from each row of [[marketing-blog-articles]] — clicking the "Comments (N)" button on an article navigates here pre-filtered by article so the merchant can moderate per-article. The admin sidebar / dashboard / [[marketing-blog-articles]] header surface a count of pending comments, labelled *"%n comments pending for approval"* — the merchant's daily nudge to visit this queue.

## What the merchant can do here

- **Triage every comment** from one queue: approve, mark as spam, mark as pending, or delete — individually via the Manage modal or in bulk via the list checkboxes. See [[marketing-blog-comment-list]] and [[marketing-blog-comment-manage-modal]].
- **Filter and search** by Article, Blog (category), Status, or free-text (commenter name / email / comment text / article name).
- **Audit who changed what** — each status change records the acting admin (`admin_id`) and a `date_status` timestamp.

The merchant **cannot** edit a comment's text, reply from the admin panel, see the commenter's IP / fingerprint, or configure auto-spam filtering — see [[marketing-blog-comment-list]] for the full "cannot do" list and [[marketing-blog-comment-anti-spam]] for the spam-filtering alternatives.

## Settings & fields

Each comment row carries `item_id` (article FK), `parent_id` (threaded reply FK, unused in the UI), `name` + `email` (guest commenters), `author_id` (logged-in customer FK), `comment` (text, max 1,000 chars), `date_added`, `status`, `date_status`, and `admin_id`. The full field table and the list-column layout live on [[marketing-blog-comment-status-model]] and [[marketing-blog-comment-list]] respectively.

## Business rules

The cluster's business rules are distributed across the aspect pages:

- **Initial status decided at submission** by the parent category's `comments` policy — see [[marketing-blog-comment-status-model]].
- **Submission validation, rate-limit, success copy, storefront visibility** — see [[marketing-blog-comment-submission]].
- **Status transitions are manual, no automation** — see [[marketing-blog-comment-status-model]].
- **Delete vs Mark-as-spam, cascade-delete** — see [[marketing-blog-comment-status-model]].
- **No built-in anti-spam; third-party replacement** — see [[marketing-blog-comment-anti-spam]].
- **Permission scope + plan gate + cache notes** — see [[marketing-blog-comment-permissions-plan]].

## Plan gates

This feature is gated by `blog_comments` (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]) — an access gate with no numeric cap. Lower plans cannot reach the `blog/comment` route at all. Full mapping on [[marketing-blog-comment-permissions-plan]].

## Related

- [[marketing-blog-articles]] — comments attach to articles via `item_id`; inline "Comments (N)" link navigates here pre-filtered.
- [[marketing-blog-category]] — sets the comment policy (`automatic` / `moderator` / `no`) that decides whether new comments arrive `pending` or `approved`.
- [[marketing-blog-tags]] — sibling blog screen, unrelated to comments.
- [[apps-disqus-comments]] — replaces the native comment module on the storefront.
- [[apps-facebook-comments]] — Facebook plugin alternative.
- [[customers]] — logged-in commenters appear in the User column with a link to their profile.
- [[marketing]] — parent hub.
- [[settings-staff]] — moderator permission scope.
- [[apps-gdpr-requests]] — comment cascade-delete on customer deletion.
- [[blog-comment]] — entity page.
- [[blog-article]] — entity page.

## Open questions

No outstanding questions.
