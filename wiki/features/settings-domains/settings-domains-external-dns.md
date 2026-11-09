---
type: feature
nav_path: "Settings → Domains → DNS kept elsewhere"
route_name: domains.settings
route_path: /admin/settings/domains
aliases: ["Manage with CNAME", "Custom hostname", "CNAME record for my domain", "A record", "Static IP for domain", "Domain IP address", "Own Cloudflare account", "Move DNS away from CloudCart", "Change nameservers back", "Records copied on nameserver change", "DKIM lost after nameserver change"]
tags: [settings, domains, dns, cname, custom-hostname, nameservers]
plan_gates: ["custom_hostname"]
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[settings-domains]]. See the hub for related aspects (add flow, DNS / Cloudflare, SSL, primary, deletion, plan gates, edge).

# Domains — DNS kept elsewhere, moving DNS, and what carries over

## Purpose

How a domain reaches the store when its DNS is **not** on CloudCart's nameservers (**Manage with CNAME**), why there is no A-record or IP method, what CloudCart copies when nameservers move to CloudCart, and what happens when they move away again (another DNS host or the merchant's own Cloudflare).

## Where to find it

Settings → Domains → a row's **DNS Records** column: **Activate DNS Records** (the Activate Domain modal, [[settings-domains-dns-cloudflare]]), **Custom hostname** and **Manage DNS**.

## What the merchant can do here

- **Connect with CNAME:** **Manage with CNAME**, then one CNAME at their own DNS provider.
- **Move DNS to CloudCart:** **Enable DNS Record management**, then the nameserver change.
- **Move DNS away:** new nameservers, with the store kept reachable through the CNAME mode.

## Settings & fields

| Item | What it is |
|---|---|
| **CNAME name** | The domain exactly as it was added on this page (e.g. `shop.example.com` or `example.com`). |
| **CNAME target** | The store's own `*.cloudcart.net` address. The row's **Custom hostname** link opens *"Custom hostname management"*: *"Go to your domain registry (e.g. name.com), enter the domain management console and create a CNAME record pointing at your official CloudCart domain {domain}."*, {domain} being that address. |
| **CNAME slot** | Each CNAME-mode domain uses one `custom_hostname` slot — [[settings-domains-plan-gates]]. |

## Business rules

### Two ways to connect, no IP method

A custom domain is connected in exactly two ways: CloudCart's nameservers (a DNS zone in CloudCart's Cloudflare account, edited in **Manage DNS**) or **Manage with CNAME** (the domain attached as a custom hostname under CloudCart's own zone, DNS kept at the merchant's provider). There is **no A-record or static-IP method**: the admin shows no IP address, the old IP instructions were removed, and the store's own `*.cloudcart.net` address is itself an alias the platform repoints when it moves a store between hosting platforms. The IP list the Admin API returns for a domain is only what it resolved to when added.

### Manage with CNAME — what happens

1. **Manage with CNAME**: with a free slot the domain is attached at once; with none, the admin offers slots to buy, or a plan upgrade.
2. The domain becomes a custom hostname on CloudCart's zone, and CloudCart asks Cloudflare to issue its edge certificate by HTTP validation.
3. The merchant creates the CNAME at their DNS provider (name and target above).
4. A CloudCart certificate is still needed (**Install SSL**, [[settings-domains-ssl]]), and **Set as primary** still checks that the domain answers as CloudCart ([[settings-domains-primary]]).

- **Root domain:** a CNAME on the bare domain, next to its MX records, works only where the DNS provider offers a flattening or ALIAS-type record. That is the provider's rule, not CloudCart's.
- **The other form:** `example.com` and `www.example.com` are one domain on this page (the second cannot be added), and only the name that was added is attached at the edge (verify whether the other form is served in this mode).
- **Not for domains bought here:** the modal offers **Manage with CNAME** only for domains registered elsewhere.
- **A domain that already has a zone:** the CNAME activation neither checks for nor removes the zone; it stays in CloudCart's account with its records. The slot stays in use until the domain is removed. The other way round, **Manage DNS** on a store with CNAME slots first warns that switching needs CloudCart's nameservers ([[settings-domains-plan-gates]]).

