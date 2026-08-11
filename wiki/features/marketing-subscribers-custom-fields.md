---
type: feature
nav_path: "Marketing → Subscribers → Custom Fields"
route_name: subscribers-fields-list-new
route_path: /admin/marketing-new/subscribers/fields
aliases: ["Subscriber Custom Fields", "Custom Subscriber Fields", "Subscriber custom attributes", "Персонализирани полета (абонати)", "Допълнителни полета на абонати"]
tags: [marketing, subscribers, custom-fields, schema]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Subscriber Custom Fields

## Purpose

The merchant's screen for **defining the per-subscriber attributes** that go beyond the built-in name / email / phone — e.g., birthday, T-shirt size, preferred language, segment-tagging dropdowns, or any other data the store wants to collect from the audience. Each custom field defined here becomes (a) a question the merchant can drop into [[marketing-subscribers-subscribe-forms]], (b) a column visible on a subscriber's profile, and (c) a condition the merchant can use in [[marketing-segments]] (*"where custom field ':field' is ':options'"*).

The page's own header text explains the intent: *"Custom fields can be used in popup forms to collect additional information from your subscribers."* Fields defined here are **distinct from customer custom fields** (see [[customers-custom-fields]]) — the two share one underlying table but live in **independent namespaces** scoped to `form = 'subscriber'`. See [[subscribers-custom-fields-downstream]].

This is the **hub page** for the subscriber-custom-fields cluster. It carries the high-level definition + plan gates; the list-page interactions, the create/edit modal, the six field types, and the downstream surfaces each live in their own aspect page (see below).

## Sub-pages (in this cluster)

This screen is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read the whole cluster.

- [[subscribers-custom-fields-list]] — the list page: columns, the Type filter, search, drag-reorder (`sort_order`), single + bulk delete, the option-values count cell, where-to-find.
- [[subscribers-custom-fields-editor]] — the Create / Edit field modal: the two cards (Field settings + Field option values), per-field validation, the option diff-on-save behaviour, the 250-option cap.
- [[subscribers-custom-fields-types]] — the six field types, the Selection vs Text families, and why the type is **locked after creation**.
- [[subscribers-custom-fields-downstream]] — where a defined field surfaces (subscribe forms, subscriber detail, segments), the name-uniqueness namespace, deletion cascade, and the legacy admin screen.

## Where to find it

Sidebar → **Marketing** → **Subscribers** → **Custom fields**.

The route is `/admin/marketing-new/subscribers/fields`. Breadcrumb: Marketing → Subscribers → Custom fields.

A legacy version of the same screen still exists at `/admin/subscribers/fields` (old admin); the modern Vue page replaces it — see [[subscribers-custom-fields-downstream]] for the differences.

## What the merchant can do here

- **Define custom fields** of six types (Dropdown, Radio button, Checkbox, Text field, Text area, Phone) via the Create field modal — see [[subscribers-custom-fields-editor]] and [[subscribers-custom-fields-types]].
- **Manage the list** — see all fields, filter by Type, search by name, drag-reorder, edit (click the name), single-delete and bulk-delete — see [[subscribers-custom-fields-list]].
- **Use the fields downstream** — drop them into subscribe forms, view their values on subscriber profiles, and filter segments by them — see [[subscribers-custom-fields-downstream]].

What the merchant CANNOT do here (cluster-wide gaps):

- **Cannot change a field's type after creating it** — the type is locked; the merchant must delete and recreate. See [[subscribers-custom-fields-types]].
- **No JSON-API surface for the field definitions themselves** — they are admin-managed.
- **No per-field `required` toggle on this screen** — `required` is set on the subscribe form that uses the field, not on the field definition. See [[subscribers-custom-fields-downstream]].

## Settings & fields

The full field set is documented per-aspect:

