---
type: feature
nav_path: "Apps → GDPR → Cookies → Google Consent Mode"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["Google Consent Mode", "Google Consent Mode v2", "consent_mode_for_traffic", "Consent Mode subscription gating", "gdpr:activate-gc"]
tags: [apps, gdpr, compliance, cookies, consent, google, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# GDPR — Cookies: Google Consent Mode v2

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (bar & wall, groups, definitions, consent state).

## Purpose

This aspect documents CloudCart's **first-class support for Google Consent Mode v2** — the dedicated `consent_mode_for_traffic` cookie group that, when activated, emits consent signals to Google's tags (Ads / Analytics / Floodlight). It covers what the group does, why it defaults to off, and the subscription gating that restricts activation to recurring plans. The group sits alongside the standard taxonomy on [[apps-gdpr-cookies-groups]]; the script-firing consequences of a consent signal are on [[apps-gdpr-overview-script-gating]].

## Where to find it

Sidebar → Apps → GDPR → **Cookies tab** (`/admin/apps/gdpr/cookies`). The **Google Consent Mode** group (`consent_mode_for_traffic`) appears among the cookie groups. It is only exposed when the GDPR app is active AND the group is activated. Help URLs (EN / BG / EL / RO) for setting up Consent Mode are surfaced in the settings UI.

## What the merchant can do here

- Activate the `consent_mode_for_traffic` group to enable Google Consent Mode v2 signalling.
- Edit its customer-facing label and description like any other group.
- Acknowledge the implications when activating (a confirmation flow gates the toggle).

## Settings & fields

### The `consent_mode_for_traffic` group

| Property | Value |
|---|---|
| Group key | `consent_mode_for_traffic` |
| Default state | **no** — explicit opt-in required (unlike the other 4 groups, which default to yes) |
| Customer-facing label | Google Consent Mode |
| Purpose | Emits Consent Mode v2 signals to Google Ads / Analytics / Floodlight tags when the visitor accepts |

Because the default is `no`, until the visitor explicitly accepts, the consent state for this group is "no consent" — see [[apps-gdpr-cookies-consent-state]] for how that default is stored in the `cc-cookie-consent` cookie.

## Business rules

### Activation requires acknowledgement

When the merchant activates the group, the cookie-group validation applies a special check: the `field 'consent_mode_for_traffic.active'` validation surfaces a confirmation flow requiring the merchant to acknowledge the implications before the group goes live.

### Activation is gated by subscription type (402 for one-time purchases)

When the merchant tries to activate `consent_mode_for_traffic`, the platform checks the GDPR app subscription. **One-time purchase (legacy `billing_period == 'once'`) subscriptions get a `402 Payment Required` response** prompting the merchant to upgrade to a recurring plan — Consent Mode is available only on recurring-subscription plans. There is also a CLI command `gdpr:activate-gc` that bulk-activates Consent Mode for all sites whose subscription qualifies.

### Storefront signalling

When the group is activated and the visitor accepts, the storefront JS emits the consent signals to Google's tags. The downstream effect on whether tracking scripts fire is documented on [[apps-gdpr-overview-script-gating]].

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-groups]] — the standard cookie groups taxonomy this group belongs to.
- [[apps-gdpr-cookies-consent-state]] — how the default-off state is stored in the consent cookie (referenced inline above).
- [[apps-gdpr-overview-script-gating]] — how a consent signal gates Google's tracking scripts (referenced inline above).
- [[apps-google-analytics]] / [[apps-google-tags]] / [[apps-google-dynamic]] — Google integrations that respond to Consent Mode signals.

## Open questions

None.
