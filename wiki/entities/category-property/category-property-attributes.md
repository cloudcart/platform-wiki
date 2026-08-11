---
type: entity
nav_path: "Entity → Category Property → Key attributes"
aliases: ["Category Property attributes", "Property fields", "Property record fields", "Property definition schema"]
tags: [catalog, products, properties, attributes, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[category-property]]. See the hub for the other aspects (types, business rules, storefront, API).

# Category Property — Key attributes

## Identity

The full per-field schema for the [[category-property|Category Property]] definition — every attribute the merchant configures across the 3-step wizard on [[products-property]] (details → categories → values), with its purpose, allowed values, and notes. This is the page the AI Assistant cites when a merchant asks *"What goes in field X when I create a Property?"* or *"What's the difference between Use as filter and Active?"*. The structural Property record is documented here; how the values behave for the customer is on [[category-property-storefront]], and the validation / lifecycle rules are on [[category-property-business-rules]].

## Aliases

- **Category Property attributes** / **Property fields** — the per-record field definitions.
- **Property record fields** / **Property definition schema** — the structural columns that define a Property (as opposed to the per-product value that populates it).

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Property name** (`name`) | Required free text | The label shown on the product editor, the storefront filter sidebar, and the product specs table. Translatable per-locale on multilang stores. Max **191 characters** — see [[category-property-business-rules]]. |
| **Option type** (`type`) | Required at create — Checkbox or Range | **Checkbox** = discrete categorical values (Color: Red / Blue / Green). **Range** = continuous numeric values (Screen size: 5.0–7.0 inches). **Type is locked after creation** — see [[category-property-types]]. |
| **Option values** (`options_list`) | Multi-row list (Checkbox type only) | The discrete choices the merchant can assign per product (Red, Blue, Green for a Color Property). Each value can carry an optional image (e.g., colour swatches on the storefront filter). Range Properties skip this — they have no discrete values; the min/max comes from the per-product numeric inputs. |
| **Range decimal places** (`dec_points`) | Integer 0–5 (Range type only) | Controls how many decimals are stored / displayed for the slider (e.g., `1` = 5.0–7.0 inches; `2` = 5.00–7.00; weight might use `2` for 1.25 kg). Slider step derivation lives on [[category-property-types]]. |
| **Categories** (M2M) | Required at create — multi-select | Which [[category]] records this Property is attached to. The Property appears on the product editor for every Product in those Categories. A Property can be attached to many Categories; a Category can carry many Properties. Detaching a Category stops the Property appearing on products in that Category — but does NOT delete the saved per-product values (see [[category-property-business-rules]]). |
| **Use as filter** (`is_visible`) | Toggle | When ON, the Property surfaces in the storefront category-page filter sidebar (customers can narrow by its values). When OFF, the Property is purely descriptive — visible on the product detail page in the specs table, but NOT shown as a filter. See [[category-property-storefront]]. |
| **Active** (`active`) | Toggle | When OFF, the Property is hidden EVERYWHERE — the product editor doesn't show it, the product detail page doesn't show it, the filter sidebar doesn't show it. Soft-disable preserves the per-product values for later reactivation. |
| **Sort priority** (`sort`) | Integer + drag-and-drop reorder | Lower = higher in the storefront filter sidebar AND in the product editor's category-properties section. Drag-reorder on [[products-property]] writes this field. |
| **URL handle** (`url_handle`) | Auto-derived from name, manually editable | The slug used in storefront filter URLs (`/category/electronics?<handle>=red`). Per-Property uniqueness enforced — two Properties cannot share a handle. See [[category-property-business-rules]]. |
| **Category Property image** (`image`) | Optional single image upload | Some themes display this icon next to the Property name on the filter sidebar. Mass-assignment guarded — image must go through the dedicated upload pipeline. |
| **Image dimensions** (`width` / `height` / `max_thumb_size`) | Per-Property pixel dimensions | Apply to all value-images for this Property — all Color swatches in a single Color Property share dimensions. No platform default; the merchant picks the size that fits the storefront theme. |
| **Per-product value** | n/a — set on the [[products-products]] product editor per product | The Property defines the structure; the per-product value is what actually populates the customer-facing spec / filter for that one product. Stored separately from the Property definition. |
| **Products count** (`products_count`) | Read-only | How many products currently have a per-product value for this Property. Shown on the Properties list. Drives the delete-protection block and the click-through to filtered [[products-products]]. |
| **URL handle keyed cache** | n/a — internal cache | The platform caches `url_handle → property_id` for fast storefront filter URL parsing. Invalidated when a Property is created OR when its URL handle changes — see [[category-property-api]] for the cache key. |

The Property record has **no time-windowed visibility** (unlike products, which can be scheduled for publish / unpublish) and has **no `created_at` / `updated_at` audit columns surfaced in the UI**.

## Where it appears

- [[products-property]] — the Add (3-step wizard) / Edit surface where these fields are set.
- [[products-products]] — the product editor's Categories section, where the per-product value is entered.
- [[apps-csv-import]] — CSV imports write to `name`, `type`, `options_list`, and the M2M Categories attachment.
- [[api-properties]] — JSON-API v2 read / write surface for the Property definition.
- [[api-property-options]] — JSON-API v2 surface for the discrete option values.

## Related

- [[category-property]] — hub.
- [[category-property-types]] — Checkbox vs Range, type-locked-after-create, `dec_points` slider-step derivation.
- [[category-property-business-rules]] — name / value / URL-handle length caps + uniqueness, delete-blocked-while-in-use, orphan values on detach.
- [[category-property-storefront]] — how `is_visible` / `active` / the per-product value behave for the customer.
- [[category]] — the Categories the M2M attachment targets.
- [[product]] / [[products-products]] — where the per-product value is set.
- [[settings-files]] — where the Property image + value images live.

## Open Questions

- ⏸️ Whether the **per-Property image dimensions** (`width`, `height`, `max_thumb_size`) are hard-enforced on upload (resize / reject oversize) or merely advisory hints surfaced to the merchant (verify).
