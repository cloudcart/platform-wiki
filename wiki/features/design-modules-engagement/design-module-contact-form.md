---
type: feature
nav_path: "Design → Modules → Engagement → Contact form (slot)"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/contactForm
aliases: ["Contact form module", "contactForm module", "Contacts page form", "Модул контактна форма", "Форма за контакт"]
tags: [design, modules, engagement, contact, contact-form]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Engagement module — contactForm (Contacts page form)

> Part of [[design-modules-engagement]]. See the category page for the other engagement modules.

## Purpose

`contactForm` is the **render slot** on the storefront's `/contacts` page that the theme uses to drop the platform's built-in **Name + Email + Phone + Subject + Message** form. It is one of the platform's **system modules** — every theme can rely on it being present, regardless of whether the theme JSON declares it. There is **no edit panel** for this module; the form's fields, validation strings, recipient email, and GDPR consent block are all configured outside the Modules screen.

This page documents how merchants control the form even though it has no settings panel of its own.

## Where to find it

The module itself shows no editable card on **Design → Modules → Contacts**. What the merchant CAN configure indirectly:

| To change | Go to |
|-----------|-------|
| Whether the form renders | The `show_form` setting on `contactInformation` — see [[design-module-contact-information]] |
| Recipient email for submissions | [[settings-general]] (`site_email`) |
| GDPR consent text | [[settings-general]] (GDPR section) |
| Custom multi-page / branching contact form | Build it in [[marketing-subscribers-subscribe-forms]] and embed via [[design-module-cc-form]] |

On the storefront, the form lives on `/contacts` alongside the [[design-module-contact-information]] block and (optionally) the [[design-module-contact-google-map]] block.

## What the merchant can do here

Effectively nothing on the Modules screen — `contactForm` is a `contact.form`-mapped slot with no editable settings of its own. To customise the surface a shopper sees, the merchant works through three other screens:

- Toggle visibility via [[design-module-contact-information]] → **Show form** dropdown.
- Change the recipient email in [[settings-general]].
- Replace with a custom multi-page form via [[design-module-cc-form]] + [[marketing-subscribers-subscribe-forms]].

## Settings & fields

The Modules screen shows **no edit panel** for `contactForm`. The form below is **hard-coded by the platform template** (the contact-form template under the theme templates):

| Form field | Type | Required | Notes |
|------------|------|----------|-------|
| `first_name` | text | yes (when guest) | Label: *"First name"* — hidden when the shopper is logged in |
| `last_name` | text | yes (when guest) | Label: *"Last name"* — hidden when logged in |
| `email` | email | yes (when guest) | Label: *"E-mail"* — hidden when logged in |
| `phone` | tel | no | International phone-format picker (`js-phone-intl`) — hidden when logged in |
| `subject` | text | yes | Label: *"Subject"* — pre-fills when navigated from a product "request product" link |
| `message` | textarea | yes | 5 rows — pre-fills similarly |
| GDPR consent | checkbox | yes (when GDPR enabled) | Pulled from the platform's `contacts` GDPR form definition |
| Google reCAPTCHA v3 | hidden | yes | Anti-spam — automatic via `GoogleReCaptchaV3` integration |

The merchant cannot add custom fields, remove the GDPR block, or change validation rules through this module. **For a custom contact form**, see [[design-module-cc-form]].

**Hidden fields injected when arriving from a product page:**

- `requested_product_id` — set when the shopper landed on `/contacts` via a product detail's "Ask about this product" link.
- `requested_variant_id` — same, for a specific variant.

These cause the form to behave as a **product-request form** rather than a generic contact form — the merchant's inbox shows which product the shopper was asking about.

## Theme dependencies

- Most modern themes (a theme that ships it, `echappe`, another custom theme, etc.) ship a `contactForm` entry in their theme JSON mapping to `contact.form`.
- `contactForm` is also in the platform's **hard-coded system-module list** — it is always resolvable via the module facade even if the theme JSON omits it.
- A theme without a `/contacts` page slot simply doesn't render the form. The merchant cannot edit the form template through the admin; only a custom theme can override its layout.

## Business rules

### No edit panel — slot only

Clicking through to `/admin/storefront/widgets/contactForm` returns a 404 because the module exposes no editable settings. The Modules screen index does not show a card for it.

### Recipient is store-wide

Form submissions are routed to the email address configured in [[settings-general]] (`site_email`) — there is **no per-module recipient override**. To change where contact submissions land, the merchant edits the general settings, not the module.

### Logged-in customers skip the identity fields

When the shopper is signed in, the **first name / last name / email / phone** rows hide automatically — the form uses the customer's saved details. Only **subject** + **message** + GDPR remain visible.

### Anti-spam

Google reCAPTCHA v3 is automatically inserted by the platform. The merchant does not see a captcha toggle in the Modules screen. If reCAPTCHA fails to load (ad-blocker / network), the form silently fails on submit — there is no visible captcha element to signal this, only an AJAX error.

### Submit endpoint

The form posts to the storefront's `contacts` route via AJAX (`js-form-submit-ajax`). On success, the page emits the jQuery custom event `cc.contact.form.sent` and resets the form. The success / error messages are platform translation strings (e.g., *"Your message was sent"*), not editable per-module.

### Product-request mode

When `requested_product_id` is set (the shopper clicked "Ask about this product" on a product detail), the same form persists the product reference into the contact-message payload. The merchant's inbox can then surface which product the shopper was asking about. See [[settings-emails]] for the templates used. Note: the **subject** and **message** fields pre-fill from any matching query-string or session value, not only from the product-request flow.

## Related

- [[design-modules-engagement]] — hub.
- [[design-module-contact-information]] — sibling; controls `show_form` and the text blocks around the form.
- [[design-module-contact-google-map]] — sibling; usually rendered next to the form on `/contacts`.
- [[design-module-cc-form]] — sibling; the way to embed a custom multi-page contact form instead of this fixed one.
- [[settings-general]] — sets `site_email` (recipient) + GDPR consent text.
- [[settings-emails]] — email templates used for contact-form notifications.
- [[marketing-subscribers-subscribe-forms]] — visual builder for custom multi-page forms.

## Open questions

- 📡 **Per-store contact-form recipient.** Configured in [[settings-general]] under `site_email`. GraphQL-resolvable: query the merchant's general settings to read the recipient.
- 📡 **GDPR consent text.** The `contacts` GDPR form definition is in the platform-level GDPR config. GraphQL-resolvable: query whether GDPR is enabled and the consent body for the `contacts` form.
- ⏸️ **Product-request mode.** Triggered automatically by hidden `requested_product_id` field — no merchant-side configuration. (verify) whether a separate notification template fires when the field is present.
