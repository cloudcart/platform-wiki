---
type: feature
nav_path: "Marketing → Landing Pages"
route_name: admin.pages.list
route_path: /admin/marketing/pages
aliases: ["Landing pages", "Static pages", "Pages", "Landing Pages", "Page CMS", "About Us", "Contact page", "FAQ page", "Целеви страници", "Статични страници", "Страници"]
tags: [marketing, content, pages, cms, seo]
plan_gates: ["static_pages", "landing_page", "faq_page", "storefront_builder"]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Landing Pages

## Purpose

The **Landing Pages** screen is the merchant's storefront CMS for everything that isn't a product, a category, a blog article, or the checkout flow. This is where the merchant creates the "About Us", "Contact", "Privacy Policy", "Terms & Conditions", "Shipping Information", "FAQ", and any custom one-off landing page (e.g. a Black Friday promo, a partnership announcement, a brand story). Each page has its own URL, its own SEO title and description, optional cover image, type-specific content, an active/inactive toggle, and an optional **system-page assignment** that wires the page up as the store's actual Home page, Thank-you page, or 404 page.

These pages are **distinct from blog articles** ([[marketing-blog-articles]] — `/blog/<slug>` content with comments and tags) and from product / category pages (auto-generated from the catalogue). Landing pages live at `/page/<url-handle>` on the storefront (or `/private-page/<url-handle>` when the [[apps-membership]] gate is on), and are routinely linked from the storefront's main menu, footer, checkout disclaimers, and email-template legal links.

Because the screen covers several independent concerns — the list view, the type picker, the per-type editor, the system-slot assignment, the FAQ editor, the builder editor, and the plan-gate stack — it is split into aspect pages. Drill into the aspect that matches the question rather than reading every page.

## Where to find it

Sidebar → **Marketing** → **Pages** (may appear as "Landing pages" in the Marketing dropdown depending on store).

The route is `/admin/marketing/pages`. The breadcrumb reads "Landing pages" (label key: `page.header.pages`).

Sub-routes:

| Action | Route name | Path |
|--------|------------|------|
| List | `admin.pages.list` | `/admin/marketing/pages` |
| Add | `admin.pages.add` | `/admin/marketing/pages/add/{type}` |
| Edit | `admin.pages.edit` | `/admin/marketing/pages/edit/{page_id}` |
| Toggle active | `admin.pages.status` | `/admin/marketing/pages/status/{page_id}/{status?}` |
| Assign system page | `admin.pages.assign` | `/admin/marketing/pages/assign/{page_id?}` |
| Copy | `admin.pages.copy` | `/admin/marketing/pages/copy` |
| Page Builder | `admin.pages.builder` | `/admin/marketing/pages/builder/{page_id?}` |

## What the merchant can do here

Top-level actions on the screen:

- Browse the table of all pages, filter / search / inline-toggle Active, inline-assign system slot, bulk-act on selection — see [[landing-pages-list-view]].
- Click **+ Add new page** to open the **Choose page type** modal — four cards (`regular` / `faq` / `landing` / `builder`); see [[landing-pages-types]].
- Open the Add / Edit form for a page — fields, validation rules, URL-handle handling, SEO and Open Graph, Private toggle — see [[landing-pages-editor]].
- Assign a page to a **system slot** (`home` / `thank_you` / `error.404`) — instantly, no save needed — see [[landing-pages-system-slots]].
- Edit FAQ-type pages via the **shifting-rows Q&A editor** — see [[landing-pages-faq-editor]].
- Edit builder-type pages via the **page builder** (auto-active, 500-version history, module restrictions) — see [[landing-pages-builder-rules]].
- See the remaining-pages allowance — gated by plan features — see [[landing-pages-plan-gates]].

## Sub-pages (in this cluster)

