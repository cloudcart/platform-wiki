---
type: feature
nav_path: "Marketing → SEO → Sharing → Default Open Graph image"
route_name: seo-main
route_path: /admin/marketing-new/seo
aliases: ["Main sharing picture", "Default og:image", "og:image default", "Open Graph image", "Cover image for sharing", "Facebook share preview image", "Снимка за споделяне", "OG изображение по подразбиране", "Споделяне снимка"]
tags: [marketing, seo, sharing, open-graph, distribution]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
> Part of [[marketing-seo-sharing]]. See the hub for the other aspects (the sharing toolbar, storage & save mechanics).

# Default Open Graph image (`Main sharing picture`)

## Purpose

The **Main sharing picture** field on the "Share a product" card sets the store-wide **default `og:image`** — the fallback Open Graph cover image that Facebook, LinkedIn, X/Twitter, Viber, etc. use to build a link preview when a storefront page is shared and that page has **no image of its own**. Stored as `setting('og_image_url')`.

This is the single field on the whole Sharing card that has a real, theme-independent effect. Unlike the toolbar toggles (which are hard-disabled on modern themes — see [[seo-sharing-toolbar]]), the `og:image` is read directly when the storefront renders each page's `<meta property="og:image">` tag.

## Where to find it

Sidebar → Marketing → **SEO** → **"Share a product"** card → the **Main sharing picture** tile at the bottom of the card (below the toolbar layout selects, after the last horizontal rule). Route `/admin/marketing-new/seo`. The tile is a 160 × 100 px thumbnail with a trash icon (clear) and a rotate icon (reopen picker).

## What the merchant can do here

- Upload, replace, or delete the default cover image. The tile opens the standard **Filemanager image picker** (modal).
- Clear the image with the trash icon (sets `og_image_url` back to empty).
- Re-open the picker with the rotate icon to swap the image.

### What the merchant CANNOT do here

- Set a **per-product** `og:image` — that lives on the product editor ([[product]]); per-category on [[category]]; per-CMS-page on the CMS page editor. This card only sets the **store-wide fallback**.
- Set `og:title` or `og:description` defaults — those come from the section metas on [[marketing-seo-meta]] (per page-type), with per-entity fallback to the entity's own meta title / description.
- Get any size / aspect-ratio validation on upload — there is none. Facebook recommends 1200 × 630 px.

## Settings & fields

| Field | What it does | Default | Validation / notes |
|-------|--------------|---------|--------------------|
| **Main sharing picture** (image upload — 160 × 100 px thumbnail tile) | Default `og:image` for the entire storefront; fallback when a shared page has no image of its own. Stored as `setting('og_image_url')`. | empty | URL selected via the Filemanager image picker. Trash icon clears the URL; rotate icon reopens the picker. **No size / aspect-ratio validation** — Facebook recommends 1200 × 630 px. |

`og_image_url` is the **only** field on this card written to the store's global settings table — everything else goes to a theme-scoped module row (see [[seo-sharing-storage-save]]). Because it is global, it **survives theme changes**.

## Business rules

### The fallback chain — where this image kicks in

The merchant-uploaded image is used everywhere the storefront generates a `<meta property="og:image">` tag **and** the per-entity OG image is empty. Typical pages where this fallback applies:

- Home page (no per-entity og:image — falls back to this one).
- Contact / About / generic CMS pages without their own OG image.
- Brand / vendor index pages.
- Blog index page.
- Any product, category, vendor, page, or blog article whose own OG image field is blank.

A page that DOES set its own OG image (e.g. a product with an image, or a CMS page with an explicit OG field) uses that image and ignores this default.

### Why this is the highest-impact field on the card

If the merchant doesn't set this image, link previews for the pages above render either with no cover image (Facebook will pick an arbitrary body image, sometimes the wrong one) or completely blank — a frequent source of **"my Facebook share preview is broken"** support tickets. Setting a 1200 × 630 px branded image here is the single highest-impact action on the entire Sharing card.

### Support note — preview caching is external

Even after the merchant sets or changes this image, social platforms cache the old preview. Facebook's Sharing Debugger (and the equivalent re-scrape tools on LinkedIn / X) must be run to force a refresh — the platform cannot purge an external network's preview cache. (verify — exact merchant-facing wording of this guidance not yet standardised)

## Related

- [[marketing-seo-sharing]] — hub.
- [[seo-sharing-toolbar]] — the sharing toolbar this field shares a card with (but is functionally independent of).
- [[seo-sharing-storage-save]] — why `og_image_url` survives theme changes while the toolbar config does not.
- [[marketing-seo-meta]] — source of the `og:title` / `og:description` defaults (this card sets only the image).
- [[product]] — per-product Open Graph image override.
- [[category]] — per-category OG image override.

## Open questions

- Exact merchant-facing wording for the "re-scrape on Facebook/LinkedIn after changing the image" guidance is not standardised. (verify)
