---
type: feature
nav_path: "Settings → Domains → SSL → Expiry & fallback"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["SSL expiry fallback", "SSL primary fallback", "Certificate expired switch", "Domain deactivation on expiry", "SSL fallback to cloudcart.net"]
tags: [settings, ssl, certificate, expiry, fallback, domains, alerts]
plan_gates: ["ssl_certificate"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-ssl]]. See the hub for the other aspects (automatic install, manual install, auto-renewal, edge propagation, troubleshooting).

# SSL — Certificate expiry and automatic fallback

## Purpose

When a certificate actually **expires** (not just enters the renewal window — see [[settings-ssl-auto-renewal]] for that), the platform takes automatic remediation so the storefront stays serving. The exact remediation depends on whether the expired cert covers the store's **primary domain** or a **non-primary** domain.

This page documents the daily expired-cert sweep, the primary-domain fallback to the CloudCart subdomain, the non-primary deactivation behaviour, the admin alerts that fire, and the merchant's recovery path.

## Where to find it

There is no direct UI for the fallback mechanism — it runs automatically. What the merchant CAN see and act on:

- Admin notifications panel — the expiry alert is surfaced there.
- Email notifications — depending on [[settings-admin-notifications]] gating.
- The domain's row in [[settings-domains]] — a deactivated domain shows its inactive state there.
- The SSL modal — opening it for the affected domain shows no cert installed (the merchant can then install a new one).

## What the merchant can do here

### React to an expiry alert

Recovery depends on the cert type:

- **Let's Encrypt cert** (rare — usually means DNS broken ≥ 25 days, or store billing `not_paid`): fix the underlying issue (DNS, billing, or `lets_encrypt` app subscription); re-activate the domain in [[settings-domains]] if deactivated; re-issue via [[settings-ssl-automatic-install]]; if the domain was previously primary, re-set it as primary.
- **Manual external cert** (merchant forgot to renew): obtain a renewed cert from the CA; re-run the full Manual install flow ([[settings-ssl-manual-install]]); re-set as primary if needed.

### Understand the alerts

Two distinct alert strings (rendered in the admin notifications panel; emailed depending on the merchant's [[settings-admin-notifications]] preferences):

- Primary-domain expiry: *"The SSL certificate for domain X is expired. Switched to main host: {mystore.cloudcart.net}."*
- Non-primary expiry: *"The SSL certificate for domain X is expired. Domain is deactivated."*

### Use the CloudCart subdomain while resolving

The storefront keeps serving via the `*.cloudcart.net` subdomain (platform-managed wildcard cert — see [[settings-ssl-edge-propagation]]). Customers visiting the original custom domain will see the browser's HTTPS warning until the cert is re-installed or the custom domain is removed.

## Settings & fields

This aspect does not have dedicated form fields — the behaviour is automatic. The relevant per-domain fields are:

| Field | Where it lives | What it shows |
|-------|----------------|---------------|
| Domain `is_active` flag | [[settings-domains]] row | `false` after fallback fires for that domain. |
| Store `primary` domain | [[settings-domains]] | Switched back to `*.cloudcart.net` when the primary's cert expired. |
| Cert record | (cleared) | Removed from the domain on fallback. |
| Alert text | Admin notifications panel | One of the two strings above. |

## Business rules

### Daily expired-cert sweep

A platform-wide daily sweep finds expired certificates and runs the fallback. This is a SEPARATE sweep from the renewal sweep covered in [[settings-ssl-auto-renewal]] — that one targets certs in the 25-day pre-expiry window for renewal; this one targets certs that have actually crossed `validTo` without successful renewal.

### Primary-domain fallback — switch to `*.cloudcart.net`

If the expired cert's domain is the **primary** domain of its store:

- The platform switches the store's primary back to the `*.cloudcart.net` subdomain.
- The custom domain is **deactivated**.
- Alert text: *"The SSL certificate for domain X is expired. Switched to main host: {mystore.cloudcart.net}."*

Effect on customers: the storefront serves via the subdomain (which has a valid platform-managed wildcard cert). Bookmarks and SEO referring to the custom domain may break until the merchant re-installs and re-sets as primary.

### Non-primary fallback — domain just deactivated

If the expired cert's domain is **NOT** the primary domain:

- The domain is just deactivated. No primary switch.
- Alert text: *"The SSL certificate for domain X is expired. Domain is deactivated."*

The storefront continues to serve from the still-valid primary domain (or its `*.cloudcart.net` fallback if the primary is also broken).

### When this should and shouldn't fire

- **Let's Encrypt cert** — only fires when renewal was blocked for ≥ 25 days (DNS broken, billing `not_paid`, app subscription lapsed). For a healthy cert the daily renewal sweep ([[settings-ssl-auto-renewal]]) keeps `validTo` rolling forward and this expiry sweep never acts.
- **Manual external cert** — fires whenever the merchant forgets to replace before expiry; the merchant's signal to renew via [[settings-ssl-manual-install]].

### Alerts route through admin-notifications gating

Whether the alert is emailed depends on the notification-types toggles configured in [[settings-admin-notifications]]; the admin notifications panel shows it regardless.

### Recovery — re-activate the domain after re-installing

After the merchant successfully re-installs a cert via the SSL modal:

- The cert record is restored on the domain.
- The domain's `is_active` flag is NOT automatically flipped back to true — the merchant must re-activate it in [[settings-domains]] (`(verify)` — automatic vs manual re-activation may depend on whether the domain was deactivated only for SSL or for other reasons too).
- If the merchant wants the domain back as primary, they must explicitly re-set it as primary in [[settings-domains]].

### The CloudCart subdomain wildcard cert cannot expire from the merchant's perspective

The `*.cloudcart.net` subdomain wildcard cert is rotated by CloudCart's platform team via separate infrastructure. From the merchant's perspective it is always valid — which is exactly why falling back to it keeps the storefront serving without HTTPS warnings. See [[settings-ssl-edge-propagation]].

### Removing a cert does NOT pre-emptively trigger fallback

If the merchant manually clicks **Remove** (with confirm *"Are you sure you want to remove it?"*), the cert record is deleted and HTTPS stops working for the domain. The platform does NOT auto-fall-back the primary on user-initiated Remove — only on the daily expired-cert sweep. A merchant who Removes a cert from their primary domain has a broken storefront on that domain until they install a replacement or re-set another (still-certed) domain as primary. `(verify)` whether the Remove confirm warns about primary impact.

## Related

- [[settings-ssl]] — hub.
- [[settings-domains]] — where deactivated domains are visible and re-activated; where the primary domain is re-set.
- [[settings-admin-notifications]] — controls whether the expiry alert is emailed in addition to the notifications panel.
- [[settings-ssl-auto-renewal]] — the upstream sweep that SHOULD prevent expiry from ever firing for healthy Let's Encrypt certs.
- [[settings-ssl-manual-install]] — recovery path for an expired external cert.
- [[settings-ssl-automatic-install]] — recovery path for an expired Let's Encrypt cert (after fixing the underlying issue).

## Open questions

- After re-installing a cert on a previously-deactivated domain, is the domain auto-re-activated or does the merchant have to manually re-activate via [[settings-domains]]? `(verify)`
- Does the SSL Modal's Remove confirm warn if the cert being removed is on the merchant's primary domain (a destructive removal that breaks the storefront)? `(verify)`
