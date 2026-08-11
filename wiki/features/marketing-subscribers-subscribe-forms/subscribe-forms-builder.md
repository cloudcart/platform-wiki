---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Builder"
route_name: subscribe-forms.form
route_path: /admin/marketing-new/subscribers/subscribe-forms/form/:id?
aliases: ["Subscribe form builder", "Form builder iframe", "Subscribe forms editor", "Визуален редактор за форми"]
tags: [marketing, subscribers, forms, builder, popup, embedded, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list, button & confirmation, templates, layout, triggers, fields, submission flow, GDPR consent, known issues).

# Subscribe forms — visual builder

## Purpose

The drag-and-drop visual editor where the merchant composes a subscribe form: structural template, layout position, display triggers, input slots, custom fields, terms checkboxes, styling per element, success-page content. The builder runs in an isolated preview frame so its styling never clashes with the admin panel.

## Where to find it

Opened from [[subscribe-forms-list]] by clicking **Add form** or an existing form's row name. Route: `/admin/marketing-new/subscribers/subscribe-forms/form/:id?`. The breadcrumb reads Marketing → Subscribe forms → Edit form (existing) or New form (no `:id`).

## What the merchant can do here

- Compose two pages (`form` + `success`) — see [[subscribe-forms-fields]] for input slots per page.
- Pick a structural template ([[subscribe-forms-templates]]), set layout position per device ([[subscribe-forms-layout]]), and configure popup display triggers ([[subscribe-forms-triggers]]).
- Style every element (colors, borders, spacing, ~80 Google Fonts, per-device background images, dimensions).
- Pick subscriber custom fields from [[marketing-subscribers-custom-fields]].
- Attach legal terms pages as checkboxes — see [[subscribe-forms-gdpr-consent]].
- Add visibility rules: included-URLs (allowlist), excluded-URLs (denylist), `displayForAll`, `cookies_consent`.
- Toggle **Mark as verified** vs **Send validation email link** — mutually exclusive; see [[subscribe-forms-submission-flow]].
- Toggle **Embedded** between popup mode and inline page-module mode.
- Free-text **Tags** auto-applied to every captured subscriber.

## Settings & fields

### Top-level form fields

| Field | What it does | Validation |
|-------|--------------|------------|
| **Title** (`pages.form.texts.title.text`) | Form heading shown to the visitor. | Max 200 characters. |
| **Description** (`pages.form.texts.description.text`) | Subtitle / instructional text. | Max 5000 characters. |
| **Button text** (`pages.form.button.text`) | Submit-button label. | Required unless the button is set to hidden. |
| **Button action type** (`pages.form.button.actionType`) | `submit` (save subscriber + show success page) or `url` (also redirect). | Required field. |
| **Button URL** (`pages.form.button.actionUrl`) | Redirect target when action type is `url`. | Required if actionType=url; must be valid URL ("Form button url is not valid"). |
| **Success page is default** (`pages.success.is_default`) | Use platform default success message vs merchant custom content. | Cross-validated: *"You need to fill in confirmation info"* if button visible + actionType=submit but success page empty. |
| **Included URLs** (`pages.form.includedUrls`) | Allowlist of URLs where the form is allowed to appear. | Each must be a valid URL ("In settings for display has invalid urls"). |
| **Excluded URLs** (`pages.form.excludedUrls`) | Denylist of URLs where the form is suppressed. | Each must be a valid URL ("In settings for not display has invalid urls"). |
| **Display for all** (`displayForAll`) | If TRUE, the form is shown even to already-subscribed visitors. If FALSE (default), it's hidden after the visitor subscribes. | Boolean. |
| **Cookies consent** (`cookies_consent`) | GDPR targeting-cookie gate — **inverted semantic**. See [[subscribe-forms-gdpr-consent]]. | Boolean. |
| **Embedded** (`embedded`) | If TRUE, this form is INLINE (not popup) — embedded into a specific page via the JS snippet. When set, the platform forces `startDisplaying = [{type: 'auto'}]` and clears the included-URLs list. | Boolean. |
| **Mark as verified** (`pages.form.markAsVerified`) | Submitted email marked verified=1 immediately (no double-opt-in). | Boolean — mutually exclusive with email-confirm. |
| **Send validation email link** (`pages.form.emailConfirm`) | Sends "Email confirmation for subscription in store:site_name" email; verified=1 only after click. | Boolean — mutually exclusive with mark-as-verified. |
| **Custom fields** (`pages.form.custom_fields[]`) | Pick from defined subscriber custom fields; per field: `is_visible`, `required`, `label`, `placeholder`, custom styling. | Each must reference an existing SubscriberFormFields key. |
| **Terms** (`terms`) | Multi-select of `Page` rows (legal pages, marketing policies). Each has `required` + custom `labelStyle`. | Required-flagged terms become validation rules at submit — see [[subscribe-forms-submission-flow]]. |
| **Tags** (`tags`) | Array of tag strings auto-applied to subscribers who submit. | Free text. |

