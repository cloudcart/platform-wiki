---
type: feature
nav_path: "Marketing → Subscribers → Custom Fields → Field types"
route_name: subscribers-fields-list-new
route_path: /admin/marketing-new/subscribers/fields
aliases: ["Subscriber custom field types", "Selection vs text fields", "Subscriber field type locked", "Dropdown radio checkbox text textarea phone", "Subscriber field families"]
tags: [marketing, subscribers, custom-fields, types]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers-custom-fields]]. See the hub for the other aspects (list page, editor modal, downstream surfaces).

# Subscriber Custom Fields — the six field types

## Purpose

This page documents the **six field types** a subscriber custom field can take, the two families they group into (Selection vs Text), how each behaves downstream, and the hard rule that **a field's type is locked once it is created**.

## Where to find it

The type is chosen in the **Choose field type** picker (Card 1) of the Create / Edit modal — Sidebar → **Marketing** → **Subscribers** → **Custom fields** → **Add custom field**. See [[subscribers-custom-fields-editor]] for the modal layout. The Type also appears as a column and a filter on [[subscribers-custom-fields-list]].

## What the merchant can do here

- Pick one of six types when creating a field.
- The picker is split into two visual tabs — **Selection** and **Text fields** — to reinforce the two families.
- The type radio shows a descriptive label per type (below).

Type-specific labels shown in the radio:

| Type key | Radio label |
|----------|-------------|
| `select` | Dropdown - select from list |
| `radio` | Radio button - single choise |
| `checkbox` | Checkbox - multiple choise |
| `text` | Text field - short text |
| `textarea` | Text area field - longer text |
| `phone` | Phone |

## Settings & fields

| Type key | Family | UI label | Behaviour |
|----------|--------|----------|-----------|
| `select` | Selection | Dropdown | Single-pick from a configured option list. Renders Card 2 (option values). |
| `radio` | Selection | Radio button | Single-pick from a configured option list. Renders Card 2. |
| `checkbox` | Selection | Checkbox | Multi-pick from a configured option list. Renders Card 2. |
| `text` | Text | Text field | Free-input short text. No options. |
| `textarea` | Text | Text area | Free-input longer text. No options. |
| `phone` | Text | Phone | Free-input text with phone-formatting behaviour. No options. |

`type` allowed values (server-validated): `checkbox, select, radio, text, textarea, phone`. The full cap table is on the hub: [[marketing-subscribers-custom-fields]].

## Business rules

### Selection family vs Text family

The six types group into two families that behave differently downstream:

- **Selection family** (`select`, `radio`, `checkbox`) — has an `options` list; the storefront renders the configured choices, and the segment-condition picker lets the merchant filter by which option the subscriber picked. `checkbox` allows multi-pick; `select` and `radio` are single-pick. These are the only types that show Card 2 (Field option values) in the modal — see [[subscribers-custom-fields-editor]].
- **Text family** (`text`, `textarea`, `phone`) — free-input; no `options`. `phone` is just a text input with phone-formatting behaviour (no dial-code dropdown configuration here — that lives on the subscribe-form builder, see [[marketing-subscribers-subscribe-forms]]).

The type radio is split into the two visual tabs (*Selection*, *Text fields*) to reinforce this grouping. On the list page the families differ visibly too: selection types show an Option values count, text types show **N/A** — see [[subscribers-custom-fields-list]].

### Type cannot be changed after creation

Once a custom field is saved, its type is **locked**. The edit modal disables the type tabs and radio. Reason: existing subscriber values were stored against the original type's shape (option references for selection fields, free text for text fields); switching would orphan or misinterpret stored data. To change type, the merchant must delete the field (which removes all stored subscriber values for it — see [[subscribers-custom-fields-downstream]]) and create a new one.

The lock is also enforced server-side, not just in the UI: on edit the backend does not read or alter the field's type from the request — a forced type change is silently ignored with no error. See [[subscribers-custom-fields-editor]].

### Why the family matters downstream

In [[marketing-segments]], the `subscriber.custom_field` condition behaves differently per family: only selection-type fields produce a populated option list to pick from; text-type fields match against the typed value itself. See [[subscribers-custom-fields-downstream]] for the full downstream picture.

## Related

- [[marketing-subscribers-custom-fields]] — hub.
- [[subscribers-custom-fields-editor]] — the modal where the type is picked (and locked on edit).
- [[subscribers-custom-fields-list]] — Type column + Type filter; option-count vs N/A by family.
- [[subscribers-custom-fields-downstream]] — how each family behaves in segment conditions.

## Open questions

No outstanding questions.
