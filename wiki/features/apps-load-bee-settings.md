---
type: feature
nav_path: "Apps → LoadBee → Settings"
route_name: apps.load_bee.settings
route_path: /admin/apps/load_bee/settings
aliases: ["LoadBee Settings", "Load Bee config"]
tags: [apps, administration, load-bee, content-sync, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-26
source_count: 1
---
# LoadBee → Settings

## Purpose

The **Settings** tab is where the merchant configures **LoadBee** API credentials, match key (EAN / SKU / custom), and event subscriptions for manufacturer-content auto-pull. See [[apps-load-bee]] for the full feature set.

## Where to find it

Sidebar → Apps → LoadBee → **Settings tab**. Route: `/admin/apps/load_bee/settings`.

## What the merchant can do here

### Credentials

| Field | Notes |
|---|---|
| **LoadBee API key** | Authentication. |
| **LoadBee partner ID** | Identifies which LoadBee partnership account is in use. |

### Match key

Per [[apps-load-bee]] `match(Variant)` method — the merchant configures which CloudCart field maps to LoadBee's content identifier (typically EAN / GTIN).

### Event subscription

Per [[apps-load-bee]] `getEvents`: subscribed events trigger content auto-pull. Common toggles:
- product.created — pull manufacturer content on new product.
- product.updated — refresh content on edits.

### What the merchant CANNOT do here
- Use without an active LoadBee subscription / partner-access.
- Override manufacturer content (LoadBee is the source of truth — merchant manually adds custom content if needed).

## Settings & fields

Per [[apps-load-bee]] Manager:
- the configured check — credential check.
- `getEvents` — event subscription list.
- `hasStatusChange` — boolean.
- `match(Variant)` — variant-level identifier mapping.

## Business rules

### Manufacturer-authoritative content

LoadBee provides content from manufacturers — high quality but the merchant doesn't control wording. When a product is mapped, LoadBee's content typically renders alongside (or replaces) the merchant's own description.

### Match key cascade

Products without an EAN / GTIN (or whichever match key is set) can't be mapped to LoadBee content — they simply don't get manufacturer content.

### Permission
Standard apps permission scope.

## Related

- [[apps-load-bee]] — hub.
- [[apps-e-store-content]] — sister content-provider integration.
- [[apps-flix-facts]] — sister event-driven integration.
- [[products-products]] — products receive LoadBee content.

### Manufacturer coverage is determined by LoadBee, not CloudCart

CloudCart only loads LoadBee's JavaScript module on the product page — the module itself queries LoadBee's CDN for content keyed by GTIN/EAN. Which manufacturers have content available depends entirely on the merchant's contract with loadbee.com. CloudCart does NOT maintain a partner list and cannot guarantee coverage for any particular brand; the merchant verifies coverage directly with LoadBee.

### Single locale per store — set via the `locale` setting

The module receives one `data-loadbee-locale` value passed through to LoadBee. The merchant configures this once in Settings — there is no automatic per-storefront-language selection. On a multi-language store, all visitors see LoadBee content in the merchant's configured locale regardless of their session language.

### Layout — appended AFTER the merchant's product description

LoadBee content is injected into the storefront product page by appending the module container (`loadbeeTabContent` div + the loadbee JS) to the end of the product's description on the product-details page. The merchant's own description text appears first; LoadBee's manufacturer content renders below it. The module then populates the container client-side from LoadBee's CDN.

### LoadBee renders only when the merchant left the description empty

The platform skips injection when the merchant has already written real description text — the merchant's text always wins. LoadBee fills the gap only when the description field is empty (or contains no meaningful text). To force LoadBee to take over a product page where the merchant previously typed text, the merchant must clear the description first.

### "Partner ID" field is actually the API key
The settings key on the platform's side is `load_bee` (the API key the merchant pastes from their LoadBee dashboard). This is passed as `data-loadbee-apikey` to the module. There is NO separate "Partner ID" field despite older UI labels suggesting it — the merchant supplies only the API key.

### LoadBee match key is via `match.self` (sku or barcode), passed as GTIN
The match key field accepts only TWO values: `sku` (default) or `barcode`. Whichever the merchant picks gets sent to LoadBee as the product's GTIN/EAN. There's no third option for the variant's MPN, EAN, or a custom field.

### Permission
Standard apps permission scope.

## Open questions

All previously-flagged questions resolved. See body sections.
