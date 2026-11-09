---
type: feature
nav_path: "Design"
route_name: design
route_path: /admin/design
aliases: ["Design", "Дизайн", "Storefront pillar", "Магазин", "Мой магазин", "Направи ми дизайн", "Нов дизайн", "Собствен дизайн", "Редизайн", "Промяна на дизайна", "How do you want to design your store?", "Design choice page", "Ready-made templates", "Go to Nitrogen", "See the templates", "Готови шаблони", "Готов шаблон", "Nitrogen или шаблон", "Избор на дизайн"]
tags: [design, storefront, hub]
plan_gates: []
created: 2026-05-23
updated: 2026-11-09
source_count: 4
---
# Design

## Purpose

> **Making a design? Go to Nitrogen.** When a merchant wants a design of their own, a redesign, or something a theme's settings cannot do, the answer is a Nitrogen storefront, not editing a theme's templates. See [[nitrogen-vs-themes]]. Nitrogen starts from [[headless-starter]], opens at **Design → Nitrogen** ([[nitrogen]]), and an agent building it must use the `cloudcart-nitrogen` skill. The other screens below adjust the standard theme the store already runs.

Top-level sidebar pillar that groups every **storefront design** surface in one place. Clicking it opens a page that asks how the store should be designed: with **Nitrogen** or with **ready-made templates**. Its sub-menu starts with **Nitrogen**. After it, the merchant picks the store's **theme** (free or paid), edits the **navigation menus**, edits the theme's **modules** on the homepage, category and product pages, opens the **Theme Editor** to tweak colours / fonts / CSS, opens the **Page Builder** to compose drag-and-drop landing pages, and reaches the **Static Pages** CMS. The actual editing happens inside each sub-screen; this pillar is the navigation hub for everything that controls how the storefront LOOKS and how visitors NAVIGATE through it.

The sidebar icon is the pen-paintbrush (`fa-light fa-pen-paintbrush`). The label is **Дизайн** (BG) / **Design** (EN).

## Where to find it

Top-level sidebar pillar **Дизайн** (BG) / **Design** (EN). Position depends on enabled apps but it typically sits below Marketing and above Apps / Settings.

What clicking the pillar opens depends on the staff member's permissions. The store owner gets the choice page.

| Permissions | Clicking **Design** opens |
|---|---|
| **Nitrogen Storefronts**, and `store` or `store.templates` | The choice page, `/admin/design` |
| **Nitrogen Storefronts**, without `store` or `store.templates` | Nitrogen, `/admin/nitrogen` |
| No **Nitrogen Storefronts** | **Choose Design**, `/admin/design/templates` |

The sub-menu is open on the choice page, on Nitrogen's pages, where **Nitrogen** is lit, and on the theme screens. Clicking a child opens that child's screen directly.

## What the merchant can do here

### Choose between Nitrogen and ready-made templates

The page at `/admin/design` is titled *"How do you want to design your store?"*. It only leads on: it saves nothing and changes nothing on the store. It has two cards, the Nitrogen one wider:

| Card | What it says | Button |
|---|---|---|
| **Nitrogen**, with a purple border and the **Recommended** badge | *"Describe the store you want to your AI agent, and it builds it with a design entirely your own. Products, orders and payments stay in CloudCart."* Then four ticked lines: *Build with your AI agent*, *A design entirely your own*, *Everything stays in CloudCart*, *Live in one command*. | **Go to Nitrogen** opens [[nitrogen-storefronts]] |
| **Ready-made templates** | *"A finished design you use as it comes, with no option to edit or customize it."* | **See the templates** opens [[design-themes]] |

The menu's links for a theme's colours and fonts, Custom CSS/JS, modules and page-builder pages stay as they were ([[theme-customization-layers]]).

### The sub-menu

These sub-screens appear in this order, grouped by the three sub-headers in the sub-menu (**Редакция на дизайн** / Design edit, **Страници** / Pages, **Настройки** / Settings):

**Top of the menu (no header):**

- **Nitrogen** — tagged **new**. The store's own storefronts. Route: `nitrogen.storefronts` → `/admin/nitrogen`. See [[nitrogen]].
- **Избери дизайн** / **Choose Design** — pick / preview / install one of CloudCart's storefront themes (free or paid). Route: `design.templates` → `/admin/design/templates`. See [[design-themes]].
- **Навигация** / **Navigation** — manage the storefront menus. Route: `design.navigation` → `/admin/design/navigation`. See [[design-navigation]].
- **Лого** / **Logo** — opens Brand settings at `/admin/settings/brand`. See [[settings-brand]].

**Под "Редакция на дизайн" / under "Design edit":**

- **Цветове и шрифтове** / **Colors and Fonts** — opens the full-screen Theme Editor at `/admin/builder` (colours, fonts, SCSS variables of the active theme). See [[design-theme-editor]].
- **Добавяне на CSS/JS** / **Custom CSS/JS** — inject custom CSS or JavaScript into the storefront (advanced). Route: `design.custom-assets` → `/admin/design/custom-assets`. See [[design-custom-assets]].

**Под "Страници" / under "Pages":**

- **Начална** / **Homepage** — opens the homepage in the Page Builder. See [[marketing-landing-pages]].
- **Целеви страници** / **Static pages** — list + add custom landing pages, at `/admin/design/pages`. See [[marketing-landing-pages]].
- **Успешна поръчка** / **Thank you page** — edit the post-checkout thank-you page in the Page Builder. See [[marketing-landing-pages]].
- **Грешка 404** / **Error 404 page** — edit the storefront 404 page in the Page Builder. See [[marketing-landing-pages]].
- **Често Задавани Въпроси** / **FAQ** — add an FAQ page. See [[marketing-landing-pages]].
- **Външна страница** / **External page** — add a generic landing page. See [[marketing-landing-pages]].

