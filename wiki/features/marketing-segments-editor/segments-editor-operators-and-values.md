---
type: feature
nav_path: "Marketing → Segments → Editor → Operators & values"
route_name: segments.core_new.list
route_path: /admin/marketing-new/segments
aliases: ["Segment editor operators", "Segment editor value controls", "Segment condition operator vocabulary", "Segment condition value kinds", "Value control vocabulary"]
tags: [marketing, segments, editor, operators, value-controls]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-segments-editor]]. See the hub for the other aspects (modal layout, condition builder, create popup, validation, save pipeline, plan gates).

# Segment editor — operators & values

## Purpose

Every condition row in the editor has an **operator** (the comparison verb) and a **value** (the right-hand side). The operator vocabulary depends on the condition's `value_kind`; the value-control vocabulary depends on the condition's identity. This page catalogues both vocabularies. The row mechanics around these modules are on [[segments-editor-condition-builder]].

## Where to find it

Inside any condition row in the Segment editor modal, between the condition picker (left) and the action icons (right). Hidden entirely when the condition's schema has `allow_value = false`.

## What the merchant can do here

- **Pick the comparison verb** (operator) — available operators depend on the condition's `value_kind`. See the operator table below.
- **Enter or pick the right-hand value** — the value-control module changes with the condition (multi-select, autocomplete, date picker, currency input, etc.). See the value-control table below.
- **Switch the City picker scope** by first picking a Country in a parent / sibling Country condition.
- **Combine cascading dropdowns** for Device type (Type → Manufacturer → Model) and Subscriber custom field (Field → Option).

## Settings & fields

### Operator vocabulary by condition value kind

| Value kind / condition | Operator options | UI labels (English) |
|------------------------|------------------|---------------------|
| **Default** (most multi-select / single-pick conditions) | `=`, `<>` | Is / Is not |
| **Numeric** — `Amount`, `Price`, `Average`, currency conditions, numeric `valueKind` | `=`, `<>`, `<`, `>` | Exactly / Not equal to / Less than / More than |
| **Click rate**, **Open rate** | `=`, `<>`, `<`, `>` | Exactly / Not equal to / Less than / More than |
| **Date interval** (`date_interval`, `last_active`, `membership_expiration`) | `before_more_than`, `in_last` | More than / In the last |
| **Exact date** (`date`) | `=`, `<>`, `<`, `>` | Is / Is not / Before / After |
| **Customer** condition | `=`, `<>` | Is / Is not |
| **Product / Category / Vendor / Order product** (needs the rich product filter) | `any`, `=`, `<>` | Any / Is / Is not |
| **Page** (`landing page`) | `=`, `<>` | Is / Is not |
| **Text input** — First name, Last name, channel-identifier `contains` | `=`, `<>`, `begin`, `not_begin`, `contains`, `not_contains`, `end`, `not_end` | Is / Is not / Begins with / Does not begin with / Contains / Does not contain / Ends with / Does not end with |
| **Membership** | `any`, `=`, `<>` | Any / Is / Is not |
| **Feedback rating** (apps.product_review) | `>` only | More than |

The operator-select control offers no clear button — the operator is always one of the allowed values for the chosen condition.

### Value-control vocabulary

