---
type: feature
nav_path: "Apps → LoadBee"
route_name: apps.load_bee.overview
route_path: /admin/apps/load_bee
aliases: ["LoadBee", "Load Bee", "Product content enrichment", "enable disable button", "app active toggle"]
tags: [apps, administration, content, manufacturer-feed, sync]
plan_gates: ["load_bee"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# LoadBee (product content enrichment)

## Purpose

**LoadBee** integration — pulls **rich manufacturer content** (premium product descriptions, brochures, comparison sheets, videos, lifestyle imagery) directly into the merchant's product pages. LoadBee is a content-syndication service partnered with manufacturers; the merchant subscribes and gets automatic content updates whenever the manufacturer publishes new material.

Used by merchants who sell brand-name products and want professional-quality product pages without manually creating content for each SKU.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it — a disabled app stops working while keeping its settings. The button is briefly absent while the screen is still loading its configuration; it appears once the settings arrive.

## Where to find it

Sidebar → Apps → install → **LoadBee**. See [[apps-load-bee-settings]] for configuration.

## What the merchant can do here

- Configure LoadBee account credentials.
- Map CloudCart products to LoadBee content (typically by EAN / GTIN).
- Activate content auto-sync on product changes.

### What the merchant CANNOT do here
- Use without a LoadBee subscription + permitted manufacturer access.

## Settings & fields

Manager exposes:
- `match(Variant $variant)` — maps a CloudCart variant to LoadBee's content identifier.
- `getEvents` — subscribed event types.
- `hasStatusChange` — boolean.
- the configured check — credential validity.

Event-driven pattern matches other content / ERP apps.

## Business rules

### Manufacturer-provided content

LoadBee content comes from manufacturers (Bosch, Samsung, etc.) — high quality but the merchant doesn't control wording. The merchant's own description (if set) typically renders ABOVE the LoadBee block (verify the layout).

### Variant-level matching

LoadBee maps to specific variants (not just product). When a variant has its own LoadBee content (e.g., model-specific brochure), it renders.

### Event-driven sync

When a product is created / updated, the platform pulls fresh LoadBee content if available.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `load_bee` | Access gate (install URL) | The install URL `/admin/apps/load_bee/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-load-bee-settings]] — settings sub-page.
- [[apps-e-store-content]] — similar content-sync pattern.
- [[apps-flix-facts]] — similar event-driven integration.
- [[products-products]] — products receive LoadBee blocks.

## How it works (verified against backend)

### Provider: loadbee.com (third-party rich-content module)

LoadBee is the SaaS service **loadbee.com**. CloudCart's integration loads loadbee's `loadbee_integration.js` module from `https://cdn.loadbee.com/js/loadbee_integration.js` on the product-details page. The module connects to loadbee.com and renders manufacturer-provided content (rich descriptions, lifestyle imagery, videos, comparison sheets) inline.

There is **no server-side data sync**. The module runs in the customer's browser; nothing is rewritten in CloudCart's product database. Manufacturer coverage and pricing are arranged directly with loadbee.com — CloudCart provides only the integration plumbing.

### Match key: SKU or barcode, sent as EAN/GTIN

The `match.self` setting picks how products are looked up against loadbee.com's content catalog:

- `sku` (default) — sends the variant's SKU as the `data-loadbee-gtin`.
- `barcode` — sends the variant's barcode as the `data-loadbee-gtin`.

The match type is hard-coded to `ean` (`data-loadbee-gtintype="ean"`). Products without a matching GTIN in loadbee's database render nothing.

### Required settings

The app needs all three of `load_bee` (the merchant's **API key** registered with loadbee.com — passed as `data-loadbee-apikey`), `match.self` (sku or barcode), and `locale` (the content language). All three are required for the module to load.

### Vendor required on every product

Unlike [[apps-e-store-content]], LoadBee skips products that have **no vendor assigned**. The platform's check is *"if the product has a vendor and the merchant has a LoadBee API key and the page does not already contain the module…"* Then the module loads. So when the merchant installs LoadBee, every product they want covered must have a [[products-vendors]] entry — naked products bypass the module.

### When the module renders

On the product details page, the LoadBee integration runs after the product view event:

1. Exits if not in the `site` namespace.
2. Loads the module only when the product has a vendor, the merchant's API key is set, and the page does not already contain `loadbeeApiKey=` (idempotency check).
3. Requires the merchant has **not** written a substantive description (`hasText` check). Pages where the merchant wrote their own copy are left alone.
4. Appends an HTML snippet at the end of the description that creates a `<div class="loadbeeTabContent">` with the merchant's API key + product GTIN + locale, plus the async script tag.

The loadbee module then renders the manufacturer's content inside that div.

### Layout: end of the description

The module is appended **at the end of the existing description field**. So if the merchant has a short intro line, the loadbee content renders below it.

### Multi-language

The `locale` setting tells loadbee which language version of the manufacturer's content to fetch. Set it to the storefront's primary content language. The module always loads in the configured locale — there is no per-language switching when the customer changes the storefront language.

### Mixed merchant + LoadBee content

The integration is **gated** on the merchant's own description being empty (`hasText` guard). The merchant cannot have their description AND the loadbee block visible at the same time on the same product. Practically, merchants on LoadBee tend to leave the description empty so the manufacturer's syndicated content shows.

### Cost model

CloudCart does not charge per product for the integration — pricing depends on the merchant's contract with loadbee.com. Without a valid API key the integration is inactive.

### GTIN type is hard-coded as "ean"
The module always passes `data-loadbee-gtintype="ean"` regardless of whether the merchant's `match.self` is SKU or barcode. So loadbee always treats the supplied value as an EAN — products with non-EAN SKUs may not match against loadbee's catalog even when match.self is correctly configured. The merchant should ensure their SKU / barcode values are valid EANs / GTINs (which industry-standard manufacturers usually are).

### Idempotency guard: `loadbeeApiKey=` string
The platform checks the description for the string `loadbeeApiKey=` before injection. If already present, the module is not duplicated. So a merchant who has manually pasted a LoadBee snippet into a description will see the auto-injection skip — they control whether their custom snippet OR the auto-injection is used.

### Same module pattern as E-Store Content and FlixFacts
LoadBee, [[apps-e-store-content]] and [[apps-flix-facts]] all use the same "manufacturer-content module" architecture: a single API key/Distributor ID + a match-key (sku or barcode) + a locale, with a `hasText` guard preventing overwrite of the merchant's own description and an idempotency string check that prevents double-injection. The three apps can be installed concurrently; the merchant typically picks one based on which content provider their brands work with.

## Open questions

