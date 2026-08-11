---
type: feature
nav_path: "Apps → Google Shopping → Attributes (Mappings)"
route_name: apps.google_shopping.attributes
route_path: /admin/apps/google_shopping/attributes
aliases: ["Google Shopping Attributes", "GMC attribute mapping", "Google Shopping Mappings"]
tags: [apps, google, shopping, attributes, mapping]
plan_gates: ["google_shopping"]
created: 2026-05-21
updated: 2026-06-11
source_count: 2
---
# Google Shopping → Attributes (Mappings)

> Part of [[apps-google-shopping]]. See the hub for the other aspects (settings, products, status, auto-sync, feed formatter, batch upload).

## Purpose

The **Attributes** tab is where the merchant maps **CloudCart product fields to Google Merchant Center attributes**. Google's taxonomy is category-driven: different categories require different attributes (Color + Size for apparel, GTIN + MPN for electronics, etc.). Without complete mapping, Google rejects products with "missing required attribute" disapprovals, which surface in [[apps-google-shopping-products]] and [[apps-google-shopping-status]].

Important: only a small set of Google attributes are actually applied to the feed (see Business rules). Mapping any other attribute has no effect even though it appears in the picker.

## Where to find it

Sidebar → Apps → Google Shopping → **Attributes tab**. Route: `/admin/apps/google_shopping/attributes`.

## What the merchant can do here

The tab shows a data table of existing mappings, one row per Google attribute, with the Google attribute name and a **Delete** action.

- **+ Add parameter** — opens the Select Parameters slide-over to create a new mapping (see Settings & fields).
- **Click an existing row's name** — opens the same slide-over to edit that mapping's source/values (the target Google attribute itself cannot be changed when editing — delete and re-add to retarget).
- **Delete** — removes a mapping after a confirmation dialog; toast *"Deleted successfully"*.

What the merchant CANNOT do here:
- Map to a Google attribute that isn't in Google's taxonomy (the taxonomy is closed; no custom Google attributes).
- Map the same Google attribute more than once (one source per attribute — saving replaces any prior mapping).
- Bulk-import mappings — there is no CSV / JSON import; each mapping is entered one at a time.
- Set `size_system` here — it is a store-wide value set on the [[apps-google-shopping-settings]] tab, deliberately excluded from this list.

## Settings & fields

### Select Parameters slide-over (Add / Edit)

An extra-large right-side slide-over with a **Close** and **Save** button in the header.

1. **Select parameters** — single-select autocomplete to pick the Google attribute (e.g., `google_product_category`, `color`, `condition`). Disabled when editing an existing row.
2. After picking the attribute, the form adapts to that attribute's type:
   - **Enum attributes** (fixed Google value list — e.g., `condition`, `age_group`, `gender`): one row per Google value, each with a **Type** dropdown (`Parameter` = variant parameter option, `Attribute` = category property option) and a **Value** autocomplete. The merchant maps each Google value to a CloudCart option. Several CloudCart values may map to one Google value (e.g., "Brand new" + "New with tags" → Google `new`).
   - **Free-text attributes** (e.g., `color`, `material`): one **Select type** dropdown (`Parameter` / `Attribute`) + one autocomplete for the CloudCart parameter or property. The value sent to Google is taken from each product's actual variant/property value.
3. **Save** — toast *"You have successfully saved your changes"*. Field-level errors appear under the relevant dropdown.

### Source types

A mapping points at one of four CloudCart sources: a **variant parameter**, a **specific variant parameter option**, a **category property**, or a **specific category property option**. Tags and custom fields are NOT selectable here. The **vendor** maps to Google `brand` automatically elsewhere (not on this tab).

### Common Google attributes per category

| Product type | Typically required Google attributes |
|---|---|
| **Apparel & Accessories** | Color, Size, Gender, Age group, Material, Pattern |
| **Electronics** | GTIN, MPN, Brand, Condition |
| **Food, Beverages** | Brand, Nutritional info (varies) |
| **Cars, Vehicles** | Brand, Model, Year |
| **Books, Media** | ISBN / GTIN, Brand, Author |
| **General (all categories)** | google_product_category, item_group_id (for variants) |

(Verify against current Google taxonomy — Google updates periodically.)

## Business rules

### Only a fixed set of mapped attributes actually reaches the feed

This is the most important rule. Even though the picker lists many Google attributes, the integration only applies these:

- **Resolved from a variant parameter OR category property**: `color`, `material`, `pattern`, `size`. For each, the system auto-detects whether the saved source is a variant parameter or a category property and reads the product's matching value — so the merchant may map `color` to a variant parameter named "Color" or to a category property called "Color".
- **Direct setters**: `age_group`, `gender`, `size_type`, `size_system`.

Any other attribute the merchant maps is **not** sent to Google. If a product is disapproved for a required attribute outside this set, mapping it here will not fix it.

### Category-driven requirements

Each Google category has required attributes; products in that category must have them mapped AND populated or Google rejects them. Mappings are catalog-wide — there are no per-category overrides. The merchant cannot map `color` to one property for apparel and a different one for accessories; per-product variation comes from each product's own values, not from the mapping.

### Value mapping only for enum attributes

The per-value mapping (the Values controls) exists only for Google attributes with a fixed enum (`condition`, `age_group`, `gender`, `availability`, etc.). Free-text attributes like `color` store only the source; the value comes from the product itself.

### Save replaces, delete is per attribute

Saving a mapping for a Google attribute first removes any existing mapping for that attribute, then stores the new one — so a re-save overwrites the previous setup for that attribute. Delete removes a single attribute's mapping.

### No automatic suggestions

There is no name-match heuristic — a CloudCart property named "Color" is not auto-linked to Google's `color`. Every mapping is picked manually.

### Taxonomy updates are platform-wide

The list of available Google attributes is maintained centrally by CloudCart. When Google adds attributes, new options simply appear in the picker after the platform updates — there is no in-store alert.

### Side effects on save

The mapping is persisted; products previously rejected for that missing attribute may auto-revalidate on the next push to Google. Standard apps permission scope applies.

## Related

- [[apps-google-shopping]] — Google Shopping hub.
- [[apps-google-shopping-settings]] — OAuth + config, and the store-wide `size_system` setting.
- [[apps-google-shopping-products]] — products consuming these mappings.
- [[apps-google-shopping-status]] — feed status (surfaces disapproval reasons).
- [[products-property]] — CloudCart properties used as sources.
- [[products-variants-options]] — variant parameter options used as sources.
- [[products-vendors]] — vendors auto-mapped to Google `brand`.

## Open questions

(None currently outstanding for this page.)
