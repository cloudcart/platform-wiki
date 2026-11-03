---
type: feature
nav_path: "Customers → Create / Edit modal"
route_name: customers-list
route_path: /admin/customers
aliases: ["Add customer", "Add customer modal", "Create customer", "Edit customer", "Customer create form", "Add customer side panel"]
tags: [customers, modal, create, edit, custom-fields, validation]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-11-03
source_count: 4
---

> Part of [[customers]]. See the hub for the other aspects (list view, filters, bulk actions, ban flow, flags, lifetime KPIs).

# Customers — Create / Edit customer modal

## Purpose

The side-panel that opens from the **+ Add customer** button (and from the pencil icons on [[customers-details]]). It collects identity, contact, group, note, and per-store custom fields, then POSTs / PATCHes the customer. This aspect covers every field, validation rule, save behaviour and custom-fields rendering, and opening the panel from the Notes card.

## Where to find it

- Customers list header → **+ Add customer** button → opens in create mode.
- Customer detail page ([[customers-details]]) → identity-card pencil → **Edit customer**, or the Notes card pencil → opens in edit mode.

Route context: `/admin/customers` and `/admin/customers/details/:id`.

## What the merchant can do here

- Add a new customer manually, with or without a password.
- Edit an existing customer's identity, contact, group, note, and custom-field values.
- Go straight to the note from the Notes card pencil: the same panel opens with the **Customer note** field focused.
- Manage custom field definitions in a new tab via the **Manage fields** button — see [[customers-custom-fields]].

## Settings & fields

### Section: Customer details (single card)

| Field | Key | Type | Required | Validation / Notes |
|-------|-----|------|----------|--------------------|
| **First name** | `first_name` | Text | YES | Max 191 chars. *"Customer first name is required"*. |
| **Last name** | `last_name` | Text | YES | Max 191 chars. *"Customer last name is required"*. |
| **Email** | `email` | Text | YES | Max 191 chars, valid email, unique within the store. *"Customer email is required"*, *"Customer email already exists"*. |
| **Password** | `password` | Password | No | Leave empty on edit to keep the current password. |
| **Phone** | `alternative_phone` | International phone input | No | With a country code. |
| **Customer group** | `group_id` | Searchable dropdown | YES | Populated from `GET /admin/api/core/customers/groups`. Starts on group ID 1. Not clearable. |
| **Customer note** | `note` | Textarea | No | Max 191 chars (server-enforced). Help block: *"This note will not be visible to customer"*. Placeholder: *"Add customer note here"*. |

### Section: Custom fields (second card, only if store has custom fields defined)

- Info banner: blue info icon + *"These are custom fields that the customer can fill in, they can also be required."* + a **Manage fields** button on the right that opens [[customers-custom-fields]] in a new tab AND closes the modal.
- Fields are rendered in a **2-column grid** (split in half by index).
- Field renderers per type:
  - `text` / `link` → text input.
  - `textarea` → text area.
  - `phone` → international phone input.
  - `select` → searchable dropdown, not clearable.
  - `radio` → radio buttons with the field's option values.
  - `checkbox` → multiple checkboxes (each option separate); the value is stored as an ARRAY of option-IDs that are ticked.

### Panel title

- **+ Add customer** → *"Add customer"*.
- Identity-card pencil → **Edit customer** → the customer's full name.
- Notes card pencil → *"Add customer"*, though the panel edits this customer.

### Opening from the Notes card

The Notes card's pencil opens the full panel (identity fields and custom fields) with the **Customer note** field focused.

### Save behaviour

- POST `/admin/api/core/customers` on create, PATCH `/admin/api/core/customers/{id}` on edit.
- Empty custom-field values are left out of the save.
- An empty **Password** leaves the customer's stored password untouched.
- On success: toast *"Customer saved successfully"* and the panel closes. A new customer appears at the top of the list, and the merchant stays on the list. An edit updates the customer's page in place.
- Validation errors (HTTP 422) show in red next to each field.
- The panel blocks backdrop close while saving.
- A spinner shows while the customer and custom fields load.

## Business rules

### Email uniqueness scope (per-store) — verified

The email uniqueness check is scoped to the current store's customers table — each store has its own customers table in its own schema. So the same email CAN belong to different customer accounts in different CloudCart stores. Within one store, the email is unique across all customer accounts (both guest and registered).

### An email already in the store is refused

**+ Add customer** refuses an email that any customer in the store already has, registered or guest, with *"Customer email already exists"*.

### Field limits on the server

- **Note**: 191-character maximum.

### Plan-gate `customers` blocks create at cap

Every customer-create path (this panel, storefront registration, JSON-API v2 POST) checks the plan's customer cap. When the cap is reached, the create returns HTTP 402 and the merchant is redirected to `/admin/plan/feature/customers`. Existing customers continue to work; only NEW records are blocked. Add-on packs (+100 / +500 / +1000) stack — see [[plan-features]].

### Manage fields button closes the panel

Clicking the **Manage fields** button in the Custom fields card opens [[customers-custom-fields]] in a new tab AND closes the panel, with no prompt, so unsaved edits are discarded. The merchant should save first if they have pending input.

### Side effects on save

- `customer.created` (POST) or `customer.updated` (PATCH) webhook — see [[settings-hooks]].
- Subscriber record provisioned (when applicable); Marketing changes propagate — see [[customers-flags]].
- KPIs start at 0 — see [[customers-lifetime-kpis]].

## Related

- [[customers]] — hub.
- [[customers-custom-fields]] — custom-field definitions reached via Manage fields.
- [[customers-custom-groups]] — group picker source.
- [[customers-flags]] — Marketing flag side effects.
- [[customers-details]] — the customer's page, whose pencils open this panel.
- [[plan-features]] — `customers` cap + add-on packs.
- [[settings-hooks]] — `customer.created` / `customer.updated` webhooks.

## Open questions

None.
