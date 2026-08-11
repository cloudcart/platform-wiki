---
type: feature
nav_path: "Products → Categories → SEO & URL"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Category SEO", "Category URL handle", "Category SEO title", "Category meta description", "301 redirect", "url_handle", "Категория — SEO", "Категория — URL"]
tags: [products, categories, seo, url]
plan_gates: []
created: 2026-06-10
updated: 2026-06-11
source_count: 3
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, edit modal, hierarchy rules, cart restrictions, deletion rules, JSON-API/validation). Google-Shopping / feed **taxonomy** mapping is on [[products-categories-taxonomy]].

# Categories — SEO & URL handle

## Purpose

How a category surfaces in search engines: the **SEO title**, **SEO description**, **URL handle** (slug), and the **301-redirect-on-rename** trail — all set on the category Add / Edit modal's **Advanced settings** card. (Google Shopping / feed **taxonomy** mapping is a separate concern — see [[products-categories-taxonomy]].)

## Where to find it

Sidebar → Products → **Categories** → +Add category (or Edit) → expand the **Advanced settings** card.

## What the merchant can do here

- Set the **SEO title** (the storefront category page's `<title>` tag).
- Set the **SEO description** (the page's `<meta name="description">`).
- Set the **URL handle** (slug → `/category/<handle>`).

### What the merchant CANNOT do here

- Bulk-set the same SEO title / description across many categories — edit one at a time, or generate via [[apps-seo-spinner]].
- Auto-cascade SEO fields from a parent to children — they are stored per category and do NOT inherit.
- Reuse a URL handle already used by another category — duplicates are rejected with a validation error on this screen.

## Settings & fields

| Field | What it does |
|-------|--------------|
| **SEO title** (`seo_title`) | `<title>` tag value. Falls back to the category name if blank. |
| **SEO description** (`seo_description`) | `<meta name="description">` value. Falls back to a truncation of the description if blank. |
| **URL handle** (`url_handle`) | URL slug, prefixed with `/category/` (e.g. `electronics` → `/category/electronics`). Auto-generated from the name if blank (lowercase, hyphens, accent-stripped). |

## Business rules

### SEO fields do NOT inherit from parent
The SEO fields (and `taxonomy_id`, `make_interval`) are stored **per category** and are NOT cascaded from the parent. A child category with empty `seo_title` falls back to its **own** name — not the parent's. For a consistent SEO pattern across subcategories, set the fields explicitly on each, or use [[apps-seo-spinner]] for bulk generation.

### `seo_generated_through_spinner` flag identifies auto-generated content
When [[apps-seo-spinner]] generates the SEO description, the `seo_generated_through_spinner` flag flips to true — letting the merchant tell auto-generated from hand-written content. The flag is set by the app, not the merchant.

### URL handle uniqueness — behaviour diverges by entry path
The URL handle must be **unique across all categories**. On a duplicate:

- **Admin form (this screen)** — save is **REJECTED** with a validation error; the merchant must pick another handle (or rely on auto-derivation).
- **CSV / XML import** ([[apps-csv-import]]) — the handle is **silently auto-suffixed** (`-1`, `-2`, …) so the bulk import doesn't fail mid-batch.
- **JSON-API v2** ([[api-categories]]) — follows the admin behaviour: duplicate handles return 422. See [[products-categories-api-validation]].

### URL handle change records a 301 redirect
When the merchant changes the URL handle on an existing category, the previous handle is recorded in a URL-handle history store and the storefront serves a permanent HTTP 301 redirect from the old URL to the new one — protecting bookmarked links and search-engine equity. No merchant-facing UI surfaces this redirect list directly (verify).

### Per-category image dimensions are merchant-controlled
The `width`, `height`, and `max_thumb_size` fields set the recommended image dimensions for that category. The platform imposes no hard category-image cap.

### Permission
Editing the SEO + URL fields requires the products / categories permission.

## Related

- [[products-categories]] — hub.
- [[products-categories-taxonomy]] — Google Shopping / feed taxonomy mapping (the sibling concern).
- [[products-categories-edit-modal]] — the Advanced settings card lives here.
- [[products-categories-api-validation]] — URL-handle + SEO validation and JSON-API behaviour.
- [[apps-seo-spinner]] — bulk-generates SEO content; sets `seo_generated_through_spinner`.
- [[apps-csv-import]] — bulk-import flow that auto-suffixes duplicate URL handles.
- [[category]] — entity page.
- [[seo-handling]] — the store-wide SEO concept.

## Open questions

- Whether the URL-handle 301-redirect history is surfaced to the merchant anywhere in the admin (verify).
- Exact validation message on duplicate URL handle in the admin form (verify wording).
