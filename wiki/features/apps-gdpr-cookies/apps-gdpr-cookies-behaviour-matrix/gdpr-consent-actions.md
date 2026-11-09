---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix → Visitor actions"
route_name: ""
route_path: ""
aliases: ["Accept all vs Save preferences", "Accept vs Save settings", "Приемам vs Запази настройките", "Отхвърлям", "Reject cookies button", "cookie banner close button", "dismiss cookie banner", "js-cookies-accept", "js-cookies-accept-modal", "js-cookies-save-modal", "js-cookies-reject", "bottom-freezed-bar-close", "cookie cleanup on reject", "reopen cookie settings", "cookie consent 180 days"]
tags: [apps, gdpr, cookies, consent, storefront]
plan_gates: []
created: 2026-08-08
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-gdpr-cookies-behaviour-matrix]]. See the hub for the other aspects (configurations, banner persistence, theme limits).

# Cookie consent — what each visitor action does

## Purpose

The things a visitor can do with the cookie prompt, and precisely what each one writes and triggers. Verified against the storefront script as changed on 06.11.2026, when every answer started to dismiss the prompt and **Accept** in the dialog started to accept everything.

## Where to find it

On the storefront prompt itself — the bar at page bottom and the settings dialog. Labels and markup: [[apps-gdpr-cookies-bar-wall]].

## What the merchant can do here

Nothing directly; this is the visitor's side. It matters to the merchant because each action produces a different stored state, which is what support has to reason about.

## Settings & fields

| Action | Where | What it does |
|---|---|---|
| **Accept Cookies** / *Приемам* | Bar and dialog | Writes every active group as `yes`, whatever the switches show. |
| **Save settings** / *Запази настройките* | Dialog | Writes each group `yes` or `no` as its switch shows. |
| **Reject Cookies** / *Отхвърлям* | Bar | Writes every group `no`, except Strictly necessary (`system:yes`). |
| **×** | Bar | Hides the bar on the current page only. **Nothing is stored.** |
| Do nothing | — | Nothing stored; the fixed pre-answer states apply ([[apps-gdpr-cookies-consent-state]]). |
| Re-open the settings | A `#cookie-settings` link, `#cookies-trigger` | Opens the dialog, switches showing the stored answer. See [[apps-gdpr-cookies-bar-wall]]. |

After each of the three answers the storefront closes the dialog, hides the bar, deletes from the browser the cookies listed under each refused group (on the store's host and its parent domains, `_ga_…` matching every GA4 stream cookie), and asks the store to delete the same on its side.

## Business rules

### Any answer dismisses the prompt

The bar or wall stops showing once the stored answer names every active group, whatever the values. A visitor who refused everything is not asked again on the next page. It shows again only when the answer expires (180 days), when the visitor clears cookies, or when the store switches on a group the answer does not name.

Until 06.11.2026 the prompt kept returning until every group was accepted, and the dialog's **Приемам** saved the switches, so pressing it with the switches off stored `no` for every optional group. Observations from before that date reflect that behaviour.

### Closing with × is neither consent nor rejection

The × hides the bar for the current page only. **Nothing is written**, so the bar returns on the next page load and the pre-answer states keep applying.

### Every answer cleans up the refused groups

Accepting everything leaves nothing to delete; any answer that refuses a group removes the cookies listed for it, in the browser and on the store's side. Only cookies the merchant listed under that group are removed ([[apps-gdpr-cookies-definitions]]).

### A stored answer lasts 180 days

Every answer — accept, partial save or reject — is written for **180 days** at the site root, `SameSite=Lax`. Format and what asks again: [[apps-gdpr-cookies-consent-state]].

### Google Consent Mode is answered like any other group

`consent_mode_for_traffic` is a normal switch in the dialog. Until the visitor accepts it, Consent Mode signals stay denied. See [[apps-gdpr-cookies-consent-mode]].

## Related

- [[apps-gdpr-cookies-behaviour-matrix]] — hub.
- [[apps-gdpr-cookies-consent-state]] — what the stored consent looks like, its lifetime, and the cleanup endpoint.
- [[apps-gdpr-cookies-bar-wall]] — the buttons' markup expectations and the re-open hooks.
- [[apps-gdpr-cookies-consent-mode]] — the Consent Mode category.
- [[apps-gdpr-overview-script-gating]] — what a rejected category actually blocks.

## Open questions

None.
