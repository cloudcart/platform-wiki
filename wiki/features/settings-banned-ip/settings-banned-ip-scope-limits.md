---
type: feature
nav_path: "Settings → Block Client IP addresses → Scope & limits"
route_name: banned-ip.settings
route_path: /admin/settings/banned-ip
aliases: ["Banned IP scope", "Banned IP limits", "No auto-ban", "No bulk import IP", "settings.banned permission", "Order rejection not site block"]
tags: [settings, security, ban, ip, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[settings-banned-ip]]. See the hub for the other aspects (list & modal, enforcement, IP formats).

# Block Client IP addresses — scope & limits

## Purpose

This aspect documents the **boundaries** of the feature: what it does and does not affect, what it will not do automatically, and who is allowed to edit it. It is the page to read when a merchant asks "why didn't this block the visitor from the site?" or "can it auto-ban after failed payments?". For what blocking does to a matched order, see [[settings-banned-ip-enforcement]].

## Where to find it

Sidebar → Settings → **Block Client IP addresses** (`/admin/settings/banned-ip`). Permission to edit is governed by the grants in [[settings-staff]].

## What the merchant can do here

- Maintain the blocklist manually (add / edit / delete entries).
- Delegate edit access to staff via the `settings.banned` granular grant.

What the merchant CANNOT rely on the feature to do is detailed in Business rules below.

## Settings & fields

This aspect has no extra fields beyond the list / modal documented on [[settings-banned-ip-list-management]]. The relevant control is the **permission grant**:

| Grant | Effect |
|-------|--------|
| `settings` (general Settings grant) | Inherits banned-IP edit rights automatically. |
| `settings.banned` (granular grant) | Grants banned-IP edit rights only — for delegating just this feature without broader Settings access. |

## Business rules

### Scope — order rejection, NOT site blocking

This list affects **order placement only**. A customer with a blocked IP can still load product pages, view the cart, etc. — the rejection happens at checkout / order submission. Merchants who need site-level blocking should use Cloudflare or another WAF (CloudCart's Cloudflare integration is documented in [[apps]] and configured at the [[settings-domains]] level).

### No auto-ban — strictly manual

The platform does NOT automatically add IPs to this list after any fraud trigger (failed payments, chargebacks, declined cards, suspicious behaviour, etc.). Every entry is one the merchant typed in manually. There is no "auto-ban after N failed attempts" toggle and no other system that writes to this table programmatically.

### No bulk import — one IP at a time

There is no CSV import path, no API endpoint that accepts a batch of IPs in a single call from this surface, and no clipboard-paste handler for multiple lines. A merchant migrating from another platform with a long blocklist must add each entry one at a time. (A bulk-DELETE endpoint exists for cleanup — see [[settings-banned-ip-list-management]] — but there is no bulk-CREATE counterpart.) Workaround for very large lists: contact CloudCart support to seed the underlying table directly.

### No per-IP order history view from this page

This page lists only the blocked IPs themselves; it does NOT surface the orders historically attempted from each one. To see past orders associated with an IP, the merchant searches Orders by IP address from the Orders area (the order's IP is recorded on creation — see [[orders-details]]). Adding an IP does NOT auto-cancel or auto-refund any past orders — only **future** orders from the IP are auto-cancelled.

### Permission inheritance

The banned-IP API endpoints require either `settings` (the general Settings grant) OR the granular `settings.banned`. A moderator with broader Settings access automatically inherits banned-IP edit rights; admins who want to delegate just this feature can grant only `settings.banned` from [[settings-staff]].

## Related

- [[settings-banned-ip]] — hub.
- [[settings-staff]] — where the `settings.banned` permission grant is assigned.
- [[settings-domains]] — Cloudflare firewall layer for true site-level / subnet blocking.
- [[apps]] — Cloudflare integration (separate site-level IP blocking at the firewall).
- [[order]] — only future orders are affected; past orders are untouched.

## Open questions

None.
