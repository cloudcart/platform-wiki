---
type: feature
nav_path: "Design → Modules → Cross-cutting → Instance model"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Module instance", "Module type", "Module mapping", "Module map", "Module instance name", "Module instance vs type", "homeText1", "bannersHomePage", "Theme modules block", "Module catalogue"]
tags: [design, modules, instance-model, theme]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Storefront Modules — Instance model

> Part of [[design-modules]]. See the hub for the other cross-cutting aspects (storage, tabs / groups, save / reset, cache invalidation, gating).

## Purpose

The "instance vs type" distinction is the **single most important model** for understanding the Modules screen. Every card the merchant sees is a named **instance** bound to an underlying module **type** — and the same TYPE can appear multiple times as different instances, each with its own settings. This aspect documents how instances are named, where the list comes from, and what the `{mapping}` URL parameter actually refers to.

Use this aspect when investigating: *"why do I see three text modules — homeText1, homeText2, homeText3?"*, *"why did my homepage banner settings disappear after switching themes?"*, *"can I add a fourth text block?"*, *"what does the URL `/admin/storefront/widgets/homeText1` mean?"*.

## Where to find it

Sidebar → **Design** → **Modules**. Each card on the screen is one instance. The `{mapping}` segment in the edit URL is the instance name.

## What the merchant can do here

- See the list of instances the active theme has declared — one card per instance.
- Open any instance and tune its settings independently of other instances of the same type — see [[design-modules-cross-save-reset]].
- See instances grouped into tabs and sidebar groups — see [[design-modules-cross-tabs-groups]].

The merchant CANNOT:

- ADD a new instance from this screen — the catalogue is fixed by the active theme.
- RENAME an instance — the name (e.g., `homeText1`) is set by the theme.
- DELETE an instance — turning the module off via its enable / disable switch is the closest equivalent.
- Move an instance to a different storefront slot — the slot is bound to the instance name by the theme.

To add new modules to a specific page, use the page-builder via [[marketing-landing-pages]] (Dynamic page type) — see [[design-modules-page-builder]].

## Settings & fields

This aspect has no editable fields — it documents the instance / type model.

### Instance name → module type (the `map`)

Every instance carries a `map` value that points to the module TYPE. Examples (theme-defined, verbatim):

| Instance name | `map` (type) | Notes |
|---------------|--------------|-------|
| `homeText1` / `homeText2` / `homeText3` | `extra.text` | Three independent text-block instances of the same type. |
| `homeText1Background` / `homeText2Background` / `homeText3Background` | `extra.backgroundImage` | Background pictures bound to the text-block slots. |
| `headerConfiguration` | `layout.header` | The header template + menu picker. |
| `footerConfiguration` | `layout.footer` | Footer template picker. |
| `buttonsConfiguration` | `layout.button` | Global button styling. |
| `gridConfiguration` | `layout.grid` | Product-grid spacing. |
| `filters` | `product.filters` | Master settings for ALL product-listing pages. |
| `carousel` / `homepageCarousel` | `extra.carousel` | Homepage slider. |
| `bannersHomePage` / `homeSingleBanner` / `pagesBanner` / `newProductsBanners` / `bannerInSidebar` / `productShowcaseBanners` | `extra.banner` | Multiple banner-grid instances. |
| `productsRelated` / `productsRelated2` / `productsCombine` | `product.related` | "Related products" / "Top products" / "Match with" rows. |
| `lastViewed` | `product.lastViewed` | Last-viewed row. |
| `productInBundles` | `product.productInBundles` | "Product in packages" row. |
| `discounts` | `product.discounts` | Discounts row. |
| `showcaseBrand` / `showcaseBrands1` / `showcaseBrands2` / `showcaseCategories` / `showcaseBestSellersProducts` / `bundleShowcase` | `product.showcase` / `product.productShowcase` / `product.bundleShowcase` | Showcase rows. |
| `blog` / `blogHome` / `recentArticles` / `recentComments` | `blog.blog` / `blog.recentArticles` / `blog.recentComments` | Blog modules. |
| `newsletter` | `mailchimp.newsletter` | Mailchimp signup pop-up. |
| `contactInformation` / `googleMap` | `contact.information` / `contact.googleMap` | Contact blocks. |
| `htmlLine` | `extra.htmlLine` | Top promo bar. |
| `search` | `extra.search` | Search bar. |
| `navigationLinks` / `navigationLinksPage` / `footerLinks1` / `footerLinks2` / `footerLinks3` | `navigation.links` | Flat link blocks (distinct from the `main` / `footer` trees in [[design-navigation]]). |
| `yotpoReviews` | `extra.yotpoReviews` | Yotpo reviews row (legacy, single enable toggle). |
| `social` | `extra.social` | Social-icons row. |
| `videoSlider` | `extra.videoSlider` | Plan-gated (see [[design-modules-cross-gating]]). |
| `pageLoader` / `latestNewsBackground` / `categoryShowcaseBackground` / `newProductsBackground` / `homeTopBackground` / `homeTopAfterCategoryBackground` / `homeTextBackground` / `footerTextBackground` / `headerImage1` / `headerImage2` / `homeVideoBackgroundImage` | `extra.backgroundImage` | Theme-slot backgrounds. |

