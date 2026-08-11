---
type: feature
nav_path: "Settings → Domains"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Domains", "Custom domains", "Domain management", "SSL", "DNS", "Домейни", "Custom URL", "ДНС"]
tags: [settings, domains, ssl, dns, cloudflare, namecom]
plan_gates: ["domains", "custom_hostname"]
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---

# Domains

## Purpose

The screen where the merchant manages all custom domains pointing at their CloudCart store: the always-present CloudCart subdomain (e.g., `mystore.cloudcart.net`), zero or more **externally-owned** domains the merchant adds and verifies via DNS, and zero or more **CloudCart-purchased** domains bought directly through this page via the integrated Name.com reseller flow. For every domain the merchant can: designate one as the **primary** (canonical storefront URL), toggle active/inactive, edit DNS records via the **Cloudflare**-managed zone, install / inspect / replace the **SSL certificate** (free via Let's Encrypt or external), update WHOIS contact info, see expiration / renewal status, and remove the domain.

CloudCart's domain stack on this page:

- **Cloudflare** — managed DNS + DDoS protection. Two modes depending on add path: a standard zone (full DNS control) or **Cloudflare for SaaS** Custom Hostname (merchant keeps DNS, only a CNAME points to CloudCart). See [[settings-domains-dns-cloudflare]].
- **Name.com registrar** — powers the "Buy a domain" search and checkout flow. See [[settings-domains-add-flow]].
- **Let's Encrypt** — free, automated SSL via the `lets_encrypt` app. External certs supported but the merchant manages renewal. See [[settings-domains-ssl]].
- **CNAME plan feature** — paid plan-feature pack controlling how many CNAME-style domains the merchant can attach; shown as the "Other domains" usage chip. See [[settings-domains-plan-gates]].

## Where to find it

Sidebar → Settings → **Domains**. Breadcrumb: "Settings → Domains". Route: `/admin/settings/domains`. Globe icon. Only Vue version (no modern `-new` counterpart yet).

## What the merchant can do here

### Page header
- **Primary domain card** at top with "Primary" badge.
- **"Other domains" section** with additional attached domains.
- **+ Add domain** opens the Add New Domain modal — see [[settings-domains-add-flow]].
- **CNAME usage chip** (e.g., `2 of 3 CNAME slots used`) — see [[settings-domains-plan-gates]].

### Per-domain row actions
- **Activate / deactivate** toggle (primary cannot be deactivated).
- **Set as primary** — confirmation modal + hard redirect on success. See [[settings-domains-primary]].
- **SSL** — opens the SSL Modal. See [[settings-domains-ssl]] + [[settings-ssl]].
- **Manage DNS** — nameserver instructions while pending, records table once active. See [[settings-domains-dns-cloudflare]].
- **Renew** — for CloudCart-purchased domains within 30 days of expiry. See [[settings-domains-add-flow]].
- **WHOIS contacts edit** — for CloudCart-purchased domains. See [[settings-domains-add-flow]].
- **Remove** — see [[settings-domains-deletion]] (asymmetric for external vs CloudCart-purchased).

### Empty state
No custom domains beyond the CloudCart subdomain: centered "Add domain" CTA.

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one slice. The Assistant should drill into the matching aspect rather than read every page.

- [[settings-domains-add-flow]] — Add New Domain modal: "Add existing" + "Buy new" sub-flows, WHOIS / ICANN, IDN domains, renewal warning, no inbound-transfer path.
- [[settings-domains-dns-cloudflare]] — Cloudflare zones vs Cloudflare for SaaS Custom Hostnames; the Manage DNS modal (pending vs active); the orange-cloud Proxy toggle and what records get force-overridden; auto-set DKIM / SPF / DMARC for hosted email.
- [[settings-domains-ssl]] — Let's Encrypt vs external SSL; auto-renewal at 25 days; the daily SSL expiry sweep + primary fallback to `*.cloudcart.net`; `DeletedCertificate` paper trail.
- [[settings-domains-primary]] — single-canonical-URL rule; set-as-primary verification gates (DNS / SSL / Powered-by-CloudCart header check at `/.well-known/acme-challenge/_selftest`); hard redirect on switch.
- [[settings-domains-deletion]] — deletion safety (primary cannot be deleted); asymmetric behaviour for external vs CloudCart-purchased; model-boot cleanup hooks; `hosts` table is platform-wide unique.
- [[settings-domains-plan-gates]] — `domains` numeric quota + `custom_hostname` numeric quota and access whitelist (cc-pro + unicorn only); CNAME usage chip; PlanFeature modal upsell; Activation modal's two methods.

## Settings & fields

### Per-domain row — visible columns

| Column | What the merchant sees |
|--------|------------------------|
| **Domain hostname** | E.g., `mystore.bg` or `mystore.cloudcart.net`. |
| **Primary badge** | Shown on the one designated primary domain. |
| **Active toggle** | On = serves customers; off = inactive (preserved but not serving). |
| **Source badge** | "External" (merchant brought it) or "CloudCart" (purchased here). |
| **DNS status** | Pending (nameservers not yet pointing) / Active (Cloudflare zone live, DNS editable). |
| **SSL badge** | Free (Let's Encrypt, auto-renewing) / External (manual renewal required). |
| **Expiry date** | For CloudCart-purchased domains; shows renewal warning within 30 days. |
| **Row actions** | Set as primary, Manage DNS, Manage SSL, Activate / Deactivate, Remove. |

### CNAME usage chip

Page header chip in the form `<used> of <limit> external domains` — shown when the CNAME plan-feature is in use. See [[settings-domains-plan-gates]].

## Business rules

### "External" vs "CloudCart-purchased" domains

- **External** (`external=yes`): merchant brought the domain from another registrar (GoDaddy, Namecheap, etc.). They change nameservers to point at CloudCart's Cloudflare nameservers. CloudCart does NOT manage renewal — the merchant keeps paying their original registrar.
- **CloudCart-purchased** (`cloudcart=1`, `purchase_namecome=1` after transform): bought through the Buy a domain flow via Name.com. CloudCart handles renewal billing through the merchant's plan subscription. Merchant gets `for_renew=true` warnings 30 days before expiry.

This distinction drives downstream rules — see [[settings-domains-deletion]] (asymmetric delete) and [[settings-domains-add-flow]] (renewal + WHOIS edit only for CloudCart-purchased).

### CloudCart subdomain is fixed at signup

The store's `*.cloudcart.net` subdomain is assigned at store creation and is NOT editable anywhere in the admin panel. Renaming requires CloudCart support intervention. Workaround for merchants wanting a different storefront URL: buy or attach a custom domain and set it as primary — the CloudCart subdomain stays as a permanent fallback URL.

### Side effects on save

- DNS edits propagate immediately (storefront reflects the change within seconds).
- Adding / removing a domain triggers a platform-wide cleanup of cached primary-host references.
- Setting a new primary domain triggers a **hard redirect** — see [[settings-domains-primary]].

### Permissions

Requires the Domains permission section. Moderators without the `settings.domains` grant from [[settings-staff]] do not see this entry in the sidebar.

### Common errors

| Error | What it means |
|---|---|
| *"Invalid domain headers"* | External domain set-as-primary attempted but DNS doesn't yet point at CloudCart. Wait for propagation (up to 48h) or fix nameservers. See [[settings-domains-primary]]. |
| *"Domain already exists"* / *"Domain already exists in system"* | Already attached to another CloudCart store. Platform-wide uniqueness — see [[settings-domains-deletion]]. |
| *"Plan limit reached"* | Exceeded external-domain quota. Upgrade plan or buy a slot. See [[settings-domains-plan-gates]]. |
| DNS edit failures | Transient DNS service issues. Retry; if persistent, contact support. |
| Domain purchase failed | Payment declined, insufficient funds, or restricted TLD. See [[settings-domains-add-flow]]. |

## Related

- [[settings]] — parent hub.
- [[settings-general]] — store URL and operation country are influenced by the primary domain.
- [[settings-cart]] — checkout URL uses the primary domain.
- [[settings-ssl]] — companion SSL screen; opened from row's Manage SSL action.
- [[apps-lets-encrypt]] — the app that provisions the free SSL certificates used here.
- [[plan]] — the plan controls how many external domains the merchant can attach.
- [[plan-gates]] — concept page on plan-based feature gating.
- [[plan-vs-feature-pack]] — pack-checkout flow used to buy additional CNAME slots.
- [[settings-backups]] — additional-slot purchase flow follows the same pack-checkout UX as domains.
- [[settings-staff]] — `settings.domains` permission grant.
- [[settings-admin-notifications]] — gates the SSL-expiry alerts emitted by the daily sweep.
- [[domain]] — entity page.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
