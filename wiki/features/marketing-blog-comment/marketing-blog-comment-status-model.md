---
type: feature
nav_path: "Marketing → Blog → Comment → Status model"
route_name: blog-comments
route_path: /admin/marketing-new/blog/comment
aliases: ["Comment status model", "Comment fields", "Comment status transitions", "Comment cascade delete", "Delete vs spam", "Статус на коментар"]
tags: [marketing, blog, comments, moderation, content]
plan_gates: ["blog_comments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-blog-comment]]. See the hub for the other aspects (list, manage modal, submission, anti-spam, permissions & plan).

# Blog Comments — Status model & fields

## Purpose

This aspect documents the **data model behind a comment**: the stored fields, the `approved` / `pending` / `spam` status enum, how the initial status is decided, the manual-only transition rules, the difference between Delete and Mark-as-spam, and the cascade-delete behaviour that ties comments to their article and customer.

## Where to find it

These rules govern every comment in the **Blog Comment** queue (Sidebar → Marketing → Blog → Comment). The merchant changes status from [[marketing-blog-comment-list]] (bulk) or [[marketing-blog-comment-manage-modal]] (single).

## What the merchant can do here

The merchant controls a comment's lifecycle entirely through its `status`: approve it (publish), mark it spam (hide but keep), mark it pending (re-queue), or delete it (wipe). All transitions are manual — there is no automation.

## Settings & fields

### Comment fields

| Field | What it stores | Notes |
|-------|----------------|-------|
| **item_id** | The article ID the comment is attached to. | FK to `blogs_articles.id`, `ON DELETE CASCADE` — deleting the article wipes its comments. |
| **parent_id** | For threaded replies. | FK to `comment__articles_comments.id`, `ON DELETE CASCADE`. Not exposed in the admin UI today. |
| **name** | Guest commenter's name (when not logged in). | Required for guest comments; empty for logged-in customers (their name comes from their customer record). |
| **email** | Guest commenter's email. | Required for guest comments; empty for logged-in customers (their email comes from their customer record). Used for the gravatar. |
| **author_id** | FK to `customers.id`. | Set when the commenter is a logged-in customer. `ON DELETE CASCADE` — deleting the customer wipes their comments. |
| **comment** | The comment text. | Required. Max **1,000 characters**. Validation message: *"Comments can not be longer than 1000 characters"*. |
| **date_added** | Timestamp the comment was submitted. | Set automatically when the comment is created. |
| **status** | `approved` / `pending` / `spam`. | Initial value is decided by the parent category's `comments` setting. |
| **date_status** | Timestamp of last status change. | Updated when the merchant moves the comment between approved / pending / spam. |
| **admin_id** | FK to `admins.id`. | Records which admin last changed the status. `ON DELETE SET NULL`. |

## Business rules

### Initial status is decided at submission time by the parent category

When a visitor submits a comment, the platform looks up the parent blog's `comments` value:

- `automatic` → new comment is saved with `status=approved` immediately.
- `moderator` → new comment is saved with `status=pending`, invisible on the storefront until the merchant approves it here.
- `no` → submission is rejected outright with *"The comments for this post are disabled"*.

So this moderation queue only matters for categories with `moderator` (or for cleaning up spam under `automatic`). To change a category's policy, see [[marketing-blog-category]]. The article itself carries no comment policy. The submission-time validation chain is documented on [[marketing-blog-comment-submission]].

### Status transitions: manual, no automation

The merchant can move a comment between any pair of statuses via the bulk actions or the Manage modal:

- pending → approved (the typical "approve a queued comment").
- pending → spam (reject a queued spam comment).
- approved → spam (a posted comment turned out to be spam).
- spam → approved (false positive — bring it back).
- spam → pending (review later).

There is NO automatic transition. CloudCart does not learn from past spam classifications, does not maintain a per-IP block-list, and does not consult external spam services. The merchant moderates by hand. See [[marketing-blog-comment-anti-spam]].

### Delete vs spam

- **Delete** wipes the row permanently. Use for clearly malicious / illegal content the merchant doesn't want kept on file.
- **Mark as spam** keeps the row in the DB with `status=spam`, invisible on the storefront. Use for routine spam — keeping the record is useful for auditing volume or accidental restoration.

### Comments stay on cascade-delete

The `comment__articles_comments` table has `ON DELETE CASCADE` on both `item_id` (article) and `author_id` (customer). Consequence:

- Deleting an article wipes all its comments. The merchant doesn't need to clean up the comment queue first.
- Deleting a customer wipes their comments (GDPR-friendly side-effect, though [[apps-gdpr-requests]] explicitly handles this).
- Renaming an article does NOT touch its comments.

## Plan gates

Gated by `blog_comments` (the whole screen). Full mapping on [[marketing-blog-comment-permissions-plan]].

## How it works (verified against backend)

- **Storage** — Comments live in the `comment__articles_comments` table (per-store DB). No soft-deletes — a delete wipes the row permanently; "Mark as spam" keeps the row with `status='spam'`.
- **Initial status decided at submission** — When a visitor posts a comment, the platform reads the parent blog category's `comments` setting and stamps the new comment with `approved` (automatic), `pending` (moderator), or rejects the submission entirely (`no`).
- **Cascade behavior** — `item_id` (article FK) uses `ON DELETE CASCADE`; `author_id` (customer FK) uses `ON DELETE CASCADE`; `parent_id` (threaded reply FK) uses `ON DELETE CASCADE`; `admin_id` (which staff member last changed status) uses `ON DELETE SET NULL`.
- **No status automation** — All status transitions are manual via the admin UI / bulk actions.

## Related

- [[marketing-blog-comment]] — hub.
- [[marketing-blog-comment-submission]] — how a new comment gets its initial status; the validation chain.
- [[marketing-blog-comment-anti-spam]] — why transitions stay manual (no spam engine).
- [[marketing-blog-category]] — sets the `automatic` / `moderator` / `no` policy that seeds the initial status.
- [[apps-gdpr-requests]] — comment cascade-delete on customer deletion.
- [[blog-comment]] — entity page.
- [[blog-article]] — entity page; comments cascade-delete with the article.
- [[customers]] — logged-in commenters set `author_id`; deletion cascades.

## Open questions

No outstanding questions.
