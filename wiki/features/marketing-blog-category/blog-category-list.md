---
type: feature
nav_path: "Marketing → Blog → Category → List & modal"
route_name: blog-categories
route_path: /admin/marketing-new/blog/category
aliases: ["Blog category list", "Blog categories list", "Add blog category", "Edit blog category", "Blog category modal", "Списък категории на блог"]
tags: [marketing, blog, content, categories, taxonomy]
plan_gates: ["blog_categories"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-blog-category]]. See the hub for the other aspects (comment policy, lifecycle, SEO, API/plan/permissions).

# Blog Categories — List screen & create/edit modal

## Purpose

The **list screen** is the entry point for managing blog categories, and the **shared create/edit modal** is where the merchant actually fills in a category's fields. There is no separate Add / Edit screen — both create and edit happen inside the same modal, opened from the list or from the Article editor. This aspect documents the list-page surface and the modal mechanics; the per-field rules that aren't UI-mechanics live on sibling aspects ([[blog-category-comment-policy]], [[blog-category-seo]]).

## Where to find it

Sidebar → **Marketing** → **Blog** → **Category**.

Route name `blog-categories`; path `/admin/marketing-new/blog/category`. Header icon is the typewriter.

## What the merchant can do here

- See a list of all blog categories with **Name** (title + thumbnail), **Created at**, **Updated at**, **Comments** policy (Automatic / Comments need approval / Turn off comments / Modified), and a **Delete** row action.
- Click **+ Add blog category** to open the create modal.
- Click any category row's name to open the edit modal.
- Filter the list by **Comments** policy (`automatic` / `moderator` / `no`).
- Search by category name (table search box).
- **Bulk-delete** selected categories.

## Settings & fields

### List columns and filter labels

The list's "Comments" filter offers three labels (the comment-policy semantics live on [[blog-category-comment-policy]]):

| Filter label | Sets |
|---|---|
| **Modified** | `comments=moderator` (pre-moderation queue). |
| **Not modified** | `comments=no` (comments off). |
| **Automatic** | `comments=automatic` (auto-publish). |

The list is sorted **newest-first** by default; the merchant cannot drag-reorder.

### Create / Edit modal

In the **Create / Edit modal** (title flips between *"Add blog category"* and *"Edit blog category"*):

- **Modal shell** — wraps the standard modal component with a per-modal save function bound to its footer save/cancel buttons. The modal is disabled (saves blocked) while either the create OR update mutation is pending.
- **Client-side validation** uses a Zod schema: `name`, `seo_description`, `seo_title` all required (min 1 char each) — but the modal auto-fills empty SEO fields with the category name BEFORE the Zod check (see [[blog-category-seo]]), so in practice only `name` ever fails Zod. Failed validation throws into the error store so per-field errors render inline; the modal scrolls/highlights the offending field.
- **Blog category title** card → `name` text input (required, 3-191 chars). On NEW categories the title also auto-derives the URL handle (locked on edit — see [[blog-category-seo]]).
- **Comments settings** card → a switch + radio group whose combined behaviour is documented on [[blog-category-comment-policy]].
- **Blog category image** card → cover-image uploader, with delete endpoint `/admin/api/core/blog/categories/{id}/delete-image` (only present on existing categories). On delete inside the modal, the parent listing fires a `removeImage` event so the row's thumbnail clears live.
- **Advanced settings** card (expandable, default-expanded) → SEO title, SEO description, and URL handle — see [[blog-category-seo]].

### The modal is shared across two entry points

1. **Categories list page** (this screen) — primary place to manage categories.
2. **Article editor** ([[marketing-blog-articles]]) — the "+ Create category" link inside the Article editor's Blog category card opens the SAME modal IN-PLACE. On success, the newly-created category is automatically selected in the article's category dropdown — the merchant doesn't leave the article editor.

## Business rules

### What the merchant CANNOT do from this screen

- Build a **hierarchy** — blog categories are FLAT (single level). There is no parent / child relationship. See [[blog-category-lifecycle]].
- **Reorder** categories — the list is sorted newest-first; no drag-reorder. Storefront listing order follows the same ordering.
- Set per-category **plan-tier gates** — blog is enabled on all plans (the count cap is plan-driven; see [[blog-category-api-plan-permissions]]).
- Manage **comment moderators** per category — moderation uses the global admin pool with the right permission ([[settings-staff]]).
- Delete a category that has articles **without consequences** — articles survive as orphaned (uncategorised); full delete behaviour on [[blog-category-lifecycle]].

### Title field

The **Title** (`name`) is required, 3 ≤ length ≤ 191 chars, with error strings *"Name is required"* / *"Name is too long"* / *"Name is too short"*. It is the field that drives the auto-slug ([[blog-category-seo]]) and the SEO fallback ([[blog-category-seo]]).

## Related

- [[marketing-blog-category]] — hub.
- [[blog-category-comment-policy]] — the comment switch + radio inside the modal.
- [[blog-category-seo]] — the SEO + URL-handle fields in the Advanced settings card.
- [[blog-category-lifecycle]] — flat hierarchy + delete behaviour referenced from the list.
- [[marketing-blog-articles]] — the Article editor that shares this modal in-place.
- [[settings-staff]] — admin permissions / moderator pool.

## Open questions

No outstanding questions.
