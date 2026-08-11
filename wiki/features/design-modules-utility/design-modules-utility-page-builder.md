---
type: feature
nav_path: "Design → Modules → Utility → Page-builder blocks"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Page builder utility modules", "Code module", "Store locations module", "Yotpo reviews block", "Brand model module", "Order details module", "Модул код", "Модул магазини"]
tags: [design, modules, storefront-customisation, page-builder]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Utility modules — Page-builder blocks

> Part of [[design-modules-utility]]. See the hub for the catalogue, editable modules, system modules, and storage / cache mechanics.

## Purpose

These modules do NOT appear on the Modules screen — they only exist inside the Dynamic page builder in [[marketing-landing-pages]]. The merchant adds them as blocks on a specific Dynamic page and configures them per-page. Five blocks fall into this group: `code`, `store_locations`, `yotpo-reviews`, `brand-model`, and `order-details`.

## Where to find it

Sidebar → **Marketing** → **Landing pages** → open a Dynamic page → click **Add block** → pick the module from the block picker. Availability depends on which apps are installed (see Business rules).

## What the merchant can do here

- Drop any of these blocks into a Dynamic page.
- Configure the block's fields in the page builder side panel.
- Reorder and remove blocks freely on the page.
- Multiple instances of the SAME block can live on the same page — each carries its own settings.

The Page Builder URL itself is gated by the `storefront_builder` plan feature. Lower plans are redirected to the upsell.

## Settings & fields

All five blocks are page-builder only and theme-agnostic (page-builder doesn't depend on the active theme). Each carries an `enabled` master toggle.

### `code` — Raw HTML/JS embed

Renders an arbitrary HTML / JavaScript snippet. Used for third-party embeds (chat, marketing pixels, custom forms, videos), A/B test code, or promo banners not covered by standard modules.

| Field | Type | Validation |
|-------|------|------------|
| `enabled` | toggle | — |
| `code` | textarea (rows: 6) | char:1-3,000,000 — up to 3 million characters of raw HTML / JS |

No input validation beyond the character limit — the merchant is responsible for valid HTML / JS. The snippet runs in an isolated `<iframe srcdoc>` (see Business rules), so DON'T paste analytics tags (Google Analytics, Facebook Pixel) here — those belong in the page `<head>`. For HTML / JS / CSS on EVERY page (not one landing page) or for scripts needing parent-DOM access, use [[design-custom-assets]] instead.

---

### `store_locations` — Stores list

Renders the store's physical locations pulled from the Store Locations app ([[apps-store-locations]]) — each location's name, address, hours, contact info, theme-controlled layout. Available only when that app is installed; otherwise the block shows a placeholder *"Application 'Store location' is not installed"* with an install link.

| Field | Type | Notes |
|-------|------|-------|
| `enabled` | toggle | Master on/off |
| `title` | text | Optional heading above the list (e.g. "Find a store" / "Намери магазин") |

Locations themselves are added/edited in [[apps-store-locations]] — this block only RENDERS the list. Best paired with the Google Map module on a "Contact / Find us" page.

---

### `yotpo-reviews` — Yotpo reviews

A page-builder variant of the Yotpo Reviews integration with finer controls than the legacy storefront module (`yotpoReviews`, see [[design-modules-utility-editable]]). Available when the Yotpo integration is installed ([[apps-yotpo-settings]]).

| Field | Type | Notes |
|-------|------|-------|
| `enabled` | toggle | Master on/off |
| `reviews` | select | **for_site** (overall site reviews) or **for_product** (a specific product's reviews) |
| `product_id` | autocomplete (shown only when `reviews=for_product`) | Product whose reviews to show — searches by name/SKU |

Use **for_site** on a Trust / Testimonials page, **for_product** when promoting one product. Yotpo API keys are configured ONCE in [[apps-yotpo-settings]] and apply to all Yotpo modules on all pages.

---

### `brand-model` — Vehicle / device compatibility picker

A specialised block for stores selling parts / accessories needing brand + model compatibility (car parts, phone cases, printer cartridges). Renders a "Pick your brand → pick your model" filter that takes the customer to a category page filtered to that brand+model. Requires the [[brand-model]] app.

| Field | Type | Notes |
|-------|------|-------|
| `enabled` | toggle | Master on/off |
| `categories` | select — **yes** / **no** | **yes** adds a category-level filter (brand + model + category); **no** is just brand + model |

The brand + model catalogue is managed in [[brand-model-brand]] and [[brand-model-model]] — this block only RENDERS the picker. Use **categories: yes** when the store sells parts across multiple categories per model (a phone case vs a screen protector for the same phone).

---

### `order-details` — Order receipt

Renders the customer's order details (products, prices, shipping, billing) on a custom thank-you / order-confirmation page, replacing the default layout with a fully merchant-controlled one.

| Field | Type | Notes |
|-------|------|-------|
| `enabled` | toggle | Master on/off |

That is the entire form — the block pulls order data from the current customer's most recent order; no further configuration is possible. It only renders in a post-purchase context (a thank-you page with an active order); on any other page it shows empty data. The standard order-confirmation email + page still use the platform's built-in layout — `order-details` is only for CUSTOM thank-you pages in [[marketing-landing-pages]]. Combine with `product-showcase` (cross-sell) and `code` (conversion pixel) for a complete post-purchase page.

## Business rules

### App-gated registration

The page-builder keeps its own block registry, separate from the Modules screen. A block is only LOADED into the picker if its required app is installed at that moment:

| Block | Required app |
|-------|--------------|
| `code` | none (always available) |
| `store_locations` | Store Locations (`store_locations`) |
| `yotpo-reviews` | Yotpo (`yotpo`) |
| `brand-model` | Brand-Model (`brand_model`) |
| `order-details` | none |

If the app isn't installed, the block is **absent** from the picker — not just disabled. Installing the app re-enables it without further configuration.

### Page Builder access gate

The Page Builder URL is gated by the `storefront_builder` plan feature. Stores on lower plans see the upsell when they try to open the per-page builder. Once inside, all blocks here are universally available — none have an additional paid gate.

### Per-instance configuration

Each block instance lives on a specific Dynamic page; settings are stored per-block-per-page, not globally. Two `code` instances on the same page each carry their own snippet; two `yotpo-reviews` instances can target different products.

### `code` runs in an isolated iframe

The `code` block renders inside an `<iframe srcdoc>` with auto-height adjustment. Scripts run isolated and **cannot reach the parent DOM** unless they use `postMessage`. For globally-scoped scripts needing DOM access, use [[design-custom-assets]] instead.

## Related

- [[design-modules-utility]] — hub.
- [[design-modules-utility-catalogue]] — full module list.
- [[design-modules-utility-editable]] — `yotpoReviews` legacy storefront module contrast.
- [[design-modules-utility-storage]] — page-builder registry vs Modules-screen registry.
- [[marketing-landing-pages]] — Dynamic pages host these blocks.
- [[design-custom-assets]] — global HTML / JS / CSS injection (alternative to `code`).
- [[apps-yotpo-settings]] — Yotpo integration (gates `yotpo-reviews`).
- [[apps-store-locations]] — Store Locations app (gates `store_locations`).
- [[brand-model]] — Brand-Model app (gates `brand-model`).

## Open questions

- 📡 **`yotpoReviews` legacy vs page-builder.** Both surfaces share the same Yotpo API key configured in the Yotpo app — no separate setup for the page-builder module. GraphQL-resolvable: query whether the Yotpo app is installed and configured on this merchant's store.
- 📡 **Page-builder `store_locations` data source.** Always shows ALL active store locations — no per-block filter override. GraphQL-resolvable: query the merchant's active store locations.
