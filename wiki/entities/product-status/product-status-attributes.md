---
type: entity
nav_path: "Entity → Product Status → Attributes"
aliases: ["Product Status fields", "Product Status attributes", "Quantity operators", "Action types", "8 quantity operators", "4 action types", "Button text auto-clear"]
tags: [entity, catalog, products, statuses, fields]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Product Status — Attributes

> Part of [[product-status]]. See the hub for related aspects (Conditional vs Non-conditional, evaluation precedence, action behaviour, lifecycle, storefront rendering).

## Identity

The verbatim **field set** carried by a Product Status row, plus the dropdown values for **quantity operator** and **action type**, plus the two silent-auto-clear rules that fire on save. These are the building blocks every other Product Status aspect references.

## Aliases

- **Product Status fields** / **Product Status attributes** — what shows up in the Add / Edit modal in [[products-statuses]].
- **8 quantity operators** — the `If the quantity is` dropdown.
- **4 action types** — the `Actions` dropdown.

## Key Attributes

A Product Status row carries these fields. The merchant edits them through the Add / Edit modal on [[products-statuses]].

| Field | What the merchant controls | Notes |
|-------|----------------------------|-------|
| **Status name** | Customer-facing label shown on the storefront product card. | Required. E.g., *"In stock"*, *"Out of stock"*, *"Limited stock"*, *"Coming soon"*, *"Request a quote"*. The label is fixed per-store (no theme styling controls here — colour / font / icon / position is theme-driven). |
| **Quantity operator** (`If the quantity is`) | One of 8 operators that triggers the status automatically based on the product's stock count. | Leave EMPTY to make the status **non-conditional** (manual assignment only). See *"8 quantity operators"* below. |
| **Quantity value** | The numeric value to compare against. | Visible only for operators that need a value (Equals, Not equal to, Lower than, Lower than or equal, Greater than, Greater than or equal). |
| **Action type** (`Actions`) | What happens to the customer-facing Buy button when this status applies. | One of 4 values — see *"4 action types"* below. |
| **Button text** | Custom label for the substitute button (Request / Subscribe). | Visible only when the action is *"Show as request"* or *"Show as subscribe for quantity"*. |
| **Sort order / priority** | Drag-and-drop position in the Conditional table. | Higher in the list = higher priority. When multiple Conditional rules match the same product, the topmost rule wins. |
| **Conditional flag** | Derived from whether a quantity operator is set. | If the operator is empty → non-conditional (manual assignment); if set → conditional (auto-applies based on stock). |

### 8 quantity operators (the `If the quantity is` dropdown)

| Operator | Triggered when |
|----------|----------------|
| **Equals** | Product quantity exactly matches the value. |
| **Not equal to** | Product quantity is anything except the value. |
| **Lower than** | Product quantity is strictly less than the value. |
| **Lower than or equal** | Product quantity is at or below the value. |
| **Greater than** | Product quantity is strictly above the value. |
| **Greater than or equal** | Product quantity is at or above the value. |
| **Not tracked** | The product has stock tracking turned OFF (per the `tracking` flag on [[products-inventory]]). Doesn't compare against a value — used for products the merchant intentionally doesn't count. |
| **Continue selling** | The product has the *"Continue selling when sold out"* option ON AND its quantity is below its minimum selling quantity. Doesn't compare against a value. Info banner: *"This status will be visible in cases where the product has the 'Continue Selling' option, and the quantity of the variation is less than its minimum selling quantity."* |

### 4 action types

| Action | What the customer sees |
|--------|------------------------|
| **Show "Buy" Button** | Normal: Buy / Add to cart button is visible. The internal `type` key for this state is `in_stock`. |
| **Hide "Buy" Button** | Status badge shown, no Buy button. Customer can view the product but not order. The internal `type` key for this state is `out_stock`. |
| **Show as request** | Buy button replaced with a *"Request"* button (custom text from the Button text field). Triggers a request / quote form. Typical for bespoke / quote-on-demand items. Requires the Request app (or similar inquiry-form app) to be installed. The internal `type` key is `request`. |
| **Show as subscribe for quantity** | Buy button replaced with a *"Notify me when in stock"* subscription button. Customer enters their email and gets notified when stock returns. Subscriptions managed at [[products-missing-product]]. The internal `type` key is `subscribe`. |

### Button text auto-clears for non-button actions

The `button_text` (custom CTA label) is **stored only when** the action is `request` or `subscribe`. On save, if the merchant picks *"Show Buy"* or *"Hide Buy"* but typed something in Button text, the platform silently NULLs the value on save. Switching from `request` → `subscribe` keeps the text; switching to a Buy/Hide action wipes it.

### Quantity auto-clears for non-quantity operators

When the operator is **Not tracked** or **Continue selling** (the two that don't compare against a number), the `quantity` field is silently NULLed on save regardless of what the merchant typed. The operator picker UI hides the quantity input for those two, but if a value sneaks through via API, the save still drops it.

## Where it appears

- [[products-statuses]] — the Add / Edit modal where each field is configured.
- [[product-status-conditional-vs-non-conditional]] — uses the operator field to split rows into the two tables.
- [[product-status-evaluation-precedence]] — the operator + value + sort order drive which rule applies first.
- [[product-status-actions-buy-button]] — the action type drives storefront Buy-button behaviour.

## Related

- [[product-status]] — hub.
- [[products-statuses]] — taxonomy management screen.
- [[products-inventory]] — `tracking` and `continue_selling` flags referenced by the *"Not tracked"* and *"Continue selling"* operators.
- [[inventory-variant-model]] — the master switches whose values these operators read against.

## Open Questions

None.
