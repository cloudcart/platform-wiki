---
type: feature
nav_path: "Customers → Custom fields → Editor modal"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["Custom field editor", "Create custom field modal", "Edit custom field modal", "Add custom field"]
tags: [customers, custom-fields, modal, editor]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Custom fields — editor modal

> Part of [[customers-custom-fields]]. See the hub for the other aspects (list view, types, system linkage, validation & storage, storefront behaviour, programmatic access).

## Purpose

The single side-panel modal handles both **Create** and **Edit** flows for a custom-field definition. It opens from the top-right **+ Add custom field** button (create mode) or from clicking any row's name in the list (edit mode). All in-flight constraints — type lockout in edit mode, type-conditional sub-cards, sticky Save behaviour — live in this modal.

## Where to find it

The modal is launched from [[customers-custom-fields-list-view]]:

- **Create**: top-right **+ Add custom field** button on `/admin/customers/custom-fields`.
- **Edit**: click any row's Name cell in the list table.

The modal is an xl side-panel that slides in from the right.

## What the merchant can do here

### Modal header + lifecycle

- **Title**: *"Create field"* in create mode, *"Edit field"* in edit mode (resolved via `resolveLabel`).
- **Sticky Save header**: a header row at the top contains Close + Save. Save shows a spinner during submit; both buttons are disabled while submitting.
- **Blocked closes during submit**: ESC and backdrop-click are both blocked while the modal is in a loading state — the merchant cannot accidentally drop a half-finished save.
- **Edit-mode preload**: when opened with an id, the modal shows a Loading spinner while fetching the field details. The `values` object is normalised to `{}` if the API returns an empty array (defensive shaping).

### Type selection tabs (Create mode only)

In Create mode the modal exposes **three type tabs** at the top — selecting a tab sets `data.type` to the first value in that group. The tabs use a sliding "active" indicator. **In Edit mode the tabs and type-radios are completely hidden** — type is locked after create.

| Tab | Radio sub-options |
|-----|-------------------|
| **Selection** | Dropdown (`select`) / Radio button (`radio`) / Checkbox (`checkbox`) |
| **Text fields** | Text field (`text`) / Text area (`textarea`) / Phone (`phone`) |
| **Other** | URL field (`link`) |

Each radio option has a label + descriptive text — e.g., for select: *"Dropdown - select from list"*. See [[customers-custom-fields-types]] for the full type catalogue.

Type-switch side effects (handled inside the modal):

- Switching TO `link` **clears** the previously-typed `data.key` value.
- Switching TO any of `select` / `checkbox` / `radio` (the Selection group) **resets BOTH** `data.key = null` AND `data.system = 0` — option-value-type fields cannot be marked as system. See [[customers-custom-fields-system-linkage]] for why.

### Per-field configuration inputs

The main card always renders these inputs (regardless of type):

| Field | What it does |
|-------|--------------|
| **Field name (for internal use)** | Technical name. Used in API / filters / segmentation. NOT shown to customers. |
| **Field name (Visible at the customer account)** | The storefront label. What customers see at checkout. |
| **Active** toggle | When OFF, the field is hidden from storefront checkout. Existing data stays stored. |
| **Field is required** toggle | When ON, the customer cannot complete checkout without filling this field. |
| **Allow customer to modify** toggle | When ON, the customer can edit their value from the storefront My-Account page; when OFF the value is set at checkout and locked. See [[customers-custom-fields-storefront-behaviour]]. |

### Type-conditional sub-cards

A **second** `SettingsCard` slides open below the main card via `Vue3SlideUpDown` depending on the current type:

| Type group | "Field option values" sub-card | "System field" toggle block |
|------------|-------------------------------|-----------------------------|
| Selection (Dropdown / Radio / Checkbox) | Yes | No |
| Text fields (Text / Textarea / Phone) | No | Yes |
| Other (URL) | No | Yes |

**Option-values sub-card** (only for select / radio / checkbox):

- Card title *"Field option values"* + sub-label *"Option value name"* + horizontal rule.
- Per-row input + delete: each option value is an input on a wide column + a red trash icon. Empty inputs surface a validation error inline. Removing the last row auto-inserts a fresh empty one (the card cannot have zero rows).
- **+ Add option value** link (purple link, bottom of card) — appends a new row with key `new_record_<N+1>` so the backend recognises it as a NEW option. Disabled during submit.
- When the modal opens with zero existing values for a select-type field, the card auto-adds one empty row so the merchant immediately sees the input.

**System-field section** (only for text / textarea / phone / link):

- An **Active toggle** labelled *"System field"* reveals when `data.type` is one of `['text', 'textarea', 'phone', 'link']`.
- Toggling it ON reveals a second `Vue3SlideUpDown` with the **System field type** dropdown (the canonical-key picker). Toggling it OFF collapses the dropdown back.
- Available canonical keys (from `keyOptions`): for non-link types — `username` / `password` / `link`; for link type — `link` only. See [[customers-custom-fields-system-linkage]] for the allowlist and the write-back semantics.

## Settings & fields

Save payload shape (sent on Save) is type-dependent:

- For `select` / `radio` / `checkbox`: body includes `value` (array of option values, filtered to drop empty strings).
- For `text` / `textarea` / `phone` / `link`: body includes `system` (1/0) and — when `system = 1` — `key` (the selected system-field type).

The controller's update path never receives `type` (it's locked in Edit mode and not sent) — see [[customers-custom-fields-validation-storage]] for the full server-side flow.

## Business rules

### Type is locked after create

The Edit modal hides the type tabs and the type radios — there is no UI path to change a field's type. To switch a field's type, the merchant must (a) export the existing customer data, (b) delete the field (losing all stored customer values — see [[customers-custom-fields-validation-storage]]), and (c) create a new field of the desired type. There is no in-place type migration.

### Modal is the only edit surface

The list page does not have inline-edit cells. Every change to Name, Required, Allow customer to modify, system-field linkage, or option values must go through this modal. The Status toggle and per-row Delete are the only exceptions — those happen directly on the list — see [[customers-custom-fields-list-view]].

### The "+ Add option value" link uses synthetic ids

New option values are appended with the key `new_record_<N+1>` so the backend can tell them apart from existing rows (which carry their stable database id). On save the backend find-or-news by id and re-orders by row index — see [[customers-custom-fields-validation-storage]] for the diff-and-delete logic.

### What the merchant CANNOT do here

- Change the field type after creation (the type tabs are hidden in Edit mode).
- Reorder fields per-language (the order is store-wide — see [[customers-custom-fields-list-view]]).
- Conditional logic ("if field X = Yes, then show field Y") — fields are independent.
- Field validation rules beyond Required + type-native (no regex, no min/max length) — see [[customers-custom-fields-validation-storage]].

## Related

- [[customers-custom-fields]] — hub.
- [[customers-custom-fields-list-view]] — entry point (Edit-row click / **+ Add custom field** button).
- [[customers-custom-fields-types]] — the 7 supported types referenced by the type tabs.
- [[customers-custom-fields-system-linkage]] — the System-field toggle block inside the modal.
- [[customers-custom-fields-validation-storage]] — what the Save payload becomes server-side.

## Open questions

None.
