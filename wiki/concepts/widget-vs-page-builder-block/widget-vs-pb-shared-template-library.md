---
type: concept
nav_path: "Concept → Module vs Page Builder block → Shared 25-template library"
aliases: ["25-template library", "Shared form templates", "Module form templates", "Page Builder block templates", "banner template", "carousel template", "Page-Builder-only blocks", "code block", "Шаблони на блокове"]
tags: [design, modules, page-builder, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[widget-vs-page-builder-block]]. See the hub for the other aspects (module mechanics, block mechanics, theme-switch behaviour, system pages + restrictions).

# Shared 25-template library

## Definition

Both surfaces — the Modules screen ([[widget-vs-pb-module-mechanics]]) and the Page Builder palette ([[widget-vs-pb-block-mechanics]]) — use the **same library of 25 form templates** to render edit panels. When the merchant opens an edit panel for a module instance or a Page Builder block, the platform resolves the right template based on the module type / block type and renders the same form shape.

About **13 of the 25 templates serve BOTH surfaces** (a `banner` form configures either a module instance OR a block). The other **~12 templates are Page-Builder–only** — they exist in the Page Builder palette but no current theme declares any of them as a module instance. (verify)

## Scope

Covered:

- The complete list of 25 form templates.
- Which ~13 templates serve both Modules + Page Builder.
- Which ~12 templates are Page-Builder–only and why.
- The resolution rule that picks the template per module type / block type.
- The shared Smarty rendering stack (the storefront-side template that turns saved settings into HTML).

Not covered:

- Where each block actually renders on the storefront — theme-specific Smarty templates outside the wiki's scope.
- Per-template field lists (what fields the `banner` template exposes, etc.) — see the individual `design-modules-*` feature pages.
- How `theme.json` declares which blocks live in the page-builder palette — see [[design-themes]].

## Contrasts

- **Dual-surface template vs. Page-Builder–only template**: ~13 templates (`banner`, `text`, `carousel`, `showcase`, `product-showcase`, etc.) work for both module instances AND Page Builder blocks. ~12 templates (`code`, `cc_form`, `order-details`, `add-to-cart`, `bundle-products`, `blog-list`, `button`, etc.) are Page-Builder–only — no current theme declares them as module instances.
- **Module form vs. block form (same template)**: the form fields are identical — what changes is the storage layer and lifecycle around it. See [[widget-vs-pb-module-mechanics]] vs [[widget-vs-pb-block-mechanics]].
- **App-conditional vs. always-available**: a few templates (`yotpo-reviews`, `brand-model`, `product_review`, `request_review`, `store_locations`) only register when the corresponding app is installed.
- **Form template vs. storefront render template**: the 25 files are admin-side form templates. The storefront render of each module / block is a separate Smarty template that the theme ships.

## Where it applies

- [[widget-vs-pb-module-mechanics]] — module edit panels resolve templates from this library.
- [[widget-vs-pb-block-mechanics]] — Page Builder edit panels resolve templates from this same library.
- [[design-modules]] — per-tab catalogue showing which templates back which module instances.
- [[design-themes]] — `theme.json` binds templates to slots (modules) and palette blocks (Page Builder).

## The full template catalogue

The 25 template files are: `add-to-cart`, `banner`, `blog-list`, `brand-model`, `bundle-products`, `button`, `carousel`, `cc_form`, `code`, `google-map`, `order-details`, `product-showcase`, `product`, `product_review`, `recent-articles`, `request_review`, `separator`, `showcase`, `store_locations`, `text-carousel`, `text`, `title`, `video-slider`, `video`, `yotpo-reviews`. (verify)

## Templates that serve BOTH surfaces

About 13 templates back module instances AND Page Builder blocks. The canonical dual-surface set includes:

- `banner`
- `carousel`
- `text`
- `text-carousel`
- `showcase`
- `product-showcase`
- `recent-articles`
- `google-map`
- `yotpo-reviews`
- `video-slider`

When the merchant configures a `banner` module instance OR drags a `banner` block onto a Dynamic page, both edit panels render the same form. Storage layer + lifecycle differ (see [[widget-vs-pb-module-mechanics]] vs [[widget-vs-pb-block-mechanics]]); the form itself is identical.

## Templates that are Page-Builder–only

About 12 templates appear ONLY in the Page Builder palette — no current theme registers them as module instances. The merchant won't find a card for these on `/admin/storefront/widgets`:

| Template | Block purpose |
|----------|---------------|
| `code` | Raw HTML / JS block. |
| `store_locations` | Embedded store-locator block (requires Store Locations app). |
| `brand-model` | Brand + model picker block (car-parts stores; requires Brand Model app). |
| `order-details` | Order-details block (for thank-you pages). |
| `title` | Section title block. |
| `separator` | Horizontal separator block. |
| `video` | Video block. |
| `cc_form` | CloudCart form block (registration / contact). |
| `product` | Product-detail block. |
| `product_review` | Product-review form block (requires Product Review app). |
| `request_review` | Request-review form block (requires Product Review app). |
| `add-to-cart` | Add-to-cart button block. |
| `bundle-products` | Product-bundle block. |
| `blog-list` | Blog-list block (required on `blog.list` system pages — see [[widget-vs-pb-system-pages-and-restrictions]]). |
| `button` | Button block. |

These are conceptually "page-level building primitives" — components that only make sense in a per-page composition (you don't put `order-details` in a header slot; you put it on a thank-you Dynamic page).

## Template resolution

When the merchant opens an edit panel:

1. The Module Service / Page Builder identifies the module type or block type.
2. The platform resolves the matching template file from the 25-template library.
3. The template renders the form with the saved settings JSON populated.
4. On Save, the form serialises back to JSON and persists (module-settings store for modules, page content JSON for blocks).

## Shared rendering stack — legacy Smarty storefront

Both module instances and Page Builder blocks render server-side via the **legacy Smarty template stack** on the storefront. The active theme is responsible for:

- The `theme.json` declaration of available module instances + their slot locations.
- The `theme.json` declaration of available page-builder block types + per-page-type restrictions.
- The Smarty templates that turn saved module / block JSON into rendered HTML.

A theme that doesn't declare a particular block type in its page-builder block library cannot render Dynamic pages that use that block — the block falls back to a placeholder (see [[widget-vs-pb-theme-switch-behavior]]).

## Related

- [[widget-vs-page-builder-block]] — hub.
- [[design-modules]] — Modules screen with per-tab catalogue.
- [[design-themes]] — `theme.json` declares which templates are bound to which slots / blocks.
- [[theme-customization-layers]] — broader customisation hierarchy.

## Open Questions

- Exact dual-surface count — documented at "about 13 of 25" but a verified per-template breakdown is unconfirmed. (verify)
- Whether the 25 template files are a fixed compile-time list or extendable via apps. (verify)
