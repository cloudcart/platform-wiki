---
type: feature
nav_path: "Design → Modules"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Widgets", "Storefront widgets", "Widget editor", "Уиджети", "Widget", "Уиджет", "Modules", "Storefront modules"]
tags: [design, widgets]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 0
---

# Storefront Modules

## Purpose

The **Widgets** screen (also known as **Modules**) is the merchant's per-theme component configurator. It lists every editable module that the currently active theme has placed on the storefront — sliders, banners, showcases, text blocks, search bar, social-icons row, MailChimp newsletter pop-up, contact information block, Google map, blog modules, product modules, layout settings (header / footer / buttons / grid), promo bar, and more — and lets the merchant tune each one without touching the theme code.

Each module on the screen is a named **instance** of an underlying widget **type** (e.g., `homeText1` is an instance of `extra.text`; `bannersHomePage` is an instance of `extra.banner`). The same TYPE can appear multiple times under different names with independent settings. The instance list is **defined by the active theme** — switching themes via [[design-themes]] swaps the catalogue.

This page is the navigation pivot for everything that is **cross-cutting** across all module categories — the instance model, storage layering, tabs / groups taxonomy, save / reset pipeline, cache invalidation, and plan / `editable` gating. Per-category module catalogues live on the eight sibling hubs listed below.

## Where to find it

Sidebar → **Design** → **Widgets**.

The route is `/admin/storefront/widgets`. The breadcrumb reads "Settings".

Sub-routes (shared across every module category):

| Action | Route name | Path |
|--------|------------|------|
| List of widgets (tabs) | `admin.storefront.widgets` | `/admin/storefront/widgets` |
| Edit one widget | `admin.storefront.widget` | `/admin/storefront/widgets/{mapping}` |
| Save widget settings | `admin.storefront.widget_save` | `POST /admin/storefront/widgets/{mapping}/save` |
| Reset widget to defaults | `admin.storefront.widget_reset` | `/admin/storefront/widgets/{mapping}/reset` |
| Load a sub-template (partial) | `admin.storefront.widget_load` | `/admin/storefront/widgets/{mapping}/{template}/load` |
| Blog widgets side panel | `admin.storefront.widget.blog_panel` | `/admin/storefront/widgets/blog/panel` |

The `{mapping}` URL parameter is the module INSTANCE name (e.g., `homeText1`, `bannersHomePage`, `productsRelated`, `headerConfiguration`), NOT the module TYPE (e.g., `extra.text`, `extra.banner`, `product.related`, `layout.header`). See [[design-modules-cross-instance-model]].

> **Only `/admin/storefront/widgets` is a real, linkable page.** Every other row above is an **internal panel / AJAX endpoint** the Modules screen calls behind the scenes — the module editor opens as a **side panel inside** the grid, it is not a standalone page. Opening a `/admin/storefront/widgets/{mapping}` URL (or the `…/save`, `…/reset`, `…/load`, `…/blog/panel` endpoints) directly in the browser just returns the bare form fragment / raw markup, not a usable editor. **When telling a merchant where to edit a module, link them to `/admin/storefront/widgets` and then give the steps** — open the right tab, then click the module's card to open its settings panel. Never hand out a `{mapping}` URL as a clickable link.

## What the merchant can do here

This hub does not own merchant actions directly — every action is documented on the aspect that owns its mechanics. From the Widgets screen the merchant can:

- See modules organised into **7 top-level tabs** and **11 sidebar groups** — see [[design-modules-cross-tabs-groups]].
- Open any editable module card to see its **edit side panel** and adjust settings — fields per module TYPE live on the per-category hubs.
- Click **Save widget** / **Reset widget** / **Cancel** — full pipeline in [[design-modules-cross-save-reset]].
- Get instant storefront pickup of the new settings on the next request — see [[design-modules-cross-cache-invalidation]].

The merchant CANNOT:

- ADD a new module instance to the storefront from this screen — the catalogue is fixed by the active theme. To add modules to a page-builder Dynamic page, use [[marketing-landing-pages]].
- RENAME or DELETE an instance — turning the module off via its enable / disable switch is the closest equivalent.
- Configure modules the active theme has flagged `editable: no`, or modules whose mapped class doesn't exist — they don't appear in the list. See [[design-modules-cross-gating]].
- Configure paid modules without an active plan — the **Video slider** (`extra.videoSlider`) requires the `video_slider_widget` plan feature. See [[design-modules-cross-gating]].

## Settings & fields

