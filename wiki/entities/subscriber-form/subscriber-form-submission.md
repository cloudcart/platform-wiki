---
type: entity
aliases: ["Subscribe form submission", "Subscribe form validation", "Subscribe form submit rules", "Subscribe form save defaults", "Subscribe form terms consent", "Subscribe form tags", "Подаване на форма за абонамент"]
tags: [marketing, customers, gdpr, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Subscribe Form — Submission & validation

> Part of [[subscriber-form]]. See the hub for the other aspects (model, eligibility, lifecycle).

## Identity

**Submission** is everything that happens when a visitor fills in a [[subscriber-form|Subscribe Form]] and clicks the button: the dynamic validation rules, the creation-or-merge of a [[subscriber|Subscriber]] row, the legal-terms consent that can flip the subscriber's marketing flag, the auto-applied tags, the `submitted` counter increment, and the save-time model defaults. This is the write side of the form — `POST /subscribers/forms/<id>` returning a saved subscriber. Eligibility (whether the form was even shown) is on [[subscriber-form-eligibility]]; the field definitions are on [[subscriber-form-model]].

## Aliases

- **Subscribe form submission** / **Subscribe form submit rules** — the act of submitting.
- **Subscribe form validation** — the dynamic rule set.
- **Subscribe form save defaults** — the model `creating` / `saving` hooks.
- **Subscribe form terms consent** — the marketing-flag flip.
- **Подаване на форма за абонамент** — Bulgarian.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Terms** (`terms[]`) | Required/optional legal pages ticked at submit | Array of `{key, required, labelStyle}` referencing `Page` IDs. Ticking the marketing-policy page flips the subscriber's `marketing` flag to `force-1`. See [[apps-gdpr-policy]]. |
| **Tags** (`tags`) | Strings auto-applied to every new subscriber | Free-text, no taxonomy. Applied via the subscriber's tag setter **after** the channel save succeeds. |
| **Submitted** (`submitted`) | (auto counter) | Atomic `$inc` on each successful submission; powers the conversion rate on the list. |
| **Per-input required flags** (`email.required`, `phone.required`, etc.) | Which inputs are mandatory | Stored under `pages.form`; drive the dynamic validation rules below. |

## Create-or-merge behaviour

A submission creates a new [[subscriber|Subscriber]] OR merges into an existing one. The match is on the channel identifier (email / phone): the same email can only be **one** Subscriber row, so a repeat submission updates the existing row rather than creating a duplicate. Every form-originated subscriber carries `subscriber_from = 'subscribe_form'` AND `form_id = <this form's id>`, which is what the `subscriber.from_form` [[segment]] condition filters on. If the submitted email matches an existing [[customer|Customer]], the new Subscriber MAY link to that Customer — but the form itself never creates a Customer (see [[subscriber-vs-customer]]).

## Validation rules at submission

Submission rules are built **dynamically** from the form definition, so a form that hides the phone input never validates phone:

- **`email`** — required if `email.required = true`; must pass standard email validation.
- **`phone`** — required if `phone.required = true`; must pass `phone_number_global:<country_iso2>`.
- **`first_name` / `last_name`** — required if marked required; max 191 characters.
- **Custom fields** — type-coerced per field: `checkbox → array + in:<options>`, `phone → phone_number_global`, etc. The field definitions live on [[marketing-subscribers-custom-fields]]; the form only carries the key + per-form display flags.
- **Terms** — each required terms page must be ticked.

Validation errors return **HTTP 422** with field-mapped errors that the storefront module renders inline.

## Submitted-counter increment is INSIDE the save

The `submitted` counter increments only **after** a successful subscriber save (channel write completed):

- A submission that fails validation does NOT increment the counter.
- A submission whose email matches an existing subscriber and merges with them DOES increment — the save succeeded, it just merged into an existing row.

This means conversion rate (`submitted / views`) counts successful captures including merges, not raw button clicks.

## Save-time defaults (model `creating` + `saving` hooks)

Two model hooks run before every form save:

- **`creating` hook — `site_id` auto-fill** — if a new form has `site_id` empty, the model fills it from `site('site_id')` at create. This is how forms inherit multi-tenant isolation without the caller explicitly passing the site id — the `owner` scope on every list query then enforces it on read.
- **`saving` hook — `draft` defaults to `false`** — every save (create AND update) normalizes `draft` from `null` to `false`. A partially-built form coming from an API client that omitted the `draft` flag is therefore treated as **published by default** — the merchant has to explicitly set `draft = true` to keep it hidden. See [[subscriber-form-lifecycle]] for the draft → published transition.

## Where it appears

- [[marketing-subscribers-subscribe-forms]] — where the required-input flags, terms, and tags are configured.
- [[marketing-subscribers]] — destination of the created / merged subscriber; "Subscribed by" shows "Popup and Form builder".
- [[marketing-subscribers-custom-fields]] — defines the custom fields a submission can carry.
- [[apps-gdpr-policy]] — the legal terms pages whose tick flips the marketing flag.

## Related

- [[subscriber-form]] — hub.
- [[subscriber]] — every submission creates / merges with a Subscriber.
- [[subscriber-vs-customer]] — forms create Subscribers, not Customers.
- [[customer]] — a submission MAY link the Subscriber to a matching Customer.
- [[marketing-subscribers-custom-fields]] — custom-field definitions.
- [[settings-hooks]] — the `subscriber.created` webhook fires when a submission creates a new subscriber.

## Open Questions

None.
