---
type: feature
nav_path: "Customers → Custom fields → Validation & storage"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["Custom field validation rules", "Custom field storage", "Custom field uniqueness", "form_fields register scope"]
tags: [customers, custom-fields, validation, storage]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Custom fields — validation & storage

> Part of [[customers-custom-fields]]. See the hub for the other aspects (list view, editor modal, types, system linkage, storefront behaviour, programmatic access).

## Purpose

This aspect documents what the server enforces when a custom-field definition is saved or deleted, how the data is shaped on disk, and what happens to stored customer answers when a definition is removed. The Save / Update / Delete paths are deterministic — every constraint here is enforceable via the admin API and reflected in the same UI errors.

## Where to find it

Validation errors surface inside the editor modal at `/admin/customers/custom-fields` — see [[customers-custom-fields-editor-modal]]. Server-side error strings are quoted verbatim below; the modal shows them inline beside the offending field.

## What the merchant can do here

The merchant can:

- Save a field definition (Create / Update) and see inline validation errors if any constraint is violated.
- Delete a field — triggers the cascade rules documented below.
- Rely on uniqueness checks on both **Name** (internal) and **Storefront name** — duplicates are rejected with explicit toasts.

The merchant cannot:

- Bypass any validation rule (no admin override exists in the UI).
- Soft-delete or archive a field (delete is destructive — see the cascade section below).
- Add custom regex / min-max length / numeric-range validators (the platform supports Required + type-native only).

## Settings & fields

### Server-enforced validation rules (CustomFieldRequest)

| Field | Rule |
|-------|------|
| `name` | Required. Max 191 characters. Unique across the store. |
| `storefront_name` | Max 191 characters. Unique across the store. |
| `type` | Required. Must be one of: `checkbox`, `select`, `radio`, `text`, `textarea`, `phone`, `link`. |
| `value` | Required when `type` is one of `select` / `radio` / `checkbox`. Array of option strings. |
| `value.*.name` | Each option value name required. Max 191 characters. Unique within the field. |
| `active` | `0` or `1`. |
| `required` | `0` or `1`. |
| `system` | `0` or `1`. |
| `customer_modify` | `0` or `1`. |
| `key` | Required when `system = 1`. Must be one of `username` / `password` / `link`. See [[customers-custom-fields-system-linkage]]. |

### Verbatim error messages

- *"Name already exists"* — duplicate internal name.
- *"Storefront name already exists"* — duplicate customer-facing name.
- *"Key must be one of the following: username, password, link"* — when System is ON and `key` is not in the allowlist.

These strings are stable across releases and safe to grep for in support tickets.

### Storage layout

**Definitions** live in a generic `form_fields` table shared with product / checkout / other form-style configurations. A **global query scope** locks every read and write on this resource to `form = 'register'` — that's the discriminator distinguishing customer custom fields from product options and other entries. A `saving` model hook force-stamps `form = 'register'` on every write, so the discriminator can never drift even via direct fillable assignment.

**Option values** (the per-row choices for Dropdown / Radio / Checkbox) live in a sibling options table linked by `field_id`, each with a `sort_order` (zero-indexed from row position) and `name`.

**Stored customer answers** live in a separate `customers_custom_fields` table — one row per `(customer_id, field_id)` with a JSON-cast `value` column:

- Checkbox-type answers (multi-select) are stored as a JSON array.
- Phone, text, textarea, link answers are stored as a JSON string.
- Select / radio answers are stored as a JSON string (the picked option's name).

## Business rules

### Type is locked after create (server-side enforcement)

The controller's `update` path does not pass `type` into the update payload — even if a request somehow sent it, the field would be ignored. The 7-type allowlist still applies at Create time. See [[customers-custom-fields-editor-modal]] for the UI lockout.

### Update payload shape (allowed fields only)

The fields actually updated on Edit are: `name`, `storefront_name`, `active`, `required`, `mapping`, `system`, `customer_modify`, `key`. The `type` field is absent. The `value` array is processed only when the field is a Selection type — see the next rule.

### Save / update transaction — option-value diff-and-delete

Both Create and Update wrap the persistence in a DB transaction:

1. Insert / update the field row in `form_fields` (with `form = 'register'` stamped by the saving hook).
2. For each submitted option value: **find-or-new by `id`**, fill, set `sort_order = row-index`, save.
3. On Update only: **diff** the submitted ids against the existing options — any existing option NOT in the submission is deleted.

This means renaming an option in place updates the label on the existing row (preserving its id), but removing it from the modal deletes it from the DB. Newly-added rows arrive with synthetic `new_record_<N+1>` keys (see [[customers-custom-fields-editor-modal]]) so the backend treats them as fresh inserts.

### Delete cascade

Deleting a field definition removes the row from `form_fields`. **The stored customer answers in `customers_custom_fields` referencing that `field_id` are also removed** — no soft-delete, no archive, no recoverable bin. Legacy data is lost.

Bulk-delete (from the table actions) has the same cascade — every selected field's answers go with it. See [[customers-custom-fields-list-view]] for the UI surfaces.

### Option-value names must be unique within the field

Within a single Selection-type field, option-value names must be unique. The validator rejects duplicates at save time. Across different fields, name reuse is allowed (e.g., two fields can both have an option called *"Other"*).

### Validation limits on storefront customer input

When a customer fills the field at checkout, the platform validates only:

- **Required**: must be present if the flag is ON.
- **Type-native**: phone format via libphonenumber, URL format for `link`.

There is **NO** support for regex, min/max length, numeric range, or custom validators on the storefront side. For more sophisticated validation the merchant needs a custom theme implementation.

### Permission gate

The list page requires `customers` permission + `customers.custom_fields` middleware. Write actions (Create / Update / Delete) need a separate write grant — see [[customers-custom-fields-list-view]].

### Custom-data scope tied to the global "register" form

The shared `form_fields` table holds entries for product options, checkout fields, and other form-style configurations alongside customer custom fields. Because of the global `form = 'register'` scope, customer custom fields appear ONLY in the customer signup / checkout flow — they are never rendered on product detail pages, the cart drawer, or other surfaces that read other slices of `form_fields`.

## Related

- [[customers-custom-fields]] — hub.
- [[customers-custom-fields-editor-modal]] — the UI that produces the validated payload.
- [[customers-custom-fields-types]] — the 7-value type allowlist enforced server-side.
- [[customers-custom-fields-system-linkage]] — the `key` allowlist (`username` / `password` / `link`).
- [[customers-custom-fields-storefront-behaviour]] — what happens at checkout + My-Account when validation passes.
- [[customers-custom-fields-list-view]] — UI for delete (which triggers the cascade).
- [[customer]] — entity that holds the canonical write-back when System is set.

## Open questions

None.