| Surface | Aspect page |
|---|---|
| List columns (Name, Type, Option values, Sort order, actions) | [[subscribers-custom-fields-list]] |
| Create / Edit modal — Card 1 (Field settings) | [[subscribers-custom-fields-editor]] |
| Create / Edit modal — Card 2 (Field option values) | [[subscribers-custom-fields-editor]] |
| The six `type` values + Selection / Text families | [[subscribers-custom-fields-types]] |
| Downstream rendering (subscribe forms, segment picker, subscriber detail) | [[subscribers-custom-fields-downstream]] |

### Confirmed backend caps & validation (cluster-wide)

| Rule | Value |
|------|-------|
| Internal `name` — min / max length | 1 / 191 |
| Internal `name` — uniqueness | scoped to subscriber fields only (`form = 'subscriber'`) |
| `storefront_name` — max length | 191 |
| `type` — allowed values | `checkbox, select, radio, text, textarea, phone` |
| `options` — required when | `type in [select, radio, checkbox]` |
| `options` — array max | 250 rows |
| `options.*.name` — min / max | 1 / 191 |

Error strings and the per-surface detail live on the aspect pages above.

## Business rules

- **Subscriber fields are a separate namespace from customer fields.** A boot hook always tags these records `form = 'subscriber'`, and a global scope auto-filters every query to subscriber-only — so a name that already exists as a [[customers-custom-fields|customer custom field]] does NOT block creating it here. See [[subscribers-custom-fields-downstream]].
- **Type is immutable after creation** — existing subscriber values were stored against the original type's shape, so switching would orphan or misinterpret the data. See [[subscribers-custom-fields-types]].
- **Sort order propagates everywhere the fields render as a list** — the subscribe-form builder picker, the storefront form, and the segment-condition picker all honour the drag order set on the list page. See [[subscribers-custom-fields-list]].
- **Deletion cascades and is permanent** — removing a field deletes its definition AND all stored per-subscriber values, with no undo. See [[subscribers-custom-fields-downstream]].

## Related

- [[subscribers-custom-fields-list]] — the list page (aspect).
- [[subscribers-custom-fields-editor]] — the create / edit modal (aspect).
- [[subscribers-custom-fields-types]] — the six types + type-lock (aspect).
- [[subscribers-custom-fields-downstream]] — downstream surfaces + deletion + legacy admin (aspect).
- [[marketing-subscribers]] — parent screen; subscribers carry these field values.
- [[marketing-subscribers-subscribe-forms]] — primary downstream consumer; subscribe forms pick which custom fields to show.
- [[marketing-segments]] — segments use the `subscriber.custom_field` condition to filter by these fields.
- [[marketing]] — section hub.
- [[customer]] — entity page; customer custom fields are a **separate** namespace.
- [[customers-custom-fields]] — the customer-side equivalent screen (separate cluster).
- [[subscriber]] — entity page; subscribers store these field values.

## Plan gates

This feature has **NO direct plan-feature mapping** (verified against backend). See [[plan-gates]] for the gating-concept overview.

| Mapping | Shape | What it controls |
|---|---|---|
| (none directly) | — | No `subscriber_fields` feature key exists. The merchant can define as many fields as needed; the only enforced caps are the server-side validation rules above. |
| `subscriber_forms` (effective gate) | Numeric (max subscribe forms) | Custom fields are only USEFUL once at least one subscribe form displays them — and subscribe forms ARE plan-gated. See [[marketing-subscribers-subscribe-forms]]. Without a subscribe-form slot, defining fields here has no storefront effect. |
| `segments` / `subscribers` (downstream) | Numeric | Field values are queryable in [[marketing-segments]] conditions, but segment + subscriber counts are gated separately. The fields themselves stay free to define. |

Access to this page is **permission-gated** (`marketing.subscribers` middleware), not plan-gated. The upgrade pressure surfaces on [[marketing-subscribers-subscribe-forms]] when the merchant tries to use the fields they defined.

## Open questions

- 📡 **Plan gating.** No `subscriber_fields` feature key. Effectively gated by the `subscriber_forms` plan-feature since custom fields are only useful when at least one subscribe form exists. GraphQL-resolvable: query the merchant's current plan + feature-pack stacks to read the `subscriber_forms` feature state.
