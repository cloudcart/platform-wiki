---
type: entity
aliases: ["Domain DNS", "DNS records modal", "Cloudflare zone", "Cloudflare Custom Hostname", "Cloudflare for SaaS", "Cloudflare Proxy toggle", "Orange cloud", "Grey cloud", "Hosted email DNS", "DKIM SPF DMARC"]
tags: [settings, apps, domains, dns, cloudflare, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[domain]]. See the hub for the other aspects (attributes, relationships, lifecycle, SSL, primary + plan gates).

# Domain — DNS & Cloudflare

## Identity

How a [[domain|Domain]] connects to CloudCart's edge infrastructure (Cloudflare) and how the merchant manages DNS records from the in-admin DNS modal. There are exactly **two Cloudflare modes** per Domain — standard zone or Custom Hostname (Cloudflare-for-SaaS) — and the platform chooses based on the add path, NOT the merchant. The DNS records table (A, AAAA, CNAME, MX, TXT, NS, etc.) is unlocked only after the Cloudflare zone reports `active`. Each record has a per-record **Proxy toggle** (orange cloud = CDN + DDoS, grey cloud = DNS-only). Activating CloudCart's hosted email service auto-inserts the right MX + SPF + DKIM + DMARC records. This page is the reference the AI Assistant cites when a merchant asks *"Where do I add an MX record?"*, *"What's the orange cloud icon?"*, or *"My DNS records are missing — where's the DNS modal?"*.

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

### Two Cloudflare modes — platform-chosen, not merchant-picked

The platform uses ONE of two Cloudflare modes per Domain depending on the add path:

| Mode | When the platform picks it | DNS records table in admin | Plan-feature consumed |
|------|----------------------------|----------------------------|------------------------|
| **Standard Cloudflare zone** (`cloudflare_zone_id` set) | Externally-owned Domains added via "Add existing" where the merchant changes nameservers; CloudCart-purchased Domains. | Full DNS record control — merchant edits A / AAAA / CNAME / MX / TXT / NS / SRV / CAA. | `cname` (or none for the CloudCart-purchased path). |
| **Cloudflare Custom Hostname / SaaS** (`cloudflare_hostname_id` set) | Externally-owned Domains where the merchant keeps DNS at their original provider and only points a CNAME to CloudCart. | Reduced — most records stay at the merchant's existing DNS provider, only the CloudCart-managed bits are visible. | `custom_hostname`. |

In Custom Hostname mode the merchant typically only needs a single CNAME record at their existing DNS provider — that one record makes the hostname resolvable to CloudCart. The platform handles the Cloudflare-for-SaaS attachment on its end.

### Hosted email auto-configures DNS

When the merchant activates CloudCart's hosted email service on a Domain, the platform automatically inserts the right records in the DNS modal:

- **MX** record pointing to `mail.cloudcart.com`.
- **TXT `_dmarc`** record: `v=DMARC1; p=none; pct=100; rua=mailto:dmarc-reports@<domain>`.
- **TXT SPF** record: `v=spf1 mx ~all`.
- **TXT DKIM** record under `<domain>._domainkey` containing the generated DKIM public key.

The merchant just confirms the records exist after activation — no manual editing required. These records must remain **grey cloud (DNS-only)** because mail does not go through Cloudflare's HTTP proxy.

### DNS status — pending vs active

The DNS records modal is unlocked only when the Cloudflare zone status reports `active`. While the status is `pending`, the modal shows a guidance message telling the merchant to complete the nameserver change at their registrar (for standard zone mode) or to add the CNAME at their original DNS provider (for Custom Hostname mode). Propagation typically takes minutes to 48 hours after the nameserver / CNAME change. See [[domain-lifecycle]] for the lifecycle phases.

## Where it appears

- [[settings-domains]] — the DNS modal is opened from the per-row action menu (Manage DNS).
- [[settings-banned-ip]] — depends on `CF-Connecting-IP` (set by Cloudflare proxy) to identify real customer IPs.
- The hosted email activation flow (a separate app integration) inserts the email-related DNS records automatically.

## Related

- [[domain]] — hub.
- [[settings-domains]] — DNS modal opens from here.
- [[settings-banned-ip]] — Cloudflare's `CF-Connecting-IP` header keeps IP-based features working.
- [[plan-gates]] — `cname` / `custom_hostname` quota controls the two Cloudflare modes — see [[domain-primary-and-plan-gates]].
- [[plan]] — the plan determines which Cloudflare-mode-related features are unlocked.

## Open Questions

None.
