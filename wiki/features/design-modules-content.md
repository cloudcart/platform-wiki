---
type: feature
nav_path: "Design → Modules → Content"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Content modules", "Banner module", "Carousel module", "Slider module", "Text module", "Title module", "Video module", "Video slider module", "Text carousel module", "Separator module", "HTML line module", "Slideshow module", "Модули - Съдържание"]
tags: [design, modules, content, banner, carousel, video]
plan_gates: ["video_slider_widget", "storefront_builder", "static_pages"]
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Storefront Modules — Content

## Purpose

The **Content** module group covers the building blocks merchants use to fill the storefront with marketing material — image carousels, banner grids, rich-text blocks, headings, videos, promo strips, separators. They turn a generic theme into a personalised storefront with the merchant's products, photography and messaging.

Most content modules live on the homepage and category-listing pages, but can also be slotted into static pages, the cart sidebar, checkout, product details and other surfaces depending on the active theme. Many appear MULTIPLE times under different INSTANCE names (e.g., `homeText1`, `homeText2`, `homeText3` are three independent text blocks all backed by the same module type).

This page is the navigation pivot — drill into the aspect that matches the question.

## Sub-pages (in this cluster)

### Per-module pages (one module TYPE per page)

- [[design-module-banner]] — image / script banner grid (1–24 slots, gallery / slider mode, 8 link kinds).
- [[design-module-background-image]] — decorative background image for theme slots.
- [[design-module-carousel]] — homepage hero slider (1–15 image / video slides, captions, HTML overlays, schedules).
- [[design-module-text]] — static rich-text block (TinyMCE editor, 1–300 000 chars).
- [[design-module-text-carousel]] — text-only rotating carousel (testimonials, quotes).
- [[design-module-video-slider]] — Reels-style video carousel; PLAN-GATED by `video_slider_widget`.
- [[design-module-code]] — raw HTML / JS block (no sanitisation; primarily a page-builder block).
- `googleMap` — Google Maps embed with pins (in the **Contacts** tab); canonical page is in the engagement cluster — see [[design-modules-engagement]].
- [[design-module-yotpo-reviews]] — Yotpo reviews surface; requires Yotpo app + App Key.

### Cluster-wide aspect pages

- [[design-modules-content-catalogue]] — full content-module list with map keys, instance examples, and which aspect documents each one.
- [[design-modules-content-carousel]] — the `carousel` hero slider walkthrough.
- [[design-modules-content-banners]] — the banner grid family walkthrough + the `htmlLine` promo strip cross-reference.
- [[design-modules-content-text]] — text-block / text-carousel walkthrough.
- [[design-modules-content-video]] — `videoSlider` + page-builder `video` walkthrough.
- [[design-modules-content-page-builder]] — `title`, `separator`, page-builder `video` modules exposed ONLY inside the Dynamic page builder.
- [[design-modules-content-storage]] — three-layer storage, Save / Reset pipeline, plan-gate enforcement, cache invalidation.

## Where to find it

Sidebar → **Design** → **Modules**. Content modules are split across two tabs:

| Tab | Modules |
|-----|---------|
| **Others** (`extra` category) | `carousel`, banners (`bannersHomePage`, `homeSingleBanner`, `pagesBanner`, `newProductsBanners`, `bannerInSidebar`, `productShowcaseBanners`, `bannersTextPage`), `htmlLine` (promo bar), text blocks (`homeText1-3`, `headerText`, `footerText`, `cartText`, `welcomeText`, `homeVideoText`, etc.), `textCarousel`, `videoSlider` |
| **Page-builder only** | `video`, `title`, `separator` — exposed via the **Dynamic page** builder in [[marketing-landing-pages]], not the Modules list |

Within the **Others** tab, the sidebar groups modules into **Slider**, **Images**, **Text fields**, and **Top bar** — clicking a group label filters the right-hand list.

## What the merchant can do here

- Identify which content modules the active theme exposes.
- Open an editable module side panel and adjust settings — drill into the right aspect for field tables.
- Save / Reset / Cancel and the master Enable / disable toggle — standard actions across every editable module (full pipeline in [[design-modules-content-storage]]).
- Reset any editable module to theme-shipped defaults.
- Inside the Dynamic page builder ([[marketing-landing-pages]]), drop in page-builder-only modules (`title`, `video`, `separator`) — see [[design-modules-content-page-builder]].

What the merchant CANNOT do here:

