---
type: feature
nav_path: "Settings → Domains → DNS / Cloudflare"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Manage DNS", "DNS records", "Cloudflare zone", "Cloudflare for SaaS", "Custom Hostname", "Nameserver change", "Proxy toggle", "Orange cloud", "DKIM", "SPF", "DMARC", "DNS-only", "Activate domain modal"]
tags: [settings, domains, dns, cloudflare, custom-hostname, email-auth]
plan_gates: ["custom_hostname"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, SSL, primary, deletion, plan gates).

# Domains — DNS / Cloudflare

## Purpose

How the merchant connects a domain to CloudCart's DNS layer and edits its records: the Activate Domain modal (CloudCart's nameservers vs **Manage with CNAME**), the Manage DNS modal (pending vs active), the per-record Proxy setting and what records the backend force-overrides, which DNS an outside service's records go in, and the legacy hosted-mailbox records (not the [[marketing-channels-email|Email marketing channel]]'s).

## Where to find it

Settings → Domains → a row's **DNS Records** column: **Manage DNS** once the domain has a zone; before that **Activate DNS Records** (or **Custom hostname** when the store has CNAME slots).

## What the merchant can do here

### Activate Domain modal — the two-path picker

Opens right after a domain is added, from **Activate DNS Records**, or when **Domain active** is switched on before DNS is set. Title *"Activate Domain"*, subtitle *"To activate the domain you need to choose one of these two methods:"*.

**Method 1 — Complete domain management and DDoS protection (Recommended)**

- Button **Enable DNS Record management** (**Manage DNS Records** once a zone exists) → the standard Cloudflare zone.

**Method 2 — Domain management via CNAME (Not recommended)** — only shown when `!domainData.purchase_namecome`:

- Plan badges **CC Pro**, **CC Master**, **Unicorn**; *"Not recommended! ... Your online store will NOT be protected from attackers!"*
- Button **Manage with CNAME** (orange) → uses a `custom_hostname` slot ([[settings-domains-plan-gates]]) and attaches the domain as a Cloudflare custom hostname; the merchant keeps their DNS and creates one CNAME to the store's `*.cloudcart.net` address. Details: [[settings-domains-external-dns]].

### Manage DNS modal — Mode 1: Zone pending

