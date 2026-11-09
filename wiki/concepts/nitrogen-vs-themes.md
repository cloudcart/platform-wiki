---
type: concept
nav_path: "Concept → Nitrogen or a standard theme"
aliases: ["Nitrogen vs theme", "Nitrogen vs standard theme", "Nitrogen or theme", "Standard theme vs Nitrogen", "Classic theme vs Nitrogen", "Theme vs headless", "Make a design", "Build a design", "Custom design", "Own design", "Custom storefront design", "Redesign", "Edit theme templates", "Edit template files", "Standard theme", "Ready-made templates", "Готови шаблони", "Нитроген или шаблон", "Нитроген или тема", "Нитроген срещу тема", "Разлика между Nitrogen и тема", "Витрина с Nitrogen", "Витрина или тема", "Направи ми дизайн", "Искам дизайн", "Нов дизайн", "Собствен дизайн", "Индивидуален дизайн", "Уникален дизайн", "Редизайн", "Редакция на темплейт", "Редакция на темплейтите", "Промяна на темплейт", "Стандартна тема", "Стандартни теми"]
tags: [nitrogen, headless, design, themes, metafields, metaobjects, concepts]
plan_gates: []
created: 2026-11-04
updated: 2026-11-05
source_count: 5
---

# Nitrogen or a standard theme

## Definition

A CloudCart store shows its customers one of two kinds of storefront. Both run on the same admin, catalogue, orders and checkout.

- A **standard theme** is a ready design from CloudCart's catalogue ([[design-themes]]). The merchant adjusts what the theme exposes.
- A **Nitrogen storefront** is the store's own application, made from CloudCart's starter ([[headless-starter]]). It reads the store through the Storefront API ([[headless-storefront]]).

**When a merchant wants to make a design, the answer is Nitrogen, not editing a theme's templates.** Nitrogen was built for full freedom. Together with metafields and metaobjects ([[metafields-metaobjects]]), it gives a fully custom, interactive online store on modern technology, whose content the merchant still manages from the admin. A theme's template files are not open to merchants at all. The admin puts the same choice to the merchant: clicking **Design** opens a page with Nitrogen, marked **Recommended**, and ready-made templates ([[design]]).

Changing the colours, fonts, logo, menus or module order of the theme a store already runs is not making a design. Those stay on the [[design]] screens.

> **For the agent:** once the merchant chooses Nitrogen, use the `cloudcart-nitrogen` skill before the first line of code, and start from the starter. See [[headless-starter]].

## Scope

### Side by side

| | Standard theme | Nitrogen storefront |
|---|---|---|
| **Starting point** | A theme from the catalogue, installed from Design → Themes | The starter, a working storefront with its pages already built ([[headless-starter]]) |
| **Design freedom** | What the theme exposes: Theme Editor variables, its modules and page-builder blocks, and code added to every page's head ([[theme-customization-layers]]). Its templates cannot be edited, and a theme of the store's own cannot be uploaded | Everything. Every page, component and route is the store's own code |
| **Technology** | Smarty pages rendered on the server, with jQuery bundled per theme ([[storefront-architecture]]) | React, React Router, TypeScript and Tailwind CSS, hosted on Nova ([[headless-nova-platform]]) |
| **Interactivity** | What the theme ships, plus code pasted into Custom CSS/JS | Any component the design calls for, such as a configurator, a comparison tool or a product builder |
| **Metafields and metaobjects** | Not shown. Their only effect is indirect: a metafield can decide what goes into a smart collection | Read through the Storefront API and shown wherever the design wants them ([[metafields-nitrogen]]) |
| **What the merchant edits in the admin** | Theme settings, modules and page-builder pages | Metafield values and metaobject entries, including whole pages built from sections ([[metafields-use-case-page-sections]]), plus CMS pages, the blog and menus |
| **Who builds and changes it** | The merchant, on admin screens | An AI agent with the `cloudcart-nitrogen` skill, or a developer. A change of layout is a code change and a deploy |
| **Going live** | Installing a theme changes the store at once | It runs on its own `{handle}.cloudcart.dev` address until a domain is routed to it. *Back to the store theme* returns the domain ([[headless-nitrogen-overview]]) |

### What is the same on both

Products, categories, customers, orders, discounts, payments and shipping are managed in the same admin. Checkout and payment stay the platform's: a Nitrogen cart hands over through `Cart.checkoutUrl` ([[headless-checkout-submit]]). A store serves one language either way ([[multi-language]]).

### What a Nitrogen storefront does not take from a theme

- **The Theme Editor, modules, page-builder pages and Custom CSS/JS** belong to themes. None of them reaches a Nitrogen storefront, whose look is its own code.
- **An app's storefront widget** appears only when the storefront is built to show it, through the Storefront API. The starter already covers reviews, fast order, back-in-stock requests, cross-sell and up-sell offers, and cookie consent.
- **On a routed domain**, the storefront applies the store's 301 redirects itself, and links in store e-mails that open the platform's pages do not work there yet. [[headless-legacy-vs-nitrogen]] has the full map.

### When a theme is enough

A merchant who wants to open a store with no code, no agent and no developer installs a theme. Moving to Nitrogen later loses nothing in the admin, and the starter keeps the store's own addresses, so links and search results keep working.

## Contrasts

- **Nitrogen is not in Design → Themes.** The catalogue holds only standard themes. Nitrogen has its own area, the first link under **Design** (`/admin/nitrogen`, [[nitrogen]]).
- **The starter vs a theme.** A theme is configured from the admin. The starter's files become the project's own and change as code.
- **This page vs [[headless-legacy-vs-nitrogen]].** This page compares the two for a merchant choosing. That one maps which addresses the platform keeps on a routed domain.
- **Standard, classic and legacy theme** are the same thing under the names other pages use. The page that **Design** opens calls them ready-made templates.

## Where it applies

- [[design]]: the page that asks the merchant to choose, and the menu.
- [[design-themes]]: the ready-made templates.
- [[nitrogen]] and [[nitrogen-create-storefront]]: where a storefront is created.
- [[metafields-use-cases]]: what to build with the store's own data.
- [[ai-agent-capabilities]]: an agent doing the build.

## Related

- [[headless-starter]]: the starting point, and the agent's rule.
- [[headless-storefront]]: Nitrogen, Nova and the Storefront API.
- [[metafields-metaobjects]]: the store's own fields and content types.
- [[metafields-nitrogen]]: how a storefront reads them.
- [[theme-customization-layers]]: what can be changed on a standard theme.
- [[storefront-themes-catalog]]: the themes on offer.

## Open Questions

- Whether Nitrogen is billed separately from the plan is open, see [[headless-storefront]].
