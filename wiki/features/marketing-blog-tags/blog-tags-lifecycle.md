---
type: feature
nav_path: "Marketing → Blog → Tags → Lifecycle & sanitization"
route_name: blog-tags
route_path: /admin/marketing-new/blog/tags
aliases: ["Blog tag auto-create", "Blog tag lowercase", "Blog tag caps", "Blog tag delete cascade", "Blog tag sanitization", "Автоматично създаване на тагове", "Изтриване на таг"]
tags: [marketing, blog, tags, taxonomy, content]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---

> Part of [[marketing-blog-tags]]. See the hub for the other aspects (list & modal, storefront & SEO, API/plan/permissions).

# Blog Tags — Lifecycle & sanitization

## Purpose

This aspect documents how blog tags come into existence, how their names are cleaned and normalised, what caps apply, and what happens when a tag is deleted. Most tags are NOT born from the central [[blog-tags-list]] "+ Add tag" button — they are auto-created the moment a merchant types a new tag into the [[marketing-blog-articles]] editor. Understanding this flow explains why tags appear in lowercase, why duplicates collapse, and why deleting a tag is safe for the articles that carried it.

## Where to find it

This behaviour spans two screens (no dedicated screen of its own):

- Sidebar → **Marketing** → **Blog** → **Tags** (`/admin/marketing-new/blog/tags`) — the "+ Add tag" pre-create path + delete + bulk-delete.
- Sidebar → **Marketing** → **Blog** → **Articles** ([[marketing-blog-articles]]) — the Tags multi-select that auto-creates tags on save, and where the per-article caps are enforced.

## What the merchant can do here

- Pre-create a tag from [[blog-tags-list]] (for planned topics) — or let it auto-create when first typed into an article.
- Type new tags freely in the article editor's Tags multi-select; saving the article creates any missing tags automatically.
- Delete a single tag (row trash icon) or bulk-delete a selection — articles previously tagged survive, they just lose that tag.

## Settings & fields

The lifecycle is governed by these validation and normalisation rules (no merchant-facing toggles):

| Rule | Where enforced | Effect |
|------|----------------|--------|
| Name length 2-191 + uniqueness | [[blog-tags-list]] modal | Rejects too-short / too-long / duplicate names. |
| Up to **100 tags per article** | Article editor | Exceed → *"Maximum 100"* on save. |
| Each tag ≤ **191 chars** | Article editor | Exceed → *"&lt;tag-name&gt; maximum length is 191"*. |
| Lowercase normalisation | Both paths | `Summer-2026` → `summer-2026`. |
| Wildcard stripping | Both paths | `%` and `_` silently removed. |

## Business rules

### Tags are auto-created from the article editor

The most common way tags appear is the article-editor flow. When the merchant types a new tag into the [[marketing-blog-articles]] Tags multi-select and saves the article, the platform:

1. Splits the typed string on commas.
2. Trims + de-duplicates case-insensitively.
3. For each tag NOT already in the blog-tags list, creates it lowercase.
4. Inserts the article-to-tag junction row.

So the "+ Add tag" button on [[blog-tags-list]] is for tags the merchant wants pre-created (perhaps to set up planned topics ahead of writing the articles). Both paths land in the same list.

### Lowercase storage

Tag inserts are lowercased before being saved. So `Summer-2026`, `summer-2026`, and `SUMMER-2026` all resolve to one tag stored as `summer-2026`. The merchant can SEE the displayed name in the original casing only for tags they re-edit; auto-created tags are stored lowercase.

### Uniqueness + race-safe insert

The `tag` name has a unique constraint. The platform safely handles the race condition where two parallel article saves try to auto-create the same tag at the same moment — one wins, the other reuses the existing tag.

### Sanitised input

The trait strips:

- Whitespace (each comma-separated piece is `trim`-ed).
- Empty strings (filtered out before insert).
- `%` and `_` (filtered — these are SQL LIKE wildcards that would break filter queries).

### Limits enforced from the article editor (not from the central page)

The [[blog-tags-list]] "+ Add tag" modal only validates name length (2-191 chars) and uniqueness. The per-article caps live in the article editor:

- **Up to 100 tags per article** — exceed and the save throws *"Maximum 100"*.
- **Each tag ≤ 191 chars** — exceed and it throws *"&lt;tag-name&gt; maximum length is 191"*.
- Tags `%` and `_` are silently filtered (SQL wildcard hygiene).

### Delete cascade

Deleting a tag wipes both the tag definition AND the related article-to-tag junction rows (`ON DELETE CASCADE`). Articles previously tagged with it survive — they just lose that tag from their tag-list. The storefront's tag page returns 404 (or redirects to `/blog/`) after the tag is gone — and note there is **no 301 redirect** on delete (see [[blog-tags-storefront-seo]]).

### Bulk delete + page-recompute

Bulk delete validates that all submitted IDs exist, then deletes them in one batch. On the front-end the page re-runs the listing query — if the current page is empty after deletion, it auto-falls-back to the previous page (the repaging logic is detailed on [[blog-tags-list]]).

## Related

- [[marketing-blog-tags]] — hub.
- [[marketing-blog-articles]] — the editor where tags auto-create + where per-article caps are enforced.
- [[blog-tag]] — entity page.
- [[blog-article]] — entity page.

## Open questions

No outstanding questions.
