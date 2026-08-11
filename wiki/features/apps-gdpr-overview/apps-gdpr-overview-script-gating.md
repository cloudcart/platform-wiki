---
type: feature
nav_path: "Apps → GDPR → Script gating"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["GDPR script gating", "Google Consent Mode v2", "consent_mode_for_traffic", "GDPR tracking integration", "Consent-gated scripts"]
tags: [apps, gdpr, compliance, privacy, cookies, tracking, analytics]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# GDPR — Script gating (consent → tracking scripts)

> Part of [[apps-gdpr-overview]]. See the hub for the other aspects (consent UX, data requests, consent logging) and the GDPR tab pages.

## Purpose

This aspect documents **how a visitor's cookie consent choice controls whether tracking scripts fire** — including the built-in Google Consent Mode v2 integration. The consent UX itself (bar/wall, groups, the `cc-cookie-consent` cookie) is on [[apps-gdpr-overview-consent-ux]]; this page covers the consequence of that choice for analytics / advertising scripts.

## Where to find it

There is no dedicated admin screen for script gating — it is wired automatically when the GDPR app is active and the relevant cookie group is active. The merchant manages the gating indirectly via the **Cookies** tab (`/admin/apps/gdpr/cookies`, route `apps.gdpr.cookies`) by activating/deactivating the cookie groups (`performance`, `targeting`, `consent_mode_for_traffic`).

## What the merchant can do here

- Activate the `consent_mode_for_traffic` cookie group to enable the Google Consent Mode v2 integration.
- Activate/deactivate `performance` and `targeting` groups, which determine whether analytics and advertising scripts are eligible to fire.
- Connect the tracking apps below; their loading then respects the visitor's consent state.

## Settings & fields

### Google Consent Mode v2 — built-in support

The GDPR app interfaces with Google Consent Mode v2 via a dedicated cookie group named `consent_mode_for_traffic`. The cookie group consent defaults are:

| Group | Default consent state |
|---|---|
| `system` | yes (always on) |
| `performance` | yes |
| `functional` | yes |
| `targeting` | yes |
| `consent_mode_for_traffic` | **no** (defaults to no consent — explicit opt-in required) |

The `consent_mode_for_traffic` group is described in seed data as "Traffic Consent Mode is an intelligent mechanism that allows our website to adjust its tags based on your consent. Specifically, it works with tags such as Google Ads, Google Analytics, and Floodlight, directing their execution depending on whether you agree or not."

The Google Consent Mode integration activates ONLY when the GDPR app is active AND the `consent_mode_for_traffic` cookie group is active. When both conditions hold, the storefront JavaScript exposes the consent state to tracking scripts so they can read whether the visitor has consented before firing.

## Business rules

### Integration with tracking apps

When GDPR is active and a customer rejects a cookie category:
- [[apps-google-analytics]] / [[apps-google-tags]] / [[apps-google-dynamic]] — should NOT load when Analytics or Marketing consent is denied.
- [[apps-tiktok-pixel]] / [[apps-facebook-comments]] / [[apps-disqus-comments]] — should NOT load.
- The integration consent state propagates to the script loaders, which read the `cc-cookie-consent` group states (see [[apps-gdpr-overview-consent-ux]]) before firing.

(Verify the exact propagation mechanism per consent group.)

### Disabling the GDPR app disables gating

Because the gating is driven entirely by the GDPR app's active state + cookie-group state, deactivating the GDPR app removes the consent layer altogether — scripts would then fire unconditionally. This is one reason the consent bar cannot be selectively hidden for non-EU visitors (no geo-gating — see [[apps-gdpr-overview-consent-ux]]).

## Related

- [[apps-gdpr-overview]] — hub.
- [[apps-gdpr-overview-consent-ux]] — the consent groups + `cc-cookie-consent` cookie this gating reads.
- [[apps-google-analytics]] / [[apps-google-tags]] / [[apps-google-dynamic]] — tracking apps gated by consent.
- [[apps-tiktok-pixel]] / [[apps-facebook-comments]] / [[apps-disqus-comments]] — tracking apps gated by consent.

## Open questions

- Exact per-group propagation mechanism from `cc-cookie-consent` to each tracking-app loader (verify).
