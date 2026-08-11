---
type: feature
nav_path: "Products → Product statuses"
route_name: product-statuses-index
route_path: /admin/products/statuses
aliases: ["Add product status modal", "Edit product status modal", "Status modal field visibility", "Continue selling alert"]
tags: [products, statuses, stock, customer-facing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Product statuses — the Add / Edit modal

## Purpose

This aspect documents the **Add / Edit modal** the merchant uses to create or change a single product status: its layout, the dynamic show/hide rules for fields, the Save-enable condition, and the extra quantity-value minimums it enforces.

> Part of [[products-statuses]]. See the hub for the related aspects (list tables, operators/actions, evaluation, side-effects).

## Where to find it

The modal opens from the Product statuses list (Sidebar → Products → **Product statuses**) — from the Add button to create, or by clicking an existing row to edit.

## What the merchant can do here

- Create a new status, or edit an existing one, in a single modal.
- Set the **Status name** (required), choose a **quantity operator** and **Quantity** value (for Conditional), pick an **Actions** type, and set a **Button text** for substitute buttons.
- Leave the operator empty to keep the status **Non-conditional**.

## Settings & fields

The modal opens as an `lg`-sized `CcModal`. The title is *"Add product status"* on create, *"Edit product status"* on edit. On open for edit, the modal fetches the full status record (so the row data is fresh) and shows a loader until the response arrives. There is a single **General settings** card.

### Save-enable rule

The Save button stays **disabled until Status name is filled**. Status name is the only hard requirement to save.

### Fields

- **Status name** (required) — what the customer sees on the storefront.
- **If the quantity is** — the quantity-operator dropdown (searchable, can-clear OFF). 8 options; leave EMPTY to make this a Non-conditional status. Full operator catalogue: [[products-statuses-operators-actions]].
- **Quantity** — the numeric value to compare against.
- **Actions** — what happens to the Buy button (4 options). See [[products-statuses-operators-actions]].
- **Button text** — custom label for a substitute button.

### Dynamic field visibility

The modal hides/shows fields based on the operator + action choices:

- The **Quantity** input is hidden when the operator is empty (Non-conditional) OR is **Not tracked** OR **Continue selling** — i.e., the non-value operators.
- The **Button text** input only appears when Actions = **Show as request** OR **Show as subscribe for quantity**.
- The **Continue selling alert** banner only appears when the operator is **Continue selling**.

A single modal handles both Conditional and Non-conditional statuses — the choice is implicit in whether a quantity operator is set. The form **clears the Quantity field automatically** whenever the operator is switched to one of the non-value operators, so the merchant never accidentally saves a leftover number.

### The Continue selling alert

When the operator is **Continue selling**, a warning-styled info banner appears:

*"This status will be visible in cases where the product has the 'Continue Selling' option, and the quantity of the variation is less than its minimum selling quantity."*

This tells the merchant the rule fires specifically when stock is below the variant's minimum selling quantity AND the product allows oversell. See [[products-inventory]] for the "Continue selling when sold out" flag.

### Quantity-value minimums

For certain operator + status-type combinations, the modal enforces extra minimums on **Quantity** (in addition to "required") so the rule actually triggers somewhere:

- **Equals** (with type `in_stock`) — Quantity must be ≥ **1**.
- **Lower than** (with type `in_stock`) — Quantity must be ≥ **2** (so the rule triggers at qty 1).
- **Lower than or equal** (with type `in_stock`) — Quantity must be ≥ **1**.

The check is skipped for other type/operator combinations, where zero-quantity comparisons make sense.

## Business rules

### Implicit normalisations on save

The modal's choices translate into normalised stored values when the merchant saves — for example an empty operator becomes the Non-conditional sentinel, the non-value operators force Quantity to NULL, and a non-substitute action forces Button text to NULL. The full list of save-time normalisations (and the storefront-cache + delete-cascade side effects) is documented in [[products-statuses-side-effects]].

## Related

- [[products-statuses]] — hub.
- [[products-statuses-operators-actions]] — the operators and actions selected in this modal.
- [[products-statuses-list-tables]] — the list the modal opens from.
- [[products-statuses-side-effects]] — what saving does behind the scenes.
- [[products-inventory]] — "Continue selling when sold out" flag tied to the Continue-selling alert.

## Open questions

None.
