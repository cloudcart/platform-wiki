---
type: feature
nav_path: "Design → Themes"
route_name: design.templates
route_path: /admin/design/templates
aliases: ["Themes", "Templates", "Storefront theme", "Theme picker", "Storefront template", "Choose design", "Ready-made templates", "Темплейт", "Темплейти", "Шаблон", "Готови дизайни", "Готови шаблони", "Избери дизайн"]
tags: [design, themes, templates]
plan_gates: ["change_theme"]
created: 2026-05-23
updated: 2026-11-09
source_count: 5
---

# Themes

## Purpose

> **Making a design of the store's own is not done here.** This screen installs ready themes, and their templates cannot be edited. A merchant who wants their own design goes to Nitrogen: [[nitrogen-vs-themes]].

The **Themes** screen is the merchant's catalogue of storefront themes (also called "templates") — where they see the **currently active** theme, browse **free** and **paid** theme catalogues, preview any theme on a live demo URL, **install** a free theme (or one already purchased), and **purchase** a paid theme through the in-platform checkout. Each theme controls the storefront's look-and-feel: layout, default modules, page-builder block library, default colours, default typography, and the customisation options exposed by the Theme Editor.

Changing the theme is a single click + confirmation, but it is a **big, store-wide visual change** — every storefront page switches (guests once their cached copy expires, up to 20 minutes). Merchants typically follow up with a pass through [[design-theme-editor]] (colours / fonts), [[design-modules]] (homepage layout), and [[design-navigation]] (menus) to tune the new theme to their brand.

This concept is split into 7 aspect pages — each covers one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[design-themes-catalogue]] — listing query, free/paid tabs, theme attributes (`mapping`, `price`, `active`, `coming_soon`, `new`, `in_dev`, `has_demo`), `is_paid` derivation, badges, sort order, screenshots.
- [[design-themes-install]] — the Install action, confirmation prompt, AJAX response, install transaction side-effects (CSS recompile, `db:translation` regen, demo-pages reseed, gate-vs-routing dual-write).
- [[design-themes-purchase]] — paid theme purchase flow, cart clearing, checkout, `redirectAfterPay` session key, theme-as-subscription model.
- [[design-themes-unpaid-middleware]] — the `unpaid_template` flag that locks the entire admin to Themes / Checkout / Login / Billing / 2FA until the merchant pays or switches to a free theme.
- [[design-themes-switch-effects]] — what's preserved vs lost on a switch: catalogue data, per-theme customisations, theme-specific modules, page-builder blocks, demo-pages reseed via `pages.json`, 500-version page-history cap.
- [[design-themes-plan-gates]] — the `change_theme` plan-feature gate + `store` / `store.templates` permission keys + the orthogonal paid-theme subscription requirement.
- [[design-themes-edge-cases]] — demo-user short-circuit, coming-soon teasers, in-dev CloudCart-staff-only themes, slug-driven demo-URL fallback, current-theme separate-query rendering, "already current" install error.

## Where to find it

Sidebar → **Design** → **Choose Design** (**Избери дизайн**), the link after **Nitrogen**. Also **See the templates** on the page that **Design** opens ([[design]]). A staff member without the **Nitrogen Storefronts** permission comes here directly on clicking **Design**.

Route `/admin/design/templates`. Breadcrumb reads **Design** → **Choose design**.

Sub-routes:

| Action | Route name | Path | Method |
|--------|------------|------|--------|
| List themes | `design.templates` | `/admin/design/templates` | GET |
| Install / change theme | `admin.api.design.templates.change` | `/admin/api/design/templates/{mapping}/change` | POST |
| Activate a theme after payment | `admin.design.templates.activate` | `/admin/design/templates/activate/{mapping}` | GET |

A paid theme is bought in the checkout panel that its **Buy** button opens on this screen.

