---
type: feature
nav_path: "Design → Modules → Navigation"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Navigation modules", "Header modules", "Footer modules", "Menu module", "Main navigation module", "Footer navigation module", "Search module", "Logo module", "User controls module", "Back to top button", "Promo bar module", "Navigation links module", "Модули - Навигация"]
tags: [design, modules, navigation, header, footer]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# Storefront Modules — Navigation

## Purpose

The **Navigation** module group covers everything the customer uses to MOVE AROUND the storefront — the main menu, the footer link tree, the search bar, the store logo, the customer account icons, the secondary link blocks, the promo bar, and the back-to-top button. These modules live in the theme's header, top-bar and footer slots; together they form the storefront's chrome.

Most navigation modules are **system modules** — they render automatically as part of the active theme's header / footer and pull their content from dedicated admin screens (Logo upload in [[settings-general]], [[design-navigation]] menu trees, customer-access mode in [[settings-cart]]). A few — `navigationLinks`, `search`, `htmlLine` (Promo bar), `social`, `buttonToTop` — DO have editable forms on the Modules screen.

This page is the navigation pivot. Drill into the per-module aspect rather than reading every module here.

## Sub-pages (in this cluster)

- [[design-module-navigation-main]] — `navigationMain` / `navigation.main`: renders the main header menu tree; content edited in [[design-navigation]].
- [[design-module-navigation-footer]] — `navigationFooter` / `navigation.footer`: renders the footer menu tree; content edited in [[design-navigation]].
- [[design-module-navigation-links]] — `navigationLinks` / `footerLinks1-3` / `navigationLinksPage`: flat link lists for top-bar shortcuts and extra footer columns; editable on the Modules screen.
- [[design-module-search]] — `search` / `extra.search`: storefront search bar + autocomplete toggles; deep settings live in the search-engine app.
- [[design-module-logo]] — `logo` / `extra.logo`: store-logo render; image uploaded in [[settings-general]] (no Modules-screen card).
- [[design-module-user-controls]] — `userControls` / `user.controls`: login / my-account / logout icons; auth-state-driven, no merchant settings.
- [[design-module-social]] — `social` / `extra.social`: social-network icons row (Facebook, X, Instagram, Pinterest, YouTube, LinkedIn, TikTok).
- [[design-module-promobar]] — `htmlLine` / `extra.htmlLine`: top promo bar with scheduled From / To window and optional CTA button.
- [[design-module-button-to-top]] — `buttonToTop`: floating back-to-top button; single enable toggle (internal `extra.text` instance with title/text hidden).

## Where to find it

Sidebar → **Design** → **Modules** — these modules appear under the **Others** tab (`extra` category) and on per-instance basis depending on the theme. Some have no editor card on this screen at all (they're rendered by the theme but configured elsewhere).

| Module instance | Edit surface |
|-----------------|--------------|
| `navigationMain` / `navigationFooter` | NOT on Modules screen — managed in [[design-navigation]] |
| `navigationLinks` / `footerLinks1-3` / `navigationLinksPage` | Modules screen → **Others** tab |
| `userControls` | NOT on Modules screen — content is auth-state-driven |
| `search` | Modules screen → **Others** tab (limited toggles) |
| `logo` | NOT on Modules screen — uploaded in [[settings-general]] |
| `buttonToTop` | Modules screen → **Others** tab |
| `htmlLine` (Promo bar) | Modules screen → **Others** tab |
| `social` | Modules screen → **Others** tab |

## What the merchant can do here

The Modules screen is the entry point. From the cards visible there the merchant can:

- Open an editable navigation module side panel and adjust settings — see the per-module aspect for field tables.
- Save / Reset / Cancel — standard actions across every editable module (see *Common behaviour* below).
- Enable / disable the master toggle on each editable module.

For system modules there is nothing to edit on the Modules screen — see [[design-navigation]], [[settings-general]], or [[settings-cart]] for the right admin surface.

The merchant CANNOT:

- Add a brand-new module instance — the catalogue is fixed by the active theme.
- Edit the main / footer menu TREES from this screen — those are in [[design-navigation]].
- Upload / change the logo from this screen — that's in [[settings-general]].

## Settings & fields

This hub does not document fields directly — every field table lives in the per-module aspect. Pick the right aspect from the *Sub-pages* list above.

## Business rules

### Navigation modules vs the menu trees

`navigationMain` and `navigationFooter` consume content from the menu trees in [[design-navigation]] (the `main` and `footer` trees respectively). The trees are richer (4-level nesting, 12 link types, drag-and-drop) and edited on a dedicated screen. The module cards on the Modules screen do NOT exist for these instances.

`navigationLinks` and siblings (`footerLinks1-3`, `navigationLinksPage`) are FLAT lists (no nesting) and ARE edited on the Modules screen — see [[design-module-navigation-links]].

### System modules without merchant forms

`userControls`, `logo`, `navigationMain`, and `navigationFooter` do not have edit cards on the Modules screen. They're rendered automatically by the theme; content comes from elsewhere (auth state, [[settings-general]], [[design-navigation]]).

### Header / Footer LAYOUT drives module rendering

The visual layout of the main menu (mega-menu vs sidemenu vs dropdown) is picked in **Header settings** (`headerConfiguration`) on the Modules screen, NOT in the navigation module itself. The footer column layout is picked in **Foot settings** (`footerConfiguration`).

### Plan-gating

None of the navigation modules are plan-gated. All are available on every plan.

## Common behaviour across all editable modules in this category

### Save / Reset / Cancel

Every editable module panel has three buttons at the top:

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists the form input; regenerates the storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Wipes the merchant's saved settings — module reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

### Per-instance settings are independent

Each module instance's settings are saved under its own instance name (e.g., `navigationLinks`, `footerLinks2`, `buttonToTop`). Identical module TYPES under different INSTANCE names have completely independent settings. Save / Reset takes effect on the storefront on the very next request.

Navigation menu CONTENT (the links in the main and footer trees) is NOT saved by these module cards — it lives in a separate menu store managed under [[design-navigation]]. The navigation modules just render whichever menu is bound to `main` / `footer`.

### Hidden / non-editable instances

Some instances the active theme renders are deliberately non-editable: they have no edit card on the Modules screen and their edit URL returns 404. An instance the active theme does not provide is simply not shown.

## Related

- [[design-modules]] — parent module catalogue (overview + tab structure).
- [[design]] — pillar hub for Design.
- [[design-themes]] — theme picker; theme controls header / footer layout and which navigation instances appear.
- [[design-navigation]] — configures the `main` and `footer` menu trees (the source of content for `navigationMain` / `navigationFooter`).
- [[design-modules-content]] — sibling module category (Content: carousel, banners, text, video, separator, title).
- [[design-modules-products]] — sibling module category (Product modules).
- [[design-modules-engagement]] — sibling module category (Mailchimp, contact, Google Map).
- [[design-modules-blog]] — sibling module category (Blog modules).
- [[design-modules-utility]] — sibling module category (Utility / layout modules).
- [[settings-general]] — store logo upload, site name, deep search settings.
- [[settings-cart]] — customer account permissions, guest checkout.

## Open questions

- 📡 **Per-language navigation content.** With `multylang` installed, navigation module content (link captions, promo text, search placeholder) supports per-language entries. GraphQL-resolvable: query whether the `multylang` app is installed.
- 📡 **Search-engine routing.** Depends on whether Algolia / Advanced Search apps are installed. GraphQL-resolvable: query the merchant's installed apps. Documented per-module in [[design-module-search]].
