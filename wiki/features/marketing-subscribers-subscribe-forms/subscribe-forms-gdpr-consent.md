---
type: feature
nav_path: "Marketing → Subscribers → Subscribe Forms → GDPR consent"
route_name: ""
route_path: ""
aliases: ["Subscribe form GDPR", "cookies_consent semantic", "Marketing policy gate", "PolicyAcceptanceLog on subscribe form", "Targeting cookie group gate", "Inverted cookies_consent flag", "GDPR на формата за абонамент"]
tags: [marketing, subscribers, forms, gdpr, consent, cookies, audit, storefront]
plan_gates: ["subscriber_forms"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-subscribers-subscribe-forms]]. See the hub for the other aspects (list view, builder, templates, layout, triggers, fields, submission flow, known issues).

# Subscribe forms — GDPR + cookie consent

## Purpose

Subscribe forms intersect GDPR in three distinct ways:

1. **Display gating** — the `cookies_consent` flag on the form determines whether the storefront targeting-cookie group must be accepted before the form is allowed to show.
2. **Marketing-consent capture** — ticking the marketing-policy terms page on submission propagates marketing consent to both the Subscriber and any matched Customer.
3. **Audit log** — every successful submission writes a `PolicyAcceptanceLog` row per ticked policy page, capturing IP / UA / time / content snapshot for compliance.

This page documents the inverted `cookies_consent` semantic — the most-misread setting on the form record.

## Where to find it

- **`cookies_consent` flag** — in [[subscribe-forms-builder]] (top-level form settings).
- **Marketing-policy gate** — set on the GDPR app (`marketing_policy` setting) or legacy `checkout_terms_page` setting — see [[apps-gdpr-overview]].
- **Targeting-cookie group** — managed on [[apps-gdpr-cookies]].
- **`PolicyAcceptanceLog`** — populated automatically on each successful submit; no admin UI surfaces it directly (verify).

## What the merchant can do here