- Add a NEW content module instance to the storefront — the slots are defined by the theme. For a brand-new content block, use the page builder in [[marketing-landing-pages]] on a Dynamic page.
- Rename a module instance.
- Use the `videoSlider` module without the `video_slider_widget` plan feature — see [[design-modules-content-video]].
- Configure modules the theme has flagged as not-editable (`editable: 'no'` in theme JSON — see [[design-modules-content-storage]]).

## Settings & fields

This hub does not document fields directly — every field table lives in the aspect that owns it. Use the catalogue to find the right aspect:

- The hero slider `carousel` → [[design-modules-content-carousel]].
- Any banner module (`bannersHomePage`, `homeSingleBanner`, etc.) → [[design-modules-content-banners]].
- Any text block (`homeText1`, `footerText`, `cartText`, etc.) or `textCarousel` → [[design-modules-content-text]].
- `videoSlider` or the page-builder `video` block → [[design-modules-content-video]].
- `title`, `separator`, and page-builder-only `video` settings → [[design-modules-content-page-builder]].
- The `htmlLine` promo strip — settings live on [[design-modules-navigation]] (sibling cluster); [[design-modules-content-banners]] explains why it is dual-classified.

Common field patterns across editable content modules:

- **Enable / Disable toggle** in the top-right of every editable module.
- **`amount`** (number of slides / banners) and **`per_row`** for grid modules.
- **TinyMCE rich-text editor** for free-form content (text blocks, slide HTML overlays, testimonial text).
- **Image picker** — Internal (file manager) or External (CDN URL); some modules also support video.
- **Link picker** — 8 link kinds: Product / Category / Vendor / Blog / Article / Page / Section / External.
- **Autoplay + Interval** for carousel-type modules; **From / To** date range for slide-level scheduling (carousel, text carousel).

## Business rules

### Each instance is an INDEPENDENT slot

`homeText1`, `homeText2`, `homeText3` are three SEPARATE instances of the same Text module — each with its own settings. Editing one does NOT change the others; the instance name tells the merchant which storefront slot it fills. Full instance list in [[design-modules-content-text]].

### Theme controls which instances exist

The list of named instances is declared in the active theme's config. Switching themes changes the catalogue — settings for instances absent from the new theme are kept in storage but not editable. Merge mechanics in [[design-modules-content-storage]].

### Per-slide scheduling for time-windowed campaigns

The carousel, text carousel, and (in some themes) banner modules support per-slide **From / To** dates. Outside the window the slide is automatically hidden — useful for Black Friday / Christmas campaigns set up weeks in advance.

### Image picker — Internal vs External

For image-bearing modules the merchant picks the CloudCart file manager (Internal) or a CDN URL (External). External URLs are faster but require the merchant to keep the image alive on the third-party server.

### Plan-gating

Only `videoSlider` is plan-gated at the module level (requires `video_slider_widget` — see [[design-modules-content-video]]). The Page Builder is gated by `storefront_builder` and page count by `static_pages` — see [[design-modules-content-page-builder]]. All other content modules are universally available.

### Page-builder-only modules

`title`, `separator`, `video` exist as module form templates but are exposed ONLY through the Dynamic page builder in [[marketing-landing-pages]], not the Modules list. See [[design-modules-content-page-builder]].

### Cache invalidation is automatic

Save and Reset both bump a per-site cache key, so merchants see changes on the very next storefront request — no manual cache clear. Full pipeline in [[design-modules-content-storage]].

## Related

- [[design-modules]] — parent module catalogue (overview + tab structure).
- [[design]] — pillar hub for Design.
- [[design-themes]] — theme picker; theme controls which instance names exist for each module type.
- [[design-modules-navigation]] — sibling module category (Navigation: menus, search, logo, user controls, back-to-top, promo bar — owns the `htmlLine` settings table).
- [[design-modules-products]] — sibling module category (Product modules — showcase, related, last viewed).
- [[design-modules-engagement]] — sibling module category (Engagement modules — Mailchimp, social, contact).
- [[design-modules-blog]] — sibling module category (Blog modules).
- [[design-modules-utility]] — sibling module category (Utility / layout modules).
- [[marketing-landing-pages]] — Dynamic page builder hosts page-builder-only modules and overrides for any content module.
- [[apps-video-slider-widget]] — dedicated app surface for the Video Slider module.
- [[plan-gates]] — `video_slider_widget` / `storefront_builder` / `static_pages` plan features that bound this cluster.

## Open questions

None at the hub level — open questions are distributed to the aspects that own them. See each aspect's own *Open questions* section.
