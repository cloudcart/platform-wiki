---
type: feature
nav_path: "Design → Modules → Engagement → Form (cc_form)"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/{cc_form_instance}
aliases: ["CloudCart form module", "cc_form module", "Embedded form module", "Embedded subscribe form module", "Модул форма", "Embedded form"]
tags: [design, modules, engagement, form, cc_form, subscribe-form, page-builder]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Engagement module — cc_form (Embedded subscribe form)

> Part of [[design-modules-engagement]]. See the category page for the other engagement modules.

## Purpose

`cc_form` is the **page-builder block** that embeds a **pre-built subscribe form** ([[marketing-subscribers-subscribe-forms]]) at a specific position on a Dynamic page. The merchant builds the form once in the visual subscribe-form editor — multi-page wizards, custom fields, GDPR gates, theme-styled layout — and slots it into a landing page by picking it from this module's `form_id` dropdown.

`cc_form` is the **right tool** when the merchant needs a multi-field or multi-page lead capture form (e.g., "Book a consultation", "Request a quote", "Join our wholesale program") that does NOT fit the simple newsletter pop-up ([[design-module-newsletter]]) or the fixed-field contacts form ([[design-module-contact-form]]).

## Where to find it

This is a **page-builder block** — it appears in the **Add module** picker when the merchant is editing a **Dynamic** page in [[marketing-landing-pages]]. It does NOT appear on the **Design → Modules** tab list directly; it is only added by drag-and-drop into the canvas of a Dynamic page.

After drop, clicking the inserted block opens its settings side panel with the single `form_id` setting below.

## What the merchant can do here

- Pick which pre-built subscribe form to embed via the `form_id` dropdown — labelled *"Select form"*.
- Enable / disable the block instance.
- Save / Reset / Cancel — Reset clears the form_id (and the block renders nothing on the storefront).

## Settings & fields

| Field | Type | Validation | Default | What it controls |
|-------|------|------------|---------|------------------|
| `enabled` | toggle | `bool` | `true` | Master on/off — when off, the block renders nothing |
| `form_id` | select (autocomplete) | `required` | empty | Which pre-built subscribe form to embed — dropdown populated from the merchant's existing forms in [[marketing-subscribers-subscribe-forms]]. Label: *"Select form"* |

The dropdown is populated from a server-side query that returns all the merchant's **active**, **non-draft**, **embedded-enabled** subscribe forms — drafts and forms with `embedded = false` are filtered out.

## Theme dependencies

Page-builder block — works across themes that support the page-builder system. The block emits an async script tag pointing at the storefront's `subscribers.subscriptions.form.embed` route for the chosen form — this loads the form's CSS + JS dynamically and renders into the block's container. The rendered form picks up the THEME's styling automatically.

## Business rules

### Form must already exist

The `form_id` dropdown only lists forms that already exist in [[marketing-subscribers-subscribe-forms]]. The merchant must:

1. Build the form in the subscribe-forms editor first.
2. Mark it as **Active** (the list-page toggle).
3. Ensure it is **not a draft** AND it has `embedded = true` set in its config.

Only then will the form appear in `cc_form`'s dropdown.

### Plan gating — `subscriber_forms`

The `cc_form` module requires the `subscriber_forms` plan feature ([[plan-gates]]). When the merchant's plan lacks it:

- Forms count against the plan's `subscriber_forms` cap.
- Adding a NEW form via [[marketing-subscribers-subscribe-forms]] may be blocked.
- Existing forms are still resolvable via this module — the plan check happens at the form-creation step, not at the embed step.

### Active toggle on the form

The subscribe form's **Active** toggle (in the subscribe-forms list) governs whether the embedded form renders at all. Inactive forms still appear in the `cc_form` dropdown (because the dropdown filter only excludes drafts), but the embed script returns nothing — the storefront block renders an empty container.

### Deleting a form leaves a stale reference

