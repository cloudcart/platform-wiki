---
type: feature
nav_path: "Apps → XML Import → Mapping fields"
route_name: apps.xml_import
route_path: /admin/apps/xml_import (Step 2 + Step 3 mapping configuration)
aliases: ["XML Import — mappable fields", "XML Import — variant patterns", "XML Import — category auto-creation", "XML Import — custom fields", "XML Import — Update checkbox", "XML Import — image download", "XML Import — base64 image rejection", "XML Import — HTML sanitisation", "XML Import — tags / brand / supplier mapping", "XML Import image update deletes existing", "XML Import broken image leaves product without image", "XML Import don't update images"]
tags: [apps, imports, xml, mapping, variants, categories]
plan_gates: []
created: 2026-06-10
updated: 2026-06-19
source_count: 2
---

> Part of [[apps-xml-import]]. See the hub for the other aspects (wizard, job pipeline, fetch transport, plan gates, side effects).

# XML Import — mappable fields

## Purpose

The wizard turns raw XML tags into CloudCart product fields. This page catalogues **what can be mapped**, **how the three variant structural patterns work**, **how category placement is decided**, **how images and inline data are handled**, and **what gets quietly transformed** (HTML sanitisation, dropped rows). Without this catalogue the wizard's Step 2 is hard to reason about — XML feeds vary wildly and the wizard's behaviour is more permissive in some places and stricter in others than merchants assume.

For the wizard flow that surfaces these mappings see [[apps-xml-import-wizard]]; for how mapped values flow into the catalog see [[apps-xml-import-side-effects]].

## Where to find it

Apps → XML Import → Step 2 (tag mapping) + Step 3 (finalisation including category / tax / vendor / custom fields).

## What the merchant can do here

- Map the repeating "product" XML tag (each occurrence becomes a CloudCart product row).
- Map per-product tags to CloudCart fields: name, price, SKU, description, image URL, category path, quantity, weight, brand_model, tags, supplier data.
- Choose ONE of three variant structural patterns and apply uniformly to every row.
- Mark each field as Update / Don't-update (the per-field Update checkbox controls subsequent re-parse overwrites).
- Map structured extras: category properties + description tabs.
- Set a fixed category that overrides the XML's category mapping.

What the merchant CANNOT do here:

- Map arbitrary "custom fields" — only the explicit category-property + description-tab slots.
- Import inline base64-encoded images (these rows are silently dropped).
- Bypass HTML sanitisation on description / SEO fields.

## Settings & fields

Mappable groups:

| Group | Examples | Notes |
|-------|----------|-------|
| Identity | name, SKU, barcode, brand_model | brand_model maps to the product's brand field. |
| Pricing | price, regular price, currency | Honoured as text → numeric conversion. |
| Inventory | quantity | Written only when `track_inventory` is ON (see [[apps-xml-import-wizard]]). |
| Description | description, short description, SEO title, SEO description | All run through `xss_clean`. |
| Images | image URL (main + gallery) | Downloaded into CloudCart media library; base64 inline data is dropped. |
| Category | category path | Auto-created when missing; multi-level on `>` separator. |
| Variants | parameter / option / variant tags | Three structural patterns — see below. |
| Tags | tag list (comma-separated) | Maps to product tags. |
| Custom data | category properties, description tabs, supplier data | Structured extras only — no arbitrary fields. |

## Business rules

### Field-mapping persists per task

The mapping skeleton and operation rules are stored on the task record. **Once configured, the same mapping is reused on every re-parse** — the merchant doesn't re-map every 12 hours. Editing any field resets the mapping (forcing re-parse). See [[apps-xml-import-wizard]] for the edit-clears-hash flow.

### Update strategy — per-field "Update" checkbox

The merchant controls which fields refresh per Step 2's `update` checkbox PER FIELD. Only fields explicitly marked "updatable" overwrite on subsequent runs. Unmarked fields (e.g., description) keep their existing CloudCart values. Matching uses the task's import ID + a per-row task key stored on the product. This lets the merchant say "refresh prices and stock every 12h, but never overwrite my edited descriptions".

### Images — downloaded into CloudCart media library

Image URLs from the XML are downloaded — **CloudCart stores each image in its own media library**. Not hot-linked. On updates, images are replaced if the URL differs (effectively comparing source URL, not content checksum). Variant images are queued separately as a background job.

### Image update is delete-first — a broken feed URL can leave the product with no image

