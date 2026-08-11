---
type: concept
nav_path: "Concept → Module vs Page Builder block"
route_name: (none)
route_path: (none)
aliases: ["Module vs Page Builder block", "Page Builder block vs Module", "Module vs Block", "Module and block difference", "Storefront module vs block", "Theme module vs Page Builder block", "Static page block vs module", "Widget vs block", "Модул срещу блок", "Блок срещу модул", "Разлика между модул и блок", "Конструктор на страници срещу модули"]
tags: [design, modules, page-builder, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Module vs Page Builder block

## Definition

CloudCart has two storefront-composition surfaces that look similar but serve different jobs:

- A **Module** ([[design-modules]]) is a **pre-defined slot in the active theme's layout**. The theme decides which module instances exist and WHERE each one renders (homepage, sidebar, category, product page, cart, checkout). The merchant configures the module ONCE and it appears on every page that includes its slot. Module settings are stored globally per `(theme, instance_name)` — switching themes hides them. See [[widget-vs-pb-module-mechanics]].
- A **Page Builder block** ([[marketing-landing-pages]] — Dynamic page type) is a **drag-and-drop content element on a Dynamic page**. The merchant composes a Dynamic page by dragging blocks onto rows; each block lives only on that specific page. Block content is stored per-page — switching themes does NOT hide it. See [[widget-vs-pb-block-mechanics]].

Both surfaces use the **same library of 25 form templates**. About 13 templates serve BOTH surfaces; the other ~12 are Page-Builder–only (e.g., `code`, `store_locations`, `cc_form`, `add-to-cart`). See [[widget-vs-pb-shared-template-library]].

The distinction matters because the SAME template type (say, a banner) has different lifecycles depending on where the merchant placed it. A `banner` Module configured once renders on every page with its slot; a `banner` Block dragged onto a Dynamic page renders only on that page.

Module screen route: `/admin/storefront/widgets`. Page Builder route: `/admin/marketing/pages/builder/<page_id>`.

## Sub-pages (in this cluster)

This concept is split into 5 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[widget-vs-pb-module-mechanics]] — module instance identity, `theme.json` slots, `front_widget` storage shape, the 25 registered module classes (app-conditional `yotpo-reviews` / `brand-model` / `product_review` / `store_locations`), system modules (`navigationMain` / `navigationFooter` / `logo` / `userControls`), `editable: 'no'` lockdown.
- [[widget-vs-pb-block-mechanics]] — Dynamic page composition (rows + flex layout + palette), per-page storage in the Page content JSON, version history with **500-snapshot cap per page**, `autoSave` snapshot-per-change + fresh preview URL.
- [[widget-vs-pb-shared-template-library]] — the 25 form templates (`banner`, `text`, `carousel`, `code`, `store_locations`, `order-details`, etc.), which ~13 serve both surfaces vs the ~12 Page-Builder–only, shared Smarty rendering stack.
- [[widget-vs-pb-theme-switch-behavior]] — modules hide on theme switch (settings preserved by theme slug); blocks survive on Dynamic pages (placeholder fallback if the new theme doesn't ship a block type).
- [[widget-vs-pb-system-pages-and-restrictions]] — Dynamic page assigned to `home` / `thank_you` / `error.404` / `blog.list` / `blog.view`, the only two enforced `PageRestriction` rules (`blog.list` requires `blog-list` block, `blog.view` requires `blog-view` block), plan gates `storefront_builder` + `video_slider_widget`, hardcoded `site_id` allowlist (`3819`, `9674`) bypass. (verify)

## Scope

What this concept covers (across the 5 sub-pages):

- The module definition + per-theme slot model.
- The Page Builder block definition + per-page composition model.
- The shared 25-template form library.
- Theme-switch asymmetry (modules hide, blocks survive).
- System-page assignment + the only enforced required-module rules.
- The two plan gates that touch this surface.

What it does NOT cover:

- The Theme Editor / Custom CSS/JS layers — see [[theme-customization-layers]].
- Per-module setting tables — see the individual `design-modules-*` feature pages.
- The Page Builder UI itself (drag-drop interactions, row layouts) — see [[marketing-landing-pages]].
- Blog articles (a separate content type with their own surfaces) — see [[marketing-blog-articles]].

## Contrasts

- **Module vs. Block — placement**: a module's placement is decided by the **theme** (slot in the layout). A block's placement is decided by the **merchant** (drag-drop onto a row inside a Dynamic page).
- **Module vs. Block — scope**: a module renders **globally** on every storefront page with its slot. A block renders **only** on the one Dynamic page it was dragged onto.
- **Module vs. Block — storage**: module settings live in a global store keyed by `(theme, instance_name)`. Block content lives inside the Page's content JSON, keyed by page ID + position. See [[widget-vs-pb-module-mechanics]] + [[widget-vs-pb-block-mechanics]].
- **Module vs. Block — theme switch**: modules hide; blocks survive. See [[widget-vs-pb-theme-switch-behavior]].
- **System module vs. configurable module**: `navigationMain` / `navigationFooter` / `logo` / `userControls` have NO settings form — content comes from [[design-navigation]] / [[settings-general]] / auth state. Configurable modules have a settings form driven by one of the 25 templates.
- **Module tabs vs. Page Builder palette**: the Modules screen organises into 7 tabs (Products / User / Blogs / Contacts / Others / Layout / Custom). The Page Builder palette is a flat list filtered to what the theme allows for that page type.
- **Page Builder vs. other page types**: Page Builder is a special **Dynamic** page type on [[marketing-landing-pages]] — alongside Static (regular), FAQ, External. Only Dynamic pages use block composition.
- **Has version history?**: blocks YES (up to 500 snapshots per page); modules NO.

## Where it applies

### Module surfaces

- [[design-modules]] — master Modules catalogue (7 tabs + 25 templates).
- [[design-modules-navigation]] / [[design-modules-content]] / [[design-modules-products]] / [[design-modules-engagement]] / [[design-modules-blog]] / [[design-modules-utility]] — per-group catalogues.
- [[design-themes]] — the active theme decides which module instances exist.

### Page Builder surfaces

- [[marketing-landing-pages]] — Static Pages screen; the **Dynamic** page type opens the Page Builder.
- Route — `/admin/marketing/pages/builder/<page_id?>`.

### Plan-feature gates (see [[widget-vs-pb-system-pages-and-restrictions]])

- `storefront_builder` — gates Dynamic page creation (Page Builder usage).
- `video_slider_widget` — gates the Video Slider module at edit-time.

## Related

- [[design]] — parent pillar (Modules + Themes both children).
- [[design-modules]] — Modules catalogue.
- [[design-themes]] — theme decides what module instances + page-builder blocks exist.
- [[design-navigation]] — feeds `navigationMain` / `navigationFooter` system modules.
- [[settings-general]] — feeds the `logo` system module.
- [[marketing-landing-pages]] — Static Pages screen; Dynamic page type opens Page Builder.
- [[theme-customization-layers]] — 3-layer customisation hierarchy.
- [[plan-gates]] — `storefront_builder` + `video_slider_widget`.
- [[plan-features]] — plan-feature paywall.

## Open Questions

None at the hub level — all previously-flagged items resolved or distributed to sub-pages.
