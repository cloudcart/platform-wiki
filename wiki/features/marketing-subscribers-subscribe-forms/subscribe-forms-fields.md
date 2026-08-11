---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Fields"
route_name: ""
route_path: ""
aliases: ["Subscribe form fields", "Form input slots", "Custom fields on subscribe form", "Email field", "Phone field", "First name field", "Last name field", "Полета на формата"]
tags: [marketing, subscribers, forms, fields, custom-fields, validation, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list view, builder, templates, layout, triggers, submission flow, GDPR consent, known issues).

# Subscribe forms — input fields

## Purpose

What the visitor actually fills in. Each form has **four built-in input slots** (email, phone, first_name, last_name) — each with its own `is_visible` / `required` / label / placeholder / style — plus an arbitrary number of **custom fields** picked from the subscriber custom-field definitions ([[marketing-subscribers-custom-fields]]). Two caveats govern whether a built-in slot actually appears: **email and phone also require the matching store channel to be active**, and the **name slots expose no show/hide switch in their property panel** (see Business rules).

## Where to find it

Inside the form builder iframe (see [[subscribe-forms-builder]]) — the field configuration is on the `form` page. Stored on the form record as:

```
pages.form.fields.email = { is_visible, required, label, placeholder, fieldStyle, labelStyle }
pages.form.fields.phone = ...
pages.form.fields.first_name = ...
pages.form.fields.last_name = ...
pages.form.custom_fields[] = [ { id, is_visible, required, label, placeholder, ... } ]
```

## What the merchant can do here

- Control which built-in slots appear (`is_visible`) — subject to the caveats below: email / phone additionally require the store channel to be active, and the two **name** slots have no hide toggle in their property panel.
- Mark each visible slot as required vs optional.
- Override the default storefront label and placeholder.
- Apply custom styling to each input's field and label.
- Pick subscriber custom fields (text, textarea, phone, select, radio, checkbox) defined on [[marketing-subscribers-custom-fields]] to surface on the form.
- Configure per-custom-field required / label / placeholder / styling (same controls as built-in slots).

## Settings & fields

### Built-in input slots (form page)

Four fixed inputs the form can show. Each carries an `is_visible` flag in the form data (separate from `required`), but whether — and how — the merchant can flip that flag differs per slot (see the notes column and Business rules):

| Slot | Per-slot fields | Visibility gate |
|------|-----------------|-----------------|
| **Email** (`pages.form.fields.email`) | `is_visible`, `required`, custom label, placeholder, `fieldStyle`, `labelStyle`. | `email.is_visible` **AND** store **email channel** active. |
| **Phone** (`pages.form.fields.phone`) | Same — plus storefront uses E.164 validation per the store's default country. | `phone.is_visible` **AND** store **phone channel** active. |
| **First name** (`pages.form.fields.first_name`) | `is_visible`, `required`, label, placeholder, style. | `first_name.is_visible` only — **no** channel gate; **no** hide toggle in the field property panel. |
| **Last name** (`pages.form.fields.last_name`) | Same. | `last_name.is_visible` only — **no** channel gate; **no** hide toggle in the field property panel. |

### Per-field configuration flags

For each input slot:

| Per-field flag | Effect |
|----------------|--------|
| `is_visible` | Show the input in the form. |
| `required` | Make it a required field for submission. |
| `label` | Override the default storefront label. |
| `placeholder` | Override the default storefront placeholder. |
| `fieldStyle` / `labelStyle` | Custom CSS overrides. |

### Validation rules (in the platform code)

- `email` — `email` rule + `required` if marked required.
- `phone` — `phone_number_global:country.iso2` rule + `required` if marked required.
- `first_name`, `last_name` — `max:191` + `required` if marked required.
- For custom fields — type-specific rules (e.g. `array` + `in:` for checkboxes, `phone_number_global` for phone-type custom fields).

### Custom fields — 6 types

For anything beyond the four built-in slots, the merchant must define a **subscriber custom field** on [[marketing-subscribers-custom-fields]] and pick it via the form's *Custom fields* section. Available types (see [[marketing-subscribers-custom-fields]] for full detail):

- `text`
- `textarea`
- `phone`
- `select`
- `radio`
- `checkbox`

