---
type: feature
nav_path: "Marketing → Subscribers → Custom Fields → Create / Edit modal"
route_name: subscribers-fields-list-new
route_path: /admin/marketing-new/subscribers/fields
aliases: ["Subscriber custom field modal", "Create field modal", "Edit field modal", "Subscriber field settings", "Subscriber field option values"]
tags: [marketing, subscribers, custom-fields, modal, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers-custom-fields]]. See the hub for the other aspects (list page, field types, downstream surfaces).

# Subscriber Custom Fields — the create / edit modal

## Purpose

The **modal where the merchant defines or edits a single subscriber custom field** — its internal name, its storefront-facing label, its type, and (for selection types) its option values. This is reached from the list page ([[subscribers-custom-fields-list]]) via **Add custom field** or by clicking a field name.

## Where to find it

Sidebar → **Marketing** → **Subscribers** → **Custom fields** → **Add custom field** (or click a field name to edit). The modal opens over the list page at `/admin/marketing-new/subscribers/fields`.

## What the merchant can do here

- Set the **internal field name** and the **storefront-facing label**.
- **Pick the field type** (only on create — locked on edit; see [[subscribers-custom-fields-types]]).
- For selection types, **add / reorder / remove option values**.
- **Save** (toast *"Saved successfully"* on both add and edit) or **Cancel**.

Title: **Create field** when adding, **Edit field** when modifying. Buttons: **Cancel** and **Save**. The modal has two cards.

## Settings & fields

### Card 1 — Field settings

| Field | What it does | Validation |
|-------|--------------|------------|
| **Field name (for internal use)** (`name`) | Internal label shown in the admin list, segment-condition picker, and reports. Not visible to the storefront customer. | Required. Min 1 character, max 191. Unique among subscriber custom fields. Error texts: *"Field is required"*, *"Field must be at least 1"*, *"Field may not be greater than 191"*, *"A field with this name already exists"*. |
| **Field name (Visible ad the customer account)** (`storefront_name`) | Label rendered to the visitor on the storefront subscribe form. (Despite the UI label, this is the **storefront-facing label**, not the customer-account label.) Optional — if empty, the storefront falls back to the internal name. | Max 191 characters. Error: *"Field may not be greater than 191"*. |
| **Choose field type** (`type`) | Two tab groups: **Selection** (Dropdown, Radio button, Checkbox) and **Text fields** (Text field, Text area, Phone). The merchant picks one type via radio. | Required. **Type cannot be changed after creation** — the tabs and radio are disabled on edit. See [[subscribers-custom-fields-types]]. |

### Card 2 — Field option values

Only shown when type is `select`, `radio`, or `checkbox` (the Selection family — see [[subscribers-custom-fields-types]]).

| Field | What it does | Validation |
|-------|--------------|------------|
| **Option value name** (`options.*.name`) | One row per option the storefront visitor can choose. Each row has its own free-text input plus a grip handle for reorder and a remove icon. | Required (at least one option). Min 1 character, max 191 each. Error texts: *"You must have at least one option"*, *"Field is required"*, *"Field may not be greater than 191"*, *"Rows may not be greater than 250"*. Max **250 options** per field. |
| **Add option value** (button) | Appends a blank option row. | |
| (remove icon) | Removes that option row. Disabled when only one row remains (a selection field must keep at least one option). | |

On save, the toast is *"Saved successfully"* (both add and edit). The initial fetch failure shows *"Error while loading data"*.

## Business rules

### Type is silently ignored on edit

When editing an existing field, the type tabs and radio are disabled. Even if a type change were forced into the request, the backend does not read or alter the field's type during edit — there is no error returned; the field's underlying type simply stays the same. To change type, the merchant must delete and recreate. The reasoning is on [[subscribers-custom-fields-types]].

### Option diff-on-save

When saving a field with options, the platform diffs the submitted rows against the stored rows:

- Each incoming option **with an id** updates the existing row.
- Each incoming option **without an id** creates a new row.
- Any existing option id **NOT in the incoming list** is **deleted**.

So removing an option in the UI cascades — the option row is deleted, and any subscriber values pointing at that option become orphan references (visible as "deleted option" labels on the segment-condition picker until the merchant updates affected segments). There is no soft-delete on options. See [[subscribers-custom-fields-downstream]] for the effect on segments.

### Caps come from the server, not the UI

The 250-option cap and the 191-character length caps are enforced by request validation, so the same caps apply on any non-UI path. There is no hard cap on the total number of subscriber custom fields per store. The full cap table is on the hub: [[marketing-subscribers-custom-fields]].

### Name uniqueness is subscriber-scoped

The internal **name** must be unique among the store's subscriber custom fields only. On collision, the save fails with *"A field with this name already exists"*. A customer custom field can share the same name without conflict — see [[subscribers-custom-fields-downstream]] for the namespace detail.

## Related

- [[marketing-subscribers-custom-fields]] — hub.
- [[subscribers-custom-fields-list]] — the list page this modal is opened from.
- [[subscribers-custom-fields-types]] — the six types + why Card 1's type radio locks on edit.
- [[subscribers-custom-fields-downstream]] — name-uniqueness namespace + how option deletes ripple into segments.

## Open questions

No outstanding questions.
