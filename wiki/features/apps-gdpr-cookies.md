---
type: feature
nav_path: "Apps → GDPR → Cookies"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["GDPR Cookies", "Cookie consent", "Cookie bar", "Cookie wall", "Cookie groups", "Cookie management"]
tags: [apps, gdpr, compliance, cookies, consent, privacy]
plan_gates: []
created: 2026-05-21
updated: 2026-08-08
source_count: 10
---
# GDPR → Cookies

## Purpose

The **Cookies** tab is where the merchant configures the **cookie-consent experience** on the storefront — the bar / wall a visitor sees on first visit, the text shown, the cookie groups offered, and the individual cookies listed within each group. Configuration here determines whether the prompt appears at all, what the customer reads, which categories are offered, which default ON vs OFF, and (critically) which tracking scripts are allowed to load once the customer makes a choice.

This page is the **hub** for the cookie-consent cluster. It is intentionally slim — definition + a catalogue of the aspect pages below. Drill into the aspect that matches the question rather than reading every page. For overall GDPR coverage (data requests, policy popups, consent logging), see [[apps-gdpr-overview]].

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages, each covering one well-scoped slice:

- [[apps-gdpr-cookies-bar-wall]] — the storefront presentation: cookie **bar** vs **wall** (mutually-exclusive dropdown), bar text, consent dialog text, the `#gdpr_popup` modal and the `#gdpr-trigger` / `#cookies-trigger` re-open hooks.
- [[apps-gdpr-cookies-groups]] — the 5 standard cookie groups taxonomy (`system`, `performance`, `functional`, `targeting`, `consent_mode_for_traffic`), the per-group editor, the `default` pre-consent fallback flag, and why the `system` group can't be rejected.
- [[apps-gdpr-cookies-definitions]] — the per-cookie 3-field modal (name / description / technical cookie names), the auto-generated `mapping` slug + duplicate rejection, one-click delete, the `{cookies_table}` storefront placeholder, and the no-auto-scan rule.
- [[apps-gdpr-cookies-consent-mode]] — Google Consent Mode v2 via the `consent_mode_for_traffic` group: default-off opt-in, the subscription gating (one-time purchases get a 402), and the bulk-activate command.
- [[apps-gdpr-cookies-consent-state]] — the `cc-cookie-consent` browser cookie: its `group:yes|no` structure, the 365-day expiry, why it is NOT encrypted, the rejected-cookie cleanup endpoint, the 20-minute group cache, and why adding a cookie does NOT force re-consent.
- [[apps-gdpr-cookies-behaviour-matrix]] — **every configuration × every visitor action → what actually happens**: why the bar keeps showing after a *partial* consent (by design), what the × really does, why Accept-all and Save-preferences are not symmetric, the four bar/wall combinations, empty groups vanishing from the prompt, and the *"the banner keeps coming back"* support playbook.

## Where to find it

Sidebar → Apps → GDPR → **Cookies tab**. Route: `/admin/apps/gdpr/cookies` (`apps.gdpr.cookies`). The tab is available when the GDPR app is active. Editing here renders on every storefront page; some changes propagate to the storefront within a 20-minute cache window (see [[apps-gdpr-cookies-consent-state]]).

## What the merchant can do here

- Choose and style the consent presentation — bar vs wall, the bar text, the consent-dialog text. See [[apps-gdpr-cookies-bar-wall]].
- Configure each cookie group: active, default state, label, description. See [[apps-gdpr-cookies-groups]].
- Add / edit / delete individual cookie definitions inside each group. See [[apps-gdpr-cookies-definitions]].
- Activate Google Consent Mode v2 (subscription-gated). See [[apps-gdpr-cookies-consent-mode]].

What the merchant **cannot** do here: disable the Necessary / `system` group, set its default to rejected, bypass consent for Analytics / Marketing scripts, register a cookie without a group, or auto-discover cookies set by installed tracking apps.

## Settings & fields

The setting keys, group taxonomy, and modal fields are documented on the aspect pages — there is no field list unique to the hub. Entry points:

- Bar / wall: `show_cookies_bar`, `show_cookies_wall`, `cookies_bar_text`, `cookies_consent_text` — see [[apps-gdpr-cookies-bar-wall]].
- Per-group: `active`, `default`, `name`, `description` — see [[apps-gdpr-cookies-groups]].
- Per-cookie: `name`, `description`, `cookies` (technical names) — see [[apps-gdpr-cookies-definitions]].

## Business rules

The cluster-wide rule: **when a customer rejects a category, scripts in that category must not load, and existing rejected cookies are actively cleaned up.** The mechanics live on the aspect pages — script gating on [[apps-gdpr-overview-script-gating]], cookie cleanup + caching on [[apps-gdpr-cookies-consent-state]]. Two important non-features apply across the whole cluster: there is **no geographic gating** (the bar shows to every visitor when GDPR is active — see [[apps-gdpr-overview]]) and **no automatic cookie scanning** (definitions are merchant-managed — see [[apps-gdpr-cookies-definitions]]).

## Related

- [[apps-gdpr-overview]] — GDPR hub.
- [[apps-gdpr-acceptance]] — consent acceptance log.
- [[apps-gdpr-settings]] — GDPR app settings.
- [[apps-gdpr-overview-script-gating]] — how a consent choice gates tracking scripts.
- [[apps-google-analytics]] / [[apps-google-tags]] / [[apps-google-dynamic]] / [[apps-tiktok-pixel]] / [[apps-facebook-comments]] / [[apps-disqus-comments]] — tracking integrations gated by cookie consent.
- [[apps-datalayer]] — data layer may be conditionally populated based on consent.

## Open questions

None.