When **Images** is marked updatable in Step 2, every re-import compares the feed's image **URLs** against the stored ones (a URL hash, not the content). If they differ, the importer **deletes the product's existing images first** (and clears `image_id`), then downloads the new URLs. Because the "changed" test is purely the URL, a feed that points an image at a **new but broken / unreachable URL** still counts as changed: the old image is deleted, the new download then fails, and **the product is left with no image at all**. The deletion is **not rolled back** when the download fails.

What avoids it:

- **Leaving Images unchecked for update** on subsequent runs — the replace path then never runs and existing images are preserved (the importer only re-evaluates images when the field is marked updatable). This is the safe choice once the catalogue's images are in place and only price / stock need refreshing.
- A feed that **omits the image field entirely** is safe — an empty new-image set short-circuits before any deletion. The risk is specifically a *present but broken* image URL, not a missing one.

### Base64 inline images — NOT supported (rows dropped)

Rows where the XML contains inline base64-encoded image data (`base64,...` substring) are **dropped silently** before being queued for insert. The merchant must supply image URLs, not embedded data. This is a defensive cap on memory / row size — a 5 MB inline-base64 image would explode the queue payload.

The silent-drop matters: the merchant won't see an error, just fewer products imported than expected. Support tickets reporting "some rows missing" should check whether the source feed embeds images inline.

### Category auto-creation from XML path

When the XML references a category not in CloudCart, **the platform auto-creates it**. Multi-level paths (e.g., `Electronics > Phones > Smartphones`) are split on `>` and each level is created in order. If the task has a fixed `category_id` set on Step 1 (see [[apps-xml-import-wizard]]), the XML's category is IGNORED and all products land in the chosen category. Categories are matched by name OR by external metadata (so re-imports don't duplicate).

### Variant import — 3 structural patterns supported

The merchant chooses ONE of three XML structure patterns in Step 2 (`(verify)` exact label per pattern):

- **Multilevel** — each XML product has nested `<option>` elements with `name + value` pairs (up to 3 option groups: p1/v1, p2/v2, p3/v3). Used when the supplier nests variant structure inside the product tag.
- **Singlelevel** — flat per-product variant fields. Used when the supplier exposes one row per variant (no nesting).
- **Template** — CloudCart's native template format. Used when the feed was generated by CloudCart or follows the platform's template shape.

The chosen pattern is stored on the task as a `singlelevel` / `multilevel` / `template` flag and applied uniformly to every row in the feed. See [[variants-model]] for what Parameter / Option / Variant mean in CloudCart.

### Custom fields = category properties + description tabs

The importer doesn't expose arbitrary "custom fields" — instead, two slots accept structured extras:

- **Category Properties** — `properties.name` + `properties_options.value` mapping creates category-property records auto-linked to the product's category.
- **Description tabs** — `tab_name` + `tab_value` pairs map to the multi-tab description blocks on the product page.

Tags (comma-separated), `brand_model`, and supplier data are similarly mapped through dedicated XML fields.

### HTML sanitised through `xss_clean` on every imported value

Every imported text value (name, description, SEO fields, etc.) is decoded (`html_entity_decode`) and run through the platform's `xss_clean` helper before storage. Script tags / event handlers / `javascript:` URLs in supplier feeds are stripped silently. Merchants relying on raw HTML in descriptions should expect light sanitisation.

### Preview-window `lines` is NOT a cap on import size

The `lines` field (rows to scan in the structure-detection preview) is validated `min:20`, `max:1500`. This is **NOT a cap on the import itself** — it's how many XML rows the platform reads to discover the structure before showing the mapping wizard. The full import processes every record in the feed.

### `track_inventory = OFF` ignores the quantity mapping

Even if the merchant maps an XML quantity tag, when Step 1's `track_inventory` toggle is OFF the quantity is NOT written. The product's Variants retain whatever stock value the merchant manages manually. See [[apps-xml-import-wizard]] + [[inventory-variant-model]].

## Related

- [[apps-xml-import]] — hub.
- [[apps-xml-import-wizard]] — the flow that surfaces these mappings.
- [[apps-xml-import-job-pipeline]] — how mapped data flows through Parse → Insert.
- [[apps-xml-import-side-effects]] — what fires after mapped data is written.
- [[apps-xml-import-step2]] / [[apps-xml-import-step3]] — screen-level documentation for the mapping screens.
- [[variants-model]] — Parameter / Option / Variant hierarchy.
- [[inventory-variant-model]] — what `quantity` means on a Variant.
- [[products-products]] — the product editor where mapped data shows up.

## Open questions

_None._
