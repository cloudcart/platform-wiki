---
type: storefront-page
route_name: page
route_path: /page/{slug?}
themes_using: [all]
tags: [storefront, cms, static-page]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Static page (storefront)

## Purpose

Generic CMS page used for any rich-text content the merchant needs: Terms of Service, Privacy Policy, Shipping Policy, About Us, Returns, etc. Slug-based routing makes the URL friendly (`/page/terms`, `/page/about`).

## URL & route

- **Route name:** `page`
- **Path:** `/page/{slug?}` with `where('slug', '(.*)')` — the slug regex accepts any characters, including `/`, so nested-looking paths like `/page/help/shipping` resolve to the same route with `slug = help/shipping`.
- **Middleware:** `uuid_generate`, `subscriber_uuid`, `TSStatistic:page` (analytics tracking).
- **Method:** `GET`.
- **Preview variant:** `/preview/page/{page_id}/{history_id?}` — route name `site.preview.page`, used by admin to preview drafts.

## How it loads

1. Route resolves to the request handler.
2. Controller looks up the page by `slug`. If not found → `404`. If found but `active != yes` → renders the notification `sf.page.err.page_no_longer_active`.
3. The page record has a `type` field. The template branches on it:
   - `type = faq` → includes [[page-faq]] template (`page/faq.tpl`).
   - `type = builder` → delegates to `preview` (renders the MyStore builder output).
   - `type = landing` → returns the page's raw HTML body verbatim (no header/footer wrap) — see [[marketing-landing-pages]].
   - Anything else → renders the body as `{$page->content nofilter}` inside the standard layout.
4. SEO meta and `Open Graph` come from the page record.

## What the customer sees

- Breadcrumb: **Home › <Page name>**.
- `<h1>` page name.
- Rich-text body inside `_textbox`.
- When loaded via AJAX or as an iframe (the platform code), the template renders a modal-friendly variant (`_popup _popup-terms`) WITHOUT the header/footer — used by the checkout to pop ToS in an overlay.

## Storefront behaviour

- The page is editable from the admin under the **Content / Pages** section (verify exact nav path).
- `nofilter` Smarty modifier means all admin-side HTML is output as-is — no escaping.
- Per-page `slug` is unique within the store; renaming the slug breaks old URLs (admin offers a 301-redirect helper via the platform code).

## JavaScript behaviour

- No page-specific JS hooks — the template is content-only.
- When opened as an AJAX modal from checkout, the parent page's modal framework handles open/close.

## Customisations available to the merchant

- Page name, slug, body (WYSIWYG), SEO title, SEO description, OG image — all editable per page.
- Active toggle (`yes`/`no`).
- Page `type`:
  - **Standard** — default, rich-text body.
  - **FAQ** — see [[page-faq]].
  - **Builder** — MyStore drag-and-drop page (see [[design]] / [[design-themes]]).
  - **Landing** — raw HTML landing page (see [[marketing-landing-pages]]).
- Private flag for membership-gated pages — see [[private-page]].

## Theme variations

- All Smarty themes use `templates/page/page.tpl` with the same controller contract. Visual differences are limited to typography and breadcrumb styling.
- Liquid-engine / headless themes render via a different pipeline — see [[storefront-architecture]].

## Known issues / by-design vs bug

- The `(.*)` slug regex means `/page/anything/at/all` matches; if the merchant intentionally uses slashes in slugs (`help/shipping`), the page resolves but breadcrumbs may not reflect the nesting.
- Inactive pages return `200` with a notification rather than `404` — keeps SEO-discovered URLs from dropping until the merchant explicitly redirects them.
- The AJAX/iframe variant strips header & footer; embedding it inside a non-modal context will look unstyled.

## Related

- [[page-faq]]
- [[private-page]]
- [[marketing-landing-pages]]
- [[design]]
- [[storefront-architecture]]
- [[storefront-known-issues]]

## Open questions

- Confirm the exact admin nav path for managing static pages (likely **Content / Pages** — verify).
- Confirm whether the platform code is invoked on the public `get` action too, or only on private/membership pages.
- Confirm the maximum supported slug length and whether unicode slugs are accepted.
