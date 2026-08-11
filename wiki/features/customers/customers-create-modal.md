---
type: feature
nav_path: "Customers → Create / Edit modal"
route_name: customers-list.new
route_path: /admin/customers-new
aliases: ["Add customer", "Add customer modal", "Create customer", "Edit customer", "Customer create form", "Add customer side panel"]
tags: [customers, modal, create, edit, custom-fields, validation]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers]]. See the hub for the other aspects (list view, filters, bulk actions, ban flow, flags, lifetime KPIs).

# Customers — Create / Edit customer modal

## Purpose

The side-panel that opens from the **+ Add customer** button (and from various pencil icons on [[customers-details]]). It collects identity, contact, group, note, and per-store custom fields, then POSTs / PATCHes the customer. This aspect covers every field, validation rule, save behaviour, custom-fields rendering, the `focusNote` / `noteOnly` opening modifiers, and the guest→registered auto-merge.

## Where to find it

- Customers list header → **+ Add customer** button → opens in create mode.
- Customer detail page ([[customers-details]]) → identity-card or Customer-note-card pencil → opens in edit mode (sometimes `noteOnly` — see below).

Route context: `/admin/customers-new` and `/admin/customers-new/details/:id`.

## What the merchant can do here

- Add a new customer manually (with password — required only on create).
- Edit an existing customer's identity, contact, group, note, and custom-field values.
- Edit just the note via the `noteOnly` opening modifier (from the Notes card pencil).
- Manage custom field definitions in a new tab via the **Manage fields** button — see [[customers-custom-fields]].

## Settings & fields

### Section: Customer details (single card)

| Field | v-model | Type | Required | Validation / Notes |
|-------|---------|------|----------|--------------------|
| **First name** | `first_name` | Text | YES | Max 191 chars. |
| **Last name** | `last_name` | Text | YES | Max 191 chars. |
| **Email** | `email` | Email | YES | Max 191 chars, valid email, unique within store. `autocomplete="off"`. |
| **Password** | `password` | Password | **YES on create**, optional on edit (leave blank = keep current). | Server-side: 3-20 chars when `has_password=true`. `autocomplete="off"`. |
| **Phone** | `alternative_phone` | International phone input | No | libphonenumber validation when supplied. Storefront error message: *"Invalid phone number"*. |
| **Customer group** | `group_id` | Searchable dropdown | YES | Populated from `GET /admin/api/core/customers/groups`. Default-selects the FIRST option if none picked (typically the Default group). Disabled until options load. Not clearable. |
| **Customer note** | `note` | Textarea | No | Max 191 chars (server-enforced). Help block: *"This note will not be visible to customer"*. Placeholder: *"Add customer note here"*. |

### Section: Custom fields (second card, only if store has custom fields defined)

- Info banner: blue info icon + *"These are custom fields that the customer can fill in, they can also be required."* + a **Manage fields** button on the right that opens [[customers-custom-fields]] in a new tab AND closes the modal.
- Fields are rendered in a **2-column grid** (split in half by index).
- Field renderers per type:
  - `text` / `link` → CcInput (link gets placeholder *"Enter URL"*).
  - `textarea` → CcTextarea.
  - `phone` → CcPhoneInput (libphonenumber).
  - `select` → searchable dropdown, not clearable.
  - `radio` → CcRadio with the field's option values.
  - `checkbox` → multiple checkboxes (each option separate); the value is stored as an ARRAY of option-IDs that are ticked.
- Required indicator (red `*`) renders next to the label when the field's `required=1`.

### Modal title behaviour

