---
type: concept
aliases: ["Subscribe form display", "When does the subscribe form show", "Why isn't my subscribe form showing", "Popup display rules", "Form targeting", "Exit intent popup", "Time on page popup", "Hide form after subscribe", "displayForAll", "Form display eligibility", "Form not appearing", "Защо не се показва формата", "Кога се показва формата за абониране"]
tags: [marketing, subscribers, forms, popup, triggers, targeting, storefront, concepts]
plan_gates: []
created: 2026-06-30
updated: 2026-06-30
source_count: 3
---

# Subscribe-form display engine

## Definition

The **display engine** decides, for each storefront visitor, **whether a subscribe form shows, where it shows, and when it fires.** A form is not simply "on" — at render time the storefront runs a cascade of conditions, and a form that fails any of them silently does not appear (the same "silent drop" pattern that makes "why isn't my form showing?" a common support question). The decision combines five independent dimensions the merchant sets in the [[subscribe-forms-builder|builder]]:

1. **Mode** — **popup** (injected into eligible storefront pages) vs **embedded** (inline, only where its snippet / page-builder module runs). The `embedded` flag toggles this; embedded forms are force-set to fire `auto` on load.
2. **Where (URLs)** — the **included-URLs allowlist** and **excluded-URLs denylist** scope which pages a popup may appear on.
3. **When (triggers)** — the `startDisplaying` array of [[subscribe-forms-triggers|trigger types]] (`auto`, `exitIntent`, `timeOnPage`), combined as logical **OR** — the form fires when ANY trigger matches; `stopDisplaying` suppresses symmetrically.
4. **To whom (consent + already-subscribed)** — the inverted [[subscribe-forms-gdpr-consent|`cookies_consent`]] gate (targeting-cookie group), and **`displayForAll`** — when false (default) the form is hidden from a visitor who has already subscribed; when true it shows to everyone.
5. **Position** — the [[subscribe-forms-layout|`layoutPosition`]] (15 values, set per device) places the rendered form (center modal, corner slide-in, top/bottom bar, sidebar, fullscreen).

## Scope

Covered: the five display dimensions and how they combine into a single show/hide + when + where decision; the **≤ 5 popup forms loaded at storefront startup** (the storefront picks/rotates among them); the popup-vs-embedded split; why a configured form may never appear. NOT covered: the visual styling of the form (colors/fonts/media — see [[subscribe-forms-builder]]); what happens *after* submit (see [[lead-capture-lifecycle]] / [[subscribe-forms-submission-flow]]); the field set (see [[subscribe-forms-fields]]).

## Contrasts

- **Popup vs embedded** — a popup is store-wide (subject to URL scoping + triggers + position), injected at startup; an embedded form is page-local (only where the merchant pasted the snippet or dropped the page-builder "Embedded subscription form" module) and renders inline on load. Embedded ignores triggers/position (it's `auto`, in-flow).
- **Triggers (OR) vs URL scope (AND)** — multiple triggers are permissive (any one fires the form), but the URL allow/deny + consent gates are restrictive (all must pass). So a form with three triggers still won't show on a denied URL or to a consent-blocked visitor.
- **`displayForAll` vs re-display suppression** — `displayForAll` is about *who* (already-subscribed visitors), `stopDisplaying` is about *when not to* re-show; both can hide a form that is otherwise eligible.
- **`cookies_consent` is inverted** — `true` is the *bypass* (show even without targeting-cookie acceptance), not the gate. This is the single most-misread display setting — see [[subscribe-forms-gdpr-consent]].

## Where it applies

### The render-time eligibility cascade

For a popup form, the storefront module shows it only when **all** of these hold (any failure = silently hidden):

- The current page is on the **included-URLs** list (or the list is empty) **and not** on the **excluded-URLs** list.
- The visitor passes the **`cookies_consent`** targeting-cookie gate.
- The visitor is **not already subscribed**, unless `displayForAll = true`.
- At least one **`startDisplaying`** trigger fires, and **no** `stopDisplaying` condition suppresses it.

Then `layoutPosition` (for the visitor's device) decides where it renders.

### Startup load + rotation

Up to **5** popup forms load at storefront startup; the storefront selects or rotates among the eligible ones (so stacking many overlapping popups does not show them all at once). Embedded forms load independently, per page where their snippet runs.

### The "why isn't my form showing?" checklist

Walk the five dimensions: is it embedded (so only on its snippet page)? is the current URL allowed and not excluded? has the visitor accepted the targeting cookie group (or is `cookies_consent` set to bypass)? has the visitor already subscribed while `displayForAll` is off? is a trigger actually configured (a popup with no trigger never fires)? — see [[subscribe-forms-triggers]], [[subscribe-forms-gdpr-consent]], [[subscribe-forms-layout]].

## Related

- [[marketing-subscribers-subscribe-forms]] — hub.
- [[subscribe-forms-triggers]] — the three trigger types + `stopDisplaying`.
- [[subscribe-forms-layout]] — the 15 `layoutPosition` values, per device.
- [[subscribe-forms-gdpr-consent]] — the inverted `cookies_consent` gate.
- [[subscribe-forms-builder]] — popup-vs-embedded toggle, included/excluded URLs, `displayForAll`.
- [[subscribe-forms-list]] — where the merchant sees / toggles each form active.
- [[lead-capture-lifecycle]] — what happens once a shown form is submitted.

## Open Questions

- (verify) The exact selection / rotation rule when more than one eligible popup form qualifies on the same page.
