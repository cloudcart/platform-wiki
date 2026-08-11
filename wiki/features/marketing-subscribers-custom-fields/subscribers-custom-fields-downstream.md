---
type: feature
nav_path: "Marketing → Subscribers → Custom Fields → Downstream surfaces"
route_name: subscribers-fields-list-new
route_path: /admin/marketing-new/subscribers/fields
aliases: ["Subscriber custom fields downstream", "Where subscriber custom fields appear", "Subscriber custom fields deletion", "Subscriber vs customer field namespace", "Subscriber custom fields legacy admin"]
tags: [marketing, subscribers, custom-fields, segments, deletion]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers-custom-fields]]. See the hub for the other aspects (list page, editor modal, field types).

# Subscriber Custom Fields — downstream surfaces, namespace & deletion

## Purpose

A defined subscriber custom field is only useful because of where it surfaces. This page documents the **three downstream consumers** (subscribe forms, subscriber detail, segments), the **subscriber-vs-customer namespace** that keeps the two field sets independent, what happens when a field is **deleted**, and the **legacy admin** version of the screen.

## Where to find it

The field definitions are managed at Sidebar → **Marketing** → **Subscribers** → **Custom fields** (`/admin/marketing-new/subscribers/fields`). Their downstream surfaces are reached from:

- [[marketing-subscribers-subscribe-forms]] — the subscribe-form builder's *Custom fields* picker.
- [[marketing-subscribers]] — a subscriber's detail / profile view.
- [[marketing-segments]] — the segment-condition picker.

## What the merchant can do here

From the downstream surfaces, the merchant can:

- **Add a custom field to a subscribe form** and mark it `required` on that form.
- **Read a subscriber's stored values** on their profile.
- **Filter a segment** by a custom field's value.

These are described per surface below; the field definitions themselves are created on [[subscribers-custom-fields-editor]].

## Settings & fields

### Where a defined field surfaces (three consumers)

1. **Subscribe forms** ([[marketing-subscribers-subscribe-forms]]): in the form builder's *Custom fields* picker, the merchant picks which custom fields to include on a given form and whether each is `required`. The storefront renders the field using its `storefront_name` (or `name` if empty), and submissions populate the subscriber's custom-field values. Note: per-field `required` is set on the **form**, not on the field definition.
2. **Subscriber detail view** ([[marketing-subscribers]]): a subscriber's stored custom-field values appear on their profile.
3. **Segment conditions** ([[marketing-segments]]): the `subscriber.custom_field` condition renders as *"where custom field ':field' is ':options'"* (or *"is not"* for negation). The merchant picks the field, then picks the option(s) — only selection-type fields produce a populated `option` list; text-type fields use the typed value itself. See [[subscribers-custom-fields-types]] for the family split.

All three surfaces list the fields in the `sort_order` set on [[subscribers-custom-fields-list]].

## Business rules

### Subscriber vs customer — independent namespaces

Subscriber and customer custom fields share one underlying table but live in **independent namespaces**. Every subscriber field is tagged `form = 'subscriber'` automatically on save, and a global scope auto-filters every query through the subscriber model to subscriber-only records. Consequences:

- The internal `name` uniqueness check is scoped to subscriber fields only. A name that already exists as a [[customers-custom-fields|customer custom field]] does NOT block creating it here, and vice-versa.
- Subscriber fields can never accidentally be mis-tagged as a customer field.

This is why the [[customer]] entity's custom fields (surfaced via the `customer.custom_field` segment condition) are entirely separate from the subscriber fields documented in this cluster.

### Deletion — what happens to stored values

Deleting a field (single-row or bulk, from [[subscribers-custom-fields-list]]) removes:

- The field **definition** itself (so it disappears from subscribe-form builders, the segment-condition picker, and subscriber detail views).
- All stored per-subscriber **values** for that field (the rows that mapped subscribers to this field's options or free-text values).
- All linked **option rows** — a deleting boot hook iterates every option of the field and deletes it (not just orphans it).

There is **no undo** and no soft-delete. Segments configured to filter by the deleted field's options will silently stop matching (the field reference becomes invalid). Existing subscribe forms that included the field will stop offering it. The merchant should review segments and subscribe forms before deleting a heavily-used field.

### Option-level deletes also ripple into segments

Even without deleting the whole field, removing a single option in the editor deletes that option row (see the option diff-on-save behaviour on [[subscribers-custom-fields-editor]]). Subscriber values pointing at the removed option become orphan references, shown as "deleted option" labels on the segment-condition picker until the merchant updates the affected segments.

### Legacy admin

A legacy version of the same screen exists at `/admin/subscribers/fields` (old admin). It exposes additional toggles per field (`active`, `required`) not present in the modern Vue page — on the modern path, newly-created fields are always set `active = 1`, and per-field `required` is set on the **subscribe form** that uses the field (not on the field definition itself). Merchants should use the modern screen; the legacy URL remains for backwards compatibility.

## Related

- [[marketing-subscribers-custom-fields]] — hub.
- [[subscribers-custom-fields-list]] — where delete is triggered; the `sort_order` these surfaces honour.
- [[subscribers-custom-fields-editor]] — option diff-on-save that ripples into segments.
- [[subscribers-custom-fields-types]] — Selection vs Text behaviour in segment conditions.
- [[marketing-subscribers-subscribe-forms]] — primary downstream consumer; sets per-field `required`.
- [[marketing-subscribers]] — subscriber detail view shows stored values.
- [[marketing-segments]] — `subscriber.custom_field` condition.
- [[customer]] — separate customer-field namespace.
- [[customers-custom-fields]] — the customer-side equivalent screen.
- [[subscriber]] — entity that stores these values.

## Open questions

No outstanding questions.
