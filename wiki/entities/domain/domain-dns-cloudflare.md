---
type: entity
aliases: ["Domain DNS", "DNS records modal", "Cloudflare zone", "Cloudflare Custom Hostname", "Cloudflare for SaaS", "Cloudflare Proxy toggle", "Orange cloud", "Grey cloud", "Hosted email DNS", "DKIM SPF DMARC"]
tags: [settings, apps, domains, dns, cloudflare, entity]
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---

> Part of [[domain]]. See the hub for the other aspects (attributes, relationships, lifecycle, SSL, primary + plan gates).

# Domain — DNS & Cloudflare

## Identity

How a [[domain|Domain]] connects to CloudCart's edge infrastructure (Cloudflare) and how the merchant manages DNS records from the in-admin DNS modal. There are exactly **two Cloudflare modes** per Domain — standard zone or Custom Hostname (Cloudflare-for-SaaS) — and the merchant picks one in the Activate Domain modal. The DNS records table (A, AAAA, CNAME, MX, TXT, NS, etc.) is unlocked only after the Cloudflare zone reports `active`. Each record has a per-record **Proxy toggle** (orange cloud = CDN + DDoS, grey cloud = DNS-only). CloudCart writes no mail records by default; only the discontinued hosted mailbox service once did. This page is the reference the AI Assistant cites when a merchant asks *"Where do I add an MX record?"*, *"What's the orange cloud icon?"*, or *"My DNS records are missing — where's the DNS modal?"*.

## Aliases

- **DNS records modal** — the in-admin per-Domain DNS table.
- **Cloudflare zone** — the standard mode (merchant's full DNS zone hosted on Cloudflare).
- **Cloudflare Custom Hostname** / **Cloudflare-for-SaaS** — the alternative mode (single hostname attached to CloudCart's own zone).
- **Orange cloud** / **Grey cloud** — Cloudflare's per-record Proxy toggle states.

## Key Attributes

### DNS records — Cloudflare-managed, edited from the in-admin modal

Once the Cloudflare zone status is `active`, the merchant can edit DNS records from the in-admin DNS modal opened from the per-row action menu on [[settings-domains]]. Record types supported: **A, AAAA, CNAME, MX, TXT, NS, SRV, CAA**, etc. Per-record actions: add / edit / delete plus the per-record Cloudflare **Proxy toggle**:

| Proxy state | What it does | When to use |
|-------------|--------------|-------------|
| **Orange cloud (proxied)** | Traffic routes through Cloudflare's edge — CDN caching, DDoS protection, WAF, IP hiding (real origin IP is masked). | HTTP / HTTPS records pointing at the storefront (root and `www` A / CNAME). |
| **Grey cloud (DNS-only)** | Cloudflare returns the record as DNS only; traffic does NOT route through Cloudflare. | Non-HTTP services like mail (MX), SSH, FTP — Cloudflare only proxies HTTP/HTTPS, so these must be DNS-only or the service breaks. |

For **storefront-serving records** (root and `www` A / CNAME), the platform sets `proxied=true` by default — the storefront benefits from the CDN automatically. The platform reads `CF-Connecting-IP` to recover the customer's real IP, so IP-based features like [[settings-banned-ip]] keep working. Toggling off the orange cloud on the storefront records will lose CDN + DDoS protection — only do this for diagnostic purposes.

### Two Cloudflare modes — picked by the merchant

Each Domain uses ONE of two Cloudflare modes:

| Mode | When it applies | DNS records table in admin | Plan-feature consumed |
|------|----------------------------|----------------------------|------------------------|
| **Standard Cloudflare zone** (`cloudflare_zone_id` set) | **Enable DNS Record management** on a domain registered elsewhere (the merchant changes nameservers); every CloudCart-purchased Domain. | Full DNS record control — merchant edits A / AAAA / CNAME / MX / TXT / NS / SRV / CAA. | None. |
| **Cloudflare Custom Hostname / SaaS** (`cloudflare_hostname_id` set) | **Manage with CNAME** on a domain registered elsewhere: DNS stays at the merchant's provider, one CNAME points to the store's `*.cloudcart.net` address. | None in the admin — every record stays at the merchant's provider. | `custom_hostname`. |

Details, and why there is no A-record / IP method: [[settings-domains-external-dns]].

### Mail records

CloudCart adds no MX, SPF, DKIM or DMARC to a zone; an outside mail provider's records are added in the DNS modal. The discontinued hosted mailbox service once wrote an MX to `mail.cloudcart.com`, `v=spf1 mx ~all`, a `_dmarc` TXT and a DKIM TXT at `<domain>._domainkey` on CloudCart-purchased domains ([[settings-domains-dns-cloudflare]]). Mail records must stay DNS-only.

### DNS status — pending vs active

The DNS records modal is unlocked only when the Cloudflare zone status reports `active`. While the status is `pending`, the modal shows the nameserver change to make at the registrar. A Custom Hostname domain has no zone; its row's **Custom hostname** link shows the CNAME to add. Propagation typically takes minutes to 48 hours after the nameserver / CNAME change. See [[domain-lifecycle]] for the lifecycle phases.

## Where it appears

- [[settings-domains]] — the DNS modal is opened from the per-row action menu (Manage DNS).
- [[settings-banned-ip]] — depends on `CF-Connecting-IP` (set by Cloudflare proxy) to identify real customer IPs.

## Related

- [[domain]] — hub.
- [[settings-domains]] — DNS modal opens from here.
- [[settings-banned-ip]] — Cloudflare's `CF-Connecting-IP` header keeps IP-based features working.
- [[plan-gates]] — the `custom_hostname` quota controls the Custom Hostname mode — see [[domain-primary-and-plan-gates]].
- [[plan]] — the plan determines which Cloudflare-mode-related features are unlocked.

## Open Questions

None.
