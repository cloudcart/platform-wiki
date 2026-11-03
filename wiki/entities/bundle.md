---
type: entity
nav_path: "Entity → Bundle"
aliases: ["Bundle", "Product bundle", "Bundle product", "Combo", "Kit", "Subscription box", "Бундъл", "Комплект", "Пакет"]
tags: [entity, catalog, products, bundles, cross-sell]
created: 2026-05-24
updated: 2026-06-10
source_count: 1
---

# Bundle

## Identity

A **Bundle** is a special type of [[product|Product]] that groups multiple **constituent products** together and sells them at a single bundled price — typically discounted compared to the sum of the component prices ("Camera + Lens + Tripod = 999 BGN", "Beginner skateboarding kit = board + helmet + pads", "Subscription box: 3 curated coffees"). The merchant defines a Bundle in [[bundles-list]] (Sidebar → Products → Bundles) by giving it a name, an image, a price, and a list of component products with their quantities. The platform creates a parent Product record with `type = 'bundle'` that has its own storefront listing page, its own image gallery, its own SEO settings, and its own price — but whose **stock and availability** are derived from the constituents rather than tracked independently.

When a customer buys a Bundle, the checkout decrements EACH constituent product's stock (not a separate "bundle stock" counter). Buying one "Camera + Lens + Tripod" bundle decrements 1 camera + 1 lens + 1 tripod. The Bundle's availability is the **lowest available quantity** across all components — if ANY constituent is out of stock (and "Continue selling" is off on that component), the Bundle becomes unavailable on the storefront. Bundles are therefore a sales-presentation layer on top of existing catalogue products, not a separate SKU type with its own warehouse counter.

Bundles are managed by the **Bundles app**, installed from the [[apps|App Store]] under the `bundles` app-key. The Bundle count is plan-gated under a dedicated `bundles` plan-feature key — **NOT** counted against the `products` cap — so the merchant can build many Bundles without burning their product quota.

A Bundle is distinct from:

- A regular [[product|Product]] with [[variant|Variants]] — variants are different SKUs of the SAME product (size, colour); Bundles are different products sold together.
- A [[discount|Discount]] that gives "buy X get Y free" — discounts apply at checkout based on cart rules; Bundles are pre-built combinations the customer adds to cart as a single line.
- A **Smart Collection** ([[products-smart-collections]]) — collections are merchandising groupings for navigation / filtering, not purchasable units.
- A **cross-sell** recommendation — cross-sells suggest related products as separate cart additions; a Bundle is one cart line with components inside it.

## Aliases

- **Bundle** / **Product bundle** / **Bundle product** — canonical merchant-facing terms in the admin UI and on the storefront.
- **Combo** — informal phrasing ("camera combo", "starter combo").
- **Kit** — used by merchants whose Bundles are gear sets ("beginner skateboarding kit").
- **Subscription box** — used when the Bundle is curated content sold as a recurring product.
- **Бундъл** / **Комплект** / **Пакет** — Bulgarian labels used interchangeably in the BG admin.

## Key Attributes

The Bundle is a multi-faceted entity split across **six well-scoped aspects**. The Assistant should drill into the aspect that matches the question, not read every page.

- [[bundle-entity-attributes]] — the merchant-controlled fields (name, image, components, bundled price, description, SEO, `is_active`) + the per-pivot column shape (`product_id`, `qty`, `sort_order`, the override flags).
- [[bundle-entity-relationships]] — has-many components, is-itself-a Product, file-asset gallery, category assignment, indirect Variant references, special Bundle cart-item type, and what a Bundle does NOT do (no per-group pricing, no auto-generation).
- [[bundle-entity-lifecycle]] — the six merchant-controlled states (Draft → Active → derived Out-of-stock → Auto-deactivated → Inactive → Deleted), the asymmetric one-way deactivation cascade, and what happens to carts on delete.
- [[bundle-entity-component-overrides]] — the rich per-row overrides each constituent supports (`optional`, `individual_price_enabled`, `override_title`, `hide_thumb`, the three visibility scopes), plus the flat-headline-price gotcha around `optional`.
- [[bundle-entity-stock-and-activation]] — derived availability (`min(qty / inclusion)` across constituents), per-constituent decrement on checkout, auto-deactivation cascade on constituent save, the active-scope SQL counting `active AND non-draft` constituents, and the dangling-component edge case after constituent deletion.
- [[bundle-entity-app-and-storefront]] — Bundles app install / uninstall behaviour, the dedicated `bundles` plan gate (separate from `products`), storefront URL + landing page, store-wide defaults on [[apps-bundles-settings-new]], no per-Bundle analytics dashboard, no per-group pricing, no CSV import / auto-generation.

## Where it appears

- [[bundles-list]] — the master list view. Search, paginate, add, edit, delete, activate / deactivate.
- [[apps-bundles-overview-new]] — Bundles app hub (modern Vue). Install state + CTA to the list.
- [[apps-bundles-settings-new]] — store-wide Bundle defaults (savings display, stock model, label localisation).
- [[apps]] — App Store entry point for installing the Bundles app.
- [[products-products]] — Bundles also appear in the master product list because they're Products with `type='bundle'` (some filters explicitly exclude them; verify per-screen).
- [[cart]] — Bundles appear as a special cart-item type with components nested inside the line.
- [[orders]] — Bundle purchases appear as one order line; [[orders-ordered-products]] expands the constituent breakdown.
- [[analytics-top-order-bundles-by-sales]] — analytics dashboard showing top Bundles by sales revenue.
- [[analytics-top-bundles-by-traffic]] — analytics dashboard showing top Bundles by storefront traffic.

## Related

### Related entities

- [[product]] — each Bundle is itself a Product record; constituents are also Products.
- [[variant]] — constituents with variants reference specific variants in the Bundle pivot.
- [[category]] — Bundles can be categorised like any product.
- [[file-asset]] — Bundle image + gallery.
- [[cart]] — Bundles appear as a Bundle cart-item type; deletion cleans up cart entries.
- [[order]] — Bundle purchases decrement each constituent's stock and snapshot the Bundle as the parent SKU.
- [[discount]] — alternative way to give "buy X get Y discount" without creating a Bundle (cart-level rule vs. pre-built Bundle).

### Cross-cutting concepts

- [[inventory-tracking]] — Bundle availability derives from constituent stock; "Continue selling" on constituents drives Bundle behaviour.
- [[inventory-bundle-stock]] — the canonical inventory-side aspect for bundle stock derivation (min-across-children + child-flag-wins).
- [[plan-gates]] — `bundles` plan-feature key, separate from `products`.
- [[checkout-flow]] — Bundle cart-items decrement each constituent at order placement.

### Settings & feature pages

- [[bundles-list]] — primary admin screen.
- [[apps-bundles-overview-new]] — modern Vue overview hub.
- [[apps-bundles-settings-new]] — store-wide defaults.
- [[apps]] — App Store (Bundles app must be installed).

## Open Questions

- ⏸️ The exact behaviour of the "Strict" vs "Partial" stock model in [[apps-bundles-settings-new]] — no dedicated `bundles_stock_model` setting was found in the platform source. The two-mode UI may reflect a planned-but-not-yet-shipped feature, or the toggle may proxy a different underlying field.
