---
type: feature
nav_path: "Apps → GDPR → Cookies → Consent state"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["cc-cookie-consent", "Consent cookie", "Consent state", "Cookie consent expiry", "Cookie cleanup", "Cookie groups cache", "Re-consent rules"]
tags: [apps, gdpr, compliance, cookies, consent, storefront, cache]
plan_gates: []
created: 2026-06-10
updated: 2026-08-08
source_count: 5
---
# GDPR — Cookies: consent state & lifecycle

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (bar & wall, groups, definitions, consent mode).

## Purpose

This aspect documents **where and how the visitor's consent choice is stored and acted on** — the `cc-cookie-consent` browser cookie, its structure and defaults, its 365-day lifespan, why it is deliberately left unencrypted, the storefront cleanup of rejected cookies, the 20-minute group cache, and the rules for when (and when not) a visitor is re-prompted. This is the runtime / lifecycle slice; the admin UI for editing groups and cookies is on [[apps-gdpr-cookies-groups]] and [[apps-gdpr-cookies-definitions]].

## Where to find it

This behaviour runs on the storefront, driven by the configuration in the **Cookies tab** (`/admin/apps/gdpr/cookies`). The runtime endpoint is `GET /gdpr/cookie-consent`. There is no separate admin screen for the consent state itself — the merchant sees logged acceptances on [[apps-gdpr-acceptance]].

## What the merchant can do here

- Set per-group defaults that become the visitor's assumed state until they choose (see [[apps-gdpr-cookies-groups]]).
- Rely on the storefront to persist the choice for 365 days and to clean up rejected cookies automatically.
- Understand that editing the cookie LIST does not force existing visitors to re-consent, and plan re-consent strategy accordingly.

## Settings & fields

### The `cc-cookie-consent` cookie — structure + defaults

The consent state is persisted in a browser cookie named `cc-cookie-consent`. Its value is a `+`-separated list of `group:yes|no` pairs, e.g.:

```
system:yes+performance:yes+functional:yes+targeting:no+consent_mode_for_traffic:no
```

When no cookie is set yet, each group falls back to its `default` (see [[apps-gdpr-cookies-groups]]): `system`, `performance`, `functional`, `targeting` default to **yes**; `consent_mode_for_traffic` defaults to **no** (see [[apps-gdpr-cookies-consent-mode]]). Consent is recorded **per group, not per individual cookie**.

### 365-day expiry

When the customer accepts via "Accept all" or "Save preferences", the storefront JS writes the cookie with `expires: 365` days. After one year (or when the visitor clears browser cookies) the cookie is gone and the bar/wall re-appears on the next visit, prompting re-consent.

> **Writing the cookie does not necessarily dismiss the bar.** A **partial** consent (some categories rejected) is stored correctly and honoured, but the bar **keeps showing** until the visitor accepts every category — by design, as a standing reminder. So "the banner came back" is not evidence that the cookie failed to save. See [[gdpr-consent-persistence]] for the full outcome table and the support playbook.

## Business rules

### The consent cookie is NOT encrypted (by design)

The platform explicitly leaves the `cc-cookie-consent` cookie unencrypted, so the value is plain readable text (`system:yes+performance:yes+...`). This is intentional: it lets storefront JavaScript and third-party tracking scripts read the consent state directly via `Cookies.get` without a server round-trip.

### Storefront cleans up rejected cookies

The storefront endpoint `GET /gdpr/cookie-consent` deletes any browser cookie whose name appears in a not-yet-accepted group — actively removing tracking cookies the visitor hasn't agreed to. (This is the endpoint the consent-modal "Save preferences" button triggers — see [[apps-gdpr-cookies-bar-wall]].)

### 365-day expiry is the only automatic re-consent trigger

Adding a NEW cookie to an existing group does **not** re-prompt visitors — their group-level consent already covers it. To force fresh consent, the merchant must rebuild the consent UX themselves (e.g., delete and re-create a group, so visitors whose cookie lacks that group key fall back to the default state). The 365-day expiry is the only built-in automatic **re-consent** trigger — i.e. the only thing that discards a stored consent.

That is a different thing from the bar **re-appearing**: after a partial consent the bar keeps showing on every page load even though the stored consent is intact and unexpired (see [[gdpr-consent-persistence]]). Expiry discards the consent; the bar's persistence does not.

### 20-minute group cache, invalidated on save

The cookie-groups list is cached as `gdpr.cookie_groups_v2` with a 20-minute TTL. The cache is invalidated whenever **either** a cookie group OR a cookie inside a group is saved — so adding / editing / deleting a group or a cookie flushes the cache and admin changes propagate to the storefront within seconds rather than the full 20 minutes.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-groups]] — per-group `default` flag that seeds the pre-consent state.
- [[apps-gdpr-cookies-consent-mode]] — why `consent_mode_for_traffic` defaults to no (referenced inline above).
- [[apps-gdpr-cookies-bar-wall]] — the "Save preferences" button that triggers the cleanup endpoint (referenced inline above).
- [[apps-gdpr-acceptance]] — the merchant-facing log of recorded consent acceptances.

## Open questions

None.