The full list is theme-specific — the table above is illustrative, not exhaustive. (verify)

### What the `{mapping}` URL parameter is

The `{mapping}` segment in `/admin/storefront/widgets/{mapping}` is the INSTANCE name — not the TYPE. So the `homeText1` endpoint serves the first text-block instance's panel; `bannersHomePage` serves the homepage banner row's panel. This is an **internal panel endpoint** the Modules grid loads over AJAX when the merchant clicks the module's card — it is **not** a page to navigate to directly (opened on its own it returns just the bare form fragment). The merchant always starts at `/admin/storefront/widgets`, opens the right tab, and clicks the card. The instance name is the **key** for the merchant's saved settings — see [[design-modules-cross-storage]].

## Business rules

### The module catalogue is defined by the active theme

What shows up on `/admin/storefront/widgets` is the active theme's declared `modules` block, merged with any per-site overrides (custom modules the merchant has had CloudCart add). Switching themes via [[design-themes]] replaces the catalogue — settings for instances that don't exist in the new theme are kept in the database but orphaned (never read). See [[design-modules-cross-storage]].

### Each instance is a NAMED slot — not a free-standing component

An instance like `homeText1` is bound to a specific slot on the theme (e.g., the first text block on the homepage). The theme decides WHERE on the storefront the slot renders; the merchant only configures WHAT goes in the slot via this screen. To move content to a different slot, the merchant either edits a different instance or switches themes.

### The same TYPE can appear multiple times

A module TYPE like `extra.text` can be instanced multiple times — `homeText1`, `homeText2`, `homeText3` all use the same form layout but store their settings independently (each is its own JSON blob keyed by instance name). The save and reset pipelines run per-instance — see [[design-modules-cross-save-reset]].

### Per-site overrides — adding instances without forking the theme

A per-site override layer (sister-site `site_widgets.site_<site_id>` config) can ADD or REPLACE instances for one specific store on top of the theme defaults. This is how special-store carve-outs are layered without forking the active theme. Full layering rules in [[design-modules-cross-storage]]. (verify)

### Category override per instance

An instance can override its tab assignment via a `category` key in the theme config; otherwise it inherits the tab from its module type's mapping group. See [[design-modules-cross-tabs-groups]] for the seven categories.

## Related

- [[design-modules]] — hub.
- [[design-modules-cross-storage]] — the storage layering that turns a theme-declared instance into a saved settings row.
- [[design-modules-cross-tabs-groups]] — how instances are sliced into tabs and groups.
- [[design-modules-cross-save-reset]] — how per-instance settings persist.
- [[design-themes]] — theme picker; the theme owns the `modules` block that defines the catalogue.
- [[marketing-landing-pages]] — Dynamic pages where the merchant CAN add new module blocks (via the page-builder, see [[design-modules-page-builder]]).

## Open questions

- ⏸️ **Per-site override surface.** The sister-site `site_widgets.site_<site_id>` overlay is configured outside the merchant admin — exact onboarding flow to be confirmed. (verify)
- 📡 **Custom instance registration.** Some stores ship custom instances that the standard theme doesn't declare — the route to add them (CloudCart-staff-only vs merchant-driven) is unclear. (verify)
