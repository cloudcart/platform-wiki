---
type: entity
nav_path: "Entity → Bundle → App and storefront"
aliases: ["Bundle app", "Bundles app install", "Bundle plan gate", "Bundle storefront URL", "Bundle settings new", "Bundle no analytics dashboard", "Bundle no per-group pricing", "Bundle no auto generation", "Bundle no CSV import"]
tags: [entity, catalog, products, bundles, app, storefront]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[bundle]]. See the hub for the other aspects (attributes, relationships, lifecycle, component overrides, stock + activation).

# Bundle — App and storefront

## Identity

Everything outside the per-Bundle editor and the per-constituent overrides: how the Bundles app gets installed, the dedicated `bundles` plan gate that's separate from `products`, the Bundle's own storefront URL and landing page, the store-wide defaults on [[apps-bundles-settings-new]], and the explicit non-features (no per-Bundle analytics dashboard, no per-customer-group pricing, no CSV import, no auto-generation).

This aspect is the "shape of the Bundles feature in the platform" view, distinct from the per-Bundle attribute / lifecycle / stock behaviour covered in the other sub-pages.

## Aliases

- **Bundles app** — the installable feature from the App Store.
- **`bundles` plan-feature key** — the plan-gate identifier.
- **Bundle landing page** — the storefront product-detail page for a Bundle.
- **Store-wide Bundle defaults** — the cluster of fallback settings on [[apps-bundles-settings-new]].

## Key Attributes

### Bundles app must be installed first

The Bundles app must be installed from [[apps]] before the Bundles section appears in the sidebar. Installation creates the necessary tables and registers the routes. The app ships an empty list (no preloaded sample bundles, no tutorial overlay); the merchant builds each Bundle manually via the **+ Create bundle** CTA.

Uninstalling the app does NOT auto-delete existing Bundles — it only hides the admin screens. If the merchant reinstalls later, all Bundles reappear intact. So uninstall is a "hide the feature" action, not a "wipe the data" action.

### Plan gate: separate `bundles` feature, not counted against `products`

The Bundle count is gated by a dedicated `bundles` plan-feature key — independent from the `products` cap that limits regular product count. So a merchant on a plan with 500 products and 10 Bundles can have BOTH 500 regular products AND 10 Bundles; the Bundles don't burn against the product quota even though each Bundle is technically a Product record.

This is a deliberate plan-design choice — Bundles are merchandising packaging, not separate SKUs. See [[plan-gates]] for the full plan-feature key catalogue.

Note: while the `bundles` plan cap limits how many Bundles the merchant can create, Bundles **DO** still count toward other catalogue plan gates downstream (XML-sync row caps, category-listing scans, the search index indexing) — see [[bundle-entity-stock-and-activation]] for the rationale.

### Storefront landing page + URL

Bundles get their own storefront URL (driven by the SEO URL handle), just like regular products. Customers can browse Bundles directly via category navigation, search results, or product-page cross-links. The Bundle page shows:

