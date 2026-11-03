---
type: feature
nav_path: "Apps → OLX → Products → Advert formatting"
route_name: apps.olx.products
route_path: /admin/apps/olx/products
aliases: ["OLX advert formatting", "OLX title truncation", "OLX description build", "OLX variant split", "merge_product OLX"]
tags: [apps, olx, marketplace, products, formatting]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX → Products — advert payload formatting

> Part of [[apps-olx-products]]. See the hub for the other aspects (pipeline UI, validation, sync).

## Purpose

This aspect covers **how the OLX advert payload is auto-generated from the CloudCart product**: title formatting, description assembly, images, price source, the BG/RO condition + currency forcing, and the per-variant split. The key takeaway for the merchant: the advert **always** uses the CloudCart product's own data — there is no separate OLX title / description / image field.

## Where to find it

This formatting runs server-side whenever a product is published or synced from the Products tab (`/admin/apps/olx/products`). The merchant influences it through the product's own CloudCart data and a few toggles on [[apps-olx-settings]] (`merge_product`, `title_trim`, `is_discount`).

## What the merchant can do here

- Control the advert text indirectly by editing the product name, description, variant attributes, properties, and vendor on [[products-products]].
- Turn on `merge_product` to split a product into one advert per variant.
- Turn on `title_trim` to surface a UI warning when the title gets truncated.
- Enable `is_discount` so active promotional prices override the regular price.

## Settings & fields

| Setting | Label | Effect on the payload |
|---|---|---|
| `merge_product` | `merge_product` — "Divide the product into varieties" | Push each variant as a separate advert with a title suffix; off = only the parent product is published. |
| `title_trim` | "Trim title" | Controls whether the truncation warning appears in the UI — truncation happens regardless. |
| `is_discount` | (promo pricing) | When on, active promotional discounts override the regular price. |

## Business rules

### No OLX-specific overrides

Title comes from the product name; description is built from variant attributes + properties + vendor + the product description; images come from the product's image collection. There is **no** separate "OLX title" / "OLX description" / "OLX images" field — the advert always reflects the CloudCart product's data.

### Title is capitalized — first letter upper, rest lowercase

The integration force-formats the title: first character `mb_strtoupper`, remaining characters `mb_strtolower`, then the variant suffix is appended. So "iPhone 15 Pro" becomes "Iphone 15 pro - black 128". Brand names with intended camelCase or uppercase styling lose that formatting.

### Title auto-truncated to 70 chars without warning

OLX's title limit is 70 characters. The integration the platform code truncates without ellipsis. The merchant does not see what got cut off unless `title_trim` is on (which only surfaces a UI warning — the truncation happens either way). The 70-char cap applies AFTER the variant suffix is appended, so long names + many variant axes can truncate the variant identifier itself.

### Variant title suffix — up to three axis values

When `merge_product` is on, each variant advert's title gets " - {v1} {v2} {v3}" appended, where v1/v2/v3 are the three variant axis values (e.g. color / size / material).

### Description auto-built from variants + vendor + properties + description

The description is concatenated from: (1) a "For more information" link to the product URL, (2) variant parameters (e.g. "Size: S, M, L"), (3) a "Vendor: {name}" line, (4) all category properties (key: values list), and (5) the product's HTML-stripped description. The merchant does not write a separate OLX description.

### Description regex strips emojis and non-Latin / non-Cyrillic characters

The description is filtered (regex `[^а-яА-Яa-zA-Z0-9 [\],:!-@#$%^&*.]+/ui`) to allow Cyrillic, Latin, digits, spaces, and a fixed set of punctuation. **Emojis, Greek, and Romanian-specific diacritics (ă, â, î, ș, ț) get stripped.** This can mangle non-Bulgarian text even for OLX Romania merchants — expect lossy text.

### No automatic translation

The advert text uses the CloudCart record's primary language. There is no machine translation when the OLX country's language differs from the store language. A Bulgarian-language store publishing to OLX Romania produces Bulgarian advert text on OLX.ro — the merchant must maintain the target-language text themselves.

### Price source — promotional price when active, else regular

The formatter uses `price_from_discounted_input ?: price_from_input` as the base. When `is_discount` is enabled, it iterates active promotional discounts (those not restricted to customer groups), takes the minimum discounted price, and overrides. So an advert can show a price that differs from the regular catalog price when a promotion is live. A product with no price at all aborts the publish — see [[apps-olx-products-validation]].

### Bulgaria / Romania — condition forced to "new", currency forced per country

When the OLX country is Bulgaria (`endpoint_id == 2`), the advert's `state` is hard-coded to `"new"` and currency to `EUR`; for Romania (`endpoint_id == 3`) currency is `RON`. The merchant **cannot publish "Used" products** via this integration on OLX.bg.

### Images passed through as URLs — no CloudCart-side resize

Each product image is added to the payload as a public URL; OLX downloads it from that URL. CloudCart does not pre-resize, re-encode, or check dimensions. Rejected images surface in [[apps-olx-history]]. The image count is capped at the OLX category's `picture_limit` (per-category, fetched from OLX — NOT a global setting). Only the merchant's **logo** has a CloudCart-side size check (minimum 300px); product photos pass through as-is.

### Permission

Standard apps permission scope.

## Related

- [[apps-olx-products]] — hub.
- [[apps-olx]] — OLX feature hub.
- [[apps-olx-settings]] — `merge_product`, `title_trim`, `is_discount` toggles.
- [[apps-olx-products-validation]] — when a missing price aborts the publish.
- [[apps-olx-history]] — where rejected-image / formatting errors surface.
- [[products-products]] — source product (name, description, images).
- [[products-property]] — properties concatenated into the description.

## Open questions

- Whether currency forcing reflects the BG EUR transition vs historic BGN (verify against current production).
