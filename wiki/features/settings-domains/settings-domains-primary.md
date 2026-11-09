---
type: feature
nav_path: "Settings → Domains → Primary domain"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Primary domain", "Set as primary", "Canonical URL", "Invalid domain headers", "Powered-by-CloudCart check", "Hard redirect on primary switch"]
tags: [settings, domains, primary, canonical, redirect]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, SSL, deletion, plan gates).

# Domains — Primary domain (canonical URL)

## Purpose

Every CloudCart store has exactly one **primary** domain — the canonical URL that customers see in the address bar and that the storefront emits in `<link rel="canonical">`, sitemaps, and outbound emails. This page covers the single-canonical-URL rule, the **set-as-primary verification gates** (DNS pointing, SSL provisioned, Powered-by-CloudCart header check), the redirect cascade for non-primary domains, and the hard SPA reload that happens when the merchant switches primary because session cookies are domain-scoped.

## Where to find it

Settings → Domains → per-domain row → **Set as primary** action. Currently only one row in the table can carry the **Primary** badge.

## What the merchant can do here

- See which domain is currently primary — visible at the top of the list with a **"Primary"** badge on the primary domain card.
- **Set another domain as primary** — opens *"Set {domain} as your primary domain?"* (*"Are you are sure you want to set this domain as a primary?"*). On confirm, the platform verifies the gates below and either:
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

1. **DNS pointing correctly** — while the domain's zone is missing or not Active, the admin shows *"Please set your DNS Records before making the domain primary!"* with a **Manage DNS** button. See [[settings-domains-dns-cloudflare]].
2. **SSL provisioned** — with no certificate it shows *"You need to install SSL first, for making this domain as a primary!"* and opens the SSL modal. The server refuses with *"No SSL found"*, *"Invalid certificate expiring date"* or *"The SSL certificate has expired on: <date>"*. See [[settings-domains-ssl]].
3. **Powered-by-CloudCart header check** — for domains other than `*.cloudcart.net`, the server requests `http://<host>/.well-known/acme-challenge/_selftest` (plain http) and needs a response header whose value is exactly `cloudcart.com`, which in practice is CloudCart's `x-powered-by: cloudcart.com`. The Let's Encrypt check reads `x-powered-by` itself, so the two agree. If it fails: *"Invalid domain headers"*. The same check runs when **Domain active** is switched on.

When the store has CNAME slots, **Set as primary** goes straight to the confirmation and these server checks decide, since a CNAME-mode domain has no zone to show as Active ([[settings-domains-external-dns]]).

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

### Non-primary domains redirect to the primary

A request that arrives on any other of the store's domains, its `*.cloudcart.net` address included, is answered with a **301 to the same path and query string on the primary domain** (the admin panel uses a 302), so search engines consolidate signal on one URL. This is automatic platform behaviour, not a setting: it runs before any page loads, so it covers every storefront page, including cart and checkout (payment-provider callback and return addresses are exempt). The merchant can have many non-primary domains all redirecting to the primary if they own multiple TLD variants (`mystore.com`, `mystore.bg`, `mystore.eu`).

The target is always this store's own **Active** primary, which must already be served by CloudCart (the *"Invalid domain headers"* check), so this cannot forward a domain to a site hosted elsewhere — see [[seo-301-redirects-types]]. [[apps-domain-redirect]] is a different thing: country-based routing between the merchant's own stores.

If an Active primary stops resolving (for example its registration lapsed), the other addresses keep redirecting to it until it is deactivated, the admin panel included (302), so the merchant cannot reach **Set as primary**. The `*.cloudcart.net` address has no gates, and switching the primary back to it from CloudCart's side restores the store at once.

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
- [[marketing-seo-301-redirects]] — per-URL 301 rules.
- [[apps-domain-redirect]] / [[apps-domain-redirect-settings]] — own-stores geo-routing (not the automatic non-primary → primary redirect).

## Open questions

None.