- [[landing-pages-list-view]] — the list table; columns; cascading filter dropdown; bulk actions (Activate / Deactivate / Delete / Duplicate); the "(N)" counter on **+ Add new page**.
- [[landing-pages-types]] — the four page types (`regular`, `faq`, `landing`, `builder`); the **Choose page type** modal; the builder system-page picker.
- [[landing-pages-editor]] — Add / Edit form fields; validation messages; URL-handle normalisation; Open Graph image; SEO fields; Private toggle; defensive fallback for unknown types.
- [[landing-pages-system-slots]] — `home` / `thank_you` / `error.404` assignment; exclusive-per-slot transaction; cache-flush cascade (`error404`, `private-shop:redirect_page`); builder system pages.
- [[landing-pages-faq-editor]] — shifting-rows Q&A module; per-row add / remove / move; full-replacement save model; at-least-one-row rule.
- [[landing-pages-builder-rules]] — builder pages auto-activate on save; 500-version `PageHistory`; per-system-slot module restrictions (`blog.list` / `blog.view` only); per-plan module restrictions.
- [[landing-pages-plan-gates]] — `static_pages` (numeric cap, feature-pack extendable), `landing_page`, `faq_page`, `storefront_builder` (access gates); the "(N)" counter mechanism; upsell redirection.

## Settings & fields

Field-level details live on the aspect pages — start with [[landing-pages-editor]] for the form fields and [[landing-pages-types]] for the type-specific shape table. The validation messages catalogue is on [[landing-pages-editor]].

## Business rules

Cross-cutting rules summarised — the full rule rationale lives on the aspect pages:

- **Page versus blog article — when to use which.** About Us / Privacy / Terms → regular `Page`. Recurring marketing content with categories, tags, comments → [[marketing-blog-articles]]. Q&A help centre → `faq` page ([[landing-pages-faq-editor]]). Drag-and-drop custom layout → `builder` page ([[landing-pages-builder-rules]]). Externally-built HTML → `landing` page. Pages are **stand-alone** — there is no concept of "page categories" or "page tags".
- **URL handle uniqueness spans ALL types** — see [[landing-pages-editor]]. The merchant can't have `/page/about-us` as both a regular page and a builder page.
- **System-page assignment is unique per slot** — assigning a new page to `home` automatically unassigns the previous one, in a single DB transaction; see [[landing-pages-system-slots]].
- **System-page changes flush two storefront caches** — `error404` and `private-shop:redirect_page` (via the platform code); the inline Active toggle on the list ALSO flushes the 404 cache. See [[landing-pages-system-slots]].
- **Bulk Copy duplicates with a `--{unix-timestamp}` suffix** on both `name` and `url_handle`. System-page assignments are dropped on the copy. See [[landing-pages-list-view]].
- **Builder pages auto-activate on save** and keep the last 500 saved snapshots in `PageHistory`. Regular / faq / landing pages do not. See [[landing-pages-builder-rules]].
- **Builder module-restriction validation covers ONLY `blog.list` / `blog.view` system slots** — there are NO required modules for `home`, `thank_you`, or `error.404`. See [[landing-pages-system-slots]] + [[landing-pages-builder-rules]].
- **Name uniqueness is case-insensitive**, URL-handle uniqueness is exact-match. See [[landing-pages-editor]].
- **Defensive fallback for unknown page types** — creation is strict (404 on unknown type), editing is lenient (falls back to `regular`). See [[landing-pages-types]] + [[landing-pages-editor]].
- **Permission** — gated by the `marketing` permission family in [[settings-staff]] (verify exact key).

## Related

- [[marketing]] — parent Marketing pillar.
- [[marketing-blog-articles]] — blog articles (distinct from pages; chronological content with comments).
- [[marketing-blog-category]] — blog categorisation (pages don't have categories).
- [[marketing-seo-meta]] — site-wide SEO meta editor.
- [[marketing-seo]] — SEO hub.
- [[analytics-top-landing-pages]] — analytics for landing-page traffic.
- [[analytics-landing-pages-by-sales]] — landing-page revenue attribution.
- [[apps-membership]] — Private-page gate.
- [[plan-gates]] — `static_pages` / `faq_page` / `landing_page` / `storefront_builder` plan caps.
- [[plan-features]] — upsell page the merchant is redirected to when over a cap.
- [[plan-vs-feature-pack]] — feature packs that extend `static_pages`.
- [[seo-handling]] — concept page on SEO across the platform.
- [[seo-meta]] — SEO meta entity.
- [[settings-staff]] — Marketing pillar permission family.

## Open questions

None at the hub level — open items live on the relevant aspect pages:

- Exact plan caps per tier — see [[landing-pages-plan-gates]].
- Theme `page_builder` + `system_pages` flag origin — see [[landing-pages-types]] + [[landing-pages-builder-rules]].
- Bulk-Copy cap pre-check behaviour — see [[landing-pages-plan-gates]].
- FAQ `multylang` translation persistence across delete-and-reinsert saves — see [[landing-pages-faq-editor]].
