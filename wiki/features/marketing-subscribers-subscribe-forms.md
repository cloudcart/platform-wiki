---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms"
route_name: subscribe-forms.list
route_path: /admin/marketing-new/subscribers/subscribe-forms
aliases: ["Subscribe Forms", "Subscription forms", "Newsletter popup", "Lead-capture forms", "Форми за абонамент", "Поп-ъп форми"]
tags: [marketing, subscribers, forms, popup, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-05-21
updated: 2026-06-10
source_count: 9
---

# Subscribe Forms

## Purpose

The merchant's tool for **collecting subscribers on the storefront**: popup, slide-in, sticky-bar, sidebar, fullscreen, and embedded subscription forms that show on the storefront and convert visitors into [[marketing-subscribers]]. Each form is a fully visual canvas — pages, layout, button styling, fonts, success message, custom fields, GDPR / cookie consent gates — built in a dedicated drag-and-drop builder (Vue-based, served via an iframe to isolate CSS).

The form's stated purpose is *"By using this form, you will be able to collect subscribers and later reach them via email or phone, even before they become your customers"* — i.e., capture intent at the moment of visit, BEFORE the visitor signs up as a [[customer]], so the merchant can later message them via [[marketing-campaigns]]. Once submitted, the form creates (or merges with) a Subscriber row tagged with `subscribed_from = 'subscribe_form'` plus the form ID.

## Where to find it

Sidebar → **Marketing** → **Subscribers** → **Subscribe Forms**.

Routes:

- List view: `/admin/marketing-new/subscribers/subscribe-forms`.
- Form editor: `/admin/marketing-new/subscribers/subscribe-forms/form/:id?`.

Both gated by the plan's `subscriber_forms` feature key.

## What the merchant can do here

This page is the cluster hub — the merchant's actions are documented in detail on the aspect pages:

- See / toggle / bulk-delete forms + view embed code — see [[subscribe-forms-list]].
- Compose forms in the iframe-sandboxed visual editor — see [[subscribe-forms-builder]].
- Pick a structural template, layout position, display triggers — see [[subscribe-forms-templates]], [[subscribe-forms-layout]], [[subscribe-forms-triggers]].
- Configure input slots + custom fields — see [[subscribe-forms-fields]].
- Attach legal terms + manage GDPR cookie consent — see [[subscribe-forms-gdpr-consent]].

## Settings & fields

This page is the cluster hub — full setting / field tables live on the aspect pages:

- List columns + Embed-code modal — see [[subscribe-forms-list]].
- Top-level builder fields + per-page settings + button action types + styling primitives — see [[subscribe-forms-builder]].
- `layoutPosition` enum (15 values) — see [[subscribe-forms-layout]].
- `startDisplaying` + `stopDisplaying` triggers — see [[subscribe-forms-triggers]].
- Built-in input slots + custom-field validation rules — see [[subscribe-forms-fields]].

## Business rules

This page is the cluster hub — full business rules live on the aspect pages. The headline rules:

- **Popup mode vs Embedded mode** — `embedded = false` (fetched in bulk via `GET /subscribers/forms/`, limit 5) vs `embedded = true` (fetched per-page via `GET /subscribers/forms/embed/<id>` JSONP). See [[subscribe-forms-builder]].
- **Storefront eligibility query** — `site_id` + `active` + `draft` + `type` + `embedded` + `displayForAll` + `cookies_consent` + dismissal-cookie filter. See [[subscribe-forms-gdpr-consent]].
- **Visitor-to-subscriber match cascade** — channel-identifier → customer_id → uuid cookie before creating a new row. See [[subscribe-forms-submission-flow]].
- **Inverted `cookies_consent` semantic** — `true` is the BYPASS, not the gate. See [[subscribe-forms-gdpr-consent]].
- **Verify-action precedence** — `markAsVerified` checked before `emailConfirm`. See [[subscribe-forms-submission-flow]].
- **Plan-gating + soft-delete** — `subscriber_forms` feature key; deleted forms set `deleted_at` and free a quota slot but keep counters. See [[subscribe-forms-list]].
- **Unique form ID in the URL** — each form has its own identifier, embedded verbatim in the public form URL and the embed snippet.

## Sub-pages (in this cluster)

This feature is split into 10 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[subscribe-forms-list]] — admin list view: name / submitted / views / embed / Active toggle, bulk-delete, soft-delete, plan-quota counter, embed-code modal.
- [[subscribe-forms-builder]] — iframe-sandboxed visual editor: top-level fields, two-page composition (`form` + `success`), styling primitives, popup-vs-embedded mode toggle.
- [[subscribe-forms-button-actions]] — the **submit button** & confirmation: the two action types (`submit` = show confirmation page / `url` = redirect), the success page (`is_default` vs custom), and the success-page button (`close` / `url`).
- [[subscribe-forms-templates]] — the 5 structural templates the new-form picker offers: `modal`, `bar`, `panel`, `sidebar`, `fullscreen` (NOT a content library).
- [[subscribe-forms-layout]] — the `layoutPosition` enum (15 values, per-device desktop/mobile).
- [[subscribe-forms-triggers]] — the 3 display triggers (`auto`, `exitIntent`, `timeOnPage`) + `stopDisplaying` complementary array.
- [[subscribe-forms-fields]] — the 4 built-in input slots (email / phone / first_name / last_name) + 6 custom-field types + per-field configuration.
- [[subscribe-forms-submission-flow]] — POST `/subscribers/forms/{id}` cascade: validation, visitor-match, channel filtering, verify-action precedence, segment re-evaluation; plus the public-endpoint security posture (no CAPTCHA / rate limit / CSRF).
- [[subscribe-forms-gdpr-consent]] — the **inverted-semantic** `cookies_consent` flag, marketing-policy gate, and the consent audit row written per ticked policy.
- [[subscribe-forms-known-issues]] — by-design carve-outs + missing capabilities (no pixel events, no A/B testing, no Mailchimp sync, no per-device visibility, no per-page-type targeting, etc.).