When the merchant deletes the subscribe form referenced by a `cc_form` instance, the module's saved `form_id` keeps pointing at the missing ID. The storefront renders the block but the form area is empty (the embed script returns 404 or empty). There is no admin-side warning. To clean up, the merchant edits the page in the page builder and either picks a different form or removes the block.

### Newsletter pop-up vs cc_form — choose the right tool

| Use case | Use |
|----------|-----|
| One-step email capture, site-wide pop-up | [[design-module-newsletter]] (Mailchimp) |
| Multi-page wizard, custom fields, branching | `cc_form` + [[marketing-subscribers-subscribe-forms]] |
| Fixed contact form on `/contacts` | [[design-module-contact-form]] |

### Reset behaviour

Reset wipes `form_id` and resets `enabled = true`. The block stays on the page but won't render any form until the merchant picks a new `form_id`. This differs from removing the block (which deletes it from the page).

## How it works (verified against backend)

### Template path

The block template under the theme templates. The module class overrides `getTemplatePath` to prefer the platform code if the active theme has shipped its own copy.

### Storage

One `front_widget` row per block instance, with the block's unique mapping name. The blob contains `enabled` + `form_id`.

### Embed pipeline

The template emits a small JS bootstrap that:

1. Loads the `subscribers.subscriptions.form.embed` route for the chosen form ID — that endpoint returns a JS payload describing the form's modules, CSS, and JS URLs.
2. Inserts a `<link>` to the form's CSS and a `<script>` to the form's JS into the page head.
3. Calls `window.CcCam.start` once the JS loads — that's the platform's embedded-form runtime that renders the actual form modules into the page.
4. Cleans up the temporary `window.CcForm_<id>` bootstrap function.

### Dropdown query

`getForms` returns active, non-draft, embedded-enabled subscribe forms owned by the merchant, ordered by name. The module panel uses this to populate the `form_id` autocomplete.

### Cache

Save / Reset bumps the per-site cache key. The embedded form's JS / CSS payload itself is cached separately by the subscribe-forms embed endpoint.

### Page-builder integration

Because `cc_form` is a page-builder block, it is registered via the page-builder module palette. Its theme-config availability depends on the active theme's `modules` block having `cc_form` registered AND the merchant editing a `builder`-type page (Dynamic page).

### Hidden quirks

- The `form_id` dropdown is empty until the merchant has created at least one form in [[marketing-subscribers-subscribe-forms]].
- Multiple `cc_form` blocks on the same page can each target a different form — no conflict.
- The embed script makes a network request per block — pages with many `cc_form` blocks (e.g., a multi-form lead-capture landing page) can show a slight render delay.
- Inactive forms in the dropdown are not visually distinguished — the merchant has no in-page hint that the chosen form won't render.
- The module's `_widget_description` is read from the subscribe-form module's translation file — when that module is missing, the panel shows an untranslated key.

## Related

- [[design-modules-engagement]] — hub.
- [[marketing-subscribers-subscribe-forms]] — visual builder for the forms this module embeds.
- [[design-module-newsletter]] — sibling; simpler one-step email capture (Mailchimp).
- [[design-module-contact-form]] — sibling; fixed-field contacts-page form.
- [[marketing-landing-pages]] — Dynamic pages use the page-builder, which exposes this block.
- [[plan-gates]] — `subscriber_forms` plan feature gates form creation.
- [[design-themes]] — theme styling is inherited by the embedded form.

## Open questions

- 📡 **`subscriber_forms` plan feature.** Gates form creation, not the embed itself. GraphQL-resolvable: query the merchant's plan + feature-pack to determine the `subscriber_forms` cap.
- 📡 **Active forms count.** Forms embedded via `cc_form` count against the cap. GraphQL-resolvable: query the count of active subscribe forms on the merchant's store.
- ⏸️ **Stale `form_id`.** No admin-side warning when the referenced form is deleted. (verify) whether a future improvement surfaces orphaned `cc_form` references in a lint or warning.