| Condition type | Value control |
|----------------|---------------|
| **Channel** (`subscriber.channel`) | Multi-select tags: Email / Phone / WebPush. (Messenger is currently commented out.) |
| **Channel verified** (`subscriber.channel.verified`) | Single-select with one option "Verified" (no clear — value is always `1`). |
| **Verified email / channel identifier substring** | Text input. |
| **Date** (`date`) | Single date picker (emits `YYYY-MM-DD`). |
| **Date interval** | Number input (0+) + interval-type select (Minutes / Hours / Days). When operator is `before_more_than` the labels read "Minutes ago / Hours ago / Days ago"; on `in_last` it is just "Minutes / Hours / Days". |
| **Membership expiration** | Number + (Hours / Days) only. Same "ago" suffix logic as date interval. |
| **Abandoned cart** (`cart.abandoned`) | Single-select with one option "Abandoned" (no clear). |
| **Order status fulfillment** | Single-select with one option "Fulfilled" (no clear). |
| **Order last** / **Last comment** | Single-select with one option "Last" (no clear). |
| **Country** (`country`) | Multi-select country picker (`CcCountries`). |
| **City** (`country.region`) | Multi-select cities — **depends on the parent Country condition**: until at least one country is picked, the city picker is disabled and the search API is country-filtered. |
| **Customer** | Multi-select autocomplete against `/admin/api/core/customers/autocomplete` — shows `<full_name> (<email>)`. |
| **Products / Categories / Vendors** | The rich `CcProductsFilter` component with filter-type (Product / Category / Vendor), an in-filter operator (in / not_in mapped to `=` / `<>`), and a multi-select against `/admin/api/core/products/search` (or vendors / categories). Hidden when operator is `any`. |
| **Page** (`page` / `membership`) | Multi-select tag-mode against `/admin/api/core/pages/search` (with `filter[private]=1` for membership pages). Hidden when operator is `any` for membership. |
| **Browser**, **OS** | Multi-select tag-mode against `/admin/api/core/browser/search` / `/admin/api/core/os/search`. Hidden when operator is `any`. |
| **Device type** | Three cascading dropdowns: **Type** → **Manufacturer** → **Model**. Manufacturer is disabled until a Type is picked; Model is disabled until a Manufacturer is picked. APIs: `/admin/segments/autocomplete/device-type`, `/admin/segments/autocomplete/device-manufacturer`, `/admin/segments/autocomplete/device-model`. |
| **Subscriber custom field** | Two dropdowns: **Field** (against `/admin/segments/autocomplete/custom-fields`) → **Option** (against `/admin/segments/autocomplete/custom-fields-options` filtered by field id). Option is disabled until a field is picked. See [[marketing-subscribers-custom-fields]]. |
| **Tag** (`tag`) | Tag picker — uses `/admin/autocomplete/customer-tags` (customer tag) by default; if the parent mapping includes `product_tag` the API switches to `/admin/api/core/product-tags/search`. |
| **UTM source / medium / campaign** | Tag picker against `/admin/autocomplete/order-meta` with the corresponding `filter[parameter]` (`utm_source` / `utm_medium` / `utm_campaign`). |
| **Order status** | Tag picker against `/admin/api/core/settings/statuses/order`. |
| **Payment** | Tag picker against `/admin/payment-providers` — filtered client-side to only providers that are both `active = yes` AND `installed = true`. |
| **Shipping** | Tag picker against `/admin/api/shipping/search`. |
| **Discount** | Tag picker against `/admin/api/core/discounts/search`. |
| **Customer group** | Tag picker against `/admin/api/core/customer-groups/search`. |
| **Vendor** (standalone) | Tag picker against `/admin/api/core/vendors/search`. |
| **Times** (under `view.product` etc.) | Number input + a **Grouped by record** switch (controls whether to count product views aggregated by product or by event row; serialised as `meta.group_by = 'record_id'`). |
| **Amount / Price / Average** (currency) | Currency input (formatted with the store's currency). |
| **Click rate / Open rate** | Percentage input (0–100). |
| **Default** (text values) | Plain text input. |

## Business rules

- **Operator depends on `value_kind`, not on the condition's identity.** Two conditions with the same `value_kind` get the same operator set. The `value_kind` is declared on the meta endpoint's schema (see [[segments-editor-validation]]).
- **Cascading value controls gate child dropdowns on the parent.** City is disabled until a Country is picked; Device type Manufacturer is gated by Type and Model by Manufacturer; Subscriber custom field Option is gated by Field (see [[marketing-subscribers-custom-fields]]).
- **Payment value control filters client-side.** Shows only providers with `active = yes` AND `installed = true`.
- **`any` operator hides the rich filter** for Products / Categories / Vendors / Membership.
- **Tag value-control switches API by parent mapping.** Customer-scoped parents hit `/admin/autocomplete/customer-tags`; parents whose mapping includes `product_tag` hit `/admin/api/core/product-tags/search`.
- **`channel.verified` always emits `value = 1`** and **Date values emit `YYYY-MM-DD`** (time stripped) — the save-payload builder forces both (see [[segments-editor-save-pipeline]]).

## Related

- [[marketing-segments-editor]] — hub.
- [[segments-editor-condition-builder]] — the row anatomy that hosts these modules.
- [[segments-editor-validation]] — how meta + scoped schema feed the operator + value vocabulary; field-mapped errors.
- [[segments-editor-save-pipeline]] — value normalisation on save (date stripping, `channel.verified` forced `value = 1`, date-interval validity check).
- [[marketing-subscribers-custom-fields]] — backs the Subscriber-custom-field value control.

## Open questions

No outstanding questions.
