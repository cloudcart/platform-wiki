---
type: feature
nav_path: "Marketing → Blog → Comment → List"
route_name: blog-comments
route_path: /admin/marketing-new/blog/comment
aliases: ["Blog comments list", "Comment list", "Comment queue list", "Comment moderation list", "Списък с коментари"]
tags: [marketing, blog, comments, moderation, content]
plan_gates: ["blog_comments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-comment]]. See the hub for the other aspects (manage modal, status model, submission, anti-spam, permissions & plan).

# Blog Comments — List screen

## Purpose

The **list screen** is the moderation queue surface itself: a table of every comment in the store with its commenter, excerpt, date, and status, plus the filters, search, bulk actions, and per-row delete that let the merchant triage at volume. This aspect documents the list page only — the per-comment editing UI lives on [[marketing-blog-comment-manage-modal]].

## Where to find it

Sidebar → **Marketing** → **Blog** → **Comment** (route name `blog-comments`, path `/admin/marketing-new/blog/comment`). Also reachable pre-filtered by article via the "Comments (N)" button on each [[marketing-blog-articles]] row.

## What the merchant can do here

On the list:

- See all comments with **User** (commenter name + email + gravatar), **Comment** (excerpt, truncated to 42 chars with "…"), **Date**, **Status** (Approved / Pending / Spam), and a **Delete** row action.
- Click a comment row's **Comment** text or **Status** chip to open the Manage modal (see [[marketing-blog-comment-manage-modal]]).
- Filter by:
  - **Article** (autocomplete from [[marketing-blog-articles]]).
  - **Blog** (autocomplete from [[marketing-blog-category]] — filters all comments on articles inside the chosen category).
  - **Status** (`approved` / `pending` / `spam`).
- Search by commenter name, email, comment text, or article name.
- Bulk actions (all POST to `/admin/api/core/blog/comments/status` with `{status, ids}` except Delete which DELETEs `/admin/api/core/blog/comments`):
  - **Approve** (icon `fa-light fa-thumbs-up`) — sets status to `approved`; toast *"Status updated"*.
  - **Mark as spam** (icon `fa-light fa-exclamation-triangle`) — sets status to `spam`; toast *"Status updated"*.
  - **Mark as pending** (icon `fa-light fa-clock`) — sets status to `pending`; toast *"Status updated"*.
  - **Delete** (icon `fa-light fa-trash-alt`) — confirms via the standard *"Caution: This action cannot be undone"* prompt; toast *"Removed successfully"*.

### What the merchant CANNOT do here

- **Edit** a comment's text — the merchant can only approve, mark spam, or delete it. There is no inline "fix typo" action.
- **Reply** to a comment from the admin panel — the admin has no UI to post replies. Replies come from visitors on the storefront.
- **See the source IP / browser fingerprint** of the commenter — these are not exposed in the admin (only commenter name, email, comment text, dates, status, and the admin who last changed status are stored).
- **Configure auto-spam filtering** — there is no built-in spam filter. Comments either pre-moderate (manual queue) or auto-publish (no filter). See [[marketing-blog-comment-anti-spam]] for the alternatives.
- **Manage comments from a third-party platform here** — when [[apps-disqus-comments]] or [[apps-facebook-comments]] is active on the storefront, comments are stored externally and not visible on this page. Existing native comments remain on file but become unreachable from the public site.

## Settings & fields

### List columns

| Column | What it shows |
|--------|----------------|
| **User** | Commenter's name + email (or full name of the logged-in customer with a link to their [[customers]] profile); gravatar avatar derived from the email. |
| **Comment** | Excerpt of the text (first 42 chars + "…"); click opens the Manage modal. |
| **Date** | When the comment was submitted, formatted in the store's date+time format. |
| **Status** | Pill: green "Approved" / yellow "Pending" / red "Spam"; click opens the Manage modal. |
| **Actions** | Trash icon — confirms then deletes. |

The underlying comment fields these columns read from (and their FK / cascade behaviour) are documented on [[marketing-blog-comment-status-model]].

## Business rules

- **Both Comment text and Status pill open the same Manage modal** — the Comment column is a `type: 'link'` cell with `handleClick`, and the Status pill is wired to a `handleStatus` callback; both set the row as the modal's active comment. See [[marketing-blog-comment-manage-modal]].
- **Delete is row-only.** The Manage modal has no Delete button — deletion is exclusively the trash icon on the row, behind its own confirm prompt. Delete wipes the row permanently; "Mark as spam" keeps it on file. See [[marketing-blog-comment-status-model]] for delete-vs-spam.
- **Bulk vs single share the same endpoints.** Bulk actions and the modal both POST status changes to the same `/admin/api/core/blog/comments/status` endpoint; the bulk toast is *"Status updated"* while the modal toast is *"Status changed successfully"*.
- **Pending-count nudge.** The list is the destination of the *"%n comments pending for approval"* count surfaced on the sidebar / dashboard / [[marketing-blog-articles]] header.

## Plan gates

Gated by `blog_comments` — an access gate; lower plans cannot reach this route. Full mapping on [[marketing-blog-comment-permissions-plan]].

## How it works (verified against backend)

The list reads from the per-store `comment__articles_comments` table. There are no soft-deletes: the row-level Delete issues a `DELETE` and removes the record permanently, whereas the status bulk actions only update `status` + `date_status` + `admin_id`. Filtering by Blog resolves the chosen category to its articles and matches comments whose `item_id` falls in that set.

## Related

- [[marketing-blog-comment]] — hub.
- [[marketing-blog-comment-manage-modal]] — opened from the Comment text or Status pill.
- [[marketing-blog-articles]] — comments attach to articles; inline "Comments (N)" link lands here pre-filtered.
- [[marketing-blog-category]] — the Blog filter resolves to articles in the chosen category.
- [[customers]] — logged-in commenters link to their profile from the User column.

## Open questions

No outstanding questions.
