---
type: feature
nav_path: "Apps → GDPR → Cookies → Consent state"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["cc-cookie-consent", "Consent cookie", "Consent state", "Cookie consent expiry", "Consent 180 days", "Cookie cleanup", "Cookie groups cache", "Re-consent rules"]
tags: [apps, gdpr, compliance, cookies, consent, storefront, cache]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 6
---
# GDPR — Cookies: consent state & lifecycle

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (bar & wall, groups, definitions, consent mode).

## Purpose

This aspect documents **where and how the visitor's consent choice is stored and acted on** — the `cc-cookie-consent` browser cookie, its structure, the states that apply before an answer, its 180-day lifespan, why it is deliberately left unencrypted, the cleanup of refused groups' cookies, the 20-minute group cache, and what asks a visitor again. This is the runtime / lifecycle slice; the admin UI for editing groups and cookies is on [[apps-gdpr-cookies-groups]] and [[apps-gdpr-cookies-definitions]].

## Where to find it

This behaviour runs on the storefront, driven by the configuration in the **Cookies tab** (`/admin/apps/gdpr/cookies`). The runtime endpoint is `GET /gdpr/cookie-consent`. There is no admin screen for it: a visitor's cookie answer lives only in their browser and is not logged by the store. The **Policy acceptance** tab ([[apps-gdpr-acceptance]]) records policy acceptances, not cookie answers.

## What the merchant can do here

- Set each group's **Default state**, the position its switch starts in (see [[apps-gdpr-cookies-groups]]).
- Rely on the storefront to keep the answer for 180 days and to delete the cookies listed under refused groups.
- Understand that editing the cookie LIST does not force existing visitors to re-consent, and plan re-consent strategy accordingly.

## Settings & fields

### The `cc-cookie-consent` cookie — structure + defaults

The consent state is persisted in a browser cookie named `cc-cookie-consent`. Its value is a `+`-separated list of `group:yes|no` pairs, e.g.:

```
system:yes+performance:yes+functional:yes+targeting:no+consent_mode_for_traffic:no
```

Every answer names every active group. Consent is recorded **per group, not per individual cookie**.

### Before an answer: fixed states, not the merchant's defaults

Until the visitor answers, the storefront and the store's server treat `system`, `performance`, `functional` and `targeting` as **yes** and `consent_mode_for_traffic` as **no**. These states are fixed in the platform: a group's **Default state** setting only moves its switch in the dialog ([[apps-gdpr-cookies-groups]]). A group the store switched off, absent from every answer, keeps its fixed state.

### 180-day lifetime

Every answer — Accept, Save settings or Reject — is written for **180 days** at the site root, `SameSite=Lax`, on the host it was given on (until 06.11.2026: 365 days). After that, or when the visitor clears cookies, the bar or wall shows again. Any answer dismisses it ([[gdpr-consent-persistence]]).

## Business rules

### The consent cookie is NOT encrypted (by design)

The platform explicitly leaves the `cc-cookie-consent` cookie unencrypted, so the value is plain readable text (`system:yes+performance:yes+...`). This is intentional: it lets storefront JavaScript and third-party tracking scripts read the consent state directly via `Cookies.get` without a server round-trip.

### Every answer cleans up the refused groups

After each answer the storefront deletes, in the browser, the cookies listed under each refused group, on the store's host and its parent domains (where trackers such as `_fbp` live); a listed `_ga_…` name matches every GA4 stream cookie. It also calls `GET /gdpr/cookie-consent`, which tells the browser to forget the same cookies, including ones scripts cannot reach. Only cookies the merchant listed under a group are removed ([[apps-gdpr-cookies-definitions]]).

### What asks a visitor again

- The answer expiring (180 days) or the visitor clearing cookies.
- The store switching on a group the stored answer does not name: everyone is asked once more.

Adding a cookie to an existing group, or editing a text, asks nobody again — the group-level answer already covers it.

### 20-minute group cache, invalidated on save

The cookie-groups list is cached as `gdpr.cookie_groups_v2` with a 20-minute TTL. The cache is invalidated whenever **either** a cookie group OR a cookie inside a group is saved — so adding / editing / deleting a group or a cookie flushes the cache and admin changes propagate to the storefront within seconds rather than the full 20 minutes.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-groups]] — per-group **Default state** that sets the switch's starting position.
- [[apps-gdpr-cookies-consent-mode]] — why `consent_mode_for_traffic` defaults to no (referenced inline above).
- [[apps-gdpr-cookies-bar-wall]] — the buttons that store an answer.
- [[apps-gdpr-cookies-platform-cookies]] — the storefront's own cookies.
- [[apps-gdpr-acceptance]] — the log of policy acceptances (cookie answers are not logged).

## Open questions

None.
