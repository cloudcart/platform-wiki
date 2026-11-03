---
type: feature
nav_path: "Apps → GDPR → Cookie consent UX"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["GDPR cookie bar", "GDPR cookie wall", "Cookie consent UX", "cc-cookie-consent", "Cookie groups taxonomy", "Manage preferences trigger"]
tags: [apps, gdpr, compliance, privacy, cookies, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# GDPR — Cookie consent UX (storefront)

> Part of [[apps-gdpr-overview]]. See the hub for the other aspects (script gating, data requests, consent logging) and the GDPR tab pages.

## Purpose

This aspect documents the **storefront cookie consent experience** the GDPR app renders for visitors: the cookie bar vs cookie wall, the standard cookie groups taxonomy, the consent cookie that stores the visitor's choice, when the consent prompt re-appears, the "manage preferences" trigger, and two important non-features (no geo-gating, no automatic cookie discovery). The admin side of editing groups + cookie definitions lives on [[apps-gdpr-cookies]]; the script-firing consequences of a consent choice live on [[apps-gdpr-overview-script-gating]].

## Where to find it

The merchant configures this from the GDPR app's **Cookies** tab (`/admin/apps/gdpr/cookies`, route `apps.gdpr.cookies`). The result renders on every storefront page when the GDPR app is active. The bar vs wall choice is the `show_cookies_bar` / `show_cookies_wall` setting pair.

## What the merchant can do here

- Choose **Cookie bar** OR **Cookie wall** as the consent presentation mode.
- Edit bar / wall text and styling.
- Define the standard cookie groups and the individual cookie definitions inside each (vendor name, purpose, duration) — see [[apps-gdpr-cookies]].
- Rely on the built-in "manage preferences" trigger so customers can re-open consent at any time.

### Cookie bar vs cookie wall — mutually exclusive in the modern UI

The modern Vue settings UI presents the cookie consent UX as a single dropdown ("Cookie Consent Mode") with two choices: **Cookie bar** OR **Cookie wall** — selecting one sets the other to 0. Behind the scenes the legacy backend has both `show_cookies_bar` and `show_cookies_wall` settings that COULD both be enabled, but the merchant-facing UI doesn't allow that combination.

- **Cookie wall** (`show_cookies_wall` ON) — the storefront JS opens the consent modal automatically on page load IF the visitor has no `cc-cookie-consent` cookie yet. The modal effectively blocks interaction with the page underneath until the customer accepts or sets preferences.
- **Cookie bar** (`show_cookies_bar` instead) — the bar is dismissible and non-modal.

## Settings & fields

### Cookie groups taxonomy (verified)

Per the GDPR seed data, the standard groups are:

| Group key | Description |
|---|---|
| `system` | Strictly Necessary — session, cart, login. Always yes, cannot reject. |
| `performance` | Performance / Analytics — counts visits, traffic sources. |
| `functional` | Functional — videos, live chat. |
| `targeting` | Marketing / Advertising — advertising-partner cookies. |
| `consent_mode_for_traffic` | Google Consent Mode v2 integration (separate from `targeting`) — see [[apps-gdpr-overview-script-gating]]. |

The seed data ships translations for these groups in EN, BG, RO, EL, HU. The merchant adjusts the per-group definitions but the standard taxonomy is preserved.

### Consent state cookie name and structure

The consent cookie is named `cc-cookie-consent`. Its value is a space/plus-separated list of `group:yes|no` pairs (e.g., `system:yes+performance:yes+targeting:no+consent_mode_for_traffic:no`). When no cookie is set, all groups fall back to their seed defaults — `system`, `performance`, `functional`, `targeting` default to **yes**; `consent_mode_for_traffic` defaults to **no** (explicit opt-in required — see [[apps-gdpr-overview-script-gating]]).

### Consent choice expires after 365 days

The storefront JS sets the `cc-cookie-consent` cookie with `expires: 365` days. After one year (or when the customer clears their browser cookies), the bar reappears so the customer can re-consent. **This is the only built-in re-consent trigger** — there is no automatic re-prompt when the cookie LIST changes (the merchant adding a new cookie does not force existing visitors to re-consent).

### "Manage preferences" trigger — `#gdpr-trigger` / `#cookies-trigger` hooks

The storefront ships JavaScript click handlers bound to elements with id `gdpr-trigger` or `cookies-trigger`. When the merchant's theme renders a button/link with one of those ids, clicking it opens the cookie consent modal (`#gdpr_popup`). The theme is responsible for placing the trigger — no admin setting controls its visibility.

## Business rules

### Cookie bar shows to ALL visitors — no geo-gating

When GDPR is active, the cookie bar/wall renders for every visitor regardless of country. There is NO geographic IP detection in the GDPR module — no EU/non-EU check, no country-based gating. The merchant cannot configure "show only to EU visitors" through the app. If the merchant wants the bar hidden for non-EU visitors, they would need to deactivate the GDPR app entirely (not recommended — would also break Google Consent Mode, policy popups, and audit logging).

### No automatic cookie discovery — definitions are merchant-managed

Cookie definitions are entered manually by the merchant via the per-group "add cookie" modal. The platform does NOT scan the storefront for third-party-set cookies and auto-classify them. When the merchant adds a tracking integration (Google Analytics, Facebook Pixel, etc.), they must also add the cookie definitions to the appropriate group themselves.

## Related

- [[apps-gdpr-overview]] — hub.
- [[apps-gdpr-cookies]] — admin Cookies tab where groups + cookie definitions are edited.
- [[apps-gdpr-overview-script-gating]] — how a consent choice gates tracking scripts (referenced inline above).

## Open questions

None.
