---
type: feature
nav_path: "Apps → Blog CSV Import"
route_name: apps.blog_csv_import.overview
route_path: /admin/apps/blog_csv_import
aliases: ["Blog CSV Import", "Blog import", "Article bulk import", "no enable disable button", "app has no active toggle"]
tags: [apps, imports, csv, blog, content, plan-gated]
plan_gates: ["blog_articles"]
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# Blog CSV Import (bulk blog article import)

## Purpose

**Blog CSV Import** integration — same pattern as [[apps-csv-import]] but for **blog articles** instead of products. Imports article content (title, body, slug, tags, category, author, publish date, featured image URL) from a CSV file.

Used for:
- Migrating a blog from WordPress / Ghost / Medium to CloudCart.
- Bulk-publishing AI-generated articles (writer produces 100 articles in a spreadsheet → bulk import).
- Periodic content imports from external content services.

Two sub-pages: List + Progress.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> There is nothing to keep "running" either — each import is a task the merchant starts by hand and it ends on its own.

## Where to find it

Sidebar → Apps → install → **Blog CSV Import**.

| Sub-page | Purpose |
|----------|---------|
| List | All blog import tasks. |
| Progress ([[apps-blog-csv-import-progress]]) | Per-task progress detail. |

## What the merchant can do here

- Upload a CSV containing blog article data.
- Map CSV columns to blog-article fields.
- Track import progress.

### What the merchant CANNOT do here
- Use without [[marketing-blog-articles]] feature active.
- Run multiple concurrent imports (same `working` lock pattern).

## Settings & fields

App key: `blog_csv_import`.

Key methods:
- `working: bool` — concurrent-import lock.
- `setWorking(bool $status)` — sets the lock state.

## Business rules

### Same lock pattern as CSV Import

Only ONE blog import runs at a time. Prevents DB contention + ensures predictable order.

### Articles map to standard blog fields

Typical CSV columns:
- Title.
- Slug / URL handle.
- Body (HTML or Markdown).
- Excerpt.
- Tags (comma-separated).
- Category.
- Author.
- Publish date.
- Featured image URL.
- SEO fields (meta title, meta description).

### Permission

Standard apps permission scope.

## Plan gates

Blog CSV Import has no dedicated plan-feature key — but every article created by an import passes through the underlying blog-article create gate (see [[plan-gates]], [[plan-vs-feature-pack]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `blog_articles` | Numeric (per-plan max blog articles) | The same numeric quota that gates manual blog-article creation on [[marketing-blog-articles]]. Each row in the CSV that produces a NEW article (the importer is create-only — see "Duplicate handling: SKIP" above) counts against the cap. Hitting the cap mid-import finalises the task with the "interrupted-by-plan-quota" failure message documented for [[apps-csv-import]]. |

The blog-category create gate (`blog_categories`) ALSO applies via the auto-create behaviour — when the CSV references a blog category that doesn't exist, CloudCart creates it, and the create call passes through the same `blog_categories` numeric cap as manual category creation. Upsell flows route through [[plan-features]]; feature packs extend numeric caps per [[plan-vs-feature-pack]].

## Related

- [[apps]] — App Store.
- [[apps-csv-import]] — sister CSV import for products.
- [[marketing-blog-articles]] — articles created.
- [[marketing-blog-category]] — categories referenced.
- [[marketing-blog-tags]] — tags created automatically (verify).
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.
- [[background-queue-inventory]] — catalogue of all background processes; covers the async blog-article CSV-import job and how to check whether it finished.

## How it works (verified against backend)

### Imported columns: only 5 fields are mapped

The merchant maps CSV columns to exactly these article fields:

| CloudCart field | CSV column hint |
|---|---|
| `blog.id` | `import_blog_id` |
| `blog.name` (**REQUIRED**) | `import_blog_name` — title |
| `blog.content` | `import_blog_content` — article body |
| `blog.image` | `import_blog_image` — featured image URL |
| `blog.category` | `import_blog_category` — blog category name |

**That's it. The platform does NOT import: tags, excerpt, publish date, SEO title/description (auto-derived), or multiple authors.** SEO title is auto-truncated from the name (250 chars). SEO description is auto-truncated from the content (160 chars). The slug (`url_handle`) is auto-derived from the name.

### Image URL: downloaded into CloudCart

When the CSV's `blog.image` column has a URL, the article is saved first, then the image is downloaded and stored in CloudCart's media library under `articles/images/`. **Not hot-linked**. Only ONE image per article — comma-separated values get split and only the FIRST URL is kept.

### HTML supported (article content is HTML); Markdown NOT auto-converted

The `blog.content` field is stored as-is, rendered as HTML on the storefront. **Markdown is NOT auto-converted to HTML**; merchants who export from Markdown sources must convert before upload (or paste Markdown and accept that it renders as plain text).

### Tag auto-create: not applicable — tags are not imported

Tags are NOT a mapped column. The import flow can't reference tags from the CSV, so tag-auto-create doesn't apply.

### Category auto-create

When the CSV references a blog category by name and it doesn't exist in CloudCart, the platform **creates it automatically** before attaching the article. If the article's `blog.category` cell is empty, the article is created without a blog category.

### Author: fixed per task (not per row)

When the task's settings include `author_id > 0`, EVERY imported article in the task is assigned to that author ID. **The author cannot be set per-row from the CSV** — the merchant picks one author for the whole import, applied uniformly to every article.

### Duplicate handling: SKIP (first-or-create only)

When an article with the same `name` (or matching integration metadata) already exists in CloudCart, the existing record is kept and the CSV row is **discarded without updating** any fields. The merchant cannot use this app to bulk-update existing articles — it's create-only.

### Multi-language sister sites: NOT supported per-import

Per the manager + ErpImport flow: there is no language column in the schema. Imports always target the current site's default language. To populate sister sites in [[apps-multilang]], the merchant runs separate imports on each site, or uses the multi-language admin tools.

### Template download: not provided in-app

Per the controller: no "Download template" endpoint. Merchants build their CSV using the 5 column names listed above.

### Reused upload pipeline + working lock

Blog CSV Import shares the [[apps-csv-import]] upload pipeline — same `csv_import_{timestamp}` staging table, same delimiter / line-ending auto-detection, same `has_header_line` toggle, same `mimes:csv,txt` file-type validation (no XLS / XLSX). The blog-specific behaviour kicks in only at the mapping + finalisation stage (5 article fields instead of product fields). The `working` lock is shared too — but **only against OTHER blog imports**, not products. A merchant can have a CSV product import + a blog CSV import running in parallel because they each have their own working flag.

### Same finalize-message logic as CSV Import

Per [[apps-csv-import]]: the manager reports the four finalisation outcomes (`failed` with "no importable rows", `failed` with first-error excerpt, `completed` with reduced imported count, `completed` with full success). For blog imports, "no importable rows" most commonly comes from leaving `import_blog_name` (title) unmapped — title is the only required field.

### No language column — defaults to current site language

Per the manager: there is no language column in the import schema. Articles are inserted with the current site's default language. To populate sister sites in a multi-language setup ([[apps-multilang]]), the merchant runs separate blog imports on each site (or uses the multi-language admin tools).

## Open questions

_None._
