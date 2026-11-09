---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix → Theme dependencies & limits"
route_name: ""
route_path: ""
aliases: ["cookie dialog theme", "gdpr_popup theme", "cookie settings link missing", "#cookie-settings menu link", "gdpr-trigger cookies-trigger", "toggle state theme dependent", "reject all optional cookies"]
tags: [apps, gdpr, cookies, consent, storefront, theme, known-issues]
plan_gates: []
created: 2026-08-08
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-gdpr-cookies-behaviour-matrix]]. See the hub for the other aspects (configurations, visitor actions, banner persistence).

# Cookie consent — what belongs to the theme

## Purpose

Which parts of the cookie prompt the store's theme affects, and which it does not. Useful before treating a difference between two stores as a platform fault.

## Where to find it

The bar, the wall and the settings dialog on the storefront.

## What the merchant can do here

Recognise a theme difference, and give visitors a way back into the settings.

## Settings & fields

No settings — theme markup is not exposed as configuration in the admin.

## Business rules

### The platform builds the prompt; the theme only styles it

The bar, the dialog, their buttons and switches are built by the platform's storefront script on every theme: the same markup, texts, switch states and stored answer. Classic themes style them through shared styles; Liquid themes show them in an isolated layer with the platform's own look. So the button behaviour, the stored value and the switch positions do not differ by theme. A difference in looks, such as capitals or colours, is the theme's.

### The re-open link is the merchant's to place

After an answer the dialog stays on the page, closed. Visitors reach it through a link whose address ends in `#cookie-settings`, an element with the id `cookies-trigger`, or the cookie table on the cookie policy page ([[apps-gdpr-cookies-bar-wall]]). Themes do not place such a link by themselves. The merchant adds one, typically a footer menu item with the address `#cookie-settings` ([[design-navigation]]); without it, a visitor can change the answer only on the cookie policy page.

### Rejecting every optional group IS recorded

**Reject Cookies**, or **Save settings** with every switch off, writes every group, each optional one as `no`. The answer dismisses the prompt and is honoured.

### Verified against the storefront script

The button behaviour, the dismissal rule, the 180-day lifetime and the cleanup are read from the platform's storefront script as changed on 06.11.2026, not observed in a store.

## Related

- [[apps-gdpr-cookies-behaviour-matrix]] — hub.
- [[gdpr-consent-persistence]] — the diagnosis flow that ends here when a defect is genuinely suspected.
- [[apps-gdpr-cookies-bar-wall]] — the theme expectations for the dialog and the re-open hooks.
- [[apps-gdpr-cookies-consent-state]] — the stored consent format, for inspecting what a store actually recorded.

## Open questions

None.
