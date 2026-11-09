---
type: storefront-page
route_name: contacts
route_path: /contacts/{product_url_handle?}
themes_using: [all]
tags: [storefront, contacts, forms, recaptcha]
created: 2026-06-08
updated: 2026-11-09
source_count: 4
---

# Contacts page (storefront)

## Purpose

The customer-facing contact page. Combines optional Google Maps embed, store contact details (phone, e-mail, address, business hours), free-text page intro, and a contact form whose submissions are e-mailed to the merchant's `site_email`.

## URL & route

- **Route name:** `contacts`
- **Path:** `/contacts/{product_url_handle?}` (also accessible at `/about/{product_url_handle?}` via route name `about`).
- **Method:** `GET` for the page, `POST /contacts/{product_url_handle?}` for the form submission.
- **Middleware:**
  - GET: a submission throttle, `uuid_generate`, `subscriber_uuid`.
  - POST: same + `gdpr_policy_acceptances`.
- **Optional `product_url_handle`** — when the customer clicks "Ask about this product" on a product page, the controller prefills `requested_product_id` / `requested_variant_id` hidden fields.

## How it loads

1. Route resolves to the request handler (or `@send` on POST).
2. The template builds a `$google_map_enabled` flag from the platform code.
3. When enabled, the map block and the information block render side-by-side at the top of the page.
4. If the merchant set a `page_text` in **Contact information** settings, it renders as a free-form HTML block above the form.
5. The form itself renders only when the platform code.
6. SEO + breadcrumb microdata come from the theme templates and the theme templates.

## What the customer sees

- Breadcrumb: **Home › Contacts** (label `sf.global.contacts`).
- Hero band with the Google Map embed and store info card (when the map is enabled).
- Optional intro paragraph (`page_text`).
- Contact form titled "Contact us" (`sf.global.header.contact_us`).

The form fields (rendered only when the customer is NOT logged in):
- `first_name`, `last_name`, `email`, `phone` (with international phone formatting via `js-phone-intl`).

Always-visible fields:
- `subject` (required text).
- `message` (required textarea).
- GDPR acceptances block (per the `gdpr_form='contacts'` configuration).
- Google reCAPTCHA v3 hidden field (the platform code) — invisible, with the platform's own keys and always on; the merchant has no CAPTCHA setting ([[seo-ai-visibility]]).
- Submit button labelled `sf.global.act.send`.

Logged-in customers skip the name / e-mail / phone fields — those identity values are pulled from the account.

## Storefront behaviour

- **AJAX submit** — the form has class `js-form-submit-ajax`; submission posts to `route('contacts')` and returns a JSON status.
- **Throttle** — a submission throttle allows 10 submissions per minute per session/IP.
- **reCAPTCHA v3** — the hidden `g-recaptcha-response` token is regenerated on every submit attempt; on success/error the script replaces `#contact_us_id` and calls `onloadCallback` to refresh the token.
- **GDPR** — `gdpr_policy_acceptances` middleware enforces the consent boxes when the store has GDPR policies configured.
- **Product-context contact** — when the URL includes `/contacts/{product_url_handle}`, hidden fields `requested_product_id` and `requested_variant_id` are added so the merchant sees which item triggered the question.
- **Where it goes.** Each submission is sent as the **Contact request** admin notification (`contact`) to the store email, `site_email` ([[settings-general]] → Store Details → Email). The visitor's name is the sender name and their address the Reply-To, so replying answers the visitor. It is not sent when that notification or the admin-notifications master switch is off ([[settings-admin-notifications]]).
- **Nothing is kept in the admin.** The message is not saved anywhere in the admin panel and raises no alert at the bell; the email is the only copy. The sender's email is added to [[marketing-subscribers]] (source: contact form) when the store uses the Email channel; marketing consent is set only if they gave it on the form.

## JavaScript behaviour

- `#contact-form` / `.extra-contact-form-js` — the form node.
- `js-form-submit-ajax` — generic AJAX submit handler.
- `js-loading` — shows a spinner on the submit button while in-flight.
- `js-phone-intl` — initialises international phone formatting (`window.Phone.init`).
- Event `cc.contact.form.sent` — fires on success; the inline `<script>` resets the form.
- Events `cc.ajax.error` / `cc.ajax.success` — the form swaps the reCAPTCHA hidden div and re-triggers `onloadCallback` so the next attempt has a fresh token.

## Customisations available to the merchant

- **Contact information module** — merchant fills phone, address, e-mail, business hours, custom info via the storefront module editor.
- **Google Map module** — enable / disable, set address pin and zoom (uses the merchant's Google Maps key).
- **show_form / show_custom_information / page_text** — three settings on the module; control which sections render.
- **GDPR text** — managed under the GDPR / legal policies area (see [[settings-general]] — verify exact location).
- **reCAPTCHA** — nothing to configure: the keys are the platform's own and the check is always on.
- **`site_email` recipient** — where submissions land; one store-wide address, set under [[settings-general]].

## Theme variations

- All themes use the same contact modules. Layout differs in:
  - Position of the map (top hero vs sidebar).
  - Whether the contact-info card overlays the map or sits beside it.
  - Stack order on mobile.
- The same template serves `/about/{product_url_handle?}` (route name `about`) — themes that style "About" differently still call the theme templates and the same map module.

## Known issues / by-design vs bug

- Disabling both the map and `show_custom_information` AND the form leaves only the breadcrumb + optional `page_text` block visible — by design.
- The international-phone script (`window.Phone.init`) must be loaded — themes without the dependency JS will leave the phone field unformatted.
- a submission throttle is shared with `/about/*` and other forms in the same throttle group — high-traffic stores may hit the limit during spam waves.
- Submissions without GDPR consent are blocked by middleware before the controller runs.

## Related

- [[settings-general]]
- [[storefront-architecture]]
- [[storefront-known-issues]]

## Open questions

- Confirm the storefront module key/path the merchant uses to edit `show_form` / `page_text` / `show_custom_information` (likely under Theme Editor → Pages → Contacts — verify).
- Confirm whether `gdpr_policy_acceptances` blocks the request entirely or returns a structured validation error for the AJAX submit.
