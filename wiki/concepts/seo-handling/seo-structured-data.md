---
type: concept
nav_path: "Concept → SEO handling → Structured data and image alt text"
aliases: ["Structured data", "JSON-LD", "Schema.org", "Product schema", "Rich results", "GTIN", "MPN", "Organization schema", "Breadcrumb schema", "Image alt text", "Alt текст", "Структурирани данни"]
tags: [seo, structured-data, json-ld, schema-org, alt-text, concepts]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[seo-handling]]. See the hub for related aspects (canonical / noindex, meta tags, crawlers and AI assistants).

# SEO — structured data and image alt text

## Definition

Structured data is the machine-readable description of a page (schema.org) that search engines and AI assistants read alongside the visible text. This page lists what a CloudCart storefront outputs on a standard (Smarty) theme, and where image alt text comes from. Read from the code on `origin/master`, not run in a store. Nitrogen storefronts build their own markup ([[nitrogen-vs-themes]]).

## Scope

Covered: the product JSON-LD block, the microdata on other pages, what is not output, and image alt text. Not covered: how Google or others use the data for rich results, which is their own rule.

## Contrasts

- **JSON-LD vs microdata.** The product page carries a JSON-LD block; breadcrumbs, the contacts page, category and vendor pages use microdata attributes in the HTML. Both are schema.org.
- **Open Graph vs schema.org.** The `og:` / `product:` meta tags serve social previews ([[marketing-seo-sharing]]); they are not structured data for search.

## Where it applies

### Product page — JSON-LD `Product`

Every Smarty theme outputs one `Product` JSON-LD block on the product page; there is no setting to turn it off. Its fields:

| Field | Filled from |
|---|---|
| `name` | product name |
| `description` | the product's meta description, else its description, else its name |
| `url`, `releaseDate` | product address; date the product was added |
| `sku` | SKU of the default variant |
| `category` | the product's category name |
| `brand` | the vendor: name, address, image |
| `image` | the main product image |
| `offers` | price (with discount), currency, `InStock` / `OutOfStock`, address; a second offer in EUR when a BGN store shows dual prices |
| `weight` | heaviest variant, in kg, for shippable products |
| `aggregateRating`, `review` | only with the Product Review app active and at least one review |

Not output: `gtin` (any length), `mpn`, `priceValidUntil`, per-variant offers. The product barcode reaches the page only as the `product:retailer_item_id` meta tag, and only when the SKU is empty. So a "missing GTIN" warning in Search Console is expected, and the merchant cannot add GTIN to the block from the admin. The price is omitted when prices are hidden from the visitor.

### Other pages — microdata

- **Breadcrumbs** — `BreadcrumbList`, on theme pages that show a breadcrumb.
- **Contacts page** — `Store`, with address, e-mail and phone only when the contacts module shows them ([[design-module-contact-information]]).
- **Category page** — `Offer` items; **vendor page** — `Brand`.

### Not output

- **Organization** and **WebSite** (with a site-search box): the platform contains them but they are switched off in the shared layout, so no store emits them; logo and social links do not appear as Organization data.
- **FAQPage / QAPage**: product questions and answers ([[apps-product-review-qa]]) are shown on the page but not marked up.

### Image alt text

| Image | Where alt text is set | When empty |
|---|---|---|
| Product images | Product → the image's edit dialog, field **Image alt text** (stored as the image's name) | Pre-filled with the product name on upload; the storefront falls back to the product name |
| Category and vendor images | No field | The theme writes the category or vendor name (as in `flair`; other themes (verify)) |
| Banners and carousel slides | The banner's or slide's caption | Empty alt |
| Page Builder images | Same rules as the banner / carousel blocks they use | — |

[[apps-image-health]] can write AI-generated alt text into the same product-image name field. The Bulgarian label of the **Image alt text** field lives in the admin's translation database, not the code.

## Related

- [[seo-handling]] — hub.
- [[seo-ai-visibility]] — crawlers, AI assistants, verification, feeds.
- [[seo-meta-tags]] — titles and meta descriptions.
- [[apps-product-review-qa]] — product questions and answers.
- [[apps-image-health]] — image checks and AI alt text.

## Open Questions

- Structured data on Nitrogen storefronts is built by each storefront and is not covered here.
