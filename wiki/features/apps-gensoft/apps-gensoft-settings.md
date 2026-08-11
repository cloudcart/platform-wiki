---
type: feature
nav_path: "Apps → Gensoft → Settings & tabs"
route_name: apps.gensoft.settings
route_path: /admin/apps/gensoft/settings
aliases: ["Gensoft settings", "Gensoft WSDL", "Gensoft credentials", "Gensoft works with", "Gensoft catalog", "Gensoft database structure", "Gensoft updates fields", "Gensoft send all products", "Gensoft tabs"]
tags: [apps, erp, gensoft, settings, soap]
plan_gates: []
created: 2026-06-25
updated: 2026-06-25
source_count: 3
---

> Part of [[apps-gensoft]]. See the hub for the other aspects (sync model, product matching, reset import, diagnostics).

# Gensoft — settings & tabs

## Purpose

The Settings-tab configuration — the SOAP connection, how the merchant's Gensoft data is structured, which catalogue is imported, the match field, and import/order defaults — plus the app's tab layout.

## Where to find it

Sidebar → Apps → **Gensoft** → **Settings** tab.

## What the merchant can do here

Enter the SOAP connection + credentials, validate them, pick the catalogue and the "Works with" data model, choose the product match field, set new-product / import defaults, and set the order-export options.

## Settings & fields

### Connection (SOAP)

Gensoft connects via a **SOAP web service**. The merchant supplies, with a **Validate credentials** step (unlike most ERPs):

- **WSDL url** (`wsdl_url`) — the Gensoft SOAP / WSDL endpoint (the connection target).
- **Access employee** (`identifier`) and **Access password** (`password`) — auth (a horizontal rule separates the WSDL from this pair). A bad value fails validation with *"Invalid credentials"*; an unreachable endpoint shows *"Could not connect to Gensoft."*

### Catalogue scope

- **Use Gensoft catalog** (`catalog_id`, with `catalog_name` stored alongside) — the single Gensoft catalogue whose articles are imported; the default option is **N/A** (no specific catalogue selected). The Settings tab lists the available catalogues from Gensoft. The configured catalogue is also what the [[apps-gensoft-diagnostics|Diagnostics]] check validates still exists.

### Data model — "Works with" (Database Structure modal)

How the merchant's Gensoft data is structured (`works_with`, default **Batches**), so variants / lots reconcile correctly:

- **Batches** — Gensoft tracks stock by batch.
- **Characteristics** — Gensoft tracks variants by attribute.
- **None of them** — neither.

### Matching + sync direction

- **Compare by** (`compare_by`, default **SKU**) — SKU / Barcode / External ID; the match-field behaviour is on [[apps-gensoft-product-matching]].
- **Action** (`action`, default **Import**) — **Import** (full catalogue import) or **Send orders only** (push orders, don't import the catalogue). See [[apps-gensoft-sync-model]].

### Import behaviour & new-product defaults

- **Fields to be updated on change in the ERP** (`updates`) — the product / variant fields the merchant lets Gensoft overwrite on each sync; fields left out stay CloudCart-controlled.
- **Import images** (`images`) — import each product's images.
- **Without variations** (`simple`) — import each Gensoft product as a **simple** product instead of building a variant product.
- **All imported products require shipping** (`require_shipping`) — marks imports as physical; it also gates the **weight** import — when ON the product's Gensoft weight is imported (else `0`), when OFF no weight is sent. There is **no** separate "default weight" setting.
- **The quantity of each imported product must be tracked** (`quantity_tracking`) and **Continue selling** (`continue_sell`) — inventory defaults for imports.
- **Publish imported products** (`publish_as_active`) / **Publish products as featured** (`publish_as_featured`) / **Publish products as new** (`publish_as_new`) — visibility defaults applied to new imports.
- **Discount** (`discount_id`) — group all Gensoft-flagged products under a CloudCart discount.

### Send-order & sweep options

- **Send all products from the order** (`all_products`) — ON sends **every** order line to Gensoft; OFF sends only products originally imported from Gensoft. Either way, lines that can't be matched by the chosen **Compare by** identifier (missing SKU / barcode / Gensoft ID) are **skipped**, so the rest of the order can still be created in Gensoft (see [[apps-gensoft-product-matching]]).
- **Update in 10 minutes** (`ten_minute_update`) — enables the **paid** 10-minute fast sweep (see [[apps-gensoft-sync-model]]); shown only when `Action` is Import / Update.

## Business rules

### Tab layout

Gensoft is the richest ERP UI: **Overview**, **Settings**, **Status** (Start / Stop), **Diagnostics** (Gensoft-only — see [[apps-gensoft-diagnostics]]), **Products** (imported products + a **Connect** modal to map a product to a Gensoft id manually — see [[apps-gensoft-product-matching]]), **Orders** (a Gensoft-side order-tracking table — which orders pushed, status, errors), and **Import history**.

## Related

- [[apps-gensoft]] — hub.
- [[apps-gensoft-product-matching]] — the `compare_by` field + manual Connect modal.
- [[apps-gensoft-sync-model]] — what `Action`, `all_products`, and `ten_minute_update` drive.
- [[apps-gensoft-diagnostics]] — validates the configured catalogue + credentials.

## Open questions

(none)
