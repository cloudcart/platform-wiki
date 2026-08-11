---
type: feature
nav_path: "Apps → GDPR → Consent capture & logging"
route_name: apps.gdpr.acceptance
route_path: /admin/apps/gdpr/acceptance
aliases: ["GDPR consent capture", "GDPR acceptance log", "policies_popup", "GDPR form types", "marketing_policy", "GDPR install seeder"]
tags: [apps, gdpr, compliance, privacy, consent, audit]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# GDPR — Consent capture & acceptance logging

> Part of [[apps-gdpr-overview]]. See the hub for the other aspects (consent UX, script gating, data requests) and the GDPR tab pages.

## Purpose

This aspect documents **where and how policy consent is captured into the acceptance log**: the five storefront form types that collect consent, the storefront routes the logging middleware attaches to, the append-only write timing, the `policies_popup` re-prompt mechanism for existing customers, the marketing-policy flag side-effect, and what the install seeder creates. The admin Acceptance tab (viewing + Export) is on [[apps-gdpr-acceptance]]; policy authoring is on [[apps-gdpr-policy]].

## Where to find it

The merchant views the resulting records on the GDPR app's **Acceptance** tab (`/admin/apps/gdpr/acceptance`, route `apps.gdpr.acceptance`). The consent itself is captured automatically across the storefront — there is no admin screen to configure capture points; they are wired by the GDPR app.

## What the merchant can do here

- View the per-customer acceptance log (WHO accepted WHICH policy version WHEN, with IP / device / timestamp).
- Designate one policy as the marketing policy so accepting it flips the customer's marketing flag.
- Rely on the `policies_popup` mechanism to re-prompt existing customers when a new policy is added.

## Settings & fields

### Form types — 5 storefront forms where GDPR consent is captured

| Form key | Description |
|---|---|
| `register` | User Registration form. |
| `contacts` | Contact Form. |
| `submit_payment` | Completing an order (checkout consent). |
| `segment_subscription_popup` | Subscribers — subscription forms (newsletter signup). |
| `policies_popup` | Request for consent for registered users after login (e.g., when a new policy is added, ask existing customers to accept). |

These are the 5 storefront touchpoints that capture consent into the acceptance log. (Commented-out form types `marketing` and `mailchimp_newsletter` are likely deprecated.)

### Middleware attaches to many storefront routes

The `gdpr_policy_acceptances` middleware is registered on: contacts form POST, checkout login POST, checkout register POST, checkout shipping address save, checkout billing address save, checkout payment submit, subscribers subscription form, and the `policies-popup` route. So acceptance can also be logged when a customer submits a shipping address or completes the contacts form — not just the obvious checkout / register / popup paths.

## Business rules

### Acceptance write happens AFTER the response is sent (terminate middleware)

The `gdpr_policy_acceptances` middleware writes acceptance log rows in its `terminate` method — meaning the response goes back to the customer BEFORE the database write. This keeps the storefront fast, but means a server crash between response-send and write-finish could miss a log row. The middleware checks `$response->getOriginalContent['status'] === 'success'` to avoid logging acceptances on failed submissions.

### `policies_popup` mechanism — existing customers re-prompted on new policies

When an existing customer logs in AND there's a new policy they haven't accepted yet, a popup asks them to accept (the `policies_popup` form type). On customer login, if the customer has NOT yet accepted any policy (no entry in the policy acceptance log for their customer ID), a `policies_popup` cookie is set for 30 days. The storefront reads this cookie and shows the consent popup until the customer accepts. **So yes — existing customers ARE re-prompted on new policy versions** via this mechanism.

### `policies_popup` skipped on the registration route

The `policiesPopupEnabled` check explicitly excludes the `site.auth.register` route — the popup will NOT appear on the registration page itself (where the customer is about to provide consent anyway). It surfaces only on OTHER pages after login for an existing customer who lacks acceptance.

### Customer marketing flag links to the designated marketing policy

When the merchant designates one policy as the `marketing_policy` setting, accepting/rejecting THAT policy on any form flips `customer.marketing` to `yes`/`no` and fires a `CustomerMarketingChange` event. Subscriber lists, email-newsletter integrations, and other marketing apps react to this event. The save retries up to 5 times with a 500ms backoff to handle concurrent writes.

### Acceptance log is append-only

GDPR audit requires retention of WHO accepted WHICH policy version WHEN. Entries are created or touched, never deleted — so the FACT of consent survives even after a customer's personal record is anonymised on a right-to-erasure request (see [[apps-gdpr-overview-data-requests]]). The log can only be exported, not edited; Export is 2FA-gated (see [[apps-gdpr-acceptance]] and [[account-cc2fa]]).

### Install flow runs a seeder (single install view, not a multi-step wizard)

When the merchant opens any GDPR sub-page on a store where the app is not yet installed, the platform short-circuits the response and shows a single install view (the platform code) with the country list — there is no multi-step wizard with progress steps. The merchant submits the install action, after which all sub-pages become accessible. The install action runs the seeder, which creates the 4 default policies + 5 default cookie groups + default cookie providers (CloudCart Platform, CloudCart Analytics, Google Analytics, AddThis, Facebook Ads, etc.). The cookie groups are documented on [[apps-gdpr-overview-consent-ux]].

## Related

- [[apps-gdpr-overview]] — hub.
- [[apps-gdpr-acceptance]] — admin Acceptance tab (view + 2FA-gated Export).
- [[apps-gdpr-policy]] — policy authoring; the marketing policy is designated here.
- [[apps-gdpr-overview-data-requests]] — append-only log retained after erasure anonymisation.
- [[apps-gdpr-overview-consent-ux]] — cookie groups the install seeder creates.
- [[account-cc2fa]] — 2FA gating the acceptance Export.

## Open questions

None.
