---
type: feature
nav_path: "Apps → GDPR → Cookies → Bar & wall"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["Cookie bar", "Cookie wall", "Information Bar", "Cookies consent dialog", "gdpr_popup", "cookies-trigger", "#cookie-settings", "Cookie Consent Mode dropdown", "Cookie policy page", "Настройки на бисквитките", "Запази настройките", "Приемам", "Отхвърлям"]
tags: [apps, gdpr, compliance, cookies, consent, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 7
---
# GDPR — Cookies: bar & wall presentation

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (groups, definitions, consent mode, consent state).

## Purpose

The **storefront presentation** of cookie consent: the dismissible **bar** or the blocking **wall**, the settings dialog, their texts and buttons, and how a visitor re-opens the settings. The group taxonomy is on [[apps-gdpr-cookies-groups]]; the stored answer is on [[apps-gdpr-cookies-consent-state]]; what each answer stores is on [[gdpr-consent-actions]].

## Where to find it

Sidebar → Apps → GDPR → **Cookies** tab (`/admin/apps/gdpr/cookies`). The presentation settings sit in two boxes: **Information bar for your cookie policy** and **Cookies consent description**. These are the admin's English labels; its Bulgarian labels are kept in the admin's translations, not in the code.

## What the merchant can do here

- Choose **Cookie bar** or **Cookie wall** in the **Cookie Consent Mode** dropdown, inside the **Information bar for your cookie policy** box.
- Pick the **Cookie policy page**, which the dialog links to.
- Write the **Information bar text** (the field shows only when the bar is chosen) and the **Cookies consent description** (the dialog's first tab).

### Bar vs wall

The dropdown has two options and no "none": choosing one clears the other.

- **Cookie bar** — a strip at the bottom; the page stays usable.
- **Cookie wall** — the settings dialog opens at once, without a close button, and stays until the visitor answers. It is not forced on the cookie policy page itself.

Either one shows until the visitor gives **any** answer, then never again until that answer expires (180 days) or the store switches on a group the answer does not cover.

## Settings & fields

| Field | Key | Notes |
|---|---|---|
| **Cookie Consent Mode** | `show_cookies_bar` / `show_cookies_wall` | One of the two is 1. The box's summary shows them as **Show information bar** and **Cookie wall**. |
| **Cookie policy page** | `cookie_policy_page` | A store page. When empty, the page with the address `cookie-policy` is used. |
| **Information bar text** | `cookies_bar_text` | Rich text, per store language. |
| **Cookies consent description** | `cookies_consent_text` | Rich text; the dialog's **Your Privacy** tab. |

### What the visitor sees

The bar, the dialog and their buttons are built by the platform's storefront script; the theme only styles them. Labels come from the store's language (themes may show them in capitals):

| Element | English | Bulgarian |
|---|---|---|
| Bar link that opens the dialog | Cookie Settings | Настройки на бисквитките |
| Bar button | Reject Cookies | Отхвърлям |
| Bar and dialog button | Accept Cookies | Приемам |
| Dialog button | Save settings | Запази настройките |
| Dialog title | Cookie Preference Center | Настройки на бисквитките |
| Dialog's first tab | Your Privacy | Вашите права |
| Link to the cookie policy page | More info | Допълнителна информация |

The dialog has one tab per active cookie group, with its switch (Strictly necessary is always on and locked) and the names of its cookie entries. Before the visitor answers, each switch starts at the group's **Default state**; afterwards it shows the stored answer.

## Business rules

### What the buttons do (since 06.11.2026)

- **Accept Cookies** — on the bar or in the dialog — accepts every group, whatever the switches show.
- **Save settings** stores what the switches show.
- **Reject Cookies** refuses every group except Strictly necessary.
- The bar's **×** hides the bar on the current page and stores nothing.

Each of the three answers dismisses the bar or wall. Until 06.11.2026 the dialog's **Приемам** saved the switches and the bar kept returning until every group was accepted; reports from before that date describe the old behaviour. Details: [[gdpr-consent-actions]].

### Re-opening the settings

After an answer, the dialog stays on every page, closed. It opens from any link whose address ends in `#cookie-settings` (the merchant can add such an item to a menu, see [[design-navigation]]), from an element with the id `cookies-trigger`, from the **Cookie Settings** link while the bar shows, and from the link the `{cookies_table}` placeholder prints on the cookie policy page ([[apps-gdpr-cookies-definitions]]).

### Not on the checkout

The bar, the wall and the dialog are not shown on the checkout pages; there the app shows only the policy re-acceptance popup ([[apps-gdpr-overview-consent-logging]]).

### Side effects on save

Saving rebuilds the storefront's apps file: signed-in visitors get the new set-up on the next page load, guests within up to 20 minutes (cached page copy, [[storefront-arch-caching-invalidation]]). Stored answers stay until they expire: changing a text asks nobody again, while switching on a group that was off asks every visitor again.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-consent-state]] — the `cc-cookie-consent` cookie, the cleanup of declined groups' cookies, and what asks a visitor again.
- [[gdpr-consent-actions]] — what each answer stores.
- [[apps-gdpr-overview]] — GDPR app overview, including the no-geo-gating rule (the bar shows to every visitor).

## Open questions

None.
