---
type: feature
nav_path: "Apps → IMOS-3D"
route_name: apps.imos3d.overview
route_path: /admin/apps/imos3d
aliases: ["IMOS-3D", "IMOS 3D", "Imos furniture", "Furniture configurator", "enable disable button", "app active toggle"]
tags: [apps, administration, furniture, configurator, niche]
plan_gates: ["imos3d"]
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# IMOS-3D (furniture configurator)

## Purpose

**IMOS-3D** integration — connects the storefront to **IMOS**, a leading 3D furniture-design software used by furniture manufacturers + retailers. Lets customers configure furniture (kitchen cabinets, wardrobes, custom builds) using IMOS's 3D configurator, with the resulting design + bill-of-materials flowing back to the merchant's order.

Niche but powerful for the furniture-manufacturing segment.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it — a disabled app stops working while keeping its settings. The button is briefly absent while the screen is still loading its configuration; it appears once the settings arrive.

## Where to find it

Sidebar → Apps → install → **IMOS-3D**. See [[apps-imos3d-settings]] for configuration.

## What the merchant can do here

- Configure IMOS API credentials (apiKey + shop ID + country).
- Map CloudCart products to IMOS designs.
- Sync customer-configured designs back to CloudCart orders.

### What the merchant CANNOT do here
- Use without an IMOS subscription + connected IMOS instance.

## Settings & fields

Manager exposes:
- `appInfo` — App Store metadata.
- the configured check — checks 4 required settings: `imos3d.apiKey`, `imos3d.shop`, `imos3d.id`, `imos3d.country`.

## Business rules

### 4 required credentials

| Setting | Notes |
|---------|-------|
| `imos3d.apiKey` | IMOS API authentication. |
| `imos3d.shop` | The merchant's shop ID in IMOS. |
| `imos3d.id` | Integration ID for this specific CloudCart store. |
| `imos3d.country` | Country code (for currency / language). |

All four required for the configured check to return true.

### Per-order XML download

Per [[orders-details]] note: when a product has IMOS metadata, the merchant can download an XML file with the order's furniture-specific data (likely the bill-of-materials for manufacturing). Route: `imos3d.order.xml`.

This is the merchant's bridge from CloudCart order → IMOS production workflow.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `imos3d` | Access gate (install URL) | The install URL `/admin/apps/imos3d/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-imos3d-settings]] — settings sub-page.
- [[products-products]] — products with IMOS metadata.
- [[orders-details]] — order page exposes "Download IMOS XML" action when applicable.
- [[products-property]] — IMOS metadata stored as product properties (verify).

## How it works (verified against backend)

### Customer-side UX: embedded popup with IMOS configurator

When the customer visits `imos3d/{catalog}/{article}/{product_id}/{alabala?}` on the storefront, CloudCart renders an embedded popup with the IMOS 3D configurator. The popup carries:
- `catalog` — IMOS catalogue identifier.
- `article` — base article reference.
- `product_id` — CloudCart product ID for cart-linking.
- `clientSecret` + `session` — random tokens used by IMOS for callback identification.
- The merchant's `apiKey` + `shop` + `id` + `country` settings.

So the customer configures the furniture in-page (no redirect to IMOS). When done, IMOS POSTs the configured article back to CloudCart's `addToCart` endpoint.

### Cart-add flow creates a TEMPORARY product

When the customer confirms a configuration:
1. CloudCart creates a HIDDEN, TEMPORARY product with the configuration data — name from `articleName`/`realArticleName`, description from IMOS, price = IMOS-supplied price × 1.2 (20% markup), SKU = `realArticleName`.
2. If IMOS sent an image, it's uploaded to the product.
3. A cart item is created in the customer's cart referencing this temporary product, with quantity, full IMOS input stored as `imos3d` meta on the cart item.
4. The description is parsed (`key: value` pairs separated by commas) and each becomes a cart-item option.

The temporary product is created per-configuration — each customer's custom build becomes its own one-off product entry. This keeps customer-personalized configurations isolated.

### Pricing IS dynamic

The price stored is the IMOS-submitted price multiplied by 1.2 — IMOS calculates the configuration price dynamically (based on materials, dimensions, etc.) and submits it; CloudCart adds a 20% markup. The merchant doesn't control the price in CloudCart — IMOS's pricing engine is authoritative for the base price (with the markup applied automatically).

### Production handoff: merchant downloads XML

Via the `imos3d.order.xml` route (`/orders/imos3d/xml/{order_id}`): when an order contains IMOS-configured products, the merchant can download an XML file from the order's detail page. The XML includes:
- Order metadata (number, date, country code).
- Per-product: `Pname` (IMOS article name), `Count` (quantity), `PVarString` (configuration parameters), `ARTICLE_TEXT_INFO1`/`INFO2`/`INFO3` (descriptions), `INDFILE` (IMOS data file reference).
- Pricing: subtotal, shipping, VAT.

The XML is NOT auto-sent to a factory — the merchant downloads it manually and forwards to their production team (typically by uploading to their IMOS production workflow).

### Multi-IMOS instances: ONE per store

The settings hold ONE `apiKey` + `shop` + `id` per CloudCart store. A merchant running multiple stores must connect each store to one IMOS instance. Multiple IMOS shops per single CloudCart store is not supported in this integration.

### Frontend-only — app must be active

If the app is uninstalled or inactive, the storefront IMOS routes return 404. The merchant must activate the integration AND complete all 4 credentials before customers can use the configurator.

### Three IMOS meta keys persisted per product

When the merchant saves a product with IMOS data in the admin product editor, three specific keys are stored as product meta: `imos3d_catalog`, `imos3d_article`, `imos3d_ind`. The save listener fires only on the product save/update routes — direct DB writes wouldn't trigger this attachment.

### Cascade delete on product removal

When a CloudCart product is deleted, its IMOS-3D records (`product->imos3d`) are also deleted. So removing a product cleans up its IMOS association — no orphan IMOS records remain.

### No order-event listener

The IMOS integration does NOT subscribe to order events. There's no auto-sync of orders to IMOS — the merchant's production handoff is the manual XML download. IMOS doesn't receive a notification when an order is paid or shipped; the merchant is responsible for forwarding the XML to their production workflow.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
