---
type: feature
nav_path: "Marketing → Blog → Articles → Add via CSV"
route_name: blog-articles-list
route_path: /admin/marketing-new/blog/articles
aliases: ["Add via CSV", "Blog CSV import", "Import articles from CSV", "Bulk import articles", "Внасяне на статии от CSV", "Импорт на статии"]
tags: [marketing, blog, articles, import, csv, apps]
plan_gates: ["blog_articles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[marketing-blog-articles]]. See the hub for the other aspects (list, editor, rules, storefront visibility, API).

# Blog Articles — CSV import wizard

## Purpose

The CSV-import wizard is the bulk-create path for blog articles: upload a CSV file, map its columns to the article fields, and queue a background job that creates each row as an article. It exists for merchants migrating content from WordPress / Ghost / Medium or any other blogging platform that can export CSV. The wizard is only available when the [[apps-blog-csv-import]] app is installed.

## Where to find it

Sidebar → **Marketing** → **Blog** → **Articles** → **Add via CSV** button in the page header.

The button is only rendered when the `blog_csv_import` app is installed (read from `useApplicationsStore`). Without the app, the import path is unreachable from the admin.

## What the merchant can do here

The action opens `CcImportCsvModal` — a 3-step wizard that shares state via `useImportCsvModal('blog')`. Each step is a separate `CcModal` instance chained from the previous; closing mid-flow loses partial state (no draft).

**Step 1 — Upload + settings** (title: *"Import CSV"*):

- **Import CSV file** card — `CcUploadFile` (extension restricted to `csv`) with help block *"Click Select to choose the file with your import data."*.
- **CSV file settings** card — `CcSwitch` *"Check this if your file has a header line explaining the columns"* + `CcInput` *"The character that separates the names of the categories"* (placeholder *"Example: >"* — the delimiter used to nest sub-categories within a single CSV cell).
- **Additional settings** card — `CcSelect` **Author** sourced from `/admin/api/core/settings/account/admins`. The selected admin user is attached as author on every imported article.
- The Save button on Step 1 disables while the file uploads. Validation errors (e.g. missing `import_file`) surface via `errorStore.getError('import_file')`.

**Step 2 — Field mapping** (title: *"Import CSV file mapping"*):

- Auto-opens after Step 1 succeeds. Loading state shows *"Loading mapping options..."* while the modal fetches the parsed CSV column list + the target-article field list.
- For each Article field exposed by the importer, a `CcSelect` lets the merchant pick which CSV column maps to it. Placeholder: *"Choose field"*. The selects are searchable.
- If the CSV had no parsable headers, the body falls through to *"No mapping options available"*.

**Step 3 — Thank-you + tracking** (title: *"Tracking progress"*):

- A large green check-circle icon + body text: *"The file was successfully uploaded and the products import task was added to the queue. If you wish, you could track the uploading in the queued jobs."*
- Primary CTA: **Track importing progress** routes to `apps.blog_csv_import.progress`.
- This modal hides its Save button (`:hide-save="true"`) — it's purely a status confirmation.

## Settings & fields

### Mappable target fields

The importer maps up to 5 article fields (per the [[apps-blog-csv-import]] app):

| Target field | Required? | Notes |
|--------------|-----------|-------|
| **Name** | Yes | Maps to `name` — same validation as the editor (3 ≤ length ≤ 191). |
| **Content** | Optional | Maps to `content`. HTML allowed. |
| **Image** | Optional | Maps to `image_url` — the importer downloads the URL into the store's media library synchronously. |
| **Category path** | Yes | A nested category path using the **separator** specified on Step 1 (e.g. `Recipes > Vegan > Dinners`). Categories are auto-created down the path if missing. |
| **Blog ID** | Optional | If provided, takes precedence over the category-path field. |

### Configurable per-import settings

| Setting | Where | Default |
|---------|-------|---------|
| **Has header line** | Step 1 `CcSwitch` | Off — the merchant must opt-in if their CSV's first row is column names. |
| **Category nesting separator** | Step 1 `CcInput` | None — the placeholder shows `>`. Affects how the Category-path field's value is split. |
| **Author** | Step 1 `CcSelect` | Required. Every imported article inherits this admin user as its author. |

## Business rules

### What CSV import does NOT bring in

Only the 5 fields listed above are mappable. Specifically, the following are **NOT importable via CSV** — the merchant has to add them manually after the bulk import (via the [[blog-articles-editor]]) or via [[blog-articles-api]]:

- Tags
- Excerpt
- Publish date
- SEO title / SEO description / URL handle (the URL handle is auto-derived from name)
- Cover image (only via the synchronous `image_url` field; separate from the editor's cover-image action)

### Closing mid-flow loses state

Each of the 3 wizard steps is a separate modal instance. Closing the wizard between Step 1 and Step 2, or between Step 2 and Step 3, abandons the partial upload — there is no draft / resume mechanism.

### Inline-image mirroring is synchronous on import (different from the editor)

When the **Image** column maps to `image_url`, the importer downloads the URL **synchronously** during article creation, then uploads to the store's media library. This is different from the editor's inline-image mirroring (which is async — see [[blog-articles-editor]]). On import, a failed image download blocks the row's save.

### Categories are auto-created down the nesting path

If the **Category nesting separator** is `>` and the cell contains `Recipes > Vegan > Dinners`, the importer walks the path and creates any missing categories: `Recipes`, then `Recipes > Vegan`, then `Recipes > Vegan > Dinners`. The 500-articles-per-category cap on [[blog-articles-rules]] still applies — overflow articles will fail their row's create with the standard cap error.

### Plan caps still apply

The plan-feature `blog_articles` cap (article count) and `blog_categories` cap (category count) both apply during the import. The job stops importing when either cap is hit, so a portion of a large CSV may succeed while the rest fail with the plan-limit error. See [[blog-articles-rules]] for plan gates and [[plan-features]] for tier counts.

### Progress is tracked separately

The wizard hands off to a background queue job; merchant progress is shown on the [[apps-blog-csv-import-progress]] route (linked from Step 3's CTA). See [[background-queue-inventory]] for the queue catalogue.

## Related

- [[marketing-blog-articles]] — hub.
- [[apps-blog-csv-import]] — the app that enables the **Add via CSV** path.
- [[apps-blog-csv-import-progress]] — the progress-tracking screen the Step-3 CTA jumps to.
- [[blog-articles-list]] — the page that hosts the **Add via CSV** button.
- [[blog-articles-editor]] — the manual create flow + where tags / SEO / publish-date can be added after CSV import.
- [[blog-articles-rules]] — the 500-per-category cap and plan-feature caps that the import respects.
- [[blog-articles-api]] — the programmatic alternative for migrating content.
- [[marketing-blog-category]] — categories auto-created along the nested path.
- [[background-queue-inventory]] — queue catalogue covering the import job.

## Open questions

- The exact column-mapping enum exposed by the importer (the names of the 5 fields shown on Step 2) is `(verify)` against the latest `blog_csv_import` app build.
