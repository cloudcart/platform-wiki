---
type: feature
nav_path: "Apps → GARAN Label → Products"
route_name: apps.garan_label.products
route_path: /admin/apps/garan_label/products
aliases: ["GARAN products", "GARAN records", "GARAN bulk generation", "Print GARAN labels", "The product has no vendor", "GARAN requires a Brand/Trademark", "GARAN requires a model identifier", "Етикет GARAN за продукт", "Отпечатай етикети GARAN", "Масово GARAN"]
tags: [apps, compliance, products, guarantee, printing, bulk]
plan_gates: ["garan_label_quota"]
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[apps-garan-label]]. See the hub for set-up and label display.

# GARAN Label — products, bulk generation and printing

## Purpose

Where guarantees are recorded: one product at a time on the **Products** tab, or many at once on the **Bulk generation** tab, plus printing labels on paper.

## Where to find it

- **Apps → GARAN Label → Products** (`/admin/apps/garan_label/products`): *"Products with a GARAN durability guarantee."*
- **Apps → GARAN Label → Bulk generation** (`/admin/apps/garan_label/bulk`): *"Apply a GARAN guarantee to many products at once by category and/or vendor."*

Both appear after set-up ([[apps-garan-label]]).

## What the merchant can do here

- **Add product**, or edit and delete a record.
- Per row and in bulk: **Print labels**, **Activate**, **Deactivate**, **Delete**.
- Filter by Manufacturer, Category, Model identifier, Guarantee (years), Start date, End date, Has start date, Has end date.
- Run a **New bulk generation** and read the history of runs.

## Settings & fields

### Add product

| Field | Rule |
|---|---|
| **Select product** | The product needs a vendor and a SKU or barcode. |
| **Guarantee (years)** | Whole or half years over 2, e.g. 2.5, 3, 3.5. |
| **Model identifier** | SKU or barcode, defaulting to the app's setting. |
| **Validity period (optional)** | Under **Advanced settings**. Start and end date. |

Refusals:

- *"The commercial guarantee must be a whole or half year over 2 (e.g. 2.5, 3, 3.5 years)"*
- *"The product has no vendor — GARAN requires a Brand/Trademark"*
- *"The product has no SKU or barcode — GARAN requires a model identifier"*
- *"End date must be on or after the start date"*

### New bulk generation

**Filter products** by **Category** and **Vendor**, then **GARAN guarantee**: **Guarantee (years)**, **Model identifier**, and under **Advanced settings** the **Validity period (optional)**. A preview says *"This will affect {count} products."*

Over the limit it refuses: *"This would create {new} new records and exceed your plan limit of {limit} ({left} left). Upgrade your plan to generate more."*

The history lists Date, Filter, Guarantee (years), Validity period, Products affected and Run by.

## Business rules

### How a guarantee is stored

In months: over 24 and a multiple of 6. The label prints it in years. A guarantee is a set number of years, so a lifetime guarantee does not get a GARAN record.

### Printing

**Print labels** opens an A4 sheet of labels from the selected rows or a filter, in colour or black and white, up to 500 labels. Beyond that: *"Showing the first:shown of:total — refine the filter to print the rest."* / *"Показани са първите:shown от:total — стеснете филтъра, за да отпечатате останалите."* The compact badge is an online format and is never printed.

### Imports

ERP imports can write guarantees. A lifetime or invalid value deletes the product's record. Imports over the limit do not fail; they notify: *"Some imported products could not get a GARAN durability label because your plan limit was reached. Upgrade your plan to label more products."*

## Related

- [[apps-garan-label]] — hub.
- [[apps-garan-label-quota]] — how many records a store can hold.
- [[products-vendors]] — the brand on the label.
- [[products-editor]] — the product's SKU and barcode.
- [[erp-integrations]] — the imports that can write guarantees.

## Open questions

None.
