---
type: feature
nav_path: "Apps → GDPR → Cookies → Bar & wall"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["Cookie bar", "Cookie wall", "Information Bar", "Cookies consent dialog", "gdpr_popup", "cookies-trigger", "Cookie Consent Mode dropdown"]
tags: [apps, gdpr, compliance, cookies, consent, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-08-08
source_count: 6
---
# GDPR — Cookies: bar & wall presentation

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (groups, definitions, consent mode, consent state).

## Purpose

This aspect documents the **storefront presentation** of cookie consent — the two ways the merchant can prompt the visitor (a dismissible **bar** at page-bottom vs a blocking **wall** modal), the text fields shown in each, and the JavaScript hooks the theme uses to render and re-open the consent UI. It is the "how the prompt looks and behaves" slice; the group taxonomy lives on [[apps-gdpr-cookies-groups]] and the consent cookie that records the choice lives on [[apps-gdpr-cookies-consent-state]].

## Where to find it

Sidebar → Apps → GDPR → **Cookies tab** (`/admin/apps/gdpr/cookies`). The presentation settings sit in two sections: **"Information Bar"** (`InformationCookieSection.vue`) and **"CookiesConsentDescription"** (`ConsentTextSection.vue`).

## What the merchant can do here

- Choose **Cookie bar** OR **Cookie wall** as the consent presentation mode.
- Write the **cookie bar text** (rich HTML) shown in the bottom strip.
- Write the **cookies consent text** shown in the detailed consent dialog (rich text editor).
- Rely on the built-in modal + trigger hooks so visitors can re-open consent (theme must place the trigger element).

### Bar vs wall — mutually exclusive in the modern UI

The modern Vue UI presents the choice as a **single dropdown** ("Cookie Consent Mode") with two options — **Cookie bar** or **Cookie wall**. Selecting one automatically sets the other to `0`. The legacy backend technically supports both `show_cookies_bar` and `show_cookies_wall` being ON simultaneously, but the merchant-facing UI prevents that combination.

- **Cookie wall** (`show_cookies_wall` ON) is the heavier UX: the storefront JS (`stript.tpl`) auto-opens the `#gdpr_popup` modal on window load **if** the visitor has no `cc-cookie-consent` cookie yet. The modal effectively blocks interaction with the page underneath until the customer accepts or sets preferences. Use only when local law explicitly requires it.
- **Cookie bar** (`show_cookies_bar` ON) is a thin, dismissible, non-modal strip at page-bottom that the customer can ignore initially.

## Settings & fields

### Information Bar section

| Field | Key | Notes |
|---|---|---|
| **Show information bar** | `show_cookies_bar` | Master toggle — when ON, the bar renders on first visit. |
| **Cookie wall** | `show_cookies_wall` | When ON, the customer must accept BEFORE seeing storefront content. Mutually exclusive with the bar in the modern UI. |
| **Cookies bar text** | `cookies_bar_text` | The text shown in the bar (rich HTML supported). |

### Cookies Consent dialog section

| Field | Key | Notes |
|---|---|---|
| **Cookies consent text** | `cookies_consent_text` | Long-form text shown in the detailed consent dialog (opened via "Manage preferences"). Rich text editor (TextEditor component). |

## Business rules

### The consent modal targets `#gdpr_popup`

The storefront JS expects a modal with id `gdpr_popup` to exist in the theme. The `cookies-table.tpl` view contains the modal markup with a toggle per cookie group. The **"Accept all"** button (`.js-cookies-accept`) sets every group to `yes`; the **"Save preferences"** button (`.js-cookies-accept-modal`) reads the per-group toggles, saves that state, and triggers the `/gdpr/cookie-consent` endpoint that cleans up rejected cookies (see [[apps-gdpr-cookies-consent-state]]).

**The two buttons are not symmetric:** only *Save preferences* calls the cleanup endpoint — *Accept all* does not (accepting everything leaves nothing to clean up). So rejected cookies are actively deleted only along the reject path.

### Closing the bar with × stores nothing

The bar's close control (`.bottom-freezed-bar-close`) **only hides the bar on the current page** — no consent is recorded. The bar therefore returns on the next page load, and every group stays on its `default` assumed state. A visitor who "dismissed the banner" has not answered it. See [[gdpr-consent-actions]].

### A partial consent does NOT dismiss the bar

Saving with only some categories enabled stores the choice correctly, but the bar **keeps showing** until every category is accepted — it doubles as a reminder that categories remain unaccepted. Full outcome table and the support playbook: [[gdpr-consent-persistence]].

### Re-open hooks — `#gdpr-trigger` / `#cookies-trigger`

The storefront JS registers click handlers for elements with id `gdpr-trigger` or `cookies-trigger` — clicking either opens the consent modal. **The platform does not auto-inject such a button.** The theme is responsible for placing one (typically a footer link "Cookie settings"). Without theme support, the customer cannot re-open the consent UI from a single click — there is no merchant-configurable "Cookie preferences" button in the stock UI.

### Side effects on save

The storefront bar / wall renders per the new config on the next page load. Existing visitors keep their stored consent until it expires (365 days) or they clear it — changing the bar text does not re-prompt anyone.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-consent-state]] — the `cc-cookie-consent` cookie, the `/gdpr/cookie-consent` cleanup endpoint, and the re-consent triggers (referenced inline above).
- [[apps-gdpr-overview]] — GDPR app overview, including the no-geo-gating rule (the bar shows to every visitor).

## Open questions

None.
