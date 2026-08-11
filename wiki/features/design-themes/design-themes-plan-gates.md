---
type: feature
nav_path: "Design → Themes → Plan gates & permissions"
route_name: admin.templates.list
route_path: /admin/storefront/templates
aliases: ["change_theme plan-feature", "Theme plan gate", "Theme permission", "store.templates permission"]
tags: [design, themes, templates, plan-gates, permissions]
plan_gates: ["change_theme"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Themes — Plan gates & permissions

> Part of [[design-themes]]. See the hub for related aspects (catalogue, install, purchase, unpaid-middleware, switch-effects, edge-cases).

## Purpose

This aspect documents the two access layers that gate the Themes screen:

1. **Staff permission** (`store` + `store.templates`) — controls whether the merchant's user role can reach the screen at all.
2. **Plan-feature gate** (`change_theme`) — controls whether the merchant's plan allows the **Install / change-theme action**.

Plus the orthogonal **paid-theme subscription** requirement that applies regardless of the plan-feature.

## Where to find it

The gates run wherever the merchant tries to:

- Click **Themes** in the Design sidebar (permission check).
- Click **Install** on a theme card at `/admin/storefront/templates/change/{mapping}` (plan-feature check).

## What the merchant can do here

If the merchant has the right permission + plan-feature, they can install any free or already-purchased theme — see [[design-themes-install]].

Even on lower plans, the merchant CAN browse the catalogue (the read-only Themes screen is not gated by `change_theme`). The current theme keeps rendering on the storefront regardless of the gate.

## What the merchant cannot do here

- Cannot reach the Themes screen at all without the `store` and `store.templates` permission keys on their staff role.
- Cannot click **Install** to switch the active theme without the `change_theme` plan-feature.
- Cannot install a paid theme they have not purchased — regardless of plan-feature (this is an orthogonal subscription requirement).

## Settings & fields

### Plan-feature key

| Mapping | Shape | What it controls |
|---|---|---|
| `change_theme` | Access gate | Path-restricts the **Install / change-theme action** at `storefront/templates/action/change/%`. Lower plans see HTTP 402 / redirect to the [[plan-features]] upsell when clicking Install on a theme card — they CAN browse the catalogue but cannot switch the active theme until they upgrade. The current theme keeps rendering on the storefront regardless of the gate. |

### Permission keys

| Key | What it controls |
|---|---|
| `store` | Top-level Design dropdown visibility. |
| `store.templates` | Themes screen access. |

A staff role with neither key sees **no Themes link** in the Design dropdown and cannot reach the screen directly.

## Business rules

### Plan-feature `change_theme` behaviour

- **Access-shaped (boolean)** — either the merchant's plan stack grants it or doesn't.
- **Gates the install path only** — `storefront/templates/action/change/%`. The catalogue listing, current-theme panel, and purchase pages are NOT gated by `change_theme`.
- **Upsell behaviour** — lower plans get redirected to the per-feature upsell at [[plan-features]] or to a plan-upgrade panel.
- See [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] for the plan-feature mechanism in general.

### Paid-theme subscription is orthogonal to `change_theme`

A separate orthogonal restriction applies to **paid themes**: each paid theme is its own subscription (`model_type='theme'`, `mapping=<theme-slug>` in `site_subscriptions`). The theme must be purchased — independently of the `change_theme` plan-feature — before it can be installed.

Even with `change_theme` granted, the merchant still needs to either:

- Choose a free theme, OR
- Purchase the paid theme via the purchase flow — see [[design-themes-purchase]].

### Unpaid-theme middleware enforces payment regardless of plan-feature

If the site has the `unpaid_template` flag set, the merchant is locked out of the admin until they pay or switch to a free theme — independent of the `change_theme` plan-feature. See [[design-themes-unpaid-middleware]].

### Permission key gates the entire screen

A staff role missing both `store` and `store.templates` cannot reach the Themes screen at all — the link does not render in the sidebar, and direct URL navigation is blocked.

## Related

- [[design-themes]] — hub.
- [[plan-gates]] — plan-tier limits in general.
- [[plan-vs-feature-pack]] — distinction between plan-features and feature-packs.
- [[plan-features]] — the per-feature upsell page that lower plans land on.
- [[design-themes-install]] — the install action the gate restricts.
- [[design-themes-purchase]] — the paid-theme subscription side.
- [[design-themes-unpaid-middleware]] — the parallel payment-enforcement lock.
- [[subscriptions]] — current subscription view (paid themes appear as subscription items).

## Open questions

- 📡 **Per-plan paid-theme availability.** Plan-tier rules for paid themes live in [[plan-gates]]; some plans bundle paid themes, others require purchase. GraphQL-resolvable: query the merchant's current plan + feature-pack stacks to determine which paid themes are bundled vs require purchase. (verify)