- Decide whether the form is allowed to render before the visitor accepts the GDPR targeting-cookie group.
- Designate which legal Page is the **marketing-policy page** (via the GDPR app's `marketing_policy` setting, or the legacy `checkout_terms_page` fallback).
- Attach terms checkboxes (any Page) to the form's `terms` array, marking each as required or optional with custom label styling.
- Rely on automatic `PolicyAcceptanceLog` writes for GDPR compliance — every ticked policy gets its own log row at submit.

## Settings & fields

### The `cookies_consent` flag — INVERTED SEMANTIC (critical)

This is the single most-misread setting on the form record. The flag does **NOT** mean "form requires consent". It means the OPPOSITE:

| `cookies_consent` value | Meaning | Storefront behaviour |
|-------------------------|---------|----------------------|
| **`true`** | "The form itself handles consent" — i.e. the form's own UI captures marketing consent; the storefront should serve it regardless of the GDPR `targeting` cookie group state. | Form is shown to ALL eligible visitors, even those who haven't accepted the `targeting` cookie group yet. |
| **`false`** | "The form needs the platform's targeting consent first." | Form is **suppressed** until the visitor accepts the `targeting` cookie group via the GDPR consent banner. |
| **`null`** (default — unset) | Same as `false` — the form needs targeting consent. | Suppressed until targeting cookies accepted. |

When the visitor has not accepted the `targeting` cookie group, only forms with `cookies_consent = true` OR `cookies_consent = null` are served. Critical takeaway: `cookies_consent = true` is the **bypass**, not the gate.

### Marketing-policy gate — precedence at submit

The submission flow's marketing-consent logic checks for a designated **marketing-policy page**:

- **(a)** If the GDPR app is active → the GDPR `marketing_policy` setting (the legal Page the merchant designated as the marketing-consent gate).
- **(b)** Else, only if the store does NOT have `hide_marketing = true` → the store's `checkout_terms_page` setting (legacy fallback).
- If `hide_marketing = true` AND GDPR is off → there's no marketing-policy page at all → no marketing checkbox is enforced.

At submit:

- If the visitor ticked the marketing-policy checkbox → the subscriber is created with marketing consent forced on. This is the **forced override** that bypasses per-channel default behaviour.
- If not → the subscriber row is created but excluded from marketing campaigns (marketing off).

**Customer propagation**: if the visitor's email matches an existing Customer AND marketing was forced on, the Customer's marketing flag is also updated to "yes" — same email, two records, propagated together.

### `PolicyAcceptanceLog` — per-policy audit row

When a submission succeeds and the request carries a `terms` array, the system writes a `PolicyAcceptanceLog` row **per ticked policy page**, with:

- `email` (from `email` field, or `phone` if email empty).
- `customer_id` (if matched to an existing customer).
- `content_id` — stable hash of the policy's name + content (re-used when content changes so the audit log preserves history).
- `ip`, `user_agent`.
- `form = 'segment_subscription_popup'` — the constant identifying the subscribe-form context, distinct from `'mailchimp_newsletter'`, `'submit_payment'`, `'contacts'`, etc.

This makes the subscribe form an **audit-grade GDPR consent capture point** — the merchant has per-acceptance log row with IP / UA / time / content snapshot for compliance audits.

## Business rules

### Dismissal cookie

Once a popup form is shown and dismissed, a `popup-subscription-displayed_<form-id> = false` cookie is written so the same visitor isn't pestered repeatedly. The cookie is per-form (a different form can still be triggered later). This `popup-subscription-displayed_*` prefix is whitelisted by the encrypted-cookies layer so the storefront JS can read it in cleartext. The popup also needs its `startDisplaying` trigger to have fired — see [[subscribe-forms-triggers]].

### Storefront eligibility filter — full query

When a storefront page renders, the available subscribe forms are filtered by:

1. `site_id = current store` (multi-tenant isolation).
2. `active = true`.
3. `draft != true`.
4. `type = 'form'`.
5. **For popup mode**: `embedded != true`. **For embedded mode**: `embedded = true` AND `_id = <requested id>`.
6. If visitor is identified (already a subscriber): only forms with `displayForAll = true` are returned. Anonymous visitors get all eligible forms.
7. **GDPR targeting-cookie filter**: if the visitor hasn't accepted the `targeting` cookie group, forms with `cookies_consent = false` are excluded (only `cookies_consent = true` or `null` pass — see inverted-semantic note above). Read the field as `bypassCookieGroupGate` to avoid the intuitive-but-wrong reading; see [[subscribe-forms-known-issues]] for this by-design naming oddity.
8. **Cookie-based dismissal**: `popup-subscription-displayed_<form-id> = false` cookies are read; any matching form id is excluded from results.
9. Limit 5 results (popup mode) — defensive cap; embed mode is effectively 1 by id match.

### GDPR-active vs GDPR-off — different gating

For stores with GDPR active (or the legacy `setting('hide_marketing')` flag), marketing acceptance must be captured **explicitly** via the marketing-policy terms checkbox. Without that tick, the subscriber row exists but `marketing = 0` and the subscriber is in the audience pool but cannot be sent marketing campaigns.

For stores with GDPR off AND `hide_marketing = false`, there's no marketing-policy page enforced — the checkbox is not required, and consent is implicit via the act of submitting (legacy behaviour).

### Disadvantages of running WITHOUT the GDPR module

The subscribe form still works without the GDPR app, but the merchant gives up the consent guarantees the module provides:

- **No explicit opt-in.** With no marketing-policy page to attach, there is no marketing-consent checkbox on the form — consent is treated as *implicit* from the act of submitting. That is legally weaker than an explicit ticked opt-in and harder to defend under GDPR / ePrivacy.
- **No audit-grade consent log.** `PolicyAcceptanceLog` rows are written **only** when the submission carries ticked policy pages (the `terms` array). With no GDPR marketing-policy page there is nothing to tick, so **no per-acceptance record** (email, IP, user-agent, timestamp, content snapshot) is stored — the merchant later cannot prove *who* consented to *what* and *when*.
- **Weaker legal-page wiring.** The only fallback is the legacy `checkout_terms_page` setting — no per-purpose policy management, no versioned content hashing, no data-request handling that the GDPR app adds.
- **Still subject to the cookie gate.** The `cookies_consent` targeting gate can still suppress the form at render, but without the module the merchant has less control over the cookie-group banner that drives it.

To capture defensible, auditable marketing consent from subscribe forms, the store should run the GDPR app, designate a `marketing_policy` page, and mark it required on the form. See [[apps-gdpr-overview]].

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-builder]] — where the `cookies_consent` flag and `terms` array are configured.
- [[subscribe-forms-submission-flow]] — how marketing consent + `PolicyAcceptanceLog` writes fit into the end-to-end submit pipeline.
- [[subscribe-forms-triggers]] — `popup-subscription-displayed_<form-id>` cookie is one of several display gates.
- [[apps-gdpr-overview]] — `marketing_policy` setting + the overall GDPR app surface.
- [[apps-gdpr-cookies]] — the `targeting` cookie group that gates `cookies_consent = false / null` forms.
- [[apps-gdpr-policy]] — legal terms pages attached to forms.

## Open questions

- Exact direction of the filter for the third `cookies_consent` state — `null` vs `false` semantics in the storefront controller. The semantic above ("null = unset = suppressed until consent, same as false") matches the original page documentation; should be re-verified against the controller source. (verify)
