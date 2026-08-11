---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix → Visitor actions"
route_name: ""
route_path: ""
aliases: ["Accept all vs Save preferences", "cookie banner close button", "dismiss cookie banner", "js-cookies-accept", "js-cookies-accept-modal", "bottom-freezed-bar-close", "cookie cleanup on reject", "reopen cookie settings", "cookie consent 365 days"]
tags: [apps, gdpr, cookies, consent, storefront]
plan_gates: []
created: 2026-08-08
updated: 2026-08-08
source_count: 3
---

> Part of [[apps-gdpr-cookies-behaviour-matrix]]. See the hub for the other aspects (configurations, banner persistence, theme limits).

# Cookie consent — what each visitor action does

## Purpose

The five things a visitor can do with the cookie prompt, and precisely what each one writes and triggers. Two of them surprise people: closing with **×** stores nothing at all, and **Accept all** does not run the cookie cleanup that **Save preferences** does.

## Where to find it

On the storefront prompt itself — the bar at page bottom and the consent dialog it opens.

## What the merchant can do here

Nothing directly; this is the visitor's side. It matters to the merchant because each action produces a different stored state, which is what support has to reason about.

## Settings & fields

| Action | Control | What it does |
|---|---|---|
| **Accept all** | `.js-cookies-accept` | Writes every category as `yes`, hides the bar, closes the dialog. Does **not** call the cleanup endpoint. |
| **Save preferences** | `.js-cookies-accept-modal` | Writes each category as `yes`/`no` per its toggle, hides the bar, closes the dialog, **and** calls the cleanup endpoint (`/gdpr/cookie-consent`). |
| **Close the bar (×)** | `.bottom-freezed-bar-close` | **Hides the bar on the current page only. Nothing is stored.** |
| **Do nothing** | — | Nothing stored. Each group's `default` acts as the assumed state. |
| **Re-open the prompt** | `#gdpr-trigger` / `#cookies-trigger` | Re-opens the dialog so the visitor can change their mind. The element must be placed by the theme — see [[gdpr-consent-theme-limits]]. |

On every page load the bar is hidden only when a stored consent is considered present; with the **wall**, the dialog auto-opens when it is not.

## Business rules

### Closing with × is neither consent nor rejection

The × hides the bar for the current page only. **Nothing is written**, so the bar returns on the next page load and every group stays on its `default` assumed state. Merchants often read this as *"I dismissed it and it came back"* — the prompt is behaving correctly; the visitor simply never answered it.

### Accept all and Save preferences are NOT symmetric

Both store a consent, but only **Save preferences** triggers the endpoint that deletes cookies belonging to rejected categories (see [[apps-gdpr-cookies-consent-state]]). **Accept all** does not call it — harmless in itself, because accepting everything leaves nothing to remove.

The practical consequence: **rejected cookies are actively cleaned up only along the reject path.** A visitor who rejects a category gets that category's existing cookies deleted; a visitor who accepts everything needs no cleanup.

### Saving does not necessarily dismiss the prompt

A **partial** save stores the choice correctly, yet the bar keeps showing until every category is accepted. That rule — and how to tell it apart from a genuine failure — is on [[gdpr-consent-persistence]].

### A stored consent lasts 365 days

The consent is written with a **365-day** lifetime at the site root. It survives page loads and sessions, and disappears when it expires or when the visitor clears their browser cookies — at which point the prompt starts over. Format and re-consent triggers: [[apps-gdpr-cookies-consent-state]].

### Google Consent Mode is answered like any other category

`consent_mode_for_traffic` is offered as a normal toggle, with one difference: it is the only standard category whose `default` ships as **rejected**. Until the visitor explicitly accepts it, Consent Mode signals stay denied — and because it is an offered category, leaving it unaccepted also keeps the bar showing under the partial-consent rule. See [[apps-gdpr-cookies-consent-mode]].

## Related

- [[apps-gdpr-cookies-behaviour-matrix]] — hub.
- [[apps-gdpr-cookies-consent-state]] — what the stored consent looks like, its lifetime, and the cleanup endpoint.
- [[apps-gdpr-cookies-bar-wall]] — the buttons' markup expectations and the re-open hooks.
- [[apps-gdpr-cookies-consent-mode]] — the Consent Mode category.
- [[apps-gdpr-overview-script-gating]] — what a rejected category actually blocks.

## Open questions

None — the one unresolved case (rejecting *every* optional category) is recorded on [[gdpr-consent-theme-limits]].