The custom field picker on the form selects from the merchant-defined SubscriberFormFields catalogue. Each picked field has its own visibility / required / label / placeholder / styling controls — identical shape to the built-in slots.

### Custom-field type coercion at submit

For each submitted custom field, the backend re-checks the field's `type` against the form's allowed custom-field list and coerces:

- **`checkbox`** — value must be an array; only values whose option `value` exists in the field's options are kept; result is an array attached as `[value => value]`.
- **`radio` / `select`** — value must match one of the field's option `value`s; otherwise dropped.
- **`text` / `textarea` / `phone`** — non-null, non-empty value is kept as-is.

Invalid or unknown field ids are **silently skipped** — no error returned to the visitor. This guards against tampered submissions trying to set fields the form didn't expose. See [[subscribe-forms-submission-flow]] for the full submit pipeline.

## Business rules

### At least one of email or phone must be collected

The submission flow extracts email and/or phone only for the channels configured at the store level. A form with neither email nor phone visible has nothing to save and the subscriber row creation would silently no-op (verify).

### Channel filtering — a disabled store channel removes the email / phone field (top cause of "the email field isn't showing")

The store-level communication channels gate **only the email and phone** built-in slots — **first name and last name have no channel dependency**. For email and phone, the slot is active only when **both** its own `is_visible` flag is on **and** the matching store channel is active:

- **Email** requires `email.is_visible` **AND** the store's **email channel** being active (`email.is_visible && channels.has('email')`); **phone** requires `phone.is_visible` **AND** an active **phone channel**. So if the merchant switched the email channel OFF (Marketing → Channels), the email input is **removed from the working form** — no matter what the form's own `is_visible` / label settings say. This is the #1 reason a merchant reports "the email field is not showing": check the store's channels first, not the form. Same for phone.
- **Submit save:** the submission flow extracts email / phone only for the store's configured channels, so even a submitted value for a switched-off channel is dropped from the saved subscriber. A form built while a channel was active and then disabled later stops collecting that channel. See [[subscribe-forms-submission-flow]].

The store channels **override** the form's per-field `is_visible` for email / phone — the form cannot force-show an input for a channel the store has switched off. **First name / last name are never channel-gated** — their appearance depends on `is_visible` alone.

### The name slots have no show/hide switch in their property panel

The form data model carries an independent `is_visible` flag for **every** built-in slot, including `first_name` and `last_name` — so a form can technically store `last_name.is_visible = false`, and the submit validation honours it (a hidden name field is simply not validated or collected). **But the builder's field-property panel for the two name slots exposes only `required` / label / placeholder / styling — no per-field show/hide toggle.** Email and phone gain an effective on/off control from the store channel (disable the channel → the slot disappears), whereas the name slots have no such external gate. So from the standard form editor a merchant does **not** see a "hide first name / last name" option. Whether any other builder gesture clears `is_visible` for a name slot is not confirmed here. (verify — the exact builder control, if any, that sets `first_name.is_visible` / `last_name.is_visible`.)

### Built-in slots are fixed — no rename / no reordering

The four built-in slots (`email`, `phone`, `first_name`, `last_name`) are keyed by name and cannot be renamed at the schema level — only labelled differently via `label`. They render in a fixed order set by the storefront module; the merchant cannot drag-reorder them. To insert content between them, the merchant uses custom fields which slot in their own rendering position.

### No file-upload field type

The 6 custom-field types are `text`, `textarea`, `phone`, `select`, `radio`, `checkbox` — there is no `file` upload type, no `image` type, no `date` picker. See [[subscribe-forms-known-issues]].

### Required-flag at the field level vs marketing-policy gate

A required built-in or custom field is a hard validation block — the visitor can't submit until it's filled. This is separate from the **marketing-policy gate** (`terms` array of legal pages) — required terms checkboxes are also validation rules at submit, but conceptually they are GDPR consent gates, not data collection. See [[subscribe-forms-gdpr-consent]].

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[marketing-subscribers-custom-fields]] — defines the custom fields the form picks from; documents the 6 types in detail.
- [[subscribe-forms-builder]] — where field configuration lives.
- [[subscribe-forms-submission-flow]] — how submitted values are validated, coerced, and saved.

## Open questions

- Whether a form with NO email and NO phone visible can be saved at all, and what happens at submit time. (verify)
