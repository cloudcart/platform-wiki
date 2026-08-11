---
type: feature
nav_path: "Marketing → Blog → Articles → Add / Edit"
route_name: blog-articles-edit
route_path: /admin/marketing-new/blog/articles/edit/:id
aliases: ["Blog article editor", "Add article", "Edit article", "Article editor", "Редактор на статия", "Нова статия", "Редакция на статия"]
tags: [marketing, blog, content, articles, editor]
plan_gates: ["blog_articles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-blog-articles]]. See the hub for the other aspects (list, CSV import, rules, storefront visibility, API).

# Blog Articles — Add / Edit editor

## Purpose

The article editor is the two-column form where the merchant writes the long-form content — title, rich-text body, SEO metadata, cover image, author, blog category, tags — that will appear at `/article/<slug>` on the storefront once published. Add (`blog-articles-add`) and Edit (`blog-articles-edit`) share the same screen; the only differences are pre-population on edit and the slug-locking behaviour described below.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Articles** → **+ Add article** (Add) or click any row in the list (Edit).

Routes:

| Label | Route name | Route path |
|-------|------------|------------|
| Add | `blog-articles-add` | `/admin/marketing-new/blog/articles/add` |
| Edit | `blog-articles-edit` | `/admin/marketing-new/blog/articles/edit/:id` |

## What the merchant can do here

A two-column grid.

**Main column:**

- **Article title** card — Title input. Typing live-updates the `url_handle` (only auto-syncs on new articles — locked after first save).
- **Content** card — rich-text editor. Accepts pasted/dropped images; external `<img src>` URLs are mirrored into the store's media library in the background.
- **Advanced settings** card (expandable, default-expanded) — three subfields (SEO title, SEO description, URL handle), `/article/` prefix preview and Google-SERP preview.

**Aside column** — four stacked cards:

- **Author** — searchable dropdown of the store's admin users. Pre-populated with the article's current author on edit.
- **Blog category** — dropdown + **"+ Create category"** inline link that opens the same category-create modal as the Categories list page, IN-PLACE. On create, the new category is auto-selected — the merchant never leaves the editor.
- **Cover image** — upload with a separate remove action (only on existing articles).
- **Tags** — free-text chips with autocomplete from existing tags. Typing a new tag and pressing Enter adds it to the chip-list; saving auto-creates any tags not yet in the system.

**Sticky save footer** — Save button + dirty-form detection. On success: create returns to [[blog-articles-list]]; edit updates the record in place. The editor always saves with `active='yes'` (see business rule below).

## Settings & fields

### Article fields

| Field | Validation | Notes |
|-------|------------|-------|
| **Title** (`name`) | Required. 3 ≤ length ≤ 191 chars. | *"Name is required"* / *"Name is too long"* / *"Name is too short"*. Drives auto-slug. |
| **URL handle** (`url_handle`) | Auto-derived from title; overrideable. Storefront URL becomes `/article/<url_handle>`. | Unique per store. Renaming creates a 301 redirect from the old handle (see [[marketing-seo-301-redirects]]). |
| **Content** (`content`) | String. Effectively unlimited length. | Stored as HTML via the rich-text editor. Inline images in the editor are uploaded into CloudCart's media library. |
| **Author** (`author_id`) | Required. Must be an existing admin user. | *"Author is required"* / *"Author does not exist"*. Picked from the store's admin users — see [[settings-staff]]. |
| **Blog category** (`blog_id`) | Required. Must be an existing blog category. | *"Blog is required"* / *"Blog does not exist"*. Picked from the blog categories list. |
| **Tags** (`tags[]`) | Array of strings. Up to **100 tags per article**, each ≤ **191 characters**. | Auto-creates new tags when not in [[marketing-blog-tags]] yet. |
| **Cover image** (`image`) | Optional. Image file with a separate remove action. | Thumb shown at `150x150` in list. |
| **SEO title** (`seo_title`) | String, max 191. | Maps to the storefront article page title. If empty, falls back to the article name. |
| **SEO description** (`seo_description`) | String, max 191. | Maps to the storefront meta description. |
| **Active** (`active`) | `yes` / `no`. The editor sets `active=yes` on save. | The Published toggle in the [[blog-articles-list]] flips this. |
| **Publish date** (`publish_date`) | Optional datetime. | Legacy field, not exposed in the modern editor, but **DOES still gate storefront visibility** — see [[blog-articles-storefront-visibility]]. Only reachable via the legacy editor or [[blog-articles-api]]. |

### What the merchant CANNOT do here

- Set a **publish date in the future** from the modern editor — articles are immediately live when toggled Active. To schedule, see [[blog-articles-storefront-visibility]] + [[blog-articles-api]].
- Choose **multiple authors** — each article has exactly one author from [[settings-staff]].
- Write articles **without a blog category** — at least one [[marketing-blog-category]] must exist before the first article.
- Bulk-edit article bodies — bulk-edit on the list page is limited to Publish / Unpublish / Delete.

## Business rules

### Title-driven slug + 301 history

While the slug field is auto-syncing, the URL handle is regenerated from the title. Once the article is saved, **editing the title later does NOT auto-rewrite the slug** (that field locks after first save). If the merchant then manually edits the URL handle on an existing article, the platform records a 301 redirect from the OLD slug to the new one — protecting external links and Google's index when the article is renamed. See [[marketing-seo-301-redirects]].

### Inline images in content → uploaded into CloudCart media (async)

Pasting or dragging an image into the rich-text editor does NOT block the save. On save, a background task downloads each external `<img src="...">` in the content, uploads it to the store's media storage, and rewrites the URL to a CloudCart-hosted one. Until it finishes, the article briefly references the external URL on the storefront. The task re-runs only when the content changes; failures are silently swallowed. Once mirrored, the article never references external image URLs — protecting content if the original host disappears. See [[background-queue-inventory]].

### Cover image: separate from inline content images, uploaded synchronously

The **featured cover image** (`image` field) is a separate upload — displayed as a `150x150` thumbnail in the [[blog-articles-list]] view, on the storefront article page (header banner) and blog listing card, and in any RSS / sitemap export. Unlike inline-image mirroring, cover-image upload is **synchronous**. Removing the cover image is a separate action from saving the article.

### Tag chips auto-create on save

Typing a new tag in the **Tags** chip-list and pressing Enter adds it locally; saving the article auto-creates the tag in [[marketing-blog-tags]]. See [[blog-articles-rules]] for the 100-tags-per-article and 191-chars-per-tag caps.

### Content size: effectively unlimited

The article content has effectively no length limit; in practice it is limited by the rich-text editor's UI performance and the inline-image upload pipeline, not by content length.

### First-save defaults `active='yes'`

The editor always submits `active='yes'` on save, whether create or edit. To create an article in draft state, the merchant flips the Published toggle on the [[blog-articles-list]] after save.

## Related

- [[marketing-blog-articles]] — hub.
- [[blog-articles-list]] — the list screen the editor opens from and returns to.
- [[blog-articles-rules]] — the server-side validation rules enforced on Save.
- [[blog-articles-storefront-visibility]] — what `active` and `publish_date` mean on the storefront.
- [[blog-articles-api]] — the same fields exposed via JSON-API v2.
- [[marketing-blog-category]] — required parent; selectable + creatable inline from the editor.
- [[marketing-blog-tags]] — auto-creating tag list.
- [[marketing-seo-301-redirects]] — auto-created when the URL handle changes.
- [[marketing-seo-meta]] — SEO title + description that map to the storefront `<title>` + `<meta description>`.
- [[settings-staff]] — author dropdown source.
- [[background-queue-inventory]] — the background task that mirrors inline images.

## Open questions

No outstanding questions for the editor surface.
