---
type: feature
nav_path: "Apps → OLX → Parameters → Values"
route_name: apps.olx.parameters.values
route_path: /admin/apps/olx/parameters/:id/values/:hash
aliases: ["OLX Values", "OLX parameter values", "OLX value mapping"]
tags: [apps, olx, marketplace, parameters, value-mapping]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# OLX → Parameters → Values

## Purpose

The **Values** sub-page is the **third mapping step** after [[apps-olx-configuration]] (category mapping) and [[apps-olx-parameters]] (parameter mapping). It handles per-VALUE mapping for OLX parameters that have a FIXED enum set.

Example: OLX's `condition` parameter accepts three values: "New" / "Used" / "Refurbished". The merchant's CloudCart `Condition` property might have different value labels: "Brand new" / "Pre-owned" / "Reconditioned". The merchant maps:
- CloudCart "Brand new" → OLX "New".
- CloudCart "Pre-owned" → OLX "Used".
- CloudCart "Reconditioned" → OLX "Refurbished".

Without this mapping, OLX's API rejects the advert because the CloudCart value doesn't match an OLX-accepted value.

URL parameters:
- `:id` — the category mapping ID (from [[apps-olx-configuration]]).
- `:hash` — the parameter hash identifying which specific parameter's values we're mapping.

For the OLX feature set, see [[apps-olx]].

## Where to find it

Sidebar → Apps → OLX → Parameters → click an enum parameter → opens this page at `/admin/apps/olx/parameters/{id}/values/{hash}`. Route name: `apps.olx.parameters.values`.

## What the merchant can do here

### Value mapping data table

For the selected parameter, the table lists OLX's accepted values + their CloudCart mappings:

| Column | Notes |
|---|---|
| **CloudCart value** | The CloudCart property value (free text or selected from a list of detected values). |
| **OLX value** | The OLX-accepted value (from the parameter's enum). |
| **Actions** | Edit, Delete. |

### Add a value mapping

The merchant clicks Add → picks the CloudCart value (autocomplete from existing property values) → picks the OLX value (dropdown from OLX's parameter enum) → saves.

### Edit / Delete

Standard table CRUD actions per row.

### Auto-suggest

The platform may suggest mappings based on string similarity (e.g., CloudCart "New" → OLX "New" auto-match). Verify whether this is implemented.

### What the merchant CANNOT do here
- Map a CloudCart value to multiple OLX values for the same parameter.
- Use a CloudCart value that doesn't exist in any product (the source must be a real value).
- Submit an OLX value that's not in the enum (the dropdown restricts to OLX-accepted values).

## Settings & fields

### Per-value-mapping data

| Field | Notes |
|---|---|
| **parameter_mapping_id** | The parameter mapping this value belongs to. |
| **cloudcart_value** | The source value (text label from CloudCart property / variant). |
| **olx_value_key** | OLX's internal value key. |
| **olx_value_label** | Human-readable OLX value label. |

### Hash-based URL

The `:hash` URL parameter encodes the specific parameter identifier in a stable form (likely a hash of the parameter key + category mapping ID). This lets the platform deep-link to specific value mappings without exposing internal IDs.

## Business rules

### Required for enum parameters

Not all OLX parameters need value mapping — only the ones with a FIXED enum set. Text parameters (free text), numeric parameters (any number), and boolean parameters (true/false) don't need this step.

When the merchant arrives at this page, the platform has already determined the parameter is enum-typed and needs value mapping.

### Unmapped value → publish failure

If a product has a property value that's NOT mapped to an OLX equivalent, the publish for that product fails. The error surfaces in [[apps-olx-products]] (Valid column) and [[apps-olx-history]] (with details).

### Many-to-one is allowed

Multiple CloudCart values CAN map to the SAME OLX value:
- CloudCart "Refurbished" → OLX "Used".
- CloudCart "Pre-owned" → OLX "Used".
- CloudCart "Second-hand" → OLX "Used".

But the reverse (one CloudCart → multiple OLX) is NOT allowed (each CloudCart value picks exactly one OLX target).

### Side effects on save
- Value mapping persisted.
- Existing CloudCart products with unmapped values may suddenly become Valid for OLX publishing.

### Permission
Standard apps permission scope.

## Related

- [[apps-olx]] — OLX hub.
- [[apps-olx-parameters]] — parameter mapping (parent step).
- [[apps-olx-configuration]] — category mapping.
- [[apps-olx-products]] — products that benefit from these mappings.
- [[products-property]] — CloudCart properties that supply values.

## How it works (verified against backend)

### OLX values come from the parameter's `values` array

The dropdown of OLX-accepted values is built from the OLX parameter's `attributes.values` JSON. Each value has a `code` (OLX-internal identifier) and a `label` (human-readable name shown to the merchant). Free-text fields would not have a `values` array — only enum parameters appear here.

### Site value source — Property OR Variant attribute

When the parent parameter mapping has `parameter_type = site_parameter`, the CloudCart side is a variant-attribute option (e.g. Color = Red). When `site_attribute`, it's a property option (e.g. Brand = Nike). The matching value is auto-formatted with the appropriate label.

### Idempotent save — duplicates prevented

Save uses a first-or-create keyed on category + OLX parameter + OLX value + site parameter + site value — the same mapping cannot be saved twice. The merchant can re-save without creating duplicates.

### Each row stores only ONE value pairing

The table stores tuples of (category, OLX parameter, OLX value, site parameter, site value). Multiple site values can target the same OLX value (different rows), but each unique combination is a separate row.

### No global "unmapped values" report

The platform does not surface a list of CloudCart property values that lack OLX mappings. The merchant discovers gaps one product at a time — a publish fails, the History tab shows which value was unmapped, the merchant comes back to this page to add the mapping. There is no pre-flight audit screen.

### ParameterMap and ParameterValueMap scoped by endpoint_id

Both `ParameterMap` and `ParameterValueMap` models inherit the `Endpoint` scope — they're auto-filtered to the current OLX country. Switching country wipes them via disconnect, ensuring the merchant doesn't accidentally apply BG-mappings to RO adverts.

### Multi-value join during publish — multiple OLX values per parameter possible

When the publish formatter assembles attributes for an advert, it iterates ALL mapped values for each parameter. So when a CloudCart property has 3 possible values mapped to 3 different OLX values, the resulting OLX attribute list includes all 3. This works for OLX parameters that accept multi-value lists (e.g., features).

## Open questions
