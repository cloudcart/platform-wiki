---
type: feature
nav_path: "Design → Theme Editor"
route_name: admin.css.builder
route_path: /admin/builder
aliases: ["Theme editor", "Design edit", "CSS Builder", "Customize theme", "Change colors", "Change fonts", "Storefront design", "Colors and typography", "Редакция на дизайн", "Дизайн редактор", "Промяна на цветове", "Промяна на шрифтове", "Цветове и шрифтове"]
tags: [design, theme, customization, colors, fonts, scss]
plan_gates: ["change_theme"]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Theme Editor

## Purpose

The **Theme Editor** is the merchant-facing visual customiser for the **currently active theme**. From here the merchant changes the storefront's **colours**, **typography** (font family, size, weight, style), and a small set of **image / layout variables** (e.g., product-image orientation) — all exposed by the active theme as a fixed list of named variables. The screen is a standalone full-screen builder shell with a **live preview iframe of the storefront** on the right and a **settings sidebar** on the left, plus deep-links into the **Header**, **Foot**, **Grid**, and **Buttons** layout modules.

This is the merchant's everyday "tweak the brand" surface — without touching theme code. Deeper structural changes (homepage module layout, menu items, active theme) live in [[design-modules]], [[design-navigation]], and [[design-themes]]. The catalogue of variables is **theme-specific** — a theme that ships only a colour palette shows no typography section; a theme that ships an image-orientation variable shows that section; etc.

## Where to find it