- Header *"Change nameservers"*: *"Log in to your domain management and remove these nameservers:"* (the current ones), then *"Replace with the following nameservers:"* (CloudCart's).
- **Save changes** — polls Cloudflare; closes once `status=active`.

### Manage DNS modal — Mode 2: Zone active

- Header: *"Manage DNS Records"*. Subtitle: *"Create, edit or delete DNS records"*.
- **+ Add DNS Record** adds an empty inline row.
- Columns: **Type** (A / AAAA / CNAME / MX / TXT / NS / etc.), **Host name**, **Answer**, **Proxy** (Yes / No), **Priority** (MX only), **Actions** (Delete).
- Rows are inline-editable; picking a Type other than MX presets **Proxy** to Yes, so set No for a subdomain that is not the website. Delete opens *"Delete record?"*.
- **Host name** takes the full name (`mail.example.com`) or the part before the domain (`mail`, `@` for the root); CloudCart's own records use the short form, and the table lists full names.

## Settings & fields

- **DNS record types editable**: A / AAAA / CNAME / MX / TXT / NS / SRV / CAA / etc.
- **Per-record Proxy** (Cloudflare's orange cloud): Yes = Cloudflare CDN/proxy (DDoS, edge cache, SSL termination, IP masking). No = DNS-only; direct to origin.

## Business rules

### Cloudflare zone activation flow (standard zone)

1. The merchant clicks **Enable DNS Record management** → CloudCart creates the zone (root and `www` CNAMEs to the store, a one-time copy of the root's MX and TXT records — see [[settings-domains-external-dns]]) → status **Pending**.
2. Merchant changes nameservers at their registrar to the ones CloudCart provides (visible in the DNS modal during pending state).
3. Cloudflare detects propagation → zone status becomes `active` (minutes to 48 hours).
4. Once active, the DNS records table unlocks for editing.

### Two Cloudflare modes — standard zone vs Custom Hostname (Cloudflare for SaaS)

- **Standard Cloudflare zone** (`cloudflare_zone_id` set): the merchant's domain has its own zone — full DNS-record control (A, AAAA, CNAME, MX, TXT, NS, etc.) via the DNS modal. The recommended method, and the only one for CloudCart-purchased domains.
- **Cloudflare Custom Hostname / SaaS** (`cloudflare_hostname_id` set): the platform attaches the merchant's domain as a custom hostname under CloudCart's own zone. The merchant keeps DNS at their original provider and only points a CNAME to CloudCart. This is the path that consumes the `custom_hostname` plan-feature quota — see [[settings-domains-plan-gates]].

The merchant picks the method in the Activate Domain modal. In CNAME mode every record stays at the merchant's DNS provider, and the row shows a **Custom hostname** link instead of **Manage DNS**.

### Proxy guidance

Storefront records (root and `www`) stay proxied; the platform reads the visitor's real IP from `CF-Connecting-IP`, so [[settings-banned-ip]] still works. Non-HTTP services (mail, SSH, FTP) must be DNS-only.

### TXT and MX records — Proxy is forced to DNS-only by the backend

The per-record `proxied` toggle in the UI is **ignored by the backend for certain record types** and silently overwritten:

- **TXT records** — always `proxied=false` (no HTTP semantics).
- **MX records** — always `proxied=false` (Cloudflare can't proxy SMTP).
- **CNAME records pointing to `*.cloudcart.net`** — always `proxied=true`, required for the storefront to work.
- **A, AAAA and other types** keep the merchant's choice, defaulting to Yes, so a mail server's A record must be set to No by hand.

So a TXT or MX saved with Yes comes back No, and a CNAME to the store saved with No comes back Yes.

### Which DNS an outside service's records go in

While a domain uses CloudCart's nameservers, this zone is its public DNS: every record for an outside service (an external mailbox's MX / SPF / DKIM / DMARC, a Google verification TXT, a marketing sender's records) goes here, and records left at the registrar's old DNS have no effect. The zone sits in CloudCart's Cloudflare account, so a service's automatic "sign in to your DNS provider" verification cannot be authorised by the merchant: add its TXT record here by hand (for Google Search Console, the [[apps-google-search-console]] meta tag is the alternative). A domain may publish only one SPF record and one `_dmarc` record (an email-standards rule): add a new sender's `include:` to the existing SPF instead of adding a second one. CloudCart writes no SPF, DKIM or DMARC by default ([[apps-google-workspace]], [[apps-smtp]]).

### Legacy hosted-mailbox records

The discontinued hosted mailbox service ([[settings-emails-discontinued]]) wrote an MX to `mail.cloudcart.com`, `v=spf1 mx ~all`, a `_dmarc` TXT and a DKIM TXT at `<domain>._domainkey`, only on CloudCart-purchased domains, when a domain's first mailbox was activated. New mailboxes cannot be created, so a zone holds these only from that time; replace them when moving mail to another provider.

### DNS edits propagate immediately

DNS edits show on the storefront within seconds. DNS edit failures usually indicate transient DNS-service issues — retry; if persistent, contact CloudCart support.

## Related

- [[settings-domains]] — hub.
- [[settings-domains-add-flow]] — what happens before the DNS step.
- [[settings-domains-primary]] — the Powered-by-CloudCart header check that runs at `/.well-known/acme-challenge/_selftest` and the verification gates for set-as-primary.
- [[settings-domains-plan-gates]] — `custom_hostname` quota and the PlanFeature modal upsell triggered by Method 2.
- [[settings-banned-ip]] — depends on `CF-Connecting-IP` for accurate customer-IP visibility.
- [[apps-smtp]] / [[apps-smtp-settings]] / [[apps-google-workspace]] — external mail-provider configuration that goes into the TXT records.
- [[settings-emails]] — the discontinued hosted mailboxes behind the legacy records.
- [[settings-domains-external-dns]] — CNAME mode, what a nameserver change copies, moving DNS away.

## Open questions

None.
