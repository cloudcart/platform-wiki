---
type: feature
nav_path: "Customers → Custom fields → System-field linkage"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["System field linkage", "Customer custom field write-back", "Username password link allowlist", "System field toggle"]
tags: [customers, custom-fields, system-field, write-back]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Custom fields — system-field linkage

> Part of [[customers-custom-fields]]. See the hub for the other aspects (list view, editor modal, types, validation & storage, storefront behaviour, programmatic access).

## Purpose

System-field linkage is the mechanism by which a custom-field input on the storefront checkout writes BACK to the **canonical customer record** in addition to the custom-field answers table. When a merchant marks a text / textarea / phone / URL field as a System field and picks a canonical key, the customer's input lands on both: the standard customer column AND the custom-field record. This is what lets the merchant collect data via custom-field UX while keeping the platform's data model normalised.

## Where to find it

The **System field** toggle appears inside the editor modal at `/admin/customers/custom-fields` — see [[customers-custom-fields-editor-modal]]. It is rendered only when `data.type` is one of `text`, `textarea`, `phone`, `link`. Toggling it ON reveals a second collapse panel with the **System field type** dropdown (the canonical-key picker).

## What the merchant can do here

- **Mark a text / textarea / phone / link field as System.** The editor reveals an extra Active toggle labelled *"System field"* on the relevant types — see [[customers-custom-fields-editor-modal]] for the slide-up-down UI.
- **Pick a canonical key** from the System-field-type dropdown. The dropdown is populated from `keyOptions` and varies by the field's type:
  - For `text` / `textarea` / `phone`: dropdown offers **Username**, **Password**, **Link**.
  - For `link`: dropdown offers **Link** only.
- **Save** — the payload includes `system = 1` and `key = <selected canonical key>`. The backend enforces the allowlist at validation time.

## Settings & fields

### The 3-key allowlist

The backend's CustomFieldRequest validates `key` against the allowlist `in:username,password,link`. Any other value is rejected with the error message *"Key must be one of the following: username, password, link"*.

| Field type | Canonical keys exposed in the dropdown |
|------------|----------------------------------------|
| `text` | `username`, `password`, `link` |
| `textarea` | `username`, `password`, `link` |
| `phone` | `username`, `password`, `link` |
| `link` | `link` only |
| `select` / `radio` / `checkbox` | **NOT AVAILABLE** — System toggle hidden for Selection types |

### Save payload shape

When the editor's System toggle is ON, the Save payload always includes:

- `system = 1`
- `key = <one of username / password / link>`

When the toggle is OFF, `system = 0` is sent and the `key` field is omitted (and any previously-typed `data.key` is cleared on type-switch to a Selection group — see [[customers-custom-fields-editor-modal]]).

## Business rules

### System linkage writes BACK to the customer record

When a text / textarea / phone / link field is marked System and linked to a canonical key (`username` / `password` / `link`), the customer's input at checkout writes to **BOTH**:

1. The custom-field answer row in the answers table (per-customer, per-field — see [[customers-custom-fields-validation-storage]]).
2. The canonical customer-record column corresponding to the chosen key.

So if the merchant creates a System Username field, the customer's input gets stored on the canonical customer record's `username` column AND visible everywhere the platform reads that column (orders, profile, customer details). This is the **value** of the feature: collect alternate login credentials (or a canonical URL link) via friendly custom-field UX while having the data normalised into the standard model.

### The allowlist is narrow on purpose

Despite the wide variety of field types (text / textarea / phone / URL), System linkage **can ONLY** target three canonical keys: `username`, `password`, `link`. This is much narrower than the type variety suggests.

Common merchant misconceptions:

- A phone-type custom field **cannot** be linked to the canonical customer phone column. There is no `phone` key in the allowlist.
- A text-type custom field **cannot** be linked to canonical email, first_name, or last_name. None of those keys are in the allowlist.
- A textarea-type custom field cannot be linked to a canonical "notes" or "comments" column.

In practice the System-field feature is effectively for **collecting alternate login credentials** (`username` + `password`) and **one canonical URL link** (`link`). For other normalisation needs the merchant must either (a) use the standard customer-record fields directly through the customer Create / Edit screen, or (b) use a custom storefront / theme integration.

### Selection-type fields cannot be system-linked

Switching the editor type tabs TO `select` / `checkbox` / `radio` automatically resets BOTH `data.key = null` AND `data.system = 0` — see [[customers-custom-fields-editor-modal]]. The System toggle is hidden for the entire Selection type group. The rationale: option-value-type fields hold structured selections, not free-form values, so the canonical-key write-back model doesn't map.

This is a strict UI rule — there is no path in the modal to set `system = 1` on a Selection-type field. The backend's allowlist would also reject it because the canonical keys (`username` / `password` / `link`) all expect single-string values, not arrays.

### Switching field type clears the system-key

- Switching TO `link`: the editor **clears** the previously-typed `data.key` value (since only `link` is allowed for URL fields).
- Switching FROM a text-style type TO a Selection type: BOTH `data.key` AND `data.system` are reset.
- Switching between text / textarea / phone: the existing `data.key` is kept (all three allow the same `username` / `password` / `link` keys).

### Link-type fields can ONLY link to `link`

Even though `link` is a Text-style sibling in spirit, its System dropdown is restricted to the single key `link` — `keyOptions` filters out `username` and `password` when `data.type = link`. So a URL custom field can only be linked to the canonical URL field; there is no `username` / `password` option.

### Save / validate flow

Server-side validation:

- If `system = 1`, the `key` field is **required** and must be one of `username` / `password` / `link`.
- If `system = 0`, the `key` field is ignored.
- For Selection types (`select` / `radio` / `checkbox`) any non-zero `system` value is implicitly disallowed because the UI never sends it.

See [[customers-custom-fields-validation-storage]] for the full server-side validation rules and how the Save payload is wrapped in a transaction.

### My-Account write-back follows the same rules

When the customer edits a System-linked field on the storefront My-Account profile, the write still updates both the custom-field answer row AND the canonical customer column — see [[customers-custom-fields-storefront-behaviour]] for the delete-all-then-insert pattern that applies to `customer_modify = 1` fields.

## Related

- [[customers-custom-fields]] — hub.
- [[customers-custom-fields-editor-modal]] — where the System toggle appears.
- [[customers-custom-fields-types]] — which types are eligible for the toggle.
- [[customers-custom-fields-validation-storage]] — server-side allowlist enforcement.
- [[customers-custom-fields-storefront-behaviour]] — how the write-back behaves at checkout and from My-Account.
- [[customer]] — entity that receives the canonical write-back.

## Open questions

- Is there a way to extend the canonical-key allowlist? (Currently hard-coded to three keys — verify whether this is intentional.)
