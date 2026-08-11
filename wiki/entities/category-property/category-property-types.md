---
type: entity
nav_path: "Entity → Category Property → Types"
aliases: ["Category Property types", "Checkbox vs Range property", "Property type lock", "Property type conversion", "dec_points slider step"]
tags: [catalog, products, properties, types, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[category-property]]. See the hub for the other aspects (attributes, business rules, storefront, API).

# Category Property — Types

## Identity

The **type** of a [[category-property|Category Property]] decides how the merchant fills in a per-product value and how the customer narrows by it on the storefront. Two types are merchant-creatable — **Checkbox** (discrete categorical values) and **Range** (continuous numeric values) — and the choice is **locked once products use the Property**. This page documents the two creatable types, the two additional types the data layer accepts but the wizard never exposes, the retro-conversion rule, and how `dec_points` drives the Range slider step.

## Aliases

- **Checkbox vs Range property** — the two creatable types.
- **Property type lock** — the locked-after-creation rule.
- **Property type conversion** — the (limited) Checkbox → Range migration.
- **dec_points slider step** — how decimal places derive the Range slider step.

## Key Attributes

| Type | Merchant-creatable? | What the customer sees | Per-product value |
|------|---------------------|------------------------|-------------------|
| **Checkbox** (`checkbox`) | Yes (wizard default) | A list of filter checkboxes (Color: Red / Blue / Green) | The merchant picks one (or more) of the Property's discrete option values |
| **Range** (`range`) | Yes | A slider with min / max (Screen size: 5.0–7.0 inches) | The merchant types a numeric value per product |
| **Select** (`select`) | No — data layer only | n/a (no Vue management UI) | Records can exist from legacy / import paths |
| **Radio** (`radio`) | No — data layer only | n/a (no Vue management UI) | Records can exist from legacy / import paths |

**Only two Property types are merchant-creatable:** `checkbox` (discrete categorical) and `range` (continuous numeric). The platform's data layer accepts two additional types — `select` and `radio` — but the wizard does not expose them; records of those types can exist from legacy or import paths, but new properties always default to `checkbox`. Treat the wizard's two-option choice as authoritative for new creation. JSON-API v2 reads / writes all four — but new API-created properties should default to `checkbox` or `range` to match the admin edit surface (see [[category-property-api]]).

## Type is locked after creation

Once a Property exists and products carry values for it, the **type cannot be switched** in the wizard — changing means creating a new Property and migrating products to it. The only conversion the platform permits is a narrow one (below), and only while the Property has no products yet.

**Range type retro-conversion is blocked when non-numeric values exist:** changing an existing Property from Checkbox to Range (allowed only if the Property has no products yet — see "Type is locked" above) fails validation if ANY existing option value is non-numeric, with the error *"There are values to the property which are not a number"*. So a Property with values "Cotton, Polyester" cannot become a Range property without first clearing those values. The same validation enforces on the JSON-API v2 write path.

## Range slider step (`dec_points`)

For Range Properties, `dec_points` controls how many decimals are stored / displayed and **auto-derives the slider step**:

| `dec_points` | Slider step | Example display |
|--------------|-------------|-----------------|
| `0` | `1` | 5–7 inches |
| `1` | `0.1` | 5.0–7.0 inches |
| `2` | `0.01` | 5.00–7.00 inches |

`dec_points` default is **2 when stored as NULL**. There is no manual step-override exposed in admin — the step always follows from `dec_points`. The slider's actual **min / max is auto-computed at runtime** from the per-product values present in the active category — there is no merchant-set fixed bound (confirmed against code paths).

## Where it appears

- [[products-property]] — the wizard's type selector (step 1) and the type-locked behaviour on edit.
- [[products-products]] — the per-product value input is a checkbox picker (Checkbox) or a number field (Range).
- Storefront category-page filter sidebar — Checkbox renders as checkboxes, Range as a slider. See [[category-property-storefront]].
- [[api-properties]] — JSON-API v2 reads / writes all four types but new records should be `checkbox` / `range`.

## Related

- [[category-property]] — hub.
- [[category-property-attributes]] — `type`, `options_list`, `dec_points` field definitions.
- [[category-property-business-rules]] — the broader validation set (length caps, uniqueness, delete blocks).
- [[category-property-storefront]] — how Checkbox vs Range render for the customer.
- [[category-property-api]] — the type-surface gap on the JSON-API v2 path.

## Open Questions

- ⏸️ Whether **Range Properties** support a fixed merchant-defined min/max (e.g., always 5–10 inches): code paths confirm runtime auto-min/max from the actual per-product values — no merchant-set fixed bounds.
