---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix → Banner persistence"
route_name: ""
route_path: ""
aliases: ["banner keeps coming back", "banner returns after reload", "банерът се връща", "лентата не изчезва", "partial consent banner stays", "cookie bar does not disappear", "toggle shows off after save", "cookie consent not saving", "consent lost after reload", "банерът за бисквитки се показва отново"]
tags: [apps, gdpr, cookies, consent, troubleshooting, support]
plan_gates: []
created: 2026-08-08
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-gdpr-cookies-behaviour-matrix]]. See the hub for the other aspects (configurations, visitor actions, theme limits).

# Cookie consent — why the banner keeps coming back

## Purpose

How to diagnose *"the cookie banner keeps coming back"*. Since 06.11.2026 **any** answer — accept, save settings or reject — dismisses the bar or wall, so a prompt that returns after an answer has a specific cause, listed below.

## Where to find it

On the storefront, after a visitor has answered the prompt.

## What the merchant can do here

Tell the expected cases apart from a genuine fault — the checks below take under a minute.

## Settings & fields

No settings. The behaviour follows from the configuration on [[gdpr-consent-configurations]] and the action the visitor took ([[gdpr-consent-actions]]).

## Business rules

### The outcome table

| Visitor action | Answer stored? | Bar / wall on the next page |
|---|---|---|
| Accept Cookies | yes, every group accepted | gone |
| Save settings, any switches | yes, as the switches show | gone |
| Reject Cookies | yes, optional groups refused | gone |
| × on the bar | no | shows again |
| Nothing | no | keeps showing |

Before 06.11.2026 the bar kept showing until every group was accepted. A complaint or an internal note from before that date may describe that old rule.

### Why it can still come back

- **× instead of a button** — nothing was stored ([[gdpr-consent-actions]]).
- **The store switched on a group after the answer** (for example the Google Consent Mode group). The stored answer does not name it, so every visitor is asked again.
- **The answer expired** — 180 days — or the visitor cleared cookies, browses privately, or blocks cookies.
- **Another host name.** The answer is kept for the host it was given on, so `www.` and the bare domain, or a second domain of the store, each ask separately.

### Verifying an answer was saved

Re-open the settings (a `#cookie-settings` link, see [[apps-gdpr-cookies-bar-wall]]). The switches show the stored answer. Only if they come back wrong after an explicit save, inspect the stored value ([[apps-gdpr-cookies-consent-state]]).

### A switch that starts off is usually a merchant setting

Before any answer, each switch starts at its group's **Default state** ([[apps-gdpr-cookies-groups]]). A store whose optional groups are off by default shows them off on the first open: a configured opt-in posture, not a lost value. That setting does not change what the tracking apps do before an answer ([[apps-gdpr-overview-script-gating]]).

## Support playbook — "the cookie banner keeps coming back"

1. **Did the visitor press a button, or the ×?** The × stores nothing.
2. **Did the store switch on a group recently?** Everyone is asked once more.
3. **Same host name?** `www.` and the bare domain ask separately.
4. **Re-open the settings: do the switches show the visitor's choice?** If yes, the answer is stored; look at the browser (private mode, cookie blocking, cleared cookies).
5. Only if the switches come back wrong **after an explicit save** is this a candidate defect. Report the browser, the host name, the store's bar or wall set-up and the exact steps.

## Related

- [[apps-gdpr-cookies-behaviour-matrix]] — hub.
- [[apps-gdpr-cookies-consent-state]] — the stored consent's name, format and lifetime.
- [[apps-gdpr-cookies-groups]] — the per-group **Default state** that sets the opening switch position.
- [[apps-gdpr-cookies-bar-wall]] — the bar / wall presentation the visitor is looking at.

## Open questions

None — the unresolved cases are collected on [[gdpr-consent-theme-limits]].
