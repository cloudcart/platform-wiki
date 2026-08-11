---
type: feature
nav_path: "Design → Modules → Content → Catalogue"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Content modules catalogue", "Content module list", "Content module map keys", "Content модули списък"]
tags: [design, modules, content, catalogue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Content modules — Catalogue

> Part of [[design-modules-content]]. See the hub for editable settings, page-builder blocks, storage and plan gates.

## Purpose

A single-glance table of every module that lives under **Design → Modules → Content**, sorted by module type and the aspect that documents its settings. Use this page to find a module by `map` key or instance name and jump to the right aspect.

## Where to find it

Sidebar → **Design** → **Modules** — then look in:

| Where on the Modules screen | Content modules |
|-----------------------------|-----------------|
| **Others** tab (`extra` category) — Slider group | `carousel`, `textCarousel`, `videoSlider` |
| **Others** tab — Images group | `bannersHomePage`, `homeSingleBanner`, `pagesBanner`, `bannerInSidebar`, `newProductsBanners`, `productShowcaseBanners`, `bannersTextPage` |
| **Others** tab — Text fields group | `homeText1`, `homeText2`, `homeText3`, `welcomeText`, `homeWelcome`, `headerText`, `headerLeft`, `headerRight`, `footerText`, `footerContent`, `footerContacts`, `cartText`, `checkoutText`, `checkoutPrice`, `checkoutSideText`, `checkoutSignInGuestText`, `checkoutSignInLoginText`, `checkoutSignInRegisterText`, `productText`, `homeTopBanner`, `homeTopTextAfterCategoryShowcase`, `homeVideoText` |
| **Others** tab — Top bar group | `htmlLine` (settings owned by [[design-modules-navigation]]) |
| **Page builder only** | `title`, `separator`, `video` |

## What the merchant can do here

- Identify which content modules the active theme exposes (and which ones it doesn't).
- Recognise that the same module TYPE (`extra.text`) is instanced multiple times under different names — each instance is a separate slot.
- Pick the right aspect page to drill into for field-level documentation.

## Settings & fields

There are no settings on this catalogue page — fields live in the aspect that owns each module.

### Master catalogue table

| Module key | Map | Where it renders (typical) | Drill into |
|------------|-----|----------------------------|------------|
| `carousel` | `extra.carousel` | Homepage hero slider (most themes) | [[design-modules-content-carousel]] |
| `bannersHomePage` | `extra.banner` | Homepage banner row | [[design-modules-content-banners]] |
| `homeSingleBanner` | `extra.banner` | One large homepage banner | [[design-modules-content-banners]] |
| `pagesBanner` | `extra.banner` | Static pages | [[design-modules-content-banners]] |
| `bannerInSidebar` | `extra.banner` | Category sidebar | [[design-modules-content-banners]] |
| `newProductsBanners` | `extra.banner` | Near the "New products" section | [[design-modules-content-banners]] |
| `productShowcaseBanners` | `extra.banner` | Inside product-showcase rows | [[design-modules-content-banners]] |
| `bannersTextPage` | `extra.banner` | Text / blog-style pages | [[design-modules-content-banners]] |
| `homeText1` / `homeText2` / `homeText3` | `extra.text` | Three independent homepage slots | [[design-modules-content-text]] |
| `welcomeText` / `homeWelcome` | `extra.text` | Homepage hero / welcome block | [[design-modules-content-text]] |
| `headerText` / `headerLeft` / `headerRight` | `extra.text` | Header chrome | [[design-modules-content-text]] |
| `footerText` / `footerContent` / `footerContacts` | `extra.text` | Footer columns | [[design-modules-content-text]] |
| `cartText` | `extra.text` | Cart page | [[design-modules-content-text]] |
| `checkoutText` / `checkoutPrice` / `checkoutSideText` | `extra.text` | Checkout page | [[design-modules-content-text]] |
| `checkoutSignInGuestText` / `checkoutSignInLoginText` / `checkoutSignInRegisterText` | `extra.text` | Checkout, by sign-in state | [[design-modules-content-text]] |
| `productText` | `extra.text` | Product-detail page | [[design-modules-content-text]] |
| `homeTopBanner` / `homeTopTextAfterCategoryShowcase` / `homeVideoText` | `extra.text` | Homepage anchor-specific slots | [[design-modules-content-text]] |
| `textCarousel` | `extra.textCarousel` | Rotating testimonials / quotes / messages | [[design-modules-content-text]] |
| `videoSlider` | `extra.videoSlider` | Reels-style video showcase (plan-gated) | [[design-modules-content-video]] |
| `htmlLine` | `extra.htmlLine` | Promo strip (top / bottom of storefront) | [[design-modules-navigation]] (settings owned by Navigation cluster) |
| `title` | (page-builder) | Inside a Dynamic page | [[design-modules-content-page-builder]] |
| `separator` | (page-builder) | Inside a Dynamic page | [[design-modules-content-page-builder]] |
| `video` | (page-builder) | Inside a Dynamic page | [[design-modules-content-page-builder]] |

## Business rules

### Instance vs type — the most-confused distinction

`homeText1` and `headerText` look like different "modules" on the screen, but internally they are TWO INSTANCES of the same type (`extra.text`). Saving content into `homeText1` does not propagate to `headerText`. The instance name is the slot identifier; the map (`extra.text`) is the renderer. See [[design-modules-content-storage]] for storage mechanics.

### Theme decides which instances exist

The set of named instances above is the union across themes. Any individual theme ships only a SUBSET — the active theme's `theme.json` declares which names get cards on the Modules screen. Saved data for absent instances stays in storage but is unreadable until the theme reappears.

### Group filters in the sidebar

The Others-tab sidebar groups (Slider / Images / Text fields / Top bar) are UI filters only — they don't change the underlying storage. Clicking a group filters the right-hand list to modules categorised under that grouping in the platform's module metadata.

### `htmlLine` is dual-classified

`htmlLine` is both a Content module (it carries a marketing message + CTA) and a Navigation module (it sits in the header / footer chrome). The settings live on [[design-modules-navigation]] — this cluster only references it. See [[design-modules-content-banners]] for the dual-classification note.

### Page-builder modules are absent from the Modules screen

`title`, `separator`, and `video` are registered modules but the Modules controller does not list them — they are exposed only inside the Dynamic page builder. See [[design-modules-content-page-builder]] for how to reach them.

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-carousel]] — `carousel` field tables.
- [[design-modules-content-banners]] — banner module settings.
- [[design-modules-content-text]] — text + text carousel settings.
- [[design-modules-content-video]] — `videoSlider` settings and plan-gating.
- [[design-modules-content-page-builder]] — Dynamic-page-only blocks.
- [[design-modules-content-storage]] — storage / cache / save pipeline.
- [[design-modules-navigation]] — owns the `htmlLine` promo-bar settings table.
- [[design-themes]] — theme JSON decides which instances appear.
- [[marketing-landing-pages]] — Dynamic page builder.

## Open questions

None.
