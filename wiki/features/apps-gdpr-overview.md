---
type: feature
nav_path: "Apps → GDPR"
route_name: apps.gdpr.overview
route_path: /admin/apps/gdpr/overview
aliases: ["GDPR", "Gdpr Overview", "Cookie consent", "Privacy compliance", "GDPR app", "ДРЛЗ", "enable disable button", "app active toggle"]
tags: [apps, gdpr, compliance, privacy, cookies, eu-regulation]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 12
---
# GDPR — Overview (compliance hub)

## Purpose

**GDPR** is the EU's General Data Protection Regulation. The CloudCart GDPR app implements the operational tools any EU-operating store needs to satisfy GDPR requirements:

- **Cookie consent management** — bar/wall on the storefront, granular consent per cookie group, integration with tracking scripts (Google Analytics / Tags / TikTok Pixel / Facebook Comments / etc.) so they only fire when the customer has consented to that category.
- **Privacy policies** — merchant-authored policy documents shown to customers + acceptance tracking.
- **Acceptance log** — record of which customer accepted which policy version at what time (with IP, device, timestamp) — the audit trail GDPR requires.
- **Customer requests** — handles right-to-access / right-to-erasure / data-portability requests (GDPR Articles 15-17, 20).
- **Store legal address** — the merchant's identifying contact details (Company name, BULSTAT, MOL, address) appearing on receipts, invoices, and privacy notices.

Without this app installed, the merchant has no cookie consent UI, no policy-acceptance log, and no customer-request workflow — meaning they're operating outside GDPR for EU traffic. The app is essentially **required for any merchant serving EU customers**.

This page is the **hub** for the GDPR app. It covers what the app is, where to find it, and what each tab does. The deeper verified mechanics — how the cookie consent UX works, how consent gates tracking scripts, how data-subject requests flow, and how consent gets captured into the audit log — are split into the aspect pages listed below.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so it can be switched off without uninstalling it. A disabled app stops working while keeping its settings.

## Where to find it

Sidebar → Apps → install → **GDPR**. The route is `/admin/apps/gdpr` (overview/hub) with sub-routes under the same prefix.

Tabs (sub-pages):

| Tab | Route name | Purpose |
|----------|------------|---------|
| Overview | `apps.gdpr.overview` | This hub page. |
| Settings | `apps.gdpr.settings` | App-level config + install-settings. See [[apps-gdpr-settings]]. |
| Address | `apps.gdpr.address` | Store legal address (company name, BULSTAT, MOL, phone, country/city). See [[apps-gdpr-address]]. |
| Cookies | `apps.gdpr.cookies` | Cookie consent management — bar/wall + per-group + per-cookie. See [[apps-gdpr-cookies]]. |
| Policy | `apps.gdpr.policy` | Privacy policies CRUD. See [[apps-gdpr-policy]]. |
| Acceptance | `apps.gdpr.acceptance` | Per-customer policy acceptance log + Export. See [[apps-gdpr-acceptance]]. |
| Requests | `apps.gdpr.requests` | Customer data-subject requests (access / erasure / portability). See [[apps-gdpr-requests]]. |

API endpoints under `/api/gdpr/*` (gated by `hasApiPermission:apps`):
- `GET/POST /api/gdpr/settings/{form?}` — load/save settings (per form section).
- `POST /api/gdpr/install` + `GET/POST /api/gdpr/install-settings` — install flow.
- `GET /api/gdpr/cookies` — cookies listing.
- `GET /api/gdpr/requests` — requests listing.
- `GET /api/gdpr/active/{status?}` — toggle active state.
- Cookies management nested routes under `/api/gdpr/cookies/*`.
- Policies management nested routes under `/api/gdpr/policy/*`.

## Sub-pages (in this cluster)

This app is split into the GDPR tab pages (Address, Cookies, Policy, Acceptance, Requests, Settings — each documented on its own page) PLUS four aspect pages under this hub that document the verified cross-tab mechanics:

- [[apps-gdpr-overview-consent-ux]] — the storefront cookie bar vs wall, the five standard cookie groups taxonomy, the `cc-cookie-consent` cookie structure + 365-day expiry, the "manage preferences" trigger hooks, no geo-gating, and no automatic cookie discovery.
- [[apps-gdpr-overview-script-gating]] — how consent gates tracking scripts: Google Consent Mode v2 via the `consent_mode_for_traffic` group, and how the consent state propagates to Google Analytics / Tags / TikTok Pixel / Facebook Comments loaders.
- [[apps-gdpr-overview-data-requests]] — the four customer data-subject request types, why rectification is not a request type, the three self-service storefront download endpoints (right-to-portability), the storefront request URLs, and the merchant-driven right-to-erasure flow.
- [[apps-gdpr-overview-consent-logging]] — how consent is captured: the five storefront form types, the append-only acceptance log, the `policies_popup` re-prompt mechanism, the marketing-policy flag, and the install seeder defaults.

