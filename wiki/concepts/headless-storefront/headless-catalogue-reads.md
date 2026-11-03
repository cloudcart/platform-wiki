---
type: concept
nav_path: "Concept → Headless storefronts → Catalogue reads"
aliases: ["Storefront API catalogue", "linkedProducts", "relatedProducts", "productRecommendations", "Product.tabs", "quantityDiscounts", "quantityTierPrice", "topLevel", "withProducts", "node", "nodes", "requiresCustomerLogin", "pricesRequireLogin", "Свързани продукти Nitrogen", "Каталог през Storefront API", "Табове на продукт API", "Частен магазин Nitrogen"]
tags: [nitrogen, headless, storefront-api, catalogue, products, collections, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

> Part of [[headless-storefront]].

# Headless — catalogue reads

## Definition

The rules behind what a Nitrogen storefront reads from the catalogue through `/api/sf`: what a list contains, in what order, and what it leaves out. The field lists themselves are answered by introspection. These are the behaviours a schema cannot show, or states only briefly.

## Scope

Covered:

- Linked and related products, product tabs, quantity tiers.
- Listing categories; `node` and `nodes`.
- What the API leaves out: private pages, stores turned off.
- The private store, credit plans, menu ids and customer orders.

Not covered:

- The default order of product listings, and listing smart collections — see [[headless-product-listing-order]].
- Metafields and metaobjects — see [[metafields-nitrogen]].
- Limits and page sizes — see [[headless-storefront-limits]].

## Contrasts

- **`linkedProducts` vs `relatedProducts` vs `productRecommendations`** — the first is the merchant's list alone. The second is that list and then the category's products, to page through. The third gives at most ten, with no cursor.
- **`ProductVariant.quantityDiscounts` vs `Product.quantityDiscounts`** — the first is that variant's tiers. The second is the default variant's.

## Where it applies

### Linked products

`linkedProducts` is the merchant's list, in the merchant's order, read as the storefront shows them: no draft, no product outside its dates, and the merchant's first 250.

`unavailableProducts: HIDE` leaves out what cannot be bought, and `LAST` lists it after the others. Left out, the store's settings decide. A store that hides such products keeps them hidden whatever is asked.

### Related products

`relatedProducts` gives up to 50 linked products, then the products of the main category and the categories under it, without this product or the linked ones.

- `first` defaults to 25, at most 100. Forward only.
- `filters` is empty on this connection.
- `linked: false` leaves out the linked part, and still every linked product: for a storefront that shows `linkedProducts` apart.

See [[metafields-use-case-related-products]] for a merchant's own lists.

### Product tabs

`Product.tabs` gives each tab's title and HTML, in the order the merchant dragged them in the product editor. Older tabs keep the order they were added in. The schema's text says "in the order they were added", which holds only for those. The web storefront's own sections (stock per shop, reviews) are not among them. `descriptionTitle` is the name given to the description's tab, or null when there is none: show your own.

### Quantity tiers

- `ProductVariant.quantityDiscounts`: its own tiers, or the product's when it has none, for the buyer's customer group.
- `Product.quantityDiscounts`: the default variant's.
- `Product.quantityTierPrice(lines:)`: what the given pieces cost by the cart's rule. By default each line reaches a tier with its own quantity. With the discount's `quantity_count_all_lines` on, the pieces of all lines add up. Each line takes its own variant's price at the tier reached. It answers null when a line is another product's, a quantity is under one, or there are over 100 lines. The schema's text describes only the pooled case.

See [[quantity-discount-line-counting]] for the switch and [[quantity-discount-tier-evaluation]] for the rule, bundle lines included.

### Discount on a product

`Product.discount` is the one the shown variant is priced from, dated and limited to the buyer's customer group, so an ended discount no longer shows. `endsAt` is the end of its last day in the store's timezone, in UTC; `endDate` is deprecated. With a manufacturer's suggested retail price, the compare-at price is that price.

### Listing categories

`collections` takes `topLevel` (no parent), `withProducts` (products in it or a category under it, as the listing engine counts them) and `sortKey: MANUAL` (the merchant's order among one parent's categories; `reverse` the other way). The store's own categories page is `topLevel: true, withProducts: true, sortKey: MANUAL`.

### `node` and `nodes`

They take the global ids of `Product`, `ProductVariant`, `Collection`, `Vendor`, `ProductTag`, `Page`, `Blog`, `Article`, `ArticleTag` and `StoreLocation`, under the same rules as the type's own lookup. An object the storefront does not show answers null, as does an id of another kind or a plain id. `nodes` takes at most 100 ids.

### What is left out

- **Pages:** `page`, `pages`, `node` and `search` leave out a page the Membership app made private, while the app is installed. Menus, policies and legal pages keep it. An inactive page and a page-builder page are left out too. See [[page]].
- **Store locations:** `storeLocation`, `storeLocations`, `node`, `nodes`, `Product.stockByStore` and `ProductVariant.stockByStore` leave out a store the merchant turned off, and `cartDeliveryAddressUpdate` refuses it as the pickup store. See [[apps-stores-main-locations]].

### Private store and prices for signed-in customers

`Shop.requiresCustomerLogin` is true when the Private store app has "require registration" on, and false when the app is not installed, is off or does not require it. The classic storefront sends a guest from its home, catalog, product, search and blog pages to the login page. Through the API the storefront itself opens on sign-in and registration. See [[apps-private-store]].

`Shop.pricesRequireLogin` follows the cart setting "Show product price only for logged in users". The schema makes showing them the client's part: a client leaves prices out for a guest, as the web storefront does.

### Smaller rules

- **Credit plans:** `ProductCreditOffer.plans` lists the lowest monthly payment first, the shorter term first between equal.
- **Menus:** `Menu.id` and `MenuItem.id` are the store's numbers, not global ids, and each is unique only among its own kind. The resource an item links to is in `resourceId`.
- **Customer orders:** `Customer.orders` lists newest first by id, with cancelled orders left out. `sortKey` and `reverse` are accepted but do not change the order yet.
- **Images:** `Image.url` takes transforms through the store's image CDN.
- **Addresses:** customer addresses follow the store's address settings, with one `CustomerUserError` per field, and a VAT number is confirmed with VIES when asked.

### Product reviews

The settings and their API names are on [[apps-product-review-settings]], and answers on [[apps-product-review-qa]].

## Related

- [[headless-storefront]] — hub.
- [[headless-product-listing-order]] — default order and smart collections.
- [[headless-storefront-limits]] — page sizes and list caps.
- [[headless-cart-rules]] — discounts in the cart.
- [[metafields-nitrogen]] — metafields and metaobjects.
- [[apps-private-store]] — the Private store app.
- [[quantity-discount-line-counting]] — counting per line or across lines.

## Open Questions

_None._
