---
type: feature
nav_path: "Settings → Domains → Edge protection and outside filters"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Sorry, you have been blocked", "Country block", "Geo block", "Visitors from a country blocked", "Cloudflare block page", "Edge firewall", "Request logs", "Access logs", "Cloudflare analytics", "Independent traffic measurement", "Phishing warning on my store", "Google Safe Browsing", "A1 Net Protect", "Antivirus blocks my store", "Minimum TLS version", "TLS 1.0 / 1.1", "HSTS", "Strict-Transport-Security", "Cipher suites", "SSL Labs grade", "Corporate web filter", "SSL inspection", "NET::ERR_CERT_AUTHORITY_INVALID", "Newly Observed Domain"]
tags: [settings, domains, cloudflare, edge, security, logs]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, DNS kept elsewhere, SSL, primary, deletion, plan gates).

# Domains — edge protection, request logs and outside safety filters

## Purpose

What sits in front of a store before a request reaches it, who controls it, and what the merchant can and cannot get from it: blocks and challenges at the edge (country rules included), the TLS settings of the secure connection, request logs and edge analytics, and warnings raised by outside safety filters such as an internet provider's filter, a company network's web filter, an antivirus product or a browser's list.

## Where to find it

There is no admin screen for any of this. **Settings → Banned IPs** ([[settings-banned-ip]]) only neutralises orders placed from listed addresses inside the store; it does not block visitors at the edge.

## What the merchant can do here

- Measure traffic with the store's own [[analytics]] and the built-in tracking apps (below).
- Ask the owner of an outside filter to review a warning about their domain.

They cannot see or change edge rules or TLS settings, let a country or a visitor through at the edge, or download request logs.

## Settings & fields

None.

## Business rules

### CloudCart runs the edge for every domain

Every connected domain goes through CloudCart's own Cloudflare account: a domain on CloudCart's nameservers has its zone created in that account, and a CNAME-mode domain and every `*.cloudcart.net` address sit on CloudCart's own zone ([[settings-domains-dns-cloudflare]], [[settings-domains-external-dns]]). The merchant has no login there, so blocks, challenges, country rules and rate limits at the edge are CloudCart's to set and to lift, and a request to let a country or a visitor through goes to CloudCart.

A blocked visitor sees Cloudflare's own page (for example *"Sorry, you have been blocked"*, with a Ray ID), not a CloudCart page; that wording is Cloudflare's. The request never reaches the store, so the store's own records show nothing about it — see [[platform-rate-limits]].

Which rules are active by default, including any country blocks and on which zones, is production configuration that the code does not hold (verify).

### TLS version, cipher suites and HSTS

A visitor's secure (HTTPS) connection to a store's domain is made with the edge in CloudCart's Cloudflare account. The admin has no setting for the minimum TLS version, the cipher suites or HSTS (the Strict-Transport-Security header that tells browsers to use only HTTPS), and the merchant has no login to the zone, so these are CloudCart's to set. CloudCart's code sets none of them when it creates a domain's zone or attaches a CNAME-mode domain, and the store itself adds no Strict-Transport-Security header; the domain gets the edge's own configuration. Which TLS versions and ciphers are accepted, and whether HSTS is sent, is production configuration the code does not hold (verify), so a public test such as SSL Labs shows what is in force. A request to change them goes to CloudCart; the certificate itself is on [[settings-domains-ssl]].

### Request logs and edge analytics

The admin has no screen, export or API for raw HTTP request logs or for the edge's traffic analytics, and the zones sit in CloudCart's account, so the merchant cannot open them there either. Whether support can provide an extract on request is not set by the code (verify).

For an independent measurement the merchant uses tracking whose data lands in their own account: [[apps-google-analytics]] or a container through [[apps-google-tags]]. The store's own [[analytics]] dashboard shows visits and traffic sources from CloudCart's data.

### Outside safety filters

A warning such as "Phishing" from an internet provider's filter (for example A1 Net Protect), an antivirus product or a browser's list (Google Safe Browsing) is the decision of that list's owner. Nothing in the platform adds a store to such a list or takes it off. The review or false-positive request is made to the list owner, through its own form, by the domain owner (verify per list), and its timing is theirs. On CloudCart's side the merchant can confirm that the domain is served by the store with a valid certificate ([[settings-domains-ssl]]); a domain without one is served over plain http.

A company or shop network's web filter works the same way: its category for the domain (for example "Newly Observed Domain", common for a recently registered domain) is the filter vendor's, and the network's administrator can allow the domain. A certificate error such as NET::ERR_CERT_AUTHORITY_INVALID that appears only on one network, while other networks show the store's valid certificate, comes from that network's inspection of secure connections, not from the store (verify per network); its administrator fixes it.

## Related

- [[settings-domains]] — hub.
- [[settings-domains-dns-cloudflare]] — zones and the two connection methods.
- [[settings-domains-external-dns]] — CNAME mode and DNS kept elsewhere.
- [[platform-rate-limits]] — the limits behind the edge and what a merchant sees for each.
- [[settings-banned-ip]] — the store's own IP list for orders.
- [[apps-google-analytics]] — the merchant's own traffic measurement.

## Open questions

- The default edge rules per zone, including country blocks.
- Whether CloudCart support provides request-log extracts on request.
- The TLS settings in force at the edge: minimum version, cipher suites, HSTS, and whether they are set per zone or account-wide.
