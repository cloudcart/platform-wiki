---
type: entity
aliases: ["Subscribe form lifecycle", "Subscribe form states", "Subscribe form draft", "Subscribe form publish", "Subscribe form soft delete", "Subscribe form Page Builder module", "Embedded subscription form module", "Жизнен цикъл на форма за абонамент"]
tags: [marketing, customers, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Subscribe Form — Lifecycle & states

> Part of [[subscriber-form]]. See the hub for the other aspects (model, eligibility, submission).

## Identity

The **lifecycle** of a [[subscriber-form|Subscribe Form]] is the sequence of states it moves through from the moment the merchant clicks Add Form to the moment it is soft-deleted: **created → drafting → published → active → inactive → soft-deleted**. Two state-bearing flags drive it — `draft` (is it finished?) and `active` (is it switched on?) — and the soft-delete keeps the form record in storage after removal. This aspect also covers the Page Builder module that places an embedded form, since that is an alternative publication path.

## Aliases

- **Subscribe form lifecycle** / **Subscribe form states** — the state machine.
- **Subscribe form draft** / **Subscribe form publish** — the `draft` flag transitions.
- **Subscribe form soft delete** — the `deleted_at` removal.
- **Embedded subscription form module** — the Page Builder module name.
- **Жизнен цикъл на форма за абонамент** — Bulgarian.

## Key Attributes

| Attribute | Role in the lifecycle | Notes |
|-----------|----------------------|-------|
| **Draft** (`draft`) | Gate before publish | True = unfinished; the list shows a save icon instead of the Active switch. Normalized `null → false` on every save (see [[subscriber-form-submission]]). |
| **Active** (`active`) | On/Off after publish | Toggle hits `/admin/api/core/marketing/subscribe-forms/:id/status`. Inactive forms aren't returned by storefront queries (see [[subscriber-form-eligibility]]). |
| **`deleted_at`** | Soft-delete marker | Set on delete; the form record stays in storage. |

## The state machine

A Subscribe Form moves through these states:

1. **Created** — merchant clicks Add Form; the builder opens and a draft form record is created with `active = false` (or `null`) and `draft = true`. The form ID (24-char hex identifier) is allocated **immediately** so the embed JS snippet can be generated before the form is even finished.
2. **Drafting** — merchant edits in the visual builder. Saves persist incremental changes. Until published, `draft = true` and the list shows the save icon instead of the Active toggle.
3. **Published** — merchant clears the draft flag (typically by Saving with all required fields valid). `draft = false`, `active = true`. The form is now eligible to render on the storefront — subject to the [[subscriber-form-eligibility]] filters.
4. **Active** — the storefront returns this form on eligible page-loads. Each render increments `views`; each submission increments `submitted` (see [[subscriber-form-model]] for the counters).
5. **Inactive** — merchant flips `active = false`. The form stops rendering. Existing JS snippets pasted in pages still call the endpoint but get an empty response.
6. **Soft-deleted** — merchant deletes from the list. `deleted_at` is set. The form is hidden from admin lists + storefront queries. The form record remains for audit. There is **no undo button** in the UI, but the record can be manually un-soft-deleted if needed.

## Soft delete + caching implications

Forms are soft-deleted; listing and storefront queries skip soft-deleted forms (those with no `deleted_at` are shown). However, browsers that have **already cached** the embedded JS snippet for a deleted form keep calling the endpoint until they refresh — the platform returns empty data and the embed module shows nothing. There is no automatic invalidation pushed to browsers, so a removed embedded form simply stops painting rather than erroring.

## Page Builder module integration

Embedded subscribe forms can also be inserted via the **Page Builder** module *"Embedded subscription form"* (help text: *"With this module, you will be able to embed a subscribe form into the page you are creating"*). The module picks an existing embedded form by id and renders it inline — the same JSONP delivery mechanism (`CcForm_<id>`) as a hand-pasted snippet, just initiated by the Page Builder's runtime. This is an alternative to publishing via a pasted snippet; the underlying form must still be `embedded = true`, published, and active to render — see [[subscriber-form-eligibility]].

## Where it appears

- [[marketing-subscribers-subscribe-forms]] — the admin list where Create / Draft / Active toggle / Delete happen, and the visual builder.
- [[marketing-subscribers]] — destination of subscribers captured while the form is Active.

## Related

- [[subscriber-form]] — hub.
- [[marketing-subscribers-subscribe-forms]] — the admin list + builder where state transitions happen.
- [[subscriber]] — the audience record created while the form is Active.

## Open Questions

None.
