---
type: concept
nav_path: "Concept → Metafields and metaobjects → Use cases → Manuals, certificates and warranty"
aliases: ["Product documents metafield", "User manual download", "Datasheet", "Safety data sheet", "Certificate of conformity", "Declaration of conformity", "Warranty metafield", "Document library", "Инструкция за употреба", "Сертификат", "Декларация за съответствие", "Гаранция", "Документи към продукт"]
tags: [metafields, metaobjects, use-case, files, documents, warranty, compliance]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Use case: manuals, certificates and warranty information

> Part of [[metafields-use-cases]] in [[metafields-metaobjects]].

## Definition

Many products come with paperwork the shopper should be able to open before buying: a user manual, a data sheet, a safety data sheet, a declaration of conformity, warranty terms. Two kinds of paperwork already have native homes, both on the Storefront API:

- **Files attached to a product and marked public**, returned as `Product.files` with name, file name, URL and size.
- The **energy label** and **product information sheet**, part of `Product.energyClass`.

A **`document` metaobject** adds what those do not hold:
- a **kind** and a **language** per document;
- an **expiry date**;
- one document **shared** by many products and replaced in one place.

## Scope

### When the native files are enough

Each product has its own manual or data sheet, and a plain download list is all the page needs. The product's public files cover this, with no metafields.

### When a `document` metaobject adds something

- One certificate or declaration covers a whole product line. Updating it should update every product.
- The storefront groups downloads by kind (*Manual*, *Declaration of conformity* …) or shows the visitor's language.
- Certificates expire and staff need to find the ones about to.
- A store-wide **documentation centre** lists documents across the catalogue.

### The data model

**Metaobject definition `document`**:

| Field | Type | Notes |
|---|---|---|
| `title` | single-line text, required | Display name: *Declaration of conformity — X200 series*. |
| `file` | file, required | Any file from the file manager; PDFs included. |
| `kind` | single-line text, `choices`: *Manual, Data sheet, Safety data sheet, Declaration of conformity, Certificate* | **Admin filter** on. |
| `language` | single-line text, `choices`: *bg, en, de …* | **Admin filter** on. |
| `valid_until` | `date` | **Admin filter** on. |
| `issuer` | single-line text | The certifying body. |

**Product metafields**:

| `namespace.key` | Type | Notes |
|---|---|---|
| `custom.documents` | `list.metaobject_reference` → `document` | The shared documents for this product. |
| `custom.warranty_months` | `number_integer`, `min` 0, `max` 120 | |
| `custom.warranty_terms` | `page_reference` | A CMS page with the full terms ([[page]]). |
| `custom.service_url` | `url`, `allowed_domains`: the manufacturer's domain | Registration or service portal. |

### On the Nitrogen storefront

- A **Downloads** tab on the product page: the native `files`, plus `custom.documents` grouped by `kind`, in the visitor's `language` when one exists. A document's file comes back as `GenericFile` (URL, MIME type, size), or `MediaImage` for images.
- A **documentation centre**: `metaobjects(type: "document", query: "fields.kind:\"Declaration of conformity\"")`.
- A **warranty badge**: "3-year warranty" from `custom.warranty_months`, linking to the terms page.

### Keeping documents valid

- Expiring certificates are found through the Admin GraphQL API: `fields.valid_until:<2026-12-31`.
- Replacing an entry's `file` updates every product referencing the entry.
- Deleting a file from the file manager ([[settings-files]]) removes it from every entry that pointed to it, so no broken download remains.

## Contrasts

- **Public product files vs `document` entries**: native files are the quickest route, one list per product. Entries pay off when documents are shared, typed, multilingual or expiring.
- **Energy label**: the native energy class already carries the label image, the label PDF and the product sheet link. It is not duplicated in metafields.
- **Documents vs digital products** ([[digital-products]]): a digital product is a paid download delivered after purchase. These documents are free information for anyone viewing the product.

## Where it applies

- Electrical and electronic goods, toys, machinery, chemicals, cosmetics, medical devices, construction products.
- Staff need the Files permission to pick or upload a new file in a field ([[metafields-permissions]]).

## Related

- [[metafields-use-cases]]: all use cases.
- [[metafields-types]]: `file_reference`, `page_reference`, `url` with allowed domains.
- [[settings-files]]: the file manager.
- [[digital-products]]: paid downloads, a different mechanism.

## Open Questions

- None known.
