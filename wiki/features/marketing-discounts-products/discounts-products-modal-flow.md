---
type: feature
nav_path: "Marketing → Discounts → Products → Modal flow"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Discount product modal", "Add product to discount modal", "Edit product discount prices modal", "Common price vs Multiple price", "Product picker for Fixed discount", "Модал за продукт в отстъпка", "Обща цена / Множество цени"]
tags: [marketing, discounts, fixed, products, modal, product-picker, pricing-mode]
plan_gates: ["discount_fixed"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Discount product modal — Add / Edit flow

> Part of [[marketing-discounts-products]]. See the hub for the list view, fields reference, save semantics, and business rules.

## Purpose

The **Discount product modal** is the merchant's single tool to attach a new product to the Fixed discount or to edit the per-variant prices of an existing product on the discount. It is one modal serving both Add and Edit modes, with the pricing-mode radio adapting to single- vs multi-variant products. This page documents the merchant-visible **sequence** of opening, picking, editing, and saving — the field-level reference is on [[discounts-products-fields]] and the backend save semantics are on [[discounts-products-save-replace]].

## Where to find it

Marketing → Discounts → (click **Products** on a Fixed-type discount row) → **+ Add product** opens the modal in Add mode. Clicking any row's product name or thumbnail opens it in Edit mode. The modal is `CcModal` size `xl`; backdrop + Esc are disabled while a save is in flight.

## What the merchant can do here

### Add mode (opening the modal via "+ Add product")

1. **Product picker step** — a single CcSelect querying `/admin/api/core/products/search`. The merchant types a product name and picks one. On select, the modal fetches the product's variants. The picker **cannot be cleared** once a product is chosen (`can-clear=false`) — the merchant has to close the modal and re-open to start fresh.
2. **Pricing mode radio** (appears only when the product has multiple variants OR `type === 'multiple'`):
   - **Common price** (`single`) — one New-price input shared by all variants. Defaults to `single` in Add mode.
   - **Multiple price** (`multiple`) — one New-price input per variant.
3. **Pricing table** renders one of three variants:
   - **`tableSimple`** — single-variant products. Columns: Price in store (read-only) + New price (currency input). On mobile (≤ 768px), an additional name row appears at the top.
   - **`tableMultipleCommonPrice`** — multi-variant + Common price. Shows only the first variant's row; the New price entered there is broadcast to all variants on save.
   - **`tableMultipleMultiplePrice`** — multi-variant + Multiple price. Each variant on its own row: **Variant options** (e.g., "Red / XL / Cotton" joined from `v1`/`v2`/`v3`) + **Price in store** + **New price**.
4. **Save** — see *Save sequence* below.

### Edit mode (opening the modal by clicking a row)

1. **Edit-mode header** — instead of the picker, the modal shows the existing product's thumbnail (64×64px, with the `noImages.150x150` fallback) and name as an `<h5>` header.
2. **Pre-fetch existing prices** — calls `apiMarketingDiscounts.getProductDiscountById` to load each variant's current `discount_price` from the saved rows. The modal **auto-detects** whether all variant prices are equal (sets pricing mode to `single`) or differ (sets it to `multiple`).
3. The pricing-mode radio + pricing table render the same way as Add mode, pre-filled.
4. **Save** — see *Save sequence* below.

### Save sequence

- Modal validates the inputs (see [[discounts-products-fields]] for the per-field rules).
- Sends an array `[{ product_id, variant_id, price_in_cents }, ...]`.
  - In **Common price** mode, the first variant's New price is broadcast to all variants in the payload.
  - In **Multiple price** mode, each variant's own input is sent.
- Backend route: `createProductDiscount` (Add) / `updateProductDiscount` (Edit).
- On success: toast *"Saved successfully"*, modal closes, list refetches.
- On error: toast surfaces the validation message from the backend (see [[discounts-products-fields]] for the catalogue of error strings).

### Close cleanup

Closing the modal (X / backdrop / Esc, when not saving) resets all internal state: `discountProductData = null`, `productId = null`, `product = null`, `differentPrices = 'single'`. Re-opening starts fresh — no leakage from the previous session.

## Settings & fields

### Modal field reference (summary — see [[discounts-products-fields]] for full validation)

| Field | Add mode | Edit mode |
|-------|---------|----------|
| **Product picker** | Required CcSelect | (not shown; product header instead) |
| **Pricing mode radio** | Appears for multi-variant products; defaults `single` | Appears for multi-variant products; auto-set from existing prices |
| **Price in store** | Read-only column | Read-only column |
| **New price** | Per variant or shared per pricing mode | Per variant or shared per pricing mode (pre-filled) |
| **Variant options** | Read-only column (multi-variant + Multiple mode only) | Read-only column (multi-variant + Multiple mode only) |

### Modal toast strings

- Save success → *"Saved successfully"*.
- Status toggle (from the list) → *"Status changed successfully"*.
- Remove (from the list) → *"Removed successfully"*.

## Business rules

- **Single source of truth for pricing data.** The list and the modal both read from the same per-product `getProductDiscountById` endpoint, so the merchant always sees the same data in both UIs without a separate per-variant fetch.
- **Pricing-mode radio appears only when meaningful.** Single-variant products bypass the radio entirely and render `tableSimple` directly. Multi-variant products get the radio so the merchant chooses between one shared price or per-variant pricing.
- **Pricing mode in Edit is detected, not stored.** The modal infers `single` vs `multiple` by comparing the existing per-variant prices; there is no "pricing mode" column on the discount row itself.
- **Common price broadcasts at save, not at edit.** Even in Common mode, the backend receives one entry per variant (all with the same price). The "Common" UI is purely a convenience — the storage is always per-variant. See [[discounts-products-save-replace]].
- **The picker only returns active products.** `/admin/api/core/products/search` scopes by default to active / published products. Disabled or unpublished products won't appear — activate the product first, then add it to the Fixed discount.
- **Cannot add a product already on this discount.** The validator rejects with *"Variant already exists in discount. Variant ID: <id>"* in Add mode. To change prices on a product already attached, click the row to open Edit mode.

## Related

- [[marketing-discounts-products]] — hub.
- [[discounts-products-list-view]] — opens this modal on row click or **+ Add product**.
- [[discounts-products-fields]] — full field-by-field validation rules and error messages.
- [[discounts-products-save-replace]] — backend save flow, the full-replace semantics, and the events fired.
- [[marketing-discounts-fixed]] — MSRP mode (when active, the modal shows the extra MSRP column).
- [[variants-model]] — the **Variant options** column joins the variant's parameter labels.

## Open questions

No outstanding questions.