## What the merchant can do here

### Activate / configure the app
- Install + go through the install-settings flow (collects required compliance data upfront).
- Toggle the app Active / Inactive via `GET /api/gdpr/active/{status?}`.
- Navigate to each tab to configure that area.

### Per-tab actions (each on its own page)
- **Store Address** — company name, BULSTAT, MOL, phone, country, city, address. See [[apps-gdpr-address]].
- **Cookies** — cookie information bar / wall toggles, bar/wall text + styling, cookie groups, per-cookie definitions. See [[apps-gdpr-cookies]] and the consent UX aspect [[apps-gdpr-overview-consent-ux]].
- **Policies** — privacy policy CRUD, multi-version support, per-policy acceptance tracking. See [[apps-gdpr-policy]].
- **Acceptance log** — per-customer acceptance records, Export (2FA-gated), filter/search. See [[apps-gdpr-acceptance]].
- **Customer Requests** — review and process customer data-subject requests. See [[apps-gdpr-requests]] and [[apps-gdpr-overview-data-requests]].

### What the merchant CANNOT do here
- Auto-comply without configuring policies + cookies first — the install flow forces minimum config.
- Skip the store-address requirement — many GDPR jurisdictions require visible business identification.
- Disable cookie consent if any tracking script is active — would be non-compliant.

## Settings & fields

The app uses a sectioned settings model — each tab has its own settings group accessed via `GET/POST /api/gdpr/settings/{form?}` (where `form` is the section identifier — `cookies` / `cookies-consent` / `address` / etc.). The detailed setting keys live on each tab's own page; the cookie consent UX settings (`show_cookies_bar`, `show_cookies_wall`) are documented on [[apps-gdpr-overview-consent-ux]] and [[apps-gdpr-cookies]].

## Business rules

### Required for EU traffic

GDPR applies to ANY business processing EU residents' personal data. If the merchant has even one EU customer, they need GDPR-compliant cookie consent + acceptance tracking + request handling. The app implements these.

### App-active enforcement

GDPR-specific routes are guarded by a check on the app's active state: if active → continue; if NOT active → return 404 (Not Found). The guard is attached to GDPR-specific routes so they're inaccessible when the app is deactivated.

### Acceptance log is immutable

GDPR audit requires retention of WHO accepted WHICH policy version WHEN. The log is append-only — entries cannot be edited or deleted (only exported). See [[apps-gdpr-overview-consent-logging]].

### Export gated by 2FA

The Acceptance Export action triggers `CC2FaAction` with action key `export_gdpr` — meaning the merchant must enter a 2FA code (TOTP / email-based) before the platform allows the export. This protects against unauthorised data export. See [[account-cc2fa]].

### Side effects on activation
- Install flow asks for minimum required config (address + cookies bar + at least one policy) and runs a seeder that creates the default policies + cookie groups + cookie providers — see [[apps-gdpr-overview-consent-logging]].
- Storefront begins showing the cookie bar / wall — see [[apps-gdpr-overview-consent-ux]].
- Customer-side request form becomes accessible — see [[apps-gdpr-overview-data-requests]].
- Acceptance log starts accumulating — see [[apps-gdpr-overview-consent-logging]].

### Permission
Standard apps permission scope. Some actions (Export) gated by 2FA additionally.

## Related

- [[apps]] — App Store hub.
- [[apps-gdpr-address]] — store legal address sub-page.
- [[apps-gdpr-cookies]] — cookie consent management sub-page.
- [[apps-gdpr-policy]] — privacy policies CRUD sub-page.
- [[apps-gdpr-acceptance]] — acceptance log + export sub-page.
- [[apps-gdpr-requests]] — customer requests sub-page.
- [[apps-gdpr-settings]] — settings sub-page.
- [[apps-gdpr-overview-consent-ux]] — cookie bar/wall UX, groups taxonomy, consent cookie (aspect).
- [[apps-gdpr-overview-script-gating]] — Google Consent Mode v2 + tracking-script gating (aspect).
- [[apps-gdpr-overview-data-requests]] — data-subject request types + self-service downloads (aspect).
- [[apps-gdpr-overview-consent-logging]] — consent capture forms + acceptance log + install seeder (aspect).
- [[apps-n18-audit]] — sister Bulgarian fiscal-compliance app (parallel concern).
- [[apps-google-analytics]] / [[apps-google-tags]] / [[apps-google-dynamic]] / [[apps-tiktok-pixel]] / [[apps-facebook-comments]] / [[apps-disqus-comments]] — tracking integrations gated by cookie consent.
- [[account-cc2fa]] — 2FA used by Acceptance Export.

## Open questions

None.
