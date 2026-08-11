---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → CloudCart form"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["CloudCart form module", "CC form block", "Form embed block", "Subscriber form embed", "Модул форма CloudCart"]
tags: [design, modules, page-builder, forms, marketing, subscribers]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# CloudCart form block (`cc_form`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **CloudCart form** block embeds a CloudCart-managed form (subscriber signup form, contact form, lead capture form) directly inside a Dynamic page. The merchant builds the form in [[marketing-subscribers-subscribe-forms]] then drops the corresponding form via this block on any landing page. The form renders inline (no pop-up, no off-canvas) and submits to the same Subscribers backend as if it lived in a header pop-up.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **CloudCart form** from the block picker.

## What the merchant can do here

- Pick a form from the dropdown — the list shows every active, non-draft form owned by the store, with type = `form`.
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot create or edit forms from this block — that lives in [[marketing-subscribers-subscribe-forms]].
- The merchant cannot configure form fields, validation, or styling from this block — those are properties of the form itself.
- The merchant cannot pick a form that is in `draft` status — the dropdown only shows published, active forms.
- The merchant cannot pick a form of type `pop_up` from this block — only `form`-type entries appear in the dropdown.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. Stored as `int(0|1)` after `saveSettings`. |
| `form_id` | select (dropdown) | `''` | Form ID — sourced from the Subscribers `SubscriberForm` model, filtered to active, owned, non-draft, type = `form`. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Form catalogue is store-scoped

The dropdown lists only forms owned by the active store — the model query is the platform code. Forms from other stores never appear.

### Embed script is rendered inline

When the block renders, the storefront template outputs an inline `<script>` that loads the form's embed payload via the route `subscribers.subscriptions.form.embed` (with `/admin/` stripped from the URL — see the embed script). The embed payload is a JSON-with-CSS-and-JS object that the browser injects into the page at the block's position.

### Subscribers app dependency

The form catalogue depends on the Subscribers app — see [[marketing-subscribers]] (or the Subscribers pillar). Without forms created on the Subscribers screen, the dropdown is empty and the block renders nothing.

### `enabled` is sanitised on save

The module's `saveSettings` method coerces `enabled` to an `int(0|1)` — anything submitted as `enabled` from the form is treated as ON, missing key as OFF. This makes the toggle behaviour deterministic.

### Empty `form_id` renders nothing

The template wraps the embed script in `{if $module->getSetting('form_id')}` — if no form is picked, the block renders zero HTML. This avoids broken-form errors.

### Form submissions go to the same backend

Whether the form is embedded via this block or rendered as a pop-up on the storefront, submissions land in the same Subscribers backend. The merchant sees the leads in the same Subscribers report in [[marketing-subscribers]].

## Related

- [[design-modules-page-builder]] — hub.
- [[marketing-subscribers-subscribe-forms]] — form catalogue (the source of the dropdown).
- [[marketing-subscribers]] — subscriber catalogue (lead destination).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Per-language form embed.** With `multylang`, does the embed render the form in the customer's storefront language? (verify against the embed payload)
- 📡 **Inline render vs. iframe.** The current template uses an inline `<script>` that injects into the parent DOM — confirm there is no iframe sandbox, so CSP rules may need to allow inline scripts. (verify against the embed payload + storefront CSP)
