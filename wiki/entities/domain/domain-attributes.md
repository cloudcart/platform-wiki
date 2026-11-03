---
type: entity
aliases: ["Domain attributes", "Domain fields", "Hostname attributes", "Domain key attributes", "SSL fields", "DNS fields"]
tags: [settings, apps, domains, ssl, dns, entity, attributes]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[domain]]. See the hub for the other aspects (relationships, lifecycle, SSL, DNS / Cloudflare, primary + plan gates).

# Domain — Key attributes

## Identity

The full per-field schema for the [[domain|Domain]] record — every attribute the merchant configures on [[settings-domains]] or sees parsed out of an installed SSL certificate, with allowed values, defaults, and edit constraints. This page is the reference the AI Assistant cites when a merchant asks *"What does this column mean?"* or *"Why can't I edit the hostname after creating it?"*. Special properties of the always-present `<handle>.cloudcart.net` subdomain are listed at the end — it behaves differently from custom Domains on almost every attribute.

## Aliases

- **Domain attributes** / **Domain fields** — the per-record field definitions visible in the [[settings-domains]] list and edit modals.
- **Hostname** — the technical phrasing used in DNS / SSL contexts; functionally a synonym of "Domain" at the attribute level.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Domain name** (`hostname`) | Required at create time, NOT editable after | The domain itself (e.g., `mystore.bg`). For internationalised domain names (IDN) — Cyrillic / Greek / Arabic — the platform converts to Punycode (UTS-46) for storage and back to display form for rendering. So `сайт.бг` is accepted and stored as `xn--80aswg.xn--90ae`. See [[domain-primary-and-plan-gates]] for IDN end-to-end behaviour. |
| **Is primary** (`is_primary`) | Designated via "Set as primary" per-row action | Exactly ONE Domain per Site is the primary at any time. Setting another Domain as primary auto-unsets the previous primary. Primary cannot be deactivated or removed without first reassigning — see [[domain-primary-and-plan-gates]]. |
| **Active toggle** | Per-row toggle | When ON, serves customers. When OFF, the Domain stays attached but doesn't serve. The primary Domain cannot be deactivated. |
| **Source** | n/a (set at create) | `external` — merchant brought the domain from another registrar; CloudCart does NOT manage renewal billing. `cloudcart` — merchant bought through the in-admin Buy a Domain flow via the integrated reseller; CloudCart handles renewal billing through the merchant's plan subscription. The CloudCart-provided `<handle>.cloudcart.net` is a third special-case kind, always-present and non-removable. |
| **DNS status** | n/a (auto-detected) | `pending` — nameservers not yet pointing at CloudCart. `active` — Cloudflare zone is live and DNS records are editable from the in-admin DNS modal. Transitions automatically when Cloudflare detects nameserver propagation (minutes to 48 hours). |
| **SSL status** | n/a (auto, depending on certificate state) | `active` (cert valid) / `pending` (issuance in progress) / `failed` (issuance / renewal failed — error visible in the SSL modal). |
| **SSL mode** (`free` flag on the cert) | Picked at install time (Automatic vs Manual tab on [[settings-ssl]]) | `free=1` — Let's Encrypt (auto-renewed). `free=0` — external manual cert (merchant renews). See [[domain-ssl]]. |
| **SSL expiry date** | n/a (parsed from the cert) | Visible in the SSL modal. For external certs, the merchant must replace before this date or the storefront breaks. |
| **Expiry date** (domain registration) | n/a (CloudCart-purchased domains only) | When the domain registration itself expires (separate from SSL). Renewal warning is shown 30 days before. External-source domains don't show this — the merchant manages registration at their original registrar. |
| **DNS records** (A, AAAA, CNAME, MX, TXT, NS, etc.) | Per-record edit / add / delete in the DNS modal | Available only once Cloudflare zone is `active`. Each record has a per-record Cloudflare **Proxy toggle** (orange cloud = CDN + DDoS protection enabled, grey cloud = DNS-only). See [[domain-dns-cloudflare]]. |
| **Cloudflare zone ID** / **Cloudflare custom-hostname ID** | n/a (set by the integration) | The platform uses one of two Cloudflare modes per Domain — standard zone (the merchant's whole zone is hosted on Cloudflare) OR Cloudflare-for-SaaS Custom Hostname (only this single hostname is attached as a custom hostname under CloudCart's own zone). The mode is platform-chosen based on the add path — see [[domain-dns-cloudflare]]. |
| **WHOIS contact info** | Editable for CloudCart-purchased domains only | Registrant name, address, email, phone (required by ICANN). External-source domains' WHOIS is managed at the original registrar. WHOIS Privacy is automatically enabled on CloudCart-purchased domains. |
| **Attached at** / **DNS validated at** | n/a (auto) | Timestamps for audit. |

## Where it appears

- [[settings-domains]] — the master list shows the hostname, primary marker, active toggle, source, DNS status, SSL status, and expiry warning chip per row.
- [[settings-ssl]] — per-Domain SSL modal exposing the SSL mode, status, and expiry.
- The DNS modal (opened from the per-row action menu on [[settings-domains]]) exposes the DNS records table once the Cloudflare zone is `active`.
- The "Other domains" usage chip in the [[settings-domains]] header surfaces the `cname` / `custom_hostname` quota — see [[domain-primary-and-plan-gates]].

## The always-present `<handle>.cloudcart.net` subdomain

The CloudCart-provided subdomain assigned at Site signup has special properties that differ from custom Domains on almost every attribute:

- **Always-present** — created at Site signup; the row cannot be removed from the admin panel.
- **Cannot be deactivated** — the Active toggle is absent / forced ON.
- **Cannot be renamed from the admin panel** — changing the `<handle>` portion requires CloudCart support intervention.
- **Uses a wildcard SSL certificate** managed by CloudCart's infrastructure — the merchant never manages this cert via [[settings-ssl]]; the SSL modal does not apply.
- **Source is a third special-case kind** (neither `external` nor `cloudcart`) — no renewal billing, no WHOIS, no domain-registration expiry date.
- **Serves as the automatic-fallback URL** when a custom primary Domain's SSL expires — see [[domain-ssl]] for the daily sweep + fallback rule.

## Related

- [[domain]] — hub.
- [[site]] — every Domain belongs to exactly one Site; the same Site can have many Domains.
- [[settings-domains]] — the master management screen these attributes appear on.
- [[settings-ssl]] — SSL mode / status / expiry attributes editable here.
- [[plan]] — `cname` / `custom_hostname` plan-features cap the number of custom Domains.

## Open Questions

None — attribute-level edge cases captured in the table.
