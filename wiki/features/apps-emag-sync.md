---
type: feature
nav_path: "Apps → eMag Sync"
route_name: apps.emag_sync.settings
route_path: /admin/apps/emag-sync
aliases: ["eMag Sync", "Emag Sync", "eMAG", "eMAG app", "eMag Marketplace", "Emag.bg", "Emag.ro", "Do eMAG orders reduce stock", "eMAG onboarding"]
tags: [apps, marketplace, emag, sync, romania, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-11-09
source_count: 2
---
# eMag Sync (Marketplace integration)

## Purpose

**eMag Sync** publishes the merchant's products to **eMag** — the dominant marketplace across Bulgaria, Romania, Hungary, and Poland. Customers browsing eMag see the merchant's products there; the price-comparison + reviews ecosystem drives discovery in eMag's served markets.

The integration is a one-way **product feed**: CloudCart writes the catalog out as eMag-formatted XML at a public address, and eMAG reads it. Nothing comes back: no orders, no stock, no offers. CloudCart has no connection to eMAG's own API (no eMAG credentials are stored, nothing is pushed to eMAG). The store's Apps catalogue lists it as **eMAG**.

## Where to find it

The feed itself is the **Emag** feed of the XML Feed app: Apps → **XML Feed** → **Emag** (`/admin/apps/xml_feed/emag`), where the merchant activates it and copies its public address ([[apps-xml-feed-emag]]). The screen at `/admin/apps/emag-sync` is an empty page with no settings. The internal feed key is `emag`.

## What the merchant can do here

- Publish the product catalog as a feed that eMAG reads (see Business rules for the refresh).
- Keep eMAG's prices and stock roughly in step with CloudCart, in that one direction.

**Onboarding.** On CloudCart's side: activate the Emag feed and give its public address to eMAG. Becoming an eMAG seller, having the feed accepted, matching products to eMAG's categories and how long that takes are eMAG's process in the seller account (verify whether CloudCart support also takes part).

### What the merchant CANNOT do here
- Sell on eMAG without an eMAG seller account; that contract is with eMAG.
- Map categories to eMAG's taxonomy in CloudCart. The feed sends the store's own category path; matching it to eMAG's categories happens on eMAG's side.
- Pull customer / order data from eMag through this app. Orders placed on eMag stay on eMag; CloudCart does not import them into the [[orders]] list, and CloudCart stock is **not** decremented when eMag sells one of the merchant's products. The merchant reconciles stock themselves or via eMag's seller portal.
- Configure credentials, category mapping, or the target market in the admin: there are none.

## Settings & fields

There are no eMAG-specific settings; the feed has the shared XML Feed controls (which products, in stock only, hidden products). Each product row in the feed carries:

- `product_id`, `category_path` (full path joined with " > "), `name`, `brand` (from the product vendor), `variant_id`, `sku`, `barcode`, `description`, `url`
- `quantity` (rounded **up** — see Business rules), `weight`, `handling_time`
- `price`, `price_without_vat`, `discounted_price`, `discounted_price_without_vat`
- up to 4 image URLs (`image_url_0` through `image_url_3`)

No warranty / return-policy fields, no eMag category ID, no FBE / Genius flags are sent.

## Business rules

### Feed refreshes every 4 hours
The feed is regenerated and re-uploaded every 4 hours (14,400 seconds). Price and stock changes on CloudCart take up to 4 hours to reach eMag, and the merchant cannot speed this up from the UI.

### A feed address eMAG reads, like the other marketplaces
The "upload" in the job's name is the upload of the generated file to the store's own file storage, exactly as for Skroutz, Glami or Pazaruvaj: the feed is a file at a public address that eMAG reads. Only the XML template is eMAG-specific. Large catalogs process in chunks; per-product failures are logged and the batch continues.

### Product allowance
The plan caps how many products the eMAG feed carries. Products beyond the cap are left out and the store gets a plan-limit alert. The included number, and how much the **(QTY) Additional products for Emag** pack adds, are billing catalogue values (verify).

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
- [[apps-olx]] — sister marketplace.
- [[apps-tiktok-shop]] / [[apps-google-shopping]] — sister marketplace integrations.
- [[apps-etsy]] — sister marketplace integration.
- [[products-products]] — products synced to eMag.

## Open questions

- The eMAG feed's included product number and the price of the additional-products pack (billing catalogue).
- What the **eMAG** catalogue entry installs (its record is in the apps database, not in code).
