---
type: feature
nav_path: "Settings → Domains → DNS / Cloudflare"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Manage DNS", "DNS records", "Cloudflare zone", "Cloudflare for SaaS", "Custom Hostname", "Nameserver change", "Proxy toggle", "Orange cloud", "DKIM", "SPF", "DMARC", "DNS-only", "Activate domain modal"]
tags: [settings, domains, dns, cloudflare, custom-hostname, email-auth]
plan_gates: ["custom_hostname"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, SSL, primary, deletion, plan gates).

# Domains — DNS / Cloudflare

## Purpose

How the merchant connects a domain to CloudCart's DNS layer, edits DNS records, and chooses between the two Cloudflare modes (standard zone vs Cloudflare for SaaS Custom Hostname). Covers the Activate Domain modal (the two-path picker), the Manage DNS modal (pending vs active), the per-record orange-cloud Proxy toggle and what records the backend force-overrides, and the automatic DKIM / SPF / DMARC records inserted when CloudCart's hosted email is activated on the domain.

## Where to find it

Settings → Domains → per-domain row → **Manage DNS** action. For a Pending domain, the row also shows an **Activate DNS Records** button that opens the Activate Domain modal first.

## What the merchant can do here

### Activate Domain modal — the two-path picker

Opens via per-row **Activate DNS Records** on a Pending external domain, OR when set-as-primary is attempted before DNS verification. Title *"Activate Domain"*, subtitle *"To activate the domain you need to choose one of these two methods:"*, medium size, X-icon close.

**Method 1 — Complete domain management and DDoS protection (Recommended)**

- Green shield icon, "Recommended!" tag.
- *"With this option, you will manage all DNS records directly through the administration of your store, as well as benefit from full DDoS protection of your store. To enable this option, you will need to add nameservers to the domain management."*
- Button **Manage DNS Records** (or **Enable DNS Record management** for not-yet-activated domains, green) → emits `openDnsModal`. Uses the **standard Cloudflare zone**.

**Method 2 — Domain management via CNAME (Not recommended)** — only shown when `!domainData.purchase_namecome`:

- Warning shield icon. Plan-tier badges: **CC Pro** (orange), **CC Master** (recommended), **Unicorn** (paid).
- *"Not recommended! This option will require you to configure a DNS zone in your domain management. Your online store will NOT be protected from attackers!"*
- Button **Manage with CNAME** (orange) → emits `open-plan-feature` with feature key `custom_hostname`. See [[settings-domains-plan-gates]]. Uses **Cloudflare Custom Hostname** (Cloudflare for SaaS) — merchant keeps DNS at their registrar; only a CNAME points to CloudCart.

Footer: *"If you need more information, click here"* — help-center article link.

### Manage DNS modal — Mode 1: Zone pending