## Why it matters to the merchant

Subscribe forms are the platform's primary **pre-conversion lead-capture surface** — they turn anonymous storefront visitors into addressable Subscribers before the visitor commits to a purchase. Three high-impact properties unique to this surface:

- **Audit-grade GDPR consent + inverted `cookies_consent`.** Every ticked policy writes an audit row (IP / UA / time / content hash), making the form a compliance-grade audit point. Note the `cookies_consent` flag is **inverted**: `true` is the BYPASS ("form handles consent itself"), not the gate — misreading it misconfigures GDPR. See [[subscribe-forms-gdpr-consent]].
- **Channel-identifier merge.** A submission whose email matches an existing Customer or Subscriber merges into that row instead of duplicating, so a visitor can submit many forms without bloating the audience. See [[subscribe-forms-submission-flow]].
- **Form-attribution segmentation.** The `subscriber.from_form = <form-id>` segment condition slices downstream orders by capture source — the closest thing to per-form revenue attribution. See [[marketing-segments]].

This page does NOT cover where captured subscribers live ([[marketing-subscribers]], [[marketing-segments]]), the legal Page entities attached as terms ([[apps-gdpr-policy]]), the targeting-cookie group ([[apps-gdpr-cookies]]), the campaign-send pipeline ([[marketing-campaigns]]), or subscriber custom-field definitions ([[marketing-subscribers-custom-fields]]).

## Where it applies

Storefront-wide. Visibility is filtered at render time per the eligibility query in [[subscribe-forms-gdpr-consent]] (site_id, active, draft, type, embedded mode, already-subscribed, targeting-cookie gate, per-form dismissal cookie, limit 5). Once dismissed, the per-form cookie `popup-subscription-displayed_<form-id> = false` suppresses re-display on that browser; the encrypted-cookies middleware whitelists this prefix so the module JS can read it cleartext.

The form **definition** is admin-panel-only (no JSON-API v2 resource for its multi-page layout JSON), but the **subscribers it captures** are readable/writable via [[api-subscribers]]. API-created subscribers get `subscribed_from = 'API'` and `form_id = NULL`, so they won't match the `subscriber.from_form` segment — tag them and segment on tag to attribute external captures.

## Related concepts

The features above are the **screens**; these concepts are the cross-cutting **behaviour** behind the form — the "how does it actually work" models a merchant reasons with:

- [[subscribe-form-display-engine]] — **when / where / to whom** a form shows: the render-time eligibility cascade (mode, URL scope, triggers, consent, already-subscribed, position) + the ≤ 5-forms startup rotation.
- [[subscriber-double-optin]] — single vs **double opt-in**: how a captured lead becomes `verified`, and why `verified` gates every campaign send.
- [[lead-capture-lifecycle]] — the **form → subscriber → segment → campaign** pipeline a lead travels (and where captured leads "disappear" before the inbox).
- [[marketing-consent-collection]] — how the form's terms / marketing-policy checkboxes **collect** marketing consent and write the audit proof (vs the consent *gate*).
- [[capture-source-attribution]] — how the form stamps `from_form` so the merchant can segment / attribute by capture source.
- [[subscriber-deliverability]] — "can this campaign reach the lead?" — the reachability predicate + "why didn't they receive it" diagnostic.
- [[subscriber-segmentation]] — automated vs one-time audiences the captured lead flows into.
- [[subscriber-vs-customer]] — Subscriber vs Customer records, channels, consent, linkage.

## Related

- [[marketing]] — parent hub.
- [[marketing-subscribers]] — destination — every submission becomes a subscriber here.
- [[marketing-subscribers-custom-fields]] — define custom fields surfaced in the builder.
- [[marketing-segments]] — `subscriber.from_form` condition for segmenting by capture source.
- [[marketing-campaigns]] — primary downstream consumer of captured subscribers.
- [[apps-gdpr-overview]] — `marketing_policy` setting + the legacy `checkout_terms_page` fallback.
- [[apps-gdpr-cookies]] — `targeting` cookie group that gates `cookies_consent = false / null` forms.
- [[apps-gdpr-policy]] — legal terms pages attached to forms.
- [[settings-hooks]] — `subscriber.created` webhook for external CRM sync.
- [[api-subscribers]] — programmatic subscriber resource.
- [[json-api-v2]] — side-effects principle for programmatic creates.
- [[subscriber-form]] — entity page.
- [[subscriber]] — destination entity row.

## Open questions

None — all previously flagged items distributed to sub-pages.
