---
type: feature
nav_path: "Marketing → Blog → Comment → Submission"
route_name: blog-comments
route_path: /admin/marketing-new/blog/comment
aliases: ["Comment submission", "Comment submit validation", "Comment rate limit", "Comment storefront visibility", "Изпращане на коментар"]
tags: [marketing, blog, comments, moderation, content, storefront]
plan_gates: ["blog_comments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-blog-comment]]. See the hub for the other aspects (list, manage modal, status model, anti-spam, permissions & plan).

# Blog Comments — Storefront submission

## Purpose

This aspect documents the **storefront side** of comments: what happens when a visitor submits the comment form on an article page — the validation order, the rate-limit, the distinct success copy, the JS event fired, and which comments the storefront actually renders. The merchant-facing moderation queue itself is on [[marketing-blog-comment-list]].

## Where to find it

Submission happens on the storefront article page `/article/<slug>` (POST endpoint `/blog/article/create-comment/{article_id}`), not in the admin. The resulting comments are moderated from Sidebar → Marketing → Blog → Comment.

## What the merchant can do here

The merchant does not submit comments — visitors do. The merchant's lever over submission is the parent category's comment policy ([[marketing-blog-category]]), which decides whether a submitted comment arrives `pending`, `approved`, or is rejected. See [[marketing-blog-comment-status-model]] for the initial-status rule.

## Settings & fields

Submission writes a new row into `comment__articles_comments` with `item_id`, `name`/`email` (guests) or `author_id` (logged-in customers), `comment`, `date_added`, and the policy-derived `status`. The full field table is on [[marketing-blog-comment-status-model]].

## Business rules

### Submission validation

Comments going through the storefront form are validated for:

- **Article exists** — *"No longer exists"* if not.
- **Comments enabled on parent category** — *"The comments for this post are disabled"* otherwise.
- **Name** — required for guests. *"Your name is required"* (storefront-facing) / *"Name is required"* (admin-facing).
- **Email** — required + format-validated for guests. *"Your email address is required"* plus a 191-char email format check.
- **Comment text** — required, ≤ 1,000 chars. *"You forgot to type a message"* / *"Comments can not be longer than 1000 characters"*.

### Validation order on submit (storefront)

The storefront comment-submit endpoint walks through checks in this exact order — the first failure is the one returned:

1. **Article exists?** Otherwise: *"No longer exists"*.
2. **Parent category's `comments` setting != `no`?** Otherwise: *"The comments for this post are disabled"*.
3. **Logged-in commenter? OR Name + Email provided for guest?** Names use *"Your name is required"* (storefront) / *"Name is required"* (admin). Email runs through `filter_var($email, FILTER_VALIDATE_EMAIL)` + 191-char length check.
4. **Comment text non-empty?** Otherwise: *"You forgot to type a message"* (storefront) / *"Comments can not be longer than 1000 characters"* (admin).
5. **Comment text ≤ 1000 chars?** Otherwise: *"Comments can not be longer than 1000 characters"*.

### Author email validation

The email field uses PHP's `filter_var(FILTER_VALIDATE_EMAIL)` — a syntactic, format-only check. No MX/DNS/SPF lookup, no integration with external reputation services, no detection of common typos (e.g. `gnail.com`), no disposable-domain blocklist. Any well-formed `local@domain.tld` is accepted.

### Submission rate-limit: 5 / minute / IP

The storefront `POST /blog/article/create-comment/{article_id}` is throttled via the a submission throttle middleware (max 5 attempts per 1 minute per IP+route key). Exceeding the cap returns HTTP 429 with the message *"Too many requests"* mapped to the `comment` field (the storefront template highlights the comment textarea). This is the platform's ONLY built-in rate-limit on the comment surface — no CAPTCHA, no Akismet, no per-IP block-list. See [[marketing-blog-comment-anti-spam]].

### Distinct success messages

The storefront's comment-submit response carries different success copy depending on the parent category's policy:

- `automatic` → *"Comment posted"*.
- `moderator` → *"Comment posted (pending moderation)"*.

The response also fires the `cc.blog.article.comment.posted` event so the storefront's theme can hook UI updates (animations, "thanks for commenting" toast).

### Storefront visibility rules

The storefront's comment module on `/article/<slug>` only renders comments where `status='approved'`. A subtlety: when the visitor is the comment's own author (logged in as the customer), their `pending` comments ARE shown to THEM. This is so a customer doesn't see their just-submitted moderated comment vanish — they see it "pending" with a note.

When an article is rendered its comment list is queried live — there's no per-comment cache, and a status change in the admin is reflected on the next storefront request without an explicit cache flush.

## Plan gates

Gated by `blog_comments` (the moderation route). The storefront 5-per-minute rate-limit applies regardless of plan tier. Full mapping on [[marketing-blog-comment-permissions-plan]].

## How it works (verified against backend)

- **Submission validation order** (storefront): article exists → parent category comments != `no` → name+email for guests → comment text non-empty → comment text ≤ 1000 chars. Email is format-only via PHP's `filter_var(FILTER_VALIDATE_EMAIL)`.
- **Storefront rate limit** — `POST /blog/article/create-comment/{article_id}` is throttled at 5 submissions per 1 minute per IP via the a submission throttle middleware (confirmed in the platform code). HTTP 429 on overflow.
- **Storefront visibility** — Article pages render only `status='approved'` comments. Exception: the logged-in author sees their own `pending` comment with a "pending moderation" note.
- **Events** — On submission the storefront fires the `cc.blog.article.comment.posted` JS event so themes can hook UI updates.

## Related

- [[marketing-blog-comment]] — hub.
- [[marketing-blog-comment-status-model]] — the initial-status rule submission feeds into.
- [[marketing-blog-comment-anti-spam]] — the rate-limit is the only native anti-spam.
- [[marketing-blog-category]] — comment policy that gates submission and seeds the success copy.
- [[marketing-blog-articles]] — articles carry the comments; deleting one cascades.

## Open questions

No outstanding questions.
