---
type: feature
nav_path: "Marketing → Landing Pages → Choose page type"
route_name: admin.pages.add
route_path: /admin/marketing/pages/add/{type}
aliases: ["Choose page type", "Page type modal", "Page types", "Dynamic page", "Static page", "FAQ page", "External page", "Builder page", "Тип страница"]
tags: [marketing, content, pages, cms, types]
plan_gates: ["static_pages", "faq_page", "landing_page", "storefront_builder"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, editor, system slots, FAQ editor, builder rules, plan gates).

# Landing Pages — Choose page type

## Purpose

When the merchant clicks **+ Add new page** on the list, a small **Choose page type** modal opens with four type cards. Picking a card routes straight to the editor for that type — no Save button on the modal itself; each card is a link whose `href` is the relevant add route. The type chosen at this step is **permanent** for the lifetime of the page: there is no "convert this regular page into a builder page" affordance.

The type drives every downstream behaviour — what content field renders, whether SEO fields appear, whether a featured image is allowed, whether plan-feature gating blocks the card, whether the editor keeps an edit history, and which storefront URL prefix the page is served from.

## Where to find it

Sidebar → **Marketing** → **Pages** → click **+ Add new page** → the **Choose page type** modal opens.

Direct deep-links (one per type) are also valid URLs the merchant can land on from a bookmark or from a help link:

| Type | Direct add URL |
|------|----------------|
| `regular` | `/admin/marketing/pages/add/regular` |
| `faq` | `/admin/marketing/pages/add/faq` |
| `landing` | `/admin/marketing/pages/add/landing` |
| `builder` | `/admin/marketing/pages/builder` (the page-builder editor; no `{page_id}` until the first save) |

## What the merchant can do here

In the **Choose page type** modal, four type cards:

| Type | Icon | Label key | Use case |
|------|------|-----------|----------|
| `builder` | palette | `help.builder_page` (**Dynamic page**) | Drag-and-drop visual page builder — custom landing pages with modules, hero banners, product slider rows. Only shown if the active theme supports `page_builder`. |
| `regular` | newspaper | `help.regular_page` (**Static page**) | TinyMCE rich-text editor + featured image + SEO fields — for About Us, Privacy, Terms. |
| `faq` | stream | `help.faq_page` (**FAQ page**) | Question/answer accordion pairs — for "Frequently asked questions" pages. See [[landing-pages-faq-editor]] for the shifting-rows Q&A manager. |
| `landing` | link | `help.landing_page` (**External page**) | Lightweight HTML-only page (raw `<textarea>` content, no TinyMCE, no image, no SEO fields) — for embedding a landing page from an external builder or pasting hand-crafted HTML. |

Each card is a simple `<a>` link — clicking routes directly to the relevant Add form (`/admin/marketing/pages/add/{type}` for `regular` / `faq` / `landing`, or `/admin/marketing/pages/builder` for `builder`). The modal closes via the page-transition itself.

### Builder system page picker (theme-driven secondary modal)

When the active theme declares `system_pages`, an additional **`SystemPageModal`** is reachable from the type picker. Same shape — a list of `<a>` cards, one per declared system page — each routes to `/admin/marketing/pages/builder/system_page/{key}` (e.g. a theme might declare `home`, `thank-you`, `404` as builder-only system pages). This routes the merchant straight to the page builder pre-bound to that system slot. The modern UI typically auto-routes through the system-page list from the Choose-page-type modal itself; the separate `SystemPageModal` is reachable only if the type picker doesn't already include the system pages inline.

## Settings & fields

### What each type renders in the editor

| Type | Content field | Image | SEO fields | URL form | Notes |
|------|---------------|-------|------------|----------|-------|
| `builder` | JSON via Page Builder | via modules | via builder | `/page/<slug>` | Routes to `/admin/marketing/pages/builder/{page_id}` for editing. Plan-feature gated by `storefront_builder`. |
| `regular` | TinyMCE rich text | Yes | Yes (title + description) | `/page/<slug>` | The most common type — used for About Us, Privacy, Terms. |
| `faq` | Q&A pairs (shifting-rows module) | Yes | Yes | `/page/<slug>` | Each row is a separate FAQ entry — see [[landing-pages-faq-editor]]. Plan-feature gated by `faq_page`. |
| `landing` | Raw `<textarea>` HTML | No | No | `/page/<slug>` | Stripped-down — no Open Graph image, no SEO meta editor in the form (the page handler still serves SEO meta from `seo_title` / `seo_description` if set via API). Plan-feature gated by `landing_page`. |

### Type whitelist & defensive fallback

The valid type values are exactly `regular`, `faq`, `landing`, `builder`. Any other value passed via `/admin/marketing/pages/add/{type}` returns a 404 ("The page no longer exists") — creation is **strict**.

At edit time, however, the editor falls back to the `regular` type if a page's stored `type` is unexpected (`custom`, `legacy`, blank, etc.). Editing is **lenient** by design — a hand-edited DB row with a malformed `type` still opens (as a regular page) rather than crashing with a template-not-found error, so the merchant always has a path to fix a broken row from the admin UI.

## Business rules

### The type is locked at creation

There is no "change type" affordance in the editor. To switch a page from one type to another, the merchant has to create a new page of the desired type and re-enter the content. (Copying with the bulk Copy action — see [[landing-pages-list-view]] — preserves the source type, so even copy is not a way to re-type.)

### Plan gating restricts which cards are clickable

The four type cards are not all available on every plan:

- `static_pages` plan-feature controls the total page-count cap (across all types).
- `faq_page` plan-feature controls whether the **FAQ page** card is clickable.
- `landing_page` plan-feature controls whether the **External page** card is clickable.
- `storefront_builder` plan-feature controls whether the **Dynamic page** (builder) card appears at all.

See [[landing-pages-plan-gates]] for the full mapping and where each gate redirects.

### Builder card visibility is theme-driven, not just plan-driven

The **Dynamic page** card only appears if the active theme declares `page_builder` support in its theme config. A merchant on a Pro plan whose theme does not support the page builder will not see the card at all — there's no error, just no card. Switching themes (or contacting CloudCart support to enable a theme's page-builder flag) is the workaround. (verify)

### External page (`landing`) skips the entire SEO + image stack

A `landing`-type page is the most stripped-down form: a single raw `<textarea>` for HTML and the URL handle. No TinyMCE, no featured image, no SEO title, no SEO description, no canonical override. This is the "I built my landing page in an external tool and just want to host the HTML on my CloudCart URL" path. The page is still subject to URL-handle uniqueness — see [[landing-pages-editor]].

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-list-view]] — list screen + filters + bulk actions; entry point to **+ Add new page**.
- [[landing-pages-editor]] — Add / Edit form details per type.
- [[landing-pages-faq-editor]] — shifting-rows Q&A editor for `faq`-type pages.
- [[landing-pages-builder-rules]] — `builder`-type specifics (history, auto-active, module restrictions).
- [[landing-pages-system-slots]] — `home` / `thank_you` / `error.404` assignment, including builder system pages.
- [[landing-pages-plan-gates]] — plan-feature caps and per-type gates.

## Open questions

- 📡 **Theme `page_builder` flag origin.** The conditional visibility of the **Dynamic page** card depends on whether the active theme advertises `page_builder` support — exact theme-config key to verify against `vuejs-storefront` theme manifests. (verify)
