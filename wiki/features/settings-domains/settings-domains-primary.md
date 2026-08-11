---
type: feature
nav_path: "Settings → Domains → Primary domain"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Primary domain", "Set as primary", "Canonical URL", "Invalid domain headers", "Powered-by-CloudCart check", "Hard redirect on primary switch"]
tags: [settings, domains, primary, canonical, redirect]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, SSL, deletion, plan gates).

# Domains — Primary domain (canonical URL)

## Purpose

Every CloudCart store has exactly one **primary** domain — the canonical URL that customers see in the address bar and that the storefront emits in `<link rel="canonical">`, sitemaps, and outbound emails. This page covers the single-canonical-URL rule, the **set-as-primary verification gates** (DNS pointing, SSL provisioned, Powered-by-CloudCart header check), the redirect cascade for non-primary domains, and the hard SPA reload that happens when the merchant switches primary because session cookies are domain-scoped.

## Where to find it

Settings → Domains → per-domain row → **Set as primary** action. Currently only one row in the table can carry the **Primary** badge.

## What the merchant can do here

- See which domain is currently primary — visible at the top of the list with a **"Primary"** badge on the primary domain card.
- **Set another domain as primary** — opens the `ConfirmModal` (*"Set as primary? — This will change the canonical URL of your store. You will be redirected to the new URL."*). On confirm, the platform verifies the gates below and either:
  - Switches the primary, triggers the hard redirect, and reloads the admin SPA on the new domain; OR
  - Surfaces a guidance modal pointing the merchant to fix whichever gate failed.

## Settings & fields

| Field | Meaning |
|---|---|
| `is_primary` (per host) | Boolean; exactly one host per store has `is_primary=true`. |
| Primary badge | UI indicator on the row of the current primary. |

## Business rules

### Single canonical URL

Only one domain can be `is_primary=true` at a time. Setting another domain as primary auto-unsets the previous primary. The primary domain CANNOT be:

- Deactivated (the Active toggle is disabled).
- Deleted (see [[settings-domains-deletion]] — primary must be reassigned first).

### Set-as-primary — the three verification gates

When the merchant tries to set a domain as primary, the platform checks three conditions and opens the relevant guidance modal if any fails:

1. **DNS pointing correctly** — if the domain's Cloudflare DNS zone isn't yet active, the merchant is taken to the DNS management modal to finish the nameserver change. See [[settings-domains-dns-cloudflare]]. ConfirmModal payload: `noDnsPrimarySet`. Modal title *"Invalid domain headers"* with message *"Your domain doesn't point at CloudCart. Fix the DNS first."*
2. **SSL provisioned** — if no valid SSL certificate is in place, the merchant is taken to the SSL modal to install one. ConfirmModal payload: `installSSLForPrimarySet`. Modal title *"Install SSL"* with message *"This domain needs a valid SSL certificate before it can be the primary."* — clicking OK opens the SSL modal. See [[settings-domains-ssl]].
3. **Powered-by-CloudCart header check** — for externally-owned domains, the platform performs a live HTTP GET to `https://<host>/.well-known/acme-challenge/_selftest` and looks for the string `cloudcart.com` in **any response header** (not specifically `x-powered-by`). If the domain doesn't actually point at CloudCart, the check fails with *"Invalid domain headers"* and the merchant is taken to the DNS modal.

If the merchant's `cnameFeature` quota is exhausted at the moment they try to set-as-primary on a CNAME-mode domain, the ConfirmModal opens with the `manageDnsWithPaidCNAME` payload instead — routing to the `PlanFeature` panel. See [[settings-domains-plan-gates]].

### Powered-by header check — single ~5-second timeout, no retry

The header check is a single ~5-second timeout request — if the domain is slow or unreachable, the check fails with no retry. Practical implication: if the merchant just finished a nameserver change, the DNS may have propagated to some resolvers but not others. **Retrying after a few minutes often succeeds.**

The same header check is also performed during Let's Encrypt certificate issuance — and there it tries BOTH `<host>` and `www.<host>`, including the apex+www variants in the certificate SAN. See [[settings-domains-ssl]].

### Hard redirect on primary switch — admin SPA reloads

Setting a new primary causes a **hard redirect** — the admin page reloads on the new domain's URL because admin session cookies are scoped to a specific domain. From the merchant's perspective: they click confirm, the browser navigates away, the new domain loads, and they may need to re-confirm their session if cookies weren't migrated. This is by design — the admin SPA cannot stay on the old domain after primary switch because storefront/checkout/email flows will all start emitting the new primary URL.

### Side effects on save

- DNS edits propagate immediately (the merchant sees the change live on the storefront within seconds).
- Adding / removing a domain triggers a platform-wide cleanup of cached primary-host references.
- Setting a new primary domain triggers a **hard redirect** (the admin page reloads on the new domain's URL).
- Outbound email templates, sitemaps, canonical tags, and webhook payloads start emitting the new primary URL on subsequent requests / cron runs.

### Non-primary domains continue to serve

Non-primary domains that are still **Active** continue to be served by CloudCart — they typically 301-redirect to the canonical primary so search engines consolidate signal on one URL. See [[apps-domain-redirect]] / [[apps-domain-redirect-settings]] for the configurable redirect-behaviour app. The merchant can have many non-primary domains all redirecting to the primary if they own multiple TLD variants (`mystore.com`, `mystore.bg`, `mystore.eu`).

### "Invalid domain headers" — what to tell the merchant

When the merchant sees *"Invalid domain headers"* the cause is almost always one of:

- The DNS just changed and hasn't propagated to the resolver the platform's check used. **Retry after a few minutes.**
- The merchant added the domain but never completed the nameserver change. **Open Manage DNS and follow Step 1 + Step 2.**
- The merchant pointed the domain at a different host (not CloudCart) by mistake. **Verify the nameservers at the registrar.**

## Related

- [[settings-domains]] — hub.
- [[settings-domains-dns-cloudflare]] — the DNS gate; Manage DNS modal that the failed gate redirects into.
- [[settings-domains-ssl]] — the SSL gate; install-SSL flow.
- [[settings-domains-deletion]] — primary cannot be deleted; reassign first.
- [[settings-general]] — store URL field that derives from the primary.
- [[settings-cart]] — checkout URL uses the primary.
- [[marketing-seo-canonical]] — `<link rel="canonical">` emission downstream.
- [[marketing-seo-sitemap]] — sitemap URLs derive from the primary.
- [[marketing-seo-301-redirects]] / [[apps-domain-redirect]] / [[apps-domain-redirect-settings]] — redirect of non-primary domains to the primary.

## Open questions

None.
