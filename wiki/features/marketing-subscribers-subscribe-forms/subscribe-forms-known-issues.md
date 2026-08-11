---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Known issues"
route_name: ""
route_path: ""
aliases: ["Subscribe forms limitations", "Subscribe forms missing features", "No pixel events on subscribe form", "No A/B testing on subscribe forms", "No CAPTCHA on subscribe form", "Subscribe form known issues", "Ограничения на формите за абонамент"]
tags: [marketing, subscribers, forms, known-issues, limitations, analytics, security, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list view, builder, templates, layout, triggers, fields, submission flow, GDPR consent).

# Subscribe forms — known issues + missing capabilities

## Purpose

A consolidated catalogue of what the subscribe-forms feature does **NOT** do, mostly by-design carve-outs and gaps merchants regularly ask about. Each item links to the relevant aspect page for full context.

## Where to find it

Not a UI surface — this page documents gaps that the merchant runs into across the builder, the storefront, and post-submit analytics.

## What the merchant can do here

(Limitations, not capabilities — see each section for the merchant's workaround.)

## Settings & fields

(Not applicable — this page documents missing settings.)

## Business rules

### Analytics gaps

The platform's only built-in goal tracking is the per-form **`views`** and **`submitted`** counters on [[subscribe-forms-list]] (compute conversion rate as `submitted / views` manually). What's missing:

- **NO** per-step funnel (form-shown → form-opened → field-1-filled → submit) — only the two terminal counters.
- **NO** revenue attribution per form. The `subscriber.from_form` segment condition lets the merchant build a segment of subscribers captured by a specific form, then read downstream orders from it — but no per-form revenue total is surfaced on the forms list.
- **NO** UTM-source pass-through on the subscriber row (submission records only the form id, not which UTM brought the visitor in).

Workaround: build a segment with `subscriber.from_form = <form-id>` on [[marketing-segments]] and read order totals downstream.

### No pixel events fire from subscribe form submissions (verified)

Despite their lead-capture purpose, subscribe-form submissions do **NOT** fire any third-party tracking pixel events:

- No **Facebook Pixel** `Lead` event.
- No **Google Analytics** `generate_lead` event.
- No **TikTok Pixel** event.

Workaround: wire a manual `fbq('track', 'Lead', ...)` (or equivalent) into the form's storefront success handler, usually via a custom-JS app or the page builder.

### No A/B testing

**NOT supported.** No variant axis on a form record, no traffic-allocation control, no automatic winner selection.

Workaround: create two forms with overlapping `includedUrls`, set both `active`, and compare their `views` / `submitted` counters manually. There is no audience-split / cohort assignment.

### No third-party newsletter sync (Mailchimp / Klaviyo / Brevo / Sendinblue)

**NOT supported** — no built-in sync to external CRMs. Submissions land in the platform's internal Subscriber list only.

Workaround: wire it via [[settings-hooks]] (the `subscriber.created` webhook fires on each form submission) or via the JSON-API v2 [[api-subscribers]] resource.

(The "mailchimp" string in storefront templates is the legacy `sf.module.mailchimp.newsletter.btn.subscribe` translation key for the *Subscribe* button label — purely a label, no integration.)

### Targeting gaps — only URL match, GDPR-cookie gate, and already-subscribed are supported

| Targeting axis | Supported? | Mechanism |
|----------------|-----------|-----------|
| **URL allow/deny** | YES | `pages.form.includedUrls[]` + `pages.form.excludedUrls[]`. |
| **GDPR cookies-consent gate** | YES | `cookies_consent` — see [[subscribe-forms-gdpr-consent]]. |
| **Already-subscribed visitors** | YES | `displayForAll` — hide from identified subscribers (default) OR keep showing. |
| **Per-device visibility** (only mobile / only desktop) | NO | Per-device *styling* exists (see [[subscribe-forms-layout]]), but no toggle to hide on one device. (verify) |
| **Per-language / per-locale** | NO | No locale-targeting toggle. |
| **Per-customer-group / per-tag** | NO | No customer-group filter on the form. (verify) |
| **Per-geo / per-region** | NO | No GeoIP-based gate. |
| **Time-of-day / day-of-week scheduling** | NO | Gate by date only by manually toggling `active` on [[subscribe-forms-list]]. |
| **After-N-page-views (frequency cap)** | NO | Only frequency cap is the binary per-form dismissal cookie (`popup-subscription-displayed_<form-id>`). |
| **Per-page-type** (cart, product, checkout, homepage) | NO | URL-only — no page-type axis; enumerate URLs or prefixes. (verify) |

### Trigger gaps — only 3 trigger types supported

The 3 built-in triggers are `auto`, `exitIntent`, `timeOnPage` — see [[subscribe-forms-triggers]]. NOT in the builder:

- After-N-page-views trigger.
- After-scroll-percentage trigger.
- After-click trigger (e.g. clicked-on-element).
- Inactivity trigger.
- Time-of-day / day-of-week trigger.
- After-N-product-views / -category-views trigger.

### Builder content gaps — no discount code-reveal, no multi-step quiz

Every form has exactly **two pages** (`form` + `success`) — see [[subscribe-forms-builder]]. There is no third page type:

- No separate consent-reveal page.
- No discount-reveal page with token interpolation. To reveal a code post-submit, the merchant writes it into the success page's title/description as a static string. For real per-subscriber unique codes, use [[marketing-discounts]] with a campaign — the form doesn't generate or hand out unique codes.
- No multi-step quiz / progressive profiling.

### Field-type gaps

The 6 custom-field types (`text`, `textarea`, `phone`, `select`, `radio`, `checkbox`) cover most lead-capture needs but exclude:

- **`file`** upload — no upload type.
- **`image`** — no image-pick type.
- **`date`** picker — no date type.

See [[marketing-subscribers-custom-fields]] for the full type catalogue.

### Built-in slots cannot be reordered or renamed at the schema level

The four built-in slots (`email`, `phone`, `first_name`, `last_name`) are keyed by name and render in a fixed order. The `label` setting changes the visible text but not the key. To insert content between them, the merchant uses custom fields. See [[subscribe-forms-fields]].

### Security gaps on the public submit endpoint

The `/subscribers/forms/{id}` POST has **NO** CAPTCHA, **NO** per-IP rate limit, and **CSRF verification is bypassed** (intentional, to allow cross-origin embeds, but it removes the normal CSRF defence). The HTML cache is also bypassed.

Programmatic spam can theoretically inflate the `submitted` counter and create subscriber records with arbitrary identifiers — merchants should know public forms can face hostile submissions. The only defences:

- Front-end module timing throttle.
- Cookie-based dismissal (`popup-subscription-displayed_<form-id> = false`).
- Channel-identifier uniqueness (a duplicate-email submit updates the existing subscriber rather than creating a new one).

See [[subscribe-forms-submission-flow]] for full submit-endpoint posture.

### Inverted `cookies_consent` semantic — by-design naming oddity

The `cookies_consent` flag on the form is inverted — `true` is the **bypass** ("form handles consent itself"), not the gate. See [[subscribe-forms-gdpr-consent]] for the full critical note. This is a frequent source of misconfiguration: merchants who set `cookies_consent = true` thinking they're requiring consent are actually instructing the storefront to **skip** the GDPR targeting-cookie check.

### Soft-delete persists counters

Deleted forms stop being served, but the form record plus its `submitted` / `views` counters remain stored indefinitely. There is no UI option to truly purge them. See [[subscribe-forms-list]].

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-triggers]] — only 3 built-in trigger types.
- [[subscribe-forms-layout]] — per-device positioning but no per-device visibility toggle.
- [[subscribe-forms-fields]] — 6 custom-field types; no `file` / `image` / `date`.
- [[subscribe-forms-gdpr-consent]] — inverted-semantic `cookies_consent` flag.
- [[subscribe-forms-submission-flow]] — public-endpoint security posture.
- [[marketing-discounts]] — workaround for per-subscriber discount codes.
- [[marketing-segments]] — `subscriber.from_form` for downstream revenue attribution.
- [[settings-hooks]] — `subscriber.created` webhook for external CRM sync.
- [[api-subscribers]] — programmatic equivalent.

## Open questions

- Whether tablet truly inherits desktop position or has its own breakpoint. (verify)
- Per-customer-group / per-tag visibility — confirmed absent in the builder UI, but worth re-checking against the form record schema for an undocumented field. (verify)
- Per-page-type axis — confirmed targeting is URL-only, but the storefront module might expose route-name awareness that the builder doesn't surface. (verify)
