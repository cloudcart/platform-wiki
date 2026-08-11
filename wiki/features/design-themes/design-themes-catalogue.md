---
type: feature
nav_path: "Design → Themes → Catalogue"
route_name: admin.templates.list
route_path: /admin/storefront/templates
aliases: ["Themes catalogue", "Theme listing", "Free vs paid themes", "Theme cards"]
tags: [design, themes, templates, catalogue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Themes — Catalogue listing

> Part of [[design-themes]]. See the hub for related aspects (install, purchase, unpaid-middleware, switch-effects, plan-gates, edge-cases).

## Purpose

The Themes screen's bottom section is a card catalogue of every theme CloudCart publishes — split into **Free** and **Paid** tabs. This aspect documents the listing query, the per-card classification (free / paid / already-purchased / coming-soon / new / in-dev), the badges, the sort order, and the screenshot / demo-URL plumbing.

## Where to find it

Sidebar → **Design** → **Themes** → bottom section (below the "current theme" panel). Route `/admin/storefront/templates`.

## What the merchant can do here

- See two tabs: **Free** and **Paid** (tabs are hidden if only one group is non-empty).
- See each theme as a card with a thumbnail screenshot, name, description (on hover), and a **Current** badge if it is the active theme.
- For each theme card, hover-state actions depend on its status:
  - **Coming soon** — dimmed thumbnail + "Coming Soon" ribbon; no action buttons.
  - **New** — "New" ribbon on the thumbnail.
  - **Active theme** — "Current" badge; no buy/install button.
  - **Free theme (or a paid theme the merchant has already purchased)** — **View** (opens demo URL in a new tab) + **Install** (see [[design-themes-install]]).
  - **Paid theme (not yet purchased)** — **View** + **Buy `<price>`** (opens the purchase page — see [[design-themes-purchase]]).

## Settings & fields

### Theme card status badges

| Badge | When shown | Visual |
|-------|-----------|--------|
| **Current** | The theme matches the site's active theme `mapping`. | Green check icon + "Current" caption below the card. |
| **New** | The theme has the `new` flag set. | Top-left "New" ribbon. |
| **Coming Soon** | The theme has the `coming_soon` flag set. | Top-right "Coming Soon" ribbon; thumbnail dimmed to 20% opacity; no action buttons. |

### Theme attributes (what each theme record carries)

| Attribute | Meaning |
|-----------|---------|
| `mapping` | Machine slug used in URLs and the site record (e.g., `nitrogen`, `pro`, `basic`). |
| `name` | Display name shown on the card. |
| `description` | Tooltip / detail text. |
| `demo_url` | Public URL where the theme can be previewed on CloudCart's demo store. |
| `price` | Price in the theme's currency. If `0` or `null`, the theme is **free**. If non-zero, it is **paid** and requires a subscription to install. |
| `currency` | The currency the theme's price is denominated in (e.g., `BGN`, `EUR`, `USD`). |
| `active` | Whether CloudCart has published the theme to the catalogue (`yes` / `no`). Inactive themes are not listed. |
| `coming_soon` | Whether the theme is shown as a preview-only "Coming Soon" card. |
| `new` | Whether the theme should display the "New" ribbon. |
| `in_dev` | Whether the theme is dev-only; non-dev users do not see it (an `in_dev` cookie can bypass this). |
| `has_demo` | Whether the demo-URL link is exposed on the card. |

### Free vs. paid — what `is_paid` actually means

A card displays as **free / already-installable** when its derived `is_paid` flag is `true`. That flag is `true` in two cases:

1. The theme's `price` is `null` or `0` — it is a free theme.
2. The theme has `price > 0` AND the site has an active paid subscription record for that theme's `mapping`.

Otherwise the card displays as **paid / needs to be bought** (and the install action silently redirects to the purchase flow — see [[design-themes-purchase]]).

## Business rules

### Catalogue listing query

The listing loads every theme where `active = 'yes'` OR `coming_soon = 1`, hides themes with `in_dev = 1` for non-dev users (unless the `in_dev` cookie is set), and sorts by [free → paid, non-coming-soon → coming-soon, new → not-new, id desc]. The listing then splits themes into two in-memory groups: `paid` (`price > 0`) and `free` (`price` null or `0`). These drive the **Free** / **Paid** tabs.

### Display order

Themes are sorted: **free first**, then **paid (descending price)**, with **coming-soon themes pushed to the end** of their respective groups, then **"new" themes brought to the top**, then by descending ID. This means the freshest free themes appear at the top of the Free tab; legacy themes are towards the bottom.

### Free / paid classification at render

Each theme card asks the derived `is_paid` flag whether to show **Install** or **Buy `<price>`**. `is_paid` is `true` when the theme is free OR when the merchant has an active site-subscription record matching the theme's mapping (`model_type = 'theme'` + `mapping = <theme-slug>` in `site_subscriptions`).

### Screenshots and demo URL

Theme screenshots are served from `sitecp/img/templates/<mapping>/desktop.png`, `mobile.png`, and `list.png` (the card thumbnail). If the thumbnail image is missing, the card falls back to a 1×1 transparent base64 placeholder with explicit dimensions. The demo URL is stored per-theme in the `demo_url` translatable attribute and opened in a new tab via the **View** action.

### Coming-soon and in-dev visibility

See [[design-themes-edge-cases]] for the visibility rules around `coming_soon` (listed in BOTH tabs as teasers) and `in_dev` (CloudCart-staff-only) themes, plus the slug-driven demo-URL fallback.

### Current-theme panel uses a separate query

The Themes page issues two separate queries: one for the catalogue (with the `coming_soon` / `in_dev` / sort logic), and one for the current theme — by joining the site's `template` slug to a theme's `mapping`. So the current-theme panel at the top is data-driven independently and continues to render even if the active theme has `active = no` (unpublished) or `coming_soon = 1`.

## Related

- [[design-themes]] — hub.
- [[design]] — parent Design pillar.

## Open questions

None.
