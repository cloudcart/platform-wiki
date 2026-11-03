---
type: feature
nav_path: "Apps → OLX → Parameters"
route_name: apps.olx.parameters
route_path: /admin/apps/olx/parameters/:id
aliases: ["OLX Parameters", "OLX parameter mapping", "OLX category parameters"]
tags: [apps, olx, marketplace, parameters, mapping]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# OLX → Parameters

## Purpose

The **Parameters** sub-page is the **second mapping step after [[apps-olx-configuration]]**. Once a CloudCart category is mapped to an OLX category, the merchant arrives here to map CloudCart product PROPERTIES (per [[products-property]]) to OLX's required PARAMETERS for that specific OLX category.

Example: OLX's "Electronics > Phones" category requires parameters Brand, Condition, Memory. CloudCart's matching category has its own properties — Brand (vendor), Condition (custom property), Storage (variant attribute). The merchant maps:
- OLX `brand` parameter ← CloudCart Vendor.
- OLX `condition` parameter ← CloudCart `Condition` property.
- OLX `memory` parameter ← CloudCart `Storage` variant.

Without this mapping, OLX rejects publishes for products in that category with `err.params_not_mapped` (per [[apps-olx]]).

The `:id` URL parameter identifies which category mapping's parameters we're configuring.

For the OLX feature set, see [[apps-olx]].

## Where to find it

Sidebar → Apps → OLX → Configuration → click a mapping → opens this page at `/admin/apps/olx/parameters/{category_mapping_id}`. Route name: `apps.olx.parameters`.

## What the merchant can do here

### Parameter mapping data table

For the selected category mapping, the table lists OLX's required parameters + their current CloudCart mapping:

| Column | Source component |
|---|---|
| **CloudCart source** (`SiteName` / `TableSiteCategoryName`) | The CloudCart property / vendor / variant attribute that maps to the OLX parameter. |
| **OLX parameter** (`OlxName` / `TableOlxCategoryName`) | The OLX-side parameter name (e.g., "Brand", "Condition", "Color"). |
| **Values link** (`TableParameters`) | Link to [[apps-olx-parameters-values]] for per-value mapping. |
| **Actions** | Edit (via `TableEditMapping` modal), Delete (via `TableDelete`). |

### Edit a parameter mapping

`TableEditMapping` modal opens with:
- Dropdown for the CloudCart source (Vendor / Property / Variant attribute / Tag).
- Dropdown for the OLX parameter (auto-populated from OLX's API for this category).
- Save.

After saving, the value-mapping step ([[apps-olx-parameters-values]]) may be required if the parameter has a fixed-value set (e.g., OLX's `condition` parameter only accepts "New" / "Used" / "Refurbished" — the merchant maps which CloudCart property values correspond to each).

### What the merchant CANNOT do here
- Map a CloudCart source to multiple OLX parameters in the same category (1:1 per parameter).
- Skip required parameters — OLX's API rejects the advert.
- Edit OLX's own parameter taxonomy (fetched from OLX's API; read-only).

## Settings & fields

### Per-parameter mapping data

| Field | Notes |
|---|---|
| **category_mapping_id** | The category mapping this parameter belongs to. |
| **olx_parameter_key** | OLX's internal parameter identifier. |
| **olx_parameter_label** | Human-readable label for the merchant. |
| **cloudcart_source_type** | What kind of CloudCart data feeds this parameter — vendor / property / variant / tag. |
| **cloudcart_source_id** | The specific record (property ID, variant attribute ID, etc.). |
| **required** | Whether OLX considers this parameter mandatory. |
| **value_type** | OLX's expected value format (text / number / enum / boolean). |

### Required vs optional parameters

OLX flags some parameters as REQUIRED for the category (without them, publish fails). Others are optional. The Parameters table shows required ones first, typically with a visual indicator.

## Business rules

### Per-category parameter set

Different OLX categories have different parameters. When the merchant changes a category's mapping in [[apps-olx-configuration]], the parameter list here updates to reflect the new category's requirements.

### Enum parameters require value mapping

When OLX's parameter has a fixed value set (`condition` = New/Used/Refurbished), the merchant ALSO needs to map values in [[apps-olx-parameters-values]] — declaring which CloudCart property value corresponds to each OLX value.

### Permission

Standard apps permission scope.

## Related

- [[apps-olx]] — OLX hub.
- [[apps-olx-configuration]] — category mapping (parent step).
- [[apps-olx-parameters-values]] — per-parameter value mapping (next step).
- [[apps-olx-products]] — products published using these mappings.
- [[products-property]] — CloudCart properties referenced as sources.
- [[products-vendors]] — Vendors referenced as Brand parameter source.

## How it works (verified against backend)

### Required parameters only — `state` and `delivery_paid_by` excluded

The listing shows only OLX attributes flagged `required = true`, AND excludes the two parameters `state` (condition: new/used) and `delivery_paid_by` (shipping payer). Those two are not merchant-mapped per product — `state` is hard-coded ("new" for Bulgaria) and `delivery_paid_by` comes from the global Settings tab.

### Parameter source types — Property OR Variant Attribute

Via the `parameter_type` field (`site_parameter` vs `site_attribute`), each OLX parameter is mapped to either a CloudCart **Property** (a category-level fixed attribute like "Color: Red") or a **Variant Attribute** (a variant-level option like Size or Memory). The merchant picks the type AND the specific source in the same modal.

### Removing a parameter mapping cascades to value mappings

Deleting a parameter mapping also deletes all associated value mappings ([[apps-olx-parameters-values]]). When changing the source for an existing parameter, the old value mappings are wiped — the merchant must remap values.

### Parameter list is per-category (not global)

The parameter list shown is scoped to the OLX category from the parent Configuration row. Different OLX categories show different required parameters.

### No "apply to many categories" — each mapping is per-category

There is no bulk mechanism to copy a parameter mapping (for example "Brand ← Vendor") across multiple OLX categories at once. Even if the same parameter appears in 20 different OLX categories with the same intended source, the merchant has to open each category's Parameters page and re-create the mapping individually.

### State / condition attribute is hard-coded per country

The `state` parameter (used by OLX for product condition: New / Used / Refurbished) is NOT exposed in the parameter-mapping UI. The integration hard-codes it:
- Bulgaria (`endpoint_id == 2`): always `"new"`.
- Romania (`endpoint_id == 3`): uses the first value from the attribute's `values` JSON (typically the OLX-default value).

So Bulgarian-stores can ONLY publish products as "new". Used / refurbished goods cannot be advertised via this integration. Romanian stores get OLX's default.

### Delivery_paid_by attribute is sourced from Settings, not Parameters

The `delivery_paid_by` attribute (who pays shipping) is filled from the `shipping_payer_id` setting on [[apps-olx-settings]] — applied to every advert globally. The merchant cannot override it per-category or per-product from the Parameters tab. So all adverts share the same shipping-payer choice.

### Parameter listing excludes `state` and `delivery_paid_by`

The Parameters table queries OLX's required attributes for the category but filters out `state` and `delivery_paid_by` — they are handled elsewhere (hard-coded / Settings). The merchant only maps the parameters they actually have control over: brand, color, size, memory, etc.

## Open questions
