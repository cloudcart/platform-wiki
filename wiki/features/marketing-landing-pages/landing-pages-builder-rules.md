---
type: feature
nav_path: "Marketing → Landing Pages → Builder rules"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Page Builder", "Dynamic page", "Builder page", "Builder editor", "Page history", "Builder module restrictions", "Builder автоматично активиране", "Builder pages"]
tags: [marketing, content, pages, builder, history, modules, restrictions]
plan_gates: ["storefront_builder"]
created: 2026-06-10
updated: 2026-10-21
source_count: 2
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, page types, editor, system slots, FAQ editor, plan gates).

# Landing Pages — Builder page rules

## Purpose

A page of type `builder` (one of the four types from [[landing-pages-types]]) is edited via the **drag-and-drop page builder** rather than the standard add/edit form. The builder owns the module palette, row settings, auto-save, publish action, and the page-history snapshot store. This page covers the **builder-specific business rules** that differ from regular / faq / landing pages: auto-active on publish, page-history retention, module-restriction validation, and the relationship to system slots.

Builder pages are gated by the `storefront_builder` plan feature (see [[landing-pages-plan-gates]]). The card on the type-picker is hidden if the merchant's plan doesn't include this feature, and the route is blocked.

## Where to find it

Sidebar → **Marketing** → **Pages** → **+ Add new page** → pick **Dynamic page** (label: `help.builder_page`).

Direct routes:

| Action | Route name | Path |
|--------|------------|------|
| New builder page | `admin.pages.builder` | `/admin/marketing/pages/builder` |
| Edit builder page | `admin.pages.builder` | `/admin/marketing/pages/builder/{page_id}` |
| Builder system page | `admin.pages.builder` (system-bound) | `/admin/marketing/pages/builder/system_page/{key}` (when the theme declares `system_pages`) |

## What the merchant can do here

The builder is its own surface (the standard Add/Edit form for `regular` / `faq` / `landing` does NOT apply). High level:

- Drag modules from the palette into rows / columns on the canvas.
- Edit per-module settings (text, images, links, products, banners).
- Changes on the canvas are auto-saved as draft history snapshots (marked *Autosaved*); the storefront keeps showing the last published version.
- **Publish changes** → creates a published history snapshot and publishes the page.
- Roll back by opening an earlier version from the page-history list (it shows the latest 50 of the up to 500 kept) and publishing it.
- For builder system pages (theme-declared) — see [[landing-pages-system-slots]] — bind the page directly to a system slot at creation time via `/admin/marketing/pages/builder/system_page/{key}`.

The Page name, URL handler, Featured image, SEO title / SEO description, and Canonical fields still apply to builder pages — they're managed via the builder UI's settings panel rather than the standard editor form.

## Settings & fields

### Module restrictions per plan tier

The `storefront_builder` plan feature is a single **access gate** for the whole builder: on a plan without it, opening the builder or any builder action (including auto-save) redirects the merchant to the plan-feature page. Publishing does **not** check the placed modules against the plan. Only two modules are gated on their own: **Video slider** and **Lookbook** appear with a padlock in the palette until their app is installed and enabled (Video slider also needs its plan feature), and the builder refuses to open or save their settings on a plan without the feature.

See [[landing-pages-plan-gates]] for the full plan-feature mapping.

### Module restrictions per system slot

A different validator — the platform code — runs when a builder page assigned to a system slot is published (auto-saves are not checked). If a required module for the slot is missing, publishing is rejected with:

> *"You must add widget ":widget" for publish this page"*

Restriction entries exist ONLY for:

- `blog.list` system slot — requires the `blog-list` module on the page.
- `blog.view` system slot — requires the `blog-view` module on the page.

There are **NO** restriction entries for `home`, `thank_you`, or `error.404` — a builder page can be assigned to the homepage slot without any required modules. The two blog slots are currently switched off (a page can be assigned only to the homepage, thank-you or 404 slot), so in practice this check never rejects a publish. See [[landing-pages-system-slots]] for the broader system-slot story.

## Business rules

### Builder pages auto-activate on publish

When publishing a `builder` page from the builder UI (**Publish changes**), `active` is set to `yes` **unconditionally** — a builder page cannot be published as inactive from the builder editor. The auto-saves made while editing are drafts: they change neither the live page nor its Active state. The merchant can still deactivate a builder page from the list ([[landing-pages-list-view]]) via the inline Active toggle, but the builder editor itself always activates the page on publish. Through the Admin GraphQL API ([[settings-pat-tokens]]), `savePageBuilderDesign` stores a draft version like an auto-save unless it is asked to publish; publishing through it or through `publishPageBuilderDesign` activates the page the same way.

### Builder pages keep edit history (last 500 versions)

When the merchant publishes a `builder` page, a new `PageHistory` row is created with the page's full content snapshot + `published = 1`; every auto-save also adds a row, marked *Autosaved* instead of *Published*. The model retains the **last 500 versions per page** (published and auto-saved together) — rows beyond that are deleted on every publish or auto-save. The builder's history list shows the latest 50; the merchant opens one and publishes it to roll back.

Regular / faq / landing pages do **NOT** keep edit history this way — every save overwrites in place.

### Bulk Copy on builder pages keeps the latest snapshot only

The bulk Copy action ([[landing-pages-list-view]]) copies builder pages with the page's current content + a single new `PageHistory` row (the latest snapshot). The original page's full 500-version history is NOT copied to the duplicate.

### URL is built by the link helper

The storefront URL for a builder page is rendered exactly like any other page: `/page/<url_handle>` (or `/private-page/<url_handle>` if the Private toggle is on). The builder editor's preview-popover uses the same helper as the standard editor.

### Module restrictions are stricter on Blog system pages than on `home` / `thank_you` / `error.404`

This is a frequent source of confusion. The wiki's earlier "a homepage builder page must include the products module" claim was **incorrect**. The actual rule:

- **Blog list / Blog view** as system slots → required modules enforced (both slots are currently switched off, so this never applies today).
- **Home / Thank-you / 404** as system slots → no required modules; the merchant can publish whatever they want.

### Content storage rewrites image URLs (same as regular pages)

Builder pages' JSON content is piped through the platform code / the platform code recursively on save / read — so embedded image URLs stay portable across CDN domain changes. See [[landing-pages-editor]] for the same mechanism on regular pages.

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-types]] — the **Dynamic page** card on the **Choose page type** modal.
- [[landing-pages-list-view]] — inline Active toggle (the only way to deactivate a builder page).
- [[landing-pages-editor]] — common form fields (Page name, URL handler, etc.).
- [[landing-pages-system-slots]] — builder system pages and the `PageRestriction` Blog slot requirements.
- [[landing-pages-plan-gates]] — the `storefront_builder` access gate and the two separately gated modules (Video slider, Lookbook).
- [[widget-vs-page-builder-block]] — concept page contrasting storefront widgets vs page-builder blocks (builder modules and widgets are related but distinct).

## Open questions

- 📡 **Theme `page_builder` flag and `system_pages` declaration.** The visibility of the **Dynamic page** card and the builder-system-page slots depends on theme-config flags whose exact keys should be verified against `vuejs-storefront` theme manifests. (verify)
