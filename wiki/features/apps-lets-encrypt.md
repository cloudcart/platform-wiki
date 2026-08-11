---
type: feature
nav_path: "Apps → Let's Encrypt"
route_name: apps.lets_encrypt.settings
route_path: /admin/apps/lets_encrypt
aliases: ["Let's Encrypt", "LetsEncrypt", "Free SSL", "HTTPS certificate", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, ssl, security, infrastructure]
plan_gates: ["ssl_certificate"]
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Let's Encrypt (free SSL certificates)

## Purpose

**Let's Encrypt** integration — automatically obtains and renews **free SSL/TLS certificates** for the merchant's custom storefront domains via the Let's Encrypt certificate authority. Required to serve the storefront over HTTPS (modern web mandatory; Google penalises HTTP).

When installed and the merchant adds a custom domain via [[settings-domains]], Let's Encrypt verifies domain ownership, issues a certificate valid for 90 days, and auto-renews it before expiry. Free and auto-renewed — no merchant action after initial setup.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → Apps → install → **Let's Encrypt**.

## What the merchant can do here

- Install the app to enable auto-SSL for custom domains (installing is the activation — there is no separate on/off switch).
- Trigger manual renewal (for troubleshooting).
- View certificate expiry date per domain.

### What the merchant CANNOT do here
- Pick a different CA (always Let's Encrypt).
- Customize certificate validity period (Let's Encrypt fixes it at 90 days).
- Issue EV (Extended Validation) certificates — Let's Encrypt only issues DV (Domain Validation).
- Issue wildcard certificates (`*.merchant.com`) — wildcards require the DNS-01 challenge, which is not implemented (see Business rules). Wildcards must be bought elsewhere and uploaded manually.

## Settings & fields

This app is intentionally minimal — installing it is the only action. All certificate operations (manual upload, viewing status, manual renewal) happen on the SSL screen under **Settings → Domains → SSL** (route `admin.ssl.create-from-session`), not inside this app.

## Business rules

### Auto-renew: 25 days before expiry

Certificates are 90 days long. The platform's scheduled renewal sweep reissues any certificate whose `valid_to` is less than **25 days** in the future — giving roughly a 65-day stable window plus a 25-day renewal-eligible window per certificate, enough to retry several times if the first attempt fails. The renewal runs unattended; the merchant does not trigger it.

**Renewal priority — newest first.** The sweep processes the most recently created certificates first. If the cycle gets throttled by rate limits, older certificates wait, so a recently registered domain is renewed sooner.

**Disabled domains are skipped.** Only certificates whose domain (Host) is active in [[settings-domains]] are renewed. A domain the merchant has disabled stops getting renewal attempts, and its certificate lapses without wasting rate-limit budget.

### Failed-renewal surface — no merchant email

When a renewal fails, the error message is stored on the certificate and is visible to the merchant on the SSL list under **Settings → Domains → SSL** (where their domain's certificate appears). An internal Slack alert goes to the `cc-system` channel with the site id and error. There is **no automatic email** to the merchant when an individual renewal fails — the merchant must check the SSL list.

### Domain ownership challenge — HTTP-01 only

Issuance requires proving the merchant owns the domain. CloudCart uses the **HTTP-01** challenge: Let's Encrypt fetches a token from `http://<domain>/.well-known/acme-challenge/<filename>`, which CloudCart serves automatically via its routing. The DNS-01 (TXT record) challenge is **not** implemented, which is why wildcard certificates are unsupported.

### One certificate per domain

Each storefront subdomain / aliased domain gets its **own** certificate — there is no "combine all my domains into one SAN/multi-domain cert" toggle.

### Force HTTPS after issuance

Once a certificate is issued and active for a domain, the platform serves all storefront routes over HTTPS and redirects HTTP → HTTPS automatically. The redirect is built into the platform's routing; the merchant does not configure it in this app.

### Resume-after-install

If a merchant tries to enable HTTPS on a custom domain before installing the app, the pending request is stored in the session (`le_request`) and the install is prompted. After install completes, the merchant is redirected back to `admin.ssl.create-from-session` to continue the certificate request — they don't restart from scratch.

### Manual paid certificate upload

Manual SSL upload exists outside this app, under **Settings → Domains → SSL**. The merchant can paste a private key + certificate bought elsewhere (EV / OV / wildcard); the platform then serves that uploaded certificate. Let's Encrypt **only auto-renews certificates flagged `free`** — manually uploaded paid certificates are the merchant's responsibility to renew.

### Rate limits

Let's Encrypt enforces rate limits (50 certs per domain per week, 5 duplicate certs per week). Stores changing domains frequently may hit the caps.

### Permission

Standard apps permission scope.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `ssl_certificate` | Access gate (plan-level) | Access to the SSL management UI in [[settings-ssl]] / [[settings-domains]] — installing or renewing a Let's Encrypt cert through this app requires the merchant's plan to include `ssl_certificate`. Lower plans see HTTP 402 at the SSL screen. Existing certificates keep auto-renewing on plan downgrade for the contract duration. |

Two NON-plan gates also gate this app:

- **`lets_encrypt` app subscription** — in some countries this is a paid CloudCart app (free in others; the per-country `is_paid` flag is resolved from the app registry). The renewal sweep checks `cc_apps_purchase:lets_encrypt`; if the app subscription has lapsed, renewal is skipped and `renew_error` records *"Renew error: no active subscription"*.
- **Site billing status** — the renewal sweep skips sites in `status = 'not_paid'`. A merchant whose plan subscription has lapsed will NOT have their certificate auto-renewed, and HTTPS breaks after the next renewal cycle.

`ssl_certificate` is access-shaped (boolean) and requires a plan upgrade; lower plans are redirected to the per-feature upsell at [[plan-features]]. The app-subscription and site-billing gates are independent of the plan-feature gate and require their own remediation (keep the subscription current for certificates to roll over).

## Related

- [[apps]] — App Store.
- [[settings-domains]] — domain configuration; LE issues certs per domain registered here.
- [[apps-private-store]] — full HTTPS required for login pages.
- [[apps-gdpr-overview]] — HTTPS required for GDPR-compliant operation.

## Open questions
