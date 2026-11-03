---
type: feature
nav_path: "Design → Modules → Content → Yotpo reviews"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Yotpo reviews module", "Yotpo module", "extra.yotpoReviews", "yotpoReviews", "Yotpo рейтинги", "Yotpo ревюта"]
tags: [design, modules, content, yotpo, reviews, app-dependent]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Yotpo reviews module (`extra.yotpoReviews`)

> Part of [[design-modules-content]]. See the category page for the other content modules.

## Purpose

The **Yotpo reviews** module surfaces Yotpo's review UI on the storefront — either a site-wide reviews carousel (showing all aggregated reviews from across the store) or a per-product reviews block (showing reviews tied to a single product). It is a thin proxy module — the actual review storage and review-collection workflows live in Yotpo's cloud; this module configures WHERE on the storefront the Yotpo blocks render.

The module has two surface modes:

1. **Legacy enable-only toggle** — a simple on / off toggle. Renders Yotpo's review block in the theme-defined slot (typically product pages + homepage).
2. **Page-builder block** with full configuration — picks site-wide vs per-product mode and (for per-product) which product to display.

Both modes are inert until the Yotpo app is installed and the merchant has entered their Yotpo App Key in [[apps-yotpo-settings]].

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → card **Yotpo reviews**.

The card appears ONLY when the Yotpo app is installed. The common instance name is `yotpoReviews`.

The richer page-builder variant is exposed when editing a Dynamic page in [[marketing-landing-pages]] — drop the **Yotpo reviews** block from the module palette.

## What the merchant can do here

In the legacy **Modules-screen** surface:

- Toggle the Yotpo block on / off.
- Save / Reset / Cancel.

In the **page-builder** surface (Dynamic pages):

- Pick **Reviews type** — site-wide reviews carousel OR per-product reviews block.
- For **per-product**, pick the specific product (autocomplete picker).
- Toggle the block on / off.
- Save / Reset / Cancel.

What the merchant CANNOT do here:

- Configure the Yotpo App Key or Secret — those live in [[apps-yotpo-settings]]. Without them the module is a no-op.
- Style the Yotpo review block — Yotpo renders its own iframe-style markup with Yotpo's own styling. CloudCart cannot override.
- Use the module to disable Yotpo for the WHOLE store — it only gates which storefront slots render the block. To fully disable Yotpo, uninstall the app or remove the API keys.

## Settings & fields

### Legacy module-screen surface

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | `bool` | on | Master on / off. When off, the theme's Yotpo slot renders empty. |

### Page-builder surface (richer)

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | `bool` | on | Master on / off. |
| `reviews` | select | `char:1,30` | empty | Mode — `for_site` for site-wide reviews carousel, or empty / per-product when `product_id` is set. |
| `product_id` | text | `char:0,30000` | empty | Product ID for the per-product reviews block. Required when `reviews ≠ for_site`. |

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists the toggle / mode; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme-shipped defaults (typically enabled with site-wide reviews) | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

## Business rules

### Yotpo app installation is REQUIRED

The module is a no-op unless the Yotpo app is installed. The render code checks the platform code first — if false, the module returns nothing. The card appears in the Modules screen only when Yotpo is installed.

### Yotpo App Key is REQUIRED

After installation, the merchant must enter their Yotpo App Key in [[apps-yotpo-settings]]. The render code reads the platform code — without it, the module returns nothing. Yotpo's own JS will not even attempt to load.

### Two render modes — site vs product

When `reviews=for_site`, the module renders Yotpo's site-wide reviews carousel template (`site-reviews`). When `reviews` is anything else and a `product_id` is set, the module renders Yotpo's per-product reviews template (`product-reviews`) for that product. If `product_id` is empty AND `reviews` is not `for_site`, the module renders nothing.

### Per-product mode loads product on render

The render code calls the platform code and passes the formatted product (with price + discounted price) into Yotpo's per-product template. A non-existent product silently renders nothing — there is no error to the merchant.

### Default settings inherit Yotpo app's `active` flag

When the module asks for its default settings, the platform reads the Yotpo app's `active` flag from the platform code — if the app is installed but marked inactive, the module defaults to `enabled=false`.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache key. The new setting is visible on the next storefront request.

### Reviews data lives in Yotpo's cloud

This module does NOT store reviews. Reviews are submitted to and stored by Yotpo. The module only triggers the Yotpo JS embed that pulls reviews live. For the review-collection emails, review moderation, and review responses, the merchant uses the Yotpo dashboard directly.

## Theme-specific notes

- **Theme-shipped slot.** The active theme decides WHERE the Yotpo block renders on the storefront. Common slots: product-detail pages (per-product reviews), homepage (site-wide reviews carousel), and the Reviews static page (site-wide).
- **Themes without Yotpo slots** ignore the module entirely — even when enabled, the block has nowhere to render.
- **Yotpo's UI is iframe-style.** Yotpo's JS injects its own DOM into the slot — the theme stylesheet has limited ability to restyle it. Star colours, fonts, and layout come from Yotpo's settings, not the theme.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[apps-yotpo-settings]] — Yotpo app settings (App Key / Secret + activation).
- [[apps-yotpot]] — Yotpo app overview (verify exact slug — possible typo in existing wiki).
- [[design-themes]] — theme picker; theme decides where the Yotpo block renders.
- [[marketing-landing-pages]] — Dynamic page builder; the richer Yotpo block lives there.

## Open questions

- 📡 **Yotpo app slug consistency.** The existing wiki has both `apps-yotpo-settings.md` and `apps-yotpot.md` — which is canonical. (verify) and possibly consolidate.
- 📡 **Per-product picker UX.** Whether the page-builder picker supports searching by SKU / name or only takes an ID. (verify) against the page-builder code.
- 📡 **Yotpo module instance + page-builder block in the same page.** Whether they coexist cleanly or compete for the same DOM mount point. (verify) by testing.
