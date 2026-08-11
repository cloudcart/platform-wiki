---
type: feature
nav_path: "Settings → Block Client IP addresses"
route_name: banned-ip.settings
route_path: /admin/settings/banned-ip
aliases: ["Banned IP", "Block Client IP addresses", "Banned IPs", "IP blacklist", "Блокирани IP адреси", "Черен списък"]
tags: [settings, security, ban, fraud, ip]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Block Client IP addresses

## Purpose

A **top fraud-prevention feature**. The merchant maintains a list of IP addresses; orders coming from those IPs are silently neutralised — they enter as cancelled with a clear audit note, never reach fulfilment, never burden the merchant with work, and the fraudster gets zero feedback that they were caught.

The design is deliberately elegant — four properties make it low-friction:

- **Silent blocking** — the fraudster sees a normal "thank you for your order" page. No rejection signal denies them the feedback to switch IPs and retry. See [[settings-banned-ip-enforcement]].
- **No merchant work** — the order arrives in admin already cancelled, with a ban-reason note. Nothing to investigate, refund, or communicate.
- **No stock tied up** — cancelled orders restore stock automatically per [[settings-cart]] rules.
- **No customer-side spam** — no confirmation email goes to the fraudster.

The auto-cancel runs ONLY for Cash-on-delivery / bank-transfer / manual-payment orders. Online-payment orders (Stripe, PayPal, etc.) are deliberately exempted — see [[settings-banned-ip-enforcement]].

Typical use cases: blocking known fraudsters after a chargeback, rejecting bot / scraper traffic, locking out a hostile competitor monitoring prices, neutralising a customer who just ran a card-test attack.

Scope: this is order-level anti-fraud, NOT a storefront-access firewall. Visitors from blocked IPs can still browse — only order placement is silently neutralised. See [[settings-banned-ip-scope-limits]].

## Where to find it

Sidebar → Settings → **Block Client IP addresses**.

The page's breadcrumb reads "Settings → Block Client IP addresses". The route is `/admin/settings/banned-ip`. The header icon is the ban icon.

## What the merchant can do here

- See a table of all blocked IPs with their IP address and the merchant's description.
- Click **+ Block new IP** in the page header to open the create modal.
- Click any row to open the edit modal.
- Remove a single entry via the per-row delete button.
- Bulk-select multiple rows and bulk-delete them.
- Filter, search, paginate (default sort: id desc — most recently added on top).

The full UI mechanics (list columns, modal shape, per-row remove vs bulk-delete confirmation differences) live on [[settings-banned-ip-list-management]].

## Settings & fields

The create / edit modal has two fields:

| Field | Type | Notes |
|-------|------|-------|
| **IP address** (`ip`) | string | Required (Zod min 1 — *"IP address is required"*). Server validates IP format. |
| **Description** (`description`) | string | Optional note about why this IP was blocked. Max 191 chars. |

Validation surfaces three known errors: *"IP address is required"*, *"Invalid IP address"*, *"IP address already exists"*, plus *"Description may not be greater than 191 characters"*. Format support (IPv4 + IPv6, no CIDR) and uniqueness semantics are detailed on [[settings-banned-ip-ip-formats]]. The complete field-by-field breakdown of the list table and modal is on [[settings-banned-ip-list-management]].

## Business rules

The blocklist affects **order placement only** — a blocked visitor can still browse the storefront; the check runs at order submission. Enforcement is a server-side post-create auto-cancel that exempts online payments. There is no auto-ban, no bulk import, and no per-IP order history view. See the sub-pages below for each rule in full.

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages. Drill into the one that matches the question.

- [[settings-banned-ip-list-management]] — the admin UI: list table columns, create/edit modal shape, per-row remove (no confirm) vs bulk-delete (with confirm), row-click-to-edit, optimistic update.
- [[settings-banned-ip-enforcement]] — the server-side post-create auto-cancel mechanism, online-payment exemption (the `is_online_payment` discriminator), customer-facing UX, invoice / cache side effects.
- [[settings-banned-ip-ip-formats]] — IPv4 + IPv6 support, no CIDR / wildcard, literal-string uniqueness, how the source IP is resolved (trusted proxies / Cloudflare), no VPN / proxy detection.
- [[settings-banned-ip-scope-limits]] — order-rejection-not-site-firewall scope, no auto-ban (strictly manual), no bulk import, no per-IP order history, the `settings.banned` permission grant, Cloudflare comparison.

## Related

- [[settings]] — parent hub.
- [[apps]] — Cloudflare integration provides separate site-level IP blocking at the firewall.
- [[order]] — entity affected by this blacklist (order creation is what's rejected).
- [[customer]] — IPs are tied to incoming requests, not customer accounts; a banned IP affects whichever customer is using it at the moment.
- [[checkout-flow]] — the IP check happens during checkout submission.

## Open questions

(All known open questions have been resolved — see the sub-pages.)
