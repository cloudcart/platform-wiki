---
type: entity
nav_path: "Entity → Product Option → Scoping & edge cases"
aliases: ["Product Option scoping", "Option attachment scope", "Option category scope", "Option vendor scope", "Option selection scope", "Option file-upload cascade", "Option bundle bypass"]
tags: [catalog, products, options, scoping, edge-cases, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product-option]]. See the hub for the other aspects (attributes, pricing, order-line storage).

# Product Option — Scoping & edge cases

## Identity

How an Option is attached to products beyond the simple per-product case, plus the small set of behavioural edge cases the merchant should know: the File-upload deletion cart cascade, where file-upload caps come from, and the Bundle Required-Option bypass. These are the "gotchas" that don't fit the field schema or the pricing model.

## Aliases

- **Attachment scope** — product / category / vendor / selection breadth of an Option.
- **File-upload cascade** — wiping cart rows when a File Option is deleted.
- **Bundle bypass** — Bundles not prompting for child Required Options.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Attachment scope** | `product` / `category` / `vendor` / `selection` | Determines how broadly the Option attaches: one product, all products in a category, all products of a vendor brand, or a custom multi-pick list of products. |
| **File-upload caps** | n/a — inherited, not per-Option | File-upload Options have no per-Option size or MIME limit; they inherit the store-wide caps from [[settings-files]]. |

## Scoping rules

### Options can be attached at four scopes

Per the validation rule, an Option can be attached at four scopes:

- **`product`** — one product (the basic case).
- **`category`** — all products in a [[category]].
- **`vendor`** — all products of a vendor brand.
- **`selection`** — a custom multi-pick list of products.

Attaching at category / vendor / selection scope is broader than per-product — the merchant doesn't have to re-attach the Option to every product manually. The per-product attachment itself happens on the [[product]] editor; the broader scopes are set on the Option definition.

## Edge cases

### File-upload caps come from store-wide settings

File-upload Options do NOT enforce per-Option size or MIME limits — uploads use the platform's general file-upload caps from [[settings-files]] and the platform's mime-type rules. There is no per-Option override.

### Deleting a File-upload Option cascades to in-progress cart selections

When the merchant deletes a File-upload type Option, the platform also wipes any active **cart-item** rows that reference that Option (the file uploads are dropped from those carts). This prevents customers from checking out with a now-deleted Option's file payload. **Other Option types** do NOT trigger this cart cascade — only the File type does, because the uploaded file is otherwise orphaned in storage. Historical orders are unaffected — the snapshot on the order line stays intact (see [[product-option-entity-order-storage]]).

### Bundles bypass child-product Required Options

Bundles compose pre-selected products only. If a [[bundle|Bundle]] child has Required Options, the Bundle add does NOT prompt the customer to fill them — the Bundle add silently passes through, leaving the Option blank on the resulting order line. Merchants should NOT include a product with Required Options as a Bundle component.

## Where it appears

- [[products-options-overview]] — where the merchant sets the attachment scope and deletes Option definitions (triggering the File cascade).
- [[product]] — per-product attachment via the product editor's Options section.
- [[category]] — category-scope attachment applies the Option to every product in the category.
- [[settings-files]] — the store-wide file-upload caps inherited by File-upload Options.
- [[cart]] — active cart rows wiped when a File-upload Option is deleted.
- [[bundle]] — Bundles bypass their child products' Required Options.

## Related

- [[product-option]] — hub.
- [[product-option-entity-attributes]] — the Required flag whose Bundle bypass is documented here.
- [[product-option-entity-order-storage]] — why historical orders survive a File-Option deletion.
- [[product]] — per-product attachment.
- [[category]] — category-scope attachment.
- [[bundle]] — the Required-Option bypass for Bundle components.
- [[settings-files]] — store-wide file-upload caps.
- [[file-asset]] — the uploaded files dropped from carts on File-Option deletion.

## Open Questions

None.
