---
type: feature
nav_path: "Settings → Domains → SSL"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["SSL", "SSL certificate", "HTTPS", "Let's Encrypt", "ССЛ", "Сертификат", "TLS", "Certificate management"]
tags: [settings, ssl, certificate, domains, lets-encrypt, security]
plan_gates: ["ssl_certificate"]
created: 2026-05-23
updated: 2026-06-10
source_count: 9
---

# SSL certificates

## Purpose

The merchant's **SSL certificate management** for every domain attached to their store — both the always-present CloudCart subdomain (e.g., `mystore.cloudcart.net`) and any custom domains added in [[settings-domains]]. SSL is what makes the storefront load over HTTPS without browser security warnings; without a valid certificate, modern browsers refuse to load the site or show a red warning.

There is **no standalone "SSL" sidebar entry** — SSL management happens inside the **Domains** page via the per-domain **SSL** action (button in each domain's row), which opens the **SSL Modal**. The modal has two top-level paths:

- **Manage existing certificate** — when a cert is already installed. Shows expiry, issuer, full parsed details, the renewal mode (Automatic / Manual), a **Remove** button, and any renewal error.
- **Install new certificate** — when no cert is in place. Two tabs: **Automatic install** (via [[apps-lets-encrypt]]) or **Manual install** (paste a cert from an external CA).

## Where to find it

Sidebar → Settings → **Domains** → click the **SSL** action in any domain's row.

The page's breadcrumb reads "Settings → Domains". The modal title reads "Install SSL Certificate for **{host}**" (when no cert) or "Manage SSL Certificate for **{host}**" (when a cert exists).

Direct URL pattern: `/admin/settings/domains` — the SSL modal is opened by user interaction, not by a standalone URL. The per-domain manage path `settings/domains/ssl/manage/%` is the access-gated endpoint behind the `ssl_certificate` plan-feature check.

## What the merchant can do here

This page is the navigation pivot for the six aspect pages below — see each for the full flow.

- **Open the SSL modal** for a domain — from [[settings-domains]], click the **SSL** action in the row. The modal opens scoped to that one domain.
- **View an existing certificate** — see expiry, issuer, full parsed details, renewal mode (Automatic / Manual), and any renewal-error banner. Remove it via the **Remove** danger button (with confirm: *"Are you sure you want to remove it?"*).
- **Install via Let's Encrypt (Automatic)** — see [[settings-ssl-automatic-install]].
- **Install via external provider (Manual)** — see [[settings-ssl-manual-install]].
- **Understand auto-renewal mechanics** — see [[settings-ssl-auto-renewal]].
- **Understand expiry and fallback to the CloudCart subdomain** — see [[settings-ssl-expiry-fallback]].
- **Understand Cloudflare / edge propagation delays** — see [[settings-ssl-edge-propagation]].
- **Diagnose validation errors and SSL ERROR banner messages** — see [[settings-ssl-troubleshooting]].

### What the merchant CANNOT do here

- Schedule certificate rotation manually (Let's Encrypt renewal is automatic; manual certs must be replaced before expiry).
- Bulk-install certs for multiple domains at once — one domain at a time.
- Upload a single SAN/wildcard cert for multiple domains through this UI alone — the merchant pastes the same cert/chain into each domain's manual-install flow.
- See historical certificates — only the currently-installed cert is visible.
- Change the CSR parameters AFTER the cert is issued — Remove and reinstall to change Organization, Locality, etc.

## Sub-pages (in this cluster)

This feature is split into six aspect pages. The Assistant should drill into the aspect that matches the question.

- [[settings-ssl-automatic-install]] — Let's Encrypt issuance flow, the `lets_encrypt` paid-app gate, ACME HTTP-01 verification, apex + www together.
- [[settings-ssl-manual-install]] — CSR + private-key generation, the Domain details form, paste cert + chain, **Regenerate** button, install-time cryptographic validation.
- [[settings-ssl-auto-renewal]] — daily `ssl:sites` sweep, the 25-day threshold, billing-state filter (`not_paid` skipped), how `renew_error` is set and cleared.
- [[settings-ssl-expiry-fallback]] — what happens when a cert actually expires: primary-domain switch back to `*.cloudcart.net`, admin alerts, deactivation of non-primary domains.
- [[settings-ssl-edge-propagation]] — Cloudflare Custom-Hostname push, `pending` / `gcloud_pending` flags, the CloudCart subdomain wildcard cert (platform-managed).
- [[settings-ssl-troubleshooting]] — verbatim validation error strings, the SSL ERROR renewal banner messages, the matched-set rule (CSR + key + cert + chain), self-signed rejection.

## Settings & fields

The full per-field reference for each tab lives on its aspect page:

- **View existing certificate (Manage mode)** — Source badge, Expiry date, Renewal badge (Automatic green / Manual purple), cert details JSON viewer, **Remove** button, SSL ERROR banner. See [[settings-ssl-auto-renewal]] for the renewal-status field semantics and [[settings-ssl-troubleshooting]] for the error-banner messages.
- **Automatic install tab** — Common Name (read-only), **Automatic install** primary button, Required-app card. See [[settings-ssl-automatic-install]].
- **Manual install tab** — Common Name (CN) / Organization (O) / Email / Country / Locality / State, CSR + Private key (after generation), Certificate textarea, Chained Certificate textarea. See [[settings-ssl-manual-install]].

### Plan-feature gate

- `ssl_certificate` plan feature — controls access to the SSL modal. Stores without the feature cannot install / manage certificates via this UI; visiting `settings/domains/ssl/manage/%` redirects to the [[plan-features]] upsell. **Existing certificates continue auto-renewing on plan downgrade for the contract duration** — only NEW install / replace actions are blocked. Most plans include `ssl_certificate` by default.
- `lets_encrypt` paid app — a separate APP subscription (NOT a plan-feature). Required for the **Automatic install** tab to work. See [[apps-lets-encrypt]].

## Business rules

The cross-cutting rules that span all aspects:

### Two installation modes — only one cert per domain

A domain can have either a Let's Encrypt cert OR a manual external cert at any given time. The cert record tracks this via a `free` boolean: `free=1` = Let's Encrypt, `free=0` = external. **Switching modes requires Remove + reinstall.** The Automatic tab warns when a `free=0` cert exists: *"To make automatic install, first you need to remove the certificate from the manual install"*. There is no equivalent warning when switching automatic → manual — the merchant must just know.

### DNS must be pointing correctly at issuance time

Both install modes require the domain's DNS to be pointing at CloudCart per [[settings-domains]]'s activation flow. DNS errors at issuance surface as validation or SSL ERROR banner messages — see [[settings-ssl-troubleshooting]].

### CloudCart subdomain has its own platform-managed cert

The store's `*.cloudcart.net` subdomain uses a wildcard certificate managed by CloudCart's infrastructure. The merchant does NOT manage that cert through this UI — it is always automatically valid and renewed by CloudCart's platform team. This is why the fallback to the CloudCart subdomain (when a custom domain's cert expires) keeps the storefront serving without HTTPS warnings — see [[settings-ssl-edge-propagation]] and [[settings-ssl-expiry-fallback]].

### Permissions

The SSL modal requires the same permission grants as [[settings-domains]] — `settings`, `settings.domains`. There is no separate SSL-only permission. See [[settings-staff]].

### Side effects on install / remove

- **Install** — cert + chain + key stored against the domain; Cloudflare custom-hostname binding updated. See [[settings-ssl-edge-propagation]] for propagation timing.
- **Remove** — cert record deleted; the domain's `ssl` flag flips to no. The HTTPS endpoint stops working until a replacement is installed. Removing a Let's Encrypt cert does NOT revoke at the CA — see [[settings-ssl-troubleshooting]].

## Related

- [[settings]] — parent hub.
- [[settings-domains]] — the parent page that hosts the per-domain **SSL** action; DNS and primary-domain rules live there.
- [[apps-lets-encrypt]] — the paid app that powers Automatic install + auto-renewal.
- [[settings-general]] — provides defaults for Organization, Email, Country, Locality on the manual-install CSR form (see [[settings-ssl-manual-install]]).
- [[settings-admin-notifications]] — controls whether expiry / fallback alerts are emailed to the merchant (see [[settings-ssl-expiry-fallback]]).
- [[apps]] — the apps catalog where the merchant browses and installs the Let's Encrypt Manager app.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — `ssl_certificate` is a plan-gated feature.
- [[settings-staff]] — moderator permission grants (same as Domains).

## Open questions

_None._