- The bundled price (and, if configured, the per-component sum + "savings vs individual" calculation).
- The list of components (filtered by the per-component `visible_product_details` and `price_visible_product_details` toggles — see [[bundle-entity-component-overrides]]).
- The main image + gallery (inherited from the Bundle's Product record).
- The description and any custom-field content the merchant has filled in.

The Bundle page is rendered by the same storefront product-detail route as regular products — the `type = 'bundle'` discriminator switches in the constituent list and the "savings" calculation, but the surrounding chrome (related products, reviews, breadcrumbs) is the same.

### Store-wide Bundle defaults live in `apps-bundles-settings-new`

[[apps-bundles-settings-new]] holds store-wide defaults that apply to ALL Bundles:

- **Show savings on the Bundle page** — display the calculated discount vs the per-component sum.
- **Show constituent prices** — display each component's individual price next to the Bundle headline.
- **Stock model** — "Strict" vs "Partial" toggle (the underlying semantics here are not fully documented in the platform source — see Open Questions).
- **Customer-facing label localisation** — the strings shown on the storefront ("Bundle includes", "You save", "Optional").

Individual Bundles can override some display behaviours via the per-component visibility toggles (see [[bundle-entity-component-overrides]]), but the global defaults apply when no per-row override is set. When a per-row override IS set, the per-row value wins against the global default — this is why a merchant who flips a store-wide toggle and sees only SOME Bundles change is not seeing a bug.

### Bundles bypass per-customer-group pricing

A Bundle has a single price for all customers. Per-customer-group pricing (loyalty tier discounts) does NOT apply to the Bundle's bundled price — the merchant cannot configure "VIP customers get this Bundle at 800 BGN, regular customers at 999 BGN". To approximate per-group pricing, the merchant creates separate Bundles or uses a [[discount|Discount]] targeted at the customer group.

This is a deliberate simplification — the Bundle's value proposition is the headline price; introducing per-group variation would multiply the merchandising surface unmanageably. Merchants who need per-group Bundle pricing should expect to maintain N parallel Bundles.

### No automatic Bundle generation

The platform does NOT analyse "frequently bought together" or "cross-sell patterns" to auto-suggest Bundles. The merchant builds every Bundle manually based on their own merchandising knowledge. There is also no "import Bundles from CSV" flow — Bundle creation is per-Bundle in the editor.

This makes Bundles a high-touch feature: every Bundle is a curated merchandising decision. Merchants with large catalogues sometimes ask for an auto-suggest workflow or a CSV importer; neither exists today.

### No per-Bundle sales dashboard

[[apps-bundles-overview-new]] is a hub page (install state + CTA to the list). It does NOT show per-Bundle revenue, units sold, conversion rates, or any other sales metrics. Per-Bundle sales data lives elsewhere:

- General [[analytics]] — filtered by the Bundle product (Bundles are Products with `type = 'bundle'`, so they appear in the standard analytics).
- [[orders]] — filtered by the Bundle SKU.
- [[analytics-top-order-bundles-by-sales]] — dedicated dashboard for top Bundles by sales revenue.
- [[analytics-top-bundles-by-traffic]] — dedicated dashboard for top Bundles by storefront traffic.

The Bundles app itself does NOT register its own analytics dashboard. The two dashboards above live under the general analytics section and surface Bundle-specific cuts of the underlying product analytics.

## Where it appears

- [[apps]] — App Store install entry point.
- [[apps-bundles-overview-new]] — install-state hub (modern Vue).
- [[apps-bundles-settings-new]] — store-wide defaults.
- [[bundles-list]] — day-to-day Bundle management.
- [[analytics-top-order-bundles-by-sales]] / [[analytics-top-bundles-by-traffic]] — dedicated analytics cuts.
- Storefront product-detail route — renders the Bundle landing page using the same route as regular products.

## Related

- [[bundle]] — hub.
- [[apps]] — App Store entry point.
- [[apps-bundles-overview-new]] — modern Vue overview hub.
- [[apps-bundles-settings-new]] — store-wide defaults.
- [[bundles-list]] — primary admin list.
- [[plan-gates]] — `bundles` plan-feature key, separate from `products`.
- [[analytics-top-order-bundles-by-sales]] / [[analytics-top-bundles-by-traffic]] — analytics dashboards.
- [[bundle-entity-component-overrides]] — per-row overrides that win against store-wide defaults.
- [[bundle-entity-stock-and-activation]] — Bundles count toward other catalogue plan gates downstream.

## Open Questions

- ⏸️ The exact behaviour of the "Strict" vs "Partial" stock model in [[apps-bundles-settings-new]] — no dedicated `bundles_stock_model` setting was found in the platform source. The two-mode UI may reflect a planned-but-not-yet-shipped feature, or the toggle may proxy a different underlying field.
