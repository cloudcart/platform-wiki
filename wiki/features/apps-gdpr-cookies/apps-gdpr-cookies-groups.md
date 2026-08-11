---
type: feature
nav_path: "Apps → GDPR → Cookies → Groups"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["Cookie groups", "Cookie group editor", "Cookie groups taxonomy", "system group", "performance group", "functional group", "targeting group", "Cookie default state"]
tags: [apps, gdpr, compliance, cookies, consent, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# GDPR — Cookies: groups

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (bar & wall, definitions, consent mode, consent state).

## Purpose

This aspect documents the **cookie groups** — the categories the visitor accepts or rejects as a unit. It covers the 5 standard groups CloudCart ships, the per-group editor the merchant uses to configure each one, the `default` flag that decides the assumed state before the visitor has chosen, and why the Necessary / `system` group can never be rejected. The individual cookies *inside* a group are a separate concern — see [[apps-gdpr-cookies-definitions]].

## Where to find it

Sidebar → Apps → GDPR → **Cookies tab** (`/admin/apps/gdpr/cookies`). Each group renders as an accordion; the group editor (`AddOrEditGroup.vue`) opens inline below the group's header. Saving fires `POST /admin/api/gdpr/settings/cookies-groups/{group.id}`.

## What the merchant can do here

- Turn a group **active** (offered to customers) or inactive.
- Set the group's **default state** (assumed accept vs reject before the visitor decides).
- Edit the customer-facing **name** and **description** per group, per language.
- Adjust default states per the compliance jurisdiction (GDPR-strict = all opt-in; CCPA = some opt-out acceptable).

What the merchant **cannot** do: disable the `system` group from showing, or set the `system` group's default to rejected — those cookies are technically essential.

## Settings & fields

### The 5 standard cookie groups (verified)

The platform ships **5** standard groups (not 4). Defaults shipped with EN, BG, RO, EL, HU translations in the seed data; the merchant can edit per-language wording.

| Group key (`mapping`) | Default state | Customer-facing label | Notes |
|---|---|---|---|
| `system` | yes | Strictly Necessary Cookies | Always yes — cannot be rejected. Session, cart, login. |
| `performance` | yes | Performance Cookies | Counts visits / traffic sources. Customer may reject. |
| `functional` | yes | Functional Cookies | Videos, live chats, language preference. |
| `targeting` | yes | Targeting Cookies | Advertising-partner cookies. |
| `consent_mode_for_traffic` | **no** | Google Consent Mode | Separate group for Google Ads / Analytics / Floodlight Consent Mode v2 signals — explicit opt-in required. See [[apps-gdpr-cookies-consent-mode]]. |

### Group editor (`AddOrEditGroup.vue`) — 4 fields, no per-cookie list inside

The per-group editor collects exactly four fields. The per-cookie list is managed via a **separate** modal opened from each group's cookie-table row (see [[apps-gdpr-cookies-definitions]]) — the group editor does not include the cookies themselves.

| Field | Component | Conditional visibility |
|---|---|---|
| **Active** (`group.active`, 0/1) | ActiveSwitch | Hidden for `system` group (always active). |
| **Default state** (`group.default`, 0/1) | ActiveSwitch | Only shown when `active = 1`. Drives the assumed-consent fallback when the visitor has no `cc-cookie-consent` cookie yet. |
| **Name** (`group.name`, max 191) | InputComponent | The customer-facing label (e.g., "Performance Cookies"). |
| **Description** (rich text via `TextEditor`) | TextEditor | The longer explanation rendered next to the toggle in the storefront's cookie modal. |

## Business rules

### The `default` flag is the pre-consent fallback

When no `cc-cookie-consent` cookie is present, each group's `default` column drives the assumed consent state. For non-`system` groups the merchant can flip `default` between **yes** (assume consent) and **no** (assume rejection). The seed data sets all groups except `consent_mode_for_traffic` to `yes`; the merchant can override per group. How that fallback is stored and read is documented on [[apps-gdpr-cookies-consent-state]].

### The `system` group is special

The `system` group covers the platform's own essential cookies (session, cart, login). It is always active, its **Active** switch is hidden, and its default cannot be set to rejected — the customer cannot opt out of functional cookies.

### Cache invalidation on group save

The cookie-groups list is cached for 20 minutes (`gdpr.cookie_groups_v2`), but the cache is invalidated whenever a group (or a cookie inside one) is saved — so a merchant's group edits appear to the admin immediately and propagate to the storefront within seconds rather than the full TTL. See [[apps-gdpr-cookies-consent-state]] for the full caching mechanics.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-definitions]] — the per-cookie modal opened from each group's cookie-table row (referenced inline above).
- [[apps-gdpr-cookies-consent-mode]] — the `consent_mode_for_traffic` group and its opt-in gating (referenced inline above).
- [[apps-gdpr-cookies-consent-state]] — how the `default` flag and group state are stored in the consent cookie (referenced inline above).

## Open questions

None.
