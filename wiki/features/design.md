---
type: feature
nav_path: "Design"
route_name: admin.templates.list
route_path: /admin/storefront/templates
aliases: ["Design", "Дизайн", "Storefront pillar", "Магазин", "Мой магазин"]
tags: [design, storefront, hub]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 3
---
# Design

## Purpose

Top-level sidebar pillar that groups every **storefront design** surface in one place. From here the merchant picks the store's **theme** (free or paid), edits the **navigation menus** (header, footer, mobile), drops in / re-orders **modules** on the homepage and category pages, opens the **Theme Editor** to tweak colours / fonts / CSS, opens the **Page Builder** to compose drag-and-drop landing pages, and reaches the **Static Pages** CMS (also surfaced under Marketing). The actual editing happens inside each sub-screen; this pillar is the navigation hub for everything that controls how the storefront LOOKS and how visitors NAVIGATE through it.

The sidebar icon is the pen-paintbrush (`fa-light fa-pen-paintbrush`). The label is **Дизайн** (BG) / **Design** (EN), translation key `sidebar.storefront`. The HTML class on the sidebar item is still `my-store` and its internal name is `my_store` — legacy artifacts from when the pillar was labelled "My Store" / "Магазин".

## Where to find it

Top-level sidebar pillar **Дизайн** (BG) / **Design** (EN). Position depends on enabled apps but it typically sits below Marketing and above Apps / Settings.

Clicking the pillar label routes to `/admin/storefront/templates` (the Themes screen) — same as the **Themes** child. Clicking any other child opens that child's screen directly.

## What the merchant can do here

The pillar exposes these sub-screens, grouped by the three sub-headers in the sub-menu (**Редакция на дизайн** / Design edit, **Страници** / Static Pages, **Настройки** / Settings):

**Top of the menu (no header):**

- **Избери дизайн** / **Themes** — pick / preview / install one of CloudCart's storefront themes (free or paid). Route: `admin.templates.list`. See [[design-themes]].
- **Навигация** / **Navigation** — manage the storefront menus (header menu, footer menu, mobile menu, sub-menus). Route: `admin.navigation.list`. See [[design-navigation]].
- **Лого** / **Logo** — opens an ajax panel for uploading store logo / favicon / social-share image. Route key: `admin.setting.logo_panel`. See [[design-themes]] for the asset slots.

**Под "Редакция на дизайн" / under "Design edit":**

- **Цветове и шрифтове** / **Colors & typography** — opens the full-screen Theme Editor at `/admin/builder` (colours, fonts, SCSS variables of the active theme). See [[design-theme-editor]].
- **Добавяне на CSS/JS** / **Custom CSS/JS** — inject custom CSS or JavaScript into the storefront (advanced). Route: `admin.custom.assets`. See [[design-custom-assets]].

**Под "Страници" / under "Static Pages":**

- **Начална** / **Homepage** — opens the homepage in the Page Builder. See [[marketing-landing-pages]].
- **Целеви страници** / **Landing Pages** — list + add custom landing pages. Route: `admin.pages.list`. See [[marketing-landing-pages]].
- **Успешна поръчка** / **Thank You Page** — edit the post-checkout thank-you page in the Page Builder. See [[marketing-landing-pages]].
- **Грешка 404** / **Error 404** — edit the storefront 404 page in the Page Builder. See [[marketing-landing-pages]].
- **Често Задавани Въпроси** / **FAQ** — add an FAQ page via the Page Builder. See [[marketing-landing-pages]].
- **Външна страница** / **Landing page (external)** — add a generic landing page via the Page Builder. See [[marketing-landing-pages]].

**Под "Настройки" / under "Settings":**

- **Модули** *(BG) / **Widgets** *(EN)* — add / remove / re-order homepage, category-page and product-page modules. Route: `admin.storefront.widgets` → `/admin/storefront/widgets`. See [[design-modules]]. (EN label is still "Widgets" — see the BG↔EN asymmetry note below.)

## What the merchant cannot do here

This is a navigation hub with no editable fields of its own — every operation happens inside a child screen. The merchant cannot:

- Build a theme from scratch — only pick from CloudCart's catalogue (the Theme Editor tweaks the active theme; it does not create a new one).
- Create / publish custom module types — only configure the modules shipped by the active theme.
- Edit the theme's underlying Smarty templates from this UI — that requires a CloudCart-staff customisation or a paid theme service.

## Settings & fields

Not applicable — this pillar is a navigation hub with no form fields.

