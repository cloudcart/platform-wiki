---
type: entity
aliases: ["Subscribe Form", "Subscriber Form", "Subscription form", "Newsletter popup", "Popup form", "Embedded subscribe form", "Форма за абонамент", "Поп-ъп форма"]
tags: [marketing, customers]
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Subscribe Form

## Identity

A **Subscribe Form** is the visual storefront module the merchant builds and embeds (or auto-pops up) to capture new [[subscriber|Subscribers]] from anonymous visitors. It collects an email and/or phone, optionally extra [[marketing-subscribers-custom-fields|custom fields]], optionally a marketing-consent / GDPR-terms tick, and writes a new Subscriber row (or merges with an existing one). It is the primary "lead capture" tool in the [[marketing]] toolset — distinct from [[customer]] sign-up (which creates a buyer account at checkout).

The merchant manages forms on [[marketing-subscribers-subscribe-forms]] and edits them in a visual drag-and-drop builder. A form is either a **popup** (auto-displays on storefront pages per visibility rules) or **embedded** (rendered inline at a specific spot via a JavaScript snippet — also offered as a Page Builder module). Forms are kept in a separate store from the main store data, use a 24-character hex identifier, and are soft-deleted on removal.

This entity is split into aspect pages below. The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[subscriber-form-model]] — the configurable fields (name, pages, layout, style, terms, tags, counters); the two render modes (popup vs embedded) and their fetch endpoints; the separate form storage; atomic `views` / `submitted` counters.
- [[subscriber-form-eligibility]] — fetch-time visibility filters (popup mode); the GDPR `targeting` cookie gate via the inverted `cookies_consent` flag; the per-visitor dismissal cookie; `displayForAll`; CORS for cross-origin storefront calls.
- [[subscriber-form-submission]] — create-or-merge of a Subscriber; dynamic validation rules; terms tick → marketing flag flip; auto-applied tags; the `submitted`-counter-inside-the-save rule; `site_id` / `draft` save-time defaults.
- [[subscriber-form-lifecycle]] — the created → drafting → published → active → inactive → soft-deleted state machine; soft-delete + browser-cache implications; the "Embedded subscription form" Page Builder module.

## Aliases

- **Subscribe Form** — canonical merchant-facing label.
- **Subscription form** / **Newsletter popup** — informal English variants.
- **Popup form** — when the form is `embedded = false`.
- **Embedded subscribe form** — when the form is `embedded = true` (also the Page Builder module name).
- **Форма за абонамент** / **Поп-ъп форма** — Bulgarian.

## Key Attributes

The form's full attribute table is on [[subscriber-form-model]]. The fields support staff most often ask about:

| Attribute | What it is | Aspect |
|-----------|-----------|--------|
| **`id`** | 24-char hex identifier; used in routes + `CcForm_<id>` JSONP callback | [[subscriber-form-model]] |
| **Embedded** (`embedded`) | False = popup, True = inline snippet / Page Builder module | [[subscriber-form-model]] |
| **Active** + **Draft** | The two state flags that gate storefront rendering | [[subscriber-form-lifecycle]] |
| **Display for all** (`displayForAll`) | Show to already-subscribed visitors or not | [[subscriber-form-eligibility]] |
| **Cookies consent** (`cookies_consent`) | Inverted GDPR `targeting` cookie gate | [[subscriber-form-eligibility]] |
| **Terms** (`terms[]`) | Legal pages; the marketing-policy tick flips the subscriber's marketing flag | [[subscriber-form-submission]] |
| **Tags** (`tags`) | Auto-applied to every captured subscriber | [[subscriber-form-submission]] |
| **Views / Submitted** | Atomic counters; conversion rate = `submitted / views` | [[subscriber-form-model]] |

Key facts: a form is **popup or embedded** (the `embedded` flag picks the fetch endpoint); it renders only when **active AND not draft** AND it passes the eligibility filters; submissions **create or merge** a Subscriber keyed on email/phone (no duplicates); the `submitted` counter increments **only on a successful save**.

## Relationships

A Subscribe Form:

- **Has many** [[subscriber|Subscribers]] indirectly — each subscriber created via this form carries `subscriber_from = 'subscribe_form'` AND `form_id = <this form's id>`. The `subscriber.from_form` [[segment]] condition lets the merchant filter by a specific form. See [[subscriber-form-submission]].
- **References** [[marketing-subscribers-custom-fields|Subscriber Custom Fields]] via `pages.form.custom_fields[]` — picks which subscriber custom fields to expose. The field definitions live elsewhere; the form only carries the key + per-form display flags.
- **References** `Page` rows via `terms[].key` — legal pages (marketing policy, privacy policy) attached for consent. The marketing-policy page identifies which checkbox flips the subscriber's marketing flag.
- **Is the target of** the storefront module JS, which fetches it at page-load (bulk for popups, JSONP for embedded) and renders it per the [[subscriber-form-eligibility]] rules.

A Subscribe Form is NOT:

- **The same as a [[subscriber|Subscriber]]** — it is the form definition (visual + behavioural) that creates Subscribers; the Subscriber is the audience record.
- **Tied to a [[customer|Customer]]** — the form creates Subscribers only; Customers are created separately at signup / checkout. See [[subscriber-vs-customer]].

## Where it appears

- [[marketing-subscribers-subscribe-forms]] — admin list and visual builder.
- [[marketing-subscribers]] — destination of new subscribers; "Subscribed by" column shows "Popup and Form builder" for form-originated subscribers.
- [[marketing-subscribers-custom-fields]] — defines the custom fields that forms can include.
- [[marketing-segments]] / [[marketing-segments-editor]] — the `subscriber.from_form` condition filters segments by which form captured the subscriber.
- [[marketing-campaigns]] — downstream consumer (campaigns reach subscribers captured via forms).
- [[apps-gdpr-cookies]] — the `targeting` cookie group gate.
- [[apps-gdpr-policy]] — legal terms pages attached to forms.

## Related

### Related entities

- [[subscriber]] — every form submission creates / merges with a Subscriber.
- [[subscriber-vs-customer]] — forms create Subscribers (not Customers); newsletter signup is a Subscriber, not a buyer.
- [[customer]] — a form submission MAY link the new Subscriber to an existing Customer if the email matches.
- [[segment]] — segments can target subscribers from specific forms.
- [[campaign]] — downstream consumer.

### Cross-cutting concepts

- [[notification-delivery]] — how subscribers captured via forms are reached by campaigns.
- [[plan-gates]] — `subscriber_forms` plan-feature caps the number of forms.
- [[checkout-flow]] — where the marketing-consent at checkout intersects with form-based signups.

### Settings & feature pages

- [[marketing-subscribers-subscribe-forms]] — primary admin screen.
- [[marketing-subscribers-custom-fields]] — defines the custom fields that forms can include.
- [[settings-hooks]] — `subscriber.created` webhook fires when a form submission creates a new subscriber.

## Open Questions

No outstanding questions — all items resolved or removed.
