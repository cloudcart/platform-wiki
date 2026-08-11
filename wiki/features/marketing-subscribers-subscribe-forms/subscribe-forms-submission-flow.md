---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Submission flow"
route_name: subscribers.subscriptions.form.store
route_path: /subscribers/forms/{id}
aliases: ["Subscribe form submit", "Form submission flow", "Subscriber creation cascade", "Visitor-to-subscriber match", "Verify-action precedence", "Подаване на форма", "Запис на абонат"]
tags: [marketing, subscribers, forms, submission, validation, segments, webhooks, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list view, builder, templates, layout, triggers, fields, GDPR consent, known issues).

# Subscribe forms — submission flow

## Purpose

When a visitor submits a subscribe form, the platform validates, matches the visitor against an existing subscriber (or creates a new one), applies tags + custom fields, runs the verify-action cascade, and triggers segment re-evaluation. This page documents the end-to-end submit pipeline plus the public-endpoint security posture.

## Where to find it

The submit endpoint is **public-facing on the storefront** — not an admin screen. It fires when a visitor submits any subscribe form (popup, slide-in, bar, sidebar, fullscreen, or embedded inline).

Route: `POST /subscribers/forms/{id}` (route name `subscribers.subscriptions.form.store`).

## What the merchant can do here

This is a programmatic flow with no admin UI. The merchant's surfaces:

- Watch the `views` and `submitted` counters move on [[subscribe-forms-list]].
- Inspect captured subscribers on [[marketing-subscribers]].
- Use the `subscriber.from_form` segment condition on [[marketing-segments]] to slice subscribers by which form captured them.
- Receive `subscriber.created` webhooks via [[settings-hooks]] for downstream sync.

## Settings & fields

(This aspect documents a flow rather than form-builder settings — see [[subscribe-forms-builder]] for builder fields and [[subscribe-forms-fields]] for input/validation specs.)

## Business rules

### Submission flow — subscriber creation cascade

When a visitor submits:

