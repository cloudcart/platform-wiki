---
type: entity
aliases: ["Subscribe form model", "Subscribe form fields", "Popup vs embedded form", "Subscribe form storage", "Subscribe form counters", "Модел на форма за абонамент"]
tags: [marketing, customers, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Subscribe Form — Model & render modes

> Part of [[subscriber-form]]. See the hub for the other aspects (eligibility, submission, lifecycle).

## Identity

The **model** of a [[subscriber-form|Subscribe Form]] is the bundle of configurable fields the merchant defines in the visual builder plus the two structural decisions that govern how the form reaches the storefront: the **render mode** (popup vs embedded) and the **storage** (a separate store from the main store data). This aspect covers what a form *is* on the data side — its attributes, its two delivery modes, and the auto-incrementing performance counters. *When* a form is shown is on [[subscriber-form-eligibility]]; *what happens on submit* is on [[subscriber-form-submission]].

## Aliases

- **Subscribe form model** / **Subscribe form fields** — the attribute set.
- **Popup vs embedded form** — the two render modes.
- **Subscribe form storage** — the separate store the form lives in.
- **Модел на форма за абонамент** — Bulgarian.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **`id`** | (auto) | 24-character hex identifier. Used in route params, embed-snippet JSONP callback names (`CcForm_<id>`), and the `subscriber.from_form` segment condition value. The route regex enforces 24 hex chars to avoid JSONP injection. |
| **Name** (`name`) | The form's admin label | Shown on the list, in segment-condition pickers, and on the subscriber's "subscribed by" attribution. Optional — the list falls back to the form id when empty. |
| **Active** (`active`) | On/Off | Boolean. Inactive forms aren't returned by the storefront queries. The list toggle hits `/admin/api/core/marketing/subscribe-forms/:id/status`. See [[subscriber-form-lifecycle]]. |
| **Draft** (`draft`) | True = unfinished | Boolean. Forms in draft state aren't served to the storefront even if `active = true`. The list shows a save icon instead of the Active switch for drafts. Auto-set to `false` on every save if it was previously null — see [[subscriber-form-submission]]. |
| **Type** (`type`) | Always `'form'` for storefront-rendered subscribe forms | The query layer filters `type = 'form'` — leaving room for non-storefront form types. |
| **Embedded** (`embedded`) | False = popup, True = inline | Boolean. When `true`, the storefront only renders this form via the explicit embed JS snippet (or the Page Builder module) and the form auto-sets `startDisplaying = [{type: 'auto'}]`. When `false`, the form is bulk-fetched at storefront startup and shown per `layoutPosition` + visibility rules. |
| **Pages** (`pages`) | Multi-page flow definition | JSON object with `form` (the input page) and `success` (the post-submit message). Drives the builder's tabbed editor. Includes `texts.title.text`, `texts.description.text`, `button.text`, `button.actionType` (submit/url), `button.actionUrl`, `markAsVerified`, `emailConfirm`, `custom_fields[]`, `includedUrls[]`, `excludedUrls[]`, and per-built-in-input flags (`email.is_visible`, `email.required`, `phone.is_visible`, etc.). |
| **Layout** (`layout`) | Visual layout | JSON. Includes the chosen **template** (`modal`, `bar`, `panel`, `sidebar`, `fullscreen` — the five starter layouts the merchant picks at form-creation time), close-button styling, dimensions. See [[marketing-subscribers-subscribe-forms]] for the template catalogue. |
| **Layout position** (`layoutPosition`) | Per-device anchor | JSON `{desktop: <key>, mobile: <key>}` — independent values per device. Enum: `topLeft`, `topCenter`, `topRight`, `topFull`, `centerLeft`, `centerCenter`, `centerRight`, `bottomLeft`, `bottomCenter`, `bottomRight`, `bottomFull`, `left`, `right`, `full`, `mobile`. The rendered position reads `layoutPosition[deviceType]` at storefront-render time. |
| **Style** (`style`) | Visual styling | JSON. Colors, fonts (Google Fonts — `fontFamily` is mapped to the matching Google Font to load the CSS), button styling. |
| **Terms** (`terms`) | Required/optional legal pages | Array of `{key, required, labelStyle}` referencing `Page` IDs. The marketing-policy page is one of the terms — ticking it is what flips the subscriber's `marketing` to `force-1`. See [[subscriber-form-submission]]. |
| **Tags** (`tags`) | Array of strings auto-applied to new subscribers | Free-text, no taxonomy. Applied after channel save — see [[subscriber-form-submission]]. |
| **Display for all** (`displayForAll`) | Show even to already-subscribed visitors | Boolean (default false). Evaluated at fetch time — see [[subscriber-form-eligibility]]. |
| **Cookies consent** (`cookies_consent`) | GDPR cookie-group gate (inverted semantic) | Boolean. Evaluated at fetch time — see [[subscriber-form-eligibility]]. |
| **Views** (`views`) | Auto-incremented counter | Atomic increment when the storefront calls `/subscribers/forms/<id>` (the "opened" endpoint, fired when the module displays). |
| **Submitted** (`submitted`) | Auto-incremented counter | Atomic increment on each successful submission. See [[subscriber-form-submission]]. |
| **GDPR consent** (`gdpr_consent`) | Boolean | Tracks whether the form gates marketing capture by the GDPR policy. Read by the projection list as one of the form's persisted attributes. |
| **`site_id`** | (auto) | Multi-tenant isolation. Auto-set to the current store's id on creating; every query is filtered to the owning store by this. See [[subscriber-form-submission]]. |
| **`deleted_at`** | (auto, soft-delete) | Set when the merchant deletes the form — see [[subscriber-form-lifecycle]]. |
| **`created_at` / `updated_at`** | (auto) | Timestamps. |

## Two render modes — popup vs embedded

The `embedded` boolean determines which storefront fetch endpoint serves the form. The toggle CAN be flipped on an existing form, but it changes how / where the form appears:

- **`embedded = false`** (popup mode): bulk-fetched via `GET /subscribers/forms/` at page-load. Up to **5 popup forms** are returned per request. The platform's module JS picks one or rotates. Shown per `layoutPosition` + visibility rules.
- **`embedded = true`** (inline mode): single-fetched via `GET /subscribers/forms/embed/<id>` using JSONP (`CcForm_<id>` callback). The merchant must paste the JS snippet (or use the Page Builder module) into the page where they want the form to appear. The storefront automatically sets `startDisplaying = [{type: 'auto'}]` so the form renders immediately when the script runs — no exit-intent or delay triggers.

The full eligibility filters that decide whether a fetched form is actually served / rendered are on [[subscriber-form-eligibility]].

## Separate form storage — not the main store database

Forms live in a separate marketing data store from the main store database. Consequences the merchant and support feel:

- The form id is a 24-char hex identifier, NOT an integer. URL/route regex enforces this.
- `pages`, `layout`, `style`, `terms`, `tags`, `custom_fields` are flexible JSON arrays — the structure can change and the visual builder can ship new fields without database migrations.
- Mass deletes select forms by their hex id list rather than by integer key.

### Atomic counters

`views` and `submitted` are bumped with an atomic increment. Concurrent submissions don't race-condition the counter. **Conversion rate = `submitted / views`** is reported on the list. `views` increments when the module displays (the "opened" endpoint fires); `submitted` increments only after a successful subscriber save — see [[subscriber-form-submission]].

## Where it appears

- [[marketing-subscribers-subscribe-forms]] — admin list and visual builder where every attribute above is set.
- [[marketing-subscribers]] — destination of new subscribers; "Subscribed by" column shows "Popup and Form builder" for form-originated subscribers.
- [[marketing-subscribers-custom-fields]] — defines the custom fields a form's `pages.form.custom_fields[]` can include.

## Related

- [[subscriber-form]] — hub.
- [[subscriber]] — the audience record a form creates / merges with.
- [[marketing-subscribers-subscribe-forms]] — the admin builder screen.
- [[marketing-subscribers-custom-fields]] — custom-field definitions referenced by forms.
- [[plan-gates]] — `subscriber_forms` plan-feature caps the number of forms.

## Open Questions

None.
