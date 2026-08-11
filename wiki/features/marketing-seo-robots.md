---
type: feature
nav_path: "Marketing → SEO → Robots.txt"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Robots.txt", "Robots", "robots file", "Crawler directives", "Crawl directives", "Robot exclusion", "Робот файл", "Robots.txt файл", "Crawl rules"]
tags: [marketing, seo, robots, crawl-directives]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---
# Robots.txt (crawler directives editor)

## Purpose

The Robots.txt card on [[marketing-seo]] is a free-form text editor for the body of the storefront's `/robots.txt` file. `robots.txt` is the first thing every web crawler — Googlebot, Bingbot, AhrefsBot, etc. — reads when visiting the storefront. It tells crawlers which URLs they may or may not fetch, sets a per-crawler request rate (`Crawl-Delay`), and can optionally point them at the [[marketing-seo-sitemap]] URL. A wrong edit here can block Google from the entire store, so the card is guarded by an explicit confirmation modal before saving.

Two facts make this card subtler than a plain text field, and each gets its own aspect page below:

- The textarea edits **only the merchant-supplied portion**. The storefront always appends a fixed safety block (checkout / cart / wishlist Disallow lines + `Crawl-Delay: 3`) and may substitute a platform default. So the live `/robots.txt` is never exactly what's in the textarea — see [[seo-robots-served-file]].
- Stores on `trial`, `plan_expired`, or development environments serve a hard-coded `Disallow: /` (block everything) **regardless** of what the merchant types — see [[seo-robots-trial-block]]. This is the single most common "why isn't my new store on Google?" cause.

This card does NOT control which URLs are listed in the [[marketing-seo-sitemap]], the canonical tag from [[marketing-seo-canonical]], or the `<meta name="robots">` tag on individual pages (that's [[marketing-seo-deindex]]). Robots.txt blocks at the URL level before the page is fetched; meta robots influences how an already-fetched page is indexed.

## Sub-pages (in this cluster)

This feature is split into 3 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[seo-robots-editor]] — the admin card itself: the 3-row textarea, the "Are you sure?" confirm modal, the Cancel/Save bar, the save flow, the `marketing.seo` permission, what the merchant can and cannot do.
- [[seo-robots-served-file]] — what the storefront ACTUALLY serves at `/robots.txt`: the platform-appended safety block, the platform default template, the 5-minute cache, the `Last-Modified` header, sitemap reference, line-ending and size quirks.
- [[seo-robots-trial-block]] — the `Disallow: /` override for `trial` / `plan_expired` / development stores; why the saved body is ignored and there is no warning banner.

## Where to find it

Sidebar → Marketing → **SEO** → Main SEO settings → the **Robots.txt file** card (the fifth card on the page, immediately below the Sitemap card). The card sits on the new Vue page; a `marketing-seo-main=old` cookie falls back to the legacy `/admin/marketing/seo` Smarty page.

## What the merchant can do here

- Read and edit the current robots.txt body in a 3-row textarea, revert via Cancel, and Save (which opens a confirmation modal first). Full UI mechanics on [[seo-robots-editor]].
- Add a `Sitemap:` line manually to point crawlers at [[marketing-seo-sitemap]] (it is not auto-injected — see [[seo-robots-served-file]]).

What the merchant CANNOT do: edit the platform-appended safety block, override the trial / expired / dev blanket-block, add per-language robots.txt, validate syntax, or preview the final assembled file. Details split across [[seo-robots-editor]] and [[seo-robots-served-file]].

## Settings & fields

The card renders one element — the robots.txt body textarea (stored as `robots.txt` in store settings plus an `update_robots` timestamp). No client-side or server-side validation. Full field reference, defaults, and the confirm-modal copy are on [[seo-robots-editor]].

## Business rules

- **The served file ≠ the textarea.** Merchant text comes first, then a fixed Disallow + `Crawl-Delay: 3` block; an empty body falls back to the platform default template. See [[seo-robots-served-file]].
- **Trial / expired / dev stores are force-blocked** with `Disallow: /` and the saved body is ignored. See [[seo-robots-trial-block]].
- **A bad edit can de-index the whole store** (e.g. `Disallow: /`); the confirm modal is the only safety net. See [[seo-robots-editor]].
- **Editing is gated by the `marketing.seo` permission**; the public `/robots.txt` endpoint is open to anyone. See [[seo-robots-editor]].

## Related

- [[marketing-seo]] — Main SEO settings hub (this card lives here).
- [[marketing-seo-sitemap]] — sitemap URL (referenced from robots.txt via a manually-pasted `Sitemap:` line).
- [[marketing-seo-canonical]] — canonical tag toggle (canonical merges URL variants; robots.txt blocks URLs).
- [[marketing-seo-deindex]] — `<meta name="robots" content="noindex">` directive (controls indexing of pages crawlers reach; robots.txt blocks the fetch entirely).
- [[marketing-seo-meta]] — per-section meta titles & descriptions (no interaction with robots.txt).
- [[marketing-seo-301-redirects]] — per-URL 301 redirects.
- [[settings-domains]] — primary domain determines the host crawlers fetch `/robots.txt` from. Each domain serves the same robots.txt body.

## Open questions

None — all previously-flagged items resolved or distributed to the aspect pages.