Each theme is identified by a `mapping` slug (the theme's machine name, e.g., `flair`, `motion`, `summer`).

## What the merchant can do here

- See the **desktop preview** and **mobile preview** of the currently active theme side-by-side, with the active theme's name + description.
- Click **Theme Editor** to jump to `/admin/builder` (same as the Design → Theme Editor sidebar link) — see [[design-theme-editor]].
- Click **Hire expert** to open the in-platform paid-services catalogue (button: `adorimo.help.hire_expert_btn`) for paid customisation help.
- Browse the Free and Paid tabs of the theme catalogue — see [[design-themes-catalogue]].
- Install a free or already-purchased theme — see [[design-themes-install]].
- Buy a paid theme — see [[design-themes-purchase]].

## What the merchant cannot do here

- Cannot **preview** a theme on their own store with their own products — only the public demo URL is available.
- Cannot **install a paid theme** without buying it first.
- Cannot **return / refund** a purchased theme through this screen.
- Cannot **revert** to a previous theme by undo — switching back means installing the previous theme again (customisations are preserved per theme).
- Cannot **upload / import a custom theme** — only CloudCart's catalogue themes are installable. A design of the store's own is made with Nitrogen ([[nitrogen-vs-themes]]).
- Cannot **reach the theme's files on a server** — a store has no FTP, SSH, cPanel or database access ([[storefront-architecture]]); custom code goes in [[design-custom-assets]].

## Settings & fields

This screen has no form fields. The actionable inputs are documented in the aspect pages:

| Action | Where documented |
|--------|------------------|
| View / Install / Buy on a card | [[design-themes-catalogue]] |
| Install transaction details | [[design-themes-install]] |
| Buy / checkout details | [[design-themes-purchase]] |

## Business rules

The detailed rules live in the aspect pages. The high-level facts:

- **Switching themes is instantaneous and store-wide** (with a few seconds for CSS recompile + translation regen). See [[design-themes-install]].
- **Paid themes are subscriptions** — `model_type='theme'` + `mapping=<slug>` in `site_subscriptions`. See [[design-themes-purchase]].
- **Unpaid paid theme locks the admin** to a small allowlist of routes. See [[design-themes-unpaid-middleware]].
- **Demo-pages reseed runs on every install** — system-page slots may be silently reassigned. See [[design-themes-switch-effects]].
- **`change_theme` plan-feature gates the Install path** — not the catalogue browsing. See [[design-themes-plan-gates]].
- **Demo user is short-circuited** at install + middleware. See [[design-themes-edge-cases]].

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `change_theme` | Access gate | Path-restricts the **Install / change-theme action** at `storefront/templates/action/change/%`. Lower plans see HTTP 402 / redirect to the [[plan-features]] upsell when clicking Install — they CAN browse the catalogue but cannot switch the active theme until they upgrade. |

A separate orthogonal restriction applies to **paid themes** — each paid theme requires its own subscription independent of `change_theme`. The `unpaid-theme` middleware locks the rest of the admin until either the paid theme is paid for OR the merchant switches to a free theme. See [[design-themes-plan-gates]] + [[design-themes-unpaid-middleware]].

## Related

- [[design]] — parent Design pillar.
- [[nitrogen-vs-themes]] — a standard theme compared with a Nitrogen storefront.
- [[design-navigation]] — storefront menus (sibling).
- [[design-modules]] — storefront modules (sibling — many modules are theme-shipped).
- [[design-theme-editor]] — per-theme customisations (colours / fonts / images).
- [[design-custom-assets]] — per-theme custom CSS / JS.
- [[marketing-landing-pages]] — Static Pages (page-builder pages depend on theme-shipped blocks).
- [[details-billing]] — billing context for paid-theme purchases.
- [[subscriptions]] — current subscription view (paid themes appear as subscription items).
- [[plan-gates]] — plan-tier limits.

## Open questions

- 📡 **Per-plan paid-theme availability.** Plan-tier rules for paid themes live in [[plan-gates]]; some plans bundle paid themes, others require purchase. GraphQL-resolvable. See [[design-themes-plan-gates]]. (verify)
- 📡 **Trial-store paid-theme buying.** Trial stores see paid themes as buyable; the purchase flow is unblocked. GraphQL-resolvable. See [[design-themes-purchase]]. (verify)
