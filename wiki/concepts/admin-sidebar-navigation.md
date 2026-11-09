---
type: concept
nav_path: "Concept → Admin sidebar navigation"
aliases: ["Admin sidebar", "Sidebar navigation", "Left navigation", "Main menu", "Главно меню", "Странична навигация", "Sidebar structure", "Admin nav"]
tags: [admin, navigation, sidebar, ui, structure]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

# Admin sidebar navigation (structure + rendering)

## Definition

The CloudCart admin's **left-rail sidebar** is the merchant's primary navigation surface. It carries **9 top-level items** in a fixed display order, plus a profile / notifications / external-link cluster at the top and bottom.

The merchant-facing labels are locale-dependent (BG vs EN) and must be cited **exactly** — a wrong label (e.g. calling a section "Design" when a BG merchant sees "Дизайн") sends support tickets down the wrong navigation tree.

**Critical asymmetry — "Модули" vs "Widgets":** the Storefront Modules screen (route `admin.storefront.widgets` → `/admin/storefront/widgets`) was renamed to **"Модули" in BG only**. The English label was never updated, so it still reads **"Widgets"**. A BG-locale merchant sees **Дизайн → Модули**; an EN-locale merchant sees **Design → Widgets**. Same screen, different label per locale. See [[design-modules]].

## Scope

Covered: the 9 top-level items + their locale labels, what clicking "Дизайн" opens, its full sub-menu (Nitrogen first, "Модули" last), and the nav_path conventions used elsewhere in the wiki.

Not covered: per-screen feature details (the individual `wiki/features/` pages); per-item permission gating (see [[settings-staff]]); how the dashboard "Setup guide" composes its steps (see [[dashboard]]).

## Contrasts

- **Translation key vs displayed label** — `sidebar.widgets` displays as "Модули" in BG but "Widgets" in EN (see Definition). Cite the displayed label in body prose; preserve the route / permission key (`store.widgets`, `admin.storefront.widgets`) verbatim.
- **Lang-file label vs per-site value** — where a screenshot differs from the lang-file label (e.g. screenshot **Анализи** vs lang-file "Анализ"), a per-site translation override or an outdated lang entry is in play; the screenshot is what that merchant actually sees. Verified on site 2160: no `sidebar.*` overrides, so the lang-file value applies there.

## Where it applies

The **9 top-level items** in display order (labels verified against the BG and EN sidebar lang files and the 2026-06-10 admin screenshots):

| # | BG (merchant-visible) | EN | Translation key | HTML class | Sub-menu (top level) |
|---|---|---|---|---|---|
| 1 | **Първи стъпки** *(setup-progress chip)* | Setup guide | (composed in the dashboard) | n/a | Progress chip → Onboarding flow. See [[dashboard]]. |
| 2 | **Поръчки** | Orders | `sidebar.orders` | `sidebar-orders-link` | Поръчки · Поръчани продукти · Незавършени · Фактури |
| 3 | **Продукти** | Products | `sidebar.products` | `sidebar-products-link` | Продукти · Инвентар · Категории · Производители · Колекции · **РАЗШИРЕНИ** · Разновидности · Характеристики · Статуси на продуктите · Очаквани продукти · Любими продукти · Продуктови етикети |
| 4 | **Клиенти** | Customers | `sidebar.customers` | `sidebar-customers-link` | Клиенти · Клиентски групи · Персонализирани полета |
| 5 | **Анализ** *(screenshot: **Анализи** — per-site `(verify)`)* | Analytics | `sidebar.analytics` | `sidebar-reports-link` | Табло за анализи · **АНАЛИЗИ** · Общо продажби · Общо поръчки · Продажби по продукти · Продажби по пакети · Продукти по продадени бройки · Трафик по продукти · … |
| 6 | **Маркетинг** | Marketing | `sidebar.marketing` | `sidebar-marketing-link` | Marketing suite · Кампании ▾ · Отстъпки · Канали ▾ · SEO ▾ · Бутон за покупка · Блог ▾ · **ПРИЛОЖЕНИЯ** · Cart Rules · Bumpcart |
| 7 | **Приложения** | Apps | `sidebar.apps` | `sidebar-apps-link` | Apps catalogue (see [[apps]]) |
| 8 | **Дизайн** | **Design** | `Design` | n/a | Opens a page with the choice between Nitrogen and ready-made templates; sub-menu below, starting with **Nitrogen** |
| 9 | **Настройки** | Settings | `sidebar.settings` | `sidebar-settings-link` | See [[settings]] hub for the full sub-menu |

