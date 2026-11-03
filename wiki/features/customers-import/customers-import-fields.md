---
type: feature
nav_path: "Customers → Import → Fields & mapping"
route_name: admin.complete.import
route_path: /admin/import/complete-import/customers
aliases: ["Import customers fields", "Customer import field map", "Customer import mapping", "Customer import required fields", "customer.email mapping", "customer.full_name split", "group.name mapping", "Customer CSV template", "Customer import addresses disabled"]
tags: [customers, import, csv, fields, mapping, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-import]]. See the hub for related aspects (wizard, concurrency, processing, side effects, plan gates, API alternative).

# Import customers — field map + validation + CSV template

## Purpose

This page is the **single reference** for the customer-import field schema: which customer fields can be mapped from CSV columns, which are required, the exact validation messages, the CSV-template column layout, and why **address fields are intentionally disabled** in the current build.

## Where to find it

The field map surfaces in **STEP 2** of the wizard ([[customers-import-wizard]]) as one **SettingsCard** per field group. Each customer field is rendered as a **SelectWithAjax** dropdown listing the available CSV columns. The wizard itself is launched from [[customers]] → **Import**.

## What the merchant can do here

Map each customer field in the card to a CSV column (by 0-indexed numeric id with a derived sample value), or leave it unmapped to skip that field. The only **required** mapping is `customer.email` (red asterisk + validation block on Submit).

The merchant CANNOT:

- Map address fields (country / city / street / postcode / phone) — see **Address fields are intentionally disabled** below.
- Map custom fields ([[customers-custom-fields]]) — only built-in customer fields plus `group.name`.
- Set passwords for imported customers — the platform generates passwords automatically (see [[customers-import-side-effects]]).

## Settings & fields

### Customer field map (Step 2)

| Customer field | UI label | Required? | Notes |
|----------------|---------|----------|-------|
| `customer.first_name` | *"First name"* (translated key) | Optional | — |
| `customer.last_name` | *"Last name"* | Optional | — |
| `customer.full_name` | *"Full name"* | Optional | If provided and `first_name` is blank, the platform splits on the first space (first token = first name, rest = last name). |
| `customer.email` | *"Email"* | **YES** (`required` array contains this key) | Every row must have a valid email; rows without a valid email are silently skipped (see [[customers-import-processing]] for dedup). |
| `customer.note` | *"Note"* | Optional | Admin-only note. |
| `customer.marketing` | *"Marketing"* | Optional | `yes` / `no`. |
| `group.name` | *"Group name"* | Optional | Per-row group override; if the name doesn't match an existing group, the group is auto-created (see [[customers-import-processing]]). |

Map-options for each dropdown come from `map_options` — derived from `GET /admin/api/core/customers/csv/mapping/{importId}` and listing every CSV column by its 0-indexed numeric id plus a derived sample value (e.g., column 0 → *"john@example.com"*).

Required fields enforced both in the UI's Step 2 ("required: true" on the email mapping) and on the back-end (rows where `customer.email` is unmapped or empty are dropped).

### Required Step 1 settings (file + group)

| Field | Validation | Notes |
|-------|------------|-------|
| `import_file` | Required, `.csv` OR `.txt` (MIME-validated as `mimes:csv,txt`) | *"Please select a file to import"* / *"Please select a valid file type (csv, txt)"* — the backend accepts BOTH extensions even though the UI says "CSV". |
| `has_header_line` | Required, `0` or `1` | Default OFF (`0`); if ON, first row is dropped from the temp table BEFORE counting. |
| `customer_group_id` | Required (integer, must exist in `type__customer_groups`) | *"Customer group is required"* / *"Customer group must be an integer"* / *"Customer group not found"*. If missing from the request body, the platform silently falls back to the **Default** group — so omitting it from an API call doesn't fail. |

### Step 2 mapping format

Each mapping is a `{customer_field: csv_column_index}` pair sent in the `import_binds` array. CSV columns not mapped are dropped during import.

### Validation messages (verbatim)

| Trigger | Exact message |
|---------|---------------|
| Missing file | "An import file is required." |
| Invalid file format | "The file is invalid" |
| Header line + zero rows | "The total line count is {count}." |
| Too many rows | "The maximum number of import items is {limit}." |
| Concurrent imports | "There cannot be more than {N} imports running simultaneously." |
| Missing email mapping | "The customer.email field is required." |
| Invalid mapping | "Field bind is invalid." |
| File too big or corrupt | "The file is invalid" |
| Plan feature missing | Standard plan-upgrade prompt |

The concurrent-imports message accompanies an HTTP 409 with an `actions` array containing a *"Reset stuck import"* button — see [[customers-import-concurrency]].

### Customer group fallback

The Step 1 customer-group picker provides the **default** group for rows that don't specify their own. The Step 2 `group.name` mapping (if present) overrides per-row — and auto-creates new groups when the row's value doesn't match an existing group (see [[customers-import-processing]]).

## Business rules

### Address fields are intentionally disabled

The `customers_addresses` block in the formatter is **commented out** (with a `@todo deprecated table customers_addresses` note). So address columns from a CSV are NOT picked up by the formatter — the addresses dropdown in Step 2 shows no address-field options.

This is a deliberate choice while CloudCart migrates address storage to the new multi-address-per-customer model (see [[customers-details-shipping-addresses]]). Until address import is restored, the merchant cannot bulk-import addresses — only customer attributes. There is no announced timeline for restoring CSV address import; for bulk address uploads the merchant must use the per-customer addresses API ([[api-customers]]), or contact CloudCart support.

### CSV Template — sample file contents

The **CSV Template** download link in Step 1 returns a sample file with **10 columns and NO header row** (so the merchant needs to leave **Has header line** unchecked when uploading the sample). Column order: First name, Last name, Full name (blank), Email, Note, Marketing flag (`yes` / `no`), Postcode-like value, Phone, Address-like text, Group name.

Only the built-in customer fields (first name, last name, full name, email, note, marketing) plus group name are actually imported — extra sample columns (phone, address, postcode) are present for the merchant to see column layout but are NOT mapped by the formatter (address import is disabled — see above). The merchant should map only the columns they want imported.

### Full-name auto-split

If `customer.full_name` is mapped and `customer.first_name` is blank for the row, the platform splits the full name on the **first space**: the first token becomes the first name, everything after the first space becomes the last name. Mapping both `customer.first_name` and `customer.full_name` for the same row uses the explicit `first_name` and only consults `full_name` if `first_name` is blank.

### Custom fields are NOT in the field map

[[customers-custom-fields]] defined for the store are NOT importable via the standard customer CSV — the formatter only consults the built-in field map above. To bulk-load custom-field values, use [[api-customers]] (one customer at a time per [[customers-import-api-alternative]]).

## Related

- [[customers-import]] — hub.
- [[customers-import-wizard]] — the Step 2 UI that surfaces this field map.
- [[customers-import-processing]] — what the formatter does with the mapped fields (email dedup, group auto-create, full-name split).
- [[customers-import-side-effects]] — webhooks, `imported` flag, password generation on imported rows.
- [[customers-custom-fields]] — store-defined custom fields (NOT importable via CSV).
- [[customers-custom-groups]] — where auto-created groups appear.
- [[customers-details-shipping-addresses]] — the multi-address model that gates address-import restoration.

## Open questions

(All resolved — the address-import restoration timeline is intentionally unannounced; not a wiki gap.)
