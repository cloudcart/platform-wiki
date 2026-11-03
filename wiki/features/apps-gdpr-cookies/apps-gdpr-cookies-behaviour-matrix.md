---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix"
route_name: ""
route_path: ""
aliases: ["Cookie banner behaviour", "Cookie consent matrix", "banner keeps coming back", "banner returns after reload", "банерът се връща", "лентата се показва пак", "partial consent banner", "cookie bar does not disappear", "why does the cookie banner keep showing", "cookie consent combinations", "cookie banner configurations"]
tags: [apps, gdpr, cookies, consent, storefront, troubleshooting]
plan_gates: []
created: 2026-08-08
updated: 2026-08-08
source_count: 3
---

> Part of [[apps-gdpr-cookies]]. See that hub for the configuration screens (bar/wall, groups, cookie definitions, consent state, consent mode); this sub-cluster covers what those settings *produce* on the storefront.

# Cookie consent — behaviour matrix

## Purpose

The complete behaviour reference for the storefront cookie prompt: **every setting that affects it, every action a visitor can take, and what each combination actually produces** — whether a consent is stored, whether rejected cookies are cleaned up, and whether the banner comes back on the next page load.

This sub-cluster exists because one behaviour reads like a bug but is not:

> **🔴 A partial consent is saved and honoured — but the bar keeps showing until the visitor accepts EVERY category.** The bar doubles as a standing reminder that categories remain unaccepted. *"The banner came back"* is therefore not evidence that the consent failed to save.

That single rule has produced repeat merchant reports and development investigations that found no defect. Anyone answering *"the cookie banner keeps coming back"* should start at [[gdpr-consent-persistence]].

## Where to find it

The settings live on [[apps-gdpr-cookies]] (Cookies tab) and [[apps-gdpr-settings]] (app-level). The behaviour described across this sub-cluster is what the visitor experiences on the storefront.

## Sub-pages (in this cluster)

- [[gdpr-consent-configurations]] — every setting that shapes the prompt: the app-level switches, the per-group `active` / `default` flags, the four **bar × wall** combinations (including OFF+OFF = no prompt at all), why an empty group vanishes from the dialog, what happens when the app is off, the absence of geographic gating, per-language texts, and why the policy re-acceptance popup is a separate thing.
- [[gdpr-consent-actions]] — the five things a visitor can do (Accept all, Save preferences, close with ×, do nothing, re-open) and exactly what each one writes and triggers, including why **Accept all and Save preferences are not symmetric** and how long a consent lasts.
- [[gdpr-consent-persistence]] — **the headline rule**: why a partial consent keeps the bar visible, the outcome table, how to verify a consent really saved, why a toggle that starts *off* is usually a merchant setting rather than a lost value, and the **support playbook** for *"the banner keeps coming back"*.
- [[gdpr-consent-theme-limits]] — the parts that are **not** the platform's: the consent dialog and its toggles are supplied by the storefront **theme**, so some behaviour differs per theme — plus the three facts documented from observed behaviour rather than platform source.

## What the merchant can do here

Nothing new — this sub-cluster maps existing settings to their outcomes. Use it to predict what a configuration will do before changing it, and to explain to a merchant why the prompt behaves as it does.

## Settings & fields

No settings of its own. The full configuration space is catalogued on [[gdpr-consent-configurations]]; the storage format of the recorded consent is on [[apps-gdpr-cookies-consent-state]].

## Business rules

The cluster-level rules, each detailed on its aspect page:

- **A partial consent does not dismiss the bar** — by design. See [[gdpr-consent-persistence]].
- **Closing with × stores nothing** — the visitor has not answered the prompt. See [[gdpr-consent-actions]].
- **Only the reject path cleans up cookies** — *Accept all* does not call the cleanup endpoint. See [[gdpr-consent-actions]].
- **A toggle that starts off is usually the group's `default`**, not a discarded choice. See [[gdpr-consent-persistence]].
- **With both bar and wall off, no prompt is ever shown** and the store runs permanently on assumed consent. See [[gdpr-consent-configurations]].
- **The dialog itself comes from the theme**, so the re-open experience is not uniform across stores. See [[gdpr-consent-theme-limits]].

## Related

- [[apps-gdpr-cookies]] — parent hub (the Cookies tab).
- [[apps-gdpr-cookies-bar-wall]] — the bar vs wall presentation and the re-open hooks.
- [[apps-gdpr-cookies-groups]] — the 5 groups and their `active` / `default` flags.
- [[apps-gdpr-cookies-consent-state]] — the stored consent's format, lifetime and cleanup endpoint.
- [[apps-gdpr-cookies-definitions]] — the per-cookie definitions that make a group renderable.
- [[apps-gdpr-overview-script-gating]] — what a rejected category actually blocks.
- [[apps-gdpr-settings]] — the app-level switches.

## Open questions

Collected on [[gdpr-consent-theme-limits]] — three behaviours documented from observation rather than platform source.
