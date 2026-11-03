---
type: feature
nav_path: "Apps → E-Store Content"
route_name: apps.e-store-content.overview
route_path: /admin/apps/e-store-content
aliases: ["E-Store Content", "EStore Content", "Estore content sync", "enable disable button", "app active toggle"]
tags: [apps, administration, content, sync]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# E-Store Content

## Purpose

**E-Store Content** integration — provides **product content synchronisation** from external content providers. Used to auto-populate product data (descriptions, images, specs) from manufacturer / distributor feeds — instead of the merchant manually writing each product description.

The integration follows the event-driven pattern (similar to ERP apps) — when a product is added or updated, the platform queries the e-store-content source for fresh data.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **E-Store Content**. See [[apps-e-store-content-settings]] for configuration.

## What the merchant can do here

- Configure E-Store Content API credentials.
- Map CloudCart products to E-Store Content products (typically by EAN / SKU).
- Trigger sync — pull descriptions, images, specs.
- Configure which event types trigger the sync.

### What the merchant CANNOT do here
- Use without an active E-Store Content subscription.
- Override synced content (the manual product description is replaced — verify behaviour).

## Settings & fields

Manager exposes:
- `match(?Variant $variant)` — maps the variant to the E-Store Content's internal identifier.
- the configured check — credential validity.
- `getEvents` — returns the list of event types this integration subscribes to.
- `hasStatusChange` — boolean indicating status-change event involvement.

Event-driven pattern matches the same model used by [[apps-flix-facts]].

## Business rules

### Content provider authority

E-Store Content is the master source for product content; CloudCart's local data is overwritten on sync. The merchant should NOT manually edit synced fields (changes would be overwritten on next sync).

### Event subscription

The `getEvents` returns the subscribed events — likely product create / update.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-e-store-content-settings]] — settings sub-page.
- [[products-products]] — products receive synced content.
- [[apps-flix-facts]] — sister event-driven integration with similar pattern.
- [[apps-load-bee]] — alternative external content provider.

## How it works (verified against backend)

### Provider: estorecontent.com (third-party rich-content module)

E-Store Content is the SaaS service **estorecontent.com**. CloudCart's integration loads their official `rich_content.js` module from `//delivery.estorecontent.com/static/rich_content.js` on the product-details page. The module then injects manufacturer-provided rich content (images, specs, marketing copy) inline.

There is **no server-side data sync** — nothing about the product is rewritten in CloudCart's database. The content is rendered client-side in the visitor's browser by the module. So the merchant's manually-written product description is preserved and the rich content appears alongside it (or replaces an empty description; see "When the module fires" below).

### Match key: SKU or barcode

The `match.self` setting picks how products are looked up against E-Store Content's catalog:

- `sku` (default) — sends the variant's SKU to the module.
- `barcode` — sends the variant's barcode instead.

Only one option is used per store. The merchant must align their SKUs / barcodes with the codes the manufacturer registered with estorecontent.com; otherwise the module finds no match and renders nothing.

### Required settings

The app needs all three of `e_store` (the **shop-id** registered with estorecontent.com — passed as `data-shop-id`), `match.self` (sku or barcode), and `locale` (the content language the merchant wants pulled from the manufacturer's catalog). All three are required for the module to load.

### When the module fires

On every storefront request for a product details page, the integration runs after the product view event:

1. Exits if not in the `site` namespace (the module only loads on the storefront).
2. The module injects only when the product **does not already contain the module div** (`id="e-store-esc-rich-content"`) AND when the merchant has not written a meaningful description themselves (the `hasText` check skips when the description has substantive content).
3. Appends an HTML snippet to the description that loads the `rich_content.js` script with the merchant's shop id + product SKU + locale.

The module then talks to estorecontent.com directly from the browser and renders the manufacturer's content into the empty `#e-store-esc-rich-content` div.

### Sync direction

The integration is **strictly one-way at runtime** (estorecontent.com → browser → product page). CloudCart does not POST anything back to estorecontent.com. Local product descriptions are not overwritten in the database; the module renders on top of whatever the merchant has written.

### Field-level merge

There is no merchant-side picker for "sync only images, not descriptions". The module chooses what rich content to render — it may include images, marketing copy, specs etc. depending on what the manufacturer uploaded to estorecontent.com. The CloudCart side cannot filter that down field-by-field.

### Multi-language

The `locale` setting tells the module which language version to fetch. Picking `en` shows English content; `bg` shows Bulgarian; etc. For a multilingual storefront, the merchant typically sets this once at install — the rich content always loads in that fixed locale regardless of which storefront language the customer is viewing.

### "Has text" guard prevents content overwrite

The integration uses `hasText` to detect whether the merchant has written a real description. If they have, the module is **not** injected — so manual descriptions take precedence. If the description is empty, the module loads.

### Cost model

CloudCart does not charge per-product for using this app — pricing depends on the merchant's contract with estorecontent.com. The Shop ID the merchant pastes in this app is issued by estorecontent.com after they sign up there. Without a valid estorecontent.com account, the module loads but renders nothing.

### Module div ID acts as idempotency guard
The platform checks the product's description for `id="e-store-esc-rich-content"` BEFORE appending the module snippet. If the merchant has already pasted the module container into their description manually (or it was injected by a previous page render that was cached), the auto-injection is skipped — no duplicate containers.

### Site namespace gate
The injection runs ONLY when `app_namespace == 'site'` — so the admin's product editor preview and the theme builder both skip the E-Store Content module. Merchants editing products don't see the rich content interfering with their own description editing.

## Open questions

