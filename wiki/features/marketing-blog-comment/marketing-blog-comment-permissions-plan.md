---
type: feature
nav_path: "Marketing → Blog → Comment → Permissions & plan"
route_name: blog-comments
route_path: /admin/marketing-new/blog/comment
aliases: ["Comment permissions", "Comment plan gate", "blog_comments gate", "marketing.blog_comments permission", "Права за коментари"]
tags: [marketing, blog, comments, moderation, content, permissions, plan-gates]
plan_gates: ["blog_comments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-comment]]. See the hub for the other aspects (list, manage modal, status model, submission, anti-spam).

# Blog Comments — Permissions & plan gate

## Purpose

This aspect documents who can reach the comment moderation queue and on which plans: the granular `marketing.blog_comments` staff permission, the `blog_comments` plan-feature access gate, and the cache / side-effect notes that apply to status changes.

## Where to find it

The staff permission is configured per role on [[settings-staff]]. The plan gate is enforced on the `blog/comment` route (Sidebar → Marketing → Blog → Comment) and surfaces an upsell at [[plan-features]] when below tier.

## What the merchant can do here

A store owner grants or revokes a staff member's access to the comment queue by toggling the `marketing.blog_comments` permission on that admin's role — independently of articles, categories, and tags. To unlock the feature on a lower plan, the merchant upgrades the plan.

## Settings & fields

The relevant identifiers:

- **Staff permission:** `marketing.blog_comments` (per-role, on [[settings-staff]]).
- **Plan-feature key:** `blog_comments` (access gate).
- **Audit field:** `admin_id` on each comment records the staff member who last changed status. See [[marketing-blog-comment-status-model]].

## Business rules

### Permission

Comment moderation requires the granular **`marketing.blog_comments`** permission on the admin's role — independent from `marketing.blog_articles`, `marketing.blog_categories`, and `marketing.blog_tags`. A role can be configured as a comment-moderator-only admin without giving them write access to articles. Bulk actions check the same permission. The `admin_id` column records which admin performed the last status change.

### Cache + side effects

Status changes write to `comment__articles_comments.status` + `date_status` + `admin_id`. The storefront's article page is rebuilt at the next request (no explicit cache flush is fired). When an article is rendered, its comment list is queried live — there's no per-comment cache. (Storefront visibility detail is on [[marketing-blog-comment-submission]].)

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `blog_comments` | Access | Lower plans cannot access the `blog/comment` route at all — the moderation queue is hidden. No numeric cap (comments are unlimited per article; the storefront enforces a 5-per-minute-per-IP rate-limit independently of plan tier — see [[marketing-blog-comment-submission]]). |

When below the access tier, the merchant is redirected to the per-feature upsell at [[plan-features]]. Access gates require a plan upgrade ([[plan-vs-feature-pack]] is not applicable for access-only gates).

## How it works (verified against backend)

- **Permissions** — Gated by the granular `marketing.blog_comments` staff permission, independent from articles / categories / tags. The `admin_id` column records which staff member performed the last status change.
- **Cache + events** — Status changes write `status` + `date_status` + `admin_id` and rely on the next storefront request to re-fetch (no explicit cache flush).
- **Plan gate** — `blog_comments` is an access gate with no numeric cap; below-tier plans are redirected to the [[plan-features]] upsell.

## Related

- [[marketing-blog-comment]] — hub.
- [[marketing-blog-comment-status-model]] — `admin_id` audit field and status writes.
- [[marketing-blog-comment-submission]] — the plan-independent storefront rate-limit.
- [[settings-staff]] — where the `marketing.blog_comments` permission is granted.
- [[plan-gates]] — plan-gating model.
- [[plan-features]] — per-feature upsell destination.
- [[plan-vs-feature-pack]] — access gate vs feature-pack distinction.

## Open questions

No outstanding questions.
