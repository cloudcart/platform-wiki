---
type: concept
nav_path: "Concept → Module vs Page Builder block → Module mechanics"
aliases: ["Module mechanics", "Storefront module mechanics", "Theme module slots", "Module instance storage", "Editable flag", "System modules", "navigationMain", "logo module", "userControls", "Модули — механика"]
tags: [design, modules, page-builder, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[widget-vs-page-builder-block]]. See the hub for the other aspects (block mechanics, shared template library, theme-switch behaviour, system pages + restrictions).

# Module mechanics

## Definition

A **Module** is a **pre-defined slot in the active theme's storefront layout**. The theme decides which module instances exist, WHERE each one renders (homepage row, header, footer, sidebar, cart, checkout), and which 25-template form drives the edit panel. The merchant configures each instance ONCE and the storefront renders it on every page that includes its slot.

The Modules screen lives at `/admin/storefront/widgets` ([[design-modules]]). The screen organises modules into 7 tabs (Products / User / Blogs / Contacts / Others / Layout / Custom) plus sidebar groups.

## Scope

Covered:

- Module instance identity — instance name + module type + slot location + settings form.
- Storage shape — settings JSON keyed by `(theme, instance_name)`; the `front_widget` table has no theme-slug column. (verify)
- Why the same module TYPE can be instanced many times (e.g., `homeText1`/`homeText2`/`headerText`/`footerText` all of type `extra.text`).
- **System modules** — instances without merchant forms (`navigationMain`, `navigationFooter`, `logo`, `userControls`).
- The `editable: 'no'` flag in `theme.json` that hides a module from the Modules screen entirely.
- The 25 registered module classes and which are app-conditional.

Not covered:

- Page Builder blocks — see [[widget-vs-pb-block-mechanics]].
- What happens on theme switch — see [[widget-vs-pb-theme-switch-behavior]].
- The shared 25-template form library — see [[widget-vs-pb-shared-template-library]].
- Per-module configuration screens — see the `design-modules-*` cluster.

## Contrasts

- **Module instance vs. module type**: one TYPE (e.g., `extra.text`) can back many INSTANCES (`homeText1`, `footerText`, `cartText`). Each instance is independent — its own JSON blob, its own slot. The merchant edits instances; the theme registers types.
- **Configurable module vs. system module**: configurable modules (`bannersHomePage`, `homeText1`) expose a settings form from the 25-template library. System modules (`navigationMain`, `navigationFooter`, `logo`, `userControls`) have NO edit card; their content comes from [[design-navigation]] / [[settings-general]] / auth state.
- **Module storage vs. block storage**: module settings live in `front_widget`, keyed by `(theme, instance_name)`. Block content lives in the Page's content JSON. See [[widget-vs-pb-block-mechanics]] for the block side.
- **Theme-declared vs. globally-registered**: 25 module classes are registered globally (some app-conditional). The active theme's `theme.json` filters which instances of which classes the merchant actually sees on the Modules screen.
- **Visible vs. `editable: 'no'`**: a theme can declare a module instance that renders in the storefront but is hidden from the Modules screen entirely.

## Where it applies

- [[design-modules]] — Modules screen `/admin/storefront/widgets`.
- [[design-modules-navigation]] / [[design-modules-content]] / [[design-modules-products]] / [[design-modules-engagement]] / [[design-modules-blog]] / [[design-modules-utility]] — per-group module catalogues.
- [[design-themes]] — `theme.json` declares the module instance catalogue.
- [[design-navigation]] — feeds `navigationMain` / `navigationFooter` system modules.
- [[settings-general]] — feeds the `logo` system module.

## How an instance is identified

Each module instance in a theme's `theme.json` declares:

- A unique **instance name** — `homeText1`, `bannersHomePage`, `productsRelated`, `headerConfiguration`, `navigationMain`, `footerLinks1`, `htmlLine` (promo bar), `search`, etc.
- A module **type** — e.g., `extra.text`, `extra.banner`, `extra.videoSlider`, `product.related`, `layout.header`.
- A **slot location** — where the theme renders this instance (homepage row, footer column, header bar, cart sidebar, etc.). The theme controls placement; the merchant cannot move a module to a different slot.
- A **settings form** — generated from one of the 25 shared template files based on the module type.