### Moving nameservers to CloudCart — what is copied

The zone is created when the merchant clicks **Enable DNS Record management**, not when the domain is added. At that moment CloudCart:

- adds a proxied CNAME for the root pointing to the store's `*.cloudcart.net` address, and a proxied CNAME for `www` pointing to the root;
- copies the domain's current **MX** and **TXT** records **of the root name only** (SPF and verification TXTs included), and only while the domain is not yet on CloudCart's nameservers. It is a one-time snapshot;
- adds the Email channel's tracking CNAME when that channel is set up ([[email-channel-dns-records]]).

**Not copied:** anything on a subdomain (DKIM at `<selector>._domainkey`, DMARC at `_dmarc`, `mail`, `autodiscover` and other hosts, SRV) and the root's A, AAAA and CNAME records. Re-create them in **Manage DNS** before switching the nameservers, or mail authentication and those services stop when the switch takes effect. Later changes at the old DNS host are not copied either. Re-adding a domain whose zone still exists reuses that zone.

### Moving DNS away from CloudCart

- **Nothing is exported or deleted.** The CloudCart zone stays in CloudCart's account with its records; CloudCart's code never deletes such a zone, not when the domain is removed, not at plan expiry, not when the store is deleted. **Manage DNS** then edits only that unused zone.
- The row's DNS badge no longer reads **Active**, and **Set as primary** asks to fix the DNS first unless the store has CNAME slots.
- To keep the store reachable, attach the domain with **Manage with CNAME** and create the CNAME at the new DNS host. Without it CloudCart's edge has no active entry for the domain (verify).
- On the merchant's own Cloudflare account, whether that CNAME may be proxied and which SSL mode it needs are Cloudflare's rules for traffic between accounts, not CloudCart's.
- The certificate and primary checks request `http://<domain>/.well-known/acme-challenge/_selftest` (Let's Encrypt also tries the `www` form), follow no redirect and expect CloudCart's `x-powered-by: cloudcart.com` header. A proxy in front that redirects plain http to https, or drops that header, makes Let's Encrypt renewal and **Set as primary** fail.
- **Mail:** store notifications need no record, because they are sent From `noreply@cloudcart.com` ([[omnichannel-mails-customisation-limits]]). The Email channel's four records, tracking CNAME included, are added by hand ([[email-channel-dns-records]]). An outside mailbox's or the [[apps-smtp|SMTP app]]'s records go wherever the domain's DNS is hosted.

### After the plan expires

The zone keeps resolving: nothing in the platform removes or pauses it at plan expiry, and **Manage DNS** keeps saving, because the settings pages and their API stay reachable in the expired lock ([[expired-subscription-redirect]]). Let's Encrypt renewals stop for an expired store, and a staff-run command can deactivate its custom domains ([[settings-domains-ssl]]).

### CloudCart-purchased domains

Their nameservers are set to CloudCart's zone at purchase. The admin has no control to change them, unlock the domain or show its transfer (EPP) code, and **Manage with CNAME** is not offered for them. There is no inbound transfer either ([[settings-domains-add-flow]]).

## Related

- [[settings-domains]] — hub.
- [[settings-domains-dns-cloudflare]] — the two methods, Manage DNS, proxy rules.
- [[settings-domains-plan-gates]] — CNAME slots.
- [[settings-domains-primary]] — the header check.
- [[settings-domains-ssl]] — certificates and their renewal.
- [[email-channel-dns-records]] — the Email channel's records.

## Open questions

- Whether the edge serves the other form (www or root) of a CNAME-mode domain that was not added itself.
- Whether the edge serves a domain whose zone is no longer active and that has no custom hostname (the code offers no such path).
