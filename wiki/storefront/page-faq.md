---
type: storefront-page
route_name: page
route_path: /page/{slug}
themes_using: [all]
tags: [storefront, cms, faq, accordion]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# FAQ static page (storefront)

## Purpose

A special render mode of the [[page]] route used when the merchant marks a CMS page as `type = faq`. Renders an accordion of Q&A pairs instead of a single rich-text body.

## URL & route

- **Route name:** `page` (same as the standard static page)
- **Path:** `/page/{slug}` — the FAQ variant is triggered by the page record's `type` field, not by the URL.
- **Middleware:** `uuid_generate`, `subscriber_uuid`, `TSStatistic:page`.
- **Method:** `GET`.

## How it loads

1. The standard the request handler controller resolves the slug to a page record.
2. Inside the theme templates the dispatcher checks `{if $page->type != 'faq'}`; when `type == faq`, it includes `./faq.tpl` instead of rendering the rich-text body.
3. The FAQ template iterates `$page->questions` and `$page->answers` in lockstep (`{foreach $page->questions|default:[] as $idx => $question}` … `{$page->answers[$idx]|default nofilter}`).
4. Heading, breadcrumb, layout chrome, and SEO meta come from the outer `page.tpl` — identical to a normal [[page]].

## What the customer sees

- Breadcrumb: **Home › <FAQ page name>**.
- `<h1>` page name.
- A `<ul>` (class `_faq`) of `<li>` entries. Each entry has:
  - `_faq-title` `<h3>` with the question text.
  - `_faq-text` `<p>` with the answer (rendered `nofilter`, so HTML is allowed in answers).
- Themes typically style the items as a click-to-expand accordion (only one open at a time, or click-toggle individual items — depends on theme CSS/JS).

## Storefront behaviour

- Questions and answers come from two parallel arrays stored on the page record.
- An empty `$page->questions` array renders an empty `<ul>` — no error notification.
- Like all static pages, inactive (`active != yes`) FAQ pages render the notification `sf.page.err.page_no_longer_active` rather than `404`.

## JavaScript behaviour

- The template itself ships no JS — the open/close interaction is added by theme-level scripts that target the `_faq` block or the `_faq-title` elements.
- Most themes use the storefront's generic accordion handler; verify the exact selector per theme (commonly `._faq-title` toggling `is-open` on the parent `<li>`).

## Customisations available to the merchant

- **Add / remove / reorder Q&A entries** — managed inside the page editor when `type = faq` is selected.
- **HTML in answers** — supported (rendered `nofilter`); merchants can embed links, formatting, even small media.
- **Page-level fields** — name, slug, SEO title/description, active toggle, OG image — same as any [[page]].

## Theme variations

- Visual: card-style vs minimal list, expand-collapse animation, accent colour — theme CSS only.
- Some themes auto-expand the first item; some collapse all by default.

## Known issues / by-design vs bug

- The questions/answers arrays are stored as parallel arrays — adding an answer without a matching question (or vice versa) can shift the pairing visually. Merchants should always edit in pairs.
- HTML in answers is NOT escaped — by design — but means a malformed `<a>` tag could break layout.
- The route shows up in the storefront sitemap the same way as a regular page; nothing about the URL signals "FAQ".

## Related

- [[page]]
- [[private-page]]
- [[marketing-landing-pages]]
- [[storefront-architecture]]

## Open questions

- Confirm the exact admin nav path / field labels for switching a page's `type` to `faq`.
- Confirm which themes ship an explicit accordion script vs relying on global storefront JS.
- Confirm whether there is a maximum number of Q&A items per page.
