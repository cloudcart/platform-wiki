---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix → Configurations"
route_name: ""
route_path: ""
aliases: ["cookie consent settings space", "bar and wall combinations", "show_cookies_bar show_cookies_wall", "no cookie prompt shown", "cookie category not in banner", "GDPR app off cookies", "cookie banner all visitors", "cookie bar text per language"]
tags: [apps, gdpr, cookies, consent, settings]
plan_gates: []
created: 2026-08-08
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-gdpr-cookies-behaviour-matrix]]. See the hub for the other aspects (visitor actions, banner persistence, theme limits).

# Cookie consent — the configuration space

## Purpose

Every setting that shapes the storefront cookie prompt, and what each combination produces — including the combinations that silently switch the prompt off altogether.

## Where to find it

App-level switches on [[apps-gdpr-settings]]; the presentation and group settings on [[apps-gdpr-cookies]] (Cookies tab).

## What the merchant can do here

Choose whether a prompt appears at all and in which form, which categories it offers, and what each category assumes before the visitor answers.

## Settings & fields

### App-level

| Setting | Values | Effect |
|---|---|---|
| App `active` | on / off | Master switch — see *When the app is off* below. |
| `show_cookies_bar` | 0 / 1 | The dismissible bar at page bottom. |
| `show_cookies_wall` | 0 / 1 | The blocking modal, auto-opened on load. |
| `show_policies_popup` | 0 / 1 | A separate policy re-acceptance popup — **not** the cookie prompt (see below). |
| `cookies_bar_text` | rich text | The bar copy — held **per store language**. |
| `cookies_consent_text` | rich text | The dialog copy. |

### Per cookie group

The 5 standard groups are catalogued on [[apps-gdpr-cookies-groups]]. Each carries:

| Setting | Values | Effect |
|---|---|---|
| `active` | 0 / 1 | Whether the category is offered at all. The `system` group is always active and can never be rejected. |
| `default` | 0 / 1 | The position the group's switch starts in before the visitor answers. It does not change what the tracking apps do before an answer (fixed states, see [[apps-gdpr-overview-script-gating]]). Only `consent_mode_for_traffic` ships as **no**. |
| cookie definitions | list | Listed in the group's tab; they are what a refusal deletes. |

## Business rules

### Bar and wall — the four combinations

| `show_cookies_bar` | `show_cookies_wall` | Result |
|---|---|---|
| ON | OFF | The normal setup: a dismissible bar at page bottom; the dialog opens on demand. |
| OFF | ON | The blocking setup: the dialog **auto-opens** without a close button until the visitor answers. |
| OFF | OFF | **No prompt and no dialog.** The current admin cannot choose this (its dropdown has only bar and wall); only settings saved earlier can hold it. Nothing is ever stored, so the fixed pre-answer states apply for good. |
| ON | ON | The storefront treats it as the bar. |

Only the **wall** is auto-opened by the platform, and only when no answer is stored.

### Every active group is offered, even an empty one

The dialog has a tab for every **active** group, with or without cookie entries. A group missing from the dialog is switched off ([[apps-gdpr-cookies-groups]]). Only the cookie table that the `{cookies_table}` placeholder prints on a page leaves out groups without entries ([[apps-gdpr-cookies-definitions]]).

### When the app itself is off

Turning the GDPR app off removes the prompt entirely — no bar, no wall, no script gating. Consent already stored in visitors' browsers stays there but stops being acted upon. Turning the app back on resumes prompting visitors who have no stored consent. See [[apps-gdpr-settings]].

### No geographic gating

The prompt is shown to **every** visitor while the app is active — there is no "EU visitors only" mode. A merchant asking why non-EU visitors see the banner is seeing intended behaviour. See [[apps-gdpr-overview]].

### The consent texts are per-language

The copy is held per store language, and the platform shipped different defaults per language. A merchant who edits the text in one language and still sees the old wording on another storefront language is looking at a **different language's value**, not a caching problem. (Genuine post-save propagation delay is the separate 20-minute group cache — see [[apps-gdpr-cookies-consent-state]].)

### The policy re-acceptance popup is a different prompt

`show_policies_popup` drives a **separate** dialog asking already-registered customers to re-accept the store's policies. It is not part of cookie consent, has its own text, and fires for logged-in customers with no acceptance record. A logged-in visitor can therefore meet **both** prompts on one visit, and accepting one does nothing to the other. See [[apps-gdpr-settings]] and [[apps-gdpr-overview-consent-logging]].

## Related

- [[apps-gdpr-cookies-behaviour-matrix]] — hub.
- [[apps-gdpr-cookies-groups]] — the group taxonomy and the `default` flag in detail.
- [[apps-gdpr-cookies-definitions]] — the per-cookie definitions a group needs to render.
- [[apps-gdpr-cookies-bar-wall]] — the admin fields behind the bar / wall choice.
- [[apps-gdpr-settings]] — the app-level switches.
- [[apps-gdpr-overview]] — the no-geo-gating rule.

## Open questions

None.
