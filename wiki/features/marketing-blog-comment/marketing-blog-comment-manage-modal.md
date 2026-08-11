---
type: feature
nav_path: "Marketing → Blog → Comment → Manage modal"
route_name: blog-comments
route_path: /admin/marketing-new/blog/comment
aliases: ["Manage comment modal", "Comment manage modal", "Comment status modal", "Управление на коментар"]
tags: [marketing, blog, comments, moderation, content]
plan_gates: ["blog_comments"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-blog-comment]]. See the hub for the other aspects (list, status model, submission, anti-spam, permissions & plan).

# Blog Comments — Manage modal

## Purpose

The **Manage comment** modal is the per-comment moderation surface: it shows the full comment text and offers a **status-aware button set** so the merchant can approve, reject (spam), or rescue a single comment in one click. It is the single-comment counterpart to the bulk actions on [[marketing-blog-comment-list]].

## Where to find it

The modal (a `CcConfirmModal` titled *"Manage comment"*) opens from the [[marketing-blog-comment-list]] screen. It has **two click-targets per row**: clicking the truncated Comment text (table column `type: 'link'` with `handleClick`) OR clicking the Status pill (`handleStatus` callback wired the same way). Both set the local `comment.value = row` and flip `commentModal = true`.

## What the merchant can do here

- See the **full comment text** rendered as HTML, prefaced by *"%name added a comment"* with the commenter's name interpolated.
- **Approve, mark spam, or rescue** the comment via the conditional buttons below. The cancel button (variant `ghost`) closes the modal without changes.
- There is **no Delete button** in the modal — deletion uses the trash icon on the row itself (separate confirm prompt). See [[marketing-blog-comment-list]].

The modal's button set is **status-aware** — buttons appear conditionally based on the comment's current status:

| Comment status | Primary button (footer, danger/primary variant) | Secondary button (header `#action` slot) |
|---|---|---|
| `pending` | **Mark as spam** (variant `danger`) | **Approve comment** (variant `primary`) — shown only for `pending` rows so the merchant can one-click approve |
| `approved` | **Mark as spam** (variant `danger`) | (none) |
| `spam` | **Approve comment** (variant `primary`) | (none) |

## Settings & fields

The modal mutates the same comment fields documented on [[marketing-blog-comment-status-model]]: a status change writes `status`, `date_status`, and `admin_id`. The modal reads `comment.status` to decide which buttons render and what the primary-button label / variant should be.

## Business rules

- **The primary button computes the opposite-status transition dynamically.** For `approved` / `pending` rows, clicking the primary button moves the comment to `spam`; for `spam` rows, it moves to `approved`.
- **The primary button's variant changes** with the destructive-vs-restorative nature of the transition: `danger` (red) when moving `approved`/`pending` → `spam`; `primary` (purple) when moving `spam` → `approved`. So the merchant can tell at a glance whether they're rescuing or rejecting the comment.
- **The label string is computed** from `tt(['approved','pending'].includes(comment.status) ? 'Mark as spam' : 'Approve comment')` — the modal's button literally changes label depending on which status the row currently has when opened.
- **The status-change handler accepts an optional explicit `status` argument.** The **Approve comment** secondary button (only shown for pending rows) calls `handleStatusChange('approved')`; the primary footer button calls `handleStatusChange` with no argument and the function computes the opposite-status transition automatically.
- **Submit-loader.** The `submit-loader` binding on `CcConfirmModal` shows a spinner inside the primary button and locks both Approve buttons while the status mutation is in flight.
- **On success:** toast *"Status changed successfully"*; the modal closes and the row's status pill updates inline.

## Plan gates

Gated by `blog_comments` (the whole screen). Full mapping on [[marketing-blog-comment-permissions-plan]].

## How it works (verified against backend)

The modal POSTs the resolved status to the same `/admin/api/core/blog/comments/status` endpoint the bulk actions use, passing `{status, ids}` with a single ID. The backend stamps `date_status` and the acting `admin_id`. Because the primary button derives its target status from the current `comment.status` at open time, the modal never needs a separate "set to X" control beyond the optional explicit-status approve shortcut for pending rows.

## Related

- [[marketing-blog-comment]] — hub.
- [[marketing-blog-comment-list]] — the list the modal opens from; Delete lives there, not here.
- [[marketing-blog-comment-status-model]] — the status enum and field set the modal mutates.

## Open questions

No outstanding questions.