- Header: *"Change nameservers"*.
- *"Step 1: Log in to your domain management and remove these nameservers..."* (lists registrar's current nameservers).
- *"Step 2: Add these..."* (lists CloudCart's Cloudflare nameservers).
- **Save changes** — polls Cloudflare; closes once `status=active`.

### Manage DNS modal — Mode 2: Zone active

- Header: *"Manage DNS Records"*. Subtitle: *"Create, edit or delete DNS records"*.
- **+ Add DNS Record** adds an empty inline row.
- Columns: **Type** (A / AAAA / CNAME / MX / TXT / NS / etc.), **Host name**, **Answer**, **Proxy** (orange-cloud toggle), **Priority** (MX only), **Actions** (Delete).
- Rows are inline-editable. Save POSTs to the DNS endpoint. Delete opens *"Delete record?"*.

### DNSRecords side-panel (legacy)

A narrower DNS-records side-panel (`DNSRecords` component, distinct from `ManageDnsModal`) overlaps with Manage DNS — reached only via deep links in some integration tutorials.

## Settings & fields

- **DNS record types editable**: A / AAAA / CNAME / MX / TXT / NS / SRV / CAA / etc.
- **Per-record Proxy toggle (orange-cloud)**: Orange (`proxied=true`) = Cloudflare CDN/proxy (DDoS, edge cache, SSL termination, IP masking). Grey (`proxied=false`) = DNS-only; direct to origin.

## Business rules

### Cloudflare zone activation flow (standard zone)

1. Merchant adds the external domain → CloudCart prepares a Cloudflare DNS zone → status starts **Pending**.
2. Merchant changes nameservers at their registrar to the ones CloudCart provides (visible in the DNS modal during pending state).
3. Cloudflare detects propagation → zone status becomes `active` (minutes to 48 hours).
4. Once active, the DNS records table unlocks for editing.

### Two Cloudflare modes — standard zone vs Custom Hostname (Cloudflare for SaaS)

- **Standard Cloudflare zone** (`cloudflare_zone_id` set): the merchant's domain has its own zone — full DNS-record control (A, AAAA, CNAME, MX, TXT, NS, etc.) via the DNS modal. Default for externally-owned domains via "Add existing" and for CloudCart-purchased domains.
- **Cloudflare Custom Hostname / SaaS** (`cloudflare_hostname_id` set): the platform attaches the merchant's domain as a custom hostname under CloudCart's own zone. The merchant keeps DNS at their original provider and only points a CNAME to CloudCart. This is the path that consumes the `custom_hostname` plan-feature quota — see [[settings-domains-plan-gates]].

The merchant doesn't pick the mode; the platform chooses based on the add path and quota. In Custom-Hostname mode the DNS records table on this page is reduced — most records stay at the merchant's existing DNS provider.

### Customer IP visibility through Cloudflare proxy

When a record is proxied, the platform sees Cloudflare edge IPs in the raw request, NOT the customer's true IP. CloudCart's HTTP layer reads the `CF-Connecting-IP` header to recover the real IP, so IP-based features like [[settings-banned-ip]] still work correctly. Merchants should NOT untick proxying for storefront records or they lose CDN/DDoS protection.

### Practical proxy guidance per record type

- **Storefront records** (A / CNAME of root + www): CloudCart sets `proxied=true` by default.
- **Non-HTTP services** (mail / SSH / FTP / etc.): set to DNS-only — Cloudflare proxies only HTTP/HTTPS; proxying these would break them.
- **SEO**: unaffected — search engines crawl the public hostname normally.

### TXT and MX records — Proxy is forced to DNS-only by the backend

The per-record `proxied` toggle in the UI is **ignored by the backend for certain record types** and silently overwritten:

- **TXT records** — always `proxied=false` (no HTTP semantics).
- **MX records** — always `proxied=false` (Cloudflare can't proxy SMTP).
- **CNAME records pointing to `*.cloudcart.net`** — always `proxied=true`, required for the storefront to work.

If a merchant reports "I un-proxied the TXT record but it still shows orange-cloud," the backend re-asserted the correct value on save. The actual record at Cloudflare reflects the backend's decision.

### DKIM / SPF / DMARC auto-set when activating CloudCart's hosted email

The TXT-record table lets the merchant add their own SPF / DKIM / DMARC for an external mail provider. But if the merchant activates CloudCart's hosted email (Modoboa) on the domain, the platform automatically inserts:

- **MX** record pointing to `mail.cloudcart.com`.
- **TXT `_dmarc`**: `v=DMARC1; p=none; pct=100; rua=mailto:dmarc-reports@<domain>`.
- **TXT SPF**: `v=spf1 mx ~all`.
- **TXT DKIM** under `<domain>._domainkey` containing the generated DKIM public key.

Merchants using CloudCart's email don't configure email auth manually — they confirm the records appear in the DNS modal after activation. See [[apps-google-workspace]] / [[apps-smtp]] for external-mail-provider alternatives.

### DNS edits propagate immediately

DNS edits show on the storefront within seconds. DNS edit failures usually indicate transient DNS-service issues — retry; if persistent, contact CloudCart support.

## Related

- [[settings-domains]] — hub.
- [[settings-domains-add-flow]] — what happens before the DNS step.
- [[settings-domains-primary]] — the Powered-by-CloudCart header check that runs at `/.well-known/acme-challenge/_selftest` and the verification gates for set-as-primary.
- [[settings-domains-plan-gates]] — `custom_hostname` quota and the PlanFeature modal upsell triggered by Method 2.
- [[settings-banned-ip]] — depends on `CF-Connecting-IP` for accurate customer-IP visibility.
- [[apps-smtp]] / [[apps-smtp-settings]] / [[apps-google-workspace]] — external mail-provider configuration that goes into the TXT records.
- [[settings-emails]] — hosted-email configuration that triggers the auto-DKIM/SPF/DMARC inserts.

## Open questions

None.