**Nitrogen is the first link under Дизайн**, at `/admin/nitrogen` ([[nitrogen]]). It has no top-level entry.

### What clicking "Дизайн" opens

The page `/admin/design`, *"How do you want to design your store?"*, with the choice between **Nitrogen** and **Ready-made templates** ([[design]]). A staff member without the **Nitrogen Storefronts** permission goes to **Избери дизайн** instead, and one with Nitrogen but without the templates permission goes to Nitrogen. The sub-menu is open on that page and on Nitrogen's pages.

### Дизайн sub-menu (order and addresses verified 2026-11-05 against the admin's code)

**"Модули"** sits under the **НАСТРОЙКИ** subsection of Дизайн — it is **not** a top-level Design item. The English labels are the code's; the Bulgarian ones come from translations held outside the code.

| Item (BG) | Item (EN) | Address | Wiki |
|---|---|---|---|
| **Nitrogen** *(tagged new)* | **Nitrogen** | `/admin/nitrogen` | [[nitrogen]] |
| **Избери дизайн** | **Choose Design** | `/admin/design/templates` | [[design-themes]] |
| **Навигация** | **Navigation** | `/admin/design/navigation` | [[design-navigation]] |
| **Банери** *(specific clients only)* | **Banners** | route `design.banners` | (client-specific carve-out) |
| **Лого** | **Logo** | `/admin/settings/brand` | [[settings-brand]] |
| **Редакция на дизайн** | **Design edit** | (section header — not clickable) | — |
| **Цветове и шрифтове** | **Colors and Fonts** | `/admin/builder` | [[design-theme-editor]] |
| **Добавяне на CSS/JS** | **Custom CSS/JS** | `/admin/design/custom-assets` | [[design-custom-assets]] |
| **Страници** | **Pages** *(section header)* | (section header) | — |
| **Начална** | **Homepage** | `/admin/marketing/pages/builder/system_page/home` | [[marketing-landing-pages]] |
| **Целеви страници** | **Static pages** | `/admin/design/pages` | [[marketing-landing-pages]] |
| **Успешна поръчка** | **Thank you page** | `/admin/marketing/pages/builder/system_page/thank_you` | [[marketing-landing-pages]] |
| **Грешка 404** | **Error 404 page** | `/admin/marketing/pages/builder/system_page/error.404` | [[marketing-landing-pages]] |
| **Често Задавани Въпроси** | **FAQ** | `/admin/design/pages/add/faq` | [[marketing-landing-pages]] |
| **Външна страница** | **External page** | `/admin/design/pages/add/landing` | [[marketing-landing-pages]] |
| **Настройки** | **Settings** *(section header)* | (section header) | — |
| **Модули** | **Widgets** ← *not "Modules" in EN* | `/admin/storefront/widgets` | [[design-modules]] |

Nitrogen shows only with the **Nitrogen Storefronts** permission. **Начална**, **Успешна поръчка** and **Грешка 404** show only on a theme with the page builder.

**Nav_path convention for pages under Дизайн → Модули:** use `"Design → Modules → <Category> → <Module>"`. The **НАСТРОЙКИ** divider inside Дизайн is a typographic section header, not a clickable nav level, so it does **not** appear in the `nav_path` breadcrumb.

### Permission gating

Each sidebar item is wrapped in a permission check. Staff with restricted roles see only items where they hold at least one matching permission. See [[settings-staff]] for the role-permission matrix.

## Related

- [[settings-staff]] — role permission keys gate every sidebar item.
- [[dashboard]] — drives the "Първи стъпки" / Setup guide top-level chip.
- [[settings]] — full sub-menu under "Настройки".
- [[design-modules]] — the Modules screen (route `/admin/storefront/widgets`).
- [[design]] — the page "Дизайн" opens.
- [[nitrogen]] — the first link under "Дизайн".
- [[design-themes]] — Choose design / templates / theme editor.
- [[design-navigation]] — Navigation menus editor.
- [[design-custom-assets]] — Custom CSS / JS injection.
- [[marketing-landing-pages]] — Landing-page family inside Дизайн → СТРАНИЦИ.
- [[apps]] — Apps catalogue.

## Open Questions

- Whether the screenshot label **Анализи** (vs lang-file "Анализ") is a per-site override or a stale lang entry `(verify)`.
