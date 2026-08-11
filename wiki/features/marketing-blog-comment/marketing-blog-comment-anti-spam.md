---
type: feature
nav_path: "Marketing → Blog → Comment → Anti-spam"
route_name: blog-comments
route_path: /admin/marketing-new/blog/comment
aliases: ["Comment anti-spam", "Comment spam filtering", "Disqus replacement", "Facebook comments replacement", "Спам коментари"]
tags: [marketing, blog, comments, moderation, content, spam]
plan_gates: ["blog_comments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-comment]]. See the hub for the other aspects (list, manage modal, status model, submission, permissions & plan).

# Blog Comments — Anti-spam & third-party replacement

## Purpose

This aspect answers the recurring merchant question: *"How do I stop spam comments?"* The short answer is that CloudCart's **native comment form has no built-in spam filtering** — the only mechanisms are manual moderation and a per-IP rate-limit — so the two practical answers are the moderator policy or a third-party platform replacement (Disqus / Facebook).

## Where to find it

Anti-spam choices are made on two screens: the comment policy on the parent blog category ([[marketing-blog-category]]), and the third-party app activation under Apps ([[apps-disqus-comments]] / [[apps-facebook-comments]]). The native moderation queue itself is [[marketing-blog-comment-list]].

## What the merchant can do here

To fight spam, the merchant can: (1) set the category to `moderator` so every comment queues before going live, or (2) activate a third-party comment platform that brings its own spam filtering. There is no in-platform filter to configure.

## Settings & fields

This aspect introduces no fields of its own. The relevant levers are the category's `comments` policy ([[marketing-blog-category]]) and the third-party app toggles. Native comment fields are on [[marketing-blog-comment-status-model]].

## Business rules

### Anti-spam: native has none built-in

CloudCart's native comment form has NO built-in:

- CAPTCHA (relying on the form's hidden honeypot, if present in the storefront template).
- Akismet check.
- Per-IP rate-limit beyond the global post throttle on the `/blog` POST routes (5 submissions per 1 minute per IP — see [[marketing-blog-comment-submission]]).
- Banned-word filter.
- Link-shortener detection.

For stores facing significant spam, the practical answer is:

1. Switch the category to `comments=moderator` (everything queues — see [[marketing-blog-category]]).
2. Or switch to [[apps-disqus-comments]] / [[apps-facebook-comments]] (third-party spam filtering).

Because there is no learning filter, all status transitions stay manual — see [[marketing-blog-comment-status-model]].

### Third-party platform replacement

When [[apps-disqus-comments]] is active, the storefront's article page renders the Disqus module INSTEAD of the native comment form. Visitors comment via Disqus (whose admin lives at disqus.com); CloudCart's `comment__articles_comments` table doesn't receive new rows from those comments. Historic native comments remain in this admin queue but are not displayed on the storefront.

Same applies to [[apps-facebook-comments]] — when active, visitors comment via Facebook's plugin and moderation moves to Facebook's developer tools.

This page (the native moderation queue at [[marketing-blog-comment-list]]) remains available for historic data review even while a third-party platform is active.

## Plan gates

The native moderation queue is gated by `blog_comments`. The third-party apps have their own activation requirements under Apps. Full plan mapping on [[marketing-blog-comment-permissions-plan]].

## How it works (verified against backend)

- The only native anti-spam mechanism is the a submission throttle rate-limit on the storefront submit route (5 per minute per IP) — confirmed against the platform code. No CAPTCHA, no Akismet, no per-IP block-list, no banned-word list.
- Activating Disqus or Facebook comments swaps the storefront comment module; the native table stops receiving new rows but retains historic comments, which stay reachable from the admin queue for review.

## Related

- [[marketing-blog-comment]] — hub.
- [[marketing-blog-comment-submission]] — the rate-limit detail.
- [[marketing-blog-comment-status-model]] — manual-only transitions (no spam engine).
- [[marketing-blog-category]] — `moderator` policy is the native spam defence.
- [[apps-disqus-comments]] — replaces the native comment module with third-party spam filtering.
- [[apps-facebook-comments]] — Facebook plugin alternative.

## Open questions

No outstanding questions.
