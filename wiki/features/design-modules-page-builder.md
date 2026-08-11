---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Page builder modules", "Page builder blocks", "Dynamic page modules", "Builder blocks", "Модули за builder", "Блокове в builder"]
tags: [design, modules, page-builder, marketing, landing-pages]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Page Builder modules

## Purpose

The **Page Builder modules** are the catalogue of blocks the merchant drops into a Dynamic page via the visual page builder. Unlike the theme-wide modules on the Modules screen, page-builder modules are configured **per-page** — every Dynamic page in [[marketing-landing-pages]] has its own arrangement of these blocks and its own per-block settings. Adding a Button block to the homepage does not put a Button block anywhere else; copying a Button on the same page makes two independent buttons.

This catalogue covers the blocks unique to the page builder — primarily content / interactive blocks that don't make sense as global theme modules (e.g., a Button with a custom link, a CloudCart form embed, a video, an order-details receipt block). The page builder ALSO surfaces several blocks that share the same module type as the Modules screen (e.g., `banner`, `carousel`, `text`, `product-showcase`); those are documented under the general module catalogue in [[design-modules]] and not duplicated here.

The page builder is gated by the `storefront_builder` plan feature (see [[plan-gates]]). Some blocks require additional apps installed (e.g., `cc_form` needs the Subscribers app; `store_locations` needs the Store Locations app; `product_review` and `request_review` need the Product Review app; `brand-model` needs the Brand Model app).

## Sub-pages (in this cluster)

- [[design-module-pb-add-to-cart]] — Add-to-cart button block bound to a specific product.
- [[design-module-pb-blog-list]] — Blog list block (per-page articles listing). (code-wired but currently disabled in the registry; verify availability)
- [[design-module-pb-brand-model]] — Brand+model picker for car-parts stores (Brand Model app).
- [[design-module-pb-bundle-products]] — Bundle products block bound to a specific bundle.
- [[design-module-pb-button]] — Button block (1-3 buttons; link, target, label, position, colour, width, attributes).
- [[design-module-pb-cc-form]] — Embedded CloudCart form (subscriber form, contact form, etc.).
- [[design-module-pb-code]] — Raw HTML / JS code block (third-party embed).
- [[design-module-pb-order-details]] — Order details block for the Thank-you / receipt page.
- [[design-module-pb-product]] — Product detail block bound to a specific product.
- [[design-module-pb-product-review]] — Product review listing block (Product Review app).
- [[design-module-pb-request-review]] — Request-review form (Product Review app).
- [[design-module-pb-separator]] — Horizontal separator line (style, colour, height, margins).
- [[design-module-pb-store-locations]] — Store-locations / shops list (Store Locations app).
- [[design-module-pb-title]] — Section title (h1-h6 tag picker).
- [[design-module-pb-video]] — Video block (YouTube / Vimeo / VBOX7 / embed / HTML5).

## Where to find it

Sidebar → **Marketing** → **Pages** → click **+ Add new page** → pick **Dynamic page** → opens the page builder at `/admin/marketing/pages/builder/{page_id?}`.

Inside the builder:

1. Click **+ Add block** on any row to open the block picker.
2. Pick a module from the picker — only apps-installed modules appear.
3. Configure the block in the side panel.
4. Click **Save** — the change is persisted to the page's content JSON and a new `PageHistory` row is created.

The same module registry is used to render the storefront — every block stored in the page's content JSON resolves to a module class via the platform code.

## What the merchant can do here

- Drop any registered module into a Dynamic page.
- Configure the block's fields per-instance — multiple instances of the same module on the same page are independent.
- Reorder and remove blocks freely.
- Roll back to a previous version via the page-builder's history dropdown (up to 500 most recent versions per page — see [[marketing-landing-pages]]).
- Combine multiple blocks in a row (the page builder is row + column based, not a free-form canvas).
- Picker shows ONLY the modules whose app dependencies are satisfied — e.g., `store_locations` is hidden if the Store Locations app is not installed.

## What the merchant cannot do here

- The merchant cannot add new module TYPES from the page builder — the registry is fixed by the platform (see `App\Services\Module::$widgets_map`).
- The merchant cannot configure the theme-wide modules (header / footer / global filters) from the page builder — those live on [[design-modules]].
- The merchant cannot save a Dynamic page as inactive — the page-builder controller forces `active = true` on save (see [[marketing-landing-pages]]).
- The merchant cannot use page-builder modules outside a Dynamic page — they only render inside the builder's rendering pipeline.

## Settings & fields

This hub does not document fields directly — every block's settings live in the sub-page. The shared `enabled` toggle (master on/off) appears on every block — the toggle is hidden when the module class returns `canDisable == false`.

## Business rules

### Per-page, per-instance configuration

Every block instance on a Dynamic page has its own JSON blob stored inside the page's content JSON. Two `button` blocks on the same page are entirely independent — different text, link, colour, position.

### App-gated blocks

The block picker only surfaces modules whose app dependency is satisfied. The dependency map is hard-coded in the platform code:

| Module | Required app |
|--------|--------------|
| `yotpo-reviews` | Yotpo |
| `brand-model` | Brand Model |
| `product_review` | Product Review (installed AND enabled) |
| `request_review` | Product Review (installed AND enabled) |
| `store_locations` | Store Locations |
| `cc_form` | Subscribers (provides the form catalogue) |

If the app is uninstalled after the merchant added the block, the storefront rendering falls back to a "not installed" message (verify behaviour per module).

### Plan gate

The page builder URL `/admin/marketing/pages/builder/...` is gated by the `storefront_builder` plan feature. Lower-tier merchants are redirected to the plan upsell. Some modules are additionally restricted per-plan via the platform code callback — see [[plan-gates]] and [[marketing-landing-pages]].

### `blog-list` module is wired but commented out in the registry

The codebase has the platform code class fully implemented (with `per_page` setting + restrictions), and the page-builder settings template `blog-list.tpl` is present. However, the entry in `App\Services\Module::$widgets_map` for `blog-list` is **commented out** (annotated `//@todo 50-60% ready`). At the time of writing, the block is therefore NOT available in the picker — see [[design-module-pb-blog-list]] for details. (verify against current main branch)

### Cache invalidation

Saving a page invalidates the page's cache key and (if the page is assigned to a system slot) the `error404` / `private-shop:redirect_page` caches — see [[marketing-landing-pages]]. The next storefront request renders the new arrangement.

## Related

- [[marketing-landing-pages]] — Dynamic pages — the only surface where page-builder modules are used.
- [[design-modules]] — theme-wide module catalogue (shares some module types with the page builder).
- [[design-modules-layout]] — sibling category: theme-wide layout settings (header / footer / buttons / grid).
- [[design-modules-utility]] — sibling category: utility modules, some also page-builder-only.
- [[plan-gates]] — `storefront_builder` plan feature gates the page builder.
- [[apps-yotpo-settings]] — gates `yotpo-reviews` block.
- [[apps-store-locations]] — gates `store_locations` block.
- [[apps-product-review]] — gates `product_review` / `request_review` blocks.
- [[brand-model]] — gates `brand-model` block.
- [[marketing-subscribers]] — provides the form catalogue for `cc_form`.

## Open questions

- 📡 **App-uninstall fallback per module.** Each app-gated module should fall back gracefully when the app is uninstalled mid-life. Confirm per module; some show a "not installed" alert (e.g., `product_review`, `request_review`, `store_locations`), others may silently render nothing. (verify)
- ⏸️ **`blog-list` shipping date.** The module is annotated `//@todo 50-60% ready` in the registry — track when it's enabled in production.
