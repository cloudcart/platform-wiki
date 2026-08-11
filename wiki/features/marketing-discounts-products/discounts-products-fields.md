---
type: feature
nav_path: "Marketing → Discounts → Products → Fields & validation"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Discount product fields", "Discount product validation", "Discount product error messages", "Price must be at least 1", "Invalid MSRP for discount", "Variant already exists in discount", "Полета на отстъпката за продукт", "Грешки при запис на отстъпка"]
tags: [marketing, discounts, fixed, products, fields, validation, errors]
plan_gates: ["discount_fixed"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Discount products — fields, validation, error messages

> Part of [[marketing-discounts-products]]. See the hub for the list view, modal flow, save semantics, and business rules.

## Purpose

This page is the **field-by-field reference** for the Discount products page and its modal — every list column, filter, sort key, bulk-action label, modal input, validation rule, error message, and toast string. Use this as the lookup when a merchant ticket quotes a verbatim message ("*Variant already exists in discount*", "*Price must be at least 1*", etc.) or asks "what does this column show".

## Where to find it

Marketing → Discounts → (click **Products** on a Fixed-type discount row). The list and its modal both live at `/admin/marketing-new/discounts/products/:id`.

## What the merchant can do here

This page is a reference page — the interactions are described on [[discounts-products-list-view]] and [[discounts-products-modal-flow]]. The merchant lands here to look up which fields exist, what they accept, and which validation errors map to which inputs.

## Settings & fields

### List columns

| Column | What it shows |
|--------|---------------|
| **Product Name** | Product image thumbnail + name. Image links to the storefront page (tooltip *"View in store"*). Name link opens the edit modal. |
| **Price** | Two lines, formatted via `moneyFormat`: top line = original price (struck-through) and the new fixed price; second line shows the EUR-to-EUR dual display when EUR-display is active for the store. |
| **Active** | Per-row toggle — green = active, grey = inactive. |
| (Remove) | Per-row remove action — immediately deletes the product from the discount. |

### List filters

| Filter | Options |
|--------|---------|
| **Active** | Yes / No |

### List sorting

Sortable columns: **Price** (ascending / descending), **Active**.

### List bulk actions

| Action key | Label | Effect |
|------------|-------|--------|
| `active` | *"Set status active"* | Toggles selected products' attachment to active. |
| `unactive` | *"Set status unactive"* | Toggles selected products' attachment to inactive. |
| `delete` | (Default delete) | Removes selected products from the discount. |

### Discount product modal — input fields

| Field | What it does | Validation |
|-------|--------------|------------|
| **Product** (Add mode only) | Searchable product picker — types product name, selects one. | Required when adding; once selected, the modal fetches the product's variants. The picker only returns active products. |
| **Pricing type** (multi-variant products only) | Radio: **Common price** (`single`) or **Multiple price** (`multiple`). | Defaults to `single` in Add mode; in Edit mode, auto-detected based on whether all existing per-variant prices are equal (`single`) or differ (`multiple`). |
| **Price in store** | Read-only — shows the variant's current catalog price. | n/a |
| **New price** (per variant or shared) | The fixed price the merchant wants to apply. Entered as decimal EUR; converted to integer cents on save. | Required, integer (in cents), strictly less than the variant's catalog price; must be at least 1 cent. |
| **Variant options** (multi-variant + Multiple-price mode) | Read-only — concatenation of the variant's property values (e.g., "S / Red", "M / Blue"). | n/a |
| **MSRP** (Add / Edit, only when parent discount has MSRP mode on) | Per-variant MSRP override; integer in cents. | Must be greater than the fixed price (otherwise *"Invalid MSRP"* fires). See [[marketing-discounts-fixed]] for the broader MSRP rule. |

### Error messages (verbatim)

| Message | Triggered by |
|---------|--------------|
| *"Price is required"* | Missing `price` on a variant entry. |
| *"Price must be at least 1 and less than <variant.price>"* | `price < 1` OR `price >= variant.price`. The validator runs per variant. The catalog price interpolates as cents. |
| *"Variant is required"* | Missing `variant_id` on an entry. |
| *"Variant must be an integer"* | Non-integer `variant_id`. |
| *"Variant does not exist"* | `variant_id` not found in the catalog. |
| *"Variant already exists in discount. Variant ID: <id>"* | Add mode: the variant is already attached to this Fixed discount. (See [[marketing-discounts-fixed]] for the broader "one Fixed discount per product across the store" rule.) |
| *"You cannot update a product other than the one you selected"* | Edit mode: the submitted `product_id` doesn't match the route's `product_id`. |
| *"Invalid MSRP"* | MSRP-mode parent discount: MSRP ≤ fixed price. |
| *"threshold has invalid value"* (parent discount) | Not raised here, but the parent discount drives this; mentioned for cross-reference. |

### Toast strings (verbatim)

| Toast | Triggered by |
|-------|--------------|
| *"Saved successfully"* | Modal save success. |
| *"Status changed successfully"* | Per-row inline toggle. |
| *"Status set to active successfully"* | Bulk *"Set status active"* success. |
| *"Status set to unactive successfully"* | Bulk *"Set status unactive"* success. |
| *"Removed successfully"* | Single-row remove success. |
| *"Error while setting the status"* | Bulk status-toggle failure. |

## Business rules

- **Validation is per-variant inside the modal save.** Each entry in the submitted array is checked independently — one bad variant's error message identifies the offending row by id.
- **Price is stored as integer cents.** The modal accepts decimal EUR and converts at save; the backend expects and persists integers (cents). Display in the list divides by 100.
- **`fixed_price >= variant.price` is **silently dropped, not errored** during save** — the validator fires only on `< 1`; the `< variant.price` check is enforced as a *skip* in the insert pass. The merchant sees the saved discount with FEWER variants than they entered. See [[discounts-products-business-rules]].
- **Validation order: required → integer → range → uniqueness.** The first failure short-circuits the response with that error message; the merchant doesn't see a list of all failures at once.

## Related

- [[marketing-discounts-products]] — hub.
- [[discounts-products-list-view]] — interactions over the list columns / filters / sort / bulk actions described here.
- [[discounts-products-modal-flow]] — the Add / Edit sequence that uses the modal inputs described here.
- [[discounts-products-save-replace]] — the backend save flow where the validation runs.
- [[marketing-discounts-fixed]] — parent discount; defines MSRP mode and the "one Fixed discount per product" rule.

## Open questions

No outstanding questions.
