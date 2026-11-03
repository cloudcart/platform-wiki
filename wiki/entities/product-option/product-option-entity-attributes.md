---
type: entity
nav_path: "Entity → Product Option → Attributes"
aliases: ["Product Option attributes", "Product Option fields", "Option input types", "Option supported types", "Option key attributes", "Option storefront name"]
tags: [catalog, products, options, attributes, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product-option]]. See the hub for the other aspects (pricing, order-line storage, scoping + edge cases).

# Product Option — Attributes

## Identity

The merchant-controlled fields on a Product Option definition: what the customer sees (Name, input type, possible values), how the field behaves (Required, Storefront name override, unit symbols), and the two admin-only control flags (`customer_modify`, `system`). This aspect documents the field schema and the complete list of supported input types. The pricing-related attributes (`amount_type`, `apply_over_price_type`, `allow_negative`, `min_square`, per-value modifiers) are catalogued separately in [[product-option-entity-pricing]].

## Aliases

- **Product Option fields** / **Option attributes** — the per-Option inputs the merchant configures.
- **Input type** — the field deciding the storefront control (text box, dropdown, file picker, etc.).
- **Possible values** — the discrete choice list for Select / Radio / Checkbox types.
- **Storefront name** — the customer-facing label override.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** | Required free text | The label the customer reads next to the input on the product page (e.g., *"Engraving text"*, *"Choose your font"*, *"Add gift wrap"*). |
| **Input type** | Required — one of Text / Textarea / Select (dropdown) / Radio / Checkbox / File upload / Image-swatch / Length / Weight / Square | Drives the storefront UI the customer sees and the format of the value stored on the order line (see [[product-option-entity-order-storage]]). Type is picked at create — switching type usually means recreating the Option. |
| **Required** | Boolean toggle | When ON, the storefront blocks the **Add to cart** button until the customer fills the Option. Useful for mandatory choices ("you must pick a font"). When OFF, the customer can leave it blank. See [[checkout-flow]]. |
| **Possible values** (`options_list`) | Multi-line list (Select / Radio / Checkbox types only) | The discrete choices the customer picks from. Text / Textarea / File / measurement types have no value list — the customer types or uploads freely. |
| **Assigned product(s)** | Multi-select on the product editor | The Option is configured here on the Options screen but **attached to specific products** from each [[product]]'s editor. The same Option definition can be reused across many products. Attachment can also be broadened to category / vendor / selection scope — see [[product-option-entity-scoping-and-edge-cases]]. |
| **Customer-submitted value** | n/a — entered by the customer at cart-add time | Stored on the **order line item**, not on the [[product]] or [[customer]] record. Each order can carry different values for the same product. For File-upload Options, the value is a reference to the uploaded [[file-asset]]. See [[product-option-entity-order-storage]]. |
| **Storefront name** | Optional 191-character override of the `name` field | When set, the storefront renders this label instead of the admin-facing `name`. Lets the merchant keep an internal label ("Engraving — sterling silver only") and a customer-facing label ("Engraving"). Max 191 chars. |
| **Customer modify** (`customer_modify`) | Storefront visibility flag | When OFF, the Option exists in the data model but is NOT rendered on the storefront — the merchant uses it for admin / system purposes only. Storefront queries auto-filter on this flag. |
| **System** (`system`) | Internal marker | When ON, the Option is system-managed (created by an app or by the platform itself) and is shielded from manual edits. Merchants typically only see this on options installed by apps. |
| **Product symbol** / **Value symbol** | Per-Option / per-value text decorators | Optional unit symbols rendered alongside the Option name and submitted value on the storefront — e.g., "cm" next to a length input or "kg" next to a weight input. |

## Supported input types (full list)

The validation rule accepts exactly these input types: `text`, `textarea`, `select`, `radio`, `checkbox`, `file`, `image` (image-swatch), `length`, `weight`, `square`.

- **`text` / `textarea`** — free-form customer typing (single line vs multi-line). No value list.
- **`select` / `radio`** — single pick from the `options_list`.
- **`checkbox`** — multi-pick from the `options_list`; per-value price modifiers sum additively (see [[product-option-entity-pricing]]).
- **`file`** — customer uploads a file; the value is a reference to the uploaded [[file-asset]] (see [[product-option-entity-order-storage]]).
- **`image`** — image-swatch picker (the customer picks a visual swatch).
- **`length` / `weight` / `square`** — measurement inputs; the merchant types a value in the configured unit (e.g., "120 cm" for a custom-cut fabric, an area for `square`). These auto-set `per_item = 1` because the merchant typically charges per measured unit — see [[product-option-entity-pricing]].

There is **NO `date` type and NO `multi-checkbox` type** — only the seven listed above plus the three measurement types. The wiki previously listed Multi-checkbox + Date — those are NOT supported.

## Where it appears

- [[products-options-overview]] — the management screen where the merchant sets every field above (Sidebar → Products → Options).
- [[apps-product-options-settings-new]] — the app-level settings sub-page.
- [[product]] — the product editor's Options section, where the Option is attached and the configured input type renders on the storefront product page.
- Storefront product detail page — the Option renders as the form control matching its input type.

## Related

- [[product-option]] — hub.
- [[product-option-entity-pricing]] — the pricing attributes (`amount_type`, `allow_negative`, `min_square`, per-value modifiers) deliberately excluded from the table above.
- [[product-option-entity-order-storage]] — where the customer-submitted value is stored.
- [[product-option-entity-scoping-and-edge-cases]] — broadening attachment beyond a single product.
- [[product]] — Options are attached per-product.
- [[variant]] — DISTINCT concept; Variants split SKUs, Product Options do not.
- [[category-property]] — DISTINCT concept; category-scoped descriptive metadata, not customer-input.
- [[file-asset]] — File-upload Option values reference uploaded assets.
- [[multi-language]] — Option names + possible values can be translated per-locale.

## Open Questions

None.
