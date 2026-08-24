---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix → Theme dependencies & limits"
route_name: ""
route_path: ""
aliases: ["cookie dialog theme", "gdpr_popup theme", "cookie settings link missing", "gdpr-trigger cookies-trigger", "toggle state theme dependent", "reject all optional cookies", "cookie consent unverified behaviour"]
tags: [apps, gdpr, cookies, consent, storefront, theme, known-issues]
plan_gates: []
created: 2026-08-08
updated: 2026-08-08
source_count: 3
---

> Part of [[apps-gdpr-cookies-behaviour-matrix]]. See the hub for the other aspects (configurations, visitor actions, banner persistence).

# Cookie consent — what belongs to the theme, and what is unverified

## Purpose

Two things support needs before escalating a cookie-consent report: **which parts of the prompt the platform does not control** (they come from the storefront theme, so they can differ between stores), and **which documented behaviours come from observation rather than platform source**.

## Where to find it

The affected surfaces are the consent dialog and the "cookie settings" re-open link on the storefront — both rendered by the active theme.

## What the merchant can do here

Recognise when a difference between two stores is a **theme** difference rather than a platform fault, and know which claims are safe to rely on.

## Settings & fields

No settings — theme markup is not exposed as configuration in the admin.

## Business rules

### 🔴 The consent dialog is supplied by the THEME

The platform ships the **logic** — which button writes what, what gets stored, what gets cleaned up — but **not the dialog markup**. The consent dialog, its per-category toggles, and **the state each toggle is rendered in when the dialog opens** come from the storefront theme.

Two consequences that matter in support:

- **The re-open toggle state is theme-rendered.** Whether a re-opened dialog shows the visitor's previously saved choices depends on the theme, not the platform. If one store shows the toggles wrong after a save while another store behaves correctly, **compare the themes first** — it is not automatically a platform defect. This is a plausible explanation when a merchant report and an internal test disagree: both can be truthful on different themes.
- **The re-open link is theme-supplied too.** The platform only listens for a `#gdpr-trigger` / `#cookies-trigger` element. If the theme places none, the visitor has **no way to re-open the dialog at all** — there is no stock merchant-configurable "Cookie settings" button. See [[apps-gdpr-cookies-bar-wall]].

Only the **wall** is auto-opened by the platform, and only when no consent is stored.

### Rejecting every optional category IS recorded

**Save preferences** writes one entry per category shown in the dialog — each as `yes` or `no` according to its switch — with no special case for "everything off". A visitor who rejects every optional category therefore gets that recorded exactly like any other combination, and the rejections are honoured.

There is only one way a save genuinely stores nothing: if the dialog renders **no category switches at all**. That happens when no group has any cookies defined, since an empty group is not rendered ([[gdpr-consent-configurations]]). With nothing to iterate, the save writes an empty value. Check the group definitions ([[apps-gdpr-cookies-definitions]]) before treating this as a fault.

The bar still returns after an all-off save — not because nothing was stored, but because of the partial-consent rule on [[gdpr-consent-persistence]].

### Two behaviours are documented from observation, not source

These live outside the application code, so they are stated from observed behaviour and should not be quoted as verified platform rules:

| Behaviour | Why it is unverified |
|---|---|
| What counts as a **"complete" consent** (and therefore hides the bar) | Decided by a storefront script asset that is not part of the application code. Observed: full acceptance dismisses the bar, partial acceptance does not. |
| The dialog's **toggle state on re-open** | Rendered by the theme, so there is no single platform-wide behaviour to assert. |

Everything else in this sub-cluster — the settings, the button behaviours, the cleanup asymmetry, the 365-day lifetime, the bar/wall combinations, the empty-group rule — is verified against the platform's own storefront script, settings form and templates.

## Related

- [[apps-gdpr-cookies-behaviour-matrix]] — hub.
- [[gdpr-consent-persistence]] — the diagnosis flow that ends here when a defect is genuinely suspected.
- [[apps-gdpr-cookies-bar-wall]] — the theme expectations for the dialog and the re-open hooks.
- [[apps-gdpr-cookies-consent-state]] — the stored consent format, for inspecting what a store actually recorded.

## Open questions

None.
