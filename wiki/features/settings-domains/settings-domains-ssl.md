---
type: feature
nav_path: "Settings → Domains → SSL"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["SSL modal", "Manage SSL", "Install SSL", "Let's Encrypt SSL", "External SSL", "SSL auto-renewal", "SSL expiry fallback", "DeletedCertificate", "SslSitesCommand"]
tags: [settings, domains, ssl, lets-encrypt, certificates]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, primary, deletion, plan gates).

# Domains — SSL provisioning and renewal

## Purpose

How the merchant inspects, installs, and replaces SSL certificates on attached domains — and what happens automatically when a certificate is about to expire or has expired. Two modes: free **Let's Encrypt** certificates (auto-provisioned and auto-renewed by the `lets_encrypt` app) and **external** certificates the merchant uploads themselves (renewal is the merchant's responsibility). This page focuses on the per-domain SSL Modal opened from the row's **Manage SSL** action and the daily platform-wide expiry sweep. The standalone SSL admin screen is documented separately at [[settings-ssl]].

## Where to find it

Settings → Domains → per-domain row → **SSL** (or **Manage SSL** / **Install SSL**) action button. Opens the SSL Modal showing certificate details and install / replace controls.

## What the merchant can do here

- **Inspect the current certificate** — issuer, expiry date, and whether it's free (Let's Encrypt, auto-renewing) or external (merchant-managed).
- **Install a new certificate** — opens the modal in install mode with two tabs: **Automatic** (Let's Encrypt — generates a fresh cert via ACME) and **Manual** (upload the certificate + private key + intermediate chain).
- **Replace an existing certificate** — only after **Remove**: both install tabs work only on a domain with no certificate ([[settings-ssl-manual-install]]). Replacing a Let's Encrypt cert with an external one ends auto-renewal for this domain; the reverse restores it.

Full SSL screen behaviour (both "Manage existing cert" mode and "Install new" mode) is documented at [[settings-ssl]].

## Settings & fields

| Field / Label | Meaning |
|---|---|
| **Issuer** | The certificate authority — usually "Let's Encrypt" for free certs or the merchant's CA for uploaded ones. |
| **Expiry date** | When the certificate's `valid_to` falls. |
| **Managed by Let's Encrypt** | Label shown for the free, auto-renewing certs. |
| **Managed by external provider. You should change it manually before the expiration date.** | Label shown for merchant-uploaded certs — no auto-renewal. |

## Business rules

### SSL provisioning when a domain is added

**Nothing is issued when a domain is added** (Add existing or Buy new — [[settings-domains-add-flow]]). The merchant installs a certificate from the row's **Install SSL** link (before the DNS is Active it carries the hint *"To secure your domain, first set up DNS records."*):

1. **Automatic install** issues a free Let's Encrypt certificate on that click; it needs the paid Let's Encrypt Manager app ([[apps-lets-encrypt]]) and is then auto-renewed by the daily sweep (below).
2. **Manual install** takes an **external SSL** (e.g., a paid wildcard cert). **CloudCart does NOT renew external certs** — the merchant must replace them before expiry or the storefront breaks with browser security warnings.

The SSL modal clearly labels which mode the current certificate is in: *"Managed by Let's Encrypt"* or *"Managed by external provider. You should change it manually before the expiration date."*

### Let's Encrypt auto-renewal sweep — 25 days before expiry

A daily platform-wide sweep renews Let's Encrypt certificates whose `valid_to < now + 25 days`. It skips inactive domains, stores whose plan has expired, and stores whose Let's Encrypt Manager subscription is unpaid (error *"Renew error: no active subscription"*). This is INDEPENDENT of the **domain registration** renewal warning (which surfaces at 1 month before `expire_date` for CloudCart-purchased domains — see [[settings-domains-add-flow]]).

A merchant whose domain has 28 days till **registration** expiry sees the renewal CTA but no SSL action is triggered yet (the cert renew sweep activates at 25 days).

### SSL certificate expiry — automatic fallback + admin alert

The same daily sweep also handles expired certificates on active domains (stores whose plan has expired are skipped). A different, staff-run command, `hosts:deactivate-expired`, deactivates the custom domains of stores whose plan has expired; it is not part of the SSL sweep.

When a domain's certificate expires:

- If the expired domain was the **primary** of its store, the platform switches the primary back to the store's `*.cloudcart.net` main host so the storefront keeps serving (with a HTTPS-warning-free CloudCart-managed cert), and the custom domain is deactivated. The merchant sees an alert: *"The SSL certificate for domain X is expired. Switched to main host: <mystore.cloudcart.net>."*
- If the expired domain was a non-primary additional domain, it is simply deactivated. Alert: *"The SSL certificate for domain X is expired. Domain is deactivated."*

These alerts surface in the admin notification panel (Let's Encrypt app namespace) and are flagged as `allow_send_notification=true`, so the merchant also gets an email/notification per the [[settings-admin-notifications]] gates.

For free Let's Encrypt certificates the auto-renewal sweep usually keeps them current, so this fallback should fire only when renewal is blocked (e.g., the domain no longer points at CloudCart, or DNS verification fails). For external (paid) certificates the merchant supplied themselves, this fallback is the merchant's main signal that they forgot to upload a renewed cert before expiry.

### `DeletedCertificate` paper trail

When a Certificate model is deleted (via the SSL modal Remove button or otherwise), a row is inserted into a `deleted_certificates` table recording the site_id and domain. When a new certificate is later created for the same site/domain pair, that record is deleted. Effect: there's an internal audit trail of cert removal/reinstallation that CloudCart support can consult, but it's not exposed to the merchant in the UI.

### SSL issuance — apex + `www` variant both go in the SAN

The Let's Encrypt issuance path tries BOTH `<host>` and `www.<host>` (including the apex+www variants in the certificate SAN). This means a single cert covers both forms — the merchant doesn't need to add two domains for `example.com` and `www.example.com` to get HTTPS on both. The same Powered-by-CloudCart header check that runs during set-as-primary (see [[settings-domains-primary]]) is also used during issuance.

### HTTPS redirect follows the certificate

A domain with an installed certificate is served over https: a plain-http request gets a 301 to the https address (302 in the admin), on every path except `/.well-known/acme-challenge/` and payment callbacks. A domain with no certificate (never installed, or removed) is served over plain http, and an https request to it is redirected to http the same way. `*.cloudcart.net` addresses are always https. On a non-primary domain the redirect goes straight to the primary ([[settings-domains-primary]]).

### SSL must be installed before set-as-primary

Setting a domain as primary requires a valid SSL certificate in place — see [[settings-domains-primary]] for the verification gates. If no certificate is installed, the confirmation modal redirects the merchant into the SSL Modal to install one first.

## Related

- [[settings-domains]] — hub.
- [[settings-ssl]] — the full standalone SSL screen documentation (Manage / Install modes, Automatic / Manual tabs).
- [[apps-lets-encrypt]] — the app that provisions the free SSL certificates.
- [[settings-domains-primary]] — the set-as-primary gate that requires an installed SSL.
- [[settings-domains-add-flow]] — domain-registration renewal warning (different from SSL renewal).
- [[settings-domains-deletion]] — domain delete also cascades the certificate row.
- [[settings-admin-notifications]] — gates the SSL-expiry alerts.

## Open questions

None.
