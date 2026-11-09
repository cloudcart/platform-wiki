---
type: feature
nav_path: "Apps → GDPR → Script gating"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["GDPR script gating", "Google Consent Mode v2", "consent_mode_for_traffic", "GDPR tracking integration", "Consent-gated scripts"]
tags: [apps, gdpr, compliance, privacy, cookies, tracking, analytics]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
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
- Google tags, verified in the storefront code. Until the visitor answers, each group counts as its default in the table above:
  - [[apps-google-analytics]] waits for `performance`, [[apps-google-dynamic]] for `targeting`. When `consent_mode_for_traffic` is active, both wait for that group instead, so an unanswered banner sends nothing to Google (the GA4 purchase included) until the visitor accepts it. See [[apps-google-analytics-purchase-event]].
  - [[apps-google-tags]] loads its container once `performance` counts as accepted, whatever the Consent Mode group.
  - A group accepted later on the same page releases the waiting tags at that moment.
- Pixels, verified in the storefront code: [[apps-facebook-pixel]], [[apps-tiktok-pixel]] and the Glami, Retargeting, Profitshare and Skroutz scripts ([[apps-xml-feed-glami]], [[apps-xml-feed-retargeting]], [[apps-xml-feed-profitshare]], [[apps-xml-feed-skroutz]]) wait for `targeting`.
  - They ignore the Google Consent Mode group and send no consent signals of their own: Consent Mode is Google's only.
  - Before an answer `targeting` counts as accepted, so they load and fire on the first page.
  - After a refusal the vendor's script is not loaded. With the Conversions API (Meta) or Events API (TikTok) on, the browser still sends each event to the store's own address (`/pixel/v2/…`, `/tiktok/pixel/…`), but the store checks the same answer and forwards nothing to Meta or TikTok.
- [[apps-facebook-comments]] / [[apps-disqus-comments]] — should NOT load (verify).
- Every check reads the visitor's `cc-cookie-consent` answer ([[apps-gdpr-cookies-consent-state]]), in the browser and on the store's server alike.

### Before an answer: fixed states

Until the visitor answers, the states in the table above apply. They are fixed in the platform: a group's **Default state** on the Cookies tab only sets where its switch starts in the dialog and changes nothing here ([[apps-gdpr-cookies-groups]]).

### External cookie-consent tools and pasted code

- **No connection.** There is no setting or hook that feeds an outside consent tool (CookieYes, CookieFirst, CookieScript and the like) into this gating. The built-in apps read only the GDPR app's own answer.
- **With the GDPR app off,** the built-in apps load with no consent check at all, so an outside tool does not stop them. Running an outside tool alongside the GDPR app shows visitors two prompts that do not share answers.
- **Code pasted in [[design-custom-assets]]** is never gated: it runs on every page whatever the visitor answered, unless the code itself checks consent. It sits in the page head after the platform's consent helper and the Consent Mode default, and before the built-in tracking apps, which load asynchronously at the end of the page ([[design-custom-assets-injection]]).
- An outside tool's own effect on the built-in pixels or on Google's tags is that vendor's behaviour, outside CloudCart's code.

### Disabling the GDPR app disables gating

Because the gating is driven entirely by the GDPR app's active state + cookie-group state, deactivating the GDPR app removes the consent layer altogether — scripts would then fire unconditionally. This is one reason the consent bar cannot be selectively hidden for non-EU visitors (no geo-gating — see [[apps-gdpr-overview-consent-ux]]).

## Related

- [[apps-gdpr-overview]] — hub.
- [[apps-gdpr-overview-consent-ux]] — the consent groups + `cc-cookie-consent` cookie this gating reads.
- [[apps-google-analytics]] / [[apps-google-tags]] / [[apps-google-dynamic]] — tracking apps gated by consent.
- [[apps-facebook-pixel]] / [[apps-tiktok-pixel]] / [[apps-facebook-comments]] / [[apps-disqus-comments]] — apps gated by consent.
- [[design-custom-assets-injection]] — where pasted code runs.

## Open questions

- Whether the Facebook Comments and Disqus widgets check the answer (verify).
