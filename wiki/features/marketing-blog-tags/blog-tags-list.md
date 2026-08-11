---
type: feature
nav_path: "Marketing → Blog → Tags → List & modal"
route_name: blog-tags
route_path: /admin/marketing-new/blog/tags
aliases: ["Blog tags list", "Add tag", "Edit tag", "Blog tag modal", "Tag list columns", "Списък с тагове на блог", "Добавяне на таг"]
tags: [marketing, blog, tags, taxonomy, content]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---

> Part of [[marketing-blog-tags]]. See the hub for the other aspects (lifecycle & sanitization, storefront & SEO, API/plan/permissions).

# Blog Tags — List & modal

## Purpose

This is the **central admin screen** where the merchant sees every blog tag in one list and manages it directly — create, rename, search, and delete tags **without** opening individual articles. This is the operational heart of the tag taxonomy: a flat, free-form list of labels attached to [[marketing-blog-articles]] alongside each article's required blog category. Unlike [[products-tags]] (which has no central admin page and is only edited from per-product editors), blog tags get this dedicated management list.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Tags**.

Route name `blog-tags`; path `/admin/marketing-new/blog/tags`; component `MarketingBlogTagsPage`. Header icon is the tag icon (`far fa-tag`). The breadcrumb reads "Marketing → Article tags".

## What the merchant can do here

- See all blog tags with their **Name**, **Articles** count (how many articles carry this tag), and **Delete** row action.
- Click **+ Add tag** to open the create modal. Type a tag name and **Save** — the tag is created in the blog-tags list.
- Click any row's **Name** to open the edit modal and rename the tag.
- Click the **Articles (N)** button to jump to [[marketing-blog-articles]] pre-filtered by this tag (`?filters[tags]=<id>`).
- Search tags by name (table search box).
- **Bulk-delete** selected tags.

### Per-row Articles button — disabled at zero

The **Articles (N)** button uses `btnDisabled: (row) => !row.items_count` — when the tag has zero articles attached, the button is rendered but visually disabled (greyed out). Clicking it is a no-op. This protects the merchant from navigating to an empty `?filters[tags]=<id>` listing.

### Bulk-delete bottom-row repaging

After a successful bulk delete, the table tries to stay on the current page. If the current page is now empty AND there's a `next_page_url`, it refetches the same page (the next page's data slides into view). If the page is empty AND there's no next page AND `page > 1`, it auto-decrements to `page-1` and refetches. Otherwise just refetches in place. So the merchant never lands on a blank page after deleting the last row.

### What the merchant CANNOT do here

- Set per-tag SEO metadata — tags only carry a `tag` name and an auto-derived `url_handle`. No description, no SEO title, no per-tag image. (Compare with [[marketing-blog-category]] which has full SEO fields.) See [[blog-tags-storefront-seo]].
- Build a tag hierarchy — tags are FLAT (the table has no parent column).
- Assign tags to articles from this page — assignment happens in the [[marketing-blog-articles]] editor's Tags multi-select.
- **Merge two tags** into one with article reassignment — there is no merge action. Merging today requires editing each affected article to switch tag, then deleting the unused tag.
- See storefront-side metrics — clicks / views per tag are not displayed (use [[analytics]] for traffic).

## Settings & fields

### Add / Edit modal (`CcConfirmModal`)

Title is *"Add tag"* on create, *"Edit tag"* on edit.

- **Tag name** (`CcInput`) — required, auto-focused on mount (`focus-on-mount=true`). The modal's **Save** button (`yes`) is disabled until the name is non-empty (`disabled-confirm` bound to `!tag.tag`); the **Cancel** button (`no`) closes without saving.
- Closing the modal (via Cancel or backdrop) clears any inline validation errors and resets the local tag state — so re-opening the modal starts with a fresh form.
- Success toast: *"Saved successfully"*.

### Tag fields

| Field | Validation | Notes |
|-------|------------|-------|
| **Tag name** (`tag`) | Required. String, 2 ≤ length ≤ 191. **Unique** in the blog-tags list. | *"Tag name is required"* / *"Tag name is too long"* / *"Tag name is too short"* / *"Tag name already exists"*. |
| **URL handle** (`url_handle`) | Auto-derived from the tag name via the `UrlHandle` trait. | Not exposed in the modal; computed automatically. Storefront URL: `/blog/tag/<url_handle>`. |

### List columns

| Column | What it shows |
|--------|----------------|
| **Name** | Tag text; click opens the edit modal. |
| **Articles** | Button "Articles (N)" — disabled when N=0; click jumps to [[marketing-blog-articles]] filtered by `filters[tags]=<id>`. |
| **Actions** | Trash icon — confirms then deletes the tag and its junction rows. |

## Business rules

- **The modal only validates name length (2-191) + uniqueness.** Per-article caps (100 tags/article, 191 chars/tag) live in the article editor, not on this page — see [[blog-tags-lifecycle]].
- **Both creation paths land in the same list.** The "+ Add tag" button is for tags the merchant wants pre-created (e.g. planned topics ahead of writing the articles); the more common path is auto-create from the article editor — see [[blog-tags-lifecycle]].
- **Rename uses PATCH, not POST** — tags are the exception versus articles. The endpoint surface is documented on [[blog-tags-api-permissions]].
- **No 301 redirect on rename or delete** — renaming or deleting a tag silently breaks inbound links to the old `/blog/tag/<old-slug>` URL. See [[blog-tags-storefront-seo]].

## Related

- [[marketing-blog-tags]] — hub.
- [[marketing-blog-articles]] — tags attach to articles via the editor's multi-select.
- [[marketing-blog-category]] — orthogonal hierarchy (one category per article + many tags).
- [[products-tags]] — sister concept on products (different table, different semantics).
- [[blog-tag]] — entity page.
- [[analytics]] — storefront traffic (not surfaced on this page).

## Open questions

No outstanding questions.
