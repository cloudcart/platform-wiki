---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → Submit button & confirmation"
route_name: subscribe-forms.form
route_path: /admin/marketing-new/subscribers/subscribe-forms/form/:id?
aliases: ["Subscribe form submit button", "Subscribe form button action", "Submit form and display confirmation info", "Submit form and go to url", "Form button action type", "actionType", "Success page", "Confirmation page", "Subscribe form thank you page", "What the button does", "Бутон на формата за абониране", "Изпрати формата и покажи потвърждение", "Изпрати формата и отиди на url"]
tags: [marketing, subscribers, forms, button, confirmation, submission]
plan_gates: ["subscriber_forms"]
created: 2026-06-30
updated: 2026-06-30
source_count: 2
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list, builder, templates, layout, triggers, fields, submission flow, GDPR consent, known issues).

# Subscribe forms — submit button & confirmation

## Purpose

**What the form's submit button does when the visitor clicks it, and what they see next.** This is the "on submit" layer of the form: the button's label and visibility, the **two action types** (`submit` vs `url`), and the **success / confirmation page** that the `submit` action shows. The rest of the visual editor is on [[subscribe-forms-builder]]; the server-side handling after submit (subscriber creation, verification, segments) is on [[subscribe-forms-submission-flow]].

## Where to find it

In the builder ([[subscribe-forms-builder]]): the **form page → button** block (its text, action type, and URL), and the separate **success page** (the confirmation the visitor sees after submitting). The settings live on the form record under `pages.form.button` and `pages.success`.

## What the merchant can do here

- Set the **button label** and whether the button is shown at all.
- Choose **what happens on submit**: show a confirmation page, or redirect to a URL.
- Design the **confirmation (success) page**, or fall back to the platform default thank-you.
- Set what the **success-page button** does: close the form, or go to a URL.

## Settings & fields

### The submit button (form page) — `pages.form.button`

| Setting | Key | What it does | Validation |
|---|---|---|---|
| **Button visible** | `pages.form.button.visible` | Show / hide the submit button. | Boolean. |
| **Button text** | `pages.form.button.text` | The button label. | Required **unless** the button is hidden — *"Button text is required when button is not hidden."* |
| **Button action type** | `pages.form.button.actionType` | What clicking the button does (the two options below). | Required field. |
| **Button URL** | `pages.form.button.actionUrl` | The redirect target — used only when action type is `url`. | Required when actionType = `url`; must be a valid URL — *"Form button url is not valid."* |

### Action types — what happens on submit

These are the two options the merchant picks for **"Изпрати формата и …"** / **"Submit form and …"**:

| `actionType` | UI label | Behaviour |
|---|---|---|
| **`submit`** | *"Submit form and display confirmation info"* | Save the subscriber, then **show the form's success / confirmation page**. This is the default. |
| **`url`** | *"Submit form and go to url"* | Save the subscriber, then **redirect** the visitor to the merchant-supplied **Button URL** (`pages.form.button.actionUrl`). |

Both options **save the subscriber first** — `url` redirects *after* the capture, so it is not a way to skip collecting the subscriber. There are only these two form-button actions; there is no "stay on page / reset" or "show a message inline" third option.

### The confirmation (success) page — `pages.success`

The **`submit`** action shows the form's **success page**. The merchant either designs it or uses the platform default:

- **`pages.success.is_default = true`** — show the **platform default** thank-you.
- **Custom** — design the success page: title, description, media (per device), and a styled **success-page button** (below).
- **Cross-validation:** if the button is **visible** AND action type is **`submit`** but the success page has **no content**, the save is rejected with *"You need to fill in confirmation info"* — a "show confirmation" button needs confirmation content (or set `is_default`).

### The success-page button — `pages.success.button`

| `actionType` | UI label | Behaviour |
|---|---|---|
| **`close`** | *"Close"* | Close / dismiss the popup. |
| **`url`** | *"Go to url"* | Redirect to a merchant-supplied URL (`pages.success.button.actionUrl`). |

## Business rules

- **Capture happens regardless of action.** Whether the merchant chose `submit` (confirmation) or `url` (redirect), the subscriber is saved before anything is shown — see [[subscribe-forms-submission-flow]].
- **Confirmation vs email verification are different things.** The on-submit confirmation page is what the visitor *sees*; whether the subscriber is *verified* depends on **Mark as verified** vs **Send validation email link** (double opt-in) — that gate is on [[subscribe-forms-builder]] / [[subscribe-forms-submission-flow]], not the button action. A `submit` confirmation still shows even when the email-validation link is pending.
- **No success-page extras out of the box.** No auto-close timeout, no built-in social-share buttons, no copy-to-clipboard discount-reveal — the merchant writes any such interaction as plain HTML/CSS in the success page's title / description (see [[subscribe-forms-known-issues]]).
- **Deliver a promo code straight on the success page.** The success page's **title / description** accept free text, so a merchant who just wants to reward the sign-up can type a **static, shared discount code** (e.g. `WELCOME10`) directly into the confirmation content. The subscriber sees it **immediately on screen** the moment they submit — no email send, and no automation/campaign delay. Create the matching code on [[marketing-discounts-code-pro]] (or any discount that accepts a code) so it actually applies at checkout, then paste that same code into the success text. Caveat: this is **one shared code for everyone** — for a **unique per-subscriber code** the merchant still needs generated discount codes plus a delivery step (an automated campaign / flow that emails each subscriber their own code), which is the slower path this shortcut avoids. The success page cannot generate or personalise a code on its own.

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-builder]] — the rest of the visual editor (fields, pages, styling, popup vs embedded).
- [[subscribe-forms-submission-flow]] — what the backend does after the button is clicked (subscriber creation, verification, segments).
- [[subscribe-forms-fields]] — the input slots the button submits.
- [[subscribe-forms-known-issues]] — success-page limitations + workarounds.

## Open questions

None.
