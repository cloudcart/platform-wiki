---
type: feature
nav_path: "Design → Static pages → Add page → Choose page type"
route_name: admin.pages.add
route_path: /admin/design/pages/add/{type}
aliases: ["Choose page type", "Page type modal", "Page types", "Dynamic page", "Regular page", "Static page", "FAQ page", "External page", "Builder page", "Add page", "Тип страница"]
tags: [marketing, content, pages, cms, types]
plan_gates: ["static_pages", "faq_page", "landing_page", "storefront_builder"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-landing-pages]]. See the hub for the other aspects (list view, editor, system slots, FAQ editor, builder rules, plan gates).

# Landing Pages — Choose page type

## Purpose

When the merchant clicks **Add page** on the list, a **Choose page type** modal opens with seven cards. Picking a card opens the editor for that type; the modal has no Save button. The type chosen at this step is **permanent** for the lifetime of the page: there is no "convert this regular page into a builder page" affordance.

The type drives every downstream behaviour — what content field renders, whether SEO fields appear, whether a featured image is allowed, whether plan-feature gating blocks the card, whether the editor keeps an edit history, and which storefront URL prefix the page is served from.

## Where to find it

Sidebar → **Design** → **Static pages** (`/admin/design/pages`) → **Add page** → the **Choose page type** modal opens. The add forms have their own addresses: `/admin/design/pages/add/regular`, `/add/faq` and `/add/landing`; the page builder is at `/admin/marketing/pages/builder`.

## What the merchant can do here

The cards of the **Choose page type** modal (English labels; the Bulgarian ones come from the admin's translations and are not recorded here):

| Card | Hint | Opens |
|------|------|-------|
| **Dynamic page** (`builder`) | "Build with the page builder" | The page builder — modules, hero banners, product rows. |
| **Regular page** (`regular`) | "Rich content (terms, about, …)" | The rich-text editor with Open Graph image and SEO fields — About Us, Privacy, Terms. |
| **Homepage** | "Your storefront home page" | The page builder bound to the home slot ([[landing-pages-system-slots]]). |
| **Thank you page** | "Shown after a successful order" | The page builder bound to the thank-you slot. |
| **Error 404 page** | "Shown when a page is not found" | The page builder bound to the 404 slot. |
| **FAQ** (`faq`) | "Questions and answers" | The Q&A editor ([[landing-pages-faq-editor]]). |
| **External page** (`landing`) | "A page you build from scratch (raw HTML)" | One raw-HTML field; no image, no SEO fields. |

The list's **Type** filter names the same types **Regular**, **FAQ**, **External** and **Page builder**. Pages a theme seeds are ordinary pages of these types and open in the matching editor ([[design-themes-switch-effects]]).

## Settings & fields

### What each type renders in the editor

| Type | Content field | Image | SEO fields | URL form | Notes |
|------|---------------|-------|------------|----------|-------|
| `builder` | JSON via Page Builder | via modules | via builder | `/page/<slug>` | Routes to `/admin/marketing/pages/builder/{page_id}` for editing. Plan-feature gated by `storefront_builder`. |
| `regular` | TinyMCE rich text | Yes | Yes (title + description) | `/page/<slug>` | The most common type — used for About Us, Privacy, Terms. |
| `faq` | Q&A pairs (shifting-rows module) | Yes | Yes | `/page/<slug>` | Each row is a separate FAQ entry — see [[landing-pages-faq-editor]]. Plan-feature gated by `faq_page`. |
| `landing` | Raw `<textarea>` HTML | No | No | `/page/<slug>` | Stripped-down — no Open Graph image, no SEO meta editor in the form (the page handler still serves SEO meta from `seo_title` / `seo_description` if set via API). Plan-feature gated by `landing_page`. |

### Type whitelist & defensive fallback

The valid type values are exactly `regular`, `faq`, `landing`, `builder`. The add address accepts only `regular`, `faq` and `landing`; any other value finds no add form (verify the exact screen shown) — creation is **strict**.

At edit time, however, the editor falls back to the `regular` type if a page's stored `type` is unexpected (`custom`, `legacy`, blank, etc.). Editing is **lenient** by design — a hand-edited DB row with a malformed `type` still opens (as a regular page) rather than crashing with a template-not-found error, so the merchant always has a path to fix a broken row from the admin UI.

## Business rules

### The type is locked at creation

There is no "change type" affordance in the editor. To switch a page from one type to another, the merchant has to create a new page of the desired type and re-enter the content. (Copying with the bulk Copy action — see [[landing-pages-list-view]] — preserves the source type, so even copy is not a way to re-type.)

### Plan gating sits on the destination, not the card

The modal itself checks no plan and always shows every card; the gates are tied to the screens the cards open:

- `static_pages` plan-feature controls the total page-count cap (across all types).
- `faq_page` plan-feature gates the FAQ add screen (`design/pages/add/faq`).
- `landing_page` plan-feature gates the External page add screen (`design/pages/add/landing`).
- `storefront_builder` plan-feature gates the page builder (`marketing/pages/builder/...`) that the **Dynamic page** and system-page cards open.

How the gate applies when the admin app switches to the FAQ / External form without a full page load is not confirmed (verify).

See [[landing-pages-plan-gates]] for the full mapping and where each gate redirects.

### The theme's `page_builder` flag gates only admin links

The current modal shows the **Dynamic page**, **Homepage**, **Thank you page** and **Error 404 page** cards on every store. The builder itself does not check the theme: the theme's `page_builder` flag only decides whether the admin shows its links to the Homepage, Thank you and Error 404 builder pages (see [[landing-pages-builder-rules]]).

### External page (`landing`) skips the entire SEO + image stack

A `landing`-type page is the most stripped-down form: a single raw `<textarea>` for HTML and the URL handle. No TinyMCE, no featured image, no SEO title, no SEO description, no canonical override. This is the "I built my landing page in an external tool and just want to host the HTML on my CloudCart URL" path. The page is still subject to URL-handle uniqueness — see [[landing-pages-editor]].

## Related

- [[marketing-landing-pages]] — hub.
- [[landing-pages-list-view]] — list screen + filters + bulk actions; entry point to **Add page**.
- [[landing-pages-editor]] — Add / Edit form details per type.
- [[landing-pages-faq-editor]] — shifting-rows Q&A editor for `faq`-type pages.
- [[landing-pages-builder-rules]] — `builder`-type specifics (history, auto-active, module restrictions).
- [[landing-pages-system-slots]] — `home` / `thank_you` / `error.404` assignment, including builder system pages.
- [[landing-pages-plan-gates]] — plan-feature caps and per-type gates.

## Open questions

None.