## Business rules

### Visibility — driven by AdminPermissions

The Design pillar is shown to a staff member if their role grants any of these permission keys: `store`, `store.templates`, `store.pages`, `store.navigation`, `store.modules`, `store.builder`, `store.blog_articles`, `store.blog_categories`, `store.blog_comments`, `store.static_pages`, `marketing.static_pages`. A staff member with none of these never sees the pillar in their sidebar.

### Per-sub-screen visibility cascades down

Each child has its own permission gate — e.g. **Themes** requires `store` or `store.templates`; **Navigation** requires `store` or `store.navigation`; **Modules** requires `store` or `store.modules`; **Theme Editor** and **Page Builder** require `store` or `store.builder`. So a "design only" role can be narrowed to "Themes only" or "Navigation only" via the deeper keys.

### Theme decides what modules and page-builder blocks are available

Many modules and page-builder block types are theme-shipped — the active theme determines which modules the merchant can drop on the homepage / category / product pages, and which block types the page builder offers. Changing the theme can hide modules configured under the previous theme. See [[design-themes]] for what is preserved across a theme switch.

### Unpaid theme blocks the rest of the admin

If the merchant is on a **paid theme that hasn't been paid for yet** (`unpaid_template` flag on the site), every admin route — except Themes / Checkout / Login — redirects to the checkout for that theme. The merchant must complete payment or switch to a free theme before the rest of the admin panel becomes usable. See [[design-themes]] for the full flow.

## Related

### Children of this pillar
- [[design-themes]] — theme picker (free + paid catalogue, install, change, purchase flow); also the Logo / favicon / social-share image asset slots.
- [[design-theme-editor]] — color / font / SCSS-variable editor for the active theme (opens at `/admin/builder`).
- [[design-navigation]] — storefront menus (header, footer, mobile, sub-menus).
- [[design-modules]] — homepage / category / product-page modules (BG "Модули", EN "Widgets").
- [[marketing-landing-pages]] — Static Pages CMS (Homepage, Thank You, 404, FAQ, Landing Pages); also under Marketing.
- [[design-custom-assets]] — custom CSS/JS injection (advanced).
- [[admin-sidebar-navigation]] — full Дизайн sub-menu table with translation keys and routes verified against `sidebar.tpl` + lang files.

### Storefront-side concepts
- [[storefront-architecture]] — how the storefront renders the active theme (Smarty templates, caching, asset bundles).
- [[theme-customization-layers]] — the theme → Theme Editor → Custom CSS/JS customization cascade.
- [[storefront-themes-catalog]] — the free / paid theme catalogue + pricing tiers behind the Themes picker.
- [[widget-vs-page-builder-block]] — Modules (theme widgets) vs Page Builder blocks: what each is and when to use which.
- [[marketing-blog-articles]] — blog articles (chronological CMS content distinct from landing pages).
- [[seo-handling]] — site-wide SEO concept overview.
- [[marketing-seo]] — SEO hub (meta info, 301 redirects, sitemap).

### Plan / billing context
- [[plan-gates]] — plan-tier caps affecting Design (e.g., static-pages count, page-builder usage).

## How it works (verified against backend, 2026-06-10)

- The label comes from translation key `sidebar.storefront` (**"Дизайн"** in `lang/bg/sidebar.php`, **"Design"** in `lang/en/sidebar.php`); the default click-target is `admin.templates.list` (Themes screen). The whole Дизайн sub-menu is rendered in legacy Smarty (`sidebar.tpl`). There is no `/admin/storefront-new/*` Vue route group; sub-menus are NOT migrated to Vue. Each sub-item has its own narrower permission gate (e.g., `store.builder` for Colors & typography; `store.modules` for Модули / Widgets).
- The **Theme Editor** (Цветове и шрифтове) and **Page Builder** open separate full-screen builder apps at `/admin/builder` and `/admin/marketing/pages/builder` respectively (NOT embedded admin views). The Page Builder is the same surface as the builder-type Landing Pages editor in [[marketing-landing-pages]].
- The Page Builder itself is NOT plan-gated; any plan tier can access it (the underlying gates are quantity caps in [[plan-gates]], not access caps).
- BG↔EN label asymmetry: the Bulgarian `sidebar.widgets` translation reads "Модули"; the English value is still "Widgets". The merchant sees different sub-item labels depending on UI locale. See [[admin-sidebar-navigation]] for the full BG / EN label table.

## Open questions

_None — pillar hub fully verified against backend code._
