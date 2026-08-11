---
type: feature
nav_path: "Apps → eMag Sync"
route_name: apps.emag_sync.settings
route_path: /admin/apps/emag-sync
aliases: ["eMag Sync", "Emag Sync", "eMag Marketplace", "Emag.bg", "Emag.ro"]
tags: [apps, marketplace, emag, sync, romania, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 1
---
# eMag Sync (Marketplace integration)

## Purpose

**eMag Sync** publishes the merchant's products to **eMag** — the dominant marketplace across Bulgaria, Romania, Hungary, and Poland. Customers browsing eMag see the merchant's products there; the price-comparison + reviews ecosystem drives discovery in eMag's served markets.

The integration is a one-way **product feed**: CloudCart writes the catalog out as eMag-formatted XML and eMag ingests it. There is no order pull-back or fulfilment API — the merchant should think of this as a feed, not a full two-way Marketplace integration.

## Where to find it

Sidebar → Apps → install → **eMag Sync**. The route is `/admin/apps/emag-sync`.

The feed reuses the **XmlFeed export pipeline** (same family as [[apps-xml-feed]]) with an eMag-specific XML template that transforms CloudCart products into eMag's expected schema. The internal feed key is `emag`.

## What the merchant can do here

- Publish the product catalog to eMag as a feed that eMag fetches on a fixed schedule (see Business rules).
- Rely on the feed to keep eMag's prices and stock roughly in step with CloudCart (within the refresh window).

### What the merchant CANNOT do here
- Use eMag Sync without an active eMag Marketplace seller contract (eMag.bg / eMag.ro / eMag.hu / eMag.pl).
- Bypass eMag's category taxonomy — products eMag can't map to its categories are rejected on eMag's side.
- Sync to multiple eMag markets with one configuration — each country is a separate contract + endpoint, so each needs its own setup.
- Pull customer / order data from eMag through this app. Orders placed on eMag stay on eMag; CloudCart does not import them into the [[orders]] list, and CloudCart stock is **not** decremented when eMag sells one of the merchant's products. The merchant reconciles stock themselves or via eMag's seller portal.
- Configure credentials, category mapping, or the target market in the admin. The modern Vue settings screen is an empty placeholder; eMag onboarding is arranged through CloudCart support, not self-service.

## Settings & fields

There is no in-app configuration UI — the Vue settings screen is a stub. The feed runs against whatever is configured at the platform level. Each product row in the feed carries:

- `product_id`, `category_path` (full path joined with " > "), `name`, `brand` (from the product vendor), `variant_id`, `sku`, `barcode`, `description`, `url`
- `quantity` (rounded **up** — see Business rules), `weight`, `handling_time`
- `price`, `price_without_vat`, `discounted_price`, `discounted_price_without_vat`
- up to 4 image URLs (`image_url_0` through `image_url_3`)

No warranty / return-policy fields, no eMag category ID, no FBE / Genius flags are sent.

## Business rules

### Feed refreshes every 4 hours
The feed is regenerated and re-uploaded every 4 hours (14,400 seconds). Price and stock changes on CloudCart take up to 4 hours to reach eMag, and the merchant cannot speed this up from the UI.

### Same pipeline as the URL-pull marketplaces
eMag uses an **upload** model — CloudCart pushes data into eMag — which differs from [[apps-xml-feed]]'s URL-pull marketplaces (Skroutz, Glami, Pazaruvaj, Arukereso) where the consumer crawls a CloudCart-exposed URL. Despite the different direction, the feed runs on the **same shared XML-feed framework** as Skroutz, Glami, Channelsight, Retargeting, Profitshare, and Commerce Connector. Scheduling, batch upload, S3 storage, and retry behaviour are all the shared framework; only the XML template is eMag-specific. Multiple eMag feed instances can run concurrently, and the upload runs as a background task on the export queue. Large catalogs process in chunks; per-product failures are logged and the batch continues.

### One feed row per variant
Each CloudCart variant becomes a separate `<product>` row. The variant name is the product name with **every** variant axis value appended, joined with ", " — so a 3-axis variant reads "Product Name, Red, M, Cotton". Each row carries that variant's own SKU, barcode, price, stock, weight, and category path; eMag treats each row as a distinct listing.

### Maximum 4 images per product
Only the first 4 additional product images are sent. Products with more get truncated. The image URL is the S3 path with the query string (resize parameters) stripped, so eMag fetches the raw S3 image directly — CloudCart does not download or resize.

### Handling time is fixed at 2 days
The `<handling_time>` element is always 2 days for every product. The merchant cannot change this per-product or per-shop.

### Prices are always sent VAT-exclusive
`price_without_vat` and `discounted_price_without_vat` are always computed pre-VAT, even for stores that display VAT-inclusive prices. The merchant cannot send VAT-inclusive prices to eMag.

### Discount display depends on `hide_discount_price`
When the product's discount has `hide_discount_price = 1` (or an `msrp_price` is set) **and** a discounted price exists, both `price` and `discounted_price` receive the discounted value — the original is hidden from eMag. Otherwise, when a discount exists, eMag gets `price` = original and `discounted_price` = discounted. With no discount, both fields are equal. Merchants who want to hide a strikethrough on eMag need `hide_discount_price` set.

### Quantity is rounded up
Variant quantity is rounded up, so 2.3 becomes 3 and 0.1 becomes 1. eMag does not accept fractional quantities, and rounding up avoids showing "0 in stock" when a partial unit exists.

### Per-product eligibility
eMag rejects products missing its required fields (e.g. EAN, brand for certain categories, safety certifications). The merchant typically pre-filters before publishing.

### Permission
Standard apps permission scope.

## Related

- [[apps]] — App Store hub.
- [[apps-xml-feed]] — URL-pull marketplaces (different model from eMag's upload).
- [[apps-xml-feed-generator]] — custom XML for arbitrary consumers.
- [[apps-olx]] — sister marketplace (Bulgarian / Polish — similar two-way model).
- [[apps-tiktok-shop]] / [[apps-google-shopping]] — sister marketplace integrations.
- [[apps-etsy]] — sister marketplace integration.
- [[products-products]] — products synced to eMag.

## Open questions

