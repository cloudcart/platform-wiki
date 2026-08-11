---
type: entity
aliases: ["Domain", "Custom domain", "Hostname", "URL", "Domain name", "Site domain", "Storefront domain", "Домейн", "Адрес на магазина", "Custom URL"]
tags: [settings, apps, domains, ssl, dns, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Domain

## Identity

A **Domain** is a hostname attached to the merchant's [[site|Site]] — a custom domain the merchant brought from an external registrar (`mystore.bg`), a custom domain bought through CloudCart's integrated reseller flow (also `mystore.bg`, registered through CloudCart on the merchant's behalf), or the always-present `<handle>.cloudcart.net` platform-provided subdomain assigned at Site signup. Domains are the **front-door identifiers**: when a customer types a URL or clicks a link, the platform's hostname-resolution layer matches the request's `Host` header against the Domain rows to find which Site to serve.

A Site can have **multiple Domains attached** — exactly one is the **primary** (the canonical storefront URL all marketing and SEO points at), and the others are **aliases** that 301-redirect to the primary so customers and search engines converge on a single canonical URL. Each Domain carries its own **SSL certificate** (required for HTTPS — without it modern browsers refuse to load the site or show a red warning). SSL has two modes: **automatic** via the Let's Encrypt Manager app ([[apps-lets-encrypt]]), or **manual** where the merchant pastes an externally-obtained cert into the SSL modal on [[settings-ssl]].

The number of custom Domains the merchant can attach is **plan-gated** by the `cname` / `custom_hostname` plan-features (visible as the "Other domains" usage chip in the [[settings-domains]] header). Beyond the quota, the merchant either upgrades their [[plan|Plan]] or buys an additional external-domain slot. A Domain is distinct from a [[site|Site]] (a Site can have many Domains; a Domain belongs to exactly one Site) and distinct from a **CMS page URL** (the customer-facing path under a Domain, e.g., `mystore.bg/products/red-shoes` — managed via [[seo-meta]] / page settings, not via [[settings-domains]]).

## Aliases

- **Domain** — the canonical merchant-facing term in the admin UI ("Settings → Domains").
- **Custom domain** — emphasises the merchant-owned domain vs the platform-provided `<handle>.cloudcart.net` fallback.
- **Hostname** — technical phrasing used in DNS / SSL contexts.
- **URL** / **Domain name** — informal phrasings used in support tickets.
- **Site domain** / **Storefront domain** — emphasises the binding to a specific [[site|Site]].
- Bulgarian: **Домейн** (standard), **Адрес на магазина** (older / merchant-facing), **Custom URL** (Bulgarian admin sometimes mixes English).

## Key Attributes

The Domain record is multi-faceted and split across **six well-scoped aspects**. The AI Assistant should drill into the aspect that matches the question, not read every page.

- [[domain-attributes]] — the per-field schema (hostname, is_primary, active toggle, source, DNS status, SSL status, SSL mode, expiry dates, Cloudflare IDs, WHOIS contact, attached / DNS-validated timestamps) + the special properties of the always-present `<handle>.cloudcart.net` subdomain.
- [[domain-relationships]] — what a Domain links to (Site, Plan, SSL certificate, Cloudflare zone or Custom Hostname binding, the platform code middleware, admin alerts, admin cookies) and what it does NOT link to (cancellation of registrar registration, per-staff permissions, cloning across Sites).
- [[domain-lifecycle]] — the 7 phases: Attached (pending DNS) → Active → SSL provisioning → Designated as primary → Renewal warning (CloudCart-purchased) → SSL expiry triggers admin alert + fallback → Removed.
- [[domain-ssl]] — the two mutually-exclusive SSL modes (Let's Encrypt auto vs external manual), switching mode requires Remove + reinstall, daily expiry sweep + automatic fallback to `<handle>.cloudcart.net`, IDN certificates use Punycode.
- [[domain-dns-cloudflare]] — DNS records modal (A, AAAA, CNAME, MX, TXT, NS), per-record Cloudflare Proxy toggle (orange cloud vs grey cloud), the two platform-chosen Cloudflare modes (standard zone vs Custom Hostname / SaaS), hosted-email auto-configures MX + SPF + DKIM + DMARC.
- [[domain-primary-and-plan-gates]] — exactly one primary per Site, set-as-primary verification gates (DNS + SSL + Powered-by header), hard redirect on primary change, external vs CloudCart-purchased billing models, `cname` / `custom_hostname` plan quota, deletion side effects, IDN support.

## Why it matters to the merchant

The Domain record is where **front-door identity, HTTPS security, DNS infrastructure, and plan-feature gating** intersect. Five high-impact behaviours the merchant should understand:

- **Exactly ONE primary per Site**, and switching it triggers a **hard redirect** because admin session cookies are scoped to a specific Domain — the admin SPA reloads on the new URL. See [[domain-primary-and-plan-gates]].
- **SSL is mandatory for HTTPS**, has two modes (auto via Let's Encrypt vs manual external), and Let's Encrypt is auto-renewed while external certs are merchant-managed. A daily sweep finds expired certs and automatically falls back to `<handle>.cloudcart.net` so the storefront keeps serving. See [[domain-ssl]].
- **External vs CloudCart-purchased domains have different billing models.** External merchants pay their original registrar; CloudCart-purchased domains renew through the merchant's plan subscription and show a 30-day-before-expiry warning. See [[domain-primary-and-plan-gates]].
- **The `<handle>.cloudcart.net` subdomain is always present** — assigned at Site signup, non-removable, non-deactivatable, and serves as the permanent fallback. See [[domain-attributes]].
- **Plan-gated quota** controls how many external Domains the merchant can attach via the `cname` / `custom_hostname` feature, displayed as the "Other domains" usage chip. See [[domain-primary-and-plan-gates]].

## Where it appears

- [[settings-domains]] — the master management screen. Add / remove Domains; designate primary; toggle Active; manage DNS; manage SSL; buy new domain; WHOIS contact edits; renewal warnings.
- [[settings-ssl]] — per-Domain SSL certificate management (Install / Manage / Remove / Regenerate CSR).
- [[settings-general]] — store URL and operation country are influenced by the primary Domain.
- [[settings-cart]] — checkout URLs are generated against the primary Domain.
- [[apps-lets-encrypt]] — the paid app that provisions free SSL via Let's Encrypt and auto-renews.
- [[settings-admin-notifications]] — controls whether SSL expiry / fallback alerts are emailed to the merchant.

## Related

### Related entities

- [[site]] — every Domain belongs to exactly one Site; one Site can have many Domains (one primary, others as aliases + the always-present fallback subdomain).
- [[plan]] — `cname` / `custom_hostname` plan-features control how many Domains the merchant can attach.
- [[admin-notification]] — SSL expiry + fallback raise admin-panel alerts.
- [[api-key]] / [[webhook]] — both are Site-scoped, served per the resolved Site (which depends on the request's matched Domain).

### Cross-cutting concepts

- [[plan-gates]] — `cname` / `custom_hostname` quota gate; SSL gated by `ssl_certificate` plan feature.
- [[notification-delivery]] — SSL expiry alerts fan out via the platform-wide admin-alert + email channels.
- [[merchant-roles]] — `settings.domains` permission grants the merchant / moderator access to this whole surface.

## Open Questions

Distributed to aspect pages. See:

- [[domain-ssl]] — exact behaviour when an SSL cert is provisioned but the Domain is then deactivated — does the cert auto-renew on the daily sweep, or skip until reactivation?
- [[domain-primary-and-plan-gates]] — whether CloudCart-purchased domain renewal price is shown to the merchant BEFORE renewal or only AFTER as an invoice line.
- [[domain-lifecycle]] — whether removing a Domain mid-checkout (with active customer sessions) triggers any user-facing fallback, or whether the customer's session breaks abruptly.