1. The request validates the form's dynamically-built rules (email, phone, custom fields, terms).
2. Email and/or phone are extracted (only the store's configured campaign channels).
3. If the email matches an existing customer, the subscriber is linked to that customer; otherwise unattached.
4. **Marketing-consent**: if the visitor ticked the marketing terms page, the subscriber is created with marketing force-enabled. See [[subscribe-forms-gdpr-consent]] for the full marketing-policy gate.
5. **Verify-action gate** (the two verification toggles are mutually exclusive in the UI; the backend checks `markAsVerified` first):
   - `markAsVerified = true` → `verified = 1` immediately on save.
   - Else if `emailConfirm = true` → `verified = 0` AND an "Email confirmation for subscription in store:site_name" email is sent with a verify link.
   - Else → `verified = 0`, no email sent.

   If `markAsVerified` is true, `emailConfirm` is ignored even if also true. Non-email channels are verified by default (no email-confirmation flow).
6. The subscriber + per-channel rows are created (or merged into an existing subscriber). Source is `subscribed_from = 'subscribe_form'` with the form ID stored alongside.
7. The form's `submitted` counter atomically increments.
8. Form-level `tags` are auto-applied to the new subscriber. These are subscriber-specific tags, NOT shared with customer tags.
9. **Custom-field values** are validated against the form's allowed custom-field list and type-coerced — see [[subscribe-forms-fields]] for the coercion rules.
10. If any active segment has a `form`-type condition, a background job is queued to evaluate segment-membership for the new subscriber. This optimisation skips the segment pipeline for stores that don't segment by form.
11. The response is a success JSON payload — the storefront then shows the success page or redirects per the configured action.

### Visitor-to-subscriber match — pre-save cascade

Before deciding "new subscriber" vs "merge into existing", the storefront matches the visitor by, in order: **storefront subscriber session** → **active cart's subscriber id** → **cookie `uuid`**. This match controls whether the form is served at all (`displayForAll = false` hides it from already-identified subscribers).

At submission time the same match cascades: try by channel identifier first → then customer if known → then `uuid` cookie. Only if all three miss does the platform create a new subscriber.

### Channel filtering — only configured channels collect

The flow checks the store's configured campaign channels before saving. If the form has an email input but the store hasn't configured email as a campaign channel, the email is silently dropped. Same for phone. A form mid-migration (channel active when built, then disabled later) can produce subscribers with fewer channels than the form looks like it collects.

### View / submit counters

Two atomic counters per form:

- **`views`** — incremented when the storefront calls `GET /subscribers/forms/{id}` (route name `subscribers.subscriptions.form`) as the form actually displays.
- **`submitted`** — incremented on every successful submission.

Conversion rate = `submitted / views`.

### No CAPTCHA, no rate limit, no CSRF token on submit

The submit endpoint goes through CORS, XSS sanitisation, and GDPR policy-acceptance logging — but:

- **No captcha** (reCAPTCHA / hCAPTCHA).
- **No per-IP rate limiting.**
- **CSRF bypassed** — `/subscribers/forms/*` is exempt (intentional for cross-origin embeds, but removes the normal CSRF defence).
- **HTML cache bypassed** — `/subscribers/forms/*` is excluded from the storefront HTML cache.

The merchant relies on: front-end module timing throttle; cookie-based dismissal (`popup-subscription-displayed_<form-id> = false`); channel-identifier uniqueness (duplicate-email submits update the existing row rather than creating new ones). Programmatic spam can inflate the `submitted` counter and create subscriber rows with arbitrary identifiers. See [[subscribe-forms-known-issues]].

### CORS-enabled storefront endpoints

All public-facing form endpoints (`subscribers/forms/*`) allow cross-origin requests; the OPTIONS preflight returns an empty 200 for any path under them. This is needed for the embed mode (cross-origin delivery + POST submit).

### Activity logging

Form submissions don't write to a form-level log directly — the resulting subscriber and channel rows do (visible in the subscriber's per-row activity log under [[marketing-subscribers]]). For form-level analytics the merchant sees the `views` / `submitted` columns on [[subscribe-forms-list]]; for fine-grained conversion tracking, use the `from_form` segment condition to compute revenue / order-rate per form.

### GDPR policy-acceptance log

When the submit returns OK and the request body has a `terms` array, a per-policy acceptance log row is written — see [[subscribe-forms-gdpr-consent]] for full details including the captured audit fields.

## Programmatic access

The subscribe-form **definition** itself is admin-panel-only (the visual builder produces a complex multi-page layout JSON with no JSON-API v2 resource). But the **subscribers a form captures** can be created, updated, and read programmatically via [[api-subscribers]] — useful when an external lead-capture tool (custom landing page, off-platform form) should feed the same audience as a CloudCart subscribe form.

**Same side effects apply.** A POST through JSON-API v2 to [[api-subscribers]] runs the same downstream pipeline as a storefront form submission: the subscriber-identity cascade (channel → customer → uuid match before creating new), the plan-cap check, automated-segment re-evaluation, phone-number E.164 normalisation, and `subscriber.created` webhook dispatch via [[settings-hooks]].

Difference from the storefront flow: API-created subscribers have `subscribed_from = 'API'` (not `'subscribe_form'`) and no form ID — so the `subscriber.from_form` segment condition will NOT match them. To attribute external captures to a specific in-platform form, use a tag instead and segment on tag.

See [[json-api-v2]] for authentication, rate limits, and the side-effects principle.

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-fields]] — input slot definitions + validation rules + type coercion.
- [[subscribe-forms-gdpr-consent]] — marketing-policy gate + policy-acceptance audit.
- [[subscribe-forms-known-issues]] — security gaps + missing analytics surfaces.
- [[marketing-subscribers]] — destination subscriber rows.
- [[marketing-segments]] — `subscriber.from_form` segmentation condition.
- [[api-subscribers]] — programmatic equivalent endpoint.
- [[settings-hooks]] — `subscriber.created` webhook.
- [[json-api-v2]] — side-effects principle for programmatic subscriber creation.

## Open questions

None.