- Create mode → *"Add customer"*.
- Edit mode → reads `<first_name> <last_name>` (the customer's own name as the header).

### Opening modifiers — `focusNote` and `noteOnly`

The modal accepts two opening modifiers from elsewhere on the customer detail page:

- `focusNote=true` — autofocuses the textarea on open (used from the Identity-card pencil and from the Customer note card pencil).
- `noteOnly=true` — hides the "Customer details" section entirely; renders ONLY the note textarea + the Custom fields card. Used by the Notes card's pencil — the merchant goes straight to editing the note without the full identity form. Verified via the `noteOnlyMode` ref + `v-if="!noteOnlyMode"` template guards.

### Save behaviour

- POST `/admin/api/core/customers` on create, PATCH `/admin/api/core/customers/{id}` on edit.
- Empty values in the `custom` payload are stripped (null / undefined / empty-string entries dropped). Arrays with all-empty entries are also dropped.
- `password` is only sent when non-empty (so editing without password change does NOT touch the customer's stored hash).
- On success: toast *"Customer saved successfully"*, modal closes, and on CREATE the merchant is auto-navigated to the new customer's `/admin/customers-new/details/:id` page.
- Validation errors (HTTP 422) populate the per-field error slots in red inline.
- The modal blocks backdrop close while `submitLoader` is true.
- Opening spinner runs while groups + custom fields are fetched.

## Business rules

### Email uniqueness scope (per-store) — verified

The email uniqueness check is scoped to the current store's customers table — each store has its own customers table in its own schema. So the same email CAN belong to different customer accounts in different CloudCart stores. Within one store, the email is unique across all customer accounts (both guest and registered).

### Guest → registered customer auto-merge on add — verified

When the merchant uses **+ Add customer** with an email that already belongs to a **guest** customer (someone who checked out without registering), the platform DOES NOT throw "Email already exists" — instead it **promotes** the existing guest record to a regular customer, preserving the prior order history attached to that email. Behind the scenes: the platform code uses `firstOrNew` on the matching guest email, so the registered customer the merchant just added IS the same customer entity who placed those earlier guest orders. This means the new customer immediately inherits the lifetime KPIs from those past orders — see [[customers-lifetime-kpis]].

### Backend Form Request notes (beyond the field table)

- **Password (on create)**: NOT required by the Form Request at the API level — but the modal's UI marks Password as required when in create mode. (At the Customer-model `validate` level, when `has_password=true` is sent, password must be at least 3 chars and at most 20 chars — stricter than the modal's "min 6", so the server-side validation may surface 422 errors on longer passwords.)
- **Note**: 191-character maximum, enforced at the model `validate` level.
- **Password complexity** beyond length is NOT enforced at the model level.

### Plan-gate `customers` blocks create at cap

Every customer-create path (this modal, storefront registration, JSON-API v2 POST) checks the platform code. When the cap is reached, the create returns HTTP 402 and the merchant is redirected to `/admin/plan/feature/customers`. Existing customers continue to work; only NEW records are blocked. Add-on packs (+100 / +500 / +1000) stack — see [[plan-features]].

### Manage fields button closes the modal

Clicking the **Manage fields** button in the Custom fields card opens [[customers-custom-fields]] in a new tab AND closes the create / edit modal — any unsaved edits are discarded silently. The merchant should save first if they have pending input.

### Side effects on save

- `customer.created` (POST) or `customer.updated` (PATCH) webhook — see [[settings-hooks]].
- Subscriber record provisioned (when applicable); Marketing changes propagate — see [[customers-flags]].
- KPIs start at 0 unless guest-merge attached existing orders — see [[customers-lifetime-kpis]].

## Related

- [[customers]] — hub.
- [[customers-custom-fields]] — custom-field definitions reached via Manage fields.
- [[customers-custom-groups]] — group picker source.
- [[customers-flags]] — Marketing flag side effects.
- [[customers-lifetime-kpis]] — denormalised KPIs the new customer inherits via guest-merge.
- [[customers-details]] — the detail page the merchant lands on after create.
- [[plan-features]] — `customers` cap + add-on packs.
- [[settings-hooks]] — `customer.created` / `customer.updated` webhooks.

## Open questions

- Manage fields button discarding unsaved edits: is there a confirm prompt? (verify)
