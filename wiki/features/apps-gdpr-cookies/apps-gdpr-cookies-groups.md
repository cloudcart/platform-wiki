---
type: feature
nav_path: "Apps → GDPR → Cookies → Groups"
route_name: apps.gdpr.cookies
route_path: /admin/apps/gdpr/cookies
aliases: ["Cookie groups", "Cookie group editor", "Cookie groups taxonomy", "system group", "performance group", "functional group", "targeting group", "Cookie default state"]
tags: [apps, gdpr, compliance, cookies, consent, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 7
---
# GDPR — Cookies: groups

> Part of [[apps-gdpr-cookies]]. See the hub for the other aspects (bar & wall, definitions, consent mode, consent state).

## Purpose

This aspect documents the **cookie groups** — the categories the visitor accepts or rejects as a unit. It covers the 5 standard groups CloudCart ships, the per-group editor the merchant uses to configure each one, the `default` flag that decides the assumed state before the visitor has chosen, and why the Necessary / `system` group can never be rejected. The individual cookies *inside* a group are a separate concern — see [[apps-gdpr-cookies-definitions]].

## Where to find it

Sidebar → Apps → GDPR → **Cookies tab** (`/admin/apps/gdpr/cookies`). Each group renders as an accordion; the group editor (`AddOrEditGroup.vue`) opens inline below the group's header. Saving fires `POST /admin/api/gdpr/settings/cookies-groups/{group.id}`.

## What the merchant can do here

- Turn a group **active** (offered to customers) or inactive.
- Set the group's **default state** (whether its switch starts on or off in the dialog).
- Edit the customer-facing **name** and **description** per group, per language.
- Start the optional switches off, so the dialog asks for opt-in.

What the merchant **cannot** do: disable the `system` group from showing, or set the `system` group's default to rejected — those cookies are technically essential.

## Settings & fields

### The 5 standard cookie groups (verified)

The platform ships **5** standard groups (not 4). Defaults shipped with EN, BG, RO, EL, HU translations in the seed data; the merchant can edit per-language wording.

| Group key (`mapping`) | Default state | Admin box title | Visitor label (seed, EN / BG) | Notes |
|---|---|---|---|---|
| `system` | yes | Necessary cookies | Strictly Necessary Cookies / Строго необходими | Always yes — cannot be rejected. Session, cart, login. |
| `performance` | yes | Efficiency | Performance Cookies / Ефективност | Counts visits / traffic sources. |
| `functional` | yes | Functionality | Functional Cookies / Функционалност | Videos, live chats, language preference. |
| `targeting` | yes | Targeting | Targeting Cookies / Таргетиране | Advertising-partner cookies. |
| `consent_mode_for_traffic` | **no** | Google Consent Mode | Google Consent Mode / Режим на съгласие за трафик | Consent Mode v2 signals — explicit opt-in. See [[apps-gdpr-cookies-consent-mode]]. |

The visitor labels are the seed's text, so they are what a store shows until the merchant renames a group. The admin's Bulgarian box titles are kept in the admin's translations, not in the code.

### Group editor (`AddOrEditGroup.vue`) — 4 fields, no per-cookie list inside

The per-group editor collects exactly four fields. The per-cookie list is managed via a **separate** modal opened from each group's cookie-table row (see [[apps-gdpr-cookies-definitions]]) — the group editor does not include the cookies themselves.

| Field | Component | Conditional visibility |
|---|---|---|
| **Active** (`group.active`, 0/1) | ActiveSwitch | Hidden for `system` group (always active). |
| **Default state** (`group.default`, 0/1) | ActiveSwitch | Only shown when `active = 1`. The position the group's switch starts in, in the dialog, before the visitor answers. |
| **Name** (`group.name`, max 191) | InputComponent | The customer-facing label (e.g., "Performance Cookies"). |
| **Description** (rich text via `TextEditor`) | TextEditor | The longer explanation rendered next to the toggle in the storefront's cookie modal. |

## Business rules

### Default state moves the switch, not the tracking

**Default state** decides whether the group's switch starts on or off when a visitor first opens the dialog, so a visitor who presses **Save settings** without touching it stores that value. It does not decide what happens before an answer: until then the tracking apps follow fixed states (`targeting`, `performance`, `functional` accepted; Consent Mode refused) whatever this setting says. See [[apps-gdpr-cookies-consent-state]] and [[apps-gdpr-overview-script-gating]].

### A switched-off group counts as accepted

A group the merchant switched off is not offered, so a visitor's choice never names it. It counts as its fixed pre-answer state: accepted, except for the Google Consent Mode group, whose switching off turns Consent Mode off instead. The Storefront API lists such groups in `cookieConsent.inactiveGroups` ([[headless-analytics-consent]]).

### The `system` group is special

The `system` group covers the platform's own essential cookies (session, cart, login). It is always active, its **Active** switch is hidden, and its default cannot be set to rejected — the customer cannot opt out of functional cookies.

### Cache invalidation on group save

The cookie-groups list is cached for 20 minutes (`gdpr.cookie_groups_v2`), but the cache is invalidated whenever a group (or a cookie inside one) is saved — so a merchant's group edits appear to the admin immediately and propagate to the storefront within seconds rather than the full TTL. See [[apps-gdpr-cookies-consent-state]] for the full caching mechanics.

## Related

- [[apps-gdpr-cookies]] — hub.
- [[apps-gdpr-cookies-definitions]] — the per-cookie modal opened from each group's cookie-table row (referenced inline above).
- [[apps-gdpr-cookies-consent-mode]] — the `consent_mode_for_traffic` group and its opt-in gating (referenced inline above).
- [[apps-gdpr-cookies-consent-state]] — how the `default` flag and group state are stored in the consent cookie (referenced inline above).
- [[headless-analytics-consent]] — consent on a Nitrogen storefront.

## Open questions

None.
