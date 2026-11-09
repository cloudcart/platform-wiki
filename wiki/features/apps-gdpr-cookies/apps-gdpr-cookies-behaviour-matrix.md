---
type: feature
nav_path: "Apps → GDPR → Cookies → Behaviour matrix"
route_name: ""
route_path: ""
aliases: ["Cookie banner behaviour", "Cookie consent matrix", "banner keeps coming back", "banner returns after reload", "банерът се връща", "лентата се показва пак", "partial consent banner", "cookie bar does not disappear", "why does the cookie banner keep showing", "cookie consent combinations", "cookie banner configurations"]
tags: [apps, gdpr, cookies, consent, storefront, troubleshooting]
plan_gates: []
created: 2026-08-08
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-gdpr-cookies]]. See that hub for the configuration screens (bar/wall, groups, cookie definitions, consent state, consent mode); this sub-cluster covers what those settings *produce* on the storefront.

# Cookie consent — behaviour matrix

## Purpose

The complete behaviour reference for the storefront cookie prompt: **every setting that affects it, every action a visitor can take, and what each combination actually produces** — whether an answer is stored, whether refused groups' cookies are cleaned up, and whether the banner comes back on the next page load.

> **🔴 Since 06.11.2026 any answer — Accept, Save settings or Reject — dismisses the bar or wall.** Before that date the bar kept showing until every group was accepted, and the dialog's **Приемам** saved the switches; reports and notes from before then describe that old behaviour.

Anyone answering *"the cookie banner keeps coming back"* should start at [[gdpr-consent-persistence]].

## Where to find it

The settings live on [[apps-gdpr-cookies]] (Cookies tab) and [[apps-gdpr-settings]] (app-level). The behaviour described across this sub-cluster is what the visitor experiences on the storefront.

## Sub-pages (in this cluster)

- [[gdpr-consent-configurations]] — every setting that shapes the prompt: the app-level switches, the per-group `active` / `default` flags, the **bar × wall** combinations, what happens when the app is off, the absence of geographic gating, per-language texts, and why the policy re-acceptance popup is a separate thing.
- [[gdpr-consent-actions]] — what a visitor can do (Accept, Save settings, Reject, close with ×, do nothing, re-open), exactly what each one writes and cleans up, and how long an answer lasts.
- [[gdpr-consent-persistence]] — the outcome table, the causes that still bring the bar back, how to verify an answer saved, why a switch that starts *off* is usually a merchant setting, and the **support playbook** for *"the banner keeps coming back"*.
- [[gdpr-consent-theme-limits]] — what the theme does and does not control (it styles the prompt; the platform builds it), and the theme-supplied re-open links.

## What the merchant can do here

Nothing new — this sub-cluster maps existing settings to their outcomes. Use it to predict what a configuration will do before changing it, and to explain to a merchant why the prompt behaves as it does.

## Settings & fields

No settings of its own. The full configuration space is catalogued on [[gdpr-consent-configurations]]; the storage format of the recorded consent is on [[apps-gdpr-cookies-consent-state]].

## Business rules

The cluster-level rules, each detailed on its aspect page:

- **Any answer dismisses the bar** (since 06.11.2026). See [[gdpr-consent-persistence]].
- **Closing with × stores nothing** — the visitor has not answered the prompt. See [[gdpr-consent-actions]].
- **Any answer that refuses a group deletes that group's listed cookies.** See [[gdpr-consent-actions]].
- **A switch that starts off is usually the group's Default state**, not a discarded choice. See [[gdpr-consent-persistence]].
- **Switching on a group asks every visitor again.** See [[apps-gdpr-cookies-consent-state]].
- **The platform builds the prompt; the theme only styles it.** See [[gdpr-consent-theme-limits]].

## Related

- [[apps-gdpr-cookies]] — parent hub (the Cookies tab).
- [[apps-gdpr-cookies-bar-wall]] — the bar vs wall presentation and the re-open hooks.
- [[apps-gdpr-cookies-groups]] — the 5 groups and their `active` / `default` flags.
- [[apps-gdpr-cookies-consent-state]] — the stored consent's format, lifetime and cleanup endpoint.
- [[apps-gdpr-cookies-definitions]] — the per-cookie definitions that make a group renderable.
- [[apps-gdpr-overview-script-gating]] — what a rejected category actually blocks.
- [[apps-gdpr-settings]] — the app-level switches.

## Open questions

None.
