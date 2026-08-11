---
type: feature
nav_path: "Customers → Custom fields"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["Customer custom fields", "Custom fields", "Custom customer fields", "Къстъм полета на клиенти", "Допълнителни полета"]
tags: [customers, custom-fields, checkout, fields]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 13
---

# Customer custom fields

## Purpose

The page where the merchant defines **additional fields** that appear on the storefront checkout to collect extra information from customers — beyond the platform's built-in name / email / phone / address fields. Examples: a *"Tax ID"* field for B2B customers, *"Preferred contact channel"* dropdown, *"Date of birth"* date input, *"Industry"* select with custom options, *"How did you hear about us?"* textarea, *"Newsletter consent"* checkbox.

Each field has a **technical name** (used internally for filtering / segmentation / API) and a **storefront name** (what the customer sees). The merchant can mark fields as required, allow the customer to modify them post-purchase, and link a text / phone / URL field to a platform **system field** so the value lands on the canonical customer record.

The page description (visible in the UI) reads: *"These fields appear in checkout to collect additional information from your customers."*

This page is the **hub** for the cluster. Each operational detail lives on a dedicated aspect page — drill into the one that matches the question.

## Where to find it

Sidebar → Customers (the breadcrumb starts from there) → **Custom fields** (or directly via `/admin/customers/custom-fields`).

Header icon: user-group icon. Page title: *"Custom fields"*.

## What the merchant can do here

- Browse, sort, and drag-reorder the list of defined custom fields — see [[customers-custom-fields-list-view]] for the table mechanics, status toggle, bulk delete, and the `/admin/api/core/customers/fields/sort` sort endpoint.
- Create a new custom field via the side-panel **+ Add custom field** modal, or edit an existing one by clicking its row name — see [[customers-custom-fields-editor-modal]] for the modal layout, type-tab selector, and type-conditional UI.
- Choose one of **7 supported field types** at creation: Dropdown, Radio, Checkbox, Text field, Text area, Phone, URL — see [[customers-custom-fields-types]] for the per-type behaviour and customer-facing UI.
- Link a text / textarea / phone / URL field to a platform **system field** so the customer's input also writes to the canonical customer record — see [[customers-custom-fields-system-linkage]] for the narrow `username` / `password` / `link` allowlist and write-back semantics.
- Mark fields as Required, Active, or "Allow customer to modify" — three independent toggles that control where and when the field appears (checkout vs My-Account profile) — see [[customers-custom-fields-storefront-behaviour]] for the storefront-side rules and the delete-all-then-insert account-page write pattern.

## Settings & fields

The merchant-facing list table on this page exposes six columns and one in-row toggle:

| Column | Notes |
|--------|-------|
| **Name** (`storefront_name`) | The customer-facing label. Click → Edit modal. |
| **Type** | Localised type label (Dropdown / Radio / Checkbox / Text field / Text area / Phone / URL field). |
| **Option values** | For select / radio / checkbox: comma-separated value list; for text-types: empty. |
| **Required** | Yes / No. |
| **Status** (`active`) | Active / Inactive toggle (calls the status endpoint per row). |
| **(actions)** | Per-row Delete (red trash). |

Default sort: ID descending (newest first). The full table behaviour (drag-reorder, Load all, bulk-select toolbar, per-row status toggle endpoint) is documented in [[customers-custom-fields-list-view]].

Per-field configuration in the editor modal — Field name (internal), Field name (storefront), Type, Active, Required, Allow customer to modify, System field, System field type, Field option values — is documented in [[customers-custom-fields-editor-modal]] (UI layout) and [[customers-custom-fields-validation-storage]] (server-enforced limits and uniqueness).

## Business rules

The cluster-wide rules a merchant needs to know up front:

- **Order of fields on storefront = drag-order on this page.** Reordering POSTs to the sort endpoint; the new order is the order customers see at checkout — see [[customers-custom-fields-list-view]].
- **Type is locked after create.** To change a field's type, the merchant must export data manually, delete the field (losing stored customer values), and create a new one — see [[customers-custom-fields-editor-modal]].
- **Required + Active + Allow customer to modify are independent toggles.** Active OFF hides the field from checkout but preserves stored values; Required ON only matters when the field is rendered; Allow customer to modify ON makes the field editable from the storefront My-Account profile — see [[customers-custom-fields-storefront-behaviour]].
- **Validation is required + type-native only.** No regex, no min/max length, no custom validators — see [[customers-custom-fields-validation-storage]].
- **System-field linkage writes BACK to the customer record.** When a text / phone / URL field is marked System and linked to a canonical key, the customer's checkout input lands on both the custom-field record AND the canonical customer column — see [[customers-custom-fields-system-linkage]].
- **Deleting a field removes stored customer values.** The cascade is hard-delete on the answers table — no archive, no soft-delete — see [[customers-custom-fields-validation-storage]].
- **No plan limit on field count.** Unlike customer groups, the platform imposes no plan-tier cap on the number of fields — see [[customers-custom-fields-programmatic-access]].

## Sub-pages (in this cluster)

This page is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[customers-custom-fields-list-view]] — list table, drag-reorder, status toggle, per-row delete, bulk-delete, Load-all paging.
- [[customers-custom-fields-editor-modal]] — Create / Edit side-panel modal: type tabs, sub-options, options sub-card, sticky Save header, Edit-mode locks.
- [[customers-custom-fields-types]] — the 7 supported types (Dropdown / Radio / Checkbox / Text / Textarea / Phone / URL); per-type configuration and customer-facing UI.
- [[customers-custom-fields-system-linkage]] — System-field linkage: the 3-key allowlist (`username` / `password` / `link`), write-back to canonical customer column, why it's narrower than the type variety suggests.
- [[customers-custom-fields-validation-storage]] — server-enforced validation rules, uniqueness constraints, shared `form_fields` table with `form = 'register'` scope, save transaction, delete cascade.
- [[customers-custom-fields-storefront-behaviour]] — checkout UX, My-Account profile write-back, delete-all-then-insert pattern, side effects on save / delete, use by segments and filters.
- [[customers-custom-fields-programmatic-access]] — JSON-API v2 status (no public CRUD on definitions), customer-tags contrast, plan gating, permission gating.

## Related

- [[customers]] — parent list (the breadcrumb).
- [[customers-details]] — custom-field values are visible on each customer's identity card.
- [[customer]] — entity page.
- [[marketing-segments]] — custom-field values queryable for building segments.
- [[settings-translations]] — `storefront_name` is translatable per storefront language.
- [[api-customer-tags]] — different concept (tags vs custom fields).
- [[json-api-v2]] — authentication and side-effects principle.
- [[plan-gates]] — gating-concept overview (this feature is NOT plan-gated).

## Open questions

None — all previously-flagged items resolved or distributed to aspect pages.
