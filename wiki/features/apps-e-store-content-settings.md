---
type: feature
nav_path: "Apps → E-Store Content → Settings"
route_name: apps.e-store-content.settings
route_path: /admin/apps/e-store-content/settings
aliases: ["E-Store Content Settings", "EStore Content config"]
tags: [apps, administration, e-store-content, content-sync, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 1
---
# E-Store Content → Settings

## Purpose

The **Settings** tab is where the merchant configures **E-Store Content** API credentials, product-match key (typically EAN / SKU), and event subscriptions for content auto-pull. See [[apps-e-store-content]] for the full feature set.

## Where to find it

Sidebar → Apps → E-Store Content → **Settings tab**. Route: `/admin/apps/e-store-content/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **API Key / token** | Authentication against E-Store Content's API. |
| **API endpoint** | Service URL (may be configurable per region — verify). |

### Match key configuration

- **Match by** — EAN / GTIN / SKU / custom field.
- The key drives the `match(?Variant $variant)` method (per [[apps-e-store-content]]).

### Event subscriptions

Per [[apps-e-store-content]] `getEvents`:
- product.created — pull content for new products.
- product.updated — refresh content on product edits.
- (Verify other events.)

Each event toggle controls whether E-Store Content auto-pulls when that event fires.

### What the merchant CANNOT do here
- Use without an E-Store Content subscription.
- Override match logic per-product — match-key is store-wide.

## Settings & fields

Per [[apps-e-store-content]] Manager: the configured check validates credentials + match key + event subscriptions.

## Business rules

### Match key cascade

When the match key is EAN and a product has no EAN, E-Store Content cannot match — no content auto-pulled. The merchant either:
- Sets EAN on the product.
- Switches to a different match key.

### Auto-pull on event

When `product.created` is subscribed AND a new product is added in [[products-products]], the platform queues a content-pull job.

### Permission
Standard apps permission scope.

## Related

- [[apps-e-store-content]] — hub.
- [[apps-load-bee]] — sister content-provider integration.
- [[apps-flix-facts]] — sister event-driven integration.

### API endpoint — single global service URL

The integration loads E-Store Content's module from one fixed endpoint (`//delivery.estorecontent.com/static/rich_content.js`) for every merchant. There is no regional URL selector in the settings page — region selection (where it matters) is handled by E-Store Content's own delivery network and account configuration, not by CloudCart.

### Single locale per store — set via the `locale` setting

The module receives one `data-content-language` value. The merchant configures this once in Settings; there is no automatic per-storefront-language selection. On a multi-language store, all visitors see E-Store Content in the merchant's configured locale regardless of their session language.

### Conflict resolution — merchant content wins

E-Store Content is injected into the product description ONLY when the merchant has not written meaningful description text. If the merchant's description field has real content, the module is suppressed for that product. There is no overwrite mode and no manual-merge UI — to force E-Store Content to take over a product where the merchant previously typed text, the merchant must clear the description first.

### Three required settings: e_store, match.self, locale
The settings page persists exactly THREE keys: `e_store` (the shop ID from estorecontent.com), `match.self` (sku or barcode — what CloudCart sends as the lookup value), and `locale` (the content language). All three are required for the module to load. There is no separate "match by GTIN" field — the merchant chooses between SKU and barcode only.

### No 4th-field for API endpoint / region
The module always loads from the global `//delivery.estorecontent.com/static/rich_content.js` URL. There is no regional CDN selector; estorecontent.com handles region routing internally on their side based on the customer's IP.

## Open questions

All previously-flagged questions resolved. See body sections.
