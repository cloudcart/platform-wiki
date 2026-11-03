---
type: feature
nav_path: "Products → Product statuses"
route_name: product-statuses-index
route_path: /admin/products/statuses
aliases: ["Quantity operators", "If the quantity is dropdown", "Buy button action types", "Show as request", "Show as subscribe for quantity"]
tags: [products, statuses, stock, customer-facing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Product statuses — operators & action types

## Purpose

This aspect is the **field catalogue** for the two dropdowns that define a product status: the **8 quantity operators** (the "If the quantity is" dropdown) that decide WHEN the status fires, and the **4 action types** that decide what happens to the customer-facing Buy button.

> Part of [[products-statuses]]. See the hub for the related aspects (list tables, modal, evaluation, side-effects).

## Where to find it

Both dropdowns live inside the Add / Edit modal on the Product statuses screen (Sidebar → Products → **Product statuses**). See [[products-statuses-modal]].

## What the merchant can do here

- Pick a **quantity operator** to make the status fire automatically against the product's stock count (Conditional), or leave it empty for a manual (Non-conditional) status.
- Pick an **action type** to decide whether the Buy button shows, hides, or is replaced.

## Settings & fields

### The 8 quantity operators (the "If the quantity is" dropdown)

The dropdown lists 8 options. Their stored IDs (shown for support reference; the merchant only sees the labels) and dropdown order:

| ID | Label | Triggered when |
|---|---|---|
| 1 | **Equals** | Product quantity exactly matches the value. |
| 2 | **Not equal to** | Product quantity is anything except the value. |
| 3 | **Lower than** | Product quantity is strictly less than the value. |
| 7 | **Lower than or equal** | Product quantity is at or below the value. |
| 4 | **Greater than** | Product quantity is strictly above the value. |
| 8 | **Greater than or equal** | Product quantity is at or above the value. |
| 5 | **Not tracked** | The product has stock tracking turned OFF (doesn't compare against a value — used for products the merchant intentionally doesn't count). |
| 6 | **Continue selling** | The product has "Continue selling when sold out" ON AND its quantity is below its minimum selling quantity (doesn't compare against a value). |

Leave the dropdown EMPTY to make this a **Non-conditional** status (manual assignment only). Operators **Not tracked** (5) and **Continue selling** (6) are non-value operators — the Quantity field is hidden for them (see [[products-statuses-modal]]).

### The 4 action types (the "Actions" dropdown)

| Action | What the customer sees |
|--------|------------------------|
| **Show "Buy" Button** | Normal: the Buy / Add-to-cart button is visible. |
| **Hide "Buy" Button** | Status badge shown, no Buy button. The customer can view the product but not order it. |
| **Show as request** | The Buy button is replaced with a "Request" button (custom text from the Button text field). Triggers a request form — typical for bespoke / quote-on-demand items. |
| **Show as subscribe for quantity** | The Buy button is replaced with a "Notify me" subscription button. The customer enters their email and gets notified when stock returns. Backed by the back-in-stock subscription system at [[products-missing-product]]. |

For the **Show as request** and **Show as subscribe for quantity** actions, a **Button text** field appears in the modal to set the substitute button's label.

## Business rules

### "Continue selling" pairs with the oversell flag

The **Continue selling** operator is the way merchants who allow oversell (per the [[products-inventory]] "Continue selling when sold out" flag) display a special status when a product goes below its minimum selling quantity. Without a rule using this operator, customers see no indication that the product is technically oversold.

### "Show as subscribe" connects to back-in-stock email

When a status uses **Show as subscribe for quantity**, the storefront button collects customer emails. When stock returns (the product becomes in-stock again), the platform sends a back-in-stock notification email to all subscribers and clears the subscription. Subscriptions are managed at [[products-missing-product]].

### "Show as request" depends on the Request app

The **Show as request** action requires the Request app (or a similar inquiry-form app) to be installed. Without it, the request button submits to a default contact form OR shows an error.

## Related

- [[products-statuses]] — hub.
- [[products-statuses-modal]] — where these two dropdowns appear.
- [[products-statuses-evaluation]] — how a chosen operator is matched against variant stock at storefront time.
- [[products-inventory]] — the "Continue selling when sold out" flag.
- [[products-missing-product]] — back-in-stock subscribers (the "Show as subscribe" target).
- [[product-status-actions-buy-button]] — the data-model view of the action types.

## Open questions

None.