**Под "Настройки" / under "Settings":**

- **Модули** *(BG) / **Widgets** *(EN)* — edit or switch off the active theme's modules; the theme fixes which exist and where (to add or re-order blocks, use a Dynamic page). Route: `/admin/storefront/widgets`. See [[design-modules]].

## What the merchant cannot do here

This is a navigation hub with no editable fields of its own — every operation happens inside a child screen. The merchant cannot:

- Build a theme from scratch — only pick from CloudCart's catalogue (the Theme Editor tweaks the active theme; it does not create a new one). A design of the store's own is made with Nitrogen ([[nitrogen-vs-themes]]).
- Create module types, or add, remove or re-order the theme's modules.
- Edit the theme's underlying Smarty templates. A different design is made with Nitrogen, not by changing a theme ([[nitrogen-vs-themes]]).

## Settings & fields

Not applicable — neither the pillar nor the choice page has form fields.

## Business rules

### Visibility — driven by AdminPermissions

The Design pillar is shown to a staff member if their role grants any of these permission keys: `nitrogen`, `store`, `store.templates`, `store.pages`, `store.navigation`, `store.widgets`, `store.builder`, `store.blog_articles`, `store.blog_categories`, `store.blog_comments`, `store.static_pages`, `marketing.static_pages`. A staff member with none of these never sees the pillar in their sidebar.

### Per-sub-screen visibility cascades down

Each child has its own permission gate — e.g. **Nitrogen** requires `nitrogen` (the **Nitrogen Storefronts** permission); **Choose Design** requires `store` or `store.templates`; **Navigation** requires `store` or `store.navigation`; **Modules** requires `store` or `store.widgets`; **Theme Editor** and **Page Builder** require `store` or `store.builder`. So a "design only" role can be narrowed to "Themes only" or "Navigation only" via the deeper keys.

**Homepage**, **Thank you page** and **Error 404 page** also need a theme with the page builder.

### Theme decides what modules and page-builder blocks are available

Many modules and page-builder block types are theme-shipped — the active theme determines which modules the merchant can drop on the homepage / category / product pages, and which block types the page builder offers. Changing the theme can hide modules configured under the previous theme. See [[design-themes]] for what is preserved across a theme switch.

### Unpaid theme blocks the rest of the admin

If the merchant is on a **paid theme that hasn't been paid for yet** (`unpaid_template` flag on the site), every admin route — except the choice page, Themes, Checkout, Billing and Login — redirects to the checkout for that theme. Nitrogen's pages redirect too. The merchant must complete payment or switch to a free theme before the rest of the admin panel becomes usable. See [[design-themes-unpaid-middleware]] for the full flow.

## Related

### Making a design
- [[nitrogen-vs-themes]] — Nitrogen compared with a standard theme, and why a design of the store's own goes to Nitrogen.
- [[nitrogen]] — the first link of this menu: every Nitrogen screen.
- [[headless-starter]] — the starter a Nitrogen storefront is made from, and the agent's `cloudcart-nitrogen` rule.
- [[metafields-metaobjects]] — the store's own fields and content types; shown on Nitrogen storefronts, not on standard themes.

### Children of this pillar
- [[design-themes]] — theme picker (free + paid catalogue, install, change, purchase flow).
- [[settings-brand]] — where **Logo** leads.
- [[design-theme-editor]] — color / font / SCSS-variable editor for the active theme (opens at `/admin/builder`).
- [[design-navigation]] — storefront menus.
- [[design-modules]] — homepage / category / product-page modules (BG "Модули", EN "Widgets").
- [[marketing-landing-pages]] — Static Pages CMS (Homepage, Thank You, 404, FAQ, Landing Pages); also under Marketing.
- [[design-custom-assets]] — custom CSS/JS injection (advanced).
- [[admin-sidebar-navigation]] — full Дизайн sub-menu table with addresses.

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

## How it works (verified against backend, 2026-11-05)

- The label comes from translation key `sidebar.storefront` (**"Дизайн"** in `lang/bg/sidebar.php`, **"Design"** in `lang/en/sidebar.php`). The choice page and the themes, navigation and Custom CSS/JS screens are all pages of the modern admin, at `/admin/design` and under it; **Modules** stays at `/admin/storefront/widgets`. Each sub-item has its own narrower permission gate (e.g., `store.builder` for Colors & typography; `store.modules` for Модули / Widgets).
- The **Theme Editor** (Colors and Fonts) and **Page Builder** open separate full-screen builder apps at `/admin/builder` and `/admin/marketing/pages/builder` respectively (NOT embedded admin views). The Page Builder is the same surface as the builder-type Landing Pages editor in [[marketing-landing-pages]].
- The Page Builder URL is gated by the `storefront_builder` plan feature ([[design-modules-page-builder]]); which plans carry it is set in the billing catalog (verify).
- BG↔EN label asymmetry: the Bulgarian `sidebar.widgets` translation reads "Модули"; the English value is still "Widgets". The merchant sees different sub-item labels depending on UI locale. See [[admin-sidebar-navigation]] for the full BG / EN label table.

## Open questions

_None — pillar hub verified against the admin's code._
