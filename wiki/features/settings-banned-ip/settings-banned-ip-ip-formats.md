---
type: feature
nav_path: "Settings → Block Client IP addresses → IP formats"
route_name: banned-ip.settings
route_path: /admin/settings/banned-ip
aliases: ["Banned IP formats", "IPv4 IPv6 ban", "CIDR support banned IP", "IP uniqueness", "Source IP resolution", "VPN proxy detection"]
tags: [settings, security, ban, ip, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[settings-banned-ip]]. See the hub for the other aspects (list & modal, enforcement, scope & limits).

# Block Client IP addresses — IP formats & matching

## Purpose

This aspect documents what the **IP address** field accepts, how a stored entry is matched against an incoming order, and the limits of that matching (no ranges, literal-string uniqueness, how the source IP is resolved, and no VPN / proxy detection). For the modal that holds the field, see [[settings-banned-ip-list-management]].

## Where to find it

The IP-address input lives in the create / edit modal of Sidebar → Settings → **Block Client IP addresses** (`/admin/settings/banned-ip`).

## What the merchant can do here

- Enter a single IPv4 address (e.g. `192.168.1.1`).
- Enter a single full IPv6 address (e.g. `2001:0db8:85a3:0000:0000:8a2e:0370:7334`).

The merchant CANNOT enter a CIDR block, wildcard, or range expression — see Business rules below.

## Settings & fields

| Aspect | Behaviour |
|--------|-----------|
| Accepted formats | IPv4 **and** IPv6 (the application framework's built-in `ip` validation rule). |
| Rejected formats | `192.168.0.0/24`, `192.168.0.*`, any range expression → *"Invalid IP address"*. |
| Empty | *"IP address is required"* (Zod min 1). |
| Duplicate | *"IP address already exists"* (uniqueness on the literal IP string). |
| Matching | Exact literal-string equality between stored `ip` and the request's resolved source IP. |

## Business rules

### IPv4 AND IPv6 supported

The input accepts both. A full IPv6 address like `2001:0db8:85a3:0000:0000:8a2e:0370:7334` saves successfully. The backend uses the application framework's `ip` validation rule, which accepts both families.

### NO CIDR / wildcard / range support

Single IP per row. There is no CIDR or wildcard support — to block a range of 256 IPs the merchant would need 256 rows. The input rejects `192.168.0.0/24`, `192.168.0.*`, or any range expression with *"Invalid IP address"*. (Backend may theoretically accept a range string, but UI validation tightens it to a single address.) (verify)

### Uniqueness is on the literal string

The uniqueness constraint is on the literal IP string. So `192.168.1.1` and `::ffff:192.168.1.1` (IPv6-mapped IPv4) are considered **different** entries even though they describe the same host — a merchant blocking a dual-stack visitor may need both forms.

### How the source IP is resolved (trusted proxies / Cloudflare)

The check uses the IP that the framework's request-IP resolution returns, which respects trusted proxy headers. Behind Cloudflare this should be the original visitor's IP, not the CDN edge. **Caveat:** if the merchant has installed a misbehaving proxy app that strips IP-forwarding headers, all storefront orders may appear to come from the proxy's IP — making the blocklist ineffective. Verify by reading the IP attached to a recent test order before relying on the list.

### No VPN / proxy / fraud-service detection

The platform does NOT integrate with any VPN / proxy / fraud-detection service (no IPQS, MaxMind, Spamhaus, etc.). The blocklist is a pure static list of IP literals — a determined fraudster who switches to a VPN or rotating proxy reaches a new IP on each attempt and will not be matched. For higher-grade defence pair this list with Cloudflare's bot management / firewall rules at the [[settings-domains]] level, which can block whole subnets, geographies, and detected proxies.

## Related

- [[settings-banned-ip]] — hub.
- [[settings-domains]] — Cloudflare firewall layer that CAN block subnets / geographies / detected proxies.
- [[apps]] — Cloudflare integration (separate site-level IP blocking).

## Open questions

- Whether the backend accepts a CIDR/range string when sent directly (UI blocks it). (verify)