Sidebar → **Design** → **Colors and typography** (the sidebar link's visible label combines the colour and typography sub-tabs into one entry; the URL is `/admin/builder`).

The screen is also reachable from:

- The **Themes** screen ([[design-themes]]) — top-right **Theme Editor** button.
- Any per-section deep-link via a query parameter (`/admin/builder?colors`, `/admin/builder?typography`, `/admin/builder?images`) — these auto-open the matching sub-tab. See [[design-theme-editor-preview-deeplinks]].

The Theme Editor opens as a **standalone full-screen builder** (not the normal admin layout). It has its own top bar with a **Back to CloudCart** link that returns the merchant to the Themes screen.

Sub-routes:

| Action | Route name | Path | Method |
|--------|------------|------|--------|
| Open the editor | `admin.css.builder` | `/admin/builder` | GET |
| Save edited variables | — (same path) | `/admin/builder` | POST |
| Reset all customisations | `admin.css.reset` | `/admin/builder/reset` | GET |

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. Drill into the aspect that matches the question, not every page.

- [[design-theme-editor-variables]] — the variable type system (`color` / `font-family` / `font-style` / `font-weight` / `font-size` / `image` / `custom`); group accordions; `theme.json` `settings.variables`; `{parameter, value, type, template}` storage row.
- [[design-theme-editor-colors]] — Colours sub-tab; Bootstrap colour picker; 80-130 colour variables per theme; group accordions (Main / Promo Bar / Header / Footer / …).
- [[design-theme-editor-typography]] — Typography sub-tab; ~88 Google Fonts catalogue; family / style / weight / size pickers; `google_fonts_url` setting; custom-font escape via [[design-custom-assets]].
- [[design-theme-editor-images]] — Images sub-tab; product-image aspect-ratio (PORTRAIT `133.33%` / LANDSCAPE `75%` / SQUARE `100%` / CUSTOM); only renders if the theme declares an `image`-type variable.
- [[design-theme-editor-save-reset]] — full-form Save; delete-then-insert; atomic Reset with rollback; defaults-merge on editor load; validation gap.
- [[design-theme-editor-css-compile]] — server-side recompile; `theme.css` `_<variable>_` token replacement; S3 upload to `<site_id>/css/theme.css`; `stylesheet_version` cache-buster; `stylesheet_storage_backend` URL format.
- [[design-theme-editor-preview-deeplinks]] — live-preview iframe; Mobile / Tablet / Desktop viewports; iframe auto-reload after Save; sub-tab deep-links (`?colors` / `?typography` / `?images`); layout-module sidebar links (Header / Foot / Grid / Buttons / Homepage).

## What the merchant can do here

This hub lists the high-level capabilities; each aspect documents the field-level mechanics.

- **Change colours** across 80-130 named variables organised by accordion group → [[design-theme-editor-colors]].
- **Change typography** by picking from ~88 Google Fonts + filtered weight / style / size dropdowns → [[design-theme-editor-typography]].
- **Change product-image aspect-ratio** (PORTRAIT / LANDSCAPE / SQUARE / CUSTOM) when the theme exposes the variable → [[design-theme-editor-images]].
- **Save the full customisation set** in one POST (no per-sub-tab save) → [[design-theme-editor-save-reset]].
- **Reset all customisations atomically** to the theme's shipped defaults → [[design-theme-editor-save-reset]].
- **See changes on the live storefront** after Save (the iframe auto-reloads) → [[design-theme-editor-preview-deeplinks]].
- **Deep-link into layout modules** (Header / Foot / Grid / Buttons / Homepage) from the sidebar → [[design-modules]] and [[marketing-landing-pages]] for Homepage.

## What the merchant cannot do here

- Cannot **add new variables** — only what the active theme declares in `theme.json` is editable; the merchant extends via [[design-themes]] or [[design-custom-assets]]. See [[design-theme-editor-variables]].
- Cannot **edit the theme's underlying CSS / SCSS** — the editor replaces `_<variable>_` placeholder tokens in the pre-built CSS, not the rules. See [[design-theme-editor-css-compile]] and [[design-custom-assets]].
- Cannot **upload a custom font** — only the curated Google Fonts catalogue is selectable; self-hosted webfonts require [[design-custom-assets]]. See [[design-theme-editor-typography]].
- Cannot **save partial changes** or **preview before saving** — every save submits the entire form and the iframe shows the LIVE storefront, not a draft. See [[design-theme-editor-save-reset]] and [[design-theme-editor-preview-deeplinks]].
- Cannot **revert just one variable** — Reset wipes every customisation in one shot. See [[design-theme-editor-save-reset]].
- Cannot **carry customisations to a different theme** — variables are stored per active theme (the `template` slug partitions storage). Switching themes hides; switching back reveals. See [[design-theme-editor-variables]].

## Settings & fields

The variable schema is owned by the active theme's `theme.json` under `settings.variables`. The full type and group catalogue is in [[design-theme-editor-variables]]. The per-sub-tab field detail lives in [[design-theme-editor-colors]], [[design-theme-editor-typography]], and [[design-theme-editor-images]]. Save and Reset writes are documented in [[design-theme-editor-save-reset]]; the storage row shape is `{parameter, value, type, template}`.

## Business rules

The cross-cutting rules — all elaborated in the aspect pages:

- **Variables are per-theme.** Switching themes hides but preserves; switching back reveals. See [[design-theme-editor-variables]].
- **Save replaces the full set** (delete-then-insert per active theme). See [[design-theme-editor-save-reset]].
- **Save recompiles the stylesheet to S3** at `<site_id>/css/theme.css`; `stylesheet_version` busts caches. See [[design-theme-editor-css-compile]].
- **Reset is atomic** — DB transaction with rollback on error. See [[design-theme-editor-save-reset]].
- **Defaults merged on load** AND written back to storage (drift correction across theme updates). See [[design-theme-editor-save-reset]].
- **Fonts bundled into `google_fonts_url`** on save and injected into every storefront page's `<head>`. See [[design-theme-editor-typography]].
- **Live preview is the LIVE storefront** — new styles appear only after Save. See [[design-theme-editor-preview-deeplinks]].
- **Theme-shipped `theme.css` is the template** — merchant only fills `_<variable>_` placeholders. See [[design-theme-editor-css-compile]].
- **Permission**: gated by `store.builder` (also satisfied by broader `store`).

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `change_theme` | Access gate (theme-switch path) | Gates the **Install action** at `storefront/templates/action/change/%` (Reset → reinstall flow + [[design-themes]] theme-switch). Lower plans cannot switch themes but CAN still edit the active theme's variables. No `change_theme` check is enforced at the Theme Editor controller itself. |

The related `storefront_builder` plan-feature gates the **Page Builder** ([[design-modules-content]] / [[marketing-landing-pages]]) — the editor's sidebar Homepage link is independently restricted. Variable customisation (colours, fonts, images) is open to every staff member with `store.builder` permission regardless of plan.

## Related

- [[design]] — parent Design pillar.
- [[design-themes]] — theme picker; the active theme decides which variables the Theme Editor exposes.
- [[design-modules]] — sibling; configures module instances (header, footer, grid, buttons modules are deep-linked from the Theme Editor sidebar).
- [[design-navigation]] — sibling; configures `main` and `footer` menu trees.
- [[design-custom-assets]] — sibling; raw CSS / JS for advanced merchants beyond what the variable editor allows; also the home of the `custom-css-js` variable.
- [[marketing-landing-pages]] — homepage page-builder, reachable from the Theme Editor's *Homepage* sidebar link.
- [[settings-brand]] — logo / favicon / social-share image (separate from colours and fonts).
- [[plan-gates]] — plan-tier caps that may affect builder features.

## Open questions

None at the hub level. Per-aspect open questions are listed in each sub-page.
