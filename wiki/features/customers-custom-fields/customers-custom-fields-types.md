---
type: feature
nav_path: "Customers → Custom fields → Field types"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["Custom field types", "Dropdown radio checkbox text textarea phone link", "7 custom field types"]
tags: [customers, custom-fields, types]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Custom fields — supported types

> Part of [[customers-custom-fields]]. See the hub for the other aspects (list view, editor modal, system linkage, validation & storage, storefront behaviour, programmatic access).

## Purpose

CloudCart supports **7 custom-field types** for customer data collection. The type is chosen at creation time (from the type tabs in the editor — see [[customers-custom-fields-editor-modal]]) and is **locked** after save: the only way to change a field's type is to delete and recreate. Each type maps to one customer-facing input pattern and, on the server side, to one of seven allowed `type` enum values.

## Where to find it

Selected via the **type tabs** at the top of the Create modal launched from `/admin/customers/custom-fields` (the **+ Add custom field** button) — see [[customers-custom-fields-editor-modal]] for the modal mechanics.

In Edit mode the tabs and type radios are completely hidden; the field's type is read-only.

## What the merchant can do here

Pick one of the 7 supported types when creating a field. Each type has its own customer-facing rendering and its own configuration shape (option values for selection types, system-field linkage for text-style types).

### The 7 supported types

| Type tab | Type enum | Customer-facing UI | Modal description |
|----------|-----------|---------------------|-------------------|
| Selection | `select` | Dropdown menu with predefined values | *"Dropdown - select from list"* |
| Selection | `radio` | Visible radio buttons (single choice) | *"Radio button - single choise"* |
| Selection | `checkbox` | Checkboxes (multi-select) | *"Checkbox - multiple choise"* |
| Text fields | `text` | Single-line text input | *"Text field - short text"* |
| Text fields | `textarea` | Multi-line text input | *"Text area field - longer text"* |
| Text fields | `phone` | Country-code phone input | Phone validation via libphonenumber |
| Other | `link` | URL input | *"URL field"* |

The allowlist is enforced server-side; submitting any other value is rejected — see [[customers-custom-fields-validation-storage]].

### Selection types (select / radio / checkbox)

All three Selection types use the same backing data shape: a list of **option values**, each with a `name` (label) and an implicit `sort_order` taken from row position. They differ only in the storefront rendering:

- **Dropdown** (`select`) — single-choice dropdown menu, compact.
- **Radio** (`radio`) — single-choice radio button group, all options visible at once.
- **Checkbox** (`checkbox`) — multi-choice checkboxes; a customer answer can hold several values at once (stored as a JSON array — see [[customers-custom-fields-validation-storage]]).

The editor modal's **"Field option values"** sub-card is shown ONLY for these three types; see [[customers-custom-fields-editor-modal]] for the per-row input + trash + **+ Add option value** UX.

### Text-style types (text / textarea / phone)

All three accept free-form customer input on the storefront. They differ in the input element rendered:

- **Text field** (`text`) — single-line `<input>`.
- **Text area** (`textarea`) — multi-line `<textarea>`.
- **Phone** (`phone`) — phone input with country-code dropdown; format validated via libphonenumber.

The **System field** toggle is available for all three — these are the canonical write-back candidates. See [[customers-custom-fields-system-linkage]] for the narrow allowlist of canonical keys (`username` / `password` / `link`) the merchant can link to.

### URL type (link)

A dedicated **URL field** (`link`) with URL-format validation. The System-field linkage block is available but **only** the canonical key `link` is exposed in the System-field dropdown when `data.type = link` (the `keyOptions` computed restricts the list — see [[customers-custom-fields-system-linkage]]).

## Settings & fields

### Per-field configuration by type group

| Type group | "Field option values" sub-card | "System field" toggle | Default Active | Default Required |
|------------|-------------------------------|------------------------|----------------|------------------|
| Selection (select / radio / checkbox) | Shown | Hidden | ON | OFF |
| Text fields (text / textarea / phone) | Hidden | Shown | ON | OFF |
| Other (link) | Hidden | Shown (link only) | ON | OFF |

### Option-value rules (select / radio / checkbox only)

- Each option value has a `name` (label) — no separate technical key, no per-option metadata.
- Option values must be **unique within the field** — see [[customers-custom-fields-validation-storage]] for the server-side enforcement.
- Each option value name is max 191 characters.
- The card cannot have zero rows — removing the last row auto-inserts a fresh empty one (see [[customers-custom-fields-editor-modal]]).

### Native validation per type

| Type | Validation enforced on customer input |
|------|---------------------------------------|
| `select` | Value must be one of the defined option names. |
| `radio` | Value must be one of the defined option names. |
| `checkbox` | Each picked value must be one of the defined option names. |
| `text` | None beyond Required. |
| `textarea` | None beyond Required. |
| `phone` | libphonenumber format validation. |
| `link` | URL format validation. |

**There are NO extra validation rules** — no min/max length, no regex, no custom validators. See [[customers-custom-fields-validation-storage]].

## Business rules

### Type is locked after create

The editor hides the type tabs in Edit mode and the controller's update path doesn't pass `type` into the update payload — see [[customers-custom-fields-editor-modal]]. To change a field's type the merchant must export data manually, delete the field (cascading the stored answers — see [[customers-custom-fields-validation-storage]]), and create a new one.

### Selection types cannot be system-linked

When the merchant picks `select` / `radio` / `checkbox` from the type tabs, the modal resets `data.system = 0` AND `data.key = null` automatically. Option-value-type fields **cannot** be marked as system — the System-field toggle block is hidden for the entire Selection group. See [[customers-custom-fields-system-linkage]] for why.

### Selection-type values are simple key=value pairs

There is no per-option technical key, no per-option metadata, no per-option visibility flag. Renaming an option in place updates the label but does NOT migrate stored customer answers that picked the old label — those rows retain the old string (verify exact behaviour).

### Phone-type fields cannot link to the canonical phone column

This is the most common misconception: even though Phone is a Text-fields tab and so the System toggle is available, the only canonical keys exposed are `username` / `password` / `link`. A merchant who wants to collect the customer phone via custom-field UX and have it land on the canonical customer phone column **cannot** do this directly through System linkage — see [[customers-custom-fields-system-linkage]].

### Storefront rendering

The storefront theme injects these fields into the checkout flow at a position the checkout templates control. The field's `storefront_name` (not the internal `name`) is shown as the label. See [[customers-custom-fields-storefront-behaviour]] for the full checkout + My-Account rendering rules.

## Related

- [[customers-custom-fields]] — hub.
- [[customers-custom-fields-editor-modal]] — type tabs UI.
- [[customers-custom-fields-system-linkage]] — why selection types can't be system-linked and which canonical keys are allowed.
- [[customers-custom-fields-validation-storage]] — server-side type allowlist and per-type validation.
- [[customers-custom-fields-storefront-behaviour]] — how each type renders on the checkout + My-Account pages.

## Open questions

- When a Selection-type option label is renamed, what happens to stored answers that picked the old label? Verify the migration path.
