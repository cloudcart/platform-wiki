---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Testimonials and press mentions"
aliases: ["Testimonial metaobject", "Customer testimonials", "Press mentions", "As seen in", "Social proof", "Case studies", "Отзиви на клиенти за магазина", "Споменавания в медии", "Препоръки", "Казуси"]
tags: [metafields, metaobjects, use-case, content, social-proof, marketing]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Use case: testimonials, press mentions and case studies

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Product reviews say what shoppers think of **a product**. Many stores also show proof about **the store itself**:

- a quote from a happy customer with their photo;
- a row of "As seen in" media logos;
- a B2B case study with a client's logo.

This content is curated by the store, not submitted by shoppers. **`testimonial` and `press_mention` metaobjects** hold it as entries that can be shown on the homepage, on landing pages, and next to the products they mention.

## Scope

### The data model

**Metaobject definition `testimonial`**, active/draft status **on** (drafts until the customer agrees to publication):

| Field | Type | Notes |
|---|---|---|
| `author` | single-line text, required | Display name: *Maria, Plovdiv*. |
| `quote` | multi-line text, required, `max` 500 | |
| `rating` | `rating`, scale 1–5 | Optional stars. |
| `photo` | file (Image) | |
| `product` | `product_reference` | The product it is about, if any. |
| `received_on` | `date` | **Admin filter** on. |
| `channel` | single-line text, `choices`: *Email, Phone, Instagram, In store* | For staff. |
| `featured` | `boolean` | **Admin filter** on: shown on the homepage. |

**Metaobject definition `press_mention`**:

| Field | Type |
|---|---|
| `outlet` | single-line text, required |
| `logo` | file (Image) |
| `headline` | single-line text |
| `url` | `url` |
| `published_on` | `date` |

**Product metafield** `custom.testimonials` (`list.metaobject_reference` → `testimonial`) picks the quotes shown on a product page.

### On the Nitrogen storefront

- **Homepage**: `metaobjects(type: "testimonial", query: "fields.featured:true", first: 6)`. Only active entries are returned.
- **Product page**: the product's `custom.testimonials`, beside the native reviews.
- **"As seen in" row**: `metaobjects(type: "press_mention", sortKey: "updated_at", reverse: true)`, or a fixed order through a `section_testimonials` entry on a landing page ([[metafields-use-case-page-sections]]).

### Consent and privacy

A testimonial names a real person. Keeping it in **draft** until consent is given, and switching it back to draft when consent is withdrawn, takes it off the storefront at once. Linking a testimonial to a customer record with `customer_reference` is possible. The Storefront API never returns the customer behind such a reference, only an id, so the public name always comes from the `author` field ([[metafields-permissions]]).

## Contrasts

- **Testimonials vs product reviews** ([[apps-product-review]], [[marketing-reviews]]): reviews are written by shoppers, collected and moderated by the review app, and returned by the Storefront API as `Product.reviews` and `reviewSummary`. Testimonials are chosen and entered by the store. The two are not mixed: a review does not become a testimonial entry automatically.
- **Entries vs a CMS page**: a page holds quotes as one HTML body. Entries can be picked per product, filtered, and drafted one by one.

## Where it applies

- Service-heavy and premium stores, B2B suppliers (case studies with client logos), brands with press coverage, stores whose customers send thank-you messages.
- Both definitions are `PUBLIC_READ`. Visibility is set per definition, not per field, so every field of a public entry can be read on the storefront, `channel` included. Internal notes, such as who approved a quote and when, go in a separate definition with storefront access `NONE` that references the testimonial.

## Related

- [[metafields-use-cases]]: all use cases.
- [[apps-product-review]]: native product reviews.
- [[metafields-use-case-page-sections]]: placing testimonials on landing pages.
- [[metaobjects-definitions]]: active/draft status.

## Open Questions

- None known.
