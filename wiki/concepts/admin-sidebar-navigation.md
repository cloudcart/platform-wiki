---
type: concept
nav_path: "Concept → Admin sidebar navigation"
aliases: ["Admin sidebar", "Sidebar navigation", "Left navigation", "Main menu", "Главно меню", "Странична навигация", "Sidebar structure", "Admin nav"]
tags: [admin, navigation, sidebar, ui, structure]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Admin sidebar navigation (structure + rendering)

## Definition

The CloudCart admin's **left-rail sidebar** is the merchant's primary navigation surface. It carries **9 top-level items** in a fixed display order, plus a profile / notifications / external-link cluster at the top and bottom.

The merchant-facing labels are locale-dependent (BG vs EN) and must be cited **exactly** — a wrong label (e.g. calling a section "Design" when a BG merchant sees "Дизайн") sends support tickets down the wrong navigation tree.

**Critical asymmetry — "Модули" vs "Widgets":** the Storefront Modules screen (route `admin.storefront.widgets` → `/admin/storefront/widgets`) was renamed to **"Модули" in BG only**. The English label was never updated, so it still reads **"Widgets"**. A BG-locale merchant sees **Дизайн → Модули**; an EN-locale merchant sees **Design → Widgets**. Same screen, different label per locale. See [[design-modules]].

## Scope

Covered: the 9 top-level items + their locale labels, the full sub-menu of the "Дизайн" item (where "Модули" lives), and the nav_path conventions used elsewhere in the wiki.

Not covered: per-screen feature details (the individual `wiki/features/` pages); per-item permission gating (see [[settings-staff]]); how the dashboard "Setup guide" composes its steps (see [[dashboard]]).

## Contrasts

- **HTML class name vs displayed label** — the "Дизайн" item carries the legacy HTML class `my-store` and the translation key `sidebar.storefront`, both survivors of an older "Design" label. Neither is the merchant-facing label. Cite the **displayed label per locale**, not the class or key.
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
| 8 | **Дизайн** | **Design** | `sidebar.storefront` | `sidebar-store-link` | See sub-menu below — Дизайн → Модули lives here |
| 9 | **Настройки** | Settings | `sidebar.settings` | `sidebar-settings-link` | See [[settings]] hub for the full sub-menu |

Items 8 and 9 are top-level chips, but their **sub-menus** are still rendered by the legacy admin layer rather than the modern one — so the "Дизайн" sub-menu structure below is the authoritative reference for that branch.

### Дизайн sub-menu (verified 2026-06-10 against the BG / EN sidebar lang files)

This is what the merchant sees on clicking "Дизайн". **"Модули"** sits under the **НАСТРОЙКИ** subsection of Дизайн — it is **not** a top-level Design item.

| Item (BG) | Item (EN) | Translation key | Route | Wiki |
|---|---|---|---|---|
| **Избери дизайн** | **Themes** | `sidebar.templates` | `admin.templates.list` | [[design-themes]] |
| **Навигация** | **Navigation** | `sidebar.navigation` | `admin.navigation.list` | [[design-navigation]] |
| **Банери** *(Zora / specific clients only)* | **Banners** | `sidebar.banners` | `admin.banners.list` | (client-specific carve-out) |
| **Лого** | **Logo** | `sidebar.logo` | `admin.setting.logo_panel` (ajax panel) | [[design-themes#Logo]] |
| **Редакция на дизайн** | **Design edit** | `sidebar.design_edit` | (section header — not clickable) | — |
| **Цветове и шрифтове** | **Colors & typography** | `global.label.colors` + `global.label.typography` | `/admin/builder` | [[design-themes#Theme Editor]] |
| **Добавяне на CSS/JS** | **Custom CSS/JS** | `template.custom_css_js` | `admin.custom.assets` | [[design-custom-assets]] |
| **Страници** | **Static Pages** *(section header)* | `sidebar.pages` | (section header) | — |
| **Начална** | **Homepage** | `sidebar.homepage` | `marketing/pages/builder/system_page/home` | [[marketing-landing-pages]] |
| **Целеви страници** | **Landing Pages** | `sidebar.static_pages` | `admin.pages.list` | [[marketing-landing-pages]] |
| **Успешна поръчка** | **Thank You Page** | `sidebar.thank_you_page` | `marketing/pages/builder/system_page/thank_you` | [[marketing-landing-pages]] |
| **Грешка 404** | **Error 404** | `sidebar.error_404` | `marketing/pages/builder/system_page/error.404` | [[marketing-landing-pages]] |
| **Често Задавани Въпроси** | **FAQ** | `sidebar.faq` | `marketing/pages/add/faq` | [[marketing-landing-pages]] |
| **Външна страница** | (no fixed EN) | `page.help.landing_page` | `marketing/pages/add/landing` | [[marketing-landing-pages]] |
| **Настройки** | **Settings** *(section header)* | `sidebar.settings` | (section header) | — |
| **Модули** | **Widgets** ← *not "Modules" in EN* | `sidebar.widgets` *(legacy key)* | `admin.storefront.widgets` → `/admin/storefront/widgets` | [[design-modules]] |

**Nav_path convention for pages under Дизайн → Модули:** use `"Design → Modules → <Category> → <Module>"`. The **НАСТРОЙКИ** divider inside Дизайн is a typographic section header, not a clickable nav level, so it does **not** appear in the `nav_path` breadcrumb.

### Permission gating

Each sidebar item is wrapped in a permission check. Staff with restricted roles see only items where they hold at least one matching permission. See [[settings-staff]] for the role-permission matrix.

## Related

- [[settings-staff]] — role permission keys gate every sidebar item.
- [[dashboard]] — drives the "Първи стъпки" / Setup guide top-level chip.
- [[settings]] — full sub-menu under "Настройки".
- [[design-modules]] — the Modules screen (route `/admin/storefront/widgets`).
- [[design-themes]] — Choose design / templates / theme editor.
- [[design-navigation]] — Navigation menus editor.
- [[design-custom-assets]] — Custom CSS / JS injection.
- [[marketing-landing-pages]] — Landing-page family inside Дизайн → СТРАНИЦИ.
- [[apps]] — Apps catalogue.

## Open Questions

- Migration of the Дизайн and Настройки **sub-menus** from the legacy layer to the modern admin — the top-level chips are already modern, but the sub-menus below them are not. Sequencing is `(verify)`.
- Whether the screenshot label **Анализи** (vs lang-file "Анализ") is a per-site override or a stale lang entry `(verify)`.
