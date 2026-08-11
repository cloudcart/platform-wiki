---
type: feature
nav_path: "Marketing → Blog → Articles → List"
route_name: blog-articles-list
route_path: /admin/marketing-new/blog/articles
aliases: ["Blog articles list", "Articles list", "Posts list", "Списък със статии", "Блог статии списък"]
tags: [marketing, blog, content, articles, list]
plan_gates: ["blog_articles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-blog-articles]]. See the hub for the other aspects (editor, CSV import, rules, storefront visibility, API).

# Blog Articles — List screen

## Purpose

The **list screen** is the entry point for the merchant's blog: it shows every article in the store, exposes the header actions (create, pending-comments shortcut, CSV import), and offers per-row publish / unpublish / delete plus bulk operations. This aspect documents the list-page surface only — the editor lives on [[blog-articles-editor]], and the CSV-import wizard on [[blog-articles-csv-import]].

## Where to find it

Sidebar → **Marketing** → **Blog** → **Articles**.

Route: `/admin/marketing-new/blog/articles` (route name `blog-articles-list`). Header icon: the typewriter icon.

## What the merchant can do here

- The page header carries up to three action buttons:
  - **Add via CSV** (default-variant, icon `far fa-file-csv`) — **only rendered when the `blog_csv_import` app is installed** (read from `useApplicationsStore`). Opens the 3-stage wizard described in [[blog-articles-csv-import]].
  - **Pending Comments (N)** (secondary-variant, icon `far fa-comments`) — always shown. The badge `(N)` reads `articles.meta.pending_comments`; clicking navigates to [[marketing-blog-comment]] pre-filtered by `filters[status]=pending`.
  - **+ Add article (N)** (primary-variant) — the badge `(N)` reads `articles.total` so the merchant sees their current article count next to the create button. Routes to `blog-articles-add`.
- Click **+ Add article** to open the article editor — see [[blog-articles-editor]].
- See a table of all articles with **Name** (title + cover thumbnail + blog category badge), **Comment** button (count of comments — clicks through to [[marketing-blog-comment]] pre-filtered by article), **Published** toggle (publish / unpublish inline), and a **Delete** row action.
- Search articles by name (via the table's search box).
- Filter the table by **Active** (Yes / No), **Has blog** (Yes / No — does the article belong to any blog category), **Tagged with** (autocomplete from [[marketing-blog-tags]]), or **Blog** (the article's category, autocomplete from [[marketing-blog-category]]).
- **Bulk-publish** / **Bulk-unpublish** selected rows.
- **Bulk-delete** selected rows.
- See a banner with the total **pending comments count** (*"%n comments pending for approval"*) — clicks through to the moderation queue.

## Settings & fields

### Sub-screens (deep links)

| Label | Route name | Route path |
|-------|------------|------------|
| List | `blog-articles-list` | `/admin/marketing-new/blog/articles` |
| Add | `blog-articles-add` | `/admin/marketing-new/blog/articles/add` |
| Edit | `blog-articles-edit` | `/admin/marketing-new/blog/articles/edit/:id` |

### List columns

| Column | What it shows |
|--------|----------------|
| **Name** | Article title with cover thumbnail (`150x150`); blog category chip beneath the title; click navigates to edit. |
| **Comment** | Button labelled *"Comments (N)"*; disabled when N=0; click jumps to [[marketing-blog-comment]] pre-filtered by `article_id`. |
| **Published** | Toggle switch — flips `active` between `yes` and `no` inline. |
| **Actions** | Trash icon — confirms then deletes the article. |

### Filters

| Filter | Values | Source |
|--------|--------|--------|
| **Active** | Yes / No | Filters by the article's `active` flag. |
| **Has blog** | Yes / No | Whether the article belongs to any blog category. |
| **Tagged with** | Autocomplete | From the merchant's tag list — see [[marketing-blog-tags]]. |
| **Blog** | Autocomplete | The article's category — see [[marketing-blog-category]]. |

## Business rules

- **Bulk-publish / bulk-unpublish endpoint** — Bulk publish / unpublish uses a single endpoint (`POST /admin/api/core/blog/articles/update-status`) with body `{ids: [], status: yes|no}`. Validated as: `ids` required, array, all IDs must exist in `blogs_articles`; `status` required, exactly `yes` or `no`. Mass-flips `active` in one UPDATE — no per-row hooks fire. (verify)
- **Bulk-delete** — Multi-select + Delete confirms then removes the rows; deletion is hard (no soft-delete on articles), so the cascade described in [[blog-articles-rules]] applies (comments wiped via FK).
- **CSV import button is app-gated** — Until the `blog_csv_import` app is installed, the **Add via CSV** action is hidden from the page header entirely. See [[apps-blog-csv-import]] + [[blog-articles-csv-import]].
- **Inline Published toggle** — Flipping the toggle issues the same `update-status` endpoint with a single ID; no full save, no editor open required.
- **Pending-comments banner** — Reads `articles.meta.pending_comments` aggregated across every article in the store; clicking lands on [[marketing-blog-comment]] with `filters[status]=pending` already applied.

## Related

- [[marketing-blog-articles]] — hub.
- [[blog-articles-editor]] — the Add / Edit screen opened from **+ Add article** or by clicking a row.
- [[blog-articles-csv-import]] — 3-step CSV-import wizard reached from **Add via CSV**.
- [[blog-articles-rules]] — server-side validation + business rules behind save + delete.
- [[marketing-blog-category]] — required parent of every article; surfaces in the Blog filter.
- [[marketing-blog-tags]] — surfaces in the Tagged-with filter.
- [[marketing-blog-comment]] — moderation queue reached from the pending-comments banner + the per-row Comment button.
- [[apps-blog-csv-import]] — the app that unlocks the **Add via CSV** action.

## Open questions

No outstanding questions for the list surface.