Editing flow: merchant clicks an instance card → opens settings panel → edits form fields → clicks **Save module**. Settings persist as JSON keyed by `(theme, instance_name)`. Storefront cache regenerates; next page render picks up the new settings.

## Storage shape

Module settings are stored in a global module-settings store (`front_widget` table). Rows are keyed by `(mapping, settings JSON, global flag)` with **no theme-slug column on the row itself**. (verify) The "theme controls visibility" effect comes from the storefront refusing to render a module whose instance name isn't declared in the active theme's `theme.json` — data persists across theme switches, what changes is whether the storefront reads it.

## The 25 registered module classes

The Module Service registers exactly 25 module classes — `banner`, `text`, `carousel`, `text-carousel`, `product-showcase`, `showcase`, `code`, `separator`, `video`, `video-slider`, `title`, `order-details`, `bundle-products`, `yotpo-reviews`, `product`, `add-to-cart`, `button`, `brand-model`, `recent-articles`, `product_review`, `request_review`, `store_locations`, `cc_form`, etc. (verify)

Several are **conditionally loaded** based on installed apps:

| Module class | Requires app |
|--------------|--------------|
| `yotpo-reviews` | Yotpo app |
| `brand-model` | Brand Model app |
| `product_review` / `request_review` | Product Review app |
| `store_locations` | Store Locations app |

So the effective per-store module catalogue depends on which apps are installed AND what the active theme declares. A module class registered globally still won't appear if the active theme doesn't declare an instance of it.

## System modules — no merchant form

Three classes of instance render in the storefront but have NO card on the Modules screen:

| Instance | Content source | Why no form |
|----------|----------------|-------------|
| `navigationMain` / `navigationFooter` | The `main` / `footer` menu trees in [[design-navigation]] | The trees have a richer editor (4-level nesting, 12 link types, drag-and-drop). |
| `logo` | The logo uploaded in [[settings-general]] | Global brand setting. |
| `userControls` | The customer's auth state (Login / Profile / Logout icons) | Icons toggle automatically; no merchant settings. |

A theme that ships `navigationMain` in its header renders it pulling content from the merchant's main menu tree. A merchant looking for a "Main navigation" module card on `/admin/storefront/widgets` won't find one — they have to edit the source surface instead. See [[widget-vs-pb-shared-template-library]] for which form templates apply to non-system modules.

## `editable: 'no'` — locking down a module

Each module instance in `theme.json` carries an optional `editable` flag. When a theme author sets `editable: 'no'`:

- The module controller returns HTTP 404 if the merchant tries to open the edit panel directly. (verify)
- The card is hidden from the Modules screen entirely.

Themes use this to lock down "branding-critical" module slots — typically logo / footer / system modules the theme author doesn't want the merchant to misconfigure.

## Example: one type, many instances

The `extra.text` type alone backs ~30+ instances in a typical theme:

- `homeText1`, `homeText2`, `homeText3` (homepage text blocks)
- `welcomeText` (welcome row)
- `headerText` / `headerLeft` / `headerRight`
- `footerText` / `footerContent` / `footerContacts`
- `cartText` / `checkoutText` / `checkoutSideText`
- `productText`
- etc.

Each instance has its own JSON blob — they're independent. The theme decides WHERE each instance renders; the merchant configures WHAT it contains. Two banners that should appear on different pages need two different instances (or one instance plus a [[widget-vs-pb-block-mechanics|Page Builder block]] on the second page).

## Related

- [[widget-vs-page-builder-block]] — hub.
- [[design-modules]] — Modules screen with the 7-tab catalogue.
- [[design-themes]] — the active theme is the source of `theme.json` declarations.
- [[design-navigation]] — feeds `navigationMain` / `navigationFooter`.
- [[settings-general]] — feeds `logo`.
- [[theme-customization-layers]] — broader 3-layer customisation hierarchy.

## Open Questions

- Exact column shape of the `front_widget` table — verified at the `(mapping, settings JSON, global flag)` level but the precise schema is unconfirmed. (verify)
- Whether `editable: 'no'` returns HTTP 404 in the current Vue admin or only on the legacy controller. (verify)