This hub does not document module fields directly — every field table lives on a per-category sibling hub. Use this table to find the right sibling:

| Looking for fields on | Go to |
|-----------------------|-------|
| Banner / carousel / text / background image / text-carousel / video-slider / yotpo-reviews | [[design-modules-content]] |
| Header / footer / buttons / grid templates | [[design-modules-layout]] |
| Product filters / showcases / related / linked / last-viewed / bundles / discounts | [[design-modules-products]] |
| Blog list / recent articles / recent comments / blog panel | [[design-modules-blog]] |
| Search / promo bar / social icons / button-to-top / logo / navigation-links | [[design-modules-navigation]] |
| Newsletter / contact info / Google map / contact-form / cc-form / product / request-review | [[design-modules-engagement]] |
| Page-builder-only blocks (add-to-cart, button, separator, title, video, code, store-locations, etc.) | [[design-modules-page-builder]] |
| Vendors / providers / leasing / authorize / wishlist / categoryProperties / page / utilities (system) | [[design-modules-utility]] |

The **cross-cutting** mechanics — how those fields are stored, validated, cached, and gated — are split into the aspects in the next section.

## Sub-pages (in this cluster)

This screen's cross-cutting mechanics are split into 6 aspects. The Assistant should drill into the aspect that matches the question, not read every page.

- [[design-modules-cross-instance-model]] — instance vs type, the `{mapping}` URL parameter, multi-instancing the same type, theme-defined catalogue, per-site overrides.
- [[design-modules-cross-storage]] — three-layer storage (theme JSON + per-site overlay + merchant saves); JSON blob per instance; orphaned settings on theme switch.
- [[design-modules-cross-tabs-groups]] — the 7 tab keys (`store` / `user` / `blog` / `contact` / `extra` / `layout` / `custom`) and 11 sidebar group keys; visibility rules; client-side filtering.
- [[design-modules-cross-save-reset]] — Save / Reset / Cancel actions; per-type restriction validation; the sub-template load route for inline "+ Add" rows; the blog panel route.
- [[design-modules-cross-cache-invalidation]] — per-site cache key bump on save / reset; storefront pickup timing; no manual cache-clear surface.
- [[design-modules-cross-gating]] — `editable: no` hiding, missing-class silent skip, plan-feature gates (`video_slider_widget`), permission requirement.

## Business rules

The cross-cutting rules are stated in full on the aspect pages. The minimum rules to know at the hub level:

- **Catalogue is theme-defined**; instances are NAMED slots — see [[design-modules-cross-instance-model]].
- **Settings are stored as JSON per instance** — see [[design-modules-cross-storage]].
- **Save validates against per-type restrictions; unknown fields drop silently. Reset has no undo** — see [[design-modules-cross-save-reset]].
- **Save and Reset both regenerate the per-site cache key** — see [[design-modules-cross-cache-invalidation]].
- **`editable: no`, missing-class, and paid widgets without plan feature are gated** — see [[design-modules-cross-gating]].
- **The Widgets screen requires storefront-design permission** — see [[settings-staff]]. (verify)

## Related

- [[design]] — parent Design pillar.
- [[design-themes]] — theme picker; theme choice controls which module instances appear here.
- [[design-navigation]] — sibling; configures the `main` and `footer` menu trees (distinct from the `navigation.links` module instances configured via [[design-modules-navigation]]).
- [[marketing-landing-pages]] — Dynamic pages use the page-builder, which reuses the same module config templates (see [[design-modules-page-builder]]).
- [[design-modules-content]] — sibling hub: banners, carousels, text, background images, yotpo-reviews, video-slider.
- [[design-modules-layout]] — sibling hub: header / footer / buttons / grid settings.
- [[design-modules-products]] — sibling hub: filters, showcases, related / linked / last-viewed.
- [[design-modules-blog]] — sibling hub: blog list, recent articles, recent comments.
- [[design-modules-navigation]] — sibling hub: search, promo bar, social, navigation-links, button-to-top.
- [[design-modules-engagement]] — sibling hub: newsletter, contact info, Google map, forms.
- [[design-modules-page-builder]] — sibling hub: page-builder-only blocks.
- [[design-modules-utility]] — sibling hub: system modules, utility editable modules.
- [[plan-gates]] — `video_slider_widget` plan feature gates the Video Slider module.

## Open questions

- 📡 **Per-language module content.** With `multylang`, text fields accept per-language entries via the language switcher. (verify)
- ⏸️ **Permission key.** Storefront-design permission key for this screen, to be confirmed against [[settings-staff]]. (verify)
