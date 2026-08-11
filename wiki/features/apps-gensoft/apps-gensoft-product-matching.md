---
type: feature
nav_path: "Apps → Gensoft → Product matching"
route_name: apps.gensoft.products
route_path: /admin/apps/gensoft/products
aliases: ["Gensoft product matching", "Gensoft compare_by", "Gensoft article ID", "Gensoft external_record_key", "Gensoft connect product", "Gensoft ID missing", "Gensoft mapping"]
tags: [apps, erp, gensoft, matching, mapping]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 3
---

> Part of [[apps-gensoft]]. See the hub for the other aspects (settings, sync model, reset import, diagnostics).

# Gensoft — product matching & the mapping

## Purpose

How a Gensoft article is matched to a CloudCart product (update vs create), where the Gensoft id is stored, how to fix a mapping by hand, and why order push can be blocked by a "missing Gensoft ID".

## Where to find it

The match field (**Compare by**) is on [[apps-gensoft-settings]]; the per-product mapping is managed on the **Products** tab (the Connect modal). The mapping rows live in the shared [[external-record-mapping]] store.

## What the merchant can do here

Pick **Compare by** so incoming Gensoft articles match the right CloudCart products, and **manually connect** a product to a Gensoft article id from the Products tab when automatic matching missed it.

## Settings & fields

Only `compare_by` (on [[apps-gensoft-settings]]) is merchant-set. The mapping itself is the `ExternalMetaData` store (`integration = gensoft`) plus the `app_import = 'gensoft-<article ID>'` origin tag.

## Business rules

### The match field — `compare_by`

The merchant picks how an incoming Gensoft article links to a CloudCart product:

- **SKU** (default) — Gensoft's `Sku` vs the CloudCart variant's SKU.
- **Barcode** — Gensoft's `Barcode` vs the variant's barcode.
- **External ID** — match by the stored Gensoft article id (the mapping below), not a catalogue field.

If the chosen field doesn't match an existing product, the article is imported as a **new** product.

### The mapping is the shared `ExternalMetaData` store

Once a Gensoft article is linked, the platform stores the link in [[external-record-mapping]]: an `ExternalMetaData` row with `integration = gensoft`, `external_record_key = <Gensoft article ID>` (`gensoftVariant->ID`) → the CloudCart **variant** (`record_type = Variant`). The product also carries `app_import = 'gensoft-<article ID>'`. This is the **same table** Microinvest and the import apps use — read it with the `externalMetaData` / `externalMetaIntegrations` queries on [[external-record-mapping]].

### Manual connect / disconnect (Products tab)

When automatic matching misses (or links the wrong product), the merchant can fix it by hand on the **Products** tab's **Connect** modal: entering a Gensoft article id writes (updates-or-creates) the variant's `ExternalMetaData` row for `integration = gensoft`. Deleting a product from the Products tab removes its mapping row. So the mapping is both auto-built (import) and hand-editable.

### Order push needs the Gensoft id — the validation block

Pushing an order to Gensoft reads each line's Gensoft id **from the mapping** (`external_record_key`). Before sending, the integration checks every product has a valid Gensoft id; if any are missing it blocks the order with *"There is a product with invalid or missing Gensoft ID"* (or *":count products with invalid or missing Gensoft IDs"*). Gensoft order lines without an article id are skipped on send. So a *"my order won't push to Gensoft"* ticket is usually an **unmapped line** — connect it on the Products tab (or re-import) so it gets a mapping row.

### Deletion / disappearance signal

There is no auto-delete of CloudCart products when Gensoft stops returning an article; instead the [[apps-gensoft-diagnostics|Diagnostics]] **Known products** check re-samples previously-mapped Gensoft article ids and warns when Gensoft no longer returns them — the classic signal behind "products silently disappeared".

## Related

- [[apps-gensoft]] — hub.
- [[external-record-mapping]] — the shared `ExternalMetaData` table + the read queries.
- [[apps-gensoft-settings]] — the `compare_by` setting.
- [[apps-gensoft-sync-model]] — order push that consumes the mapped id.
- [[apps-gensoft-diagnostics]] — the Known-products check that flags lost mappings.

## Open questions

(none)
