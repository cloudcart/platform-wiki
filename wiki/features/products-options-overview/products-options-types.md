---
type: feature
nav_path: "Products → Options → Add / Edit → Field type"
route_name: apps.product_options.edit
route_path: /admin/products/options/:type/:id?
aliases: ["Product option types", "Option field types", "Option input types", "Видове опции"]
tags: [apps, products, options, customisation]
plan_gates: ["product_options"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[products-options-overview]]. See the hub for the other aspects (pricing, assignment, order handling).

# Product Options — field types

## Purpose

Lets the merchant choose **how the customer enters or picks** an option's value on the storefront product page. The **Field type** is selected in the General settings card of the Add / Edit option form. It determines the storefront input widget, which extra price-impact controls appear, and whether the option needs a list of pre-defined values.

## Where to find it

Sidebar → Products → **Product options** (*Продуктови опции*) → **+ Create new option** (or edit an existing one) → **General settings** card → **Field type** dropdown.

## What the merchant can do here

- Pick one of 9 input types, grouped into four families in the dropdown.
- For Select-group types, build a list of values (Name + Amount + optional image per row).
- For measure types (length / square), pick the unit the price is set for and the unit the customer enters in.

## Settings & fields

The **Field type** dropdown is a grouped picker — 9 types across 4 groups:

| Group | Type | Storefront UI | Notes |
|-------|------|---------------|-------|
| **Select** | **radio** | Visible radio buttons | Requires at least one value. |
| **Select** | **select** | Dropdown menu | Requires at least one value. |
| **Select** | **checkbox** | Toggle / multi-select | Requires at least one value. |
| **Select** | **image** ("Photo") | Customer picks one image from a merchant-defined gallery | Each value has its own image + price impact. Single selection from multiple options with image preview. |
| **Text** | **text** | Single-line text input | For names, engraving. |
| **Text** | **textarea** | Multi-line text input | For longer messages, gift notes. |
| **File** | **file** | Customer uploads one file | pdf, doc, jpeg, jpg, png, gif, tiff, zip or rar, up to 25 MB; other files are refused when adding to cart. Deleting a file-type option also deletes past uploads — see [[products-options-order-handling]]. |
| **Other** | **length** (Length) | One number field, in the option unit | Built-to-measure (e.g. per metre of cable). |
| **Other** | **square** (Square) | Two number fields, length × width, in the option unit | Priced per area (e.g. per m²). |

A **weight** type exists in the platform's data but the form does not offer it; an option created with it earlier keeps working (verify).

For the Select-group types (radio / select / checkbox / image), the **Values editor** appears: per-value rows with Name + Amount + (optional) Image, each with a delete button and a "+" to add rows.

## Business rules

### Field type is LOCKED on edit

Once an option is created, the **Field type** select is **disabled** — the type cannot be changed afterwards. To switch types, the merchant must delete the option and recreate it. This is because the type determines the value shape and price-impact controls.

### Value-required rule

A list of at least one value is **required** when the type is `select`, `radio`, or `checkbox`. Each value's Name is required (max 191 chars). Without a value, the save is rejected. Text / textarea / file carry a single price for the option; measure types carry none.

### Measure types behave differently from the rest

A `length` or `square` option has **no price of its own**: it scales the product's price (the chosen variant's price is the price per unit) by the size the customer enters, and every unit in the cart is charged that way. Formula, units and minimums: [[products-options-pricing]].

### The image type is not a variant

The image ("Photo") type lets the customer pick from a gallery of pictures the merchant defines on the option — it is still a customisation of one stock unit, NOT a variant. It does not split stock; see [[inventory-variant-model]].

## Related

- [[products-options-overview]] — hub.
- [[products-options-pricing]] — the per-type price-impact controls.
- [[products-options-assignment]] — which products show the option.
- [[products-variants-options]] — DISTINCT concept (stock-determining choices).
- [[product-option]] — the underlying option entity.

## Open questions

None.
