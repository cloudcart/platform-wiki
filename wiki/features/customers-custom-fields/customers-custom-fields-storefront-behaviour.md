---
type: feature
nav_path: "Customers → Custom fields → Storefront behaviour"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["Custom fields storefront UX", "Custom fields My-Account profile", "Custom fields checkout", "Custom field segments", "customer_modify"]
tags: [customers, custom-fields, storefront, checkout, my-account]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Custom fields — storefront behaviour

> Part of [[customers-custom-fields]]. See the hub for the other aspects (list view, editor modal, types, system linkage, validation & storage, programmatic access).

## Purpose

This aspect documents how a saved custom-field definition behaves on the **storefront** — when the customer sees the field at checkout, when they can edit it again from the My-Account profile, what happens on save / delete to the cached checkout pages, and how the values flow into segments and filters on the admin side.

## Where to find it

Storefront surfaces (customer-facing):

- **Checkout** — every Active field appears in the order the merchant set on the admin list (see [[customers-custom-fields-list-view]]).
- **My Account → Profile** — only fields with `customer_modify = 1` appear here for later editing.

Admin surfaces that consume the customer answers:

- [[customers-details]] — custom-field values appear in the customer's identity card.
- [[customers]] — list filters can filter by custom-field value when configured.
- [[marketing-segments]] — segment builder can target customers by custom-field value.

## What the merchant can do here

The merchant configures three **independent toggles** on each field that together determine the storefront behaviour:

- **Active** (toggle) — when OFF, hides the field from storefront checkout. Existing stored values stay on the customer record.
- **Required** (toggle) — when ON, the customer cannot complete checkout without filling this field. Only meaningful when Active = ON.
- **Allow customer to modify** (toggle, `customer_modify` column) — when ON, the field also appears on the My-Account profile; when OFF, the field is checkout-only and the customer cannot change their answer later.

See [[customers-custom-fields-editor-modal]] for where these toggles live in the editor UI.

## Settings & fields

### Storefront-side rendering rules

| Setting | Effect at checkout | Effect on My-Account profile |
|---------|-------------------|------------------------------|
| `active = 1`, `customer_modify = 1` | Field rendered | Field rendered (editable) |
| `active = 1`, `customer_modify = 0` | Field rendered | Field hidden (checkout-only) |
| `active = 0` | Field hidden | Field hidden |
| `required = 1` (when rendered) | Submit blocked until filled | Submit blocked until filled |
| `system = 1` + `key` set | Writes BOTH to answer row AND canonical customer column | Same write-back rules apply — see [[customers-custom-fields-system-linkage]] |

### Order at checkout

The order in which Active fields appear at checkout is the **drag-order** the merchant set on the admin list page — see [[customers-custom-fields-list-view]]. There is no per-language or per-step override; the order is store-wide.

### What the customer sees

- **Label**: the `storefront_name` (translatable per language via [[settings-translations]]).
- **Input**: the type-native widget — see [[customers-custom-fields-types]] for the 7 supported renderings.
- **Validation**: Required + type-native (phone via libphonenumber, URL format). No regex, no length limits — see [[customers-custom-fields-validation-storage]].

## Business rules

### My-Account profile uses delete-all-then-insert

Custom-field values submitted from the customer's storefront My-Account profile follow a **delete-all-then-insert** pattern:

1. The platform queries the customer's existing answer rows where the underlying field has `customer_modify = 1`.
2. **Deletes ALL** of them.
3. **Inserts** the new POST.

A field not in the POST body is treated as an **explicit unset** — its previous value is cleared. Any client-side bug that drops a hidden field from the submission will silently wipe that answer. Fields with `customer_modify = 0` are not affected — they remain untouched.

### Checkout flow is append-only

At checkout the platform inserts the submitted answers. Subsequent edits go through the My-Account flow (delete-all-then-insert above) or admin staff via the Edit Customer modal.

### Side effects on save / delete

- **Create / Edit** of a definition — storefront checkout pages are **cache-flushed** so the new (or changed) field appears on the next customer visit. The admin doesn't need to manually clear the cache.
- **Delete** of a definition — removes the field definition AND every customer's stored answer for that field (hard cascade — see [[customers-custom-fields-validation-storage]]). The storefront checkout cache is also flushed.
- **Drag-reorder** on the admin list — only changes `sort_order` values; existing stored data is unaffected. The cache is flushed so the new order takes effect on the next storefront page render.

### Storefront translation

The `storefront_name` is translatable per storefront language via [[settings-translations]]. The internal `name` is not translatable (it's used in API / filters / segmentation, not customer-facing).

### Customer data is queryable for segments and filters

Stored custom-field answers feed three admin-side surfaces:

- **[[marketing-segments]]** — the segment builder can target customers by custom-field value. Useful for building lists like *"customers who answered Industry = Retail"* for campaign targeting.
- **[[customers]] list filters** — the customer-list filters can match custom-field values when configured.
- **[[customers-details]] identity card** — the per-customer details page shows custom-field answers in the customer's identity card.

This is why the **internal** `name` matters even though it's not customer-facing — segments, filters, and integrations reference the field by its internal name.

### Required is only enforced when rendered

A field marked Required but with Active OFF does **not** block checkout — the field isn't rendered, so the Required flag has no effect. The combination is valid (a merchant might Deactivate a Required field temporarily without flipping Required), but the merchant should know it doesn't affect storefront flow until they reactivate the field.

### Active OFF does not lose stored data

Toggling Active = OFF only hides the field from the storefront. Every existing customer's answer remains on the `customers_custom_fields` answers table and is still visible on the [[customers-details]] identity card, still queryable by [[marketing-segments]], and still exportable. Reactivating the field brings it back as-is — no migration step required.

### My-Account renders only `customer_modify = 1` fields

If the merchant wants a checkout-only field (collected once, locked forever), they leave **Allow customer to modify** OFF. If they want the customer to be able to update their answer later, they turn it ON — the field then appears on My Account → Profile and the customer's edit triggers the delete-all-then-insert behaviour described above.

### System linkage applies on both surfaces

When a field is marked System and linked to a canonical key (`username` / `password` / `link`), the write-back to the canonical customer column happens at **both** checkout and My-Account submit — see [[customers-custom-fields-system-linkage]]. This is the cleanest way for the merchant to collect a piece of data via custom-field UX and have it normalised onto the standard customer record.

## Related

- [[customers-custom-fields]] — hub.
- [[customers-custom-fields-list-view]] — drag-order that determines checkout-field order.
- [[customers-custom-fields-editor-modal]] — where the merchant toggles Active / Required / Allow customer to modify.
- [[customers-custom-fields-types]] — type-native rendering on the storefront.
- [[customers-custom-fields-validation-storage]] — what gets persisted on submit.
- [[customers-custom-fields-system-linkage]] — write-back to the canonical customer column.
- [[customers]] — list filters consume custom-field values.
- [[customers-details]] — identity card surfaces custom-field values.
- [[marketing-segments]] — segment builder consumes custom-field values.
- [[settings-translations]] — `storefront_name` translation per language.

## Open questions

- When a Selection-type option label is renamed (option-value rename), do the storefront's stored answers for that option get re-mapped or invalidated? (Inherited from the original page — verify exact behaviour.)
