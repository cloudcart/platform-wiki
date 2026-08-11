---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix → Banner persistence"
route_name: ""
route_path: ""
aliases: ["banner keeps coming back", "banner returns after reload", "банерът се връща", "лентата не изчезва", "partial consent banner stays", "cookie bar does not disappear", "toggle shows off after save", "cookie consent not saving", "consent lost after reload"]
tags: [apps, gdpr, cookies, consent, troubleshooting, support]
plan_gates: []
created: 2026-08-08
updated: 2026-08-08
source_count: 3
---

> Part of [[apps-gdpr-cookies-behaviour-matrix]]. See the hub for the other aspects (configurations, visitor actions, theme limits).

# Cookie consent — why the banner keeps coming back

## Purpose

The single most misreported cookie-consent behaviour, and how to diagnose it. **A partial consent saves correctly but does not dismiss the prompt** — which looks identical to "my consent isn't saving" unless you know what to check.

## Where to find it

On the storefront, after a visitor uses **Save preferences** with only some categories enabled.

## What the merchant can do here

Decide whether what they are seeing is the designed reminder behaviour or a genuine fault — the checks below separate the two in under a minute.

## Settings & fields

No settings. The behaviour follows from the configuration on [[gdpr-consent-configurations]] and the action the visitor took ([[gdpr-consent-actions]]).

## Business rules

### 🔴 The bar keeps showing until the visitor accepts EVERYTHING — by design

If a visitor enables only some categories and presses **Save preferences**, the choice **is stored and honoured** — but the bar reappears on the next page load, and keeps reappearing until every offered category is accepted.

This is intentional: the bar doubles as a **standing reminder that categories remain unaccepted**. It is *not* evidence that the consent failed to save.

### The outcome table

| Visitor choice | Consent stored? | Choice honoured on re-open? | Bar on next load |
|---|---|---|---|
| Accept all | yes | yes | **gone** |
| Save preferences, **some** categories on | **yes** | **yes — the toggles show what was chosen** | **still shows** ← by design |
| Save preferences, **all optional off** | **may not be stored at all** — see [[gdpr-consent-theme-limits]] | — | still shows |
| Close with × | **no** | — | shows again on the next page |
| Nothing | no | — | keeps showing |

So *"the banner came back"* proves nothing on its own. The question is **"were all categories accepted?"** — if not, the bar is supposed to return.

### Verifying a partial consent really saved

Two checks, in this order:

1. **Re-open the prompt** (the cookie-settings link). The toggles should show exactly what the visitor chose. If they do, the consent is stored and working — and the complaint is really the by-design rule above.
2. Only if the toggles come back wrong, inspect the stored consent value — see [[apps-gdpr-cookies-consent-state]] for its name and format.

A bar that returns **while the toggles still show the visitor's choice** is correct, documented behaviour.

### A toggle that starts off is usually a merchant setting, not a lost value

On a visitor's **first** open, each toggle starts at its group's `default` ([[apps-gdpr-cookies-groups]]). A store whose optional groups are set to *disabled by default* shows them **off** on first open — that is the configured opt-in posture, not a discarded selection.

Distinguish the two cases before escalating:

- **Off on the FIRST open, before any choice** → the group's `default` is off. Expected.
- **Off on a LATER open, after the visitor turned it on and saved** → potentially a real defect — but check [[gdpr-consent-theme-limits]] first, because the dialog's toggle state is rendered by the theme, not the platform.

## Support playbook — "the cookie banner keeps coming back"

Work through these in order; the first three cover almost every report:

1. **Were all categories accepted?** If not, the bar is *supposed* to return. Stop here and explain it.
2. **Was × used instead of a button?** Then nothing was stored — the bar returns by design ([[gdpr-consent-actions]]).
3. **Re-open the prompt: do the toggles show the visitor's choice?** If yes, the consent is saving correctly and the complaint is really rule 1.
4. **Is it the visitor's FIRST open?** Then the toggles show each group's `default` — configuration, not lost data.
5. Only if the toggles come back wrong **after an explicit save** is this a candidate defect. Before escalating, compare a second theme ([[gdpr-consent-theme-limits]]) and report the exact category, the browser, and whether the store uses the bar or the wall.

## Related

- [[apps-gdpr-cookies-behaviour-matrix]] — hub.
- [[apps-gdpr-cookies-consent-state]] — the stored consent's name, format and lifetime.
- [[apps-gdpr-cookies-groups]] — the per-group `default` that sets the opening toggle position.
- [[apps-gdpr-cookies-bar-wall]] — the bar / wall presentation the visitor is looking at.

## Open questions

None — the unresolved cases are collected on [[gdpr-consent-theme-limits]].
