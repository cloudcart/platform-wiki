---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Display triggers"
route_name: ""
route_path: ""
aliases: ["Subscribe form triggers", "Form display triggers", "startDisplaying", "stopDisplaying", "Exit intent popup", "Time on page popup", "Auto popup trigger", "Тригери на формата"]
tags: [marketing, subscribers, forms, triggers, popup, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list view, builder, templates, layout, fields, submission flow, GDPR consent, known issues).

# Subscribe forms — display triggers

## Purpose

The trigger array drives **when** a popup-mode form appears to the visitor. Each entry is `{type: <key>, ...params}`. The builder exposes exactly **three trigger types** (verbatim keys from the storefront module). Multiple triggers can be stacked — the form shows when ANY trigger fires (logical OR). A complementary `stopDisplaying` array suppresses display under similar conditions.

## Where to find it

Inside the form builder iframe (see [[subscribe-forms-builder]]) — the trigger picker is a top-level setting on the `form` page. Stored on the form record as:

```
pages.form.startDisplaying = [ {type: 'auto'}, {type: 'exitIntent'}, ... ]
pages.form.stopDisplaying = [ ... ]
```

## What the merchant can do here

- Pick one or more display triggers from the 3-value enum.
- Stack triggers (popup shows when ANY fires).
- Configure `stopDisplaying` to suppress under specific conditions.
- (For embedded forms — see [[subscribe-forms-builder]] — the trigger array is auto-set to `[{type: 'auto'}]` on save; the merchant's choice is overridden.)

## Settings & fields

### The 3 trigger types

| Trigger `type` | When it fires | Parameters | Notes |
|----------------|---------------|------------|-------|
| **`auto`** | Immediately on page load. | (none) | Default for embedded forms — the controller force-sets `startDisplaying = [{type: 'auto'}]` on save for any form with `embedded = true`. |
| **`exitIntent`** | When the visitor's cursor moves toward the browser tab close (top edge) — classic exit-intent detection. | (none) | Desktop-only behaviour; mobile has no cursor exit-intent equivalent. |
| **`timeOnPage`** | After N seconds on the current page. | `seconds: <int>` (also displayed in the UI in hours/days units). | The module shows the popup after the configured delay. |

### `stopDisplaying[]` — symmetric suppression

The `stopDisplaying` array has the same shape — used by the storefront module to gate re-display under conditions opposite to `startDisplaying`.

## Business rules

### Triggers stack as logical OR

Multiple `startDisplaying` entries fire as ANY-of: if either `exitIntent` OR `timeOnPage: 30` triggers, the form shows. There is no AND semantic — the merchant can't say "show only if visitor stayed 30 s AND moves toward tab-close".

### `auto` is forced for embedded forms

The controller mutates `startDisplaying = [{type: 'auto'}]` on save for any form with `embedded = true`. The merchant's choice is overridden — embedded forms always show as soon as the snippet's `<script>` evaluates inline. Similarly, the controller clears `pages.form.includedUrls` for embedded forms because the snippet's location implicitly defines where the form shows.

### Per-form, NOT per-device

`startDisplaying` is per-form — there is **NO** per-device trigger override (the trigger applies to whichever devices the form is visible on). For example, you can't say "exit-intent on desktop, time-on-page on mobile" — you can only stack both, and exit-intent silently won't fire on mobile (no cursor).

### Cookie-based dismissal complements the triggers

Once a visitor sees the form and dismisses it, the module JS writes a `popup-subscription-displayed_<form-id> = false` cookie so the same visitor isn't pestered repeatedly. This is independent of the trigger array — even an `auto` trigger won't re-show a dismissed form on the same browser. The cookie is per-form; a different form can still be triggered later. See [[subscribe-forms-gdpr-consent]] for the cookie-naming and the targeting-cookie gate.

### What triggers are NOT supported

The following common popup triggers are **NOT** in the builder:

- After-N-page-views trigger (frequency cap by page count).
- After-scroll-percentage trigger.
- After-click trigger (e.g. clicked-on-element).
- Inactivity trigger (visitor idle for N seconds).
- Time-of-day trigger.
- Day-of-week trigger.
- After-N-product-views / -category-views trigger.

The only frequency-cap mechanism is the per-form dismissal cookie (binary: shown or never-again-this-browser). For day-/time-scheduling, the merchant manually toggles `active` on/off on [[subscribe-forms-list]]. See [[subscribe-forms-known-issues]] for the full list of missing capabilities.

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-builder]] — where the trigger picker lives; also documents the embedded-mode auto-override.
- [[subscribe-forms-gdpr-consent]] — `popup-subscription-displayed_<form-id>` cookie + the targeting-cookie gate.
- [[subscribe-forms-known-issues]] — full list of missing trigger types.

## Open questions

None.