### Two pages — `form` + `success`

Every form has exactly **two pages** in its `pages` object:

| Page key | Purpose | Configurable content |
|----------|---------|----------------------|
| **`form`** | Input page the visitor sees. | Title, description, four built-in input slots (email / phone / first_name / last_name), custom fields, terms checkboxes, submit button, media (per device), page style, display triggers, included/excluded URLs. |
| **`success`** | Post-submit confirmation page. | Title, description, media (per device), success button (`close` or `url` actionType), button styling. **Or** `success.is_default = true` — platform default thank-you. |

There is **no third page type** — no consent-reveal, discount-reveal, multi-step quiz, or progressive-profiling page. See [[subscribe-forms-known-issues]] for what's NOT supported and workarounds (e.g. hard-coding a discount code into the success page's description).

### Submit button & confirmation — own page

What the submit button **does** (action types `submit` = show confirmation / `url` = redirect), the **success / confirmation page**, and the success-page button (`close` / `url`) are documented on **[[subscribe-forms-button-actions]]** — "what happens on submit and what the visitor sees next".

### Styling

Styling is exposed at every level — page background, form container, each input, button, label, terms checkbox:

- **Colors** — `backgroundColor`, `color`, `borderColor`.
- **Borders** — `borderRadius`, border width/style.
- **Spacing** — padding, margin.
- **Typography** — `fontFamily` (~80 pre-loaded Google Fonts), `fontSize`, font weight/style.
- **Background image** — `pages.form.media[<device>]` per device (success page has its own `media`).
- **Dimensions** — the form's **width and height are pixel values** in the page `style` (the form page and the success page each carry their own). They are stored **free-form** — the settings request does not validate or clamp them — and applied by the builder's own render, so there is **no enforced min/max**: an over-large width or height can overflow narrow viewports. There is no auto-fit/auto-resize; the only responsiveness is the separate per-device `layoutPosition` (see [[subscribe-forms-layout]]), which changes *placement*, not *size*. Widening/heightening a form is therefore a manual px edit, and the merchant must check it on mobile themselves. (verify — the exact width/height input controls in the legacy iframe builder UI.)

## Business rules

### Two form types — popup vs embedded

A single form either renders as a **popup** (or slide-in / sticky bar — layout position via `layoutPosition`, see [[subscribe-forms-layout]]) injected into every eligible storefront page, OR as an **embedded** form inline inside one specific page where the merchant pasted the snippet. The `embedded` boolean toggles the two modes:

- **Popup mode** (`embedded = false`): up to **5 forms** load at storefront startup; the storefront picks one or rotates among them. Display triggers per [[subscribe-forms-triggers]].
- **Embedded mode** (`embedded = true`): loaded per-page where its snippet runs; renders inline on page load (`startDisplaying = [{type: 'auto'}]`, set automatically).

### Page-builder integration — embedded form as a page module

Beyond the standalone embed snippet, embedded subscribe forms can be added as a **module inside the Page Builder** — labelled *"Embedded subscription form"* (*"With this module, you will be able to embed a subscribe form into the page you are creating"*). This is the merchant-friendly way to drop a subscribe form into a custom landing page without hand-pasting the JS snippet.

### Verify-action — mutually exclusive in the UI, precedence in backend

The UI presents Mark as verified / Send validation email link as mutually exclusive; if both were set, `markAsVerified` wins — see [[subscribe-forms-submission-flow]] for full precedence.

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[marketing-subscribers-custom-fields]] — define custom fields the builder can pick from.
- [[marketing-subscribers]] — destination — every submission becomes a subscriber here.

## Open questions

None.
