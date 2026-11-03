---
type: concept
aliases: ["Capture source attribution", "subscribed_from", "subscriber.from_form", "Where did this subscriber come from", "Subscriber source", "Per-form attribution", "Lead source tracking", "Form ROI", "How was this subscriber captured", "Източник на абоната", "От коя форма дойде абонатът"]
tags: [marketing, subscribers, attribution, segments, forms, concepts]
plan_gates: []
created: 2026-06-30
updated: 2026-06-30
source_count: 2
---

# Capture-source attribution

## Definition

Every subscriber the platform creates is stamped with **where it came from** — a `subscribed_from` source value, and, when a [[marketing-subscribers-subscribe-forms|subscribe form]] captured it, the specific **`form_id`**. This is the platform's built-in **lead-source attribution**: it lets the merchant answer "where do my subscribers come from?" and target / measure by capture source, including **per-form** — the closest thing CloudCart offers to per-form ROI.

The `subscribed_from` source is a fixed enum; the values (with their merchant-facing labels) include:

| `subscribed_from` | Label | When |
|---|---|---|
| `subscribe_form` | **Popup and Form builder** | a subscribe form was submitted (the `form_id` records which one) |
| `customer_login` | Customer login | captured during a customer login |
| `customer_creating` | Customer creating | a customer account was created |
| `order_creating` | Order creating | captured at checkout / order placement |
| `customer_address_creating` / `_deleting` | Customer address creating / deleting | address-book changes |
| `import` | Import | bulk import |
| `messenger` | Messenger | the Messenger channel |
| `contacts_form` | Contacts form | the storefront contact form |
| `system` | From system | platform-internal capture |

(Programmatic creates via [[api-subscribers]] carry an API source with **no** `form_id`.)

## Scope

Covered: the `subscribed_from` source enum + labels; the per-form `form_id` stamp; the `subscriber.from_form` segment condition; using source for attribution / ROI; the API/import attribution gotcha. NOT covered: the submit pipeline that sets the stamp (see [[lead-capture-lifecycle]] / [[subscribe-forms-submission-flow]]); the segment engine that consumes the condition (see [[subscriber-segmentation]]); marketing consent / verification (separate stamps).

## Contrasts

- **`subscribed_from` (broad source) vs `from_form` (specific form)** — `subscribed_from = subscribe_form` says "a form captured this"; `form_id` / the `subscriber.from_form` segment condition says **which** form. Source-level and form-level attribution are two granularities.
- **Form capture vs other sources** — a subscriber can arrive from checkout (`order_creating`), a login, an import, the contacts form, or a popup. Only the popup/builder path carries a `form_id`, so only it supports per-form attribution; the others attribute at source granularity only.
- **Attribution vs ROI** — the platform attributes the *capture* (which form/source produced the subscriber). True ROI (revenue per form) is the merchant's join of `from_form` segments to downstream orders — the building block, not a packaged report.

## Where it applies

### Stamping at capture

The source is set when the subscriber row is created — by the submit cascade for forms (`subscribe_form` + `form_id`), and by the respective surface for the other sources. See [[lead-capture-lifecycle]].

### Segmenting by source — `subscriber.from_form`

On [[marketing-segments]], the **`subscriber.from_form = <form-id>`** condition slices the audience by the exact form that captured each subscriber — e.g. an audience of "everyone from the Black-Friday popup" to target with a dedicated campaign, or to measure how that form's subscribers convert. This is the lever that turns capture attribution into targeting and measurement.

### The API / import attribution gotcha

Subscribers created via [[api-subscribers]] get the API source and **`form_id = NULL`**, so they will **not** match any `subscriber.from_form` segment. To attribute externally-captured subscribers, **tag them on create and segment on the tag** instead of relying on `from_form`.

## Related

- [[marketing-subscribers-subscribe-forms]] — the form whose `form_id` is stamped.
- [[lead-capture-lifecycle]] — where the source stamp is set in the pipeline.
- [[subscriber-segmentation]] — the segment engine that consumes `subscriber.from_form`.
- [[marketing-segments]] — the `subscriber.from_form` condition + tag-based fallback for API captures.
- [[api-subscribers]] — programmatic creates (API source, no `form_id`).
- [[subscriber]] — the entity carrying `subscribed_from` / `form_id`.

## Open Questions

- (verify) The complete `subscribed_from` enum (additional internal values beyond those listed) and the exact API source label.
