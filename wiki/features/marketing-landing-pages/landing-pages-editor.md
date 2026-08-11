---
type: feature
nav_path: "Marketing → Landing Pages → Add / Edit"
route_name: admin.pages.edit
route_path: /admin/marketing/pages/edit/{page_id}
aliases: ["Edit page", "Add page", "Page editor", "Page form", "URL handler", "SEO title", "SEO description", "Featured image", "Private page", "Редакция на страница"]
tags: [marketing, content, pages, editor, validation, seo]
plan_gates: ["static_pages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, page types, system slots, FAQ editor, builder rules, plan gates).

# Landing Pages — Add / Edit form

## Purpose

The **Add / Edit** form is the per-page content editor. It is the same screen for adding a new page and editing an existing one (the URL differs by `{page_id}`). The exact fields and content widget vary per **type** — see [[landing-pages-types]] for the four shapes. This page covers the **field-level** behaviour, **validation rules**, **URL-handle handling**, **Open Graph image semantics**, **canonical override**, and the optional **Private** toggle from the membership app. The FAQ editor's per-row Q&A specifics live on [[landing-pages-faq-editor]]; the builder editor's save / history / module rules live on [[landing-pages-builder-rules]].

## Where to find it

From the list ([[landing-pages-list-view]]) — click any row's name to open Edit, or click **+ Add new page** → pick a type → Add form. Direct routes:

| Action | Route name | Path |
|--------|------------|------|
| Add | `admin.pages.add` | `/admin/marketing/pages/add/{type}` |
| Edit | `admin.pages.edit` | `/admin/marketing/pages/edit/{page_id}` |

For builder-type pages, the editor is a separate route — `/admin/marketing/pages/builder/{page_id?}` — see [[landing-pages-builder-rules]].

## What the merchant can do here

- Enter or change the page's **Page name** (internal-use label).
- Enter or change the **URL handler** — the `/page/<slug>` URL on the storefront.
- Set an optional **Canonical** URL (regular / faq / builder only).
- Edit **type-specific content** — TinyMCE rich text (regular), Q&A pair list (faq — see [[landing-pages-faq-editor]]), `<textarea>` raw HTML (landing), or page-builder JSON (builder — see [[landing-pages-builder-rules]]).
- Upload a **Featured image** (regular / faq / builder only) — used as the page's Open Graph image when shared on social media.
- Enter **SEO title** and **SEO description** with a live Google-snippet preview (regular / faq / builder only — landing skips SEO fields).
- Toggle **Active** (top-right of the form).
- Toggle **Private** (only when the [[apps-membership]] app is installed) — restricts the page to customers who have purchased certain products.

## Settings & fields

### Validation

| Field | Validation | Error message |
|-------|------------|---------------|
| `name` | Required, max 191 chars, case-insensitive unique | *"The field 'name' is required"* / *"That name is already taken"* / *"The maximum allowed characters are X"* |
| `url_handle` | Required + lowercase regex (`address_name_sanitize_trim_js`) + unique across ALL types | *"URL is required."* / *"Invalid URL format"* / *"The provided title for the URL is already taken"* / *"The maximum allowed characters for the 'URL handler' are X"* |
| `seo_title` | Max chars cap | *"The maximum allowed characters for the 'SEO title' are X"* |
| `seo_description` | Max chars cap | *"The maximum allowed characters for the 'SEO description' are X"* |
| `content` (regular / faq) | Max 10 000 000 chars; required; FAQ also requires at least one Q&A row | *"You have to provide any content"* / *"The maximum allowed characters for the content are X"* |

Name max length matches the database's 191-character indexable text-column cap. Content max is effectively unlimited for any reasonable HTML page.

### Name uniqueness is case-INsensitive

The "name already taken" check uses `WHERE name LIKE ?` — so "About Us" and "about us" are considered duplicates. This is in addition to the URL-handle uniqueness check, which is exact-match.

### URL handle is normalised on the fly

Typing into the URL handler field runs the `address_name_sanitize_trim_js` client-side regex — lowercase letters + dashes only. Typing "About Us" produces `about-us` on the fly. Trailing / leading dashes are trimmed.

### URL preview popover

The form shows a popover preview of the final URL as the merchant types:

- Standard page: `{site_url}/page/<typed-handle>`
- Private page: `{site_url}/private-page/<typed-handle>` (the prefix changes when **Private** is toggled on)
- Canonical: `{site_url}/<typed-canonical>` (no `/page/` prefix — the canonical is the full path override)

### Featured image semantics

The featured image on a regular / faq / builder page is the page's **Open Graph image** — when the page is shared on Facebook, LinkedIn, or other OG-aware platforms, this image is rendered alongside the link preview. The image is uploaded via the standard image-upload pipe and served at multiple sizes (e.g. `150x150`).

`landing`-type pages do NOT have a featured image (no upload widget on the form).

### Private toggle (membership app only)

When the [[apps-membership]] app is installed, an extra **Private page** switch appears next to **Active**. Private pages live at `/private-page/<slug>` (not `/page/<slug>`) and are only accessible to customers who have purchased the products defined in the page's membership rules. Tooltip text: *"The page will be available to users only when purchasing certain products."* Toggling Private = yes on a store without the app installed only changes the URL prefix — the route is unreachable to customers without the membership app active.

## Business rules

### URL handle conflict detection spans all types

Saving a page with a `url_handle` that already exists on another page returns *"The provided title for the URL is already taken"* and the form does not save. The check is **across all four types** — the merchant can't have `/page/about-us` as both a regular page and a builder page; only one can claim the slug.

### Content storage rewrites image URLs

Page content is piped through the platform code on save (swapping fully-qualified storage URLs with internal placeholders) and the platform code on read (re-resolving them). The stored page content is portable across CDN URL changes. JSON content (builder pages) gets the same treatment recursively. The merchant does not see this — content with embedded images keeps working after CDN domain changes.

### Cache invalidation on every save

Every page save flushes the `private-shop:redirect_page` cache (always) and the `error404` cache (when `system_page` is dirty). See [[landing-pages-system-slots]] for the system-slot cache cascade.

### Defensive fallback for unknown page types at edit time

If a page's stored `type` is unexpected (`custom`, `legacy`, blank), the editor falls back to the `regular` type — the page opens in TinyMCE rather than crashing with a template-not-found error. This is by design: creation is strict, editing is lenient — see [[landing-pages-types]] for the contrast.

### Permission

The Landing Pages screen is part of the Marketing pillar. Visibility is gated by the `marketing` permission family (verify the exact key in [[settings-staff]]). Staff roles can be scoped down to "Pages only" within Marketing.

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-types]] — the four page types and what each renders in this form.
- [[landing-pages-list-view]] — the list screen that opens this form.
- [[landing-pages-faq-editor]] — FAQ-specific shifting-rows editor.
- [[landing-pages-builder-rules]] — builder-specific save / history / module rules.
- [[landing-pages-system-slots]] — `home` / `thank_you` / `error.404` assignment (sets cache flushes).
- [[apps-membership]] — Private-page gate (only renders when this app is installed).
- [[marketing-seo-meta]] — site-wide SEO meta editor (the page's `seo_title` + `seo_description` flow into this surface).
- [[settings-staff]] — Marketing pillar permission family.

## Open questions

- 📡 **Exact char caps per field.** `name`, `url_handle`, `seo_title`, `seo_description`, and `content` all enforce max-char caps; the validation messages reference "X" for the cap. Verify the exact numeric cap per field from the validator. (verify — name confirmed at 191, content at 10 000 000)
